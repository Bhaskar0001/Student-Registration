from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.db import IntegrityError, transaction
import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.http import HttpResponse
from .mailer import send_student_email

logger = logging.getLogger(__name__)
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
    ms = int(timezone.now().timestamp() * 1000)
    return "STU" + str(ms)[-13:]


@login_required
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
                    s.set_email(email)
                    s.set_mobile(mobile)
                    s.save()
                    
                    # Auto-create Parent User and link to Student
                    parent_name = form.cleaned_data.get("parent_name", "").strip()
                    parent_email_input = form.cleaned_data.get("parent_email", "").strip().lower()
                    
                    if parent_name and parent_email_input:
                        from django.contrib.auth import get_user_model
                        from parents.models import Parent, StudentParent
                        import secrets
                        
                        User = get_user_model()
                        
                        # Check if parent user already exists
                        parent_user = User.objects.filter(email=parent_email_input).first()
                        
                        if not parent_user:
                            # Create a new user for parent with random password
                            # Parent can reset password later
                            temp_password = secrets.token_urlsafe(12)
                            username = parent_email_input.split("@")[0] + "_" + str(s.id)
                            parent_user = User.objects.create_user(
                                username=username,
                                email=parent_email_input,
                                password=temp_password
                            )
                            # Create Parent profile
                            parent_profile = Parent.objects.create(
                                user=parent_user,
                                full_name=parent_name
                            )
                            password_info = f"\n\nYour temporary login password is: {temp_password}\nPlease change it after first login."
                        else:
                            # Parent user exists, get or create profile
                            parent_profile, _ = Parent.objects.get_or_create(
                                user=parent_user,
                                defaults={"full_name": parent_name}
                            )
                            password_info = ""
                        
                        StudentParent.objects.get_or_create(
                            student=s,
                            parent=parent_profile,
                            defaults={"relationship": "PARENT"}
                        )
                    else:
                        parent_email_input = None
                        password_info = ""
                        
            except IntegrityError:
                messages.error(request, "This email or mobile is already registered.")
                return render(request, "students/register.html", {"form": form})
            except ValidationError as e:
                messages.error(request, f"Validation error: {e}")
                return render(request, "students/register.html", {"form": form})
            except Exception as e:
                logger.exception(f"Unexpected error during registration: {e}")
                messages.error(request, f"Could not register student: {e}")
                return render(request, "students/register.html", {"form": form})

            # Send confirmation emails
            # 1. Student Email
            student_subject = "Registration Successful"
            student_body = (
                f"Hello {s.full_name},\n\n"
                f"Your registration is successful.\n"
                f"Registration ID: {s.student_uid}\n\n"
                f"Thank you.\nSchool Administration"
            )
            student_email_sent = send_student_email(s.email, student_subject, student_body)
            if not student_email_sent:
                messages.warning(request, "Student registered, but student confirmation email failed.")

            # 2. Parent Email (with login info if new)
            if parent_email_input:
                parent_subject = "Student Registration Confirmation"
                parent_body = (
                    f"Hello {parent_name},\n\n"
                    f"Your child {s.full_name} has been registered successfully.\n"
                    f"Registration ID: {s.student_uid}\n\n"
                    f"You can now login to the Parent Portal using your email: {parent_email_input}"
                    f" {password_info}\n\n"
                    f"Thank you.\nSchool Administration"
                )
                parent_email_sent = send_student_email(parent_email_input, parent_subject, parent_body)
                if not parent_email_sent:
                    messages.warning(request, "Student registered, but parent confirmation email failed.")

            success_msg = f"Successfully registered {s.full_name} (ID: {s.student_uid})."
            if password_info:
                # Include the password in the message so the user can see it during testing
                success_msg += f" A new parent portal account has been created for {parent_email_input}."
                # Safe to show here as it's a one-time message for the registrant
                success_msg += f" LOGIN PASSWORD: {temp_password}"

            messages.success(request, success_msg)
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
                logger.exception(f"Unexpected error during student update for student ID {s.id}: {e}")
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
