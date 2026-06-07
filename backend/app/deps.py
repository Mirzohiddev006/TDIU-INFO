"""Auth dependency va rol tekshiruvi (RBAC)."""
from __future__ import annotations

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from core.security import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


async def current_admin(token: str = Depends(oauth2_scheme)) -> dict:
    try:
        payload = decode_token(token)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Yaroqsiz token"
        )
    return {"username": payload.get("sub"), "role": payload.get("role")}


def require_roles(*roles: str):
    """Berilgan rollardan biri kerakligini talab qiladi."""
    async def checker(admin: dict = Depends(current_admin)) -> dict:
        if admin["role"] not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Ruxsat yo'q (rol cheklovi)",
            )
        return admin
    return checker


# Kontent tahrirlash: super yoki content-menejer
can_edit = require_roles("super", "content")
# Faqat super-admin
super_only = require_roles("super")
