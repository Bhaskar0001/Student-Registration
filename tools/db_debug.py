import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "aah_guru.settings")
django.setup()

from django.contrib.auth import get_user_model
from parents.models import Parent, StudentParent

def debug_parent():
    User = get_user_model()
    try:
        u = User.objects.get(username='parent1')
        print(f"User: {u.username}, Email: {u.email}")
        p = Parent.objects.get(user=u)
        print(f"Parent Profile: {p.full_name}")
        links = StudentParent.objects.filter(parent=p)
        print(f"Link Count: {links.count()}")
        for l in links:
             print(f" - Student: {l.student.full_name}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug_parent()
