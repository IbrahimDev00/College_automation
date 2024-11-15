import os
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get my stuff
user_id = os.getenv('USER_ID')
password = os.getenv('PASSWORD')

# GITAM URLs
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

    # Enter credentials
    print("[INFO] Entering login credentials...")
    driver.find_element(By.ID, "txtusername").send_keys(user_id)
    driver.find_element(By.ID, "password").send_keys(password)

    # Solve CAPTCHA
    print("[INFO] Solving CAPTCHA...")
    captcha_div = driver.find_element(By.CLASS_NAME, "preview")
    captcha_tags = captcha_div.find_elements(By.TAG_NAME, "span")

    num1 = int(captcha_tags[0].text)
    num2 = int(captcha_tags[4].text)
    solution = num1 + num2
    print(f"[INFO] CAPTCHA solved: {num1} + {num2} = {solution}")

    captcha_input = driver.find_element(By.ID, "captcha_form")
    captcha_input.send_keys(str(solution))

    # Submit form
    print("[INFO] Submitting login form...")
    driver.find_element(By.ID, "Submit").click()

    # Wait for the dashboard to load and the specific element to appear
    print("[INFO] Navigating to the dashboard...")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "course"))
    ).click()

    # Wait for the assignments to load
    print("[INFO] Waiting for assignments to load...")
    h6_elements = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".eventName > span:nth-child(2)"))
    )
    print(h6_elements[0].get_attribute('outerHTML'))
    # Extract and process assignment data
    assignments = [h6.text for h6 in h6_elements]

    # Print or update the calendar with extracted assignments
    if assignments:
        print("[SUCCESS] Assignments found:")
        for assignment in assignments:
            print(f"- {assignment}")
    else:
        print("[INFO] No assignments found.")

except Exception as e:
    print(f"[ERROR] An error occurred: {str(e)}")

finally:
    # Close the WebDriver
    print("[INFO] Closing the WebDriver...")
    driver.quit()
