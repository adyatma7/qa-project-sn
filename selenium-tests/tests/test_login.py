"""
Phase 4: 2 of the 6 ported tests — login. Why these specific cases:
selenium-tests/README.md (DEC-002).
"""
import pytest
from pages.login_page import LoginPage


def test_valid_login_reaches_accounts_overview(driver):
    login_page = LoginPage(driver)
    login_page.goto()
    login_page.login("john", "demo")
    login_page.expect_logged_in()


@pytest.mark.xfail(
    reason="BUG-001 (docs/bugs/BUG-001.md). NOT strict, unlike the "
    "Playwright version — an actual run showed this does NOT reproduce "
    "every time (this test unexpectedly passed once), so BUG-001 is "
    "understood to be intermittent rather than deterministic. strict=True "
    "would break the build on a legitimate pass, which isn't the signal "
    "we want here.",
    strict=False,
)
def test_invalid_password_shows_error(driver):
    login_page = LoginPage(driver)
    login_page.goto()
    login_page.login("john", "definitely-not-the-real-password")
    login_page.expect_login_error()
