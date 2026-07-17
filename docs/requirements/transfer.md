# Requirement: Transfer Funds

## Business Rules (confirmed by an actual run)
- Requires amount, a "from" account, and a "to" account.
- **Confirmed:** ParaBank rejects a transfer request for an absurdly large
  amount (999,999,999) — `test_transfer_exceeding_balance` passed cleanly,
  no "Transfer Complete!" shown. Balance validation appears to work,
  contrary to the commonly-repeated (and now disproven, for this case)
  claim that ParaBank's demo doesn't enforce it.

## Assumptions to verify empirically
- Whether ParaBank actually enforces a sufficient-balance check at all.
  Commonly reported (unconfirmed this session) that ParaBank's demo does
  NOT enforce this. `test_transfer_exceeding_balance` in
  `playwright-tests/tests/ui/transfer/test_transfer.py` is written to
  surface whichever is true — see the test's own comment.
- Whether "from" and "to" can be the same account. The shared demo account
  may only have one account, in which case a "transfer" is effectively
  self-to-self. Test selects by index rather than assuming 2+ accounts
  exist.

## Out of Scope (for now)
- Transfers between two independently-created, freshly registered accounts
  (would require Registration to be in scope first — not yet).
