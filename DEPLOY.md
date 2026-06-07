# Render.com ga joylashtirish (TDIU Info Bot)

Bot Render bepul "Web Service" sifatida ishlaydi. Bepul tarif 15 daqiqa harakatsizlikdan
keyin uxlaydi — shuning uchun botga **health-server** (port talabi uchun) va **keep-alive
self-ping** (har 14 daqiqada) qo'shilgan. Quyida bosqichma-bosqich.

## 0. Tayyorgarlik

1. Kodni GitHub repozitoriyaga joylang (`.env` git'ga tushmaydi — `.gitignore` da).
2. Telegram bot tokenini tayyorlab qo'ying (@BotFather).

## ⚠️ Muhim: ma'lumotlar bazasi

Render bepul tarifda disk **vaqtinchalik** (ephemeral) — har qayta deploy/restartda
SQLite fayli (`tdiu.db`) **o'chib ketadi**, kiritilgan ball/kvota/kontrakt yo'qoladi.

Shuning uchun **bepul tashqi PostgreSQL** ishlating (tavsiya):

- [Neon](https://neon.tech) (bepul, doimiy) yoki [Supabase](https://supabase.com) yoki Render'ning o'z PostgreSQL'i.
- Ulardan `Connection string` oling va `asyncpg` formatiga keltiring:

  ```
  DATABASE_URL=postgresql+asyncpg://user:parol@host:5432/dbname
  ```

  (Odatdagi `postgresql://...` ni `postgresql+asyncpg://...` ga o'zgartiring.)

SQLite faqat sinov uchun. Production'da Postgres.

## 1. Bot'ni joylash (Web Service)

**A varianti — Blueprint (`render.yaml` orqali, oson):**

1. Render Dashboard → **New** → **Blueprint**.
2. GitHub repongizni tanlang. Render `render.yaml` ni o'qiydi.
3. **Environment Variables** bo'limida maxfiy qiymatlarni kiriting:
   - `BOT_TOKEN` = @BotFather tokeni
   - `ADMIN_IDS` = operator Telegram ID'lari (vergul bilan), masalan `12345678`
   - `DATABASE_URL` = Neon/Postgres ulanish satri (yuqoriga qarang)
   - `SUPPORT_USERNAME` = (ixtiyoriy) qabul komissiyasi username
4. **Apply** → Render build qiladi va ishga tushiradi.

**B varianti — qo'lda:**

1. **New** → **Web Service** → repongizni ulang.
2. Sozlamalar:
   - Runtime: **Python 3**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python -m bot.main`
   - Health Check Path: `/health`
   - Plan: **Free**
3. Environment'ga yuqoridagi o'zgaruvchilarni qo'shing.
4. **Create Web Service**.

Render avtomatik `RENDER_EXTERNAL_URL` va `PORT` beradi — keep-alive ularni o'zi ishlatadi.

## 2. Keep-alive (uyqudan saqlash)

Botda allaqachon bor: har `KEEPALIVE_MINUTES` (standart 14) daqiqada o'z `/health`
manziliga ping yuboradi. Qo'shimcha sozlash shart emas.

**Ishonchliroq qilish uchun** tashqi monitor ham qo'shing (tavsiya):

- [UptimeRobot](https://uptimerobot.com) yoki [cron-job.org] da yangi monitor:
  - URL: `https://SIZNING-SERVIS.onrender.com/health`
  - Interval: **5–10 daqiqa**

Bu botni uyqudan ikki tomonlama himoya qiladi.

## 3. Birinchi ishga tushish

Bot birinchi startda DB jadvallarini yaratadi va statik kontent (tsue.uz, 32 yo'nalish,
kontrakt narxlari) bilan to'ldiradi — qo'shimcha amal kerak emas. Telegram'da botingizga
`/start` yuboring, ishlashini tekshiring.

## 4. Ballarni/kvotani keyin yangilash

- **Admin panel orqali** (agar uni ham joylasangiz) — eng qulay.
- Yoki `bot/content/admission_data.py` ni tahrirlab, kodni push qiling: Render qayta
  deploy qiladi. Mavjud DB'ni yangilash uchun Render **Shell** da `python -m core.load_admission`.

## 5. (Ixtiyoriy) Admin panelni ham joylash

- **Backend (FastAPI):** yana bitta Render Web Service —
  Start Command: `uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT`,
  `DATABASE_URL` bot bilan **bir xil**.
- **Admin (React):** Render **Static Site** —
  Build: `npm install && npm run build`, Publish dir: `admin/dist`,
  Environment: `VITE_API_URL=https://SIZNING-BACKEND.onrender.com/api`.

## Eslatmalar
- Bepul Web Service oyiga ~750 soat beradi — bitta doimiy servis uchun yetarli.
- Token oshkor bo'lsa @BotFather → `/revoke` orqali yangilang.
- Polling rejimi ishlatilmoqda; keep-alive tufayli bot doim onlayn turadi.
