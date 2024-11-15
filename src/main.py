import os
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager
from dotenv import load_dotenv
from bs4 import BeautifulSoup

# Load environment variables
load_dotenv()

# Get my stuff
user_id = os.getenv('USER_ID')
password = os.getenv('PASSWORD')

# GITAM URLS
login_url = "https://login.gitam.edu/Login.aspx"
dashboard_url = "https://glearn.gitam.edu/Student/std_dashboard_main"


firefox_options = Options()
# firefox_options.add_argument("--headless")

# Set up the WebDriver with explicit geckodriver path
gecko_driver_path = "/snap/bin/firefox.geckodriver"

# Initialize the Firefox service using the specific path for geckodriver
service = Service(executable_path=gecko_driver_path)

# Set up the WebDriver with the Firefox service and options
driver = webdriver.Firefox(service=service, options=firefox_options)

try:
    print("[INFO] Navigating to the login page...")
    driver.get(login_url)

    # Put my creds in
    print("[INFO] Entering login credentials...")
    driver.find_element(By.ID, "txtusername").send_keys(user_id)
    driver.find_element(By.ID, "password").send_keys(password)

    # solve CAPTCHA
    print("[INFO] Solving CAPTCHA...")
    captcha_div = driver.find_element(By.CLASS_NAME, "preview")
    captcha_tags = captcha_div.find_elements(By.TAG_NAME, "span") 

    num1 = int(captcha_tags[0].text)
    num2 = int(captcha_tags[4].text) 
    solution = num1 + num2
    print(f"[INFO] CAPTCHA solved: {num1} + {num2} = {solution}")

    captcha_input = driver.find_element(By.ID, "captcha_form")  # Adjust ID as needed
    captcha_input.send_keys(str(solution))

    
    print("[INFO] Submitting login form...")
    driver.find_element(By.ID, "Submit").click() 

    # Verify login success
    if "dashboard" in driver.current_url.lower():
        print("[SUCCESS] Logged in successfully!")
    else:
        print("[ERROR] Login failed! Please check your credentials or CAPTCHA solution.")
        driver.quit()
        exit()

    # Navigate to the dashboard page
    print("[INFO] Navigating to the dashboard...")
    driver.get(dashboard_url)
    html_content = driver.page_source

    # Parse the HTML with BeautifulSoup
    print("[INFO] Parsing dashboard for assignments...")
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find the div containing assignments
    #works = soup.find_all('div', class_='dashboardDivHeight cardDateBox')
    works_div = driver.find_element(By.ID, "ullist_today_cld")
    works = driver.find_elements(By.TAG_NAME, "li")
    # Extract and process assignment data
    assignments = []
    if works:
        for work in works:
            assignment_items = work.find_all('li')
            for item in assignment_items:
                assignment_txt = item.get_text(strip=True)
                assignments.append(assignment_txt)

    # Print or update the calendar with extracted assignments
    if assignments:
        print("[SUCCESS] Assignments found:")
        for assignment in assignments:
            print(f"- {assignment}")
    else:
        print("[INFO] No assignments found.")

except Exception as e:
    print(f"[ERROR] An error occurred: {e}")

finally:
    # Close the WebDriver
    print("[INFO] Closing the WebDriver...")
    driver.quit()
