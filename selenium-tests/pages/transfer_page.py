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
        # 20s, not the usual 10s — this account now has 14 accounts (see
        # docs/decision-log.md DEC-018), and transfer.htm has to render a
        # dropdown populated from all of them. 10s was fine when this
        # account had far fewer.
        self.wait = WebDriverWait(driver, 20)

    def goto(self):
        self.driver.get(url_for("transfer.htm"))

    def transfer(self, amount: str, from_index: int = 0, to_index: int = 0):
        self.wait.until(
            EC.presence_of_element_located((By.ID, "amount"))
        ).send_keys(amount)
        # Explicitly wait for the dropdown to actually have options before
        # touching .options — found via a real run that the select can be
        # present in the DOM before its options finish populating,
        # producing "IndexError: list index out of range" otherwise. Not
        # the same bug as DEC-013, a new one found on the very next run.
        self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#fromAccountId option"))
        )
        # NOT select_by_index() on purpose — found via an actual run that
        # it raises NoSuchElementException on modern Selenium. It matches
        # against the option's "index" HTML ATTRIBUTE, which browsers
        # don't literally set in markup (index is a computed DOM
        # property, not an attribute) — a known Selenium 4.x regression,
        # not a mistake in the ParaBank page. See DEC-013.
        Select(self.driver.find_element(By.ID, "fromAccountId")).options[from_index].click()
        Select(self.driver.find_element(By.ID, "toAccountId")).options[to_index].click()
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
