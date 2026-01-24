from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta

from .models import StudentAuditLog
@staff_member_required
def audit_logs(request):
    logs = StudentAuditLog.objects.select_related("student").all()[:300]
    return render(request, "audit/logs.html", {"logs": logs})

@staff_member_required
def audit_logs(request):
    days = request.GET.get("days", "30")
    field = request.GET.get("field", "ALL")

    try:
        days_int = int(days)
    except ValueError:
        days_int = 30

    since = timezone.now() - timedelta(days=days_int)

    qs = StudentAuditLog.objects.select_related("student").filter(changed_at__gte=since).order_by("-changed_at")

    if field != "ALL":
        qs = qs.filter(field_name=field)

    # Build field dropdown options from common fields
    field_options = ["ALL", "SYSTEM_CREATE", "full_name", "class_grade", "email_enc", "mobile_enc", "last_login_at"]

    return render(request, "audit/logs.html", {
        "logs": qs[:500],
        "days": days_int,
        "field": field,
        "field_options": field_options,
    })
