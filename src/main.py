import os
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
from calender import add_events
from datetime import datetime

# Load environment variables
load_dotenv()

# Get credentials
user_id = os.getenv('USER_ID')
password = os.getenv('PASSWORD')

# GITAM URLs
login_url = "https://login.gitam.edu/Login.aspx"

firefox_options = Options()
# firefox_options.add_argument("--headless")

# Set up the WebDriver with explicit geckodriver path
gecko_driver_path = "/snap/bin/firefox.geckodriver"
service = Service(executable_path=gecko_driver_path)
driver = webdriver.Firefox(service=service, options=firefox_options)

def parse_dates(dates, default_year):
    """Convert date strings like 'Nov-07' to 'YYYY-MM-DD'."""
    formatted_dates = []
    for date in dates:
        try:
            # Parse using datetime with assumed year
            parsed_date = datetime.strptime(f"{default_year}-{date}", "%Y-%b-%d")
            formatted_date = parsed_date.strftime("%Y-%m-%d")
            formatted_dates.append(formatted_date)
        except ValueError as e:
            print(f"[ERROR] Could not parse date '{date}': {e}")
            formatted_dates.append(None)  # Add None for invalid dates
    return formatted_dates

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
    WebDriverWait(driver, 35).until(
        EC.presence_of_element_located((By.CLASS_NAME, "course"))
    ).click()

    # Wait for assignments to load
    print("[INFO] Waiting for assignments to load...")
    h6_elements = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".eventName > span:nth-child(2)"))
    )
    print('reached')
    date_elements = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".eventDay"))
    )
    year_elements = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".eventYear"))
    )

    # Extract assignment data
    assignments = [h6.text for h6 in h6_elements]
    dates = [f"{year.text}-{date.text}" for date, year in zip(date_elements, year_elements)]  # Format YYYY-MM-DD
    current_year = datetime.now().year
    dates = parse_dates(dates, current_year)  # Convert to 'YYYY-MM-DD'

    # Pass assignments and dates to calendar.py
    if assignments:
        print("[INFO] Adding assignments to Google Calendar...")
        add_events(assignments, dates)
    else:
        print("[INFO] No assignments found.")

except Exception as e:
    print(f"[ERROR] An error occurred: {str(e)}")

finally:
    # Close the WebDriver
    print("[INFO] Closing the WebDriver...")
    driver.quit()
