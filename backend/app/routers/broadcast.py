"""Ommaviy xabar (broadcast) — barcha bot foydalanuvchilariga (Faza 4).

Matn, rasm yoki fayl yuborish mumkin:
  - faqat matn               -> send_message
  - rasm (+ ixtiyoriy matn)  -> send_photo (matn = caption)
  - boshqa fayl (+ matn)     -> send_document (matn = caption)
Telegram caption limiti 1024 belgidan oshsa, fayl alohida, matn alohida ketadi.
"""
from __future__ import annotations

import asyncio

from fastapi import APIRouter, Depends, File, Form, HTTPException, Request, UploadFile
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_session
from core.models import User

from backend.app.deps import can_edit

router = APIRouter(prefix="/api/broadcast", tags=["broadcast"])

CAPTION_LIMIT = 1024
MAX_FILE_MB = 20


class BroadcastResult(BaseModel):
    total: int
    sent: int
    failed: int


@router.post("", response_model=BroadcastResult, dependencies=[Depends(can_edit)])
async def send_broadcast(
    request: Request,
    text: str = Form(""),
    file: UploadFile | None = File(None),
    db: AsyncSession = Depends(get_session),
):
    bot = getattr(request.app.state, "bot", None)
    if bot is None:
        raise HTTPException(503, "Bot ishlamayapti (BOT_TOKEN sozlanmagan).")

    text = (text or "").strip()
    content = None
    filename = ""
    is_image = False
    if file is not None and file.filename:
        content = await file.read()
        if len(content) > MAX_FILE_MB * 1024 * 1024:
            raise HTTPException(413, f"Fayl juda katta (maksimum {MAX_FILE_MB}MB).")
        filename = file.filename
        is_image = (file.content_type or "").startswith("image/")

    if not text and content is None:
        raise HTTPException(400, "Xabar matni yoki fayl kerak.")

    from aiogram.types import BufferedInputFile

    caption = text if (text and len(text) <= CAPTION_LIMIT) else ""
    extra_text = text if (text and len(text) > CAPTION_LIMIT) else ""

    ids = list(await db.scalars(select(User.telegram_id)))
    sent = failed = 0
    for i, tg_id in enumerate(ids):
        try:
            if content is not None:
                media = BufferedInputFile(content, filename=filename)
                if is_image:
                    await bot.send_photo(tg_id, media, caption=caption or None)
                else:
                    await bot.send_document(tg_id, media, caption=caption or None)
                if extra_text:
                    await bot.send_message(tg_id, extra_text)
            else:
                await bot.send_message(tg_id, text)
            sent += 1
        except Exception:
            failed += 1
        if (i + 1) % 25 == 0:
            await asyncio.sleep(1)
    return BroadcastResult(total=len(ids), sent=sent, failed=failed)
