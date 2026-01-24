from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

def home(request):
    return redirect("students:register")

urlpatterns = [
    path("", home, name="home"),
    path("django-admin/", admin.site.urls),

    path("", include("students.urls")),
    path("", include("engagement.urls")),
    path("", include("parents.urls")),
    path("", include("audit.urls")),
]
