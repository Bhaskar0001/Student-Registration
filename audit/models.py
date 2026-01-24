from django.db import models
from students.models import Student


class StudentAuditLog(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    field_name = models.CharField(max_length=64)
    old_value = models.TextField(null=True, blank=True)
    new_value = models.TextField(null=True, blank=True)
    changed_by = models.CharField(max_length=128)  # admin email or "system"
    changed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-changed_at"]

    def __str__(self):
        return f"{self.student.student_uid} {self.field_name} @ {self.changed_at}"
