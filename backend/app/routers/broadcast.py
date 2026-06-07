"""Ommaviy xabar (broadcast) — barcha bot foydalanuvchilariga (Faza 4)."""
from __future__ import annotations

import asyncio

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_session
from core.models import User

from backend.app.deps import can_edit

router = APIRouter(prefix="/api/broadcast", tags=["broadcast"])


class BroadcastIn(BaseModel):
    text: str


class BroadcastResult(BaseModel):
    total: int
    sent: int
    failed: int


@router.post("", response_model=BroadcastResult, dependencies=[Depends(can_edit)])
async def send_broadcast(
    data: BroadcastIn, request: Request, db: AsyncSession = Depends(get_session)
):
    bot = getattr(request.app.state, "bot", None)
    if bot is None:
        raise HTTPException(503, "Bot ishlamayapti (BOT_TOKEN sozlanmagan).")
    if not data.text.strip():
        raise HTTPException(400, "Xabar matni bo'sh.")

    ids = list(await db.scalars(select(User.telegram_id)))
    sent = failed = 0
    for i, tg_id in enumerate(ids):
        try:
            await bot.send_message(tg_id, data.text)
            sent += 1
        except Exception:  # noqa: BLE001
            failed += 1
        # Telegram limit: ~30 msg/sek — har 25 ta xabardan keyin biroz kutamiz
        if (i + 1) % 25 == 0:
            await asyncio.sleep(1)
    return BroadcastResult(total=len(ids), sent=sent, failed=failed)
