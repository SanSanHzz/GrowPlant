# Research: GitHub Plant Gamification

## Backend Framework: FastAPI (Python 3.11+)

- **Decision**: FastAPI with Python 3.11+
- **Rationale**:
  - Python's `asyncio` provides first-class async I/O — ideal for non-blocking webhook
    ingestion required by Constitution Principle II (Data Scalability).
  - FastAPI is the fastest Python web framework (Starlette-based) and outperforms
    Express.js for I/O-bound workloads.
  - Automatic OpenAPI/Swagger documentation eliminates manual contract drift.
  - Pydantic v2 provides compile-time and runtime type validation.
  - SQLAlchemy 2.0 + Alembic is the most mature Python PostgreSQL toolchain.
  - Dependency injection system maps naturally to Clean Architecture (Principle III).
- **Alternatives considered**:
  - **Express.js**: Adequate async support via `async/await` but lacks built-in
    validation, auto-docs, and DI. Would require added layers (Joi, Swagger, tsyringe)
    increasing complexity — violates Principle I (Simplicity).
  - **NestJS**: Strong architecture but heavier framework with steeper learning curve.
    Overkill for a focused single-user dashboard. Python ecosystem better aligned with
    project's data-processing needs.

## Frontend Framework: Vue.js 3 + TypeScript

- **Decision**: Vue.js 3 (Composition API) with TypeScript, Pinia, and Vite
- **Rationale**:
  - Vue's `<Transition>` and `<TransitionGroup>` built-in components map perfectly to
    plant growth animations (sprouting, blooming, watering effects).
  - Pinia is simpler than Redux/Zustand — no boilerplate, TypeScript-native, perfect
    for focused state (user, plant, drops).
  - Composition API enables clean separation of plant rendering logic per type,
    supporting Principle IV (Visual Modularity).
  - Smaller bundle size than React for this scope (~30% smaller initial payload).
  - Vite's HMR is significantly faster than webpack/CRA for development.
  - Declarative templates make SVG rendering intuitive (plant parts as components).
- **Alternatives considered**:
  - **React 18**: Strong ecosystem but JSX + SVG animations require more manual work
    (framer-motion or react-spring). Redux/Zustand adds cognitive overhead for 3 stores.
    Vue's transition system provides better developer experience for this visual domain.

## Infrastructure Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Message Queue | **Redis** (via `rq` or `arq`) | Lightweight, in-memory, acts as cache too. Constitution II requires async processing. Redis is simpler than RabbitMQ for this scale. |
| Containerization | **Docker Compose** | Constitution I — one-command local bootstrapping with `docker compose up` |
| Testing | **pytest** (backend), **Vitest** (frontend), **Playwright** (E2E) | pytest for async test support; Vitest integrates with Vite; Playwright for real browser tests |
| Code Quality | **Ruff** (Python), **ESLint + Prettier** (frontend) | Ruff is fastest Python linter; standard JS toolchain |
| SVG Rendering | **Custom Vue components** (no framework) | Plants are visual domain — custom SVG components per type provide full control for modularity (Principle IV) |
| Auth Flow | **GitHub OAuth 2.0** (OAuth app) | Spec requirement; FastAPI has `authlib` library for OAuth flow |

## Data Flow: Webhook → Plant Growth

1. GitHub sends POST to `/api/webhooks/github` with push/pull_request event
2. FastAPI endpoint receives payload, verifies signature (HMAC-SHA256), enqueues job to Redis
3. Endpoint returns 200 immediately — **never blocks on DB writes** (Constitution II)
4. Background worker (`arq` Redis worker) picks up job, calls GitHub API for commit details
5. Worker persists drop record to PostgreSQL, recalculates plant growth stage
6. If stage changed, worker publishes event to Redis pub/sub channel
7. Frontend's WebSocket connection (via FastAPI `socket.io` or SSE) receives event
8. Vue's Pinia store updates drop counter and growth stage reactively
9. Vue `<Transition>` component triggers watering/growth animation on the SVG plant
