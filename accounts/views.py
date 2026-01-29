from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from students.mailer import send_student_email
from django.conf import settings
from django.http import HttpResponse
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)


class ParentLoginView(LoginView):
    template_name = "accounts/parent_login.html"
    redirect_authenticated_user = False

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_staff or request.user.is_superuser:
                return redirect("dashboards:admin_dashboard")
            return redirect("parents:parent_dashboard")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.get_user()
        
        if user.is_staff or user.is_superuser:
            messages.error(self.request, "Admin accounts must login from Admin Login page.")
            return redirect("accounts:admin_login")

        response = super().form_valid(form)

        if user.email:
            try:
                subject = "Login Notification"
                body = f"Hello {user.first_name or 'Parent'},\n\nYour account was just logged into.\n\nTime: {timezone.now()}\n\nIf this was not you, please contact support."
                send_student_email(user.email, subject, body)
            except Exception as e:
                logger.error(f"Failed to send login notification: {e}")

        return response


class AdminLoginView(LoginView):
    template_name = "accounts/admin_login.html"
    redirect_authenticated_user = False

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_staff or request.user.is_superuser:
                return redirect("dashboards:admin_dashboard")
            return redirect("parents:parent_dashboard")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.get_user()

        if not (user.is_staff or user.is_superuser):
            messages.error(self.request, "Parent accounts must login from Parent Login page.")
            return redirect("accounts:parent_login")

        return super().form_valid(form)

def diagnostic_check(request):
    """
    Diagnostic view to check environment variables on the live site.
    (This is safe because it only shows presence, not actual values).
    """
    status = ["<h2>⚙️ Production System Diagnostic</h2>"]

    # 1. Check DEBUG
    status.append(f"<b>DEBUG Mode:</b> {'🚨 ON (Security risk!)' if settings.DEBUG else '✅ OFF (Production)'}")

    # 2. Check Database
    try:
        from django.db import connection
        connection.ensure_connection()
        status.append("<b>Database:</b> ✅ Connected")
    except Exception as e:
        status.append(f"<b>Database:</b> ❌ ERROR ({e})")

    # 3. Check Critical Keys (Presence only)
    keys_to_check = {
        "DJANGO_SECRET_KEY": "SECRET_KEY",
        "FIELD_ENCRYPTION_KEY": "FIELD_ENCRYPTION_KEY",
        "HASH_PEPPER": "HASH_PEPPER",
        "SMTP_USER": "EMAIL_HOST_USER",
        "SMTP_PASSWORD": "EMAIL_HOST_PASSWORD",
    }

    for env_name, settings_name in keys_to_check.items():
        val = getattr(settings, settings_name, "")
        if val and not str(val).startswith("django-insecure"):
            status.append(f"<b>{env_name}:</b> ✅ Present")
        else:
            status.append(f"<b>{env_name}:</b> ❌ MISSING or INSECURE")

    # 4. Check ALLOWED_HOSTS
    status.append(f"<b>ALLOWED_HOSTS:</b> {settings.ALLOWED_HOSTS}")

    html = "<div style='font-family: sans-serif; line-height: 1.6;'>" + "<br>".join(status) + "</div>"
    return HttpResponse(html)
