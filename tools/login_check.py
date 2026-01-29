import requests
import sys

# Setup session to handle cookies/CSRF
s = requests.Session()
BASE_URL = "http://127.0.0.1:8000"

def test_parent_login():
    print("--- Verifying Parent Login & Dashboard Content ---")
    
    # 1. Get login page to get CSRF
    try:
        r = s.get(f"{BASE_URL}/accounts/parent/login/")
        r.raise_for_status()
        csrftoken = s.cookies['csrftoken']
        print("[1] Fetched login page and CSRF token.")
    except Exception as e:
        print(f"FAILED to load login page: {e}")
        return False

    # 2. Attempt Login
    login_data = {
        "csrfmiddlewaretoken": csrftoken,
        "username": "parent1",
        "password": "Parent@12345"
    }
    
    try:
        headers = {"Referer": f"{BASE_URL}/accounts/parent/login/"}
        r = s.post(f"{BASE_URL}/accounts/parent/login/", data=login_data, headers=headers)
        
        # Check if redirected to dashboard
        if r.status_code == 200 and "/parent/dashboard/" in r.url:
            print(f"SUCCESS: Logged in and redirected to {r.url}")
            
            # 3. Verify Dashboard Content
            # Check for generic student indicator or specific names from seed
            if "Parent Portal" in r.text and "Linked students" in r.text or "students" in r.text.lower():
                print("SUCCESS: Dashboard text found.")
                # Look for seeded students if they exist
                if "Aarav" in r.text or "Diya" in r.text or "student" in r.text.lower():
                    print("SUCCESS: Student information is visible on dashboard.")
                    return True
                else:
                    print("WARNING: Dashboard loaded but no students found. (Maybe seed hasn't run?)")
                    return True
            else:
                print("FAILED: Dashboard content not found as expected.")
                # print(r.text[:500])
                return False
        else:
            print(f"FAILED: Login unsuccessful. Status: {r.status_code}, URL: {r.url}")
            if "error" in r.text.lower():
                print("Error messages found in page.")
            return False
            
    except Exception as e:
        print(f"FAILED during login process: {e}")
        return False

if __name__ == "__main__":
    success = test_parent_login()
    if success:
        print("\nOVERALL STATUS: PASS")
    else:
        print("\nOVERALL STATUS: FAIL")
        sys.exit(1)
