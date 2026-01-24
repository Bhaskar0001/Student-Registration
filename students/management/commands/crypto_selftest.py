from django.core.management.base import BaseCommand
from django.utils import timezone

from students.crypto import encrypt_value, decrypt_value, hash_value
from students.models import Student


class Command(BaseCommand):
    help = "Quick self-test for encryption/decryption + hashing (includes DB round-trip test)"

    def handle(self, *args, **options):
        sample_email = "parent@example.com"
        sample_mobile = "9999999999"

        # ----------------------------
        # 1) Pure crypto test (no DB)
        # ----------------------------
        enc_email = encrypt_value(sample_email)
        enc_mobile = encrypt_value(sample_mobile)

        dec_email = decrypt_value(enc_email)
        dec_mobile = decrypt_value(enc_mobile)

        email_hash = hash_value(sample_email)
        mobile_hash = hash_value(sample_mobile)

        self.stdout.write(self.style.SUCCESS("✅ Pure Encryption/Decryption Test"))
        self.stdout.write(f"Email plain: {sample_email}")
        self.stdout.write(f"Email enc  : {enc_email[:30]}... (bytes)")
        self.stdout.write(f"Email dec  : {dec_email}")
        self.stdout.write("")
        self.stdout.write(f"Mobile plain: {sample_mobile}")
        self.stdout.write(f"Mobile enc  : {enc_mobile[:30]}... (bytes)")
        self.stdout.write(f"Mobile dec  : {dec_mobile}")
        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS("✅ Hash Test (length should be 32 bytes)"))
        self.stdout.write(f"Email hash bytes  : {len(email_hash)}")
        self.stdout.write(f"Mobile hash bytes : {len(mobile_hash)}")

        assert dec_email == sample_email, "Email decrypt mismatch!"
        assert dec_mobile == sample_mobile, "Mobile decrypt mismatch!"
        assert len(email_hash) == 32 and len(mobile_hash) == 32, "Hash length mismatch!"

        # ----------------------------
        # 2) DB round-trip test
        # ----------------------------
        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS("✅ DB Round-trip Test (Student model)"))

        # ✅ 16-char UID only
        # Format: STU + 13-digit millis = 16 chars
        uid = f"STU{int(timezone.now().timestamp() * 1000):013d}"  # e.g. STU1700000000000

        # unique email/mobile so reruns won't clash
        email2 = f"t{uid.lower()}@e.com"  # short but unique
        mobile2 = f"9{str(int(timezone.now().timestamp()))[-9:]}"  # 10 digits

        s = Student(student_uid=uid, full_name="Crypto Test Student", class_grade="10")
        s.set_email(email2)
        s.set_mobile(mobile2)
        s.save()

        s2 = Student.objects.get(id=s.id)

        # Check decrypt matches
        assert s2.email == email2, "DB email decrypt mismatch!"
        assert s2.mobile == mobile2, "DB mobile decrypt mismatch!"

        # Check hashes match
        assert s2.email_hash == hash_value(email2), "DB email hash mismatch!"
        assert s2.mobile_hash == hash_value(mobile2), "DB mobile hash mismatch!"

        # Check ciphertext doesn't contain plaintext
        assert email2.encode("utf-8") not in s2.email_enc, "Email stored as plaintext!"
        assert mobile2.encode("utf-8") not in s2.mobile_enc, "Mobile stored as plaintext!"

        self.stdout.write(self.style.SUCCESS("🎉 All crypto self-tests passed (including DB)."))
        self.stdout.write(f"Created Student UID: {uid} (id={s.id})")
