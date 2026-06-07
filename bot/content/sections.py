"""Bo'limlar matni — tsue.uz rasmiy ma'lumotlari asosida.

Yillik o'zgaruvchan raqamlar (o'tish bali, kvota, kontrakt summasi)
admission_data.py faylida boshqariladi. Bo'lim matnlari shu fayldan o'qiydi.
"""
from __future__ import annotations

from bot.content import admission_data as ad
from bot.content.programs import (
    FACULTIES,
    JOINT_PROGRAMS,
    OTHER_FACULTIES,
    find_program,
)

# Asosiy menyu bo'limlari: kalit -> tugma yorlig'i
MENU: dict[str, str] = {
    "about": "🏛 Universitet haqida",
    "faculties": "🎓 Fakultet va yo'nalishlar",
    "quota": "📊 Qabul kvotasi",
    "contract": "💰 Kontrakt summalari",
    "admission": "📝 Qabul jarayoni",
    "education": "📚 Ta'lim tizimi",
    "rating": "⭐ Reyting va stipendiyalar",
    "dormitory": "🏠 Yotoqxona va talaba hayoti",
    "international": "🌍 Xalqaro imkoniyatlar",
    "faq": "❓ Tez-tez so'raladigan savollar",
    "contact": "📞 Bog'lanish",
    "operator": "💬 Operator bilan bog'lanish",
}

# Rasmiy kontaktlar (tsue.uz)
PHONES = [
    "+998 71 245 42 43",
    "+998 71 239 01 59",
    "+998 71 239 28 78",
    "+998 71 239 28 77",
    "+998 71 239 28 79",
]
ADMISSION_PHONES = ["+998 71 239 28 78", "+998 71 239 27 23"]
EMAIL = "info@tsue.uz"
ADMISSION_EMAIL = "admission@tsue.uz"
ADDRESS = "100066, Toshkent shahri, Islom Karimov ko'chasi, 49-uy"
WEBSITE = "https://tsue.uz"
WORK_HOURS = "Dushanba–Juma, 09:00 – 18:00"

WELCOME = (
    "Assalomu alaykum! 👋\n\n"
    "<b>Toshkent Davlat Iqtisodiyot Universiteti (TDIU)</b> rasmiy ma'lumot "
    "botiga xush kelibsiz.\n\n"
    "Bu yerda yo'nalishlar, o'tish ballari, kontrakt summalari, qabul jarayoni "
    "va boshqa savollarga 24/7 javob olishingiz mumkin.\n\n"
    "Quyidagi bo'limlardan birini tanlang yoki savolingizni shunchaki yozib yuboring 👇"
)


# ── Statik bo'limlar (tsue.uz dan) ──────────────────────────────────────

ABOUT = (
    "🏛 <b>Universitet haqida</b>\n\n"
    "<b>Toshkent Davlat Iqtisodiyot Universiteti (TDIU)</b> — iqtisodiy "
    "yo'nalishlar bo'yicha respublikadagi tayanch oliy ta'lim muassasasi.\n\n"
    "📜 Universitet 1931-yil 31-avgustda O'rta Osiyo moliya-iqtisod instituti "
    "sifatida tashkil topgan. Oliy malakali iqtisodchilarni tayyorlash esa "
    "1918-yil 12-mayda boshlangan.\n\n"
    "🎯 <b>Missiya:</b> ilm-fan, ta'lim va innovatsiyalarni rivojlantirish "
    "orqali iqtisodiyot va insoniyat taraqqiyotiga munosib hissa qo'shish, "
    "kelajak yetakchilarini tayyorlash.\n\n"
    "📊 <b>Bugungi kunda:</b>\n"
    "• 24 ta bakalavriat yo'nalishi\n"
    "• 28 ta magistratura mutaxassisligi\n"
    "• 14 ta fakultet va filiallar\n"
    "• Xalqaro qo'shma ta'lim dasturlari\n\n"
    f"🌐 Sayt: {WEBSITE}\n"
    f"📍 Manzil: {ADDRESS}"
)

