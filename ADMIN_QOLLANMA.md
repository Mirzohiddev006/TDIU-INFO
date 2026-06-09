# Admin panel — to'liq qo'llanma

## 1. Loyiha 3 qismdan iborat
| Qism | Nima | Render dagi nomi |
|------|------|------------------|
| 🤖 Bot + API | Telegram bot va admin API (bitta servis) | `tdiu-bot-api` |
| 🖥 Admin panel | Boshqaruv sahifasi (React) | `tdiu-admin` |
| 🗄 Baza | PostgreSQL | `tdiu-db` |

> Admin panel API'ni o'zida saqlamaydi. U **`tdiu-bot-api`** servisidagi API'larga ulanadi.

## 2. Kirish parollari (3 ta tayyor login)
| Login | Parol | Rol | Nima qila oladi |
|-------|-------|-----|-----------------|
| `admin` | `admin123` | Super-admin | HAMMA narsa |
| `menejer` | `menejer123` | Kontent-menejer | Kontent, ball, kvota, kontrakt, FAQ, broadcast |
| `operator` | `operator123` | Operator | Faqat jonli yordam (operator chat) |

> ⚠️ Bular **standart parollar** — keyin albatta o'zgartiring (`render.yaml` → `ADMIN_PASSWORD`,
> yoki `core/seed.py` → `ADMIN_USERS`).

## 3. Admin panelni ochish
1. Render'da **`tdiu-admin`** servisi sahifasini oching → tepasidagi manzil (`https://tdiu-admin.onrender.com` yoki o'xshash) ni bosing.
2. Login oynasi chiqadi. Yuqorida **API holati** ko'rsatkichi bor:
   - 🟢 **Ulangan** — hammasi joyida, kiring.
   - 🔴 **Ulanmadi** — pastdagi "Front ishlamayapti" bo'limiga qarang.
3. `admin` / `admin123` bilan kiring.

## 4. Bo'limlar va ulardan foydalanish

### 📊 Statistika
Bot foydalanuvchilari soni, jami amallar, javobsiz savollar va mashhur bo'limlar grafigi.

### 📝 Ball / Kvota / Kontrakt — ENG MUHIM
1. Yuqorida **qidiruv** orqali yo'nalishni toping (nomi yoki kodi bo'yicha).
2. Har bir yo'nalish qatorida maydonlarni to'ldiring:
   - Grant (Uz), Grant (Ru) — davlat granti o'tish bali
   - Kontr. (Uz), Kontr. (Ru) — to'lov-kontrakt o'tish bali
   - Grant o'rin, Kontr. o'rin — kvota (o'rinlar soni)
   - Kontrakt summa — bazaviy summa (so'mda)
3. **"Saqlash"** ni bosing. ✅ **Botda darhol aks etadi.** Bo'sh qoldirilsa "tez orada" deb ko'rsatiladi.

### 🏛 Fakultetlar
Fakultet qo'shish / o'chirish.

### 🎓 Yo'nalishlar
Barcha 17 yo'nalish ro'yxati (kod, fakultet, shakl).

### 📄 Bo'lim matnlari
"Universitet haqida", "Qabul jarayoni" kabi matnlarni tahrirlash. HTML teglar (`<b>`) qo'llab-quvvatlanadi. Saqlasangiz botda yangilanadi.

### ❓ FAQ
Savol-javob qo'shish / o'chirish. Kalit so'zlar (vergul bilan) — bot matnli savolni shu so'zlar bo'yicha topadi.

### 💬 Operator (jonli yordam)
1. Foydalanuvchi botda "Operator bilan bog'lanish" → savol yozsa, bu yerda **ochiq suhbat** paydo bo'ladi.
2. Suhbatni tanlang → xabarlarni o'qing → pastdan javob yozib **Yuborish**. Javob foydalanuvchiga bot orqali boradi.
3. Tugatish uchun "Suhbatni yopish".

### 📢 Ommaviy xabar (broadcast)
Matn yozib "Hammaga yuborish" → barcha bot foydalanuvchilariga yuboriladi. (Bot ishlab turishi kerak.)

## 5. "Front ishlamayapti" — tekshirish va tuzatish

**Avval login oynasidagi API holatiga qarang:**

**🔴 "Ulanmadi" bo'lsa** (eng keng tarqalgan sabab):
1. **API manzili noto'g'ri.** `admin/dist/config.js` ni oching, `window.__API_URL__` to'g'ri backend manzili ekanini tekshiring:
   ```js
   window.__API_URL__ = "https://SIZNING-tdiu-bot-api.onrender.com/api";
   ```
   Aniq manzilni Render'da `tdiu-bot-api` servisi sahifasidan oling. O'zgartirsangiz GitHub'ga push qiling.
2. **Backend uxlab qolgan.** Render bepul servis 15 daqiqada uxlaydi; birinchi so'rov 30-50 soniya kechikadi. Biroz kuting va sahifani yangilang.
3. **Backend ishga tushmagan.** Render'da `tdiu-bot-api` servisi "Live" (yashil) ekanini tekshiring. Logs'da xato bo'lsa, menga tashlang.

**Sahifa umuman ochilmasa (oq ekran):**
1. `tdiu-admin` servisi muvaffaqiyatli deploy bo'lganini tekshiring. Build buyrug'i `echo` bo'lishi va Publish papkasi `admin/dist` bo'lishi kerak (npm build EMAS).
2. Eng so'nggi kod (tayyor `admin/dist`) GitHub'ga push qilinganini tasdiqlang.

**Login bo'lmasa ("noto'g'ri parol"):**
- API "Ulangan" bo'lsa, `admin` / `admin123` ni ishlating. Agar Render'da `ADMIN_PASSWORD` ni boshqacha qilgan bo'lsangiz, o'shani kiriting.

## 6. Parollarni o'zgartirish
- Super-admin: Render → `tdiu-bot-api` → Environment → `ADMIN_PASSWORD` ni o'zgartiring → Manual Deploy.
- `menejer` / `operator`: `core/seed.py` dagi `ADMIN_USERS` ro'yxatini tahrirlang (yangi baza uchun) yoki SQL orqali yangilang.

> Eslatma: parol o'zgarishi faqat **yangi/bo'sh bazada** avtomatik qo'llanadi (seed bir marta ishlaydi).
> Mavjud bazada parolni o'zgartirish uchun foydalanuvchini qayta yaratish kerak.
