import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

logger = logging.getLogger("growplant")

from src.api.routes.auth import router as auth_router
from src.api.routes.dashboard import router as dashboard_router
from src.api.routes.events import router as events_router
from src.api.routes.plants import router as plants_router
from src.api.routes.webhooks import router as webhooks_router
from src.core.config.settings import settings

app = FastAPI(
    title="GrowPlant API",
    version="0.1.0",
    description="GitHub Plant Gamification Backend",
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    print(f">>> {request.method} {request.url}", flush=True)
    response = await call_next(request)
    print(f"<<< {request.method} {request.url.path} -> {response.status_code}", flush=True)
    return response


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
app.include_router(events_router)


async def run_migrations():
    try:
        from alembic.command import upgrade
        from alembic.config import Config

        alembic_cfg = Config("alembic.ini")
        sync_url = settings.database_url.replace(
            "postgresql+asyncpg://", "postgresql://"
        )
        alembic_cfg.set_main_option("sqlalchemy.url", sync_url)
        upgrade(alembic_cfg, "head")
    except Exception as e:
        logger.warning("Migration skipped: %s", e)


@app.on_event("startup")
async def on_startup():
    logger.info("Running database migrations...")
    await run_migrations()
    logger.info("Startup complete")


@app.get("/favicon.ico")
async def favicon():
    return JSONResponse(content={}, status_code=204)


@app.get("/api/health")
async def health():
    engine = create_async_engine(settings.database_url)
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        db_ok = True
    except Exception:
        db_ok = False
    finally:
        await engine.dispose()
    return {"status": "ok" if db_ok else "degraded", "version": "0.1.0"}
