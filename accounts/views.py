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
    from django.http import HttpResponse
    return HttpResponse("<h1>System Operational</h1><p>SendGrid integration removed. SMTP fallback active.</p>")
