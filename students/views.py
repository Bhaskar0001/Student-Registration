from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.db import IntegrityError, transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .forms import StudentRegistrationForm, StudentEditForm
from .models import Student
from audit.models import StudentAuditLog


def _who(request) -> str:
    if request.user.is_authenticated:
        return request.user.email or request.user.username or "admin_or_system"
    return "admin_or_system"


def _is_admin(user) -> bool:
    return user.is_authenticated and (user.is_staff or user.is_superuser)


def _make_student_uid() -> str:
    # "STU" + 13 digits = 16 chars (fits max_length=16)
    ms = int(timezone.now().timestamp() * 1000)
    return "STU" + str(ms)[-13:]


def register(request):
    if request.method == "POST":
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            full_name = form.cleaned_data["full_name"].strip()
            email = form.cleaned_data["email"].strip().lower()
            mobile = form.cleaned_data["mobile"].strip()
            class_grade = form.cleaned_data["class_grade"]

            s = Student(
                student_uid=_make_student_uid(),
                full_name=full_name,
                class_grade=class_grade,
            )

            try:
                with transaction.atomic():
                    # Encrypt + hash before saving
                    s.set_email(email)
                    s.set_mobile(mobile)
                    s.save()
            except IntegrityError:
                # duplicate email_hash/mobile_hash OR any unique constraint
                messages.error(request, "This email or mobile is already registered.")
                return render(request, "students/register.html", {"form": form})
            except ValidationError as e:
                messages.error(request, f"Validation error: {e}")
                return render(request, "students/register.html", {"form": form})
            except Exception as e:
                messages.error(request, f"Could not register student: {e}")
                return render(request, "students/register.html", {"form": form})

            # Requirement #3: send confirmation email using decrypted email from DB
            try:
                to_email = s.email  # decrypted property
                subject = "Registration Successful"
                body = (
                    f"Hello {s.full_name},\n\n"
                    f"Your registration is successful.\n"
                    f"Registration ID: {s.student_uid}\n\n"
                    f"Thank you."
                )
                send_mail(
                    subject=subject,
                    message=body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[to_email],
                    fail_silently=bool(settings.DEBUG)
                )
            except Exception as e:
                # never block registration
                messages.warning(request, f"Student registered, but email could not be sent: {e}")

            messages.success(
                request,
                f"Student registered successfully: {s.full_name} (ID: {s.student_uid})"
            )
            return redirect("students:register")

    else:
        form = StudentRegistrationForm()

    return render(request, "students/register.html", {"form": form})


@login_required
def edit_student(request, student_id: int):
    if not _is_admin(request.user):
        messages.error(request, "Only admin users can edit students.")
        return redirect("accounts:admin_login")

    s = get_object_or_404(Student, id=student_id)

    if request.method == "POST":
        form = StudentEditForm(request.POST)
        if form.is_valid():
            old_full_name = s.full_name
            old_class_grade = s.class_grade
            old_email = s.email
            old_mobile = s.mobile

            new_full_name = form.cleaned_data["full_name"].strip()
            new_class_grade = form.cleaned_data["class_grade"]
            new_email = form.cleaned_data["email"].strip().lower()
            new_mobile = form.cleaned_data["mobile"].strip()

            s.full_name = new_full_name
            s.class_grade = new_class_grade

            if new_email != old_email:
                s.set_email(new_email)
            if new_mobile != old_mobile:
                s.set_mobile(new_mobile)

            try:
                with transaction.atomic():
                    s.save()
            except IntegrityError:
                messages.error(request, "This email or mobile is already used by another student.")
                return render(request, "students/edit_student.html", {"form": form, "student": s})
            except ValidationError as e:
                messages.error(request, f"Validation error: {e}")
                return render(request, "students/edit_student.html", {"form": form, "student": s})
            except Exception as e:
                messages.error(request, f"Could not update student: {e}")
                return render(request, "students/edit_student.html", {"form": form, "student": s})

            changed_by = _who(request)

            if old_full_name != new_full_name:
                StudentAuditLog.objects.create(
                    student=s, field_name="full_name",
                    old_value=old_full_name, new_value=new_full_name,
                    changed_by=changed_by
                )

            if old_class_grade != new_class_grade:
                StudentAuditLog.objects.create(
                    student=s, field_name="class_grade",
                    old_value=old_class_grade, new_value=new_class_grade,
                    changed_by=changed_by
                )

            if old_email != new_email:
                StudentAuditLog.objects.create(
                    student=s, field_name="email",
                    old_value="[ENCRYPTED]", new_value="[ENCRYPTED]",
                    changed_by=changed_by
                )

            if old_mobile != new_mobile:
                StudentAuditLog.objects.create(
                    student=s, field_name="mobile",
                    old_value="[ENCRYPTED]", new_value="[ENCRYPTED]",
                    changed_by=changed_by
                )

            messages.success(request, "Student updated successfully.")
            return redirect("dashboards:admin_dashboard")

    else:
        form = StudentEditForm(initial={
            "full_name": s.full_name,
            "class_grade": s.class_grade,
            "email": s.email,
            "mobile": s.mobile,
        })

    return render(request, "students/edit_student.html", {"form": form, "student": s})
