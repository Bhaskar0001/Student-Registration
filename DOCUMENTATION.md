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

> **Parent Password Tip**: When you register a new student, the system automatically creates a parent account and generates a temporary password. For your convenience during testing, this password is now displayed in the **Success Message** at the top of the registration page after you click submit. It is also sent via email.

---

## 🛠️ Troubleshooting Live Site Errors (Diagnostic Tool)

If you see an **Internal Server Error** on Render, visit this URL on your site:
`https://your-site-name.onrender.com/accounts/status-check/`

This page will safely check:
- If your **Database** is connected.
- If your **Encryption Keys** are correctly set in Render.
- If your **SMTP Email** settings are present.

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
