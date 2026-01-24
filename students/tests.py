from django.test import TestCase
from django.utils import timezone

from students.models import Student
from students.crypto import encrypt_value, decrypt_value, hash_value


class StudentCryptoTests(TestCase):
    def test_encrypt_decrypt_roundtrip(self):
        raw = "test@example.com"
        enc = encrypt_value(raw)
        dec = decrypt_value(enc)
        self.assertEqual(dec, raw)

    def test_hash_consistency(self):
        self.assertEqual(hash_value("9999999999"), hash_value("9999999999"))


class EngagementLogicTests(TestCase):
    def test_inactivity_days(self):
        s = Student.objects.create(
            student_uid="STU202601220001",
            full_name="Rahul",
            class_grade="10",
            email_enc=encrypt_value("rahul@example.com"),
            mobile_enc=encrypt_value("9999999999"),
            email_hash=hash_value("rahul@example.com"),
            mobile_hash=hash_value("9999999999"),
            last_login_at=timezone.now(),
        )
        self.assertEqual(s.inactivity_days(), 0)
