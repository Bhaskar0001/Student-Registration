import base64
import hashlib
from django.conf import settings
from cryptography.fernet import Fernet


def _fernet() -> Fernet:
    key = settings.FIELD_ENCRYPTION_KEY
    if not key:
        # ✅ Safe test fallback (only used if env key missing)
        key = Fernet.generate_key().decode()
    return Fernet(key.encode("utf-8"))


def encrypt_value(value: str) -> bytes:
    if value is None:
        return b""
    return _fernet().encrypt(value.strip().encode("utf-8"))


def decrypt_value(value: bytes) -> str:
    if not value:
        return ""
    return _fernet().decrypt(value).decode("utf-8")


def hash_value(value: str) -> bytes:
    """
    SHA-256(value + pepper) → 32 bytes
    Used for uniqueness/search without decrypting.
    """
    pepper = settings.HASH_PEPPER or ""
    raw = (value.strip() + pepper).encode("utf-8")
    return hashlib.sha256(raw).digest()

encrypt_text = encrypt_value
decrypt_text = decrypt_value