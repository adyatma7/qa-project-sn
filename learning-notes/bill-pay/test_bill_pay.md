# Learning Notes: `test_bill_pay.py`

Companion notes for `playwright-tests/pages/bill_pay_page.py` and
`tests/ui/bill-pay/test_bill_pay.py`. Backfilled in Phase 5.

## Field selectors — inferred, not inspected, and it worked
`payee.name`, `payee.address.street`, etc. were never confirmed by
looking at the live page's HTML directly. They were inferred from two
confirmed sources: the REST Bill Pay API's XML payload structure (same
field names as XML elements), and the established `customer.firstName`
naming pattern already proven correct on the registration page. Worth
remembering as a general technique: a consistently-named API can be a
legitimate way to predict UI form field names without direct inspection
— documented honestly as an inference in DEC-010, and it turned out
correct on the first real run.

## Why no `fromAccountId` selection here, unlike Transfer
Bill Pay's form does have a "from account" dropdown, but this page object
never explicitly selects it — relies on the browser's default first-option
selection. This works because the shared demo account has at least one
account, and worked without needing the `Select` handling Transfer
required. Simpler, but only correct because of that assumption — worth
revisiting if the account's structure ever changes.

## `expect_not_completed()` — the case that's still genuinely unresolved
This is the most interesting (and most honest) part of this whole
project's testing. `test_empty_payee_name_is_rejected` initially appeared
to pass in Playwright. A Selenium port of the same case failed —
"Bill Payment Complete" appeared for an empty payee name. Fixing a race
condition in the assertion (same fix as Transfer, see that file's notes)
didn't resolve the disagreement — Playwright kept saying "rejected,"
Selenium kept saying "accepted," consistently, across multiple runs each.

The working explanation, still not confirmed either way: Selenium's
`send_keys("")` sends zero keystrokes and never fires the `input`/`blur`
events that Playwright's `.fill("")` fires regardless of value. If
ParaBank has any client-side check gated on a field being
touched-and-left-empty, Selenium's version of this test may never be
exercising the app the way a real user would — which would mean this was
never a ParaBank bug, just a gap in how faithfully the test simulated a
real interaction. Full writeup and the experiment designed to settle it:
`docs/bugs/OBSERVATION-002.md`.

**Why this note doesn't end with a tidy answer:** because there isn't one
yet. Writing "still investigating, here's the leading hypothesis and how
to test it" is a more honest learning note than inventing a clean
resolution for the sake of finishing the file.

## `test_bill_pay_amount_exceeds_balance` — added from an AI-assisted exercise
Not written from scratch by hand — came out of a documented AI-assisted
brainstorm (`ai-assisted-testing/bill-pay-negative-cases.md`), kept
specifically because [BUG-002](../../docs/bugs/BUG-002.md) already showed
Transfer doesn't enforce a balance check, making "does Bill Pay have the
same gap" the obvious next question rather than a generic idea picked at
random.
