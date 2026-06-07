"""Statik kontentni (bot.content) bazaga ko'chiradi. Idempotent."""
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


async def seed() -> None:
    await init_db()
    async with async_session_factory() as db:
        # ── Fakultetlar + yo'nalishlar ──
        for fi, fac in enumerate(FACULTIES):
            existing = await db.scalar(select(Faculty).where(Faculty.slug == fac["id"]))
            if existing is None:
                existing = Faculty(slug=fac["id"], name=fac["name"], sort_order=fi)
                db.add(existing)
                await db.flush()
            for pi, prog in enumerate(fac["programs"]):
                p = await db.scalar(select(Program).where(Program.slug == prog["id"]))
                if p is None:
                    p = Program(
                        slug=prog["id"], faculty_id=existing.id, code=prog["code"],
                        name=prog["name"], form=prog["form"], lang=prog["lang"],
                        sort_order=pi,
                    )
                    db.add(p)
                    await db.flush()
                # Joriy yil uchun bo'sh admission/contract qatorlari
                a = await db.scalar(
                    select(Admission).where(
                        Admission.program_id == p.id, Admission.year == CURRENT_YEAR
                    )
                )
                if a is None:
                    d = AD.get(prog["id"])
                    db.add(Admission(
                        program_id=p.id, year=CURRENT_YEAR,
                        grant_places=d["grant_places"], contract_places=d["contract_places"],
                        passing_grant=d["passing_grant"], passing_grant_ru=d.get("passing_grant_ru"),
                        passing_contract=d["passing_contract"], passing_contract_ru=d.get("passing_contract_ru"),
                    ))
                c = await db.scalar(
                    select(Contract).where(
                        Contract.program_id == p.id, Contract.year == CURRENT_YEAR
                    )
                )
                if c is None:
                    d = AD.get(prog["id"])
                    db.add(Contract(program_id=p.id, year=CURRENT_YEAR,
                                    form=prog["form"], amount=d["contract_amount"]))

        # ── FAQ ──
        for fi, item in enumerate(FAQ):
            q = await db.scalar(select(Faq).where(Faq.question == item["question"]))
            if q is None:
                db.add(Faq(
                    question=item["question"], answer=item["answer"],
                    category=item.get("category"),
                    keywords=",".join(item.get("keywords", [])),
                    sort_order=fi,
                ))

        # ── Tahrirlanadigan bo'lim matnlari ──
        for key, body in S.TEXTS.items():
            sec = await db.scalar(select(Section).where(Section.key == key))
            if sec is None:
                db.add(Section(key=key, title=S.MENU.get(key, key), body=body))

        # ── Birinchi super-admin ──
        admin = await db.scalar(select(AdminUser).where(AdminUser.username == ADMIN_USERNAME))
        if admin is None:
            db.add(AdminUser(
                username=ADMIN_USERNAME,
                password_hash=hash_password(ADMIN_PASSWORD),
                role="super",
            ))

        await db.commit()
    print("Seed tugadi ✅")



async def ensure_seeded() -> None:
    """Jadvallarni yaratadi va baza bo'sh bo'lsa to'ldiradi (idempotent)."""
    from sqlalchemy import select
    from core.models import Faculty
    await init_db()
    async with async_session_factory() as db:
        has = await db.scalar(select(Faculty).limit(1))
    if has is None:
        await seed()

if __name__ == "__main__":
    asyncio.run(seed())
