# Contributing to Assignment Tracker Automation

🎉 Thank you for considering contributing to **Assignment Tracker Automation**! Your contributions can help students worldwide manage their time better and reduce the stress of tracking assignments. Below are some guidelines to help you get started.

---

## 🚀 How to Contribute

1. **Fork the Repository**
   Click the `Fork` button on the top right of this repository to create your own copy.

2. **Clone the Forked Repository**
   ```bash
   git clone https://github.com/your-username/assignment-tracker-automation.git
   cd assignment-tracker-automation


1.  **Create a Branch**\
    Use a descriptive branch name related to your feature or bug fix.

    ```
    git checkout -b feature-name

    ```

2.  **Make Changes**\
    Make sure your changes adhere to the guidelines mentioned below.

3.  **Test Your Changes**\
    Before committing, ensure your changes work as expected and do not break existing functionality.

4.  **Commit and Push**\
    Write a clear and concise commit message.

    ```
    git add .
    git commit -m "Add feature description"
    git push origin feature-name

    ```

5.  **Create a Pull Request (PR)**\
    Go to the original repository, click on `Pull Requests`, and submit your PR. Ensure you fill out the PR template (if provided).

* * * * *

🛠️ Development Setup
---------------------

### Prerequisites

-   **Python 3.7 or later**
-   **pip** for managing Python packages
-   **Geckodriver** for Selenium (Ensure it is in your `PATH`)
-   **Firefox** browser
-   **Google Calendar API credentials**

### Installation

1.  Clone the repository and navigate to the directory:

    ```
    git clone https://github.com/your-username/assignment-tracker-automation.git
    cd assignment-tracker-automation

    ```

2.  Install dependencies:

    ```
    pip install -r requirements.txt

    ```

3.  Set up `.env` file for credentials:

    ```
    USER_ID=<your-portal-user-id>
    PASSWORD=<your-portal-password>

    ```

4.  Follow the [Google Calendar API Quickstart](https://developers.google.com/calendar/quickstart/python) to set up your `client.json`.

5.  Run the project:

    ```
    python main.py

    ```

* * * * *

📝 Contribution Guidelines
--------------------------

### Code of Conduct

Please follow our [Code of Conduct](https://chatgpt.com/c/CODE_OF_CONDUCT.md) to create a welcoming and inclusive environment.

### Reporting Bugs

-   **Check Existing Issues**: Before opening a new issue, ensure it hasn't been reported yet.
-   **Provide Details**: Clearly describe the issue, steps to reproduce it, and any relevant logs or screenshots.

### Suggesting Features

-   Open an issue and select the `Feature Request` template.
-   Describe your feature idea in detail and explain its value to users.

### Writing Code

-   Write clean, readable, and well-documented code.
-   Follow [PEP 8](https://pep8.org/) for Python code style.
-   Include comments for complex logic.

### Testing

-   Ensure all existing functionality works after your changes.
-   Add test cases for new features if possible.

* * * * *

🙌 Acknowledgments
------------------

Thank you for your interest in contributing! Every contribution, no matter how small, helps make this project better. We appreciate your efforts and look forward to collaborating with you!

* * * * *

### 🌟 Contact

For questions or discussions, feel free to open an issue or reach out via [Your Preferred Contact Method].

Let's build something amazing together! 🚀
