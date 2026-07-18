"""
Phase 4: transfer — High risk per risk-analysis.md, ported per DEC-002.
"""
from pages.login_page import LoginPage
from pages.transfer_page import TransferPage


def _login(driver):
    login_page = LoginPage(driver)
    login_page.goto()
    login_page.login("john", "demo")


def test_valid_transfer_completes(driver):
    _login(driver)
    transfer_page = TransferPage(driver)
    transfer_page.goto()
    transfer_page.transfer(amount="1")
    transfer_page.expect_success()


def test_transfer_exceeding_balance(driver):
    _login(driver)
    transfer_page = TransferPage(driver)
    transfer_page.goto()
    transfer_page.transfer(amount="999999999")
    transfer_page.expect_not_completed()
