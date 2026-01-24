from django.contrib.auth.models import Group


def is_parent(user):
    if not user.is_authenticated:
        return False
    return user.groups.filter(name="parents").exists()
