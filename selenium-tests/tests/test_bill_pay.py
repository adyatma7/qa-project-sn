"""
Phase 4: bill pay — High risk per risk-analysis.md, ported per DEC-002.
"""
from pages.login_page import LoginPage
from pages.bill_pay_page import BillPayPage
import pytest


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


@pytest.mark.xfail(
    reason="OBSERVATION-002 (docs/bugs/OBSERVATION-002.md): this "
    "consistently disagrees with the Playwright version of the same "
    "case across 3 environments now (Windows local, Linux CI, and after "
    "a click+blur experiment) — root cause still unresolved, NOT "
    "confirmed as a ParaBank bug (may be a Selenium/WebDriver-specific "
    "limitation instead). xfail here so CI reflects 'known, tracked, "
    "unresolved' rather than an untriaged failure. strict=False since "
    "the outcome isn't fully understood yet.",
    strict=False,
)
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
