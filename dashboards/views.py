import csv
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils import timezone

from audit.models import StudentAuditLog
from students.models import Student
from .queries import fetch_dashboard_counts, fetch_dashboard_rows


def _is_admin(user) -> bool:
    return user.is_authenticated and (user.is_staff or user.is_superuser)


@login_required(login_url=reverse_lazy("accounts:admin_login"))
def admin_dashboard(request):
    if not _is_admin(request.user):
        messages.error(request, "Only admin users can access Admin Dashboard.")
        return redirect("accounts:admin_login")

    status = request.GET.get("status")
    counts = fetch_dashboard_counts()

    rows = fetch_dashboard_rows(limit=200, status=status)

    return render(request, "dashboards/admin_dashboard.html", {
        "counts": counts,
        "rows": rows,
        "status": status,
    })


@login_required(login_url=reverse_lazy("accounts:admin_login"))
def mark_active_now(request, student_id: int):
    if not _is_admin(request.user):
        messages.error(request, "Only admin users can perform this action.")
        return redirect("accounts:admin_login")

    s = get_object_or_404(Student, id=student_id)
    old = s.last_login_at
    s.last_login_at = timezone.now()
    s.save()

    changed_by = request.user.email or request.user.username or "admin"
    StudentAuditLog.objects.create(
        student=s,
        field_name="last_login_at",
        old_value=str(old) if old else "",
        new_value=str(s.last_login_at),
        changed_by=changed_by,
    )

    messages.success(request, f"Marked {s.full_name} as active now.")
    return redirect(reverse("dashboards:admin_dashboard"))


@login_required(login_url=reverse_lazy("accounts:admin_login"))
def export_engagement_csv(request):
    if not _is_admin(request.user):
        messages.error(request, "Only admin users can export reports.")
        return redirect("accounts:admin_login")

    status = request.GET.get("status")
    rows = fetch_dashboard_rows(limit=5000, status=status)

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="student_engagement_report.csv"'

    writer = csv.writer(response)
    writer.writerow(["Student UID", "Name", "Class", "Status", "Last Active", "Inactivity Days"])

    for r in rows:
        writer.writerow([
            r["student_uid"],
            r["full_name"],
            r["class_grade"],
            r["engagement_status"],
            r["last_login_at"] or "",
            r["inactivity_days"],
        ])

    return response


@login_required(login_url=reverse_lazy("accounts:admin_login"))
def encryption_proof(request):
    if not _is_admin(request.user):
        messages.error(request, "Only admin users can access this page.")
        return redirect("accounts:admin_login")

    students = Student.objects.order_by("-created_at")[:30]

    rows = []
    for s in students:
        # ✅ never crash if old bad rows exist
        try:
            email_dec = s.email
        except Exception as e:
            email_dec = f"[DECRYPT ERROR: {type(e).__name__}]"

        try:
            mobile_dec = s.mobile
        except Exception as e:
            mobile_dec = f"[DECRYPT ERROR: {type(e).__name__}]"

        rows.append({
            "student_uid": s.student_uid,
            "full_name": s.full_name,
            "class_grade": s.class_grade,
            "created_at": s.created_at,
            "email_dec": email_dec,
            "mobile_dec": mobile_dec,
            "email_enc_len": len(s.email_enc or b""),
            "mobile_enc_len": len(s.mobile_enc or b""),
            "email_hash_hex": (s.email_hash or b"").hex(),
            "mobile_hash_hex": (s.mobile_hash or b"").hex(),
        })

    return render(request, "dashboards/encryption_proof.html", {"rows": rows})