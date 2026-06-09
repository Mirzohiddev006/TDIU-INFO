"""Async DB engine va sessiya (bot va backend uchun umumiy)."""
from __future__ import annotations

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from core.settings import DATABASE_URL, needs_ssl
from core.models import Base

# Tashqi Postgres (Neon/Render) uchun SSL + uxlab qolgan ulanishlarni tekshirish.
_engine_kwargs: dict = {"echo": False, "future": True}
if "+asyncpg" in DATABASE_URL:
    _engine_kwargs["pool_pre_ping"] = True
    _engine_kwargs["pool_recycle"] = 300
    if needs_ssl():
        import ssl as _ssl

        _ctx = _ssl.create_default_context()
        _engine_kwargs["connect_args"] = {"ssl": _ctx}

engine = create_async_engine(DATABASE_URL, **_engine_kwargs)
async_session_factory = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def init_db() -> None:
    """Jadvallarni yaratadi (mavjud bo'lmasa)."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency."""
    async with async_session_factory() as session:
        yield session
