from django.contrib import admin
from .models import Parent, StudentParent


@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "user", "created_at")
    search_fields = ("full_name", "user__username", "user__email")
    list_select_related = ("user",)


@admin.register(StudentParent)
class StudentParentAdmin(admin.ModelAdmin):
    list_display = ("id", "parent", "student", "relationship", "created_at")
    search_fields = ("parent__full_name", "student__full_name", "student__student_uid")
    list_filter = ("relationship",)
    # ✅ keep it simple for now:
    # autocomplete_fields = ("parent", "student")