ADMISSION_PROCESS = (
    "📝 <b>Qabul jarayoni</b>\n\n"
    "1️⃣ <b>Ro'yxatdan o'tish</b>\n"
    "Davlat qabul platformasi (my.gov.uz / qabul.edu.uz) orqali ariza "
    "topshiriladi.\n\n"
    "2️⃣ <b>Test imtihoni</b>\n"
    "Davlat test markazi (DTM) belgilagan tartibda blok fanlardan test "
    "topshiriladi.\n\n"
    "3️⃣ <b>Natijalar va tavsiya</b>\n"
    "O'tish ballari e'lon qilinadi, abituriyentlar tavsiya etiladi.\n\n"
    "4️⃣ <b>Hujjat topshirish va shartnoma</b>\n"
    "Tavsiya etilganlar hujjatlarini topshiradi va (kontrakt asosida) "
    "shartnoma imzolaydi.\n\n"
    "📄 <b>Kerakli hujjatlar (odatda):</b> pasport/ID, ma'lumotnoma yoki "
    "diplom, 3x4 rasm, tibbiy ma'lumotnoma.\n\n"
    f"ℹ️ Aniq muddatlar va batafsil yo'riqnoma: {WEBSITE}/admission\n"
    f"☎️ Qabul komissiyasi: {', '.join(ADMISSION_PHONES)}"
)

EDUCATION = (
    "📚 <b>Ta'lim tizimi</b>\n\n"
    "🎓 <b>Bosqichlar:</b>\n"
    "• Bakalavriat (24 yo'nalish)\n"
    "• Magistratura (28 mutaxassislik)\n"
    "• Doktorantura (PhD / DSc)\n\n"
    "🕘 <b>Ta'lim shakllari:</b> kunduzgi, sirtqi, kechki va masofaviy "
    "(yo'nalishga qarab).\n\n"
    "📐 <b>Tizim:</b> kredit-modul tizimi asosida; semestrlar, oraliq va "
    "yakuniy nazoratlar orqali baholanadi.\n\n"
    "🤝 <b>Qo'shma dasturlar:</b>\n" + "\n".join(f"• {p}" for p in JOINT_PROGRAMS)
)

RATING = (
    "⭐ <b>Reyting va stipendiyalar</b>\n\n"
    "🏆 <b>Reytinglar:</b>\n"
    "TDIU milliy va xalqaro reytinglarda (jumladan QS mintaqaviy reytinglar) "
    "ishtirok etadi va iqtisodiy ta'lim bo'yicha mamlakatdagi yetakchi "
    "universitetlardan biri hisoblanadi.\n\n"
    "💵 <b>Stipendiya turlari:</b>\n"
    "• Davlat stipendiyasi — grant asosida o'qiydigan, o'zlashtirishi yuqori "
    "talabalarga.\n"
    "• Nomli/maxsus stipendiyalar — yuqori natija ko'rsatgan talabalarga.\n"
    "• Ijtimoiy yordam — ijtimoiy himoyaga muhtoj talabalar uchun.\n\n"
    f"ℹ️ Batafsil shartlar: {WEBSITE}"
)

DORMITORY = (
    "🏠 <b>Yotoqxona va talaba hayoti</b>\n\n"
    "🛏 <b>Talabalar turar joyi:</b>\n"
    "Universitet talabalar uchun turar joy (yotoqxona) bilan ta'minlaydi. "
    "Joylar cheklangan bo'lib, ustuvorlik hududdan kelgan va ijtimoiy himoyaga "
    "muhtoj talabalarga beriladi.\n"
    "<i>Joriy joylar soni, narxi va ariza tartibi qabul davrida e'lon qilinadi.</i>\n\n"
    "🎭 <b>Talaba hayoti:</b>\n"
    "• Jamoaviy klublar va to'garaklar\n"
    "• Sport inshootlari va musobaqalar\n"
    "• Madaniy tadbirlar, tanlovlar (\"Talabalar bahori\" va b.)\n"
    "• Kafeteriyalar, kitob do'koni\n"
    "• Imkoniyati cheklangan talabalar uchun qulayliklar\n\n"
    f"ℹ️ Batafsil: {WEBSITE}"
)

INTERNATIONAL = (
    "🌍 <b>Xalqaro imkoniyatlar</b>\n\n"
    "🤝 <b>Qo'shma ta'lim dasturlari:</b>\n"
    + "\n".join(f"• {p}" for p in JOINT_PROGRAMS)
    + "\n\n"
    "🔄 <b>Imkoniyatlar:</b>\n"
    "• Xalqaro grantlar va almashinuv dasturlari\n"
    "• Xorijda malaka oshirish va amaliyot\n"
    "• Xalqaro hamkorlik memorandumlari\n"
    "• MITx MicroMasters dasturi (TSUE)\n"
    "• Xorijiy talabalar uchun ta'lim imkoniyatlari\n\n"
    f"ℹ️ Batafsil: {WEBSITE}"
)

