"""Fakultetlar va bakalavriat yo'nalishlari — tsue.uz rasmiy katalogidan.

Manba: https://tsue.uz/page/bachelor (32 ta bakalavriat yo'nalishi).
Yo'nalish kodlari va nomlari rasmiy. Yo'nalishlarning fakultetlarga taqsimoti
mavzu bo'yicha tuzilgan — admin panel orqali aniqlashtirilishi mumkin.

Har bir yo'nalishning `id` si — o'tish bali / kontrakt summasi kabi yillik
qiymatlarni bog'lash uchun ishlatiladi (qarang: admission_data.py).
"""
from __future__ import annotations

# Standart qiymatlar
DEFAULT_FORM = "Kunduzgi"
DEFAULT_LANG = "O'zbek"


def _p(pid: str, code: str, name: str) -> dict:
    return {"id": pid, "code": code, "name": name, "form": DEFAULT_FORM, "lang": DEFAULT_LANG}


FACULTIES: list[dict] = [
    {
        "id": "economics",
        "name": "Iqtisodiyot fakulteti",
        "programs": [
            _p("prof_econ", "60112400", "Professional ta'lim: iqtisodiyot"),
            _p("econ_branch", "60310100", "Iqtisodiyot (tarmoqlar va sohalar bo'yicha)"),
            _p("econ_dev", "60310100", "Iqtisodiyot (taraqqiyot iqtisodiyoti)"),
            _p("econ_city", "60310100", "Iqtisodiyot (shaharlar iqtisodiyoti)"),
            _p("econ_green", "60310100", "Iqtisodiyot (yashil iqtisodiyot)"),
            _p("econometrics", "60310200", "Ekonometrika"),
            _p("regional_econ", "60310300", "Mintaqaviy iqtisodiyot"),
            _p("econ_security", "60310400", "Iqtisodiy xavfsizlik"),
        ],
    },
    {
        "id": "digital",
        "name": "Raqamli iqtisodiyot va axborot texnologiyalari fakulteti",
        "programs": [
            _p("digital_econ", "60310500", "Raqamli iqtisodiyot (tarmoqlar va sohalar bo'yicha)"),
            _p("info_systems", "60610200", "Axborot tizimlari va texnologiyalari (tarmoqlar va sohalar bo'yicha)"),
            _p("info_security", "60610300", "Axborot xavfsizligi (sohalar bo'yicha)"),
            _p("ai", "60610700", "Sun'iy intellekt"),
        ],
    },
    {
        "id": "accounting",
        "name": "Buxgalteriya hisobi fakulteti",
        "programs": [
            _p("accounting_audit", "60410100", "Buxgalteriya hisobi va audit (tarmoqlar bo'yicha)"),
            _p("statistics", "60410800", "Statistika (tarmoqlar va sohalar bo'yicha)"),
        ],
    },
    {
        "id": "taxes",
        "name": "Soliqlar va byudjet hisobi fakulteti",
        "programs": [
            _p("taxes", "60410200", "Soliqlar va soliqqa tortish (faoliyat turlari bo'yicha)"),
            _p("budget_treasury", "60410700", "Budjet nazorati va g'aznachiligi"),
        ],
    },
    {
        "id": "finance",
        "name": "Moliya fakulteti",
        "programs": [
            _p("finance_fintech", "60410400", "Moliya va moliyaviy texnologiyalar"),
        ],
    },
    {
        "id": "banking",
        "name": "Bank ishi fakulteti",
        "programs": [
            _p("banking_audit", "60410500", "Bank ishi va auditi"),
            _p("insurance", "60410600", "Sug'urta ishi"),
            _p("currency_credit", "60412100", "Xalqaro valyuta-kredit munosabatlari"),
        ],
    },
    {
        "id": "management",
        "name": "Menejment fakulteti",
        "programs": [
            _p("management", "60411200", "Menejment (tarmoqlar va sohalar bo'yicha)"),
            _p("biz_sustainable", "60411300", "Biznesni boshqarish (barqaror biznes)"),
            _p("biz_branch", "60411300", "Biznesni boshqarish (tarmoqlar bo'yicha)"),
            _p("hr", "60411400", "Inson resurslarini boshqarish"),
            _p("biz_analysis", "60411500", "Biznes-tahlil"),
            _p("corporate", "60411600", "Korporativ boshqaruv"),
            _p("logistics", "60411700", "Logistika (yo'nalishlar bo'yicha)"),
            _p("world_econ", "60411900", "Jahon iqtisodiyoti va xalqaro iqtisodiy munosabatlar"),
            _p("marketing", "60412500", "Marketing (tarmoqlar va sohalar bo'yicha)"),
        ],
    },
    {
        "id": "tourism",
        "name": "Turizm fakulteti",
        "programs": [
            _p("tourism_mgmt", "60411200", "Menejment: turizm biznesini boshqarish"),
            _p("hotel", "61010100", "Mehmonxona xo'jaligini tashkil etish va boshqarish"),
            _p("tourism", "61010400", "Turizm (faoliyat yo'nalishlari bo'yicha)"),
        ],
    },
]

# Ta'lim shakli / joylashuv bo'yicha qo'shimcha fakultetlar (yuqoridagi yo'nalishlar
# turli shakllarda taklif etiladi). Ma'lumot uchun ko'rsatiladi.
OTHER_FACULTIES: list[str] = [
    "Moliya fakulteti",
    "Sirtqi ta'lim fakulteti",
    "Kechki ta'lim va magistratura fakulteti",
    "Masofaviy va Ikkinchi oliy ta'lim fakulteti",
    "Qo'shma ta'lim fakulteti",
    "To'rtko'l fakulteti (filial)",
    "Andijon fakulteti (filial)",
]

JOINT_PROGRAMS: list[str] = [
    "TDIU – London universiteti qo'shma ta'lim dasturi",
    "TDIU – IMC Krems (Avstriya) qo'shma ta'lim dasturi",
    "TDIU – Pendidikan qo'shma ta'lim dasturi",
    "TDIU – UrDIU qo'shma ta'lim dasturi",
]


def find_program(program_id: str) -> dict | None:
    for fac in FACULTIES:
        for prog in fac["programs"]:
            if prog["id"] == program_id:
                return prog
    return None


def find_faculty(faculty_id: str) -> dict | None:
    return next((f for f in FACULTIES if f["id"] == faculty_id), None)
