"""TDIU — Admin API + Telegram bot bitta servisda (Render bepul tarif uchun).

  • admin panel uchun REST API (/api/...),
  • lifespan ichida aiogram botni (long polling) fon vazifasi sifatida ishga tushiradi,
  • /health (keep-alive) va /docs (Swagger) beradi.

Render'da bitta web servis: uvicorn backend.app.main:app
BOT_TOKEN berilmasa, bot ishga tushmaydi (faqat API ishlaydi).
"""
from __future__ import annotations

import asyncio
import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.seed import ensure_seeded

from backend.app.routers import admission, auth, broadcast, content, operator, stats

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger("tdiu_app")

_bot = None
_bot_task = None


async def _run_bot() -> None:
    """Botni long polling rejimida ishga tushiradi (fon vazifasi)."""
    global _bot
    token = os.getenv("BOT_TOKEN", "").strip()
    if not token:
        logger.warning("BOT_TOKEN yo'q — bot ishga tushmaydi (faqat API).")
        return
    from aiogram import Bot, Dispatcher
    from aiogram.client.default import DefaultBotProperties
    from aiogram.enums import ParseMode

    from bot.handlers import get_router
    from bot.middlewares.subscription import SubscriptionMiddleware

    _bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    dp.message.outer_middleware(SubscriptionMiddleware())
    dp.callback_query.outer_middleware(SubscriptionMiddleware())
    dp.include_router(get_router())
    app.state.bot = _bot
    try:
        await _bot.delete_webhook(drop_pending_updates=True)
        logger.info("Bot ishga tushdi (long polling, combined servis).")
        await dp.start_polling(_bot)
    except asyncio.CancelledError:
        raise
    except Exception as e:  # noqa: BLE001
        logger.error("Bot polling xatosi: %s", e)


async def _keepalive() -> None:
    url = os.getenv("KEEPALIVE_URL") or os.getenv("RENDER_EXTERNAL_URL")
    minutes = int(os.getenv("KEEPALIVE_MINUTES", "14"))
    if not url:
        return
    from aiohttp import ClientSession, ClientTimeout
    ping = url.rstrip("/") + "/health"
    await asyncio.sleep(60)
    async with ClientSession(timeout=ClientTimeout(total=30)) as s:
        while True:
            try:
                async with s.get(ping) as r:
                    logger.info("keep-alive: %s", r.status)
            except Exception as e:  # noqa: BLE001
                logger.warning("keep-alive xato: %s", e)
            await asyncio.sleep(minutes * 60)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await ensure_seeded()
    global _bot_task
    _bot_task = asyncio.create_task(_run_bot())
    asyncio.create_task(_keepalive())
    yield
    if _bot_task:
        _bot_task.cancel()
    if _bot:
        await _bot.session.close()


app = FastAPI(
    title="TDIU Info Bot — Admin API",
    version="2.0",
    description=(
        "TDIU admin panel uchun REST API.\n\n"
        "Kirish: POST /api/auth/login (admin / admin123) -> access_token. "
        "So'ng yuqoridagi 'Authorize' tugmasiga tokenni qo'ying."
    ),
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)
app.state.bot = None

# Token (Bearer) bilan ishlaymiz — cookie ishlatmaymiz, shuning uchun credentials=False.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(content.router)
app.include_router(admission.router)
app.include_router(stats.router)
app.include_router(broadcast.router)
app.include_router(operator.router)


@app.get("/", include_in_schema=False)
async def root():
    return {
        "service": "TDIU Info Bot — Admin API",
        "status": "ok",
        "docs": "/docs",
        "health": "/api/health",
    }


@app.get("/api/health")
async def health():
    return {"status": "ok"}


@app.get("/health")
async def health_root():
    return {"status": "ok"}
