# Requirement: Bill Pay

## Business Rules (confirmed by an actual run)
- Requires payee name, address (street/city/state/zip), phone, account
  number, a repeated "verify account" number, amount, and a "from" account.
- **Confirmed:** submitting with an empty payee name is rejected —
  `test_empty_payee_name_is_rejected` passed cleanly, no "Bill Payment
  Complete" shown.

## Assumptions to verify empirically
- Exact client-side vs server-side validation behavior for blank fields —
  unconfirmed, same category of unknown as Phase 1's empty-credentials
  case.
- Form field names (`payee.name`, `payee.address.street`, etc.) are a
  reasonable inference from the confirmed REST API's XML payload
  structure and ParaBank's established naming pattern
  (`customer.firstName` on registration), not a live DOM inspection this
  session. See DEC-010 in decision-log.md.

## Out of Scope (for now)
- Recurring/scheduled bill payments (ParaBank's UI doesn't appear to
  support this — not automating a feature that may not exist).
