# Selenium Tests — Differentiation Notes

6 critical-path tests ported from the Playwright suite, not a full mirror.
Reasoning: `docs/decision-log.md` DEC-002.

## Why these specific 6 (not all 8)
Risk-based, following `docs/risk-analysis.md`:
- **Login (2 tests)** — the gateway everything else depends on.
  `test_invalid_password_shows_error` is included specifically to confirm
  BUG-001 reproduces via a completely different tool/driver, ruling out a
  Playwright-specific quirk as the explanation.
- **Transfer (2 tests) + Bill Pay (2 tests)** — both High risk (move real
  money) per `risk-analysis.md`, get full positive/negative coverage.
- **Not ported:** `test_empty_credentials_are_rejected` (redundant signal
  with the invalid-password case) and the API login test (Selenium drives
  browsers — it isn't the idiomatic tool for API testing; Playwright's
  request context already covers that ground).

## Technical differences from the Playwright suite, on purpose

### Explicit waits everywhere, no auto-wait
Playwright's `.fill()`/`.click()` wait for the element automatically.
Selenium's `find_element()` does not — every interaction here is preceded
by an explicit `WebDriverWait(...).until(...)`. Compare
`selenium-tests/pages/login_page.py` directly against
`playwright-tests/pages/login_page.py` — same login flow, written both
ways.

### Manual screenshot-on-failure
Playwright's config does this in one line
(`screenshot: 'only-on-failure'`). Selenium has no built-in equivalent —
`conftest.py` here implements it manually via a
`pytest_runtest_makereport` hook.

### No baseURL mechanism
`pytest-playwright` has `--base-url` built in. Selenium has nothing
equivalent — `config.py`'s `url_for()` is the manual substitute, written
with a trailing slash from the start because of the base_url bug already
found and fixed in the Playwright suite (DEC-008). Same lesson, applied
here proactively instead of being re-discovered the hard way twice.

### No clean "assert absence" primitive
Playwright's `not_to_be_visible()` polls automatically until an element
is confirmed gone. Selenium has no exact equivalent for "wait and confirm
this never appears" — `expect_not_completed()` in the page objects here
falls back to a fixed `time.sleep()`, which is slower and less robust.
Worth raising unprompted in an interview: this is a genuine limitation of
vanilla Selenium, not a gap in this code specifically.

### Isolated dependencies
This folder has its own `requirements.txt` and its own virtual
environment, deliberately separate from `playwright-tests/`, to avoid any
version conflict between the two frameworks' dependency trees.

## How to run
```bash
cd selenium-tests
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pytest -v
```
Requires a real Chrome installation locally. `webdriver-manager` handles
downloading a matching ChromeDriver automatically — it does not install
Chrome itself.
