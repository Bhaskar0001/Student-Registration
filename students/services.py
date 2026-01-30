from django.db import transaction
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings

from audit.models import StudentAuditLog
from audit.utils import mask_if_sensitive

from .models import Student
from .crypto import encrypt_value, hash_value


def _generate_student_uid() -> str:
    """
    STU + YYYYMMDD + last 4 digits of timestamp
    Example: STU202601220123
    """
    now = timezone.now()
    suffix = str(int(now.timestamp()))[-4:]
    return f"STU{now.strftime('%Y%m%d')}{suffix}"


@transaction.atomic
def register_student(full_name: str, email: str, mobile: str, class_grade: str) -> Student:
    email_hash = hash_value(email.lower())
    mobile_hash = hash_value(mobile)

    # Unique checks (hash-based)
    if Student.objects.filter(email_hash=email_hash).exists():
        raise ValueError("This email is already registered.")
    if Student.objects.filter(mobile_hash=mobile_hash).exists():
        raise ValueError("This mobile is already registered.")

    student_uid = _generate_student_uid()

    student = Student.objects.create(
        student_uid=student_uid,
        full_name=full_name.strip(),
        class_grade=class_grade,
        email_enc=encrypt_value(email.lower()),
        mobile_enc=encrypt_value(mobile),
        email_hash=email_hash,
        mobile_hash=mobile_hash,
    )

    return student


@transaction.atomic
def update_student(student: Student, data: dict, changed_by: str):
    """
    Updates student fields safely and writes audit logs with changed_by.
    """
    old = Student.objects.get(pk=student.pk)

    # Apply changes
    student.full_name = data["full_name"]
    student.class_grade = data["class_grade"]

    # encrypted fields
    student.email_enc = encrypt_value(data["email"])
    student.mobile_enc = encrypt_value(data["mobile"])

    # hashes for uniqueness/search
    student.email_hash = hash_value(data["email"])
    student.mobile_hash = hash_value(data["mobile"])

    student.updated_at = timezone.now()
    student.save()

    # Audit differences (mask encrypted)
    tracked = ["full_name", "class_grade", "email_enc", "mobile_enc"]
    for f in tracked:
        old_val = getattr(old, f)
        new_val = getattr(student, f)
        if old_val != new_val:
            StudentAuditLog.objects.create(
                student=student,
                field_name=f,
                old_value=mask_if_sensitive(f, old_val),
                new_value=mask_if_sensitive(f, new_val),
                changed_by=changed_by or "admin",
            )


    return student
