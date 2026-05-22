---

description: "Task list for GitHub Plant Gamification feature"
---

# Tasks: GitHub Plant Gamification

**Input**: Design documents from `specs/001-github-plant/`

**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/

**Tests**: Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks grouped by 4 chronological phases: Configuración y Auth, Backend y Webhooks, Frontend y Lógica de la Planta, Integración.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Backend**: `backend/src/`, `backend/tests/` (FastAPI + Python)
- **Frontend**: `frontend/src/`, `frontend/tests/` (Vue 3 + TypeScript)
- **Infrastructure**: Root level `docker-compose.yml`, `.env.example`

---

## Fase 1: Configuración y Auth (Setup + GitHub OAuth)

**Propósito**: Inicializar el monorepo, contenedores, base de datos, y flujo completo de autenticación GitHub OAuth (US1).

**Duración estimada**: Día 1–2

---

### Setup (Infraestructura Compartida)

- [X] T001 Create monorepo root with `backend/` and `frontend/` directory structure
- [X] T002 Initialize Python project with FastAPI, SQLAlchemy, Alembic, and `arq` in `backend/pyproject.toml`
- [X] T003 Initialize Vue 3 + TypeScript + Vite project in `frontend/` with `package.json`, `tsconfig.json`, `vite.config.ts`
- [X] T004 [P] Create `docker-compose.yml` with postgres:16, redis:7, backend, and frontend services
- [X] T005 [P] Create `.env.example` with GITHUB_CLIENT_ID, GITHUB_CLIENT_SECRET, GITHUB_WEBHOOK_SECRET, SECRET_KEY, DATABASE_URL, REDIS_URL
- [X] T006 [P] Create `backend/Dockerfile` (Python slim image with uvicorn)
- [X] T007 [P] Create `frontend/Dockerfile` (Node multi-stage build with nginx)
- [X] T008 [P] Configure linting: `ruff` in `backend/pyproject.toml`, ESLint + Prettier in `frontend/`
- [X] T009 Create `backend/src/main.py` with FastAPI app factory, CORS, and health check endpoint at `/api/health`

**Checkpoint**: `docker compose up --build` starts all 4 services; `curl localhost:8000/api/health` returns 200.

---

### Foundational: Base de Datos y Modelos

- [X] T010 Configure SQLAlchemy async engine and session factory in `backend/src/infrastructure/database/engine.py`
- [X] T011 Initialize Alembic at `backend/alembic/` with async migration environment
- [X] T012 Create SQLAlchemy User model in `backend/src/infrastructure/database/models/user.py` (github_id, username, display_name, avatar_url, encrypted_token, token_nonce, github_connected_at, timestamps)
- [X] T013 [P] Create `idx_user_github_id` and `idx_user_username` unique indexes in Alembic migration
- [X] T014 Create UserRepository protocol in `backend/src/core/ports/user_repository.py`
- [X] T015 Implement PostgresUserRepository in `backend/src/infrastructure/database/repositories/user_repository.py`

**Checkpoint**: Alembic migrations apply cleanly; User CRUD works through repository interface.

---

### User Story 1 — Connect GitHub Account (P1) 🎯 MVP

**Goal**: User visits the app, authenticates via GitHub OAuth, and is redirected back with a session.

**Independent Test**: Visitor clicks "Connect GitHub", completes OAuth, sees their GitHub username in the header.

