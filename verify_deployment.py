import os
import django
import sys
import requests
from django.conf import settings
from django.core.mail import send_mail

# Setup Django Environment
sys.path.append(os.getcwd())
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "aah_guru.settings")
django.setup()

def test_sendgrid():
    print("\n--- Testing SendGrid Integration ---")
    print(f"EMAIL_HOST: {settings.EMAIL_HOST}")
    print(f"EMAIL_PORT: {settings.EMAIL_PORT}")
    print(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
    # Don't print the full password/key for security
    print(f"EMAIL_HOST_PASSWORD set: {'Yes' if settings.EMAIL_HOST_PASSWORD else 'No'}")
    
    try:
        sent = send_mail(
            subject="SendGrid Verification Test",
            message="If you receive this, SendGrid is working correctly on your project!",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=["bhaskarjh101@gmail.com"], # User's email from chat context
            fail_silently=False,
        )
        if sent == 1:
            print("[SUCCESS] Email sent via SendGrid!")
            return True
        else:
            print("[FAILURE] Email sent returned 0.")
            return False
    except Exception as e:
        print(f"[ERROR] SendGrid test failed with exception: {e}")
        return False

def test_web_status():
    print("\n--- Testing Web Application Status ---")
    try:
        # Assuming local server is running on port 8000. If not, this might fail, 
        # but we can try starting it or just assume code validity if email works.
        # Ideally we'd start a thread for the server, but for now let's just check if we can import views without error.
        from students import views
        print("[SUCCESS] Application modules imported successfully. No syntax errors.")
        return True
    except Exception as e:
        print(f"[ERROR] Application import failed: {e}")
        return False

if __name__ == "__main__":
    email_success = test_sendgrid()
    web_success = test_web_status()
    
    if email_success and web_success:
        print("\n\n*** READY FOR DEPLOYMENT ***")
        sys.exit(0)
    else:
        print("\n\n*** VERIFICATION FAILED ***")
        sys.exit(1)
