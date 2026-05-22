# Implementation Plan: GitHub Plant Gamification

**Branch**: `001-github-plant` | **Date**: 2026-05-22 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `specs/001-github-plant/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/plan-template.md` for the execution workflow.

## Summary

An interactive SPA that gamifies GitHub contribution history. Users connect via GitHub OAuth,
select a plant type (Cactus, Bonsai, Cannabis, Fruit), and watch it grow through 5 stages
(seed → sprout → young → mature → bloomed) as commits translate into water drops. A FastAPI
backend ingests GitHub webhooks asynchronously via Redis queue, persists to PostgreSQL, and
serves a Vue 3 + TypeScript frontend that renders the plant with growth animations.

## Technical Context

<!--
  The user specified stack options. Phase 0 research will resolve the final choices.
  Key knowns: PostgreSQL, GitHub OAuth, dark mode, monorepo (frontend/backend).
-->

**Language/Version**:
- Backend: Python 3.11+ (FastAPI) or Node.js 20+ (Express/NestJS) — resolved in research
- Frontend: TypeScript 5+ with Vue.js 3 or React 18 — resolved in research

**Primary Dependencies**:
- Backend: FastAPI or Express/NestJS; SQLAlchemy + Alembic or Prisma/TypeORM
- Frontend: Vue 3 or React; SVG rendering library for plant visuals
- Infrastructure: PostgreSQL, Redis (message queue), Docker Compose

**Storage**: PostgreSQL 16 — primary data store for users, plants, drops, growth history

**Testing**:
- Backend: pytest (if Python) or Vitest/Jest (if Node)
- Frontend: Vitest + Vue Test Utils or React Testing Library
- E2E: Playwright

**Target Platform**: Linux server (Docker container); modern browsers (Chrome, Firefox, Safari, Edge last 2 versions)

**Project Type**: Web application — monorepo with `backend/` and `frontend/` workspaces

**Performance Goals**:
- Webhook endpoint responds in <200ms (p95) to meet GitHub delivery expectations
- Dashboard initial load <2s
- Plant stage transitions render in <500ms

**Constraints**:
- No plaintext credentials (Constitution V)
- Async webhook ingestion only (Constitution II)
- Plant rendering decoupled from business logic (Constitution IV)
- Single-user mode for v1 (spec assumption)

**Scale/Scope**: Single-user personal dashboard with potential multi-tenancy in future

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Pre-Design Evaluation

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Deployment Simplicity | ✅ PASS | Docker Compose provided; single `.env` config; dependencies declared in `package.json` / `pyproject.toml` |
| II. Data Scalability | ✅ PASS | Redis queue decouples webhook ingestion from DB writes; async processing |
| III. Clean Architecture | ✅ PASS | `backend/src/core/` (domain) → `backend/src/services/` → `backend/src/api/`; frontend/backend fully separated |
| IV. Visual Modularity | ✅ PASS | Plant types defined as config; growth stages per type; SVG components swappable |
| V. Security & Privacy | ✅ PASS | GitHub tokens encrypted via env vars; only `public_repo` scope; no plaintext storage |

### Post-Design Re-Evaluation

| Principle | Status | Evidence |
|-----------|--------|----------|
| I. Deployment Simplicity | ✅ PASS | `docker-compose.yml` orchestrates 4 services (postgres, redis, backend, frontend); `.env.example` documents all config vars; `quickstart.md` provides one-command boot |
| II. Data Scalability | ✅ PASS | Webhook endpoint returns 202 in <200ms and enqueues to Redis (contract `api-webhooks.md`); background `arq` worker persist asynchronously; idempotency via `github_event_id` UNIQUE index |
| III. Clean Architecture | ✅ PASS | `backend/src/core/entities/` has zero infra imports; `backend/src/infrastructure/` implements `core/ports/` interfaces; API routes in `api/` depend only on services, not DB |
| IV. Visual Modularity | ✅ PASS | `PlantTypeConfig` is external YAML — adding a plant means adding one config file + SVG assets folder; growth thresholds are per-type config, not hardcoded |
| V. Security & Privacy | ✅ PASS | Token stored as `encrypted_token` + `token_nonce` (BYTEA, AES-256-GCM); OAuth scope limited to `read:user,public_repo`; no private repo data collected by default |

**Result**: All gates pass. No complexity justification required.

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
├── backend/
│   ├── src/
│   │   ├── core/               # Domain entities, business logic (plant, growth, drops)
│   │   │   ├── entities/       # Plant, User, Drop, GrowthStage domain models
│   │   │   ├── services/       # PlantGrowthService, DripCalculationService
│   │   │   └── ports/          # Interfaces (repository, queue, auth ports)
│   │   ├── infrastructure/
│   │   │   ├── database/       # SQLAlchemy models, Alembic migrations, PostgreSQL repo
│   │   │   ├── queue/          # Redis queue adapter (producer/consumer)
│   │   │   ├── github/         # GitHub API client, webhook verification
│   │   │   └── auth/           # GitHub OAuth flow handler, token encryption
│   │   ├── api/
│   │   │   ├── routes/         # FastAPI route modules (auth, plants, webhooks, dashboard)
│   │   │   ├── schemas/        # Pydantic request/response schemas
│   │   │   └── middleware/     # Auth middleware, error handlers
│   │   └── main.py             # FastAPI app entry point
│   ├── tests/
│   │   ├── unit/               # Core business logic tests (no infra)
│   │   ├── integration/        # DB + API integration tests
│   │   └── contract/           # API contract tests
│   ├── alembic/
│   ├── pyproject.toml
│   └── Dockerfile
│
├── frontend/
│   ├── src/
│   │   ├── components/         # Reusable UI components
│   │   │   ├── plant/          # PlantCanvas, WaterDrop, StageTransition animations
│   │   │   ├── auth/           # LoginButton, UserMenu
│   │   │   └── dashboard/      # DropCounter, DropHistory, ProgressBar
│   │   ├── pages/              # Route-level components
│   │   │   ├── LoginPage.vue
│   │   │   ├── PlantSelectPage.vue
│   │   │   └── DashboardPage.vue
│   │   ├── services/           # API client, webSocket connection
│   │   ├── stores/             # Pinia stores (user, plant, drops)
│   │   ├── types/              # TypeScript interfaces matching backend schemas
│   │   ├── assets/             # Plant SVG definitions per type per stage
│   │   └── App.vue
│   ├── tests/
│   │   ├── unit/
│   │   └── e2e/
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   └── Dockerfile
│
├── docker-compose.yml          # Postgres, Redis, backend, frontend
├── .env.example
└── README.md
```

**Structure Decision**: Option 2 — monorepo web application with separated `backend/`
and `frontend/` workspaces. `backend/src/core/` enforces Clean Architecture by isolating
domain entities from infrastructure. Frontend uses Vue 3 with TypeScript.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
