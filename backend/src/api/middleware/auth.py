from fastapi import HTTPException, Request

from src.infrastructure.auth.session import verify_session_token


async def get_current_user_id(request: Request) -> str | None:
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        return None
    token = auth.removeprefix("Bearer ")
    user_id = verify_session_token(token)
    return str(user_id) if user_id else None


async def require_auth(request: Request) -> str:
    user_id = await get_current_user_id(request)
    if user_id is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return user_id
