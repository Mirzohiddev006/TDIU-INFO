# Render.com ga joylashtirish — TDIU Info Bot + Admin panel

Loyiha 3 qismdan iborat va Render Blueprint (`render.yaml`) orqali **bir marta** to'liq joylashadi:
1. **PostgreSQL** (bepul) — doimiy ma'lumotlar bazasi
2. **tdiu-bot-api** — bot + admin API bitta web servisda
3. **tdiu-admin** — React admin panel (static site)

## 0. Tayyorgarlik
1. Loyihani **GitHub** repozitoriyaga push qiling (`.env` git'ga tushmaydi).
2. @BotFather'dan bot tokeni tayyorlang.

## 1. Blueprint orqali joylash
1. Render Dashboard → **New** → **Blueprint**.
2. GitHub repongizni tanlang — Render `render.yaml` ni o'qib, 3 ta resursni yaratadi.
3. So'raladigan maxfiy qiymatlarni kiriting:
   - `BOT_TOKEN` — @BotFather tokeni
   - `ADMIN_IDS` — operator/admin Telegram ID'lari (vergul bilan), `@userinfobot` dan oling
   - `ADMIN_PASSWORD` — admin panelga kirish paroli (o'zingiz tanlang)
   - `SUPPORT_USERNAME` — (ixtiyoriy) qabul komissiyasi username
4. **Apply** → Render hammasini build qiladi.
   - `DATABASE_URL` avtomatik Postgresga ulanadi.
   - `JWT_SECRET` avtomatik yaratiladi.
   - Admin login: `admin` / siz kiritgan `ADMIN_PASSWORD`.

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
