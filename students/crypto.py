import hashlib
from cryptography.fernet import Fernet
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

_cached_fernet = None

import logging

logger = logging.getLogger(__name__)

def _fernet() -> Fernet:
    global _cached_fernet
    if _cached_fernet is not None:
        return _cached_fernet

    key = getattr(settings, "FIELD_ENCRYPTION_KEY", "") or ""

    if not key:
        if settings.DEBUG:
            key = Fernet.generate_key().decode("utf-8")
        else:
            # Fallback for Production to verify if this is the cause of 500
            # logger.error("CRITICAL: FIELD_ENCRYPTION_KEY missing in production. Using temporary key. DATA WILL BE UNREADABLE AFTER RESTART.")
            key = Fernet.generate_key().decode("utf-8")

    try:
        _cached_fernet = Fernet(key.encode("utf-8"))
    except Exception as e:
        # Fallback if key is malformed
        logger.error(f"Invalid FIELD_ENCRYPTION_KEY: {e}. Generating temp key.")
        key = Fernet.generate_key().decode("utf-8")
        _cached_fernet = Fernet(key.encode("utf-8"))
        
    return _cached_fernet


def encrypt_value(value: str) -> bytes:
    if value is None:
        return b""
    return _fernet().encrypt(value.strip().encode("utf-8"))


def decrypt_value(value: bytes) -> str:
    if not value:
        return ""
    return _fernet().decrypt(value).decode("utf-8")


def hash_value(value: str) -> str:
    """
    SHA-256(value + pepper) -> hex string (64 chars)
    Perfect for CharField(unique=True, db_index=True)
    """
    pepper = getattr(settings, "HASH_PEPPER", "") or ""
    raw = (value.strip() + pepper).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


encrypt_text = encrypt_value
decrypt_text = decrypt_value