- [X] T016 [US1] Create GitHub OAuth protocol in `backend/src/core/ports/github_oauth.py`
- [X] T017 [US1] Implement GitHubOAuthService in `backend/src/infrastructure/auth/github_oauth.py` with login URL generation and code→token exchange via `httpx`
- [X] T018 [US1] Create token encryption service in `backend/src/infrastructure/auth/token_encryption.py` using `cryptography.fernet` (AES-256-GCM)
- [X] T019 [US1] Implement session management (JWT) in `backend/src/infrastructure/auth/session.py`
- [X] T020 [US1] Create AuthMiddleware in `backend/src/api/middleware/auth.py` to verify JWT on protected routes
- [X] T021 [US1] Create Pydantic auth schemas in `backend/src/api/schemas/auth.py` (LoginResponse, AuthStatusResponse)
- [X] T022 [US1] Create auth router at `backend/src/api/routes/auth.py` with endpoints:
  - `GET /api/auth/github/login` — redirect to GitHub
  - `GET /api/auth/github/callback` — OAuth callback → create/authenticate user
  - `GET /api/auth/status` — check session
  - `POST /api/auth/logout` — invalidate session
- [X] T023 [US1] Create frontend API client for auth in `frontend/src/services/authService.ts`
- [X] T024 [US1] Create LoginButton component in `frontend/src/components/auth/LoginButton.vue`
- [X] T025 [US1] Create UserMenu component in `frontend/src/components/auth/UserMenu.vue`
- [X] T026 [US1] Create LoginPage in `frontend/src/pages/LoginPage.vue` with "Connect with GitHub" button
- [X] T027 [US1] Create Pinia user store in `frontend/src/stores/userStore.ts` (login, logout, status check, persist session)
- [X] T028 [US1] Configure Vue Router with auth guard in `frontend/src/router/index.ts`

**Checkpoint**: User clicks "Connect with GitHub" → redirected to GitHub → authorizes → redirected back → username displayed.

---

## Fase 2: Backend y Webhooks

**Propósito**: Backend completo de plantas, drops, ingesta de webhooks, worker asíncrono y lógica de crecimiento.

**Duración estimada**: Día 3–5

---

### User Story 3 — Receive Water Drops from Commits (P2)

**Goal**: Commits detected via webhook or historical import translate into water drops that advance the plant's growth stage.

**Independent Test**: User connects a GitHub account with 20+ public commits. Plant receives drops equal to commit count and advances at least one growth stage.

- [X] T029 [P] [US3] Create PlantTypeConfig YAML loader in `backend/src/core/config/plant_types/loader.py` with 4 plant definitions (cactus, bonsai, cannabis, fruit)
- [X] T030 [P] [US3] Create Plant domain entity in `backend/src/core/entities/plant.py` (`PlantType` StrEnum, `GrowthStage` IntEnum, `Plant` dataclass)
- [X] T031 [P] [US3] Create Drop domain entity in `backend/src/core/entities/drop.py` (`DropEventType` StrEnum, `Drop` dataclass)
- [X] T032 [US3] Create PlantGrowthService in `backend/src/core/services/plant_growth.py` with:
  - `calculate_stage(total_drops, plant_type)` → calculates current stage + drops in stage
  - `check_stage_transition(plant, new_drops)` → returns old stage, new stage, whether transition occurred
- [X] T033 [US3] Create DripCalculationService in `backend/src/core/services/drip_calculation.py` with `calculate_drops(events)` mapping commit events to drops
- [X] T034 [US3] Create PlantRepository protocol in `backend/src/core/ports/plant_repository.py`
- [X] T035 [P] [US3] Create DropRepository protocol in `backend/src/core/ports/drop_repository.py`
- [ ] T036 [US3] Implement PostgresPlantRepository in `backend/src/infrastructure/database/repositories/plant_repository.py`
- [ ] T037 [P] [US3] Implement PostgresDropRepository in `backend/src/infrastructure/database/repositories/drop_repository.py`
- [ ] T038 [US3] Create SQLAlchemy Plant model in `backend/src/infrastructure/database/models/plant.py`
- [ ] T039 [P] [US3] Create SQLAlchemy Drop model in `backend/src/infrastructure/database/models/drop.py`
- [ ] T040 [US3] Create Alembic migration for Plant + Drop tables with indexes (`idx_plant_user`, `idx_drop_plant`, `idx_drop_github_event`, `idx_drop_created_at`)
- [X] T041 [US3] Create webhook signature verification in `backend/src/infrastructure/github/webhook_verification.py` (HMAC-SHA256)
- [X] T042 [US3] Create Redis queue adapter in `backend/src/infrastructure/queue/redis_queue.py` (producer: enqueue event, consumer: dequeue + process)
- [ ] T043 [US3] Create GitHub API client in `backend/src/infrastructure/github/github_client.py` for fetching commit history (paginated, rate-limited)
- [X] T044 [US3] Create webhook schemas in `backend/src/api/schemas/webhooks.py` (WebhookResponse)
- [X] T045 [US3] Create webhook router at `backend/src/api/routes/webhooks.py`:
  - `POST /api/webhooks/github` — verify signature → enqueue to Redis → return 202
