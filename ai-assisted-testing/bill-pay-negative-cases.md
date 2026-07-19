# AI-Assisted Test Generation: Bill Pay Negative Cases

This is the one deep example required by blueprint Section 5.6 — real
prompt, real output, real review, not a folder of screenshots.

## Prompt used
> "Suggest negative and edge-case test scenarios for a bill payment form
> with fields: payee name, address (street/city/state/zip), phone,
> account number, verify account number, amount, from-account. Focus on
> realistic business-rule violations, not just empty fields."

## Raw AI output
1. Empty payee name
2. Account number and "verify account number" don't match
3. Amount is zero or negative
4. Amount exceeds the from-account's available balance
5. Non-numeric characters entered in the amount field
6. Invalid zip code format (letters instead of digits)
7. Phone number in an invalid format
8. Extremely long payee name (truncation/buffer behavior)
9. Special characters / SQL-injection-style input in payee name
10. Duplicate payment from rapid double-clicking Submit
11. Payee account number belonging to a different, unrelated customer
12. Submitting with no "from account" selected

## Human review

**Already covered, not duplicated:**
- #1 (empty payee name) — already implemented as
  `test_empty_payee_name_is_rejected`; this whole case is, notably, still
  an open investigation (see `docs/bugs/OBSERVATION-002.md`), not a
  settled result.

**Kept and implemented (see below):**
- #4 (amount exceeds balance) — kept specifically *because* of
  [BUG-002](../docs/bugs/BUG-002.md): Fund Transfer was already found to
  not enforce a balance check. Testing the same business rule on Bill Pay
  is the obvious next question, not a generic idea picked at random.

**Discarded, with a reason — not silently dropped:**
- #11 (payee account belonging to a different customer) — this assumes
  ParaBank validates the payee's account against a real internal
  customer, but Bill Pay's payee account number is an external biller
  reference, not a ParaBank account lookup, based on how the form and
  REST payload are actually structured (see DEC-010). The AI suggested a
  validation relationship that doesn't match how this feature actually
  works.
- #10 (duplicate submission via rapid double-click) — a real and
  reasonable idea, but needs a more involved test setup (simulating
  near-simultaneous clicks and checking for a duplicate transaction) than
  fits a single Phase 5 example. Parked in `future-ideas.md` rather than
  attempted here.

**Reasonable, not pursued yet — parked, not ignored:**
- #2, #3, #5, #6, #7, #8, #9 — all legitimate test ideas. Not implementing
  all twelve suggestions in one pass is deliberate: Section 5.6 asks for
  one deep, well-reasoned example, not maximum coverage from a single AI
  prompt. Logged in `future-ideas.md` for a later phase.

## Final implemented test
`playwright-tests/tests/ui/bill-pay/test_bill_pay.py::test_bill_pay_amount_exceeds_balance`
— directly follows from the #4 decision above. Uses the same absurd-amount
adversarial pattern already established for Transfer (`999999999`).

**Result, confirmed by an actual run:** this is a real finding, not just a
reasonable hypothesis. Bill Pay accepts the oversized amount exactly like
Transfer did — filed as [BUG-003](../docs/bugs/BUG-003.md), now marked
`xfail(strict=False)`. This is the clearest payoff in the whole project
for keeping an AI-suggested idea *because* it connected to an existing
finding, rather than picking from the list at random.
