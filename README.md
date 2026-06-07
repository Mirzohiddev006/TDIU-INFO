# TDIU Info Bot 🎓

Toshkent Davlat Iqtisodiyot Universiteti abituriyentlari uchun ma'lumot beruvchi Telegram bot + admin panel.

**Holati:** Faza 1 (MVP bot) ✅ va Faza 2 (DB + FastAPI + React admin panel) ✅ tugadi.
Kontent tsue.uz rasmiy saytidan olingan. Faza 3 (jonli operator) va Faza 4 (broadcast, polish) — keyingi bosqichlar.

## Arxitektura

```
Telegram foydalanuvchi
        │
   aiogram bot ──────┐
        │            │  (umumiy core/ paketi: modellar + DB)
   React admin ─ FastAPI ─┘
        │            │
        └──── PostgreSQL / SQLite ────┘
```

- `bot/` — aiogram 3.x bot. Kontentni **bazadan** o'qiydi (DB ishlamasa statik fallback).
- `core/` — umumiy qatlam: SQLAlchemy modellari, async DB sessiya, seed, JWT/parol.
- `backend/` — FastAPI admin API (JWT auth, RBAC, CRUD).
- `admin/` — React + TypeScript + Tailwind admin panel.

## Komponentlar

### 1) Bot
12 bo'lim, 32 yo'nalish (rasmiy kodlar), FAQ qidiruv, operatorga yo'naltirish, foydalanuvchi/analitika logi.

### 2) Admin panel (React)
- 🔐 Login (JWT)
- 📊 Statistika: foydalanuvchilar, amallar, javobsiz savollar, mashhur bo'limlar
- 📝 **Ball / Kvota / Kontrakt** — yo'nalish bo'yicha kiritish (botda darhol aks etadi)
- 🏛 Fakultetlar (qo'shish/o'chirish)
- 🎓 Yo'nalishlar ro'yxati
- 📄 Bo'lim matnlarini tahrirlash (HTML)
- ❓ FAQ qo'shish/o'chirish
- 👥 RBAC: super-admin / kontent-menejer / operator

## Ishga tushirish

### 0. Ma'lumotlar bazasi
Standart — SQLite (o'rnatishsiz). Production uchun PostgreSQL: `backend/.env` va bot `.env` da
bir xil `DATABASE_URL` ni belgilang, masalan:
`postgresql+asyncpg://tdiu:parol@localhost:5432/tdiu`

### 1. Bot
```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env        # BOT_TOKEN, ADMIN_IDS, DATABASE_URL
python -m core.seed         # bazani statik kontent bilan to'ldirish (bir marta)
python -m bot.main          # bot ishga tushadi (birinchi startda avtomatik seed ham bo'ladi)
```

### 2. Backend (FastAPI)
```bash
pip install -r backend/requirements.txt
cp backend/.env.example backend/.env     # DATABASE_URL bot bilan BIR XIL!
uvicorn backend.app.main:app --reload --port 8000
# API hujjati: http://localhost:8000/docs
```
Birinchi admin: `admin` / `admin123` (`.env` da o'zgartiring).

### 3. Admin panel (React)
```bash
cd admin
npm install
cp .env.example .env.development   # VITE_API_URL=http://localhost:8000/api
npm run dev      # http://localhost:3000
```

## O'tish ballari / kvota / kontrakt kiritish

Ikki yo'l:
1. **Admin panel** (tavsiya): «Ball / Kvota / Kontrakt» bo'limi → qiymat yozib «Saqlash». Botda darhol ko'rinadi.
2. **To'g'ridan-to'g'ri** (admin paneldan oldin): `bot/content/admission_data.py` ni tahrirlash — bu statik fallback uchun.
   So'ng `python -m core.load_admission` ishga tushiring — qiymatlar bazaga yoziladi (botda ko'rinadi).

`None`/bo'sh qoldirilgan qiymatni bot "tez orada kiritiladi" deб ko'rsatadi.

## Struktura
```
TDIU_INFO_BOT/
├── bot/                 aiogram bot (provider.py orqali DB dan o'qiydi)
│   ├── content/         statik fallback kontent (tsue.uz)
│   ├── handlers/  keyboards/  services/
│   ├── provider.py      DB ↔ statik ko'prik
│   └── main.py
├── core/                umumiy DB qatlami (modellar, sessiya, seed, security)
├── backend/app/         FastAPI (auth, content, admission, stats routerlari)
├── admin/               React admin panel (Vite+TS+Tailwind+TanStack+Zustand)
├── requirements.txt
└── README.md
```

## Texnologiyalar
Python 3.11+ · aiogram 3 · SQLAlchemy 2 (async) · FastAPI · PostgreSQL/SQLite ·
React 18 · TypeScript · Vite · Tailwind 4 · TanStack Query · Zustand · JWT

## Keyingi bosqichlar
- **Faza 3 — Operator:** to'liq jonli chat relay (foydalanuvchi ↔ operator) + admin operator paneli.
- **Faza 4 — Polish:** broadcast (ommaviy xabar), statistikani kengaytirish, optimizatsiya, testlar.