- [ ] T046 [US3] Create arq background worker at `backend/src/worker.py` that:
  - Consumes webhook events from Redis
  - Calls GitHub API for commit details
  - Persists Drop record (idempotent via `github_event_id`)
  - Calls PlantGrowthService to recalculate stage
  - Publishes stage transition event to Redis pub/sub if changed
- [ ] T047 [US3] Create Pydantic dashboard schemas in `backend/src/api/schemas/dashboard.py` (DashboardResponse, PlantStateResponse, DropHistoryResponse)
- [ ] T048 [US3] Create dashboard router at `backend/src/api/routes/dashboard.py`:
  - `GET /api/dashboard` — current plant state + drop counter + recent drops + progress
  - `GET /api/dashboard/history` — paginated drop history with cursor

**Checkpoint**: Webhook payload received → verified → queued → processed → Drop persisted → Plant stage recalculated. API returns correct stage and drop count.

---

## Fase 3: Frontend y Lógica de la Planta

**Propósito**: Interfaz de usuario completa: selección de planta, dashboard, componentes visuales de planta, stores y servicios frontend.

**Duración estimada**: Día 6–8

---

### User Story 2 — Select a Plant (P1)

**Goal**: After connecting GitHub, user chooses a plant type and sees their seed on the dashboard.

**Independent Test**: User sees 4 plant cards, selects one, dashboard loads with plant as seed.

- [ ] T049 [P] [US2] Create Pydantic plant schemas in `backend/src/api/schemas/plants.py` (PlantTypeResponse, PlantSelectRequest, PlantResponse)
- [ ] T050 [US2] Create plants router at `backend/src/api/routes/plants.py`:
  - `GET /api/plants/types` — list available plant types with preview info
  - `POST /api/plants/select` — create plant for authenticated user
  - `GET /api/plants/mine` — get current user's plant state
- [ ] T051 [US2] Create frontend API client for plants in `frontend/src/services/plantService.ts`
- [ ] T052 [US2] Create PlantSelectPage in `frontend/src/pages/PlantSelectPage.vue` with 4 plant cards
- [ ] T053 [US2] Create Pinia plant store in `frontend/src/stores/plantStore.ts` (set type, fetch state, watch for changes)
- [ ] T054 [US2] Create TypeScript interfaces in `frontend/src/types/plant.ts` matching backend schemas

**Checkpoint**: After GitHub auth, user sees 4 plant options → selects one → redirected to dashboard with seed.

---

### User Story 4 — View Dashboard (P2)

**Goal**: User visits the dashboard to see their plant, drop counter, progress bar, and history.

**Independent Test**: Authenticated user navigates to dashboard, sees plant visual, drop counter, progress bar, and chronological drop list.

