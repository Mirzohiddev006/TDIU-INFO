"""Bo'limlar matni — tsue.uz va rasmiy hujjatlar asosida."""
from __future__ import annotations

from bot.content import admission_data as ad
from bot.content.programs import (
    FACULTIES,
    JOINT_PROGRAMS,
    OTHER_FACULTIES,
    find_program,
)

MENU: dict[str, str] = {
    "about": "Universitet haqida",
    "faculties": "Fakultet va yo'nalishlar",
    "quota": "Qabul kvotasi",
    "contract": "Kontrakt summalari",
    "admission": "Qabul jarayoni",
    "education": "Ta'lim tizimi",
    "rating": "Ilmiy faoliyat va stipendiyalar",
    "dormitory": "Yotoqxona va talaba hayoti",
    "international": "Xalqaro imkoniyatlar",
    "faq": "Tez-tez so'raladigan savollar",
    "contact": "Bog'lanish",
    "operator": "Operator bilan bog'lanish",
}

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
    "Assalomu alaykum!\n\n"
    "<b>Toshkent davlat iqtisodiyot universitetining</b> rasmiy axborot botiga "
    "xush kelibsiz.\n\n"
    "Bu bot orqali siz qabul jarayoni, yo'nalishlar, o'tish ballari, kontrakt "
    "to'lovlari va universitetning boshqa muhim ma'lumotlari bilan tanishishingiz "
    "mumkin — kechayu kunduz, hech qanday kutish talab qilmagan holda.\n\n"
    "Kerakli bo'limni tanlang yoki savolingizni yozib yuboring:"
)

ABOUT = (
    "🏛 <b>Universitet haqida</b>\n\n"
    "Toshkent davlat iqtisodiyot universiteti nafaqat O'zbekistonda, balki "
    "xalqaro maydonda ham yetakchi o'rinlarni egallab kelmoqda. "
    "Universitetimizning so'nggi muvaffaqiyatlari bilan tanishing:\n\n"
    "🌟 <b>QS Stars 5 Stars</b> — TDIU QS Stars 5 yulduziga ega bo'lgan Markaziy "
    "Osiyodagi ikkinchi va O'zbekistondagi birinchi oliy ta'lim muassasasidir!\n\n"
    "🌍 <b>QS Asia University Rankings – 2026:</b>\n"
    "• Osiyo reytingida: 274-o'rin;\n"
    "• O'zbekiston OTMlari ichida: 3-o'rin;\n"
    "• Markaziy Osiyo davlatlari ichida: 15-o'rin.\n\n"
    "🌱 <b>Barqarorlik va Innovatsiyalar:</b>\n"
    "• QS Sustainability Rankings – 2026: dunyoning eng sara 1000 ta OTM qatoridan joy oldi.\n"
    "• THE Impact Ranking: dunyoning eng kuchli TOP–500 universiteti qatorida.\n"
    "• UI Greenmetric: dunyoning 250 ta eng yaxshi \"yashil\" universitetlari qatorida hamda "
    "ekologik barqarorlik va innovatsiyalar bo'yicha Respublikada 1-o'rin!\n\n"
    "💻 <b>Raqamli ta'lim va ochiqlik:</b>\n"
    "• Webometrics: raqamli makondagi faolligi bo'yicha O'zbekiston oliygohlari o'rtasida 1-o'rin!\n\n"
    "📚 <b>\"QS by subject – 2026\" yo'nalishlar bo'yicha dunyo reytingi:</b>\n"
    "🔸 TOP 300: Iqtisodiyot va ekonometrika (Economics & Econometrics) — 251–300-o'rin;\n"
    "🔸 TOP 300: Huquq (Law) — 251–300-o'rin;\n"
    "🔸 TOP 500: Ijtimoiy fanlar va menejment (Social Sciences & Management) — 451–500-o'rin;\n"
    "🔸 TOP 600: Biznes va menejment tadqiqotlari (Business & Management Studies) — 551–600-o'rin.\n\n"
    "✅ <b>Sifat va akkreditatsiya:</b>\n"
    "• 7 ta yo'nalish ACBSP va NAAR xalqaro akkreditatsiyasidan o'tgan;\n"
    "• \"Buxgalteriya hisobi\" dasturi ACCA tomonidan tan olingan;\n"
    "• Bitiruvchilar bandligi 95%+.\n\n"
    "🌐 Sayt: https://tsue.uz\n"
    "📍 Manzil: 100066, Toshkent, Islom Karimov ko'chasi, 49\n"
    "🎬 <a href=\"https://youtu.be/5fuw8rnBVyI?si=n3PKnpgeMumvVIbW\">Universitet haqida video</a>"
)

