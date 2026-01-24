from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone

from parents.models import Parent, StudentParent
from students.models import Student


class Command(BaseCommand):
    help = "Seed demo admin + parent + student linking for AAH_GURU_ASSIGNMENT"

    def handle(self, *args, **options):
        # Admin
        admin_user, created = User.objects.get_or_create(username="admin")
        if created:
            admin_user.set_password("Admin@12345")
            admin_user.is_staff = True
            admin_user.is_superuser = True
            admin_user.email = "admin@aahguru.local"
            admin_user.save()
            self.stdout.write(self.style.SUCCESS("Created admin user: admin / Admin@12345"))
        else:
            self.stdout.write("Admin user already exists.")

        # Parent auth user
        parent_user, created = User.objects.get_or_create(username="parent1")
        if created:
            parent_user.set_password("Parent@12345")
            parent_user.is_staff = False
            parent_user.is_superuser = False
            parent_user.email = "parent1@aahguru.local"
            parent_user.save()
            self.stdout.write(self.style.SUCCESS("Created parent user: parent1 / Parent@12345"))
        else:
            # ensure not staff
            parent_user.is_staff = False
            parent_user.is_superuser = False
            parent_user.save()
            self.stdout.write("Parent user already exists (ensured non-staff).")

        # Parent profile
        parent_profile, _ = Parent.objects.get_or_create(
            user=parent_user,
            defaults={"full_name": "Mrs Sharma"}
        )

        # Find or create a student
        student = Student.objects.order_by("-created_at").first()
        if not student:
            # create minimal student (you may need to adapt if your Student model requires encryption fields)
            # If your Student model has required encrypted fields, skip creation and register one from UI first.
            self.stdout.write(self.style.WARNING(
                "No Student found. Please register one student from /register/ first, then rerun seed_demo."
            ))
            return

        # Link
        StudentParent.objects.get_or_create(student=student, parent=parent_profile)

        self.stdout.write(self.style.SUCCESS("Linked parent1 -> latest student successfully."))
        self.stdout.write(self.style.SUCCESS("DONE. Now login with parent1 / Parent@12345"))
