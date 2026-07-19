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

**Playwright suite:**
```bash
# macOS/Linux
cd playwright-tests
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
playwright install --with-deps
pytest -v
```
```powershell
# Windows PowerShell
cd playwright-tests
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
playwright install --with-deps
pytest -v
```

**Selenium suite** (separate, isolated environment — see
`selenium-tests/README.md`):
```powershell
# Windows PowerShell
cd selenium-tests
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pytest -v
```
Requires a real Chrome installation locally (CI doesn't need this step —
`ubuntu-latest` runners ship with Chrome already).

## Reports
**Live report:** https://adyatma7.github.io/qa-project-sn/report.html
— updates automatically after every push to `main`, pass or fail.

## Known Bugs
- **[BUG-001](docs/bugs/BUG-001.md) — Critical, intermittent.** Submitting
  an incorrect password for a valid username (`john`) sometimes
  authenticates the user anyway, alongside a generic "internal error"
  banner, instead of being rejected. Reproduced 2/2 in Playwright; did
  not reproduce in a Selenium cross-check, so treated as intermittent
  rather than deterministic. Regression tests in both frameworks are
  marked `xfail(strict=False)` accordingly.
- **[BUG-002](docs/bugs/BUG-002.md) — High, cross-tool confirmed.** Fund
  Transfer does not enforce a sufficient-balance check — a transfer of
  999,999,999 completes successfully. Confirmed in both Playwright (2/2)
  and Selenium. `xfail(strict=False)` in both suites.
- **[BUG-003](docs/bugs/BUG-003.md) — High.** Bill Pay has the same gap
  as BUG-002 — an oversized payment amount is accepted. Likely shares a
  root cause with BUG-002 rather than being a coincidence (see DEC-017).
  Found via a documented AI-assisted testing exercise. `xfail(strict=False)`.
- **Under investigation:** [OBSERVATION-002](docs/bugs/OBSERVATION-002.md)
  — whether Bill Pay accepts an empty payee name. Playwright (2/2) says
  rejected; Selenium (3/3) says accepted — each tool is internally
  consistent, which points away from random flakiness and toward
  `send_keys("")` in Selenium not triggering the same form events as
  Playwright's `.fill("")`. A concrete experiment is written up to settle
  it either way; not filed as a bug yet because it may turn out to be a
  gap in how the Selenium test simulates a real user, not a ParaBank bug.

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

**Cross-tool testing caught a bug that single-tool testing missed
entirely.** Porting 6 tests to Selenium (Phase 4) wasn't just about
proving Selenium competency — it directly found a real problem: the
Playwright suite's `expect_not_completed()` checked for a success heading
immediately after form submission, which could report "not visible" a
moment before a delayed success page actually rendered — a false pass,
not a real rejection. The Selenium port happened to include a short wait
before checking (for an unrelated reason) and caught "Bill Payment
Complete" actually appearing where Playwright had reported success at
rejecting it. Two features (`XFER-02`, `BILL-02`) that were marked
"confirmed, no bug" in the traceability matrix had to be reopened for
re-verification once the race condition was fixed in both frameworks. The
lesson generalizes past this one bug: a test passing is not the same
claim as a test being correct, and a second tool built differently is one
of the more reliable ways to catch that gap.

**A bug can be real and still not be deterministic — and the test
strategy should say so honestly.** BUG-001 reproduced 2 out of 2 times in
Playwright, then didn't reproduce at all on the first Selenium attempt.
Rather than treat that as disproving the bug, both regression tests were
downgraded from `xfail(strict=True)` to `strict=False` — an intermittent
bug deserves a marker that won't break the build on a legitimate pass,
which is a different (and more honest) claim than "this always fails."

**The adversarial testing tactic paid off for real, on the second try.** The
negative-login test was deliberately written to probe for a real finding
(blueprint Section 7), not just to pad coverage. First run looked like it
might be shared-account flakiness (see `OBSERVATION-001.md`); re-running
it twice more, back to back, showed the identical failure shape with the
account's real name intact, which ruled that out. Confirmed as
[BUG-001](docs/bugs/BUG-001.md): an incorrect password authenticates the
user instead of being rejected. The test wasn't rewritten to match the
buggy behavior — it stays `xfail`, asserting what *should* happen, so it
keeps failing loudly rather than silently going green forever.

**Not every adversarial test finds a bug, and that's a legitimate result
too.** Phase 2's exploratory cases — an absurdly large transfer amount, an
empty payee name — were written the same way as Phase 1's empty-credentials
test: genuinely not knowing the outcome in advance. Both times, ParaBank
handled it correctly. That's not a wasted test; it's a confirmed, documented
finding ("balance validation works," "required-field validation works") —
see `docs/requirements/transfer.md` and `bill-pay.md`. The discipline is the
same either way: write the adversarial case, run it, record what's actually
true, don't assume the outcome before checking.

**Fixing a false-negative assertion immediately surfaced a real,
previously-hidden bug.** The race-condition fix (above) wasn't just a
theoretical correction — re-running Transfer's adversarial test with it
confirmed [BUG-002](docs/bugs/BUG-002.md): a transfer of 999,999,999
actually completes, no balance check enforced. The earlier "pass" on
this exact test had been masking that the whole time. This is the
clearest evidence in the whole project that a green test is not the same
claim as a correct one.

**A cross-tool disagreement can itself be the finding — and ruling out
the wrong explanation matters as much as finding the right one.** The
empty-payee-name question ([OBSERVATION-002](docs/bugs/OBSERVATION-002.md))
first looked like shared-account flakiness. But re-running both suites
showed each tool was internally *consistent* with itself (Playwright 2/2
one way, Selenium 3/3 the other) — which argues against shared, randomly
fluctuating state like account balance, and toward something
deterministic about how each tool interacts with the page. Current best
explanation: Selenium's `send_keys("")` sends zero keystrokes and never
fires the input/blur events that Playwright's `.fill("")` fires even for
an empty value — meaning the Selenium test may not be exercising the app
the way an actual user would. If that holds up, this was never a
ParaBank bug at all; it was a gap in how faithfully one test simulated
real interaction. A concrete experiment is written up to settle it either
way, rather than guessing and moving on.

**Trade-off, stated plainly:** Chromium only, no load testing, no
white-box access to ParaBank's server code — see Testing Scope above for
the full list and why each is excluded for now rather than silently
missing.


## Future Improvements
_Fill in — see blueprint Section 1.4 (Out of Scope) for the honest list of
what a real production version would need that this doesn't cover._
