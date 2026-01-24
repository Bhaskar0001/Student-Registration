SENSITIVE_FIELDS = {"email_enc", "mobile_enc", "email_hash", "mobile_hash"}


def mask_if_sensitive(field_name: str, value) -> str:
    if field_name in SENSITIVE_FIELDS:
        return "[ENCRYPTED]"
    if value is None:
        return ""
    return str(value)
