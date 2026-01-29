import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "aah_guru.settings")
django.setup()

from django.contrib.auth import get_user_model
from parents.models import Parent, StudentParent
from students.models import Student
from django.utils import timezone

User = get_user_model()

def create_users():
    print("--- Creating Production-Ready Test Data ---")
    
    # 1. Admin
    admin_email = "admin@aahguru.local"
    if not User.objects.filter(username="admin").exists():
        User.objects.create_superuser("admin", admin_email, "Admin@12345")
        print(f"SUCCESS: Created Admin (User: admin, Pass: Admin@12345)")
    else:
        print("INFO: Admin already exists.")

    # 2. Parent Tester
    parent_email = "parent_tester@aahguru.local"
    parent_user = User.objects.filter(email=parent_email).first()
    if not parent_user:
        parent_user = User.objects.create_user("parent_tester", parent_email, "Parent@12345")
        print(f"SUCCESS: Created Parent (Email: {parent_email}, Pass: Parent@12345)")
    
    parent_profile, created = Parent.objects.get_or_create(
        user=parent_user,
        defaults={"full_name": "Demo Parent User"}
    )

    # 3. Create 3 Linked Students
    students_data = [
        {"name": "Aarav Sharma", "grade": "10"},
        {"name": "Isha Patel", "grade": "12"},
        {"name": "Ryan Dsouza", "grade": "8"},
    ]

    for i, data in enumerate(students_data):
        email = f"student{i+1}@aahguru.local"
        mobile = f"987654321{i}"
        
        # Check if student exists by hash
        temp_s = Student()
        temp_s.set_email(email)
        
        if not Student.objects.filter(email_hash=temp_s.email_hash).exists():
            s = Student(
                student_uid=f"STU_DEMO_00{i+1}",
                full_name=data["name"],
                class_grade=data["grade"],
                last_login_at=timezone.now() - timezone.timedelta(days=i*2)
            )
            s.set_email(email)
            s.set_mobile(mobile)
            s.save()
            
            # Link to parent
            StudentParent.objects.get_or_create(
                student=s,
                parent=parent_profile,
                defaults={"relationship": "PARENT"}
            )
            print(f"SUCCESS: Created Student {s.full_name} and linked to parent.")
        else:
            print(f"INFO: Student {data['name']} already exists.")

if __name__ == "__main__":
    create_users()
