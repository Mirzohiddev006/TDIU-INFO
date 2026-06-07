"""Kontent CRUD: fakultetlar, yo'nalishlar, bo'limlar, FAQ."""
from __future__ import annotations

import re

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_session
from core.models import Faculty, Faq, Program, Section

from backend.app.deps import can_edit
from backend.app.schemas import (
    FacultyIn, FacultyOut, FaqIn, FaqOut,
    ProgramIn, ProgramOut, SectionIn, SectionOut,
)

router = APIRouter(prefix="/api", tags=["content"])


def _slugify(text: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")
    return s or "item"


# ── Fakultetlar ──
@router.get("/faculties", response_model=list[FacultyOut])
async def list_faculties(db: AsyncSession = Depends(get_session)):
    rows = await db.scalars(select(Faculty).order_by(Faculty.sort_order))
    return list(rows)


@router.post("/faculties", response_model=FacultyOut, dependencies=[Depends(can_edit)])
async def create_faculty(data: FacultyIn, db: AsyncSession = Depends(get_session)):
    slug = _slugify(data.name)
    base, i = slug, 1
    while await db.scalar(select(Faculty).where(Faculty.slug == slug)):
        slug = f"{base}_{i}"; i += 1
    fac = Faculty(slug=slug, **data.model_dump())
    db.add(fac)
    await db.commit()
    await db.refresh(fac)
    return fac


@router.put("/faculties/{fid}", response_model=FacultyOut, dependencies=[Depends(can_edit)])
async def update_faculty(fid: int, data: FacultyIn, db: AsyncSession = Depends(get_session)):
    fac = await db.get(Faculty, fid)
    if not fac:
        raise HTTPException(404, "Fakultet topilmadi")
    for k, v in data.model_dump().items():
        setattr(fac, k, v)
    await db.commit()
    await db.refresh(fac)
    return fac


@router.delete("/faculties/{fid}", dependencies=[Depends(can_edit)])
async def delete_faculty(fid: int, db: AsyncSession = Depends(get_session)):
    fac = await db.get(Faculty, fid)
    if not fac:
        raise HTTPException(404, "Fakultet topilmadi")
    await db.delete(fac)
    await db.commit()
    return {"ok": True}


# ── Yo'nalishlar ──
@router.get("/programs", response_model=list[ProgramOut])
async def list_programs(faculty_id: int | None = None, db: AsyncSession = Depends(get_session)):
    q = select(Program).order_by(Program.sort_order)
    if faculty_id is not None:
        q = q.where(Program.faculty_id == faculty_id)
    rows = await db.scalars(q)
    return list(rows)


@router.post("/programs", response_model=ProgramOut, dependencies=[Depends(can_edit)])
async def create_program(data: ProgramIn, db: AsyncSession = Depends(get_session)):
    slug = _slugify(data.name)
    base, i = slug, 1
    while await db.scalar(select(Program).where(Program.slug == slug)):
        slug = f"{base}_{i}"; i += 1
    prog = Program(slug=slug, **data.model_dump())
    db.add(prog)
    await db.commit()
    await db.refresh(prog)
    return prog


@router.put("/programs/{pid}", response_model=ProgramOut, dependencies=[Depends(can_edit)])
async def update_program(pid: int, data: ProgramIn, db: AsyncSession = Depends(get_session)):
    prog = await db.get(Program, pid)
    if not prog:
        raise HTTPException(404, "Yo'nalish topilmadi")
    for k, v in data.model_dump().items():
        setattr(prog, k, v)
    await db.commit()
    await db.refresh(prog)
    return prog


@router.delete("/programs/{pid}", dependencies=[Depends(can_edit)])
async def delete_program(pid: int, db: AsyncSession = Depends(get_session)):
    prog = await db.get(Program, pid)
    if not prog:
        raise HTTPException(404, "Yo'nalish topilmadi")
    await db.delete(prog)
    await db.commit()
    return {"ok": True}


# ── Bo'lim matnlari ──
@router.get("/sections", response_model=list[SectionOut])
async def list_sections(db: AsyncSession = Depends(get_session)):
    rows = await db.scalars(select(Section).order_by(Section.id))
    return list(rows)


@router.put("/sections/{key}", response_model=SectionOut, dependencies=[Depends(can_edit)])
async def update_section(key: str, data: SectionIn, db: AsyncSession = Depends(get_session)):
    sec = await db.scalar(select(Section).where(Section.key == key))
    if not sec:
        raise HTTPException(404, "Bo'lim topilmadi")
    sec.title = data.title
    sec.body = data.body
    await db.commit()
    await db.refresh(sec)
    return sec


# ── FAQ ──
@router.get("/faq", response_model=list[FaqOut])
async def list_faq(db: AsyncSession = Depends(get_session)):
    rows = await db.scalars(select(Faq).order_by(Faq.sort_order))
    return list(rows)


@router.post("/faq", response_model=FaqOut, dependencies=[Depends(can_edit)])
async def create_faq(data: FaqIn, db: AsyncSession = Depends(get_session)):
    item = Faq(**data.model_dump())
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return item


@router.put("/faq/{qid}", response_model=FaqOut, dependencies=[Depends(can_edit)])
async def update_faq(qid: int, data: FaqIn, db: AsyncSession = Depends(get_session)):
    item = await db.get(Faq, qid)
    if not item:
        raise HTTPException(404, "FAQ topilmadi")
    for k, v in data.model_dump().items():
        setattr(item, k, v)
    await db.commit()
    await db.refresh(item)
    return item


@router.delete("/faq/{qid}", dependencies=[Depends(can_edit)])
async def delete_faq(qid: int, db: AsyncSession = Depends(get_session)):
    item = await db.get(Faq, qid)
    if not item:
        raise HTTPException(404, "FAQ topilmadi")
    await db.delete(item)
    await db.commit()
    return {"ok": True}
