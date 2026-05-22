# Quickstart: GitHub Plant Gamification

## Prerequisites

- Docker & Docker Compose (v2.20+)
- Git
- A GitHub OAuth App registered at https://github.com/settings/developers
  - Homepage URL: `http://localhost:8000`
  - Authorization callback URL: `http://localhost:8000/api/auth/github/callback`

## Setup

```bash
# 1. Clone and enter the project
git clone <repo-url>
cd growplant

# 2. Configure environment
cp .env.example .env
# Edit .env with your GitHub OAuth credentials:
#   GITHUB_CLIENT_ID=your_client_id
#   GITHUB_CLIENT_SECRET=your_client_secret
#   GITHUB_WEBHOOK_SECRET=your_webhook_secret
#   SECRET_KEY=generate_a_random_key

# 3. Start all services
docker compose up --build
```

## Access

| Service | URL |
|---------|-----|
| Frontend | http://localhost:5173 |
| Backend API | http://localhost:8000 |
| API Docs (Swagger) | http://localhost:8000/docs |
| PostgreSQL | localhost:5432 |
| Redis | localhost:6379 |

## Configure GitHub Webhook

1. Go to your GitHub repository → Settings → Webhooks → Add webhook
2. Payload URL: `http://<your-public-url>/api/webhooks/github`
3. Content type: `application/json`
4. Secret: same as `GITHUB_WEBHOOK_SECRET` in `.env`
5. Events: Select "Push" and "Pull requests"
6. Enable SSL verification only if using HTTPS

## First Run

1. Open `http://localhost:5173` in your browser
2. Click "Connect with GitHub" — OAuth flow redirects you
3. Select a plant type from the 4 options
4. The dashboard loads with your plant as a seed
5. Initial contribution history imports automatically (past 12 months)
6. Push new commits to see watering animations in real time
