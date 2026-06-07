"""Health-server + keep-alive (Render.com bepul tarif uchun).

Render bepul Web Service 15 daqiqa harakatsizlikdan so'ng uyquga ketadi.
Ikki narsa kerak:
  1) HTTP port'ga bog'lanish (Render uni talab qiladi) — health-server.
  2) Har ~14 daqiqada o'z URL'iga ping — uyquni oldini oladi (self-ping).

KEEPALIVE_URL yoki Render avtomatik beradigan RENDER_EXTERNAL_URL ishlatiladi.
"""
from __future__ import annotations

import asyncio
import logging
import os

from aiohttp import ClientSession, ClientTimeout, web

logger = logging.getLogger("tdiu_bot.keepalive")


async def _health(_request: web.Request) -> web.Response:
    return web.json_response({"status": "ok", "service": "tdiu-info-bot"})


async def start_webserver() -> web.AppRunner:
    """Health-serverni $PORT da ishga tushiradi (Render uchun zarur)."""
    app = web.Application()
    app.router.add_get("/", _health)
    app.router.add_get("/health", _health)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.getenv("PORT", "8080"))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    logger.info("Health-server ishga tushdi: 0.0.0.0:%s", port)
    return runner


async def keepalive_loop() -> None:
    """Har KEEPALIVE_MINUTES daqiqada o'z URL'iga GET yuboradi."""
    url = os.getenv("KEEPALIVE_URL") or os.getenv("RENDER_EXTERNAL_URL")
    minutes = int(os.getenv("KEEPALIVE_MINUTES", "14"))
    if not url:
        logger.info("KEEPALIVE_URL/RENDER_EXTERNAL_URL yo'q — self-ping o'chirilgan.")
        return
    ping_url = url.rstrip("/") + "/health"
    logger.info("Keep-alive yoqildi: har %s daqiqada %s", minutes, ping_url)
    await asyncio.sleep(60)  # server to'liq ko'tarilishini kutamiz
    timeout = ClientTimeout(total=30)
    async with ClientSession(timeout=timeout) as session:
        while True:
            try:
                async with session.get(ping_url) as resp:
                    logger.info("Keep-alive ping: %s", resp.status)
            except Exception as e:  # noqa: BLE001
                logger.warning("Keep-alive ping xato: %s", e)
            await asyncio.sleep(minutes * 60)
