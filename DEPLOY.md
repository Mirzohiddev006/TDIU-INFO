# Render.com ga joylashtirish — TDIU Info Bot + Admin panel

Loyiha 2 ta Render servisi + 1 ta tashqi bepul baza (Neon) dan iborat:
1. **Neon Postgres** (bepul, alohida) — doimiy ma'lumotlar bazasi
2. **tdiu-bot-api** — bot + admin API bitta web servisda (Render)
3. **tdiu-admin** — React admin panel, static site (Render)

> **Nega Neon?** Render bepul tarifda akkauntda faqat BITTA bepul Postgres ruxsat etiladi.
> Sizda allaqachon bitta bor (currency). Shuning uchun TDIU bazasini bepul **Neon**'da
> ochamiz — currency'ga tegmaymiz, ikkalasi ham bepul ishlaydi.

## 0. Tayyorgarlik
1. Loyihani **GitHub**'ga push qiling (`.env` git'ga tushmaydi).
2. @BotFather'dan bot tokeni tayyorlang.

## 1. Bepul baza — Neon
1. https://neon.tech → **Sign up** (GitHub bilan kirish mumkin).
2. **New Project** → nom: `tdiu` → region Europe (Frankfurt) → **Create**.
3. **Connection string** ni nusxa oling (masalan:
   `postgresql://user:pass@ep-xxx.eu-central-1.aws.neon.tech/tdiu?sslmode=require`).
   Bu manzilni 2-qadamda `DATABASE_URL` ga qo'yasiz. (Kod `sslmode` ni avtomatik moslaydi.)

## 2. Blueprint orqali joylash
1. Render Dashboard → **New** → **Blueprint** (yoki mavjud TDIU-INFO Blueprint → **Manual Sync**).
2. GitHub repongizni tanlang — Render `render.yaml` ni o'qib, **2 ta servis** yaratadi (baza yaratmaydi).
3. So'raladigan maxfiy qiymatlarni kiriting:
   - `DATABASE_URL` — **Neon connection string** (1-qadam)
   - `BOT_TOKEN` — @BotFather tokeni
   - `ADMIN_IDS` — admin Telegram ID'lari (vergul bilan), `@userinfobot` dan
   - `SUPPORT_USERNAME` — (ixtiyoriy)
4. **Apply** → Render build qiladi.
   - `JWT_SECRET` avtomatik yaratiladi. `ADMIN_PASSWORD` = `admin123` (keyin o'zgartiring).
   - Admin login: `admin` / `admin123`.

## 2. Admin panelni API'ga ulash (1 marta)
Admin panel oldindan build qilingan (`admin/dist`), Render uni npm bilan qaytadan
qurmaydi. API manzili **runtime'da** `admin/dist/config.js` faylidan o'qiladi.

Birinchi deploydan keyin `tdiu-bot-api` manzilini oling (masalan
`https://tdiu-bot-api.onrender.com`) va `admin/dist/config.js` ni tahrirlang:

```js
window.__API_URL__ = "https://tdiu-bot-api.onrender.com/api";
```

So'ng GitHub'ga push qiling — `tdiu-admin` avtomatik yangilanadi.
Endi admin panel manzili (`https://tdiu-admin.onrender.com`) orqali kirasiz.

## 3. Majburiy kanal obunasi (muhim!)
Bot foydalanuvchidan 2 ta kanalga obunani talab qiladi:
**TSUE-TDIU** (@tsueuzofficial), **TDIU | Yoshlar kanali** (@tdiu_official).

⚠️ **Bot har bir kanalda ADMINISTRATOR bo'lishi SHART** — aks holda a'zolikni
tekshira olmaydi va hech kim botdan foydalana olmaydi.
Kanal → Administrators → Add Admin → botingizni qo'shing.

- Obunani o'chirish: `SUBSCRIPTION_CHECK=false`.
- Kanallarni o'zgartirish: `bot/services/subscription.py` → `REQUIRED_CHANNELS`.

## 4. Tekshirish
- Telegram'da botga `/start` → obuna oynasi → obuna bo'lib «✅ Obunani tekshirish» → menyu.
- Admin panel → login → Ball/Kvota/Kontrakt, Operator, Ommaviy xabar bo'limlari.

## Admin panel imkoniyatlari (TZ bo'yicha)
- 📊 Statistika dashboard (foydalanuvchilar, amallar, javobsiz savollar, mashhur bo'limlar)
- 📝 O'tish bali / kvota / kontrakt (O'zbek+Rus) — botda darhol aks etadi
- 🏛 Fakultetlar, 🎓 yo'nalishlar, 📄 bo'lim matnlari, ❓ FAQ
- 💬 Operator jonli yordam (foydalanuvchi bilan yozishish)
- 📢 Ommaviy xabar (broadcast)
- 👥 RBAC: super-admin / kontent-menejer / operator

## Eslatmalar
- Bepul web servis ~750 soat/oy beradi — bitta combined servis uchun yetarli.
- Bepul Postgres muddati cheklangan bo'lishi mumkin — uzoq muddat uchun [Neon](https://neon.tech) ham mos (`DATABASE_URL` ni almashtiring).
- Token oshkor bo'lsa @BotFather → `/revoke`.
- Keep-alive tufayli bot uxlamaydi (har 14 daqiqada self-ping).
