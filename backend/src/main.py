from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routes.auth import router as auth_router
from src.api.routes.dashboard import router as dashboard_router
from src.api.routes.plants import router as plants_router
from src.api.routes.webhooks import router as webhooks_router

app = FastAPI(
    title="GrowPlant API",
    version="0.1.0",
    description="GitHub Plant Gamification Backend",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(webhooks_router)
app.include_router(plants_router)
app.include_router(dashboard_router)


@app.get("/api/health")
async def health():
    return {"status": "ok", "version": "0.1.0"}
