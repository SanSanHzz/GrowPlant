import hashlib
import hmac

from src.core.config.settings import settings


def verify_signature(payload_body: bytes, signature_header: str) -> bool:
    expected = hmac.new(
        settings.github_webhook_secret.encode(),
        payload_body,
        hashlib.sha256,
    ).hexdigest()
    expected_prefix = f"sha256={expected}"
    return hmac.compare_digest(expected_prefix, signature_header)
