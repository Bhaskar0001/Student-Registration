from django.contrib import admin
from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    search_fields = ("student_uid", "full_name")
    list_display = ("student_uid", "full_name", "class_grade", "last_login_at", "created_at")
    list_filter = ("class_grade",)
    readonly_fields = ("student_uid", "created_at", "updated_at")
