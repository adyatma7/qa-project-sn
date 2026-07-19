"""
Phase 2: Bill Pay. High risk per risk-analysis.md — moves real money, same
class of risk as Transfer.
"""
from pages.login_page import LoginPage
from pages.bill_pay_page import BillPayPage


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


def test_bill_pay_amount_exceeds_balance(page):
    # From the AI-assisted testing exercise — see
    # ai-assisted-testing/bill-pay-negative-cases.md. Kept specifically
    # because BUG-002 already found Fund Transfer doesn't enforce a
    # balance check; testing whether Bill Pay has the same gap is the
    # obvious follow-up, not a generic idea. Exploratory on purpose — not
    # marked xfail, because the outcome isn't known yet, unlike
    # test_transfer_exceeding_balance which only got its xfail marker
    # after BUG-002 was actually confirmed.
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
