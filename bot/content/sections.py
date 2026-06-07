"""Bo'limlar matni — tsue.uz va rasmiy hujjatlar asosida.

Yillik o'zgaruvchan raqamlar (o'tish bali, kvota, kontrakt summasi)
admission_data.py faylida boshqariladi.
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


ABOUT = (
    "🏛 <b>Universitet haqida</b>\n\n"
    "<b>Toshkent Davlat Iqtisodiyot Universiteti (TDIU)</b> — nafaqat "
    "O'zbekiston, balki butun Markaziy Osiyoda iqtisodiyot, moliya, axborot "
    "texnologiyalari va sun'iy intellekt sohalarida yuqori malakali "
    "mutaxassislar tayyorlaydigan yetakchi oliy ta'lim muassasalaridan biri. "
    "1931-yilda tashkil etilgan.\n\n"
    "🏆 <b>Reyting va e'tirof:</b>\n"
    "• QS Stars <b>5 yulduz</b> — O'zbekistonda birinchi, Markaziy Osiyoda ikkinchi\n"
    "• QS Asia University Rankings 2026: <b>274-o'rin</b> (O'zbekistonda 3-, mintaqada 15-o'rin)\n"
    "• QS Sustainability 2026: dunyoning eng sara 1000 ta universiteti qatorida\n"
    "• QS by subject 2026: «Iqtisodiyot va ekonometrika» — TOP-300 da\n"
    "• THE Impact Ranking: TOP-500 | UI GreenMetric: TOP-250 (respublikada 1-o'rin)\n"
    "• Webometrics: respublikada 1-o'rin\n\n"
    "📊 <b>Bugungi kunda:</b>\n"
    "• 14 fakultet, 45 kafedra, 1 filial\n"
    "• 17 bakalavriat yo'nalishi, 32 magistratura mutaxassisligi\n"
    "• ~50 000 mahalliy va xorijiy talaba\n"
    "• ~2 500 professor-o'qituvchi (≈70% ilmiy darajaga ega)\n"
    "• 2 akademik litsey va 11 texnikum\n\n"
    "🌍 <b>Xalqaro hamkorlik:</b>\n"
    "• 200+ nufuzli universitet bilan hamkorlik (MIT, Sapienza, Tsukuba va b.)\n"
    "• LSE, IMC Krems, Universitas Pendidikan Indonesia, Padjadjaran kabi 12 ta "
    "universitet bilan «1+1», «3+1» qo'sh diplom dasturlari\n"
    "• Erasmus+ va akademik almashinuv; 100+ xorijiy professor; inglizcha guruhlar\n\n"
    "✅ <b>Sifat va akkreditatsiya:</b>\n"
    "• 7 yo'nalish ACBSP va NAAR xalqaro akkreditatsiyasidan o'tgan\n"
    "• «Buxgalteriya hisobi» dasturi ACCA tomonidan tan olingan\n"
    "• Bitiruvchilar bandligi 95%+\n\n"
    "🔬 <b>Innovatsion markazlar:</b> «Eksperimental iqtisodiyot» laboratoriyasi, "
    "IT Park bilan «Digital Finance» akseleratsiya markazi, Anhalt universiteti "
    "bilan «Yashil iqtisodiyot» markazi.\n\n"
    "🌐 Sayt: https://tsue.uz\n"
    "📍 Manzil: 100066, Toshkent, Islom Karimov ko'chasi, 49"
)

ADMISSION_PROCESS = (
    "📝 <b>Qabul jarayoni</b>\n\n"
    "1️⃣ <b>Ro'yxatdan o'tish</b>\n"
    "Davlat qabul platformasi (my.gov.uz / qabul.edu.uz) orqali ariza topshiriladi.\n\n"
    "2️⃣ <b>Test imtihoni</b>\n"
    "Davlat test markazi (DTM) belgilagan tartibda blok fanlardan test topshiriladi.\n\n"
    "3️⃣ <b>Natijalar va tavsiya</b>\n"
    "O'tish ballari e'lon qilinadi, abituriyentlar tavsiya etiladi.\n\n"
    "4️⃣ <b>Hujjat topshirish va shartnoma</b>\n"
    "Tavsiya etilganlar hujjatlarini topshiradi va (kontrakt asosida) shartnoma imzolaydi.\n\n"
    "📄 <b>Kerakli hujjatlar (odatda):</b> pasport/ID, ma'lumotnoma yoki diplom, 3x4 rasm, tibbiy ma'lumotnoma.\n\n"
    f"ℹ️ Aniq muddatlar va batafsil yo'riqnoma: {WEBSITE}/admission\n"
    f"☎️ Qabul komissiyasi: {', '.join(ADMISSION_PHONES)}"
)

EDUCATION = (
    "📚 <b>Ta'lim tizimi</b>\n\n"
    "🎓 <b>Bosqichlar:</b>\n"
    "• Bakalavriat (17 yo'nalish)\n"
    "• Magistratura (32 mutaxassislik)\n"
    "• Doktorantura (PhD / DSc)\n\n"
    "🕘 <b>Ta'lim shakllari:</b> kunduzgi, sirtqi, kechki va masofaviy (yo'nalishga qarab).\n\n"
    "📐 <b>Tizim:</b> kredit-modul tizimi; semestrlar, oraliq va yakuniy nazoratlar orqali baholanadi.\n\n"
    "🤝 <b>Qo'shma dasturlar:</b>\n" + "\n".join(f"• {p}" for p in JOINT_PROGRAMS)
)

RATING = (
    "⭐ <b>Reyting va stipendiyalar</b>\n\n"
    "🏆 <b>Reytinglar:</b>\n"
    "• QS Stars 5 yulduz (O'zbekistonda 1-, Markaziy Osiyoda 2-o'rin)\n"
    "• QS Asia 2026: 274-o'rin | QS Sustainability 2026: TOP-1000\n"
    "• THE Impact: TOP-500 | UI GreenMetric: TOP-250\n\n"
    "💵 <b>Stipendiya turlari:</b>\n"
    "• Davlat stipendiyasi — grant asosida o'qiydigan, o'zlashtirishi yuqori talabalarga.\n"
    "• Nomli/maxsus stipendiyalar — yuqori natija ko'rsatgan talabalarga.\n"
    "• Ijtimoiy yordam — ijtimoiy himoyaga muhtoj talabalar uchun.\n\n"
    f"ℹ️ Batafsil shartlar: {WEBSITE}"
)

DORMITORY = (
    "🏠 <b>Yotoqxona va talaba hayoti</b>\n\n"
    "🛏 <b>Talabalar turar joyi:</b>\n"
    "Universitetda 10 dan ortiq talabalar turar joyi mavjud — zamonaviy infratuzilma, "
    "sport va madaniy maydonchalar bilan jihozlangan.\n"
    "<i>Joriy joylar soni, narxi va ariza tartibi qabul davrida e'lon qilinadi.</i>\n\n"
    "🎭 <b>Talaba hayoti:</b>\n"
    "• Jamoaviy klublar va to'garaklar\n"
    "• Sport inshootlari, «Karaoke» klubi va kibersport zallari\n"
    "• Madaniy tadbirlar, tanlovlar («Talabalar bahori» va b.)\n"
    "• Kafeteriyalar, kitob do'koni\n"
    "• «Kariera markazi» — bitiruvchilar bandligi 95%+\n\n"
    f"ℹ️ Batafsil: {WEBSITE}"
)

INTERNATIONAL = (
    "🌍 <b>Xalqaro imkoniyatlar</b>\n\n"
    "🤝 <b>Qo'sh diplom dasturlari («1+1», «3+1»):</b>\n"
    + "\n".join(f"• {p}" for p in JOINT_PROGRAMS)
    + "\n\n"
    "🔄 <b>Imkoniyatlar:</b>\n"
    "• 200+ nufuzli universitet bilan hamkorlik (MIT, Sapienza, Tsukuba va b.)\n"
    "• Erasmus+ va akademik almashinuv dasturlari\n"
    "• Xorijda malaka oshirish va amaliyot\n"
    "• 100+ xorijiy professor; barcha yo'nalishlarda inglizcha guruhlar\n"
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
    head = f"💰 <b>Kontrakt summalari — bazaviy ({ad.YEAR})</b>\n\n"
    any_amount = any(
        ad.get(p["id"])["contract_amount"] is not None
        for f in FACULTIES for p in f["programs"]
    )
    if not any_amount:
        return (
            head
            + "Joriy o'quv yili kontrakt summalari hozircha kiritilmagan.\n\n"
            f"ℹ️ Rasmiy ma'lumot: {WEBSITE}"
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
    lines.append("<i>Eslatma: yuqoridagilar bazaviy summalar. Ball darajasiga qarab "
                 "tabaqalashtirilgan (oshirilgan) summa belgilanishi mumkin.</i>")
    return "\n".join(lines)


def faculties_intro() -> str:
    return (
        "🎓 <b>Fakultet va yo'nalishlar</b>\n\n"
        "TDIU da 17 ta bakalavriat yo'nalishi mavjud. Quyidagi fakultetlardan "
        "birini tanlang — yo'nalishlar ro'yxati chiqadi.\n\n"
        "ℹ️ Shuningdek, sirtqi, kechki, masofaviy va qo'shma ta'lim dasturlari mavjud."
    )


def program_card(program_id: str) -> str:
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


TEXTS: dict[str, str] = {
    "about": ABOUT,
    "admission": ADMISSION_PROCESS,
    "education": EDUCATION,
    "rating": RATING,
    "dormitory": DORMITORY,
    "international": INTERNATIONAL,
    "contact": CONTACT,
}
