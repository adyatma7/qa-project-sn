# Traceability Matrix

| Req ID    | Requirement                          | Test Case ID  | Automated?         | Bug Found |
|-----------|----------------------------------------|----------------|----------------------|-----------|
| LOGIN-01  | Valid login reaches Accounts Overview | TC-AUTH-001    | ✅ `test_valid_login_reaches_accounts_overview` | - |
| LOGIN-02  | Invalid password shows generic error  | TC-AUTH-002    | ✅ `test_invalid_password_shows_error` (marked `xfail` — see BUG-001) | **BUG-001** |
| LOGIN-03  | Empty credentials are rejected        | TC-AUTH-003    | ✅ `test_empty_credentials_are_rejected` | TBD — run and update |
| LOGIN-04  | Valid login returns customer via API  | TC-AUTH-004    | ✅ `test_valid_login_returns_customer_via_api` | - (confirmed correct, see DEC-007) |
| XFER-01   | Valid transfer completes              | TC-XFER-001    | ✅ `test_valid_transfer_completes` | - |
| XFER-02   | Transfer exceeding balance rejected   | TC-XFER-002    | ✅ `test_transfer_exceeding_balance` | - (confirmed enforced, no bug) |
| BILL-01   | Valid bill payment completes          | TC-BILL-001    | ✅ `test_valid_bill_payment_completes` | - (selectors confirmed, DEC-010) |
| BILL-02   | Empty payee name is rejected          | TC-BILL-002    | ✅ `test_empty_payee_name_is_rejected` | - (confirmed enforced, no bug) |

Detailed step-by-step test cases (preconditions, exact steps, expected
result) live in Jira, not here — see DEC-005. This file only tracks the
ID-level mapping, so it stays small and never goes stale.
