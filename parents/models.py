from django.db import models
from django.conf import settings


class Parent(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="parent_profile")
    full_name = models.CharField(max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)

    # convenient: parent.students.all()
    students = models.ManyToManyField("students.Student", through="StudentParent", related_name="parents")

    def __str__(self):
        return self.full_name


class StudentParent(models.Model):
    student = models.ForeignKey("students.Student", on_delete=models.CASCADE, related_name="parent_links")
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE, related_name="student_links")
    relationship = models.CharField(max_length=30, default="PARENT")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["student", "parent"], name="uniq_student_parent")
        ]

    def __str__(self):
        return f"{self.parent} -> {self.student}"
