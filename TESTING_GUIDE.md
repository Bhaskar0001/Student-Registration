# Testing Guide: Student Registration System

Follow these steps to test the registration flow and verify the parent-student mapping.

## 1. Credentials for Manual Testing

### Admin Dashboard
- **URL**: [http://127.0.0.1:8000/accounts/admin/login/](http://127.0.0.1:8000/accounts/admin/login/)
- **Username**: `admin`
- **Password**: `Admin@12345`

### Parent Portal (Test Data)
- **Email**: `parent_tester@aahguru.local`
- **Password**: `Parent@12345`
*(Note: These only work if you have run the seed script `python tools/setup_demo.py` on your server).*

### Admin Dashboard (Test Data)
- **Username**: `admin`
- **Password**: `Admin@12345`

---

## 2. Test Step-by-Step

### Step A: Register a New Student
1. Open [http://127.0.0.1:8000/register/](http://127.0.0.1:8000/register/).
2. Fill in the student details (Name, Email, Mobile).
3. Fill in the **Parent Name** and **Parent Email**.
   > [!NOTE]
   > Use a unique email if you want to see a new parent account being created.
4. Click **Register**.

### Step B: Verify Email (Console)
1. Check your terminal/server logs.
2. You should see two emails printed:
   - One for the **Student** (Confirmation).
   - One for the **Parent** (with login credentials if it's a new parent).

### Step C: Login as Parent
1. Go to [http://127.0.0.1:8000/accounts/parent/login/](http://127.0.0.1:8000/accounts/parent/login/).
2. Use the **Parent Email** and the **Temporary Password** found in the terminal/console log.
3. Once logged in, you should see the **Parent Dashboard**.

### Step D: Verify Automatic Mapping
1. On the Parent Dashboard, verify that the student you just registered is listed.
2. **Multiple Students**: Try registering another student using the *same parent email*.
3. Login as that parent again; both students should now appear automatically.

---

## 4. Testing on Render (Live Site)
If testing on your live Render URL:
1. **Logs**: If you get a 500 error, check your **Render Dashboard -> Logs**. You will see a detailed Python error message.
2. **Setup**: Ensure you have added all **Environment Variables** (SMTP, Secret Key, Encryption Keys) in the Render Settings.
3. **Database**: If it's your first push, Render will run migrations automatically if you use the `build.sh` or the build command provided in `DOCUMENTATION.md`.

---

## 3. How "Automatic Mapping" Works
The system uses the `Parent Email` field during registration to link a student:
1. It checks if a `User` with that email already exists.
2. If not, it creates a new `User` and a `Parent` profile.
3. It then creates a `StudentParent` link between the new `Student` and the `Parent`.
4. This ensures that whenever that parent logs in, they see all students linked to their email.
