"""FAQ bazasi (statik — MVP).

Har bir element: savol, javob, kalit so'zlar (erkin matnli qidiruv uchun).
Keyingi fazada bu baza PostgreSQL `faq` jadvaliga ko'chiriladi.
"""
from __future__ import annotations

FAQ: list[dict] = [
    {
        "id": 1,
        "question": "Hujjat topshirish qachon boshlanadi?",
        "answer": (
            "Ariza topshirish rasmiy platforma orqali amalga oshiriladi. "
            "Aniq muddatlar uchun «📝 Qabul jarayoni» bo'limiga qarang. "
            "<i>[TODO: aniq sana]</i>"
        ),
        "keywords": ["hujjat", "ariza", "topshirish", "qachon", "muddat", "boshlanadi"],
    },
    {
        "id": 2,
        "question": "Kontrakt summasi qancha?",
        "answer": (
            "Kontrakt summalari yo'nalishga qarab farq qiladi. "
            "«💰 Kontrakt summalari» bo'limidan to'liq ro'yxatni ko'ring."
        ),
        "keywords": ["kontrakt", "summa", "narx", "pul", "to'lov", "qancha", "kontract"],
    },
    {
        "id": 3,
        "question": "O'tish ballari qanday?",
        "answer": (
            "O'tgan yilgi o'tish ballarini har bir yo'nalish kartochkasida "
            "ko'rishingiz mumkin. «🎓 Fakultet va yo'nalishlar» bo'limiga o'ting."
        ),
        "keywords": ["ball", "o'tish", "otish", "ball", "passing", "score", "kerak"],
    },
    {
        "id": 4,
        "question": "Qaysi yo'nalishlar bor?",
        "answer": (
            "Barcha fakultet va yo'nalishlar ro'yxatini «🎓 Fakultet va "
            "yo'nalishlar» bo'limidan topasiz."
        ),
        "keywords": ["yo'nalish", "yonalish", "fakultet", "yvnalish", "mutaxassislik", "qaysi"],
    },
    {
        "id": 5,
        "question": "Yotoqxona bormi?",
        "answer": (
            "Ha. Yotoqxona joylari, narxi va ariza tartibi haqida «🏠 Yotoqxona "
            "va talaba hayoti» bo'limida ma'lumot berilgan."
        ),
        "keywords": ["yotoqxona", "yotoq", "turar joy", "obshejitiya", "joy"],
    },
    {
        "id": 6,
        "question": "Stipendiya beriladimi?",
        "answer": (
            "Davlat, nomli va ijtimoiy stipendiya turlari mavjud. Shartlari "
            "bilan «⭐ Reyting va stipendiyalar» bo'limida tanishing."
        ),
        "keywords": ["stipendiya", "stependiya", "nafaqa", "stipend"],
    },
    {
        "id": 7,
        "question": "Manzil va telefon raqami qayerda?",
        "answer": (
            "Qabul komissiyasi telefoni, manzili va ish vaqti «📞 Bog'lanish» "
            "bo'limida keltirilgan."
        ),
        "keywords": ["manzil", "telefon", "raqam", "qayerda", "aloqa", "bog'lanish", "call"],
    },
]


def search_faq(text: str, limit: int = 3) -> list[dict]:
    """Erkin matnli savol bo'yicha mos FAQ elementlarini qaytaradi.

    Oddiy kalit so'z mosligi (MVP). Keyinroq fuzzy/semantik qidiruvga
    almashtirilishi mumkin.
    """
    text_low = text.lower()
    scored: list[tuple[int, dict]] = []
    for item in FAQ:
        score = sum(1 for kw in item["keywords"] if kw in text_low)
        if score > 0:
            scored.append((score, item))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [item for _, item in scored[:limit]]
