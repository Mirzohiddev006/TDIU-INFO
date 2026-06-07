"""Operatorga yo'naltirish (MVP — oddiy bildirishnoma).

MVP bosqichida to'liq relay-chat yo'q. Foydalanuvchi «operatorga ulanish»ni
bosganda, so'rov admin/operator ID'lariga oddiy xabar sifatida yuboriladi.
Keyingi fazada (Faza 3) bu admin panel orqali to'liq jonli chatga aylantiriladi.
"""
from __future__ import annotations

from aiogram.types import CallbackQuery

from bot.config import load_config

_config = load_config()


def operator_intro_text() -> str:
    if _config.support_username:
        contact = f"\n\nTo'g'ridan-to'g'ri yozish: @{_config.support_username}"
    else:
        contact = ""
    return (
        "💬 <b>Operator bilan bog'lanish</b>\n\n"
        "So'rovingiz qabul qilindi. Operatorlar ish vaqtida siz bilan "
        "bog'lanishadi.\n\n"
        "🕘 Ish vaqtidan tashqari bo'lsa: savolingizni shu yerga yozib "
        "qoldiring — operator ko'rganda javob beradi." + contact
    )


async def notify_operator_request(callback: CallbackQuery) -> None:
    """So'rovni adminlarga/operatorlarga yuboradi."""
    if not _config.admin_ids:
        return
    user = callback.from_user
    username = f"@{user.username}" if user and user.username else "—"
    text = (
        "🔔 <b>Yangi operator so'rovi</b>\n\n"
        f"👤 Foydalanuvchi: {user.full_name if user else '—'}\n"
        f"🆔 ID: <code>{user.id if user else '—'}</code>\n"
        f"🔗 Username: {username}"
    )
    bot = callback.bot
    for admin_id in _config.admin_ids:
        try:
            await bot.send_message(admin_id, text)
        except Exception:
            # Admin botni bloklagan yoki ID noto'g'ri bo'lishi mumkin — e'tiborsiz
            continue
