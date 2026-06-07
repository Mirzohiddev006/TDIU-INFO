"""Yillik o'zgaruvchan ma'lumotlar: o'tish ballari, kvota, kontrakt summalari.

╔══════════════════════════════════════════════════════════════════════╗
║  SHU FAYLNI TO'LDIRING — bot avtomatik ravishda ko'rsatadi.           ║
║  Kalit (key) = programs.py dagi yo'nalish `id`.                        ║
║  None  → bot "tez orada kiritiladi" deb yozadi.                       ║
║  Raqam → bot aynan shu qiymatni ko'rsatadi.                           ║
║                                                                        ║
║  Maydonlar:                                                            ║
║   passing_grant     — davlat granti o'tish bali (masalan: 178.5)      ║
║   passing_contract  — to'lov-kontrakt o'tish bali (masalan: 150.2)    ║
║   contract_amount   — kontrakt summasi, so'mda (masalan: 18_000_000)  ║
║   grant_places      — grant o'rinlari soni (kvota)                    ║
║   contract_places   — kontrakt o'rinlari soni (kvota)                 ║
╚══════════════════════════════════════════════════════════════════════╝
"""
from __future__ import annotations

# Joriy o'quv yili (matnlarda ko'rsatiladi)
YEAR = "2025/2026"


def _blank() -> dict:
    return {
        "passing_grant": None,
        "passing_contract": None,
        "contract_amount": None,
        "grant_places": None,
        "contract_places": None,
    }


