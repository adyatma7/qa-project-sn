"""
Transfer Funds page object — Selenium version. Field names confirmed
already via playwright-tests/pages/transfer_page.py (DEC-010) — reused
here, not re-researched.
"""
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from config import url_for


class TransferPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def goto(self):
        self.driver.get(url_for("transfer.htm"))

    def transfer(self, amount: str, from_index: int = 0, to_index: int = 0):
        self.wait.until(
            EC.presence_of_element_located((By.ID, "amount"))
        ).send_keys(amount)
        Select(self.driver.find_element(By.ID, "fromAccountId")).select_by_index(from_index)
        Select(self.driver.find_element(By.ID, "toAccountId")).select_by_index(to_index)
        self.driver.find_element(By.CSS_SELECTOR, 'input[value="Transfer"]').click()

    def expect_success(self):
        self.wait.until(
            EC.presence_of_element_located((By.XPATH, "//h1[text()='Transfer Complete!']"))
        )

    def expect_not_completed(self):
        # No clean "wait and confirm this never appears" primitive in
        # Selenium the way Playwright's not_to_be_visible() polls
        # automatically — see selenium-tests/README.md. Fixed sleep is a
        # genuine, worth-discussing limitation, not an oversight.
        time.sleep(2)
        headings = self.driver.find_elements(
            By.XPATH, "//h1[text()='Transfer Complete!']"
        )
        assert len(headings) == 0
