"""
Phase 1: Auth module — positive + negative coverage per blueprint Section 7's
table. Still using ParaBank's shared demo login (john/demo) for the positive
case; test_data_generator.py exists now but isn't wired in yet since none of
these tests create accounts — that happens once Registration is in scope.
"""
from pages.login_page import LoginPage
import pytest


def test_valid_login_reaches_accounts_overview(page):
    login_page = LoginPage(page)
    login_page.goto()
    login_page.login("john", "demo")
    login_page.expect_logged_in()


@pytest.mark.xfail(
    reason="BUG-001: invalid password authenticates the user instead of "
    "rejecting the login (docs/bugs/BUG-001.md). Reproduced 2/2 in this "
    "tool, but did NOT reproduce in a Selenium cross-check (see "
    "selenium-tests/), so this is understood as intermittent rather than "
    "guaranteed — strict=False on purpose now. A guaranteed 'always "
    "fails' claim (strict=True) would be an overclaim given that "
    "evidence; downgraded from an earlier version of this marker that "
    "did use strict=True before the cross-tool run.",
    strict=False,
)
def test_invalid_password_shows_error(page):
    login_page = LoginPage(page)
    login_page.goto()
    login_page.login("john", "definitely-not-the-real-password")
    login_page.expect_login_error()


def test_empty_credentials_are_rejected(page):
    # Deliberately adversarial per Section 7's bug-hunting tactic: ParaBank
    # is an old-style server-rendered app, so there may be no client-side
    # "this field is required" validation at all — submitting blank fields
    # might just hit the server and come back with the same generic error,
    # or it might behave unexpectedly. Using the defensive assertion here
    # on purpose, because the exact behavior isn't confirmed yet.
    #
    # RUN THIS FIRST AND READ WHAT ACTUALLY HAPPENS. If the behavior is
    # anything other than a clean rejection, that's a real Phase 1 bug
    # report — see docs/bugs/README.md for what to do next.
    login_page = LoginPage(page)
    login_page.goto()
    login_page.login("", "")
    login_page.expect_login_failed()
