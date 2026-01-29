# 🎓 Student Registration System - Technical Documentation

This document provides a deep dive into the architecture, logic, and implementation details of the Student Registration System.

---

## 🏗️ Project Architecture

The project is built using **Django 4.2**, following a modular architecture:

-   **`students`**: Core app handling student data, encryption, registration, and auditing.
-   **`parents`**: Manages parent profiles and the relationship mapping to students.
-   **`accounts`**: Custom authentication logic (Username/Email login).
-   **`dashboards`**: Business logic for Admin and Parent views.
-   **`audit`**: Tracking of changes to student records.

---

## 🚀 Deployment Guide (Update your Repo)

To update your repository [Bhaskar0001/Student-Registration](https://github.com/Bhaskar0001/Student-Registration.git):

1. **Stage all changes**:
   ```bash
   git add .
   ```
2. **Commit**:
   ```bash
   git commit -m "Complete project with full documentation"
   ```
3. **Push to GitHub**:
   ```bash
   git push -u origin main
   ```

---

## ⚠️ Important: Render Deployment Checklist (Fixing 500 Errors)

If you see an **Internal Server Error** on Render, it is usually because of missing **Environment Variables**. Please ensure these are added in your Render Dashboard (Environment tab):

| Variable | Recommended Value |
| :--- | :--- |
| `DJANGO_SECRET_KEY` | (Any long random string) |
| `DJANGO_DEBUG` | `False` |
| `FIELD_ENCRYPTION_KEY` | (Run `python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"` locally) |
| `HASH_PEPPER` | (Any random string) |
| `SMTP_HOST` | `smtp.gmail.com` |
| `SMTP_PORT` | `587` |
| `SMTP_USER` | `bhaskarjoshi900@gmail.com` |
| `SMTP_PASSWORD` | (Your Gmail App Password) |
| `DEFAULT_FROM_EMAIL` | `bhaskarjoshi900@gmail.com` |

---

## 🎤 Interview Preparation (25 Q&A)

### Technical & Architecture
1.  **Q: How do you handle unique email constraints if the data is encrypted?**
    *   **A**: We use a "Hashed Lookup" strategy. We store a non-reversible `SHA-256` hash of the email in a separate indexable column (`email_hash`). This allows us to check for duplicates without ever needing to decrypt the actual data during the uniqueness check.
2.  **Q: Why standard Fernet encryption instead of a simple library?**
    *   **A**: Fernet provides "authenticated encryption". This means it not only encrypts the data but also ensures it hasn't been tampered with.
3.  **Q: Explain the `StudentParent` model. Why not just a Foreign Key on the Student?**
    *   **A**: We used a Many-to-Many relationship. This allows siblings to have multiple registered parents or a single parent to manage multiple students in the same portal.
4.  **Q: What happens if the `send_mail` function fails during registration?**
    *   **A**: The registration is inside `transaction.atomic()`, but email is outside to prevent network glitches from rolling back a successful database registration.
5.  **Q: Why use `whitenoise` for static files?**
    *   **A**: It allows Django to serve its own static files efficiently on platforms like Render without Needing Nginx.
6.  **Q: How do you protect the encryption keys?**
    *   **A**: We use environment variables. The `FIELD_ENCRYPTION_KEY` is never hardcoded.
7.  **Q: Explain the custom `EmailBackend`.**
    *   **A**: We overridden `authenticate` to check both `username` and `email` fields.
8.  **Q: How would this system scale to 100,000 students?**
    *   **A**: Use a Task Queue (Celery) for emails and an optimized search index for hashed fields.
9.  **Q: What is the most critical security feature of this app?**
    *   **A**: **Audit Logging**. Every sensitive change is logged with the modifier's ID and timestamp.
10. **Q: How do you ensure the Parent Portal stays separate from the Admin Portal?**
    *   **A**: We check `user.is_staff` in the `dispatch` method of the dashboard views.
11. **Q: Why generate temporary passwords?**
    *   **A**: Prevents "User Enumeration" and ensures the email is valid before setting permanent credentials.
12. **Q: How would you add "Attendance Tracking"?**
    *   **A**: Create an `Attendance` model linked to `Student` and show summaries on the dashboard.
13. **Q: Biggest challenge in auto-mapping?**
    *   **A**: Handling existing parents vs new parents gracefully without creating duplicate `User` accounts.
14. **Q: Why use a "Pepper" in hashing?**
    *   **A**: Prevents "Rainbow Table" attacks by adding a secret salt to every hash.
15. **Q: How does the system handle "At-Risk" status?**
    *   **A**: Dynamically calculates days since `last_login_at`. If > 7 days, it's "AT_RISK".
16. **Q: SQL Injection protection?**
    *   **A**: Django ORM uses parameterized queries automatically.
17. **Q: SQLite vs PostgreSQL?**
    *   **A**: SQLite for easy development; Postgres for production concurrency and data integrity.
18. **Q: Whitenoise middleware placement?**
    *   **A**: Must be right after `SecurityMiddleware` to serve files before other processing.
19. **Q: Non-blocking login notifications?**
    *   **A**: Email is wrapped in `try-except` so a failure doesn't stop the login response.
20. **Q: Benefit of `secrets.token_urlsafe`?**
    *   **A**: Cryptographically strong randomness, better than the `random` module.
21. **Q: Password Reset flow?**
    *   **A**: Leverages Django's built-in `PasswordResetView` for a secure token-based flow.
22. **Q: `select_related` optimization?**
    *   **A**: Performs a SQL JOIN to avoid N+1 query problems when listing students on the dashboard.
23. **Q: Handling file uploads?**
    *   **A**: Use `FileField` and a cloud storage backend like S3 for production.
24. **Q: Criticality of `.env`?**
    *   **A**: Separates secrets from code; `.gitignore` prevents leaks.
25. **Q: Next feature to add?**
    *   **A**: Multi-Factor Authentication (MFA) for the Admin Portal.
