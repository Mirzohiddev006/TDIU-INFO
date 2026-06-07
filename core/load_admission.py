"""admission_data.py dagi qiymatlarni (ball/kvota/kontrakt) mavjud bazaga yozadi.

Seed faqat bo'sh qatorlarni yaratadi. Bu skript esa MAVJUD qatorlarni ham
yangilaydi (upsert). admission_data.py ni tahrirlagandan keyin ishga tushiring:

    python -m core.load_admission
"""
from __future__ import annotations

import asyncio

from sqlalchemy import select

from core.database import async_session_factory, init_db
from core.models import Admission, Contract, Program
from core.settings import CURRENT_YEAR

from bot.content import admission_data as AD


async def load() -> None:
    await init_db()
    updated = 0
    async with async_session_factory() as db:
        programs = list(await db.scalars(select(Program)))
        for p in programs:
            d = AD.get(p.slug)
            a = await db.scalar(select(Admission).where(
                Admission.program_id == p.id, Admission.year == CURRENT_YEAR))
            if a is None:
                a = Admission(program_id=p.id, year=CURRENT_YEAR)
                db.add(a)
            a.passing_grant = d["passing_grant"]
            a.passing_grant_ru = d.get("passing_grant_ru")
            a.passing_contract = d["passing_contract"]
            a.passing_contract_ru = d.get("passing_contract_ru")
            a.grant_places = d["grant_places"]
            a.contract_places = d["contract_places"]

            c = await db.scalar(select(Contract).where(
                Contract.program_id == p.id, Contract.year == CURRENT_YEAR))
            if c is None:
                c = Contract(program_id=p.id, year=CURRENT_YEAR, form=p.form)
                db.add(c)
            c.amount = d["contract_amount"]
            updated += 1
        await db.commit()
    print(f"Yangilandi: {updated} yo'nalish ({CURRENT_YEAR}) ✅")


if __name__ == "__main__":
    asyncio.run(load())
