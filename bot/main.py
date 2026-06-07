"""TDIU Info Bot — ishga tushirish nuqtasi (long polling + keep-alive).

Ishga tushganda DB jadvallarini yaratadi va bo'sh bo'lsa statik kontent bilan
to'ldiradi (seed). Render.com uchun health-server va self-ping keep-alive ham
ishga tushadi (uyqudan saqlash uchun).
"""
from __future__ import annotations

import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from sqlalchemy import select

from bot.config import load_config
from bot.handlers import get_router
from bot.middlewares.subscription import SubscriptionMiddleware
from bot.webserver import keepalive_loop, start_webserver
from core.database import async_session_factory, init_db
from core.models import Faculty
from core.seed import seed

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger("tdiu_bot")


async def _ensure_seeded() -> None:
    await init_db()
    async with async_session_factory() as db:
        has = await db.scalar(select(Faculty).limit(1))
    if has is None:
        logger.info("DB bo'sh — statik kontent bilan to'ldirilmoqda (seed)...")
        await seed()


async def main() -> None:
    config = load_config()
    await _ensure_seeded()

    bot = Bot(
        token=config.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()
    dp.message.outer_middleware(SubscriptionMiddleware())
    dp.callback_query.outer_middleware(SubscriptionMiddleware())
    dp.include_router(get_router())

    # Health-server (Render port talabi) + keep-alive self-ping
    await start_webserver()
    asyncio.create_task(keepalive_loop())

    logger.info("Bot ishga tushdi (long polling).")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot to'xtatildi.")
