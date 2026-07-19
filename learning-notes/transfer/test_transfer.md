# Learning Notes: `test_transfer.py`

Companion notes for `playwright-tests/pages/transfer_page.py` and
`tests/ui/transfer/test_transfer.py`. Backfilled in Phase 5 — written
after the fact, but describing real decisions and a real bug found along
the way, not reconstructed from memory.

## `Select(...).select_option(index=from_index)`
Playwright's way of choosing an option from a `<select>` by position
rather than by value or visible text. Chosen over a specific account
number because the shared demo account's number of accounts isn't fixed
— selecting by index works whether there's one account or several.

## Why `from_index` and `to_index` default to `0`
If the account only has one account, "from" and "to" end up being the
same one — effectively a self-transfer. Not ideal, but acceptable for
Phase 2's scope: registering a second, independent account is out of
scope until Registration is automated (see `docs/requirements/transfer.md`).

## `expect_success()` — checking a heading, not a URL
`get_by_role("heading", name="Transfer Complete!")` matches on the
accessible role and visible text together, which is more specific than
matching a CSS class or checking the URL changed — a URL check wouldn't
distinguish "the transfer succeeded" from "the page merely navigated
somewhere."

## `expect_not_completed()` — the one that actually caught a bug
This one has a real story, not just a design note. The original version
called `not_to_be_visible()` immediately after clicking Transfer. That
can early-exit as "not visible YET" if checked before a delayed success
page finishes rendering — a false pass, not a real rejection.

This stayed hidden until Phase 4's Selenium port ran the equivalent bill
pay case with an incidental 2-second sleep before checking, and got a
different (correct) answer than Playwright had been reporting. Once the
same wait was added to Playwright's version here too, re-running this
exact test revealed [BUG-002](../../docs/bugs/BUG-002.md): a transfer of
999,999,999 actually completes — ParaBank doesn't enforce a balance check
on Transfer at all. The earlier "pass" had been masking that the whole
time.

**Lesson, stated once so it doesn't need repeating per test file:** a
negative assertion checked too early can report success for the wrong
reason. If a test asserts "X does not happen," give the page a moment to
actually finish doing whatever it's going to do before checking — don't
check-then-hope.
