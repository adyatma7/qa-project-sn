"""
Phase 2: Transfer Funds. High risk per risk-analysis.md — moves real money.
Every test logs in fresh via the shared john/demo account first (same
known trade-off as Phase 1, see DEC-006).
"""
from pages.login_page import LoginPage
from pages.transfer_page import TransferPage


def _login(page):
    login_page = LoginPage(page)
    login_page.goto()
    login_page.login("john", "demo")


def test_valid_transfer_completes(page):
    _login(page)
    transfer_page = TransferPage(page)
    transfer_page.goto()
    transfer_page.transfer(amount="1")
    transfer_page.expect_success()


def test_transfer_exceeding_balance(page):
    # ADVERSARIAL, exploratory — same spirit as Phase 1's empty-credentials
    # test. ParaBank is commonly reported (unconfirmed this session) to not
    # enforce a sufficient-balance check on transfers. If this test finds
    # the transfer succeeds anyway, that's a legitimate finding for
    # docs/bugs/ — reproduce a couple of times per the usual process before
    # filing. Using an absurdly large amount specifically to make "did it
    # silently succeed" unambiguous either way.
    _login(page)
    transfer_page = TransferPage(page)
    transfer_page.goto()
    transfer_page.transfer(amount="999999999")
    transfer_page.expect_not_completed()
