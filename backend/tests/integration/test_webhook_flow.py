"""Integration test: webhook endpoint → Redis queue → worker → DB.

NOTE: This test requires a running PostgreSQL and Redis instance.
Set DATABASE_URL and REDIS_URL environment variables or update defaults below.
"""
import json
import pytest
from httpx import AsyncClient, ASGITransport

from src.main import app
from src.core.config.settings import settings


pytestmark = pytest.mark.skipif(
    not settings.database_url or "localhost" not in settings.database_url,
    reason="Requires local PostgreSQL + Redis",
)


@pytest.fixture
def client():
    transport = ASGITransport(app=app)
    return AsyncClient(transport=transport, base_url="http://test")


@pytest.mark.asyncio
async def test_webhook_endpoint_rejects_no_signature(client):
    payload = {"ref": "refs/heads/main", "commits": []}
    resp = await client.post(
        "/api/webhooks/github",
        json=payload,
    )
    assert resp.status_code == 400
    assert "signature" in resp.text.lower()


@pytest.mark.asyncio
async def test_health_endpoint(client):
    resp = await client.get("/api/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"
