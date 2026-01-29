from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def send_student_email(to_email: str, subject: str, body: str):
    """
    Sends an email using the configured Django EMAIL_BACKEND.
    """
    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", "noreply@student-portal.com")

    try:
        send_mail(
            subject=subject,
            message=body,
            from_email=from_email,
            recipient_list=[to_email],
            fail_silently=True,  # Critical for production: ensures the site doesn't 500 if Gmail is slow.
        )
    except Exception as e:
        logger.error(f"Failed to send email to {to_email}: {e}")
        # Re-raise so views can handle/log it or show a message
        raise e

