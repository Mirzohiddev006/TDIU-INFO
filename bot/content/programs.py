"""Fakultetlar va bakalavriat yo'nalishlari — 2025/2026 rasmiy qabul ro'yxati.

Manba: TDIU 2025/2026 kunduzgi bakalavriat qabul parametrlari (17 yo'nalish).
Kodlar va nomlar rasmiy. Yo'nalishlarning fakultetlarga taqsimoti mavzu bo'yicha.
"""
from __future__ import annotations

DEFAULT_FORM = "Kunduzgi"
DEFAULT_LANG = "O'zbek / Rus"


def _p(pid: str, code: str, name: str) -> dict:
    return {"id": pid, "code": code, "name": name, "form": DEFAULT_FORM, "lang": DEFAULT_LANG}


FACULTIES: list[dict] = [
    {
        "id": "economics",
        "name": "Iqtisodiyot fakulteti",
        "programs": [
            _p("econ", "60410100", "Iqtisodiyot"),
            _p("hr", "60411000", "Inson resurslarini boshqarish"),
        ],
    },
    {
        "id": "digital",
        "name": "Raqamli iqtisodiyot va axborot texnologiyalari fakulteti",
        "programs": [
            _p("info_systems", "60610100", "Axborot tizimlari va texnologiyalari"),
            _p("info_security", "60610200", "Axborot xavfsizligi"),
            _p("statistics", "60410700", "Statistika"),
            _p("ai", "60610500", "Sun'iy intellekt"),
        ],
    },
    {
        "id": "tourism",
        "name": "Turizm fakulteti",
        "programs": [
            _p("tourism", "61010100", "Turizm va mehmondo'stlik"),
            _p("marketing", "60411200", "Marketing"),
            _p("trade", "60411300", "Savdo ishi"),
        ],
    },
    {
        "id": "management",
        "name": "Menejment fakulteti",
        "programs": [
            _p("management", "60410800", "Menejment"),
            _p("logistics", "61010400", "Logistika"),
            _p("business", "60410900", "Biznesni boshqarish"),
            _p("world_econ", "60411100", "Jahon iqtisodiyoti va xalqaro iqtisodiy munosabatlar"),
        ],
    },
    {
        "id": "finance",
        "name": "Moliya va moliyaviy texnologiyalar fakulteti",
        "programs": [
            _p("finance", "60410500", "Moliya va moliyaviy texnologiyalar"),
        ],
    },
    {
        "id": "banking",
        "name": "Bank ishi fakulteti",
        "programs": [
            _p("banking", "60410600", "Bank ishi"),
        ],
    },
    {
        "id": "taxes",
        "name": "Soliqlar va byudjet hisobi fakulteti",
        "programs": [
            _p("taxes", "60410300", "Soliqlar va soliqqa tortish"),
        ],
    },
    {
        "id": "accounting",
        "name": "Buxgalteriya hisobi fakulteti",
        "programs": [
            _p("accounting", "60410200", "Buxgalteriya hisobi"),
        ],
    },
]

OTHER_FACULTIES: list[str] = [
    "Sirtqi ta'lim fakulteti",
    "Kechki ta'lim va magistratura fakulteti",
    "Masofaviy va Ikkinchi oliy ta'lim fakulteti",
    "Qo'shma ta'lim fakulteti",
]

JOINT_PROGRAMS: list[str] = [
    '🇬🇧 <a href="https://t.me/iseflseuol">London universiteti (University of London)</a> — Buyuk Britaniya',
    '🇦🇹 <a href="https://t.me/imckremsuz">IMC Krems University of Applied Sciences</a> — Avstriya (QS: 941, THE: 1001–1500)',
    '🇨🇿 <a href="https://t.me/tgeu_fmsop">Praga menejment va texnologiya universiteti</a> — Chexiya',
    '🇮🇩 <a href="https://t.me/ijdp_tsue">Universitas Pendidikan Indonesia</a> — Indoneziya (QS: 951–1000)',
    '🇷🇺 <a href="https://t.me/usue_tsue">Ural davlat iqtisodiyot universiteti</a> — Rossiya',
    '🇧🇾 <a href="https://t.me/tgeu_fmsop">Belarus davlat universiteti</a> — Belarus',
    '🇰🇬 <a href="https://t.me/tgeu_fmsop">M. Risqulbekov nomidagi Iqtisodiyot va tadbirkorlik universiteti</a> — Qirg\'iziston',
    '🇹🇯 <a href="https://t.me/tgeu_fmsop">Tojikiston davlat huquq, biznes va siyosat universiteti</a> — Tojikiston',
    '🇮🇩 <a href="https://t.me/ijdp_tsue">Padjadjaran universiteti</a> — Indoneziya (QS: 596)',
    '🇷🇺 <a href="https://t.me/tgeu_fmsop">Moliya universiteti (RF hukumati huzurida)</a> (QS: 1001–1200)',
    '🇷🇺 <a href="https://t.me/tsuemephimifi">Rossiya Milliy tadqiqotlar yadro universiteti (MEPhI)</a> (QS: 591, THE: 501–600)',
    '🇨🇳 <a href="https://t.me/tgeu_fmsop">Uxan universiteti (Wuhan University)</a> — Xitoy (QS: 801–850, THE: 134)',
    '🇦🇿 <a href="https://t.me/tgeu_fmsop">Ozarbayjon davlat iqtisodiyot universiteti</a> (QS: 1001–1200)',
    '🇷🇺 <a href="https://t.me/tgeu_fmsop">Butunrossiya tashqi savdo akademiyasi</a> — Rossiya',
]


def find_program(program_id: str) -> dict | None:
    for fac in FACULTIES:
        for prog in fac["programs"]:
            if prog["id"] == program_id:
                return prog
    return None


def find_faculty(faculty_id: str) -> dict | None:
    return next((f for f in FACULTIES if f["id"] == faculty_id), None)
