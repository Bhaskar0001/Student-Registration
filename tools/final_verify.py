import requests
import random
from bs4 import BeautifulSoup

BASE_URL = "http://127.0.0.1:8007"
s = requests.Session()

def test_parent_dashboard():
    print("--- Testing Parent Dashboard & Mapping ---")
    
    # 1. Login
    login_url = f"{BASE_URL}/accounts/parent/login/"
    r = s.get(login_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    csrf = soup.find('input', {'name': 'csrfmiddlewaretoken'})['value']
    
    data = {
        "csrfmiddlewaretoken": csrf,
        "username": "parent_tester@aahguru.local",
        "password": "Parent@12345"
    }
    
    r = s.post(login_url, data=data, headers={"Referer": login_url})
    if r.status_code == 200 and "Demo Parent User" in r.text:
        print("SUCCESS: Logged in as parent tester.")
    else:
        print(f"FAILED: Login failed. Status: {r.status_code}")
        return False

    # 2. Check initial students
    found_students = 0
    for name in ["Aarav Sharma", "Isha Patel", "Ryan Dsouza"]:
        if name in r.text:
            print(f"SUCCESS: Found student '{name}' on dashboard.")
            found_students += 1
    
    if found_students < 3:
        print("FAILED: Some seeded students are missing.")
        return False

    # 3. Register a new student
    print("\n--- Registering New Student for Auto-Mapping ---")
    reg_url = f"{BASE_URL}/register/"
    r = s.get(reg_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    csrf = soup.find('input', {'name': 'csrfmiddlewaretoken'})['value']
    
    suffix = random.randint(1000, 9999)
    reg_data = {
        "csrfmiddlewaretoken": csrf,
        "full_name": f"Tina Singh {suffix}",
        "email": f"tina{suffix}@aahguru.local",
        "parent_name": "Demo Parent User",
        "parent_email": "parent_tester@aahguru.local",
        "mobile": f"987654{suffix}",
        "class_grade": "7"
    }
    
    r = s.post(reg_url, data=reg_data, headers={"Referer": reg_url})
    if r.status_code == 200 or r.status_code == 302:
        print(f"SUCCESS: Registered 'Tina Singh {suffix}'.")
    else:
        print(f"FAILED: Registration failed. Status: {r.status_code}")
        return False

    # 4. Refresh Dashboard
    dash_url = f"{BASE_URL}/parent/dashboard/" # Adjusted based on url structure
    # Actually, the parent portal home
    r = s.get(dash_url)
    if f"Tina Singh {suffix}" in r.text:
        print("SUCCESS: New student automatically mapped to parent dashboard!")
        return True
    else:
        print("FAILED: New student not found on dashboard.")
        # Print a snippet to debug
        print(r.text[:1000])
        return False

if __name__ == "__main__":
    test_parent_dashboard()
