from django.urls import path
from .views import audit_logs

app_name = "audit"

urlpatterns = [
    path("admin/audit-logs/", audit_logs, name="audit_logs"),
]
