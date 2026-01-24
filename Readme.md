
##  What this project does
- Student registration with encrypted sensitive fields (email, mobile stored as ciphertext + hash for uniqueness)
- Parent portal: view linked students + engagement status (ACTIVE / AT_RISK)
- Admin portal: engagement dashboard + mark active + export CSV
- Audit logs: track student field changes, sensitive values masked


- Student registration form
- Email + Mobile are encrypted before saving (Fernet)
- Hash stored for uniqueness/search (SHA-256 + pepper)
- Confirmation email sent using decrypted email + Registration ID (student_uid)
- Separate login for Parent and Admin
- Admin dashboard + audit logs + encryption proof page




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
Admin

Username: admin

Password: Admin@12345

Parent

Username: parent1

Password: Parent@12345

//test
python manage.py test
