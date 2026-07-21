# OBSERVATION-003 (not yet a confirmed bug — needs reproduction check)

**Found:** CI run, 2026-07-2x — `test_valid_login_returns_customer_via_api`
(Playwright) failed with a 400: `Invalid username and/or password`, in
the **same CI run** where `test_valid_login_reaches_accounts_overview`
(UI login, identical credentials `john`/`demo`) **passed**.

## Why this is a genuinely interesting asymmetry
Same account, same password, same approximate moment — one
authentication path (browser form login) accepted it, the other (REST
API endpoint) rejected it. This has never happened before in this
project; every prior run had the API endpoint working correctly (it's
how the real customer XML record was first confirmed back in Phase 1).

## Competing explanations
1. **Genuinely different code paths with different validation logic** —
   the REST login service and the UI login form may not share the same
   underlying authentication check, and could have drifted out of sync
   for this account specifically (maybe interacting badly with BUG-001's
   already-confirmed intermittent auth weirdness on the UI side).
2. **A transient server-side hiccup specific to the API layer** at the
   moment this ran — consistent with the same general window where
   Selenium's Bill Pay test also failed 3 times in a row despite retries
   (see `docs/decision-log.md` DEC-021). If ParaBank's server was having
   a rough patch generally, an API-specific timeout/error surfacing as a
   clean 400 rather than a connection error is plausible.

## Before filing as a bug
Re-run `pytest tests/api/auth/test_login_api.py -v` on its own a few
times. Consistent 400 → a real, reproducible auth-path inconsistency,
worth filing formally. Passes cleanly again → most likely explanation 2,
note it as resolved/transient rather than filing.

## Not chasing this indefinitely
Given the volume of intermittent, hard-to-pin-down issues accumulating
against this specific shared public demo account recently (BUG-001's
intermittency, Selenium's persistent-through-retries flakiness, and now
this), it's worth naming directly: at some point, "the third-party demo
occasionally has a rough window, out of this project's control" becomes
the more honest conclusion than continuing to hunt for a root cause in
our own code. This entry exists to track the finding, not to promise
it'll be fully resolved.

---

## RESOLVED — confirmed, promoted to BUG-004

Re-ran the API call, then immediately ran the UI login test with the
identical credentials in the same session: API rejected (400, same
message as before), UI login passed cleanly. Second confirmation of the
exact asymmetry, close together in time — ruling out "the account's
password quietly changed" as the explanation (that would have broken UI
login too). See `BUG-004.md` for the full write-up.
