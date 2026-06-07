"""Menyu bo'limlari, fakultet/yo'nalishlar, FAQ va operator callback'lari."""
from __future__ import annotations

from aiogram import F, Router
from aiogram.types import CallbackQuery

from bot import provider as P
from bot.content.sections import MENU
from bot.keyboards.menu import (
    FACULTY, FAQ_ITEM, OPERATOR, PROGRAM, SECTION,
    back_to_main, faculties_menu, faq_answer_menu, faq_menu,
    operator_session_menu, program_card_menu, programs_menu,
)
from bot.services.operator import close_chat, notify_operator_request, operator_intro_text

router = Router()


async def _edit(callback: CallbackQuery, text: str, markup) -> None:
    if callback.message:
        await callback.message.edit_text(text, reply_markup=markup)
    await callback.answer()


@router.callback_query(F.data.startswith(f"{SECTION}:"))
async def open_section(callback: CallbackQuery) -> None:
    key = callback.data.split(":", 1)[1]
    await P.log_action(callback.from_user.id if callback.from_user else None, "open_section", key)

    if key == "faculties":
        facs = await P.get_faculties()
        await _edit(
            callback,
            "🎓 <b>Fakultet va yo'nalishlar</b>\n\nQuyidagi fakultetlardan birini tanlang:",
            faculties_menu(facs),
        )
        return

    if key == "quota":
        await _edit(callback, await P.quota_text(), back_to_main())
        return

    if key == "contract":
        await _edit(callback, await P.contract_text(), back_to_main())
        return

    if key == "faq":
        faq = await P.get_faq()
        await _edit(
            callback,
            "❓ <b>Tez-tez so'raladigan savollar</b>\n\nSavolni tanlang yoki "
            "savolingizni shunchaki yozib yuboring:",
            faq_menu(faq),
        )
        return

    if key == "operator":
        await _edit(callback, operator_intro_text(), operator_session_menu())
        await notify_operator_request(callback)
        return

    text = await P.get_section(key)
    if text is None:
        text = f"{MENU.get(key, 'Bo''lim')}\n\n<i>Kontent tez orada qo'shiladi.</i>"
    await _edit(callback, text, back_to_main())


@router.callback_query(F.data.startswith(f"{FACULTY}:"))
async def open_faculty(callback: CallbackQuery) -> None:
    slug = callback.data.split(":", 1)[1]
    fac = await P.get_faculty(slug)
    if not fac:
        await callback.answer("Fakultet topilmadi", show_alert=True)
        return
    await _edit(callback, f"🎓 <b>{fac['name']}</b>\n\nYo'nalishni tanlang:", programs_menu(fac))


@router.callback_query(F.data.startswith(f"{PROGRAM}:"))
async def open_program(callback: CallbackQuery) -> None:
    slug = callback.data.split(":", 1)[1]
    await P.log_action(callback.from_user.id if callback.from_user else None, "open_program", slug)
    facs = await P.get_faculties()
    faculty_slug = next(
        (f["id"] for f in facs if any(p["id"] == slug for p in f["programs"])), None
    )
    card = await P.program_card(slug)
    await _edit(callback, card, program_card_menu(faculty_slug))


@router.callback_query(F.data.startswith(f"{FAQ_ITEM}:"))
async def open_faq_item(callback: CallbackQuery) -> None:
    faq_id_raw = callback.data.split(":", 1)[1]
    faq = await P.get_faq()
    item = next((q for q in faq if str(q["id"]) == faq_id_raw), None)
    if not item:
        await callback.answer("Savol topilmadi", show_alert=True)
        return
    await _edit(callback, f"❓ <b>{item['question']}</b>\n\n{item['answer']}", faq_answer_menu())


@router.callback_query(F.data == f"{OPERATOR}:start")
async def connect_operator(callback: CallbackQuery) -> None:
    await P.log_action(callback.from_user.id if callback.from_user else None, "operator")
    await _edit(callback, operator_intro_text(), operator_session_menu())
    await notify_operator_request(callback)


@router.callback_query(F.data == f"{OPERATOR}:end")
async def end_operator(callback: CallbackQuery) -> None:
    if callback.from_user:
        await close_chat(callback.from_user.id)
    await callback.answer("Suhbat yakunlandi ✅")
    if callback.message:
        from bot.content.sections import WELCOME
        from bot.keyboards.menu import main_menu
        await callback.message.edit_text(WELCOME, reply_markup=main_menu())
