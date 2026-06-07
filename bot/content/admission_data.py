"""Yillik o'zgaruvchan ma'lumotlar: o'tish ballari (O'zbek/Rus), kvota, kontrakt.

Manba: TDIU 2025/2026 kunduzgi qabul ballari + 2024/2025 bazaviy kontrakt summasi.
Kalit = programs.py dagi yo'nalish `id`. None → bot "tez orada" deb yozadi.

Maydonlar:
  passing_grant / passing_grant_ru        — davlat granti o'tish bali (O'zbek / Rus)
  passing_contract / passing_contract_ru  — to'lov-kontrakt o'tish bali (O'zbek / Rus)
  contract_amount                          — bazaviy kontrakt summasi (so'm)
  grant_places / contract_places           — kvota (o'rinlar soni)
"""
from __future__ import annotations

YEAR = "2025/2026"


def _blank() -> dict:
    return {
        "passing_grant": None, "passing_grant_ru": None,
        "passing_contract": None, "passing_contract_ru": None,
        "contract_amount": None,
        "grant_places": None, "contract_places": None,
    }


def _e(pg, pgr, pc, pcr, amount) -> dict:
    return {
        "passing_grant": pg, "passing_grant_ru": pgr,
        "passing_contract": pc, "passing_contract_ru": pcr,
        "contract_amount": amount,
        "grant_places": None, "contract_places": None,
    }


# 2025/2026 kunduzgi o'tish ballari (O'zbek/Rus) + bazaviy kontrakt summasi
PROGRAM_DATA: dict[str, dict] = {
    "econ":          _e(185.5, 185.7, 169.3, 157.4, 10_500_000),
    "accounting":    _e(181.6, 182.4, 148.2, 127.3, 10_500_000),
    "statistics":    _e(170.5, None,  120.9, None,  10_500_000),
    "taxes":         _e(178.0, 178.9, 126.4, 114.7, 10_500_000),
    "finance":       _e(184.1, 184.6, 157.2, 140.6, 10_500_000),
    "banking":       _e(182.4, 182.4, 157.5, 131.4, 10_500_000),
    "management":    _e(179.1, 179.3, 140.8, 135.5, 10_500_000),
    "business":      _e(180.2, 180.2, 135.7, 130.0, 10_500_000),
    "hr":            _e(169.9, None,  114.4, None,  10_500_000),
    "world_econ":    _e(186.8, 186.8, 173.2, 161.4, 11_250_000),
    "marketing":     _e(175.1, 175.3, 130.8, 124.2, 10_500_000),
    "trade":         _e(174.3, None,  120.0, None,  10_500_000),
    "logistics":     _e(168.8, None,  116.7, None,  10_500_000),
    "info_systems":  _e(151.0, 163.5, 106.9, 66.6,  8_150_000),
    "info_security": _e(166.7, 173.3, 131.1, 70.7,  8_150_000),
    "ai":            _e(149.9, 152.2, 91.5,  59.8,  8_150_000),
    "tourism":       _e(162.8, 169.8, 126.8, 128.8, 8_150_000),
}


# ── Formatlash yordamchilari ────────────────────────────────────────────

def _score_pair(uz, ru) -> str:
    parts = []
    if uz is not None:
        parts.append(f"O'zbek {uz}")
    if ru is not None:
        parts.append(f"Rus {ru}")
    return " | ".join(parts) if parts else "tez orada kiritiladi"


def _fmt_amount(value) -> str:
    if value is None:
        return "tez orada kiritiladi"
    return f"{value:,.0f} so'm".replace(",", " ")


def _fmt_places(value) -> str:
    return f"{value} ta" if value is not None else "—"


def get(program_id: str) -> dict:
    return PROGRAM_DATA.get(program_id, _blank())


def admission_lines(program_id: str) -> str:
    d = get(program_id)
    return (
        f"📈 Grant o'tish bali: <b>{_score_pair(d['passing_grant'], d['passing_grant_ru'])}</b>\n"
        f"📊 To'lov-kontrakt o'tish bali: <b>{_score_pair(d['passing_contract'], d['passing_contract_ru'])}</b>\n"
        f"💰 Kontrakt summasi (bazaviy): <b>{_fmt_amount(d['contract_amount'])}</b>"
    )


def has_any_quota() -> bool:
    return any(
        d.get("grant_places") is not None or d.get("contract_places") is not None
        for d in PROGRAM_DATA.values()
    )
