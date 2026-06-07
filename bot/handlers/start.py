"""/start va asosiy menyuga qaytish."""
from __future__ import annotations

from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, Message

from bot import provider as P
from bot.content.sections import WELCOME
from bot.keyboards.menu import MAIN, main_menu
from bot.services.subscription import unsubscribed_channels, subscribe_keyboard, GATE_TEXT

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    u = message.from_user
    if u:
        await P.ensure_user(u.id, u.full_name, u.username)
        await P.log_action(u.id, "start")
    await message.answer(WELCOME, reply_markup=main_menu())


@router.callback_query(F.data == MAIN)
async def back_to_main(callback: CallbackQuery) -> None:
    if callback.message:
        await callback.message.edit_text(WELCOME, reply_markup=main_menu())
    await callback.answer()


@router.callback_query(F.data == "check_sub")
async def check_subscription(callback: CallbackQuery) -> None:
    missing = await unsubscribed_channels(callback.bot, callback.from_user.id)
    if missing:
        await callback.answer(
            "Siz hali barcha kanallarga obuna bo'lmadingiz ❗", show_alert=True
        )
        return
    if callback.message:
        await callback.message.edit_text(WELCOME, reply_markup=main_menu())
    await callback.answer("Rahmat! Endi botdan to'liq foydalanishingiz mumkin ✅")
