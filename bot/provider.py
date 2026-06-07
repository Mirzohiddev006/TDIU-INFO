"""Kontent provayderi — bazadan o'qiydi, xato bo'lsa statik kontentga qaytadi.

Bu qatlam handlerlarni DB detallaridan ajratadi. Barcha funksiyalar statik
modullar bilan bir xil shaklda ma'lumot qaytaradi, shuning uchun klaviaturalar
va matn generatorlari o'zgarmaydi.
"""
from __future__ import annotations

import logging

from sqlalchemy import select

from core.database import async_session_factory
from core.models import (
    Admission, Analytics, Contract, Faculty, Faq, Program, Section, User,
)
from core.settings import CURRENT_YEAR

# Statik fallback
from bot.content import sections as S
from bot.content.programs import FACULTIES as STATIC_FACULTIES
from bot.content.faq import FAQ as STATIC_FAQ

logger = logging.getLogger("tdiu_bot.provider")


def _fmt_score(v) -> str:
    return f"{v}" if v is not None else "tez orada kiritiladi"


def _score_pair(uz, ru) -> str:
    parts = []
    if uz is not None:
        parts.append(f"O'zbek {uz}")
    if ru is not None:
        parts.append(f"Rus {ru}")
    return " | ".join(parts) if parts else "tez orada kiritiladi"


def _fmt_amount(v) -> str:
    if v is None:
        return "tez orada kiritiladi"
    return f"{v:,.0f} so'm".replace(",", " ")


def _fmt_places(v) -> str:
    return f"{v} ta" if v is not None else "—"


async def get_faculties() -> list[dict]:
    """[{id(slug), name, programs:[{id(slug),code,name,form,lang}]}]"""
    try:
        async with async_session_factory() as db:
            facs = list(await db.scalars(select(Faculty).order_by(Faculty.sort_order)))
            out = []
            for f in facs:
                progs = list(await db.scalars(
                    select(Program).where(Program.faculty_id == f.id).order_by(Program.sort_order)
                ))
                out.append({
                    "id": f.slug, "name": f.name,
                    "programs": [
                        {"id": p.slug, "code": p.code, "name": p.name,
                         "form": p.form, "lang": p.lang} for p in progs
                    ],
                })
            if out:
                return out
    except Exception as e:  # noqa: BLE001
        logger.warning("get_faculties DB xato, statik: %s", e)
    return STATIC_FACULTIES


async def get_faculty(slug: str) -> dict | None:
    for f in await get_faculties():
        if f["id"] == slug:
            return f
    return None


async def program_card(program_slug: str) -> str:
    try:
        async with async_session_factory() as db:
            p = await db.scalar(select(Program).where(Program.slug == program_slug))
            if p:
                a = await db.scalar(select(Admission).where(
                    Admission.program_id == p.id, Admission.year == CURRENT_YEAR))
                c = await db.scalar(select(Contract).where(
                    Contract.program_id == p.id, Contract.year == CURRENT_YEAR))
                pg = a.passing_grant if a else None
                pgr = a.passing_grant_ru if a else None
                pc = a.passing_contract if a else None
                pcr = a.passing_contract_ru if a else None
                amt = c.amount if c else None
                return (
                    f"🎓 <b>{p.name}</b>\n\n"
                    f"🔢 Kodi: <code>{p.code}</code>\n"
                    f"🕘 Ta'lim shakli: {p.form}\n"
                    f"🌐 O'qitish tili: {p.lang}\n\n"
                    f"📈 Grant o'tish bali: <b>{_score_pair(pg, pgr)}</b>\n"
                    f"📊 To'lov-kontrakt o'tish bali: <b>{_score_pair(pc, pcr)}</b>\n"
                    f"💰 Kontrakt summasi (bazaviy): <b>{_fmt_amount(amt)}</b>"
                )
    except Exception as e:  # noqa: BLE001
        logger.warning("program_card DB xato, statik: %s", e)
    return S.program_card(program_slug)


