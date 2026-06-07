"""Autentifikatsiya: login -> JWT."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_session
from core.models import AdminUser
from core.security import create_token, verify_password

from backend.app.deps import current_admin
from backend.app.schemas import LoginIn, TokenOut

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/login", response_model=TokenOut)
async def login(data: LoginIn, db: AsyncSession = Depends(get_session)):
    user = await db.scalar(select(AdminUser).where(AdminUser.username == data.username))
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Login yoki parol noto'g'ri",
        )
    token = create_token(user.username, user.role)
    return TokenOut(access_token=token, role=user.role, username=user.username)


@router.get("/me")
async def me(admin: dict = Depends(current_admin)):
    return admin
