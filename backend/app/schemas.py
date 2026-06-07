"""Pydantic sxemalari (API kirish/chiqish)."""
from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class ORM(BaseModel):
    model_config = ConfigDict(from_attributes=True)


# ── Auth ──
class LoginIn(BaseModel):
    username: str
    password: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str
    username: str


# ── Faculties ──
class FacultyIn(BaseModel):
    name: str
    description: str | None = None
    sort_order: int = 0


class FacultyOut(ORM):
    id: int
    slug: str
    name: str
    description: str | None
    sort_order: int


# ── Programs ──
class ProgramIn(BaseModel):
    faculty_id: int
    code: str
    name: str
    form: str = "Kunduzgi"
    lang: str = "O'zbek"
    sort_order: int = 0


class ProgramOut(ORM):
    id: int
    slug: str
    faculty_id: int
    code: str
    name: str
    form: str
    lang: str
    sort_order: int


# ── Admission (ball + kvota) ──
class AdmissionIn(BaseModel):
    grant_places: int | None = None
    contract_places: int | None = None
    passing_grant: float | None = None
    passing_grant_ru: float | None = None
    passing_contract: float | None = None
    passing_contract_ru: float | None = None


class AdmissionOut(ORM):
    id: int
    program_id: int
    year: str
    grant_places: int | None
    contract_places: int | None
    passing_grant: float | None
    passing_grant_ru: float | None
    passing_contract: float | None
    passing_contract_ru: float | None


# ── Contract ──
class ContractIn(BaseModel):
    form: str = "Kunduzgi"
    amount: int | None = None


class ContractOut(ORM):
    id: int
    program_id: int
    year: str
    form: str
    amount: int | None


# birlashtirilgan: yo'nalish + joriy yil ball/kontrakt (admin formasi uchun qulay)
class ProgramAdmissionOut(BaseModel):
    program: ProgramOut
    admission: AdmissionOut | None
    contract: ContractOut | None


# ── FAQ ──
class FaqIn(BaseModel):
    question: str
    answer: str
    category: str | None = None
    keywords: str | None = None
    sort_order: int = 0


class FaqOut(ORM):
    id: int
    question: str
    answer: str
    category: str | None
    keywords: str | None
    sort_order: int


# ── Section ──
class SectionIn(BaseModel):
    title: str
    body: str


class SectionOut(ORM):
    id: int
    key: str
    title: str
    body: str


# ── Stats ──
class StatsOut(BaseModel):
    users: int
    actions: int
    top_sections: list[dict]
    unanswered: int
