from django.urls import path
from .views import admin_dashboard, export_engagement_csv, mark_active_now, encryption_proof

app_name = "dashboards"

urlpatterns = [
    path("admin/dashboard/", admin_dashboard, name="admin_dashboard"),
    path("admin/students/<int:student_id>/mark-active/", mark_active_now, name="mark_active_now"),
    path("admin/export/engagement.csv", export_engagement_csv, name="export_engagement_csv"),
    path("admin/security/encryption-proof/", encryption_proof, name="encryption_proof"),
]
