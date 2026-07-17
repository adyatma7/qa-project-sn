"""
Page Object for ParaBank's login form.
Selectors live here and only here — if ParaBank's markup ever changes,
this is the one file to fix, not every test that happens to log in.
"""
from playwright.sync_api import Page, expect


class LoginPage:
    def __init__(self, page: Page):
        self.page = page

    def goto(self):
        # No leading slash on purpose — see learning-notes for why. With a
        # base_url ending in "/parabank/", a relative "index.htm" appends
        # to it. A leading "/index.htm" would instead reset to the domain
        # root and silently drop "/parabank" — that was BUG #1, found by
        # actually running this against the live site.
        self.page.goto("index.htm")

    def login(self, username: str, password: str):
        self.page.locator('input[name="username"]').fill(username)
        self.page.locator('input[name="password"]').fill(password)
        self.page.locator('input[value="Log In"]').click()

    def expect_logged_in(self):
        # Checking the page TITLE rather than visible text on purpose —
        # titles tend to survive redesigns that change on-page wording.
        expect(self.page).to_have_title("ParaBank | Accounts Overview")

    def expect_login_error(self, message: str = "The username and password could not be verified."):
        # ParaBank renders login errors inside an element with class="error".
        # Verified against a real working Selenium example, not assumed.
        error = self.page.locator(".error")
        expect(error).to_contain_text(message)

    def expect_login_failed(self):
        # Weaker, more defensive check for cases where the exact error text
        # is uncertain (e.g. empty-field submission) — just confirms login
        # did NOT succeed, without betting on specific wording.
        expect(self.page).not_to_have_title("ParaBank | Accounts Overview")
