# Linux for DevOps — From Zero to Production

An interactive, responsive educational platform for learning Linux systematically from absolute beginner to production troubleshooting. Built with **Next.js + React + TypeScript** (frontend) and **FastAPI + SQLAlchemy + SQLite** (backend).

> ⚠️ The terminal labs are **browser-simulated** — clearly labeled as simulated. No user-entered command ever executes on the application server. Real isolated Linux labs are on the roadmap.

## Features implemented (vertical slice)

- **Curriculum**: all 6 goal-based learning paths, 22 modules across 5 stages
- **Stage 1 fully authored**: Module 1 (Introduction to Linux & DevOps) + Module 2 (Terminal Fundamentals) — 10 detailed beginner lessons with objectives, command examples, labs, case studies, quizzes, and assignments
- **Interactive simulated terminal**: virtual filesystem, command registry (`pwd`, `ls`, `cd`, `cat`, `echo`, `history`, `clear`, `uname`, `whoami`, `id`, `which`, `type`), scenario-specific initial state, completion validation, reset
- **Labs & case studies**: guided troubleshooting scenarios with objective, symptoms, evidence, root cause, solution, verification, prevention
- **Assessments**: multiple-choice, command-completion, and output-interpretation questions with server-side validation and explanations
- **Progress tracking**: lesson completion, quiz scores, lab pass/fail, persisted per authenticated user (guest mode supported)
- **Cheat-sheet library**: searchable, filterable by topic, copy-to-clipboard commands, safety warnings
- **Dashboard**: progress stats, continue-learning, guest/auth modes
- **Themes**: dark + light, system preference, responsive desktop/mobile layout
- **API**: REST backend with JWT auth, optional guest mode, CORS

## Quick start

### Prerequisites
- Node.js 18+ (v24 used in development)
- Python 3.11+ (3.12 used in development)
- `pip` and `npm`

### 1. Backend

```bash
cd backend
python -m venv .venv
# Windows: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python scripts/seed.py       # create DB + seed curriculum
python scripts/import_content.py  # import the 25 authored chapters from ../content/*.html
                             # (run this AFTER seed.py if rebuilding from scratch)
uvicorn app.main:app --reload --port 8000
```

The API is available at `http://127.0.0.1:8000` (health: `/api/v1/health`).

### 2. Frontend

```bash
cd frontend
npm install
npm run dev                  # http://localhost:3000
```

The frontend proxies `/api/*` to `http://127.0.0.1:8000` (see `frontend/next.config.js`).

### 3. Explore
- Open `http://localhost:3000`
- Click **"Explore as guest"** (no account required) or register/login
- Work through Module 1 → Module 2 lessons
- Visit `/reference` for cheat sheets

### Demo credentials
A seeded demo user exists: `demo` / `demo123`.

## Project structure

```
linotutor/
├── backend/                 # FastAPI API
│   ├── app/
│   │   ├── api/             # route modules (auth, curriculum, labs, progress, cheatsheets, assessments)
│   │   ├── core/            # config, security
│   │   ├── db/              # SQLAlchemy session + engine
│   │   ├── models/          # User, Module, Lesson, Lab, CheatSheet, Progress, ...
│   │   ├── schemas/         # Pydantic schemas
│   │   └── main.py          # app factory
│   ├── alembic/             # migrations (skeleton)
│   ├── scripts/seed.py      # curriculum + seed data
│   ├── requirements.txt
│   └── .env
├── frontend/                # Next.js app
│   ├── app/
│   │   ├── page.tsx         # dashboard
│   │   ├── learn/[slug]/    # lesson page
│   │   ├── reference/       # cheat sheets
│   │   └── layout.tsx
│   ├── components/
│   │   ├── layout/          # sidebar, navbar
│   │   ├── terminal/        # commandRegistry.ts + Terminal.tsx (simulated shell)
│   │   └── ui/              # card, button, input
│   ├── lib/                 # utils, api client
│   └── types/
├── docs/
│   └── ARCHITECTURE.md
├── README.md
└── roadmap.md
```

## Data model

Core entities: `User`, `LearningPath`, `Module`, `Lesson`, `LearningObjective`, `CommandExample`, `Lab`, `LabScenario`, `CheatSheet`, `Assignment`, `Question`, `UserProgress`, `LabAttempt`, `AssessmentAttempt`, `Bookmark`, `Achievement`.

Curriculum content is stored as structured JSON separate from UI components so the syllabus can grow without redesigning the app.

## Safety

- Simulated terminal runs entirely in the browser; no host execution.
- No arbitrary user-entered shell commands are executed on the server.
- Roadmap real labs use isolated containers/VMs with resource limits, restricted privileges, network controls, and disposable state.

## Testing

Backend:
```bash
cd backend
pytest
```

Frontend build:
```bash
cd frontend
npm run build
```

## Roadmap

See `roadmap.md` for phases 3–7 (remaining modules 3–22, real isolated Linux labs, advanced animations, PostgreSQL, production deployment).

- python scripts/import_cheatsheets.py  # import phoenixNAP Linux commands cheat sheet (19 topic sheets)

