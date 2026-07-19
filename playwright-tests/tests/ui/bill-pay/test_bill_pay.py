"""
Phase 2: Bill Pay. High risk per risk-analysis.md — moves real money, same
class of risk as Transfer.
"""
from pages.login_page import LoginPage
from pages.bill_pay_page import BillPayPage
import pytest


def _login(page):
    login_page = LoginPage(page)
    login_page.goto()
    login_page.login("john", "demo")


def test_valid_bill_payment_completes(page):
    _login(page)
    bill_pay_page = BillPayPage(page)
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


def test_empty_payee_name_is_rejected(page):
    # Negative — required field left blank, per the minimum coverage table
    # in blueprint Section 7. Exploratory like Phase 1's empty-credentials
    # test: exact validation behavior not confirmed yet.
    _login(page)
    bill_pay_page = BillPayPage(page)
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


@pytest.mark.xfail(
    reason="BUG-003: Bill Pay does not enforce a sufficient-balance check "
    "(docs/bugs/BUG-003.md) — same symptom as BUG-002 on Transfer. "
    "strict=False, consistent with how BUG-002 is handled. Confirmed by "
    "an actual run — this test ran unmarked for its first attempt, "
    "exactly like test_transfer_exceeding_balance did before BUG-002.",
    strict=False,
)
def test_bill_pay_amount_exceeds_balance(page):
    _login(page)
    bill_pay_page = BillPayPage(page)
    bill_pay_page.goto()
    bill_pay_page.pay(
        name="Test Payee",
        street="123 Main St",
        city="Beverly Hills",
        state="CA",
        zip_code="90210",
        phone="555-555-5555",
        account_number="12345",
        amount="999999999",
    )
    bill_pay_page.expect_not_completed()
