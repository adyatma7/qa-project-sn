# Requirement: Transfer Funds

## Business Rules (confirmed by an actual run — corrected)
- Requires amount, a "from" account, and a "to" account.
- **Correction:** an earlier version of this file stated balance
  validation was confirmed working. That result came from an assertion
  with a race condition (see DEC-012) — once fixed, a re-run showed the
  transfer of 999,999,999 actually succeeds. **Confirmed: ParaBank does
  NOT enforce a sufficient-balance check on transfers.** See
  [BUG-002](bugs/BUG-002.md).

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
