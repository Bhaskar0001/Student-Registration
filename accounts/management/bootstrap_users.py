import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = "Create/update default admin + demo parent from env vars"

    def handle(self, *args, **options):
        User = get_user_model()

        admin_user = os.getenv("BOOTSTRAP_ADMIN_USERNAME", "admin")
        admin_email = os.getenv("BOOTSTRAP_ADMIN_EMAIL", "admin@example.com")
        admin_pass = os.getenv("BOOTSTRAP_ADMIN_PASSWORD", "Admin@12345")

        u, created = User.objects.get_or_create(username=admin_user, defaults={"email": admin_email})
        u.email = admin_email
        u.is_staff = True
        u.is_superuser = True
        u.set_password(admin_pass)
        u.save()
        self.stdout.write(self.style.SUCCESS(f"Admin ready: {admin_user} / {admin_email}"))

        parent_user = os.getenv("BOOTSTRAP_PARENT_USERNAME", "parent1")
        parent_email = os.getenv("BOOTSTRAP_PARENT_EMAIL", "parent1@example.com")
        parent_pass = os.getenv("BOOTSTRAP_PARENT_PASSWORD", "Parent@12345")

        p, created = User.objects.get_or_create(username=parent_user, defaults={"email": parent_email})
        p.email = parent_email
        p.is_staff = False
        p.is_superuser = False
        p.set_password(parent_pass)
        p.save()
        self.stdout.write(self.style.SUCCESS(f"Parent ready: {parent_user} / {parent_email}"))