- [ ] T055 [US4] Create base PlantCanvas component in `frontend/src/components/plant/PlantCanvas.vue` that renders an SVG based on plant type + stage
- [ ] T056 [P] [US4] Create Cactus SVG assets (5 stages) in `frontend/src/assets/plants/cactus/` (seed.svg, sprout.svg, young.svg, mature.svg, bloomed.svg)
- [ ] T057 [P] [US4] Create Bonsai SVG assets (5 stages) in `frontend/src/assets/plants/bonsai/`
- [ ] T058 [P] [US4] Create Cannabis SVG assets (5 stages) in `frontend/src/assets/plants/cannabis/`
- [ ] T059 [P] [US4] Create Fruit SVG assets (5 stages) in `frontend/src/assets/plants/fruit/`
- [ ] T060 [US4] Create DropCounter component in `frontend/src/components/dashboard/DropCounter.vue`
- [ ] T061 [US4] Create ProgressBar component in `frontend/src/components/dashboard/ProgressBar.vue` (shows drops to next stage + percentage)
- [ ] T062 [US4] Create DropHistory component in `frontend/src/components/dashboard/DropHistory.vue` (chronological list with date + repo + event type)
- [ ] T063 [US4] Create DashboardPage in `frontend/src/pages/DashboardPage.vue` composing plant + counter + progress + history
- [ ] T064 [US4] Create frontend API client for dashboard in `frontend/src/services/dashboardService.ts`
- [ ] T065 [US4] Create Pinia drops store in `frontend/src/stores/dropsStore.ts` (recent drops, paginated history)
- [ ] T066 [US4] Add dark mode theme (default) in `frontend/src/assets/styles/main.css` with CSS custom properties

**Checkpoint**: Dashboard shows plant at correct stage, drop counter matches API, progress bar shows advancement, history lists recent drops.

---

## Fase 4: Integración y Pulido

**Propósito**: Conexión en tiempo real, animaciones, transiciones de etapa, y pulido final.

**Duración estimada**: Día 9–10

---

### User Story 5 — Watering Animations (P3)

**Goal**: Real-time drop detection and stage transitions with visual animations.

**Independent Test**: Dashboard open → new commit pushed → water drop animation plays → counter increments.

- [ ] T067 [US5] Create SSE endpoint at `backend/src/api/routes/events.py`:
  - `GET /api/events/stream` — Server-Sent Events for authenticated user (sends `drop_received` and `stage_advanced` events)
- [ ] T068 [US5] Publish events from arq worker after processing each webhook (publish to Redis pub/sub channel per user)
- [ ] T069 [US5] Create frontend EventSource service in `frontend/src/services/eventService.ts` that connects to SSE stream and dispatches to stores
- [ ] T070 [US5] Create WaterDrop animation component in `frontend/src/components/plant/WaterDrop.vue` (SVG droplet that falls and fades)
- [ ] T071 [US5] Create StageTransition animation component in `frontend/src/components/plant/StageTransition.vue` (glow + morph between stages)
- [ ] T072 [US5] Integrate WaterDrop + StageTransition into PlantCanvas with animation queue for sequential playback
- [ ] T073 [US5] Add "max level" badge to PlantCanvas when plant reaches bloomed stage

**Checkpoint**: SSE stream delivers events; drop animation plays on new commit; stage transition animates on growth.

---

### Polish & Cross-Cutting Concerns

- [ ] T074 [P] Create backend unit tests for PlantGrowthService in `backend/tests/unit/test_plant_growth.py` (stage transitions, threshold logic, max stage)
- [ ] T075 [P] Create backend unit tests for DripCalculationService in `backend/tests/unit/test_drip_calculation.py`
- [ ] T076 [P] Create backend integration test for webhook ingestion → Redis queue → worker → DB in `backend/tests/integration/test_webhook_flow.py`
- [ ] T077 [P] Create frontend component tests for PlantCanvas in `frontend/tests/unit/PlantCanvas.spec.ts`
- [ ] T078 [P] Create frontend component tests for DropCounter in `frontend/tests/unit/DropCounter.spec.ts`
- [ ] T079 Create E2E test with Playwright at `frontend/tests/e2e/auth-flow.spec.ts` (GitHub OAuth → plant select → dashboard)
- [ ] T080 [P] Create README.md at root with project description, architecture overview, and setup instructions
- [ ] T081 Run quickstart.md validation: verify `docker compose up` boots all services cleanly

