# Traceability Matrix

| Req ID    | Requirement                          | Test Case ID  | Automated?         | Bug Found |
|-----------|----------------------------------------|----------------|----------------------|-----------|
| LOGIN-01  | Valid login reaches Accounts Overview | TC-AUTH-001    | ✅ `test_valid_login_reaches_accounts_overview` | - |
| LOGIN-02  | Invalid password shows generic error  | TC-AUTH-002    | ✅ `test_invalid_password_shows_error` (marked `xfail` — see BUG-001) | **BUG-001** |
| LOGIN-03  | Empty credentials are rejected        | TC-AUTH-003    | ✅ `test_empty_credentials_are_rejected` | TBD — run and update |
| LOGIN-04  | Valid login returns customer via API  | TC-AUTH-004    | ✅ `test_valid_login_returns_customer_via_api` | TBD — endpoint unverified, see test docstring |

Detailed step-by-step test cases (preconditions, exact steps, expected
result) live in Jira, not here — see DEC-005. This file only tracks the
ID-level mapping, so it stays small and never goes stale.
