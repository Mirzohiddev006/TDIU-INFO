"""Majburiy kanal obunasi — botdan foydalanish uchun kanallarga a'zo bo'lish shart.

DIQQAT: getChatMember ishlashi uchun bot HAR BIR kanalda ADMIN bo'lishi kerak.
Aks holda obunani tekshirib bo'lmaydi (bot a'zolikni ko'ra olmaydi).
"""
from __future__ import annotations

import logging
import os

from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

logger = logging.getLogger("tdiu_bot.subscription")

# Majburiy obuna kanallari
REQUIRED_CHANNELS = [
    {"name": "TSUE-TDIU", "username": "tsueuzofficial", "url": "https://t.me/tsueuzofficial"},
    {"name": "TDIU | Yoshlar kanali", "username": "tdiu_official", "url": "https://t.me/tdiu_official"},
]

# A'zo deb hisoblanadigan statuslar
_SUBSCRIBED = {"creator", "administrator", "member"}

GATE_TEXT = (
    "🔒 <b>Botdan foydalanish uchun rasmiy kanallarga obuna bo'ling</b>\n\n"
    "Quyidagi kanallarga a'zo bo'ling, so'ng «✅ Obunani tekshirish» tugmasini bosing 👇"
)


def is_enabled() -> bool:
    """Obuna tekshiruvi yoqilganmi (env: SUBSCRIPTION_CHECK=false bilan o'chiriladi)."""
    return os.getenv("SUBSCRIPTION_CHECK", "true").strip().lower() not in {"false", "0", "no"}


async def unsubscribed_channels(bot: Bot, user_id: int) -> list[dict]:
    """Foydalanuvchi a'zo BO'LMAGAN kanallar ro'yxatini qaytaradi."""
    missing: list[dict] = []
    for ch in REQUIRED_CHANNELS:
        try:
            member = await bot.get_chat_member(f"@{ch['username']}", user_id)
            if member.status not in _SUBSCRIBED:
                missing.append(ch)
        except Exception as e:  # noqa: BLE001
            # Bot kanalda admin emas yoki kanal topilmadi — xavfsiz tomoni: obuna talab qilamiz
            logger.warning("Obunani tekshirib bo'lmadi (%s): %s", ch["username"], e)
            missing.append(ch)
    return missing


def subscribe_keyboard(channels: list[dict] | None = None) -> InlineKeyboardMarkup:
    chans = channels if channels is not None else REQUIRED_CHANNELS
    kb = InlineKeyboardBuilder()
    for ch in chans:
        kb.button(text=f"📢 {ch['name']}", url=ch["url"])
    kb.button(text="✅ Obunani tekshirish", callback_data="check_sub")
    kb.adjust(1)
    return kb.as_markup()
