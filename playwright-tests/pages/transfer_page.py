"""
Page Object for ParaBank's Transfer Funds form.

Field names (`fromAccountId`, `toAccountId`, `amount`) are confirmed
against ParaBank's own REST service source code
(github.com/parasoft/parabank, ParaBankService.java) — the UI form fields
mirror the service parameter names, which is ParaBank's consistent pattern
(same as `customer.firstName` on registration). Not independently
confirmed by inspecting the live transfer.htm DOM this session, though —
see DEC-010 in docs/decision-log.md.
"""
from playwright.sync_api import Page, expect


class TransferPage:
    def __init__(self, page: Page):
        self.page = page

    def goto(self):
        self.page.goto("transfer.htm")

    def transfer(self, amount: str, from_index: int = 0, to_index: int = 0):
        # Selecting by index rather than a specific account number on
        # purpose — the shared demo account's number of accounts isn't
        # fixed or known in advance. See DEC-010.
        self.page.locator("#amount").fill(amount)
        self.page.locator("#fromAccountId").select_option(index=from_index)
        self.page.locator("#toAccountId").select_option(index=to_index)
        self.page.locator('input[value="Transfer"]').click()

    def expect_success(self):
        expect(
            self.page.get_by_role("heading", name="Transfer Complete!")
        ).to_be_visible()

    def expect_not_completed(self):
        # Defensive assertion for the adversarial case below, where the
        # actual expected behavior isn't confirmed yet.
        expect(
            self.page.get_by_role("heading", name="Transfer Complete!")
        ).not_to_be_visible()
