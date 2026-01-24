import os
import requests
from django.conf import settings

def send_student_email(to_email: str, subject: str, body: str):
    api_key = os.getenv("RESEND_API_KEY", "")
    if not api_key:
        raise Exception("RESEND_API_KEY is missing in environment variables")

    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", "Student Portal <onboarding@resend.dev>")

    payload = {
        "from": from_email,
        "to": [to_email],
        "subject": subject,
        "text": body,
    }

    r = requests.post(
        "https://api.resend.com/emails",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=20,
    )

    if r.status_code >= 400:
        raise Exception(f"Resend error {r.status_code}: {r.text}")
