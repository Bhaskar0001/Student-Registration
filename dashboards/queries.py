from dataclasses import dataclass
from datetime import timedelta
from django.utils import timezone
from students.models import Student

ACTIVE_DAYS = 7
AT_RISK_DAYS = 30


@dataclass
class Counts:
    total: int
    active: int
    at_risk: int
    inactive: int


def _status_for(last_login_at):
    now = timezone.now()
    if not last_login_at:
        return "inactive", 9999

    days = (now - last_login_at).days

    if days <= ACTIVE_DAYS:
        return "active", days
    if days <= AT_RISK_DAYS:
        return "at_risk", days
    return "inactive", days


def fetch_dashboard_counts() -> Counts:
    now = timezone.now()
    active_cutoff = now - timedelta(days=ACTIVE_DAYS)
    at_risk_cutoff = now - timedelta(days=AT_RISK_DAYS)

    total = Student.objects.count()
    active = Student.objects.filter(last_login_at__gte=active_cutoff).count()
    at_risk = Student.objects.filter(last_login_at__lt=active_cutoff, last_login_at__gte=at_risk_cutoff).count()
    inactive = Student.objects.filter(last_login_at__lt=at_risk_cutoff).count() + Student.objects.filter(last_login_at__isnull=True).count()

    return Counts(total=total, active=active, at_risk=at_risk, inactive=inactive)


def fetch_dashboard_rows(limit=200, status=None):
    qs = Student.objects.all().order_by("-created_at").prefetch_related("parent_links__parent")

    now = timezone.now()
    active_cutoff = now - timedelta(days=ACTIVE_DAYS)
    at_risk_cutoff = now - timedelta(days=AT_RISK_DAYS)

    if status == "active":
        qs = qs.filter(last_login_at__gte=active_cutoff)
    elif status == "at_risk":
        qs = qs.filter(last_login_at__lt=active_cutoff, last_login_at__gte=at_risk_cutoff)
    elif status == "inactive":
        qs = qs.filter(last_login_at__lt=at_risk_cutoff) | qs.filter(last_login_at__isnull=True)

    rows = []
    for s in qs[:limit]:
        st, days = _status_for(s.last_login_at)

        # first parent (if any)
        parent_name = "-"
        relationship = "-"
        link = next(iter(getattr(s, "parent_links").all()), None)
        if link:
            parent_name = link.parent.full_name
            relationship = link.relationship

        rows.append({
            "id": s.id,
            "student_uid": s.student_uid,
            "full_name": s.full_name,
            "class_grade": s.class_grade,
            "last_login_at": s.last_login_at,
            "inactivity_days": days,
            "engagement_status": st,
            "parent_name": parent_name,
            "relationship": relationship,
        })

    return rows
