"""
Login page object — Selenium version. Compare directly against
playwright-tests/pages/login_page.py: same flow, explicit waits instead
of auto-wait. See selenium-tests/README.md.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import url_for


class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def goto(self):
        self.driver.get(url_for("index.htm"))

    def login(self, username: str, password: str):
        # Explicit wait before every interaction — Playwright's .fill()
        # does this implicitly; Selenium's find_element does not.
        self.wait.until(
            EC.presence_of_element_located((By.NAME, "username"))
        ).send_keys(username)
        self.driver.find_element(By.NAME, "password").send_keys(password)
        self.driver.find_element(
            By.CSS_SELECTOR, 'input[value="Log In"]'
        ).click()

    def expect_logged_in(self):
        self.wait.until(EC.title_is("ParaBank | Accounts Overview"))

    def expect_login_error(
        self, message: str = "The username and password could not be verified."
    ):
        error = self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".error"))
        )
        assert message in error.text
