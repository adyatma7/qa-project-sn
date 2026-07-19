"""
Bill Pay page object — Selenium version. Field names confirmed already
via playwright-tests/pages/bill_pay_page.py (DEC-010) — reused, not
re-researched.
"""
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import url_for


class BillPayPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def goto(self):
        self.driver.get(url_for("billpay.htm"))

    def pay(
        self,
        name: str,
        street: str,
        city: str,
        state: str,
        zip_code: str,
        phone: str,
        account_number: str,
        amount: str,
    ):
        # Click (focus) explicitly before typing, and always let the next
        # click below force a real blur — even when `name` is empty.
        # send_keys("") alone sends zero keystrokes and never touches the
        # field at all, which is the experiment described in
        # docs/bugs/OBSERVATION-002.md: does a real focus+blur, even with
        # nothing typed, change the result vs the original no-op version?
        name_field = self.wait.until(
            EC.presence_of_element_located((By.NAME, "payee.name"))
        )
        name_field.click()
        if name:
            name_field.send_keys(name)
        self.driver.find_element(By.NAME, "payee.address.street").click()  # forces blur on name field
        self.driver.find_element(By.NAME, "payee.address.street").send_keys(street)
        self.driver.find_element(By.NAME, "payee.address.city").send_keys(city)
        self.driver.find_element(By.NAME, "payee.address.state").send_keys(state)
        self.driver.find_element(By.NAME, "payee.address.zipCode").send_keys(zip_code)
        self.driver.find_element(By.NAME, "payee.phoneNumber").send_keys(phone)
        self.driver.find_element(By.NAME, "payee.accountNumber").send_keys(account_number)
        self.driver.find_element(By.NAME, "verifyAccount").send_keys(account_number)
        self.driver.find_element(By.NAME, "amount").send_keys(amount)
        self.driver.find_element(By.CSS_SELECTOR, 'input[value="Send Payment"]').click()

    def expect_success(self):
        self.wait.until(
            EC.presence_of_element_located((By.XPATH, "//h1[text()='Bill Payment Complete']"))
        )

    def expect_not_completed(self):
        time.sleep(2)
        headings = self.driver.find_elements(
            By.XPATH, "//h1[text()='Bill Payment Complete']"
        )
        assert len(headings) == 0
