# QA Automation Portfolio — ParaBank

[![QA Automation CI](https://github.com/adyatma7/qa-project-sn/actions/workflows/ci.yml/badge.svg)](https://github.com/adyatma7/qa-project-sn/actions/workflows/ci.yml)


> **Status: Phase 0 (foundation).** This README is intentionally incomplete —
> it fills in as each phase closes. See `QA-PORTFOLIO-BLUEPRINT.md` for the
> full plan, roadmap, and the reasoning behind every decision in this repo.

## Overview
_Fill in after Phase 2 — a plain-language summary for non-technical readers._

## Business Goal
_Fill in — see blueprint Section 1._

## Testing Scope
_Fill in — see blueprint Section 1.3 (In Scope) and 1.4 (Out of Scope)._

## Tech Stack
- Playwright + Python (`pytest-playwright`) — primary automation framework
- Selenium + Python — added Phase 4
- GitHub Actions (CI)

## Architecture
_Fill in once the repo structure stabilizes past Phase 2._

## Coverage
_Fill in — see blueprint Section 7._

## How to Run
```bash
cd playwright-tests
python3 -m venv .venv && source .venv/bin/activate
# OR
python -m venv .venv && .venv\Scripts\activate.bat
pip install -r requirements.txt
playwright install --with-deps
pytest
```

## Reports
**Live report:** https://adyatma7.github.io/qa-project-sn/report.html
— updates automatically after every push to `main`, pass or fail.

## Known Bugs
- **[BUG-001](docs/bugs/BUG-001.md) — Critical.** Submitting an incorrect
  password for a valid username (`john`) does not reject the login —
  it authenticates the user anyway, alongside a generic "internal error"
  banner. Reproduced twice, consistently. Regression test exists and is
  marked `xfail(strict=True)` so it won't silently start passing unnoticed.

## Lessons Learned

**Why Python over TypeScript, decided mid-project, not at the start.**
Playwright + TypeScript was the original plan (see `decision-log.md`,
DEC-001). After Phase 0 was already built and passing its own checks,
I realized I could read JavaScript fluently but not write it independently
— versus Python, which I can do both, and already use for a personal ML
project. Caught before Phase 1 existed, so the cost was rewriting five
files, not a mid-project rebuild (DEC-006).

**A URL bug that took down every UI test at once, and how I found the
actual cause instead of guessing.** All three UI tests failed on the exact
same line — a timeout waiting for the username field — which looked at
first like a flaky selector. The real clue was buried in the failure log:
the page had actually loaded `parabank.parasoft.com/index.htm` instead of
`parabank.parasoft.com/parabank/index.htm`. Standard URL-resolution rules
(not a Playwright quirk) mean a `base_url` without a trailing slash,
combined with a `goto()` path that starts with `/`, silently drops the
base path. Fixed by pairing a trailing-slash `base_url` with a
leading-slash-free relative path (DEC-008). The bigger habit this
reinforced: three tests failing with an *identical* stack trace shape is a
signal to look for one shared cause, not three separate bugs.

**An assertion failure that turned out to be a wrong assumption about the
response format, not a wrong endpoint.** The API test asserted on
`response.json()` and got a `JSONDecodeError`. It would have been easy to
assume the endpoint path itself was wrong — instead, the actual response
body was visible right there in the failure output: real customer XML.
The endpoint was correct all along; the fix was parsing XML instead of
JSON (DEC-007). Lesson: read what the failure actually contains before
assuming what kind of bug it is.

**A public shared demo account is not a reliable test fixture, and now I've
seen why first-hand.** `john`/`demo` is ParaBank's own long-standing public
login, used deliberately in Phase 0/1 to keep the smallest test slice
possible. A later run showed the account's displayed name had changed to
something clearly not "John Smith," and an invalid-password attempt
returned a generic server error instead of the expected clean rejection —
consistent with another person's automation script hitting the same shared
account concurrently (see `docs/bugs/OBSERVATION-001.md`). This was a
known, named risk before it happened (DEC-006, blueprint Section 6), not a
surprise — which is exactly the point of writing risks down in advance.
It's also the concrete case for moving negative-path tests to
self-registered, unique-per-run accounts sooner rather than later.

**The adversarial testing tactic paid off for real, on the second try.** The
negative-login test was deliberately written to probe for a real finding
(blueprint Section 7), not just to pad coverage. First run looked like it
might be shared-account flakiness (see `OBSERVATION-001.md`); re-running
it twice more, back to back, showed the identical failure shape with the
account's real name intact, which ruled that out. Confirmed as
[BUG-001](docs/bugs/BUG-001.md): an incorrect password authenticates the
user instead of being rejected. The test wasn't rewritten to match the
buggy behavior — it stays `xfail(strict=True)`, asserting what *should*
happen, so it will loudly fail the build the day the bug gets fixed,
rather than silently staying green forever.

**Not every adversarial test finds a bug, and that's a legitimate result
too.** Phase 2's exploratory cases — an absurdly large transfer amount, an
empty payee name — were written the same way as Phase 1's empty-credentials
test: genuinely not knowing the outcome in advance. Both times, ParaBank
handled it correctly. That's not a wasted test; it's a confirmed, documented
finding ("balance validation works," "required-field validation works") —
see `docs/requirements/transfer.md` and `bill-pay.md`. The discipline is the
same either way: write the adversarial case, run it, record what's actually
true, don't assume the outcome before checking.

**Trade-off, stated plainly:** Chromium only, no load testing, no
white-box access to ParaBank's server code — see Testing Scope above for
the full list and why each is excluded for now rather than silently
missing.


## Future Improvements
_Fill in — see blueprint Section 1.4 (Out of Scope) for the honest list of
what a real production version would need that this doesn't cover._
