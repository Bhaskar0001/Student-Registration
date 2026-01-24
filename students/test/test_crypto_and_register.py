from django.test import TestCase, override_settings
from django.urls import reverse
from django.core import mail

from students.crypto import encrypt_value, decrypt_value, hash_value
from students.models import Student


class CryptoTests(TestCase):
    def test_encrypt_decrypt_roundtrip(self):
        plain = "parent@example.com"
        enc = encrypt_value(plain)
        self.assertIsInstance(enc, (bytes, bytearray))
        self.assertNotEqual(enc, plain.encode("utf-8"))
        dec = decrypt_value(enc)
        self.assertEqual(dec, plain)

    def test_hash_is_32_bytes(self):
        h = hash_value("parent@example.com")
        self.assertEqual(len(h), 32)


@override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
class RegistrationFlowTests(TestCase):
    def setUp(self):
        self.url = reverse("students:register")

    def test_register_stores_encrypted_and_sends_email(self):
        payload = {
            "full_name": "Test Student",
            "email": "parent@example.com",
            "mobile": "9999999999",
            "class_grade": "10",
        }

        resp = self.client.post(self.url, data=payload, follow=False)
        # you usually redirect back to register page on success
        self.assertIn(resp.status_code, (302, 303))

        s = Student.objects.get(email_hash=hash_value(payload["email"].lower().strip()))

        # encrypted blobs exist
        self.assertTrue(s.email_enc)
        self.assertTrue(s.mobile_enc)

        # ensure NOT stored as plain
        self.assertNotIn(payload["email"].encode("utf-8"), s.email_enc)
        self.assertNotIn(payload["mobile"].encode("utf-8"), s.mobile_enc)

        # decrypted equals original
        self.assertEqual(s.email, payload["email"].lower().strip())
        self.assertEqual(s.mobile, payload["mobile"].strip())

        # hashes should be 32 bytes
        self.assertEqual(len(s.email_hash), 32)
        self.assertEqual(len(s.mobile_hash), 32)

        # email sent
        self.assertEqual(len(mail.outbox), 1)
        msg = mail.outbox[0]
        self.assertIn(payload["email"].lower().strip(), msg.to)

        # body contains registration id (student_uid)
        body = (msg.body or "") + " " + (msg.subject or "")
        self.assertIn(s.student_uid, body)

    def test_duplicate_email_or_mobile_blocked(self):
        payload = {
            "full_name": "Student 1",
            "email": "dup@example.com",
            "mobile": "9999999999",
            "class_grade": "9",
        }

        self.client.post(self.url, data=payload)
        self.assertEqual(Student.objects.count(), 1)

        payload2 = {
            "full_name": "Student 2",
            "email": "dup@example.com",   # same email
            "mobile": "8888888888",
            "class_grade": "9",
        }
        resp = self.client.post(self.url, data=payload2)

        # should not create second record
        self.assertEqual(Student.objects.count(), 1)
        # should show error message on page (status 200) OR redirect with message
        self.assertIn(resp.status_code, (200, 302, 303))
