from django.urls import path
from .views import parent_dashboard

app_name = "parents"

urlpatterns = [
    path("parent/dashboard/", parent_dashboard, name="parent_dashboard"),
]