async def quota_text() -> str:
    try:
        async with async_session_factory() as db:
            facs = list(await db.scalars(select(Faculty).order_by(Faculty.sort_order)))
            lines, any_q = [f"📊 <b>Qabul kvotasi ({CURRENT_YEAR})</b>\n"], False
            for f in facs:
                progs = list(await db.scalars(
                    select(Program).where(Program.faculty_id == f.id).order_by(Program.sort_order)))
                rows = []
                for p in progs:
                    a = await db.scalar(select(Admission).where(
                        Admission.program_id == p.id, Admission.year == CURRENT_YEAR))
                    if a and (a.grant_places is not None or a.contract_places is not None):
                        any_q = True
                        rows.append(f"  • {p.name}: grant {_fmt_places(a.grant_places)}, "
                                    f"kontrakt {_fmt_places(a.contract_places)}")
                if rows:
                    lines.append(f"<b>{f.name}</b>"); lines.extend(rows); lines.append("")
            if any_q:
                return "\n".join(lines)
            return (
                f"📊 <b>Qabul kvotasi ({CURRENT_YEAR})</b>\n\n"
                "Joriy o'quv yili kvotasi hozircha kiritilmagan.\n\n"
                "🔔 Raqamlar e'lon qilinishi bilan shu yerda ko'rsatiladi."
            )
    except Exception as e:  # noqa: BLE001
        logger.warning("quota_text DB xato, statik: %s", e)
    return S.quota_text()


async def contract_text() -> str:
    try:
        async with async_session_factory() as db:
            facs = list(await db.scalars(select(Faculty).order_by(Faculty.sort_order)))
            lines, any_a = [f"💰 <b>Kontrakt summalari — bazaviy ({CURRENT_YEAR})</b>\n"], False
            for f in facs:
                progs = list(await db.scalars(
                    select(Program).where(Program.faculty_id == f.id).order_by(Program.sort_order)))
                rows = []
                for p in progs:
                    c = await db.scalar(select(Contract).where(
                        Contract.program_id == p.id, Contract.year == CURRENT_YEAR))
                    if c and c.amount is not None:
                        any_a = True
                        rows.append(f"  • {p.name}: {_fmt_amount(c.amount)}")
                if rows:
                    lines.append(f"<b>{f.name}</b>"); lines.extend(rows); lines.append("")
            if any_a:
                return "\n".join(lines)
            return (
                f"💰 <b>Kontrakt summalari ({CURRENT_YEAR})</b>\n\n"
                "Joriy o'quv yili summalari hozircha kiritilmagan.\n\n"
                "🔔 Rasmiy summalar e'lon qilinishi bilan shu yerda ko'rsatiladi."
            )
    except Exception as e:  # noqa: BLE001
        logger.warning("contract_text DB xato, statik: %s", e)
    return S.contract_text()


async def get_section(key: str) -> str | None:
    try:
        async with async_session_factory() as db:
            sec = await db.scalar(select(Section).where(Section.key == key))
            if sec:
                return sec.body
    except Exception as e:  # noqa: BLE001
        logger.warning("get_section DB xato, statik: %s", e)
    return S.TEXTS.get(key)


async def get_faq() -> list[dict]:
    try:
        async with async_session_factory() as db:
            rows = list(await db.scalars(select(Faq).order_by(Faq.sort_order)))
            if rows:
                return [{"id": r.id, "question": r.question, "answer": r.answer,
                         "keywords": (r.keywords or "").split(",")} for r in rows]
    except Exception as e:  # noqa: BLE001
        logger.warning("get_faq DB xato, statik: %s", e)
    return STATIC_FAQ


async def search_faq(text: str, limit: int = 3) -> list[dict]:
    items = await get_faq()
    low = text.lower()
    scored = []
    for it in items:
        score = sum(1 for kw in it.get("keywords", []) if kw and kw.strip() and kw.strip() in low)
        if score:
            scored.append((score, it))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [it for _, it in scored[:limit]]


async def ensure_user(tg_id: int, name: str | None, username: str | None) -> None:
    try:
        async with async_session_factory() as db:
            u = await db.scalar(select(User).where(User.telegram_id == tg_id))
            if u is None:
                db.add(User(telegram_id=tg_id, name=name, username=username))
                await db.commit()
    except Exception as e:  # noqa: BLE001
        logger.warning("ensure_user DB xato: %s", e)


async def log_action(user_id: int | None, action: str, section: str | None = None) -> None:
    try:
        async with async_session_factory() as db:
            db.add(Analytics(user_id=user_id, action=action, section=section))
            await db.commit()
    except Exception as e:  # noqa: BLE001
        logger.warning("log_action DB xato: %s", e)
