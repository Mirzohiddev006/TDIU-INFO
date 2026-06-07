"""Statistika dashboard ma'lumotlari."""
from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_session
from core.models import Analytics, User

from backend.app.deps import current_admin
from backend.app.schemas import StatsOut

router = APIRouter(prefix="/api/stats", tags=["stats"])


@router.get("", response_model=StatsOut, dependencies=[Depends(current_admin)])
async def stats(db: AsyncSession = Depends(get_session)):
    users = await db.scalar(select(func.count(User.id))) or 0
    actions = await db.scalar(select(func.count(Analytics.id))) or 0
    top_rows = await db.execute(
        select(Analytics.section, func.count(Analytics.id).label("c"))
        .where(Analytics.section.is_not(None))
        .group_by(Analytics.section)
        .order_by(func.count(Analytics.id).desc())
        .limit(10)
    )
    top = [{"section": s, "count": c} for s, c in top_rows.all()]
    unanswered = await db.scalar(
        select(func.count(Analytics.id)).where(Analytics.action == "unanswered")
    ) or 0
    return StatsOut(users=users, actions=actions, top_sections=top, unanswered=unanswered)
