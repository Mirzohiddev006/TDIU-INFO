"""Umumiy sozlamalar (bot va backend uchun)."""
from __future__ import annotations

import os
import re

from dotenv import load_dotenv

load_dotenv()


def _normalize_db_url(url: str) -> str:
    """Render/Heroku beradigan postgres URL'ini async (asyncpg) formatiga keltiradi."""
    if url.startswith("postgres://"):
        url = "postgresql+asyncpg://" + url[len("postgres://"):]
    elif url.startswith("postgresql://"):
        url = "postgresql+asyncpg://" + url[len("postgresql://"):]
    if "+asyncpg" in url and "sslmode=" in url:
        url = re.sub(r"[?&]sslmode=[^&]*", "", url)
    return url


# Standart: SQLite (o'rnatishsiz ishlaydi). Production: PostgreSQL.
DATABASE_URL: str = _normalize_db_url(
    os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./tdiu.db")
)

# Joriy o'quv yili
CURRENT_YEAR: str = os.getenv("ADMISSION_YEAR", "2025/2026")

# JWT (admin panel autentifikatsiyasi)
JWT_SECRET: str = os.getenv("JWT_SECRET", "CHANGE-ME-in-production-please")
JWT_ALG: str = "HS256"
JWT_EXPIRE_MINUTES: int = int(os.getenv("JWT_EXPIRE_MINUTES", "720"))

# Birinchi super-admin (seed paytida yaratiladi)
ADMIN_USERNAME: str = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD: str = os.getenv("ADMIN_PASSWORD", "admin123")
