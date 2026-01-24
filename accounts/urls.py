from django.urls import path
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy

from .views import ParentLoginView, AdminLoginView

app_name = "accounts"

urlpatterns = [
    path("parent/login/", ParentLoginView.as_view(), name="parent_login"),
    path("admin/login/", AdminLoginView.as_view(), name="admin_login"),

    # Logout MUST be POST in modern Django
    path("logout/", LogoutView.as_view(next_page=reverse_lazy("accounts:parent_login")), name="logout"),
]
