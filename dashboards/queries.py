# dashboards/queries.py
from __future__ import annotations

from django.utils import timezone
from students.models import Student

ACTIVE_DAYS = 7
AT_RISK_DAYS = 30


def _status_for_last_login(last_login_at):
    if not last_login_at:
        return ("inactive", 9999)

    days = (timezone.now() - last_login_at).days
    if days <= ACTIVE_DAYS:
        return ("active", days)
    if days <= AT_RISK_DAYS:
        return ("at_risk", days)
    return ("inactive", days)


def fetch_dashboard_counts() -> dict:
    qs = Student.objects.all().only("id", "last_login_at")

    total = qs.count()
    active = 0
    at_risk = 0
    inactive = 0

    for s in qs:
        status, _days = _status_for_last_login(s.last_login_at)
        if status == "active":
            active += 1
        elif status == "at_risk":
            at_risk += 1
        else:
            inactive += 1

    return {
        "total": total,
        "active": active,
        "at_risk": at_risk,
        "inactive": inactive,
    }


def fetch_dashboard_rows(limit: int = 200, status: str | None = None) -> list[dict]:
    qs = (
        Student.objects
        .all()
        .only("id", "student_uid", "full_name", "class_grade", "last_login_at", "created_at")
        .order_by("-created_at")
    )

    rows = []
    for s in qs[: max(limit, 1) * 5]:
        st, days = _status_for_last_login(s.last_login_at)

        if status and st != status:
            continue

        rows.append({
            "id": s.id,
            "student_uid": s.student_uid,
            "full_name": s.full_name,
            "class_grade": s.class_grade,
            "engagement_status": st,
            "last_login_at": s.last_login_at,
            "inactivity_days": days,
        })

        if len(rows) >= limit:
            break

    return rows