ADMISSION_PROCESS = (
    "📝 <b>Qabul jarayoni</b>\n\n"
    "Qabul jarayonlari «avval test, so'ng tanlov» tamoyiliga muvofiq quyidagi "
    "ikki bosqichda amalga oshiriladi:\n\n"
    "1️⃣ <b>Birinchi bosqich:</b>\n"
    "Abituriyentlar 5-iyundan 25-iyunga qadar (25-iyun kuni ham) test sinovi "
    "topshirish uchun ro'yxatdan o'tadi. Bunda abituriyentlar faqat test sinovi "
    "topshiriladigan fanlar majmuasi, ta'lim tili va test topshirish hududini, "
    "hamda kasbiy (ijodiy) imtihon bo'lsa, ushbu imtihonni topshiradigan oliygohni tanlaydi.\n"
    "Ya'ni birinchi bosqichda universitet yoki institut tanlanmaydi — abituriyent "
    "faqat qaysi fandan, qaysi tilda, qaysi hududda test topshirishini belgilaydi xolos.\n"
    "✅ Imtihonlar iyul–avgust oylarida o'tkaziladi.\n\n"
    "2️⃣ <b>Ikkinchi bosqich:</b>\n"
    "Test sinovlari to'liq yakunlanganidan so'ng abituriyent 15 kun davomida oliy "
    "ta'lim muassasasi, bakalavriat ta'lim yo'nalishi va ta'lim shaklini tanlaydi.\n"
    "Ya'ni o'zining olgan baliga qarab, testlar o'tib bo'lgandan keyin qaysi "
    "oliygohning qaysi yo'nalishiga topshirishini tanlaydi (o'ylab olishga 15 kun beriladi).\n\n"
    "<b>O'qishga kira olmaganlar nima qiladi?</b>\n"
    "• Oltinchi yo'nalishni tanlash imkoni beriladi: tanlagan 5 ta yo'nalishga "
    "tavsiya etilmagan yoki yo'nalish tanlash esidan chiqqan abituriyentlar fanlar "
    "majmuasi mos va bali yetadigan oltinchi yo'nalishni ham tanlashi mumkin.\n"
    "• Testda to'plagan bali bilan kollej va (yoki) texnikumni tanlash mumkin. "
    "Buning uchun OTMlarga qabulning yakuniy natijasi (mandat) e'lon qilingach yana 10 kun beriladi.\n\n"
    "📲 Ro'yxatdan o'tish: my.uzbmb.uz"
)

EDUCATION = (
    "📚 <b>Ta'lim tizimi</b>\n\n"
    "🎓 <b>Bosqichlar:</b>\n"
    "• Bakalavriat (17 yo'nalish)\n"
    "• Magistratura (32 mutaxassislik)\n"
    "• Doktorantura (PhD / DSc)\n\n"
    "🕘 <b>Ta'lim shakllari:</b> kunduzgi, sirtqi, kechki va masofaviy (yo'nalishga qarab).\n\n"
    "📐 <b>Tizim:</b> kredit-modul tizimi; «5+1» formati — soha korxonalarida 35 ta kafedra filiali; simulyatsion o'quv laboratoriyalari.\n\n"
    "🤝 <b>Qo'shma dasturlar:</b>\n" + "\n".join(f"• {p}" for p in JOINT_PROGRAMS)
)

RATING = (
    "⭐ <b>Ilmiy faoliyat va stipendiyalar</b>\n\n"
    "🔬 <b>Ilmiy faoliyat:</b>\n"
    "• 1355 professor-o'qituvchi; ilmiy salohiyat 63,4%\n"
    "• 2025: 224 monografiya, 2809 ilmiy maqola\n"
    "• Scopus: 2021-y. 130 → 2025-y. ~926 publikatsiya (7,1 barobar o'sish), Q1+Q2 ulushi 60%+\n"
    "• Web of Science: 2023–2025 da 901 maqola\n"
    "• 5 ilmiy kengash, 12 ixtisoslik; 2025-y. 271 dissertatsiya himoyasi (53 DSc, 218 PhD)\n"
    "• Fan olimpiadalarida respublika OTMlari orasida 1-o'rin\n"
    "• «Digital Finance» markazi: 58 startap, 1,2 mlrd so'm; «Eksperimental Iqtisodiyot» laboratoriyasi (Moody's ORBIS — 600 mln+ tashkilot bazasi)\n\n"
    "💵 <b>Stipendiyalar:</b>\n"
    "• Davlat stipendiyasi (grant asosida, yuqori o'zlashtirganlarga)\n"
    "• Prezident stipendiyasi va granti\n"
    "• Islom Karimov, Abu Rayhon Beruniy, Alisher Navoiy nomidagi davlat stipendiyalari\n"
    "• Ijtimoiy yordam — himoyaga muhtoj talabalarga\n\n"
    f"ℹ️ Batafsil: {WEBSITE}"
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
    "Hozirgi kunda TDIU dunyoning turli mintaqalaridagi <b>14 ta yetakchi universitet</b> "
    "bilan qo'shma ta'lim dasturlarini shakllantirmoqda:\n\n"
    + "\n".join(f"• {p}" for p in JOINT_PROGRAMS)
    + "\n\n"
    "TDIU talabalari ikki tomonlama diplomlarga (TDIU va hamkor OTM diplomi) ega bo'lib, "
    "zamonaviy bilim va ko'nikmalar bilan jahon miqyosida tan olingan mutaxassis sifatida "
    "yetishib chiqmoqdalar.\n\n"
    "🔄 <b>Akademik almashinuv:</b> Erasmus+, Global Korea, Germaniya (Saksoniya), Slovakiya "
    "grantlari; 2025-yilda ~150 talaba xorijga o'qishga yuborilgan; 150+ xorijiy professor jalb etilgan.\n\n"
    "👨‍🎓 <b>Xorijiy talabalar:</b> 15 davlatdan 610+ talaba.\n\n"
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
            "Hozircha yo'nalishlar ro'yxatini «Fakultet va yo'nalishlar» "
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
