from django.test import TestCase, override_settings
from django.urls import reverse
from django.core import mail
from cryptography.fernet import Fernet

from students.models import Student


class StudentRegistrationTests(TestCase):
    @override_settings(
        EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
        DEFAULT_FROM_EMAIL="no-reply@test.local",
        FIELD_ENCRYPTION_KEY=Fernet.generate_key().decode(),
        HASH_PEPPER="test-pepper-123",
    )
    def test_register_encrypts_and_sends_email_with_registration_id(self):
        url = reverse("students:register")

        payload = {
            "full_name": "Test Student",
            "email": "student@example.com",
            "mobile": "9999999999",
            "class_grade": "10",
        }

        resp = self.client.post(url, payload, follow=True)
        self.assertEqual(resp.status_code, 200)

        # Student created
        self.assertEqual(Student.objects.count(), 1)
        s = Student.objects.first()

        # Encrypted fields should not contain plaintext
        self.assertNotIn(b"student@example.com", s.email_enc)
        self.assertNotIn(b"9999999999", s.mobile_enc)

        # Decrypted properties should return original values
        self.assertEqual(s.email, "student@example.com")
        self.assertEqual(s.mobile, "9999999999")

        # Email sent to decrypted email and contains registration ID
        self.assertEqual(len(mail.outbox), 1)
        sent = mail.outbox[0]
        self.assertIn("student@example.com", sent.to)
        self.assertIn(s.student_uid, sent.body)
