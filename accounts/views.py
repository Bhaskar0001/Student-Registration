from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect


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
        super().form_valid(form)
        user = self.request.user

        if user.is_staff or user.is_superuser:
            messages.error(self.request, "Admin accounts must login from Admin Login page.")
            return redirect("accounts:admin_login")

        return redirect("parents:parent_dashboard")


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
        super().form_valid(form)
        user = self.request.user

        if not (user.is_staff or user.is_superuser):
            messages.error(self.request, "Parent accounts must login from Parent Login page.")
            return redirect("accounts:parent_login")

        return redirect("dashboards:admin_dashboard")
