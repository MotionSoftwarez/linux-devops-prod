# Architecture — Linux for DevOps Platform

## Stack

| Layer | Choice |
|-------|--------|
| Frontend | Next.js 14 (App Router), React 18, TypeScript, Tailwind CSS |
| Frontend UI | Custom accessible primitives (card, button, input), Lucide icons, Framer Motion ready |
| Terminal | Browser-based simulated shell (command registry + virtual filesystem) — no host execution |
| Backend | FastAPI (Python 3.12) |
| API | REST, JSON |
| Auth | JWT (python-jose) + bcrypt, optional guest mode, registration/login |
| Database | SQLAlchemy 2.0 ORM; SQLite for local dev, PostgreSQL for production |
| Migrations | Alembic (skeleton in `backend/alembic`) |
| Seeding | `backend/scripts/seed.py` |

## Data model (key entities)

- `User` — account, guest flag, learning goal
- `LearningPath` — 6 goal-based paths (beginner, administrator, devops, troubleshooter, interview, advanced)
- `Module` — 22 modules across 5 stages
- `Lesson` — structured content (JSON), objectives, examples, labs, quizzes
- `Lab` + `LabScenario` — guided/unguided troubleshooting scenarios with completion criteria
- `CheatSheet` — searchable reference entries
- `Assignment` + `Question` — 3 difficulty levels, MCQ / command completion / output interpretation
- `UserProgress`, `LabAttempt`, `AssessmentAttempt` — persisted progress
- `Bookmark`, `Achievement`

## Safety boundary

- Phase 1–6: terminal is fully simulated in the browser. Clearly labeled "Simulated terminal".
- Commands never reach the app server.
- Roadmap: real labs via isolated containers/VMs (resource limits, restricted privileges, network controls, disposable state). Never arbitrary user commands on the host.

## Content model

Curriculum is stored as structured JSON in the DB, separate from UI components. New lessons/modules are added by seeding JSON — no UI redesign required.

## Endpoints (selected)

- `GET /api/v1/health`
- `POST /api/v1/auth/register`, `/login`, `/guest`, `GET /auth/me`
- `GET /api/v1/curriculum/paths`, `/paths/{key}/modules`, `/modules/{key}/lessons`, `/lessons/{slug}`, `/lessons/{slug}/progress`
- `GET /api/v1/labs/lessons/{slug}`, `POST /labs/lessons/{slug}/attempt`
- `POST /api/v1/progress/lessons/{slug}`, `GET /progress/summary`
- `GET /api/v1/cheatsheets`, `/cheatsheets/topics`, `/cheatsheets/{key}`
- `GET /api/v1/assessments/lessons/{slug}`, `POST /assessments/lessons/{slug}/submit`

## Progress rules

A lesson is marked complete only when required labs and/or assessments are passed (server-side validated), not merely opened.
