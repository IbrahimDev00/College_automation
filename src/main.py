import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Retrieve credentials from environment variables
user_id = os.getenv('USER_ID')
password = os.getenv('PASSWORD')

# URLs for logging in and accessing the dashboard
login_url = "https://login.gitam.edu/Login.aspx"
dashboard_url = "https://glearn.gitam.edu/student/std_dashboard_main"

# Start a session
session = requests.Session()

# Payload for login
payload = {
    'User ID': user_id,
    'Password': password
}

# Perform the login request
response = session.post(login_url, data=payload)

# Check if login was successful
if response.ok:
    print("Logged in successfully!")
else:
    print("Login failed. Please check your credentials.")
    exit()

# Get the dashboard page
response = session.get(dashboard_url)
soup = BeautifulSoup(response.text, 'html.parser')

# Find the div containing assignments
works = soup.find_all('div', class_='dashboardDivHeight cardDateBox')

assignments = []
if works:
    for work in works:
        # Each work is a div, find all list items within it
        assignment_items = work.find_all('li')
        for item in assignment_items:
            assignment_txt = item.get_text(strip=True)
            assignments.append(assignment_txt)

# Print the extracted assignments
if assignments:
    for assignment in assignments:
        print(assignment)
else:
    print("No assignments found.")
