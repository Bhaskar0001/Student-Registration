from django.test import TestCase
from students.crypto import encrypt_value, decrypt_value, hash_value


class CryptoTests(TestCase):
    def test_encrypt_decrypt_roundtrip(self):
        plain = "test@example.com"
        enc = encrypt_value(plain)
        self.assertNotEqual(enc, plain.encode())
        dec = decrypt_value(enc)
        self.assertEqual(dec, plain)

    def test_hash_is_stable_and_32_bytes(self):
        v = "9999999999"
        h1 = hash_value(v)
        h2 = hash_value(v)
        self.assertEqual(h1, h2)
        self.assertEqual(len(h1), 32)
