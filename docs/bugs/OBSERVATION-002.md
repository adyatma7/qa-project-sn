# OBSERVATION-002 (not yet a confirmed bug — needs re-run with fixed assertion)

**Found:** running the Selenium port of `test_empty_payee_name_is_rejected`
against the live demo, 2026-07-17.

**What happened:** submitting Bill Pay with an empty payee name resulted
in "Bill Payment Complete" — the payment went through. This contradicts
`docs/traceability-matrix.md`'s earlier record of this case as "confirmed
enforced, no bug," which came from the Playwright version of this same
test appearing to pass.

**Why the earlier Playwright result is now suspect, not trusted:** the
assertion used `expect(heading).not_to_be_visible()` immediately after
clicking submit, with no settle time. If ParaBank's success page takes a
moment to render, this assertion can observe "not visible yet" and
report success — before the success heading actually appears a moment
later. The Selenium version added a 2-second sleep before checking, by
coincidence of a different design choice (not a deliberate fix at the
time), and caught the payment actually completing. This is now fixed in
both frameworks — `expect_not_completed()` in both
`playwright-tests/pages/bill_pay_page.py` and
`playwright-tests/pages/transfer_page.py` now waits before checking (see
DEC-012).

**Why this isn't `BUG-002.md` yet:** the Playwright suite hasn't been
re-run with the fixed assertion. Before filing:
1. Re-run `pytest tests/ui/bill-pay/test_bill_pay.py -v` (Playwright,
   with the DEC-012 fix in place).
2. If it now also shows "Bill Payment Complete" for an empty name →
   confirmed, matches the Selenium finding, file `BUG-002.md`.
3. Also worth re-running `test_transfer_exceeding_balance` in the same
   pass — it used the identical assertion pattern and hasn't been
   independently re-verified with the timing fix. If it still correctly
   rejects the oversized transfer even with the extra wait, that result
   can now be trusted; if not, that's a second finding.

---

## Update: still unresolved, evidence now conflicts

Re-ran both suites with the DEC-012 fix in place:
- **Playwright:** `test_empty_payee_name_is_rejected` now PASSES (empty
  name correctly rejected).
- **Selenium:** the same case FAILED again (empty name accepted) — same
  result as before the fix.

The two tools now disagree on the same scenario, both using an
equivalent wait-before-checking approach. This isn't resolved yet.

**New working hypothesis:** the shared `john`/`demo` account's checking
balance may be getting drawn down across all these test runs (every
`test_valid_transfer_completes` moves $1, every
`test_valid_bill_payment_completes` moves $10 — dozens of runs across
this whole project so far). If the balance ever gets low enough, a
payment could fail for an unrelated reason (insufficient funds) that
*looks* like "empty payee name correctly rejected" by coincidence, not
because that field is actually validated. This would also mean the
Playwright "pass" is itself unreliable, for a different reason than the
original race condition.

**Not filing a bug for this yet.** Next step, before drawing a
conclusion: check the account's current balance directly (Accounts
Overview) before and after this specific test, to rule the
low-balance hypothesis in or out. Recorded here rather than guessed at
in a bug report.

---

## Update: the balance hypothesis is likely wrong — better evidence found

Re-ran both suites again. New data point: **each tool is now internally
consistent across multiple runs** — Playwright: 2/2 "rejected." Selenium:
3/3 "accepted." If the earlier balance-depletion hypothesis were right,
we'd expect *inconsistency within* each tool too, since account balance is
shared global state that doesn't care which tool is asking. A clean split
by *tool* rather than by *time/order* points somewhere else.

**New, more specific hypothesis:** `send_keys("")` in Selenium sends zero
keystrokes — it's effectively a no-op that never dispatches `input` or
`blur` events on the field. Playwright's `.fill("")` sets the value (to
empty) AND dispatches the equivalent events regardless. If ParaBank has
any client-side validation that only activates once a field has actually
been focused-and-left (a "touched" state), Selenium's version of this test
may never trigger it — meaning the form submits in a state a real user
interacting normally would never produce. If so, **this would not be a
ParaBank bug at all — it would mean the Selenium test itself isn't a
valid simulation of real user behavior for this specific case**, and
Playwright's "rejected" result would be the trustworthy one.

**Concrete experiment to actually settle this** (not filing anything
until this is tried): in `selenium-tests/pages/bill_pay_page.py`,
explicitly click into the name field and then click into the next field
(forcing a real focus + blur) even when leaving it empty, instead of
relying on `send_keys("")` alone:
```python
name_field = self.wait.until(
    EC.presence_of_element_located((By.NAME, "payee.name"))
)
name_field.click()
if name:
    name_field.send_keys(name)
self.driver.find_element(By.NAME, "payee.address.street").click()  # forces blur
```
If this changes the Selenium result to "rejected" (matching Playwright),
the hypothesis is confirmed — this was a test-simulation gap, not an app
bug, and OBSERVATION-002 closes with "no bug, Selenium needed a more
realistic interaction to test this fairly." If it still shows "accepted,"
the hypothesis is wrong and the investigation continues.
