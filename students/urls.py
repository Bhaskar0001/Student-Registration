from django.urls import path
from . import views

app_name = "students"

urlpatterns = [
    path("register/", views.register, name="register"),
     path("admin/students/<int:student_id>/edit/", views.edit_student, name="edit_student"),
]
