# Traceability Matrix

| Req ID    | Requirement                          | Test Case ID  | Automated?         | Bug Found |
|-----------|----------------------------------------|----------------|----------------------|-----------|
| LOGIN-01  | Valid login reaches Accounts Overview | TC-AUTH-001    | ✅ `test_valid_login_reaches_accounts_overview` | - |
| LOGIN-02  | Invalid password shows generic error  | TC-AUTH-002    | ✅ `test_invalid_password_shows_error` (marked `xfail` — see BUG-001) | **BUG-001** |
| LOGIN-03  | Empty credentials are rejected        | TC-AUTH-003    | ✅ `test_empty_credentials_are_rejected` | TBD — run and update |
| LOGIN-04  | Valid login returns customer via API  | TC-AUTH-004    | ✅ `test_valid_login_returns_customer_via_api` (`xfail`) | **BUG-004** |
| XFER-01   | Valid transfer completes              | TC-XFER-001    | ✅ `test_valid_transfer_completes` | - |
| XFER-02   | Transfer exceeding balance rejected   | TC-XFER-002    | ✅ `test_transfer_exceeding_balance` (`xfail`, both frameworks) | **BUG-002**, cross-tool confirmed |
| BILL-01   | Valid bill payment completes          | TC-BILL-001    | ✅ `test_valid_bill_payment_completes` | - (selectors confirmed, DEC-010) |
| BILL-02   | Empty payee name is rejected          | TC-BILL-002    | ✅ `test_empty_payee_name_is_rejected` | ⚠️ **conflicting, consistently** — Playwright 2/2 rejected, Selenium 3/3 accepted. Likely a Selenium `send_keys("")` event-dispatch gap, not a ParaBank bug — see OBSERVATION-002 for the experiment to confirm. |
| BILL-03   | Bill Pay amount exceeds balance       | TC-BILL-003    | ✅ `test_bill_pay_amount_exceeds_balance` (`xfail`) | **BUG-003** |

Detailed step-by-step test cases (preconditions, exact steps, expected
result) live in Jira, not here — see DEC-005. This file only tracks the
ID-level mapping, so it stays small and never goes stale.

## Cross-tool validation (Phase 4)
6 of the above (LOGIN-01, LOGIN-02, XFER-01, XFER-02, BILL-01, BILL-02)
are also automated in `selenium-tests/`, not to double coverage but to
cross-validate — most notably, LOGIN-02 / BUG-001 reproducing identically
via a second, completely independent tool. See `selenium-tests/README.md`
for exactly which cases and why.
