# Roadmap

## Completed (Phase 1–6 vertical slice)
- Backend API, data model, seed curriculum (22 modules, 6 paths)
- Stage 1 Modules 1–2 fully authored (10 lessons, labs, case studies, quizzes, assignments)
- Simulated terminal engine + virtual filesystem + state validation
- Dashboard, sidebar, lesson page, reference library
- Auth (guest + registered), progress persistence
- Dark/light themes, responsive layout
- Build + full E2E learner journey verified

## Next milestones
1. Author Stage 1 Modules 3–4 (Files & Directories, Reading & Editing Files) using the same reusable structures
2. Author Stage 2 Modules 5–11 (Users/Permissions, Packages, Processes, systemd, Storage, Networking, Logs)
3. Expand lab command registry (grep, find, chmod, chown, ps, systemctl, curl, etc.)
4. Add guided + unguided case-study modes (root cause hidden until diagnosis submitted)
5. Rich educational animations (SVG/CSS) for filesystem tree, permissions, pipes, DNS, etc.
6. PostgreSQL + Alembic migrations for production
7. Automated test suite (unit/integration/E2E) with CI
8. Real isolated Linux labs (containers/VMs) behind an execution service — never host execution
9. Production deployment docs (Docker, env vars, reverse proxy)
