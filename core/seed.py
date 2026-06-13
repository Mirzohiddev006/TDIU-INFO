"""Statik kontentni (bot.content) bazaga ko'chiradi va majburiy moslaydi.

- seed(): baza bo'sh bo'lsa boshlang'ich to'ldirish (idempotent).
- sync_static_content(): har startupda fakultet-yo'nalish TARKIBI va bo'lim
  MATNLARINI koddagi holatga MAJBURIY moslaydi (kod o'zgarsa botda darhol aks etadi).
  Admin kiritgan BALLAR/kvota/kontrakt (Admission/Contract) saqlanadi — ular faqat
  yo'q bo'lsa qo'shiladi, ustiga yozilmaydi.
"""
from __future__ import annotations

import asyncio

from sqlalchemy import select

from core.database import async_session_factory, init_db
from core.models import (
    AdminUser,
    Admission,
    Contract,
    Faculty,
    Faq,
    Program,
    Section,
)
from core.security import hash_password
from core.settings import ADMIN_PASSWORD, ADMIN_USERNAME, CURRENT_YEAR

from bot.content.programs import FACULTIES
from bot.content.faq import FAQ
from bot.content import sections as S
from bot.content import admission_data as AD


# Admin panel foydalanuvchilari: (username, parol, rol).
ADMIN_USERS = [
    (ADMIN_USERNAME, ADMIN_PASSWORD, "super"),
    ("menejer", "menejer123", "content"),
    ("operator", "operator123", "operator"),
]


async def _ensure_admission_contract(db, program) -> None:
    """Admission/Contract qatorlarini faqat YO'Q bo'lsa qo'shadi (ballarni saqlash uchun)."""
    a = await db.scalar(
        select(Admission).where(Admission.program_id == program.id, Admission.year == CURRENT_YEAR)
    )
    if a is None:
        d = AD.get(program.slug)
        db.add(Admission(
            program_id=program.id, year=CURRENT_YEAR,
            grant_places=d["grant_places"], contract_places=d["contract_places"],
            passing_grant=d["passing_grant"], passing_grant_ru=d.get("passing_grant_ru"),
            passing_contract=d["passing_contract"], passing_contract_ru=d.get("passing_contract_ru"),
        ))
    c = await db.scalar(
        select(Contract).where(Contract.program_id == program.id, Contract.year == CURRENT_YEAR)
    )
    if c is None:
        d = AD.get(program.slug)
        db.add(Contract(program_id=program.id, year=CURRENT_YEAR,
                        form=program["form"] if isinstance(program, dict) else program.form,
                        amount=d["contract_amount"]))


async def sync_static_content() -> None:
    """Fakultet-yo'nalish tarkibi va bo'lim matnlarini koddan bazaga majburiy moslaydi."""
    await init_db()
    async with async_session_factory() as db:
        # ── Fakultet va yo'nalishlar (mavjudini YANGILAYDI, yangisini qo'shadi) ──
        for fi, fac in enumerate(FACULTIES):
            f = await db.scalar(select(Faculty).where(Faculty.slug == fac["id"]))
            if f is None:
                f = Faculty(slug=fac["id"], name=fac["name"], sort_order=fi)
                db.add(f)
                await db.flush()
            else:
                f.name = fac["name"]
                f.sort_order = fi
            for pi, prog in enumerate(fac["programs"]):
                p = await db.scalar(select(Program).where(Program.slug == prog["id"]))
                if p is None:
                    p = Program(
                        slug=prog["id"], faculty_id=f.id, code=prog["code"],
                        name=prog["name"], form=prog["form"], lang=prog["lang"], sort_order=pi,
                    )
                    db.add(p)
                    await db.flush()
                else:
                    p.faculty_id = f.id      # yo'nalishni to'g'ri fakultetga ko'chiradi
                    p.code = prog["code"]
                    p.name = prog["name"]
                    p.form = prog["form"]
                    p.lang = prog["lang"]
                    p.sort_order = pi
                await _ensure_admission_contract(db, p)

        # ── Bo'lim matnlari (about/contact/...) — MAJBURIY yangilanadi ──
        for key, body in S.TEXTS.items():
            sec = await db.scalar(select(Section).where(Section.key == key))
            if sec is None:
                db.add(Section(key=key, title=S.MENU.get(key, key), body=body))
            else:
                sec.title = S.MENU.get(key, sec.title)
                sec.body = body

        # ── FAQ — yo'q bo'lsa qo'shiladi ──
        for fi, item in enumerate(FAQ):
            q = await db.scalar(select(Faq).where(Faq.question == item["question"]))
            if q is None:
                db.add(Faq(
                    question=item["question"], answer=item["answer"],
                    category=item.get("category"),
                    keywords=",".join(item.get("keywords", [])),
                    sort_order=fi,
                ))
        await db.commit()


async def _seed_admins(db) -> None:
    for uname, pwd, urole in ADMIN_USERS:
        exists = await db.scalar(select(AdminUser).where(AdminUser.username == uname))
        if exists is None:
            db.add(AdminUser(username=uname, password_hash=hash_password(pwd), role=urole))
            await db.flush()


async def seed() -> None:
    await init_db()
    await sync_static_content()
    async with async_session_factory() as db:
        await _seed_admins(db)
        await db.commit()
    print("Seed tugadi ✅")


async def ensure_seeded() -> None:
    """Jadvallarni yaratadi, kontentni koddan moslaydi, adminlarni ta'minlaydi."""
    await init_db()
    # Kontentni har safar koddagi holatga moslaymiz (fakultet/yo'nalish/matn).
    await sync_static_content()
    async with async_session_factory() as db:
        await _seed_admins(db)
        await db.commit()


if __name__ == "__main__":
    asyncio.run(seed())
