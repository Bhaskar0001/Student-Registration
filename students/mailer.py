from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def send_student_email(to_email: str, subject: str, body: str) -> bool:
    """
    Sends an email using the configured Django EMAIL_BACKEND.
    Returns True if successful, False otherwise.
    """
    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", "noreply@student-portal.com")

    try:
        sent = send_mail(
            subject=subject,
            message=body,
            from_email=from_email,
            recipient_list=[to_email],
            fail_silently=False,  # Set to False so we catch it in the try block
        )
        return bool(sent)
    except Exception as e:
        logger.error(f"Failed to send email to {to_email}: {e}")
        return False

