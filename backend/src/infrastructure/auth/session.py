from datetime import UTC, datetime, timedelta
from uuid import UUID

from joserfc.jwk import OctKey
from joserfc.jwt import decode as jwt_decode
from joserfc.jwt import encode as jwt_encode

from src.core.config.settings import settings


def _derive_jwt_secret() -> str:
    import hashlib
    return hashlib.sha256(settings.secret_key.encode()).hexdigest()


_jwk = OctKey.import_key({"k": _derive_jwt_secret(), "kty": "oct"})


def create_session_token(user_id: UUID) -> str:
    now = datetime.now(UTC)
    claims = {
        "sub": str(user_id),
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(days=7)).timestamp()),
    }
    return jwt_encode(claims, _jwk)


def verify_session_token(token: str) -> UUID | None:
    try:
        decoded = jwt_decode(token, _jwk)
        return UUID(decoded.claims["sub"])
    except Exception:
        return None
