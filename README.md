# College Automation: Assignment Calendar Integration

This project automates the process of logging into the GITAM portal, scraping assignments with their due dates, and adding them as events to your Google Calendar. The automation runs daily using a `systemd` timer and leverages Selenium for web scraping and the Google Calendar API for event creation.

---

## **Features**
1. Automated login to the GITAM portal.
2. CAPTCHA solving using Selenium.
3. Assignment scraping with due dates.
4. Integration with Google Calendar to create events.
5. Scheduled execution every 24 hours using a `systemd` timer.

---

## **Project Architecture**
Below is a high-level overview of the workflow:





## Prerequisites

### 1\. Install Dependencies

  * **Python and pip:**
    Ensure you have Python and `pip` (package manager) installed. Refer to your Linux distribution's documentation for installation instructions.

  * **Required Python packages:**

    ```bash
    pip install selenium python-dotenv google-api-python-client google-auth-httplib2 google-auth-oauthlib
    ```

  * **geckodriver (for Firefox scraping):**

    ```bash
    sudo apt install firefox-geckodriver
    ```

    (Replace `apt` with your package manager if different.)

### 2\. Set Up Google API Credentials

1.  Go to the Google Cloud Console: [https://console.cloud.google.com/](https://www.google.com/url?sa=E&source=gmail&q=https://console.cloud.google.com/)
2.  Create a new project or select an existing one.
3.  Enable the Google Calendar API.
4.  Create OAuth 2.0 credentials (Service account key) and download the JSON file.
5.  Place the downloaded `credentials.json` file in the `src` directory of your project.

### 3\. Set Up Environment Variables

1.  Create a file named `.env` (notice the leading dot) in the `src` directory:

<!-- end list -->

```
USER_ID=<your_gitam_user_id>
PASSWORD=<your_gitam_password>
```

Replace `<your_gitam_user_id>` and `<your_gitam_password>` with your actual credentials.

## Running the Project

### 1\. Manually

1.  Navigate to the `src` directory of your project.
2.  Execute the main script:

<!-- end list -->

```bash
python3 main.py
```

### 2\. Automate with systemd

**Step 1: Create a Shell Script**

1.  Create a new shell script named `run_gitam_scraper.sh` in your project's root directory:

<!-- end list -->

```bash
nano run_gitam_scraper.sh
```

2.  Paste the following content into the file:

<!-- end list -->

```bash
#!/bin/bash
cd ~/Documents/Github_clones/College_automation/src
/usr/bin/python3 main.py
```

3.  Make the script executable:

<!-- end list -->

```bash
chmod +x run_gitam_scraper.sh
```

**Step 2: Set Up Systemd Service**

1.  Open a terminal window with root privileges (use `sudo su` or `sudo -i`).
2.  Create a new systemd service file named `gitam_scraper.service` in the `/etc/systemd/system/` directory:

<!-- end list -->

```bash
sudo nano /etc/systemd/system/gitam_scraper.service
```

3.  Paste the following content into the file, replacing `<username>` and `<group>` with your actual username and group (usually the same as your username):

<!-- end list -->

```
[Unit]
Description=Automation to scrape assignments and add them to Google Calendar
After=network.target

[Service]
ExecStart=/home/<username>/Documents/Github_clones/College_automation/run_gitam_scraper.sh
WorkingDirectory=/home/<username>/Documents/Github_clones/College_automation/src
User=<username>
Group=<group>
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

**Step 3: Create a Timer**

1.  Remain in the terminal window with root privileges.
2.  Create a new systemd timer file named `gitam_scraper.timer` in the same directory (`/etc/systemd/system/`):

<!-- end list -->

```bash
sudo nano /etc/systemd/system/gitam_scraper.timer
```

3.  Paste the following content into the file:

<!-- end list -->

```
[Unit]
Description=Timer to run GITAM scraper every 24 hours

[Timer]
OnBootSec=5min
OnUnitActiveSec=24h
Unit=gitam_scraper.service

[Install]
WantedBy=multi-user.target
```

**Step 4: Enable and Start the Timer**

1.  Reload systemd:

<!-- end list -->

```bash
sudo systemctl daemon-reload
```

2.  Enable the timer:

<!-- end list -->

```bash
sudo systemctl enable gitam_scraper.timer
```

3.  Start the timer:

<!-- end list -->

```bash
sudo systemctl start gitam_scraper.timer
```
