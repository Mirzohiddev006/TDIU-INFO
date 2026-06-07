"""Inline klaviaturalar — asosiy menyu, bo'limlar, orqaga qaytish.

Fakultet/yo'nalish ma'lumotlari handlerdan (provider orqali) uzatiladi.
"""
from __future__ import annotations

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.content.sections import MENU

SECTION = "sec"      # sec:<key>
FACULTY = "fac"      # fac:<faculty_slug>
PROGRAM = "prog"     # prog:<program_slug>
FAQ_ITEM = "faq"     # faq:<id>
MAIN = "main"
OPERATOR = "op"      # op:start


def main_menu() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for key, title in MENU.items():
        kb.button(text=title, callback_data=f"{SECTION}:{key}")
    kb.adjust(2)
    return kb.as_markup()


def back_to_main() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="⬅️ Asosiy menyu", callback_data=MAIN)
    return kb.as_markup()


def faculties_menu(faculties: list[dict]) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for fac in faculties:
        kb.button(text=fac["name"], callback_data=f"{FACULTY}:{fac['id']}")
    kb.button(text="⬅️ Asosiy menyu", callback_data=MAIN)
    kb.adjust(1)
    return kb.as_markup()


def programs_menu(faculty: dict) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for prog in faculty.get("programs", []):
        kb.button(text=prog["name"], callback_data=f"{PROGRAM}:{prog['id']}")
    kb.button(text="⬅️ Fakultetlar", callback_data=f"{SECTION}:faculties")
    kb.button(text="🏠 Asosiy menyu", callback_data=MAIN)
    kb.adjust(1)
    return kb.as_markup()


def program_card_menu(faculty_slug: str | None) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    if faculty_slug:
        kb.button(text="⬅️ Yo'nalishlar", callback_data=f"{FACULTY}:{faculty_slug}")
    kb.button(text="🏠 Asosiy menyu", callback_data=MAIN)
    kb.adjust(1)
    return kb.as_markup()


def faq_menu(faq_items: list[dict]) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for item in faq_items:
        kb.button(text=item["question"], callback_data=f"{FAQ_ITEM}:{item['id']}")
    kb.button(text="🏠 Asosiy menyu", callback_data=MAIN)
    kb.adjust(1)
    return kb.as_markup()


def faq_answer_menu() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="⬅️ FAQ ro'yxati", callback_data=f"{SECTION}:faq")
    kb.button(text="💬 Operatorga yozish", callback_data=f"{OPERATOR}:start")
    kb.button(text="🏠 Asosiy menyu", callback_data=MAIN)
    kb.adjust(1)
    return kb.as_markup()


def operator_menu() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="💬 Operatorga ulanish", callback_data=f"{OPERATOR}:start")
    kb.button(text="🏠 Asosiy menyu", callback_data=MAIN)
    kb.adjust(1)
    return kb.as_markup()


def operator_session_menu() -> InlineKeyboardMarkup:
    """Operator sessiyasi: suhbatni yakunlash + asosiy menyu."""
    kb = InlineKeyboardBuilder()
    kb.button(text="❌ Suhbatni yakunlash", callback_data=f"{OPERATOR}:end")
    kb.button(text="🏠 Asosiy menyu", callback_data=MAIN)
    kb.adjust(1)
    return kb.as_markup()
