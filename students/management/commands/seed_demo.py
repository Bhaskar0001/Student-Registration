from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

from students.models import Student
from parents.models import Parent, StudentParent


class Command(BaseCommand):
    help = "Seeds demo users + students + links for quick testing."

    def handle(self, *args, **kwargs):
        # --- Admin user ---
        admin_user, _ = User.objects.get_or_create(username="admin")
        admin_user.set_password("Admin@12345")
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.email = "admin@aahguru.local"
        admin_user.save()

        # --- Parent user ---
        parent_user, _ = User.objects.get_or_create(username="parent1")
        parent_user.set_password("Parent@12345")
        parent_user.is_staff = False
        parent_user.is_superuser = False
        parent_user.email = "parent1@aahguru.local"
        parent_user.save()

        # --- Parent profile ---
        parent_profile, _ = Parent.objects.get_or_create(
            user=parent_user,
            defaults={"full_name": "Parent One"},
        )

        # --- Students ---
        s1, _ = Student.objects.get_or_create(
            student_uid="STU001",
            defaults={"full_name": "Aarav Sharma", "class_grade": "Class 5"},
        )
        s2, _ = Student.objects.get_or_create(
            student_uid="STU002",
            defaults={"full_name": "Diya Verma", "class_grade": "Class 7"},
        )

        # Last login: one active, one at-risk
        s1.last_login_at = timezone.now() - timedelta(days=2)   # ACTIVE
        s2.last_login_at = timezone.now() - timedelta(days=10)  # AT_RISK
        s1.save()
        s2.save()

        # --- Link parent to students ---
        StudentParent.objects.get_or_create(student=s1, parent=parent_profile, defaults={"relationship": "FATHER"})
        StudentParent.objects.get_or_create(student=s2, parent=parent_profile, defaults={"relationship": "MOTHER"})

        self.stdout.write(self.style.SUCCESS("✅ Seed complete"))
        self.stdout.write(self.style.SUCCESS("Admin: admin / Admin@12345"))
        self.stdout.write(self.style.SUCCESS("Parent: parent1 / Parent@12345"))
