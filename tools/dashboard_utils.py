import requests
from bs4 import BeautifulSoup

s = requests.Session()
BASE_URL = "http://127.0.0.1:8003"

def check_dashboard():
    # 1. Login
    r = s.get(f"{BASE_URL}/accounts/parent/login/")
    soup = BeautifulSoup(r.text, 'html.parser')
    csrf = soup.find('input', {'name': 'csrfmiddlewaretoken'})['value']
    
    login_data = {
        'csrfmiddlewaretoken': csrf,
        'username': 'parent1',
        'password': 'Parent@12345'
    }
    s.post(f"{BASE_URL}/accounts/parent/login/", data=login_data)
    
    # 2. Get Dashboard
    r = s.get(f"{BASE_URL}/parent/dashboard/")
    print(f"Dashboard URL: {r.url}")
    if "No students linked yet" in r.text:
         print("FAILURE: Dashboard says no students linked.")
    else:
         print("SUCCESS: Students are visible on the dashboard!")
         # Print some student names to be sure
         if "Aarav" in r.text or "Bhaskar" in r.text:
              print("Confirmed: Student names found in HTML.")

if __name__ == "__main__":
    check_dashboard()