**Checkpoint**: All tests pass; `docker compose up` creates a fully working app.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Fase 1 (Configuración y Auth)**: No dependencies — starts first
  - Setup and Foundational must complete before US1
  - US1 completes end-to-end OAuth flow
- **Fase 2 (Backend y Webhooks)**: Depends on database models from Fase 1 Foundations
  - US3 builds plant/drop models, webhook endpoint, worker, growth logic
- **Fase 3 (Frontend y Lógica de la Planta)**: Depends on US1 being complete
  - US2 (plant select) depends on US1 (auth)
  - US4 (dashboard) depends on US2 (plant exists) and US3 (backend data available)
- **Fase 4 (Integración y Pulido)**: Depends on US4 (dashboard exists to animate)
  - US5 (animations) needs the dashboard + SSE infrastructure

### User Story Dependencies

- **US1 (P1)**: No dependencies — starts after Foundations
- **US2 (P1)**: Depends on US1 (user must be authenticated to select plant)
- **US3 (P2)**: Depends on US1 (user must be connected to receive drops) and Foundations (DB models)
- **US4 (P2)**: Depends on US2 (plant must exist) and US3 (drops must be populated)
- **US5 (P3)**: Depends on US4 (dashboard must render the plant)

### Within Each Phase

- Models before services
- Services before endpoints
- Backend before frontend integration
- Core logic before animations

### Parallel Opportunities

- T004–T008 (infrastructure files): All [P] — no shared dependencies
- T029–T031 (entities + config): All [P] — independent files
- T034–T035 (repository protocols): All [P] — independent files
- T056–T059 (SVG plant assets): All [P] — independent per plant type
- T074–T078 (tests): All [P] — different test files

---

## Parallel Execution Examples

```bash
# Fase 1 — Infrastructure files (all independent):
Task: T004 "Create docker-compose.yml"
Task: T005 "Create .env.example"
Task: T006 "Create backend/Dockerfile"
Task: T007 "Create frontend/Dockerfile"
Task: T008 "Configure linting tools"

# Fase 2 — Domain entities (all independent):
Task: T029 "Create PlantTypeConfig YAML loader"
Task: T030 "Create Plant domain entity"
Task: T031 "Create Drop domain entity"

# Fase 3 — Plant SVG assets (all independent):
Task: T056 "Create Cactus SVG assets"
Task: T057 "Create Bonsai SVG assets"
Task: T058 "Create Cannabis SVG assets"
Task: T059 "Create Fruit SVG assets"

# Fase 4 — Tests (all independent):
Task: T074 "PlantGrowthService unit tests"
Task: T075 "DripCalculationService unit tests"
Task: T076 "Webhook integration test"
Task: T077 "PlantCanvas component test"
Task: T078 "DropCounter component test"
```

---

## Implementation Strategy

### MVP First (Fase 1 Only)

1. Complete Setup + Foundations
2. Complete US1 (GitHub Auth)
3. **STOP**: End-to-end OAuth flow works — user can log in
4. Deploy/demo if ready

### Incremental Delivery

1. **Fase 1** → Config + Auth working (MVP: user can log in)
2. **Fase 2** → Backend processing drops + growing plant
3. **Fase 3** → Frontend renders plant state + dashboard
4. **Fase 4** → Real-time animations + polish

### Parallel Team Strategy

With multiple developers:
- Dev A: Fase 1 (Setup + US1 auth)
  - Dev B: Fase 2 plant domain entities (T029–T033) — parallel with Fase 1 infra
- Dev A + B: Fase 2 webhook + worker (T041–T048)
- Dev C: Fase 3 SVG assets + frontend components (T055–T066)
- Dev A: Fase 4 SSE + animations (T067–T073)
- Dev B + C: Tests + Polish (T074–T081)

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Tests (T074–T078) are optional — only include if TDD approach is chosen
- Commit after each task or logical group
- Stop at each fase checkpoint to validate independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
