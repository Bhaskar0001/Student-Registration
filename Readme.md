# Student Registration System & Management Portal

## Project Evolution & Requirement Integration
This project has been enhanced with enterprise-grade features including biometric-safe encryption, automated parent-student mapping, and a premium administrative dashboard. 

## Changes & Implemented Requirements Summary
Below is a detailed breakdown of the recent system-wide updates and their technical impact.
- **Student Registration**: Encrypted sensitive fields (email, mobile stored as ciphertext + hash for uniqueness).
### 🛠️ Developer Tools
I have included several utility scripts to help with development:
-   `tools/setup_demo.py`: Creates admin and parent test users.
-   `tools/register_test.py`: Fast verification of the student registration flow.
-   `tools/login_check.py`: Checks parent login stability.
- **Automated Parent Linking**: Real-time creation of Parent accounts and relationship mapping during registration.
- **Security**: Fernet encryption for data-at-rest; SHA-256 hashing for data-in-transit uniqueness checks.
- **Parent Portal**: Personalized dashboard for viewing student status and engagement alerts.
- **Admin Portal**: Centralized management with export tools, audit logs, and encryption verification.

## Recent Changes & System Enhancements

| Feature Area | Implementation Detail | Impact & Value |
| :--- | :--- | :--- |
| **Parent Integration** | Added `parent_name` and `parent_email` to registration. Auto-creates `User` and `Parent` profiles. | Eliminates manual admin overhead for account creation and linking. |
| **Notification System** | Automated SMTP logic to send login credentials to parents and confirmation to students. | Immediate communication ensures parents can access the portal instantly. |
| **UI/UX Refactoring** | Migrated to a premium dark theme with optimized contrast (Inter font, modern CSS grid). | Professional appearance and improved accessibility across all devices. |
| **Dashboard Intelligence**| Unified Admin/Parent dashboard tables with improved status filtering and "Parent" visibility. | Faster data retrieval and better oversight of student engagement levels. |
| **Security Auditing** | Enhanced encryption proof page and masked audit logs for sensitive field changes. | Ensures GDPR/privacy compliance while maintaining an audit trail for changes. |

###  Technical Implementation Notes
- **Models**: Expanded `StudentParent` to support multiple students per parent.
- **Views**: Refactored `register` view with atomic transactions to ensure data integrity during multi-object creation.
- **Styling**: `modern.css` now centralizes all premium accents, isolating them from core layout logic for easier maintenance.




##  Tech Stack
- Django 6.x
- SQLite (dev)
- Django Templates
- Auth: Django User (Admin vs Parent login separated)

---

##  Setup (Windows)
```bash
# 1) Create venv
python -m venv venv

# 2) Activate venv
venv\Scripts\activate

# 3) Install deps
pip install -r requirements.txt

# 4) Migrate
python manage.py makemigrations
python manage.py migrate

# 5) Seed demo users + demo data
python manage.py seed_demo

# 6) Run server
python manage.py runserver

//urlslocal
Student register: http://127.0.0.1:8000/register/

Parent login: http://127.0.0.1:8000/accounts/parent/login/

Parent dashboard: http://127.0.0.1:8000/parent/dashboard/

Admin login: http://127.0.0.1:8000/accounts/admin/login/

Admin dashboard: http://127.0.0.1:8000/admin/dashboard/

Export CSV: http://127.0.0.1:8000/admin/export/engagement.csv

Audit logs: http://127.0.0.1:8000/admin/audit-logs/


 //DemoCredentials
Admin Credentials: 
admin
Admin@12345
Parent Credentials: 
parent1 
/ Parent@12345 (or generated during registration).

//test
python manage.py test

---

### 🛠️ Developer Tools
I have included several utility scripts to help with development:
-   `tools/setup_demo.py`: Creates admin and parent test users.
-   `tools/register_test.py`: Fast verification of the student registration flow.
-   `tools/login_check.py`: Checks parent login stability.

---

## 🧪 How to Test Parent Dashboard
To verify that students are correctly linked and visible to parents:

1. **Login**: Go to [http://127.0.0.1:8000/accounts/parent/login/](http://127.0.0.1:8000/accounts/parent/login/)
2. **Credentials**:
   - **Username**: Use the **Parent Email** you entered during registration (e.g., `parent@gmail.com`).
   - **Password**: 
     - For existing parents: Use your current password.
     - For new parents: Use the **Temporary Password** sent to your email (or printed in the terminal console).
3. **Verify**: Once logged in, the system automatically fetches all students linked to your email address.
4. **Real-time update**: If you register a new child using the same parent email, they will appear on your dashboard instantly.

> [!TIP]
> **If you see "No students linked yet":**
> 1. Make sure you are logged in with the **correct email** (the one you used during registration).
> 2. Log out and log back in to refresh your session.
> 3. Ensure the student was registered successfully at the `/register/` page.
