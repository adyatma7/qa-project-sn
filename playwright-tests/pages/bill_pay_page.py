"""
Page Object for ParaBank's Bill Pay form.

Field name pattern (`payee.name`, `payee.address.street`, etc.) is inferred
from two confirmed sources, not a live DOM inspection this session:
1. ParaBank's REST bill-pay API accepts an XML body using these exact
   element names (name, address.street/city/state/zipCode, phoneNumber,
   accountNumber) — confirmed via a working example request.
2. ParaBank consistently names UI form fields after the underlying Java
   bean property (`customer.firstName` on registration, confirmed working
   in this project's own Phase 0/1 tests).
Reasonable confidence, not full confirmation — see DEC-010.
"""
from playwright.sync_api import Page, expect


class BillPayPage:
    def __init__(self, page: Page):
        self.page = page

    def goto(self):
        self.page.goto("billpay.htm")

    def pay(
        self,
        name: str,
        street: str,
        city: str,
        state: str,
        zip_code: str,
        phone: str,
        account_number: str,
        amount: str,
    ):
        self.page.locator('input[name="payee.name"]').fill(name)
        self.page.locator('input[name="payee.address.street"]').fill(street)
        self.page.locator('input[name="payee.address.city"]').fill(city)
        self.page.locator('input[name="payee.address.state"]').fill(state)
        self.page.locator('input[name="payee.address.zipCode"]').fill(zip_code)
        self.page.locator('input[name="payee.phoneNumber"]').fill(phone)
        self.page.locator('input[name="payee.accountNumber"]').fill(account_number)
        self.page.locator('input[name="verifyAccount"]').fill(account_number)
        self.page.locator('input[name="amount"]').fill(amount)
        self.page.locator('input[value="Send Payment"]').click()

    def expect_success(self):
        expect(
            self.page.get_by_role("heading", name="Bill Payment Complete")
        ).to_be_visible()

    def expect_not_completed(self):
        expect(
            self.page.get_by_role("heading", name="Bill Payment Complete")
        ).not_to_be_visible()
