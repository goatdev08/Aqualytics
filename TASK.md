<!--
TASK.md
AquaLytics App – Ordered execution checklist
Cursor‑AI: Each task is atomic, starts with a checkbox, includes a numeric
complexity score (1‑5). Items scored 4‑5 are flagged **(HIGH)** and broken
into finer sub‑tasks. Dependencies are explicit for context‑aware completions.
-->

# ☑️ AquaLytics Task Board

> **Legend**  
> • `Score` 1‑2 = easy • 3 = medium • 4‑5 = hard (split)  
> • Mark tasks `[x]` when done to keep token usage lean.

---

## Phase 0 — Repository & Workspace

- [x] **Create mono‑repo and workspace** (Score 2)  
  _Dependencies_: git, VS Code/Cursor  
  1. Initialise `AquaLytics-app` repo, push to GitHub.  
  2. Add `frontend/` + `backend/` folders.  
  3. Save `AquaLytics.code-workspace`.

---

## Phase 1 — Database Foundation

- [ ] **Set up Supabase project & schema** (Score 3)  
  _Dependencies_: Supabase dashboard, `psql`  
  1. Create project.  
  2. Run SQL schema script (tables: swimmers, competitions, results).  
  3. Copy `SUPABASE_URL`, `SUPABASE_KEY` to `.env.example`.

---

## Phase 2 — Backend Environment

- [ ] **Python venv & core deps** (Score 2)  
  _Dependencies_: python 3.12, `pip`, requirements.txt  
  1. `python -m venv venv`  
  2. `pip install fastapi uvicorn[standard] pandas sqlalchemy asyncpg python-dotenv python-multipart pydantic`  
  3. Freeze versions.

---

## Phase 3 — FastAPI Skeleton

- [ ] **Bootstrap API application** (Score 3)  
  _Dependencies_: fastapi, uvicorn, pydantic  
  1. `main.py` with FastAPI instance.  
  2. Enable CORS for `localhost:3000`.  
  3. Health‑check route `/ping`.

---

## Phase 4 — Data Layer **(HIGH)**

- [ ] **Design async SQLAlchemy models & connection** (Score 4)  
  _Dependencies_: sqlalchemy 2, asyncpg, pandas  
  - [ ] _Sub 4.1_ `connection.py` – async engine using `DATABASE_URL`.  
  - [ ] _Sub 4.2_ `models/*.py` – Swimmer, Competition, Result.  
  - [ ] _Sub 4.3_ Alembic/SQLModel migrations (optional).

---


- [ ] **Endpoint `/import` multipart CSV → DB** (Score 4)  
  _Dependencies_: pandas, python‑multipart  
  - [ ] _Sub 5.1_ Validate header contains 16‑20 metric columns.  
  - [ ] _Sub 5.2_ Bulk‑insert rows with asyncpg transaction.  
  - [ ] _Sub 5.3_ Return summary JSON `{inserted, skipped}`.

---

## Phase 5b — Data-Entry Pipeline **(HIGH)**

- [ ] **Metric Dictionary bootstrap** (Score 3)  
  _Dependencies_: none (JSON file)  
  - Create `dictionaries/metrics.json` with codes, labels, units, types.

- [ ] **Backend `/dictionary` endpoint** (Score 2)  
  _Dependencies_: fastapi  
  - Serve the JSON dictionary for the UI.

- [ ] **Data-Entry router & validation** (Score 4)  
  _Dependencies_: pydantic, sqlalchemy  
  - [ ] _5b.1_ `POST /metrics` — persist manual fields.  
  - [ ] _5b.2_ Call `auto_metrics.py` for derived metrics.  
  - [ ] _5b.3_ `PUT /metrics/{id}` — partial updates.

- [ ] **Auto-metrics service** (Score 4)  
  _Dependencies_: pandas, numpy  
  - Implement functions referenced in `metrics.json`.

- [ ] **Frontend `data-entry.js`** (Score 4)  
  _Dependencies_: react, axios, tailwindcss  
  - [ ] Fetch `/dictionary`, generate dynamic form.  
  - [ ] Dropdown for `phase` (`PRELIM|SEMIS|FINAL`).  
  - [ ] Submit via `POST`, show toast + optimistic update.

## Phase 6 — Metrics & Analysis Engine **(HIGH)**

- [ ] **`data_analysis.py` calculations** (Score 5)  
  _Dependencies_: pandas, numpy (implicit)  
  - [ ] _Sub 6.1_ Compute aggregates (avg, best, std) per metric.  
  - [ ] _Sub 6.2_ Delta comparison between two swimmers/races.  
  - [ ] _Sub 6.3_ Serialize results for Plotly shape.

---

## Phase 7 — Feature Routers

- [ ] **`/competitions` & `/results` endpoints** (Score 3)  
  _Dependencies_: fastapi, sqlalchemy  
  1. List competitions with pagination.  
  2. Detail endpoint returns metrics JSON.

---

## Phase 8 — Frontend Environment

- [ ] **Init Next.js + TailwindCSS** (Score 2)  
  _Dependencies_: next 14, react 18, tailwindcss 3  
  1. `npx create-next-app frontend --ts`.  
  2. Configure Tailwind (`postcss.config.js`, `globals.css`).  
  3. Splash page `/` with Supabase auth.

---

## Phase 9 — API Service Layer

- [ ] **`services/api.js` Axios wrapper** (Score 2)  
  _Dependencies_: axios 1  
  1. BaseURL env‑driven.  
  2. Interceptor for error logging.

---

## Phase 10 — Competitions UI **(HIGH)**

- [ ] **Build `pages/competitions.js`** (Score 4)  
  _Dependencies_: react, next, axios, plotly.js  
  - [ ] _Sub 10.1_ Fetch & list competitions (table).  
  - [ ] _Sub 10.2_ Detail drawer with 16‑20 metrics Plotly graphs.  
  - [ ] _Sub 10.3_ CSV uploader component -> toast feedback.

---

## Phase 11 — Dashboard UI

- [ ] **`pages/dashboard.js` KPI cards & comparisons** (Score 3)  
  _Dependencies_: plotly.js, tailwindcss  
  1. Call analysis API.  
  2. Render line/bar graphs for progress.

---

## Phase 12 — Authentication Flow

- [ ] **Integrate Supabase Auth** (Score 3)  
  _Dependencies_: `@supabase/supabase-js`, next-auth (opt)  
  1. Sign‑in page, protected routes wrapper.  
  2. Store JWT in cookies/localStorage.

---

## Phase 13 — Testing & QA

- [ ] **Backend Pytest suite** (Score 2)  
  _Dependencies_: pytest, httpx  
  - CRUD endpoints + analysis unit tests.

- [ ] **Frontend lint & unit tests** (Score 2)  
  _Dependencies_: eslint, jest/react-testing-library

---

## Phase 14 — CI/CD

- [ ] **GitHub Actions pipeline** (Score 3)  
  _Dependencies_: actions/setup-node, actions/setup-python  
  1. Job lint + test.  
  2. Deploy frontend to Vercel & backend to Railway on push to `main`.

---

## Phase 15 — Deployment

- [ ] **Release backend to Railway** (Score 2)  
  _Dependencies_: Railway CLI  
- [ ] **Release frontend to Vercel** (Score 2)  
  _Dependencies_: Vercel CLI

---

## Phase 16 — Pilot & Feedback

- [ ] **Invite first coaches, collect logs** (Score 2)  
  _Dependencies_: Vercel analytics, Railway logs  

---

<!-- End TASK.md -->