# Yo'nalish bo'yicha ma'lumotlar. Qiymatlarni shu yerga kiriting.
# Misol uchun:
#   "econ_branch": {"passing_grant": 178.5, "passing_contract": 150.2,
#                   "contract_amount": 18_000_000,
#                   "grant_places": 25, "contract_places": 100},
PROGRAM_DATA: dict[str, dict] = {
    # — Iqtisodiyot fakulteti —
    "prof_econ": {"passing_grant": None, "passing_contract": None, "contract_amount": 7400000, "grant_places": None, "contract_places": None},
    "econ_branch": {"passing_grant": None, "passing_contract": None, "contract_amount": 10500000, "grant_places": None, "contract_places": None},
    "econ_dev": {"passing_grant": None, "passing_contract": None, "contract_amount": 10500000, "grant_places": None, "contract_places": None},
    "econ_city": {"passing_grant": None, "passing_contract": None, "contract_amount": 10500000, "grant_places": None, "contract_places": None},
    "econ_green": {"passing_grant": None, "passing_contract": None, "contract_amount": 10500000, "grant_places": None, "contract_places": None},
    "econometrics": {"passing_grant": None, "passing_contract": None, "contract_amount": 10500000, "grant_places": None, "contract_places": None},
    "regional_econ": {"passing_grant": None, "passing_contract": None, "contract_amount": 10500000, "grant_places": None, "contract_places": None},
    "econ_security": {"passing_grant": None, "passing_contract": None, "contract_amount": 10500000, "grant_places": None, "contract_places": None},
    # — Raqamli iqtisodiyot va AT fakulteti —
    "digital_econ": {"passing_grant": None, "passing_contract": None, "contract_amount": 10500000, "grant_places": None, "contract_places": None},
    "info_systems": {"passing_grant": None, "passing_contract": None, "contract_amount": 8150000, "grant_places": None, "contract_places": None},
    "info_security": {"passing_grant": None, "passing_contract": None, "contract_amount": 8150000, "grant_places": None, "contract_places": None},
    "ai": {"passing_grant": None, "passing_contract": None, "contract_amount": 8150000, "grant_places": None, "contract_places": None},
    # — Buxgalteriya hisobi fakulteti —
    "accounting_audit": {"passing_grant": None, "passing_contract": None, "contract_amount": 10500000, "grant_places": None, "contract_places": None},
    "statistics": {"passing_grant": None, "passing_contract": None, "contract_amount": 10500000, "grant_places": None, "contract_places": None},
    # — Soliqlar va byudjet hisobi fakulteti —
    "taxes": {"passing_grant": None, "passing_contract": None, "contract_amount": 10500000, "grant_places": None, "contract_places": None},
    "budget_treasury": {"passing_grant": None, "passing_contract": None, "contract_amount": 10500000, "grant_places": None, "contract_places": None},
    # — Moliya fakulteti —
    "finance_fintech": {"passing_grant": None, "passing_contract": None, "contract_amount": 10500000, "grant_places": None, "contract_places": None},
    # — Bank ishi fakulteti —
    "banking_audit": {"passing_grant": None, "passing_contract": None, "contract_amount": 10500000, "grant_places": None, "contract_places": None},
    "insurance": {"passing_grant": None, "passing_contract": None, "contract_amount": 10500000, "grant_places": None, "contract_places": None},
    "currency_credit": {"passing_grant": None, "passing_contract": None, "contract_amount": 11250000, "grant_places": None, "contract_places": None},
    # — Menejment fakulteti —
    "management": {"passing_grant": None, "passing_contract": None, "contract_amount": 10500000, "grant_places": None, "contract_places": None},
    "biz_sustainable": {"passing_grant": None, "passing_contract": None, "contract_amount": 10500000, "grant_places": None, "contract_places": None},
    "biz_branch": {"passing_grant": None, "passing_contract": None, "contract_amount": 10500000, "grant_places": None, "contract_places": None},
    "hr": {"passing_grant": None, "passing_contract": None, "contract_amount": 10500000, "grant_places": None, "contract_places": None},
    "biz_analysis": {"passing_grant": None, "passing_contract": None, "contract_amount": 10500000, "grant_places": None, "contract_places": None},
    "corporate": {"passing_grant": None, "passing_contract": None, "contract_amount": 10500000, "grant_places": None, "contract_places": None},
    "logistics": {"passing_grant": None, "passing_contract": None, "contract_amount": 10500000, "grant_places": None, "contract_places": None},
    "world_econ": {"passing_grant": None, "passing_contract": None, "contract_amount": 11250000, "grant_places": None, "contract_places": None},
    "marketing": {"passing_grant": None, "passing_contract": None, "contract_amount": 10500000, "grant_places": None, "contract_places": None},
    # — Turizm fakulteti —
    "tourism_mgmt": {"passing_grant": None, "passing_contract": None, "contract_amount": 8150000, "grant_places": None, "contract_places": None},
    "hotel": {"passing_grant": None, "passing_contract": None, "contract_amount": 8150000, "grant_places": None, "contract_places": None},
    "tourism": {"passing_grant": None, "passing_contract": None, "contract_amount": 8150000, "grant_places": None, "contract_places": None},
}


# ── Formatlash yordamchilari (o'zgartirish shart emas) ──────────────────

def _fmt_score(value) -> str:
    return f"{value}" if value is not None else "tez orada kiritiladi"


def _fmt_amount(value) -> str:
    if value is None:
        return "tez orada kiritiladi"
    return f"{value:,.0f} so'm".replace(",", " ")


def _fmt_places(value) -> str:
    return f"{value} ta" if value is not None else "—"


def get(program_id: str) -> dict:
    """Yo'nalish ma'lumotini xavfsiz qaytaradi (yo'q bo'lsa bo'sh)."""
    return PROGRAM_DATA.get(program_id, _blank())


def admission_lines(program_id: str) -> str:
    """Yo'nalish kartochkasi uchun ball/kontrakt qatorlari."""
    d = get(program_id)
    return (
        f"📈 Grant o'tish bali: <b>{_fmt_score(d['passing_grant'])}</b>\n"
        f"📊 Kontrakt o'tish bali: <b>{_fmt_score(d['passing_contract'])}</b>\n"
        f"💰 Kontrakt summasi: <b>{_fmt_amount(d['contract_amount'])}</b>"
    )


def has_any_quota() -> bool:
    return any(
        d.get("grant_places") is not None or d.get("contract_places") is not None
        for d in PROGRAM_DATA.values()
    )
