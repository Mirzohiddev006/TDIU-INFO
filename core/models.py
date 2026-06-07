"""SQLAlchemy 2.x modellari — TZ 5.3 dagi jadvallar (+ admin_users, sections)."""
from __future__ import annotations

from datetime import datetime

from sqlalchemy import (
    BigInteger,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    """Bot foydalanuvchilari."""
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
    name: Mapped[str | None] = mapped_column(String(255))
    username: Mapped[str | None] = mapped_column(String(255))
    lang: Mapped[str] = mapped_column(String(8), default="uz")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class Faculty(Base):
    __tablename__ = "faculties"

    id: Mapped[int] = mapped_column(primary_key=True)
    slug: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)

    programs: Mapped[list["Program"]] = relationship(
        back_populates="faculty", cascade="all, delete-orphan", order_by="Program.sort_order"
    )


class Program(Base):
    """Yo'nalishlar."""
    __tablename__ = "programs"

    id: Mapped[int] = mapped_column(primary_key=True)
    slug: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    faculty_id: Mapped[int] = mapped_column(ForeignKey("faculties.id", ondelete="CASCADE"))
    code: Mapped[str] = mapped_column(String(32))
    name: Mapped[str] = mapped_column(String(255))
    form: Mapped[str] = mapped_column(String(32), default="Kunduzgi")
    lang: Mapped[str] = mapped_column(String(32), default="O'zbek")
    sort_order: Mapped[int] = mapped_column(Integer, default=0)

    faculty: Mapped["Faculty"] = relationship(back_populates="programs")
    admissions: Mapped[list["Admission"]] = relationship(
        back_populates="program", cascade="all, delete-orphan"
    )


class Admission(Base):
    """Yillik: kvota va o'tish ballari (yo'nalish + yil)."""
    __tablename__ = "admission"

    id: Mapped[int] = mapped_column(primary_key=True)
    program_id: Mapped[int] = mapped_column(ForeignKey("programs.id", ondelete="CASCADE"))
    year: Mapped[str] = mapped_column(String(16), index=True)
    grant_places: Mapped[int | None] = mapped_column(Integer)
    contract_places: Mapped[int | None] = mapped_column(Integer)
    passing_grant: Mapped[float | None] = mapped_column(Float)
    passing_contract: Mapped[float | None] = mapped_column(Float)

    program: Mapped["Program"] = relationship(back_populates="admissions")


class Contract(Base):
    """Yillik: kontrakt summalari (yo'nalish + yil + shakl)."""
    __tablename__ = "contracts"

    id: Mapped[int] = mapped_column(primary_key=True)
    program_id: Mapped[int] = mapped_column(ForeignKey("programs.id", ondelete="CASCADE"))
    year: Mapped[str] = mapped_column(String(16), index=True)
    form: Mapped[str] = mapped_column(String(32), default="Kunduzgi")
    amount: Mapped[int | None] = mapped_column(BigInteger)


class Faq(Base):
    __tablename__ = "faq"

    id: Mapped[int] = mapped_column(primary_key=True)
    question: Mapped[str] = mapped_column(String(512))
    answer: Mapped[str] = mapped_column(Text)
    category: Mapped[str | None] = mapped_column(String(64))
    keywords: Mapped[str | None] = mapped_column(Text)  # vergul bilan
    sort_order: Mapped[int] = mapped_column(Integer, default=0)


class Section(Base):
    """Tahrirlanadigan bo'lim matnlari (about, admission, education, ...)."""
    __tablename__ = "sections"

    id: Mapped[int] = mapped_column(primary_key=True)
    key: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    title: Mapped[str] = mapped_column(String(255))
    body: Mapped[str] = mapped_column(Text)


class OperatorChat(Base):
    __tablename__ = "operator_chats"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, index=True)  # telegram_id
    status: Mapped[str] = mapped_column(String(32), default="open")  # open/closed
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True)
    chat_id: Mapped[int] = mapped_column(ForeignKey("operator_chats.id", ondelete="CASCADE"))
    sender: Mapped[str] = mapped_column(String(16))  # user/operator
    text: Mapped[str] = mapped_column(Text)
    ts: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class Analytics(Base):
    __tablename__ = "analytics"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int | None] = mapped_column(BigInteger, index=True)
    action: Mapped[str] = mapped_column(String(64))   # open_section, search, operator, start
    section: Mapped[str | None] = mapped_column(String(64))
    ts: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class AdminUser(Base):
    """Admin panel foydalanuvchilari (RBAC)."""
    __tablename__ = "admin_users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(32), default="content")  # super/content/operator
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
