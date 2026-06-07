"""O'tish ballari, kvota va kontrakt summalarini boshqarish (joriy yil)."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_session
from core.models import Admission, Contract, Program
from core.settings import CURRENT_YEAR

from backend.app.deps import can_edit
from backend.app.schemas import (
    AdmissionIn, AdmissionOut, ContractIn, ContractOut, ProgramAdmissionOut, ProgramOut,
)

router = APIRouter(prefix="/api/admission", tags=["admission"])


async def _get_or_create_admission(db, program_id: int, year: str) -> Admission:
    a = await db.scalar(
        select(Admission).where(Admission.program_id == program_id, Admission.year == year)
    )
    if a is None:
        a = Admission(program_id=program_id, year=year)
        db.add(a)
        await db.flush()
    return a


async def _get_or_create_contract(db, program_id: int, year: str, form: str) -> Contract:
    c = await db.scalar(
        select(Contract).where(Contract.program_id == program_id, Contract.year == year)
    )
    if c is None:
        c = Contract(program_id=program_id, year=year, form=form)
        db.add(c)
        await db.flush()
    return c


@router.get("/overview", response_model=list[ProgramAdmissionOut])
async def overview(year: str = CURRENT_YEAR, db: AsyncSession = Depends(get_session)):
    """Barcha yo'nalishlar + joriy yil ball/kvota/kontrakt (admin formasi uchun)."""
    programs = list(await db.scalars(select(Program).order_by(Program.sort_order)))
    result = []
    for p in programs:
        a = await db.scalar(
            select(Admission).where(Admission.program_id == p.id, Admission.year == year)
        )
        c = await db.scalar(
            select(Contract).where(Contract.program_id == p.id, Contract.year == year)
        )
        result.append(ProgramAdmissionOut(
            program=ProgramOut.model_validate(p),
            admission=AdmissionOut.model_validate(a) if a else None,
            contract=ContractOut.model_validate(c) if c else None,
        ))
    return result


@router.put("/{program_id}/scores", response_model=AdmissionOut, dependencies=[Depends(can_edit)])
async def set_scores(
    program_id: int, data: AdmissionIn, year: str = CURRENT_YEAR,
    db: AsyncSession = Depends(get_session),
):
    if not await db.get(Program, program_id):
        raise HTTPException(404, "Yo'nalish topilmadi")
    a = await _get_or_create_admission(db, program_id, year)
    for k, v in data.model_dump().items():
        setattr(a, k, v)
    await db.commit()
    await db.refresh(a)
    return a


@router.put("/{program_id}/contract", response_model=ContractOut, dependencies=[Depends(can_edit)])
async def set_contract(
    program_id: int, data: ContractIn, year: str = CURRENT_YEAR,
    db: AsyncSession = Depends(get_session),
):
    if not await db.get(Program, program_id):
        raise HTTPException(404, "Yo'nalish topilmadi")
    c = await _get_or_create_contract(db, program_id, year, data.form)
    c.form = data.form
    c.amount = data.amount
    await db.commit()
    await db.refresh(c)
    return c
