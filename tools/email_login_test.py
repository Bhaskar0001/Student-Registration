import requests
import sys

# Setup session to handle cookies/CSRF
s = requests.Session()
BASE_URL = "http://127.0.0.1:8004"

def test_email_login():
    print("--- Verifying Email-Based Parent Login ---")
    
    # 1. Get login page to get CSRF
    try:
        r = s.get(f"{BASE_URL}/accounts/parent/login/")
        r.raise_for_status()
        csrftoken = s.cookies['csrftoken']
    except Exception as e:
        print(f"FAILED to load login page: {e}")
        return False

    # 2. Attempt Login with EMAIL (seeded parent's email)
    # Based on seed_demo.py, parent1's email is parent1@aahguru.local
    login_data = {
        "csrfmiddlewaretoken": csrftoken,
        "username": "parent1@aahguru.local",
        "password": "Parent@12345"
    }
    
    try:
        headers = {"Referer": f"{BASE_URL}/accounts/parent/login/"}
        r = s.post(f"{BASE_URL}/accounts/parent/login/", data=login_data, headers=headers)
        
        # Check if redirected to dashboard
        if r.status_code == 200 and "/parent/dashboard/" in r.url:
            print(f"SUCCESS: Logged in via EMAIL and redirected to Dashboard.")
            return True
        else:
            print(f"FAILED: Login unsuccessful with email. Status: {r.status_code}, URL: {r.url}")
            return False
            
    except Exception as e:
        print(f"FAILED during login process: {e}")
        return False

if __name__ == "__main__":
    if test_email_login():
        print("\nOVERALL STATUS: PASS")
    else:
        print("\nOVERALL STATUS: FAIL")
        sys.exit(1)
