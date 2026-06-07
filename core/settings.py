"""Umumiy sozlamalar (bot va backend uchun)."""
from __future__ import annotations

import os

from dotenv import load_dotenv

load_dotenv()

# Standart: SQLite (o'rnatishsiz ishlaydi). Production: PostgreSQL.
# PostgreSQL misol:
#   postgresql+asyncpg://user:pass@localhost:5432/tdiu
DATABASE_URL: str = os.getenv(
    "DATABASE_URL", "sqlite+aiosqlite:///./tdiu.db"
)

# Joriy o'quv yili (admission/contract uchun standart)
CURRENT_YEAR: str = os.getenv("ADMISSION_YEAR", "2025/2026")

# JWT (admin panel autentifikatsiyasi)
JWT_SECRET: str = os.getenv("JWT_SECRET", "CHANGE-ME-in-production-please")
JWT_ALG: str = "HS256"
JWT_EXPIRE_MINUTES: int = int(os.getenv("JWT_EXPIRE_MINUTES", "720"))

# Birinchi super-admin (seed paytida yaratiladi)
ADMIN_USERNAME: str = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD: str = os.getenv("ADMIN_PASSWORD", "admin123")
