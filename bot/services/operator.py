"""Operator jonli yordam (Faza 3) — DB orqali relay.

Foydalanuvchi «operatorga ulanish» bosganda OperatorChat (open) ochiladi.
Shundan keyin foydalanuvchining matnli xabarlari shu chatga yoziladi va
adminlarga bildiriladi. Operator admin paneldan javob beradi (relay).
"""
from __future__ import annotations

import logging

from aiogram.types import CallbackQuery
from sqlalchemy import select

from core.database import async_session_factory
from core.models import Message, OperatorChat

from bot.config import load_config

logger = logging.getLogger("tdiu_bot.operator")
_config = load_config()


def operator_intro_text() -> str:
    contact = f"\n\nTo'g'ridan-to'g'ri: @{_config.support_username}" if _config.support_username else ""
    return (
        "💬 <b>Operator bilan bog'lanish</b>\n\n"
        "So'rovingiz qabul qilindi. Endi shu yerga savolingizni <b>matn ko'rinishida</b> "
        "yozsangiz, operatorga yetkaziladi va u sizga shu bot orqali javob beradi.\n\n"
        "🕘 Ish vaqtidan tashqari javob biroz kechikishi mumkin." + contact
    )


async def get_open_chat_id(user_id: int) -> int | None:
    try:
        async with async_session_factory() as db:
            chat = await db.scalar(
                select(OperatorChat).where(
                    OperatorChat.user_id == user_id, OperatorChat.status == "open"
                )
            )
            return chat.id if chat else None
    except Exception as e:  # noqa: BLE001
        logger.warning("get_open_chat_id xato: %s", e)
        return None


async def open_chat(user_id: int) -> int | None:
    """Ochiq chat bo'lmasa yangi ochadi, bor bo'lsa o'shani qaytaradi."""
    try:
        async with async_session_factory() as db:
            chat = await db.scalar(
                select(OperatorChat).where(
                    OperatorChat.user_id == user_id, OperatorChat.status == "open"
                )
            )
            if chat is None:
                chat = OperatorChat(user_id=user_id, status="open")
                db.add(chat)
                await db.commit()
                await db.refresh(chat)
            return chat.id
    except Exception as e:  # noqa: BLE001
        logger.warning("open_chat xato: %s", e)
        return None


async def add_user_message(chat_id: int, text: str) -> None:
    try:
        async with async_session_factory() as db:
            db.add(Message(chat_id=chat_id, sender="user", text=text))
            await db.commit()
    except Exception as e:  # noqa: BLE001
        logger.warning("add_user_message xato: %s", e)


async def close_chat(user_id: int) -> bool:
    try:
        async with async_session_factory() as db:
            chat = await db.scalar(
                select(OperatorChat).where(
                    OperatorChat.user_id == user_id, OperatorChat.status == "open"
                )
            )
            if chat:
                chat.status = "closed"
                await db.commit()
                return True
    except Exception as e:  # noqa: BLE001
        logger.warning("close_chat xato: %s", e)
    return False


async def notify_operator_request(callback: CallbackQuery) -> None:
    """Yangi operator so'rovini adminlarga yuboradi."""
    user = callback.from_user
    await open_chat(user.id)
    if not _config.admin_ids:
        return
    username = f"@{user.username}" if user and user.username else "—"
    text = (
        "🔔 <b>Yangi operator so'rovi</b>\n\n"
        f"👤 {user.full_name if user else '—'}\n"
        f"🆔 <code>{user.id if user else '—'}</code>\n"
        f"🔗 {username}\n\n"
        "Admin panel → Operator bo'limida javob bering."
    )
    for admin_id in _config.admin_ids:
        try:
            await callback.bot.send_message(admin_id, text)
        except Exception:  # noqa: BLE001
            continue


async def relay_user_message(bot, user, text: str) -> bool:
    """Foydalanuvchi matnini ochiq operator chatiga yozadi. True = relay qilindi."""
    chat_id = await get_open_chat_id(user.id)
    if chat_id is None:
        return False
    await add_user_message(chat_id, text)
    # adminlarga xabar (ixtiyoriy)
    for admin_id in _config.admin_ids:
        try:
            uname = f"@{user.username}" if user.username else user.full_name
            await bot.send_message(
                admin_id, f"💬 <b>{uname}</b> (operatorga):\n{text}"
            )
        except Exception:  # noqa: BLE001
            continue
    return True
