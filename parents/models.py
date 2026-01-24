from django.db import models
from django.contrib.auth.models import User
from students.models import Student


class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=120)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name


class StudentParent(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE)
    relationship = models.CharField(max_length=30, default="PARENT")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("student", "parent")

    def __str__(self):
        return f"{self.parent} -> {self.student}"
