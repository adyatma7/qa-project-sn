# Requirement: Login

## Business Rules (observed)
- Username and password are both required fields on `/parabank/index.htm`.
- Invalid credentials (wrong password, or a username that doesn't exist)
  return one generic error: "The username and password could not be
  verified." — confirmed the same message either way, so ParaBank does not
  leak whether a username exists. That's actually good security practice,
  worth noting positively rather than assuming every generic error is a bug.

## Assumptions to verify empirically (run Phase 1 tests to confirm)
- Account lockout after N failed attempts — not observed yet. If it doesn't
  exist after real testing, that's a legitimate finding for `docs/bugs/`.
- Empty-field submission behavior — unconfirmed whether it's client-side
  blocked, or silently hits the server and returns the same generic error.
  `test_empty_credentials_are_rejected` in
  `playwright-tests/tests/ui/auth/test_login.py` is designed to surface
  whichever it turns out to be.
- Session timeout duration — unknown until observed.

## Out of Scope (for now)
- Password reset flow ("Forgot login info?") — not automated in Phase 1;
  revisit if a later phase needs it.
- Account lockout enforcement — covered above as an assumption to test,
  not yet a confirmed requirement to automate against.
