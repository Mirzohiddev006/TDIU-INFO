"""Obuna middleware — a'zo bo'lmagan foydalanuvchini handlergacha o'tkazmaydi."""
from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message, TelegramObject

from bot.services.subscription import (
    GATE_TEXT,
    is_enabled,
    subscribe_keyboard,
    unsubscribed_channels,
)


class SubscriptionMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        if not is_enabled():
            return await handler(event, data)

        user = data.get("event_from_user")
        bot = data.get("bot")
        if user is None or bot is None:
            return await handler(event, data)

        # «Obunani tekshirish» tugmasi har doim o'tadi (handlerda qayta tekshiriladi)
        if isinstance(event, CallbackQuery) and event.data == "check_sub":
            return await handler(event, data)

        missing = await unsubscribed_channels(bot, user.id)
        if not missing:
            return await handler(event, data)

        # A'zo emas — obuna oynasini ko'rsatamiz, handler chaqirilmaydi
        if isinstance(event, Message):
            await event.answer(GATE_TEXT, reply_markup=subscribe_keyboard(missing))
        elif isinstance(event, CallbackQuery):
            await event.answer("Avval kanallarga obuna bo'ling ❗", show_alert=True)
            if event.message:
                await event.message.answer(GATE_TEXT, reply_markup=subscribe_keyboard(missing))
        return None
