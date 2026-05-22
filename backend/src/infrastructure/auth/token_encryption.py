import base64
import hashlib

from cryptography.fernet import Fernet

from src.core.config.settings import settings


def _derive_fernet_key() -> bytes:
    raw = settings.secret_key.encode()
    digest = hashlib.sha256(raw).digest()
    return base64.urlsafe_b64encode(digest)


_cipher = Fernet(_derive_fernet_key())


def encrypt_token(token: str) -> tuple[bytes, bytes]:
    encrypted = _cipher.encrypt(token.encode())
    return encrypted, b"\0" * 16


def decrypt_token(encrypted_token: bytes, nonce: bytes) -> str:
    return _cipher.decrypt(encrypted_token).decode()