CONTACT = (
    "📞 <b>Bog'lanish (Qabul komissiyasi)</b>\n\n"
    "☎️ <b>Call-markaz:</b>\n" + "\n".join(f"• {p}" for p in PHONES) + "\n\n"
    "📋 <b>Qabul komissiyasi:</b>\n" + "\n".join(f"• {p}" for p in ADMISSION_PHONES) + "\n\n"
    f"📧 Email: {EMAIL}\n"
    f"📧 Qabul: {ADMISSION_EMAIL}\n"
    f"🕘 Ish vaqti: {WORK_HOURS}\n"
    f"📍 Manzil: {ADDRESS}\n"
    f"🌐 Sayt: {WEBSITE}"
)


def quota_text() -> str:
    """Qabul kvotasi — admission_data dan, hozircha bo'sh bo'lsa eslatma."""
    head = f"📊 <b>Qabul kvotasi ({ad.YEAR})</b>\n\n"
    if not ad.has_any_quota():
        return (
            head
            + "Joriy o'quv yili uchun davlat granti va to'lov-kontrakt o'rinlari "
            "soni hozircha kiritilmagan.\n\n"
            "🔔 Qabul komissiyasi raqamlarni e'lon qilishi bilan shu yerda "
            "yo'nalishlar bo'yicha to'liq kvota ko'rsatiladi.\n\n"
            "Hozircha yo'nalishlar ro'yxatini «🎓 Fakultet va yo'nalishlar» "
            "bo'limidan ko'rishingiz mumkin."
        )
    lines = [head]
    for fac in FACULTIES:
        rows = []
        for prog in fac["programs"]:
            d = ad.get(prog["id"])
            if d["grant_places"] is not None or d["contract_places"] is not None:
                rows.append(
                    f"  • {prog['name']}: grant {ad._fmt_places(d['grant_places'])}, "
                    f"kontrakt {ad._fmt_places(d['contract_places'])}"
                )
        if rows:
            lines.append(f"<b>{fac['name']}</b>")
            lines.extend(rows)
            lines.append("")
    return "\n".join(lines)


def contract_text() -> str:
    """Kontrakt summalari — admission_data dan."""
    head = f"💰 <b>Kontrakt summalari ({ad.YEAR})</b>\n\n"
    any_amount = any(
        ad.get(p["id"])["contract_amount"] is not None
        for f in FACULTIES for p in f["programs"]
    )
    if not any_amount:
        return (
            head
            + "Joriy o'quv yili kontrakt summalari hozircha kiritilmagan.\n\n"
            "🔔 Rasmiy summalar e'lon qilinishi bilan har bir yo'nalish bo'yicha "
            "shu yerda va yo'nalish kartochkalarida ko'rsatiladi.\n\n"
            f"ℹ️ Rasmiy ma'lumot: {WEBSITE}/page/contract-prices-2024"
        )
    lines = [head]
    for fac in FACULTIES:
        rows = []
        for prog in fac["programs"]:
            amt = ad.get(prog["id"])["contract_amount"]
            if amt is not None:
                rows.append(f"  • {prog['name']}: {ad._fmt_amount(amt)}")
        if rows:
            lines.append(f"<b>{fac['name']}</b>")
            lines.extend(rows)
            lines.append("")
    return "\n".join(lines)


def faculties_intro() -> str:
    return (
        "🎓 <b>Fakultet va yo'nalishlar</b>\n\n"
        "TDIU da 24 ta bakalavriat yo'nalishi mavjud. Quyidagi fakultetlardan "
        "birini tanlang — yo'nalishlar ro'yxati chiqadi.\n\n"
        "ℹ️ Shuningdek, sirtqi, kechki, masofaviy va filial fakultetlari, "
        "hamda xalqaro qo'shma dasturlar mavjud."
    )


def program_card(program_id: str) -> str:
    """Yo'nalish kartochkasi — kod, shakl, til + ball/kontrakt (admission_data)."""
    prog = find_program(program_id)
    if not prog:
        return "Yo'nalish topilmadi."
    return (
        f"🎓 <b>{prog['name']}</b>\n\n"
        f"🔢 Kodi: <code>{prog['code']}</code>\n"
        f"🕘 Ta'lim shakli: {prog['form']}\n"
        f"🌐 O'qitish tili: {prog['lang']}\n\n"
        f"{ad.admission_lines(program_id)}"
    )


# Statik matnli bo'limlar (callback key -> matn)
TEXTS: dict[str, str] = {
    "about": ABOUT,
    "admission": ADMISSION_PROCESS,
    "education": EDUCATION,
    "rating": RATING,
    "dormitory": DORMITORY,
    "international": INTERNATIONAL,
    "contact": CONTACT,
}
