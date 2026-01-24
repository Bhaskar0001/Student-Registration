# dashboards/queries.py
from datetime import timedelta
from django.utils import timezone
from students.models import Student

ACTIVE_DAYS = 7
AT_RISK_DAYS = 30  # >7 and <=30

def _status_for(last_login_at):
    now = timezone.now()
    if not last_login_at:
        return "inactive"
    days = (now - last_login_at).days
    if days <= ACTIVE_DAYS:
        return "active"
    if days <= AT_RISK_DAYS:
        return "at_risk"
    return "inactive"

def fetch_dashboard_counts():
    now = timezone.now()
    active_cutoff = now - timedelta(days=ACTIVE_DAYS)
    at_risk_cutoff = now - timedelta(days=AT_RISK_DAYS)

    total = Student.objects.count()
    active = Student.objects.filter(last_login_at__gte=active_cutoff).count()
    at_risk = Student.objects.filter(last_login_at__lt=active_cutoff, last_login_at__gte=at_risk_cutoff).count()
    inactive = Student.objects.filter(last_login_at__isnull=True).count() + Student.objects.filter(last_login_at__lt=at_risk_cutoff).count()

    return {
        "total": total,
        "active": active,
        "at_risk": at_risk,
        "inactive": inactive,
    }

def fetch_dashboard_rows(limit=200, status=None):
    qs = Student.objects.all().order_by("-created_at")

    now = timezone.now()
    active_cutoff = now - timedelta(days=ACTIVE_DAYS)
    at_risk_cutoff = now - timedelta(days=AT_RISK_DAYS)

    if status == "active":
        qs = qs.filter(last_login_at__gte=active_cutoff)
    elif status == "at_risk":
        qs = qs.filter(last_login_at__lt=active_cutoff, last_login_at__gte=at_risk_cutoff)
    elif status == "inactive":
        qs = qs.filter(last_login_at__isnull=True) | qs.filter(last_login_at__lt=at_risk_cutoff)

    qs = qs[:limit]

    rows = []
    for s in qs:
        last = s.last_login_at
        inactivity_days = 9999 if not last else (now - last).days
        rows.append({
            "id": s.id,
            "student_uid": s.student_uid,
            "full_name": s.full_name,
            "class_grade": s.class_grade,
            "engagement_status": _status_for(last),
            "last_login_at": last,
            "inactivity_days": inactivity_days,
        })
    return rows
