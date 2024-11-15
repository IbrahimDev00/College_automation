# Automated Assignment Extractor

This script automates the process of extracting assignments from your GITAM university website and potentially adding them to your calendar (calendar integration not included in this example).

## Features
* Logs in to your GITAM account (using environment variables for secure credential storage).
* Solves basic CAPTCHAs (addition problems).
* Extracts assignment titles from the dashboard.
* Optionally extracts due dates and years (assuming they are in separate elements).

## Requirements
* Python 3
* Selenium library (`pip install selenium`)
* Gecko driver for Firefox (`https://github.com/mozilla/geckodriver`)

## Instructions
1. Clone this repository.
2. Install required libraries (`pip install selenium`).
3. Download the appropriate Gecko driver for your operating system and place it in a directory accessible by your system (e.g., `/usr/local/bin`).
4. Create a `.env` file in the project root directory.
5. Add the following lines to your `.env` file, replacing `<USER_ID>` and `<PASSWORD>` with your actual credentials
6. Run the script using `python main.py` (replace `main.py` with your actual script filename).
