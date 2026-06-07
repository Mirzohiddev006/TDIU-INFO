"""Erkin matnli savol — avval operator relay, keyin FAQ qidiruv."""
from __future__ import annotations

from aiogram import F, Router
from aiogram.types import Message

from bot import provider as P
from bot.keyboards.menu import faq_menu, operator_menu
from bot.services.operator import relay_user_message

router = Router()


@router.message(F.text & ~F.text.startswith("/"))
async def handle_text(message: Message) -> None:
    query = message.text or ""
    user = message.from_user
    uid = user.id if user else None

    # 1) Agar foydalanuvchining ochiq operator chati bo'lsa — operatorga yetkazamiz
    if user and await relay_user_message(message.bot, user, query):
        await message.answer("✅ Xabaringiz operatorga yuborildi. Javobni shu yerda kuting.")
        return

    # 2) FAQ qidiruv
    matches = await P.search_faq(query)
    if matches:
        await P.log_action(uid, "search", "faq_hit")
        best = matches[0]
        text = f"❓ <b>{best['question']}</b>\n\n{best['answer']}"
        if len(matches) > 1:
            text += "\n\n📌 Boshqa o'xshash savollar quyida:"
            await message.answer(text, reply_markup=faq_menu(matches[1:]))
        else:
            await message.answer(text, reply_markup=operator_menu())
        return

    await P.log_action(uid, "unanswered", query[:64])
    await message.answer(
        "🤔 Afsus, savolingizga aniq javob topa olmadim.\n\n"
        "Quyidagi menyudan kerakli bo'limni tanlang yoki operatorga ulaning:",
        reply_markup=operator_menu(),
    )
