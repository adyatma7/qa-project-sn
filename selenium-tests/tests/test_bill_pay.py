"""
Phase 4: bill pay — High risk per risk-analysis.md, ported per DEC-002.
"""
from pages.login_page import LoginPage
from pages.bill_pay_page import BillPayPage


def _login(driver):
    login_page = LoginPage(driver)
    login_page.goto()
    login_page.login("john", "demo")


def test_valid_bill_payment_completes(driver):
    _login(driver)
    bill_pay_page = BillPayPage(driver)
    bill_pay_page.goto()
    bill_pay_page.pay(
        name="Test Payee",
        street="123 Main St",
        city="Beverly Hills",
        state="CA",
        zip_code="90210",
        phone="555-555-5555",
        account_number="12345",
        amount="10",
    )
    bill_pay_page.expect_success()


def test_empty_payee_name_is_rejected(driver):
    _login(driver)
    bill_pay_page = BillPayPage(driver)
    bill_pay_page.goto()
    bill_pay_page.pay(
        name="",
        street="123 Main St",
        city="Beverly Hills",
        state="CA",
        zip_code="90210",
        phone="555-555-5555",
        account_number="12345",
        amount="10",
    )
    bill_pay_page.expect_not_completed()
