from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.db import connection
from django.db.utils import OperationalError, ProgrammingError

from students.models import Student
from .models import StudentAuditLog
from .utils import mask_if_sensitive

_old_student_cache = {}


def _audit_table_ready() -> bool:
    try:
        return StudentAuditLog._meta.db_table in connection.introspection.table_names()
    except (OperationalError, ProgrammingError):
        return False


@receiver(pre_save, sender=Student)
def cache_old_student(sender, instance: Student, **kwargs):
    if not instance.pk:
        return
    try:
        _old_student_cache[instance.pk] = Student.objects.get(pk=instance.pk)
    except Student.DoesNotExist:
        pass


@receiver(post_save, sender=Student)
def create_student_audit_logs(sender, instance: Student, created: bool, **kwargs):
    if not _audit_table_ready():
        return

    if created:
        StudentAuditLog.objects.create(
            student=instance,
            field_name="SYSTEM_CREATE",
            old_value="",
            new_value="Student created",
            changed_by="system",
        )
        return

    old = _old_student_cache.pop(instance.pk, None)
    if not old:
        return

    tracked_fields = ["full_name", "class_grade", "email_enc", "mobile_enc", "last_login_at"]

    for f in tracked_fields:
        old_val = getattr(old, f)
        new_val = getattr(instance, f)
        if old_val != new_val:
            StudentAuditLog.objects.create(
                student=instance,
                field_name=f,
                old_value=mask_if_sensitive(f, old_val),
                new_value=mask_if_sensitive(f, new_val),
                changed_by="admin_or_system",
            )
