from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone

from .models import Parent, StudentParent


@login_required
def parent_dashboard(request):
    if request.user.is_staff or request.user.is_superuser:
        messages.info(request, "Admin accounts cannot access the Parent Portal.")
        return redirect("dashboards:admin_dashboard")

    try:
        parent = Parent.objects.get(user=request.user)
    except Parent.DoesNotExist:
        return render(request, "parents/not_linked.html")

    links = StudentParent.objects.select_related("student").filter(parent=parent)

    items = []
    now = timezone.now()

    for link in links:
        s = link.student
        last = s.last_login_at

        if last:
            days = (now - last).days
            status = "AT_RISK" if days > 7 else "ACTIVE"
        else:
            days = None
            status = "AT_RISK"

        items.append({
            "student_uid": s.student_uid,
            "full_name": s.full_name,
            "class_grade": s.class_grade,
            "last_login_at": last,
            "days": days,
            "status": status,
        })

    return render(request, "parents/dashboard.html", {"parent": parent, "items": items})
