# GrowPlant 🌱

An interactive web application that gamifies your GitHub contribution history. Connect your GitHub account, pick a plant, and watch it grow as you commit code.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.11+, FastAPI, SQLAlchemy 2.0 (async), Alembic |
| Frontend | Vue 3 + TypeScript, Pinia, Vite |
| Database | PostgreSQL 16 |
| Queue | Redis 7 (message queue + pub/sub) |
| Auth | GitHub OAuth 2.0 |
| Encryption | Fernet (AES-256-GCM) |
| Infrastructure | Docker Compose |

## Architecture

```
backend/
├── src/
│   ├── core/          # Domain entities, services, repository ports
│   │   ├── entities/  # Plant, Drop, GrowthStage domain models
│   │   ├── services/  # PlantGrowthService, DripCalculationService
│   │   └── ports/     # Repository interfaces
│   ├── infrastructure/# DB, queue, GitHub API, auth implementations
│   │   ├── database/  # SQLAlchemy models + PostgreSQL repositories
│   │   ├── queue/     # Redis queue adapter
│   │   ├── github/    # Webhook verification, API client
│   │   └── auth/      # OAuth service, token encryption, JWT sessions
│   └── api/           # FastAPI routes, Pydantic schemas, middleware

frontend/
├── src/
│   ├── components/    # PlantCanvas, WaterDrop, DropCounter, etc.
│   ├── pages/         # LoginPage, PlantSelectPage, DashboardPage
│   ├── services/      # API clients + SSE event stream
│   ├── stores/        # Pinia stores (user, plant, drops)
│   └── assets/        # SVG plant sprites per type per stage
```

## Quick Start

```bash
# 1. Register a GitHub OAuth App at https://github.com/settings/developers
#    Homepage: http://localhost:8000
#    Callback: http://localhost:8000/api/auth/github/callback

# 2. Copy and edit environment
cp .env.example .env
# Fill in GITHUB_CLIENT_ID, GITHUB_CLIENT_SECRET, and SECRET_KEY

# 3. Launch everything
docker compose up --build
```

Then open http://localhost:5173 and click "Connect with GitHub".

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/health` | Health check |
| GET | `/api/auth/github/login` | GitHub OAuth login |
| GET | `/api/auth/github/callback` | OAuth callback |
| GET | `/api/auth/status` | Session status |
| POST | `/api/auth/logout` | Logout |
| POST | `/api/webhooks/github` | GitHub webhook receiver |
| GET | `/api/plants/types` | Available plant types |
| POST | `/api/plants/select` | Select a plant |
| GET | `/api/plants/mine` | My plant state |
| GET | `/api/dashboard` | Full dashboard |
| GET | `/api/dashboard/history` | Paginated drop history |
| GET | `/api/events/stream` | SSE real-time events |

## Plant Types

| Plant | Stages | Description |
|-------|--------|-------------|
| 🌵 Cactus | seed → sprout → young → mature → bloomed | Resilient and low-maintenance |
| 🌳 Bonsai | seed → sprout → young → mature → bloomed | Patience and discipline |
| 🌿 Cannabis | seed → sprout → young → mature → bloomed | Fast-growing and vibrant |
| 🍓 Fruit | seed → sprout → young → mature → bloomed | Bears fruit from your hard work |

Growth thresholds: seed (0) → sprout (5) → young (15) → mature (30) → bloomed (50)
