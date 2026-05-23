import logging
from datetime import UTC, datetime

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from src.api.middleware.auth import get_current_user_id
from src.api.schemas.auth import (
    AuthStatusResponse,
    LogoutResponse,
    UserResponse,
)
from src.core.ports.user_repository import UserData
from src.infrastructure.auth.github_oauth import GitHubOAuthService
from src.infrastructure.auth.session import (
    create_session_token,
)
from src.infrastructure.auth.token_encryption import encrypt_token
from src.infrastructure.database.engine import async_session_factory
from src.infrastructure.database.repositories.user_repository import (
    PostgresUserRepository,
)

logger = logging.getLogger("growplant.auth")
router = APIRouter(prefix="/api/auth", tags=["auth"])
oauth_service = GitHubOAuthService()


def _user_to_response(user):
    return UserResponse(
        id=user.id,
        github_id=user.github_id,
        username=user.username,
        display_name=user.display_name,
        avatar_url=user.avatar_url,
    )


@router.get("/github/login")
async def github_login():
    import secrets
    state = secrets.token_urlsafe(16)
    url = oauth_service.get_authorization_url(state)
    logger.info("Login redirect URL generated: %s...", url[:80])
    return RedirectResponse(url=url, status_code=302)


@router.get("/github/callback")
async def github_callback(
    request: Request,
    code: str | None = None,
    state: str | None = None,
):
    logger.info("Callback received. URL: %s", request.url)
    logger.info("Query params: code=%s, state=%s", code, state)

    if not code:
        logger.warning("No code in callback")
        return HTMLResponse(
            content="""<html><body>
<p>No authorization code received.</p>
<p><a href="http://localhost:5173">Go back to GrowPlant</a></p>
</body></html>""",
            status_code=200,
        )

    try:
        result = await oauth_service.exchange_code(code)
        logger.info("GitHub token exchange OK. User: %s", result.user.username)
    except Exception as e:
        logger.error("Token exchange failed: %s", e)
        return RedirectResponse(
            url=f"http://localhost:5173/?error=GitHub+token+exchange+failed:+{e}",
            status_code=302,
        )

    encrypted, nonce = encrypt_token(result.access_token)

    async with async_session_factory() as session:
        repo = PostgresUserRepository(session)
        existing = await repo.get_by_github_id(result.user.github_id)

        if existing:
            await repo.update_token(existing.id, encrypted, nonce)
            user = await repo.get_by_id(existing.id)
            logger.info("Existing user updated: %s", user.username)
        else:
            user = await repo.create(
                UserData(
                    github_id=result.user.github_id,
                    username=result.user.username,
                    display_name=result.user.display_name,
                    avatar_url=result.user.avatar_url,
                    encrypted_token=encrypted,
                    token_nonce=nonce,
                    github_connected_at=datetime.now(UTC),
                )
            )
            logger.info("New user created: %s", user.username)
        await session.commit()

    session_token = create_session_token(user.id)
    logger.info("Session token created, redirecting to frontend")

    return HTMLResponse(
        content=f"""<html><body>
<script>window.location.replace("http://localhost:5173/?token={session_token}");
</script></body></html>""",
        status_code=200,
    )


@router.get("/status", response_model=AuthStatusResponse)
async def auth_status(request: Request):
    user_id = await get_current_user_id(request)
    if user_id is None:
        return AuthStatusResponse(authenticated=False, user=None)

    from uuid import UUID
    async with async_session_factory() as session:
        repo = PostgresUserRepository(session)
        user = await repo.get_by_id(UUID(user_id))

    if user is None:
        return AuthStatusResponse(authenticated=False, user=None)

    return AuthStatusResponse(
        authenticated=True,
        user=_user_to_response(user),
    )


@router.post("/logout", response_model=LogoutResponse)
async def auth_logout():
    return LogoutResponse(message="Logged out successfully")
