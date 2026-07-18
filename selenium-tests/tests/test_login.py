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
    reason="BUG-001 (docs/bugs/BUG-001.md), same root cause as the "
    "Playwright version. Ported specifically to confirm the bug isn't a "
    "Playwright-specific quirk — it reproduces via a completely "
    "different driver/tool. strict=True for the same reason as the "
    "Playwright version.",
    strict=True,
)
def test_invalid_password_shows_error(driver):
    login_page = LoginPage(driver)
    login_page.goto()
    login_page.login("john", "definitely-not-the-real-password")
    login_page.expect_login_error()
