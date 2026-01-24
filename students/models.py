from django.db import models
from django.core.exceptions import ValidationError

from .crypto import encrypt_value, decrypt_value, hash_value


class Student(models.Model):
    student_uid = models.CharField(max_length=16, unique=True)
    full_name = models.CharField(max_length=120)
    class_grade = models.CharField(max_length=20)

    # encrypted (ciphertext)
    email_enc = models.BinaryField()
    mobile_enc = models.BinaryField()

    # hashes for uniqueness/search
    email_hash = models.CharField(max_length=64, unique=True, db_index=True)
    mobile_hash = models.CharField(max_length=64, unique=True, db_index=True)

    last_login_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # -----------------------
    # Convenience properties (not DB fields)
    # -----------------------
    @property
    def email(self) -> str:
        return decrypt_value(self.email_enc)

    @property
    def mobile(self) -> str:
        return decrypt_value(self.mobile_enc)

    # -----------------------
    # Helper setters
    # -----------------------
    def set_email(self, email: str):
        if not email:
            raise ValidationError("Email is required.")
        self.email_enc = encrypt_value(email)
        self.email_hash = hash_value(email)

    def set_mobile(self, mobile: str):
        if not mobile:
            raise ValidationError("Mobile is required.")
        self.mobile_enc = encrypt_value(mobile)
        self.mobile_hash = hash_value(mobile)

    # -----------------------
    # Auto-validate before save
    # -----------------------
    def clean(self):
        if not self.email_enc or not self.email_hash:
            raise ValidationError("Email must be set using set_email(email).")
        if not self.mobile_enc or not self.mobile_hash:
            raise ValidationError("Mobile must be set using set_mobile(mobile).")




    def inactivity_days(self) -> int:
        if not self.last_login_at:
            return 9999
        return (timezone.now() - self.last_login_at).days

    def __str__(self):
        return f"{self.full_name} ({self.student_uid})"
