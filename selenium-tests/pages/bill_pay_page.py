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
        self.wait.until(
            EC.presence_of_element_located((By.NAME, "payee.name"))
        ).send_keys(name)
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
