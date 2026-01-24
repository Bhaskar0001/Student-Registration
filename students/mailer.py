import os
import requests

def send_student_email(to_email: str, subject: str, body: str):
    api_key = os.getenv("RESEND_API_KEY", "")
    from_email = os.getenv("DEFAULT_FROM_EMAIL", "no-reply@yourdomain.com")

    if not api_key:
        raise RuntimeError("RESEND_API_KEY is missing in environment variables.")

    r = requests.post(
        "https://api.resend.com/emails",
        headers={"Authorization": f"Bearer {api_key}"},
        json={
            "from": from_email,
            "to": [to_email],
            "subject": subject,
            "text": body,
        },
        timeout=20,
    )

    if r.status_code >= 400:
        raise RuntimeError(f"Resend error {r.status_code}: {r.text}")
