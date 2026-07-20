# QA Automation Portfolio — ParaBank

[![QA Automation CI](https://github.com/adyatma7/qa-project-sn/actions/workflows/ci.yml/badge.svg)](https://github.com/adyatma7/qa-project-sn/actions/workflows/ci.yml)

> **Status: Phases 0–5 complete.** 17 automated tests across two
> frameworks, 3 confirmed bugs, 1 honestly-documented open investigation.
> This README is the single source of truth for the project — the
> planning document that shaped it is merged in below, not kept as a
> separate, driftable file.

## Overview
This project tests [ParaBank](https://parabank.parasoft.com), a public
banking demo application, using two complementary automation frameworks
(Playwright and Selenium) in Python. It's built to demonstrate the full
QA lifecycle — requirement analysis, risk-based test design, automation,
execution, structured bug reporting, and CI/CD — not just scripts that
happen to run. Along the way it found three real, reproducible bugs in
the application under test, all documented with evidence and reproduction
steps, and one investigation that's still honestly unresolved rather than
forced to a tidy conclusion.

## Business Goal
Build one QA Automation portfolio project — maintained continuously, not
rebuilt from scratch — usable to apply for QA Automation roles both in
Indonesia and remote/global, while deepening automation skills and
English communication in parallel with the job search itself.

**Objectives:**
- Demonstrate hands-on Playwright competency (primary) and Selenium
  competency (secondary) — not tutorial-following
- Demonstrate the full QA lifecycle in practice: requirement analysis →
  risk-based test design → automation → execution → reporting → bug
  tracking → regression
- Demonstrate API testing, SQL/data validation reasoning, CI/CD
  integration, and structured bug reporting
- Demonstrate deliberate, reviewed use of AI-assisted testing — not just
  "I used AI"
- Produce documentation that works for two different readers in the same
  repo: a non-technical recruiter skimming for 30 seconds, and a
  technical interviewer going deep

## Testing Scope

**In scope:**
- UI automation on ParaBank: Playwright (full coverage), Selenium (6
  critical-path tests)
- REST API automation: functional, contract, negative
- SQL-based data validation (local SQLite simulation)
- CI/CD pipeline via GitHub Actions, with a public live report
- Structured, honestly-sourced bug reports from real exploratory testing
- Requirement analysis, risk analysis, and requirement-to-test
  traceability
- One deeply-documented AI-assisted test generation example

**Out of scope, and why:**

| Excluded | Why |
|---|---|
| Load/performance testing at scale | Not a core deliverable — named as a known gap, not silently skipped. |
| Security penetration testing | Basic adversarial input only, not a formal security audit. |
| Native mobile app testing | ParaBank has no mobile app to target. |
| Full cross-browser matrix | Chromium only. A real production project would need this — naming the trade-off is more credible than pretending it's covered. |
| White-box / source-code testing | Black-box only — no access to ParaBank's server code. |
| Production monitoring/observability | Out of scope for a portfolio project by definition. |
| Full visual regression suite | Not attempted; noted as a possible future addition. |

## Tech Stack
- Playwright + Python (`pytest-playwright`) — primary automation
  framework
- Selenium + Python — secondary, cross-validation framework
- SQLite — local data-validation simulation
- GitHub Actions — CI/CD, with GitHub Pages publishing live reports

## Repository Structure
```
qa-portfolio/
├── README.md                    # you are here — project overview + planning reference
├── docs/
│   ├── requirements/             # per-feature requirement notes (login, transfer, bill-pay)
│   ├── test-plan.md               # scope, environment, entry/exit criteria
│   ├── test-strategy.md           # test pyramid, coverage shape, bug-hunting process
│   ├── risk-analysis.md           # why effort isn't spread evenly across features
│   ├── traceability-matrix.md     # requirement → test case → bug, single source of truth
│   ├── decision-log.md            # 17 real decisions, made and revised as they happened
│   └── bugs/                      # BUG-001/002/003, plus 2 investigation write-ups
├── learning-notes/                 # line-by-line explainers, mirrors the test suites
├── playwright-tests/                # primary suite — see its own README
├── selenium-tests/                  # secondary suite — see its own README
├── db-validation/                    # SQLite simulation — see its own README
├── ai-assisted-testing/               # 1 real, reviewed AI-assisted example
├── future-ideas.md                     # parking lot, not scope creep
└── .github/workflows/ci.yml             # 3 jobs: playwright-tests, selenium-tests, deploy-report
```

## Skill-to-Job-Market Traceability
Every tool in this project maps to demonstrated demand from real job
listing data collected before starting, not personal preference:

| Skill (from job market data) | Covered by |
|---|---|
| Selenium (35 local listings) | `selenium-tests/` |
| Playwright (32 local, dominant global) | `playwright-tests/` |
| API testing / Postman (32 local, 102 mentions of "API") | `playwright-tests/tests/api/` |
| SQL (37 local) | `db-validation/` |
| GitHub Actions CI/CD (6 local, standard global) | `.github/workflows/` |
| SDLC & Agile (57 local — highest signal) | `docs/test-plan.md`, `docs/risk-analysis.md` |
| AI-assisted testing (emerging global trend) | `ai-assisted-testing/` |
| Domain: banking/insurance (dominant local) | Target app choice (ParaBank) |
| English communication | All docs and code comments in English |
| Python (17 local mentions) | Primary language for both frameworks |

## Coverage
**17 automated tests, across 3 tools:**

| Suite | Tests | What's covered |
|---|---|---|
| Playwright | 9 | Login (positive/negative/adversarial), Transfer, Bill Pay, 1 API test |
| Selenium | 6 | Login, Transfer, Bill Pay — risk-based subset, not a full mirror |
| DB validation | 2 | Balance reconciliation logic (positive case + deliberately-broken case) |

Full requirement-to-test mapping: [`docs/traceability-matrix.md`](docs/traceability-matrix.md).
Why coverage isn't spread evenly: [`docs/risk-analysis.md`](docs/risk-analysis.md).

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
[`selenium-tests/README.md`](selenium-tests/README.md)):
```powershell
cd selenium-tests
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pytest -v
```
Requires a real Chrome installation locally (CI doesn't need this step —
`ubuntu-latest` runners ship with Chrome already).

**DB validation** (fully offline, no ParaBank access needed — see
[`db-validation/README.md`](db-validation/README.md)):
```bash
cd db-validation
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pytest -v
```

## Reports
**Live, updated automatically after every push to `main`, pass or fail:**
- Index: https://adyatma7.github.io/qa-project-sn/
- Playwright report: https://adyatma7.github.io/qa-project-sn/playwright/report.html
- Selenium report: https://adyatma7.github.io/qa-project-sn/selenium/report.html

Kept as two separate report pages rather than merged into one — the two
suites are deliberately independent tools, and their results are more
useful reviewed that way.

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
  999,999,999 completes successfully. Confirmed in both Playwright and
  Selenium. `xfail(strict=False)` in both suites.
- **[BUG-003](docs/bugs/BUG-003.md) — High.** Bill Pay has the same gap
  as BUG-002 — an oversized payment amount is accepted. Likely shares a
  root cause with BUG-002 rather than being a coincidence. Found via a
  documented AI-assisted testing exercise. `xfail(strict=False)`.
- **Under investigation:** [OBSERVATION-002](docs/bugs/OBSERVATION-002.md)
  — whether Bill Pay accepts an empty payee name. Playwright consistently
  says rejected; Selenium consistently says accepted, confirmed across 3
  environments. Root cause still unresolved — may be a Selenium/WebDriver
  limitation rather than a ParaBank bug. Marked `xfail(strict=False)` so
  CI reflects "known, tracked" rather than an untriaged failure.

## Lessons Learned

**Why Python over TypeScript, decided mid-project, not at the start.**
Playwright + TypeScript was the original plan. After Phase 0 was already
built and passing its own checks, I realized I could read JavaScript
fluently but not write it independently — versus Python, which I can do
both, and already use for a personal ML project. Caught before Phase 1
existed, so the cost was rewriting five files, not a mid-project rebuild.

**A URL bug that took down every UI test at once, and how I found the
actual cause instead of guessing.** All three UI tests failed on the exact
same line — a timeout waiting for the username field — which looked at
first like a flaky selector. The real clue was buried in the failure log:
the page had actually loaded `parabank.parasoft.com/index.htm` instead of
`parabank.parasoft.com/parabank/index.htm`. Standard URL-resolution rules
(not a Playwright quirk) mean a `base_url` without a trailing slash,
combined with a `goto()` path that starts with `/`, silently drops the
base path. The bigger habit this reinforced: three tests failing with an
*identical* stack trace shape is a signal to look for one shared cause,
not three separate bugs.

**An assertion failure that turned out to be a wrong assumption about the
response format, not a wrong endpoint.** The API test asserted on
`response.json()` and got a `JSONDecodeError`. It would have been easy to
assume the endpoint path itself was wrong — instead, the actual response
body was visible right there in the failure output: real customer XML.
The endpoint was correct all along; the fix was parsing XML instead of
JSON. Lesson: read what the failure actually contains before assuming
what kind of bug it is.

**A public shared demo account is not a reliable test fixture, and now
I've seen why first-hand.** `john`/`demo` is ParaBank's own long-standing
public login, used deliberately to keep the smallest test slice possible.
A run showed the account's displayed name had changed to something
clearly not "John Smith," consistent with another person's automation
script hitting the same shared account concurrently. This was a known,
named risk before it happened, not a surprise — which is the point of
writing risks down in advance.

**Cross-tool testing caught a bug that single-tool testing missed
entirely.** Porting 6 tests to Selenium wasn't just about proving
Selenium competency — it directly found a real problem: the Playwright
suite's negative assertion checked for a success heading immediately
after form submission, which could report "not visible" a moment before a
delayed success page actually rendered — a false pass, not a real
rejection. The Selenium port happened to include a short wait before
checking (for an unrelated reason) and caught the truth. A test passing
is not the same claim as a test being correct.

**A bug can be real and still not be deterministic — and the test
strategy should say so honestly.** BUG-001 reproduced 2 out of 2 times in
Playwright, then didn't reproduce at all on the first Selenium attempt.
Both regression tests were downgraded from `xfail(strict=True)` to
`strict=False` — an intermittent bug deserves a marker that won't break
the build on a legitimate pass, which is a different (and more honest)
claim than "this always fails."

**The adversarial testing tactic paid off for real, more than once.**
Negative-path tests were deliberately written to probe for real findings,
not just pad coverage. The invalid-password test confirmed BUG-001; the
Transfer/Bill Pay oversized-amount tests confirmed BUG-002 and BUG-003;
the empty-field tests on Login worked correctly, which is also a
legitimate, documented result, not a wasted test. The discipline is the
same either way: write the case, run it, record what's actually true,
don't assume the outcome before checking.

**A cross-tool disagreement can itself be the finding — and knowing when
to stop investigating is also a real skill.** The empty-payee-name
question went through two rounds of hypothesis-and-test: shared-account
balance depletion (ruled out), then a theory about Selenium's
`send_keys("")` not firing the same events as Playwright's `.fill("")`
(also ruled out by an explicit experiment). Confirmed consistent across
three environments, with the actual root cause still unknown. Rather than
keep chasing it, it's marked `xfail(strict=False)` and documented
honestly as unresolved — continuing to dig into a secondary,
un-confirmed discrepancy has diminishing returns once three solid,
cross-tool-confirmed bugs already came out of the same general effort.

**A wrong hypothesis, checked and corrected, is a normal part of the
process — not a failure to hide.** Two previously-reliable tests started
timing out in CI. First guess: the shared account's balance had gone
extreme from the confirmed no-balance-check bugs. A manual check showed
that guess was wrong — no extreme numbers — but revealed something more
interesting instead: the shared `john` login now has 14 separate
accounts, almost certainly accumulated from years of other people's
testing against the same long-standing public demo account, with 2 of
them sitting at a negative balance. The real explanation for the timeouts
was more mundane: rendering a 14-account dropdown takes longer than the
original fixed wait allowed for. The shared-account risk named back at
the start of this project (DEC-006) stopped being a hypothetical the
moment there were literally 14 accounts to prove it.

## Future Improvements
A real production version of this project would need, in rough priority
order:
1. Move Login's negative-path tests off the shared `john`/`demo` account
   onto self-registered, unique-per-run accounts (`test_data_generator.py`
   already exists for this, just not wired in yet)
2. Resolve OBSERVATION-002's root cause, or accept and document it as a
   permanent, understood tooling limitation
3. Full cross-browser coverage, not just Chromium
4. Self-hosted ParaBank via Docker for genuine DB-level validation
   (currently a local SQLite simulation)
5. Allure reporting for trend history across runs, visual regression,
   accessibility checks

Full, unfiltered parking lot of smaller ideas: [`future-ideas.md`](future-ideas.md).

---

<details>
<summary><b>📘 Full Planning Methodology & Interview Reference</b> — click to expand</summary>

This section is what was originally a separate `QA-PORTFOLIO-BLUEPRINT.md`
planning document, merged here once execution caught up to planning. Kept
collapsed by default so the project reads cleanly at a glance; expand for
the full reasoning behind how this project is structured.

### Anti-Scope-Creep Discipline
Given a known personal pattern of broad exploration without finishing —
this was the actual safeguard used throughout, more important than any
single tool choice:
1. No new folder or tool got created until the current phase's
   Definition of Done was checked off.
2. An idea for something not already planned went into `future-ideas.md`,
   not into the code.
3. One passing, documented, boring test beats three half-finished
   ambitious ones.
4. The plan itself didn't get revised without genuinely new information
   — the one real exception (the Python-over-TypeScript pivot) happened
   because of a real, concrete fact (actual skill depth), not a fresh
   doubt, and it was caught while the cost was still one afternoon.

### Phase-by-Phase Status
| Phase | Scope | Status |
|---|---|---|
| 0 | Repo scaffold, first passing test, CI green | ✅ Done |
| 1 | Auth module, first real bug hunted (BUG-001) | ✅ Done |
| 2 | Transfer + Bill Pay, same coverage pattern | ✅ Done — *(MVP line: sufficient to start applying from here)* |
| 3 | HTML report wired into CI, public live link | ✅ Done |
| 4 | Selenium: 6 cross-validated tests, differentiation notes | ✅ Done |
| 5 | AI-assisted example, DB validation, learning-notes backfill | ✅ Done |
| 6 *(optional stretch)* | Docker self-host, Allure, visual regression, accessibility, k6 | Not started — see Future Improvements |

### Interview Cheat-Sheet
Know where every likely question is answered before walking in:

| Likely Question | Where the Answer Lives |
|---|---|
| Why Playwright over Selenium/Cypress? | `docs/decision-log.md` → DEC-001 |
| Why Python over JavaScript/TypeScript? | DEC-006 |
| Walk me through a bug you found | `docs/bugs/BUG-001.md`, `BUG-002.md`, or `BUG-003.md` |
| How do you handle test data / independence? | `playwright-tests/utils/test_data_generator.py` |
| Why only 6 Selenium tests, not a full port? | DEC-002, `selenium-tests/README.md` |
| How would you validate the database here? | DEC-003, `db-validation/README.md` |
| Why isn't coverage even across all features? | `docs/risk-analysis.md` |
| How did you actually use AI in this project? | `ai-assisted-testing/bill-pay-negative-cases.md` — led directly to BUG-003 |
| Tell me about a test that passed but shouldn't have | DEC-012 — a race condition hid BUG-002 for a while |
| Tell me about cross-tool testing catching something | Lessons Learned above — the Selenium port found BUG-002 |
| What do you do when two tools disagree with each other? | OBSERVATION-002 — two hypotheses tested and disproven, documented as unresolved rather than forced |
| How do you handle an intermittent bug in your test suite? | BUG-001 — `xfail(strict=False)` instead of `strict=True` |
| Walk me through your CI/CD setup | `.github/workflows/ci.yml` — 3 jobs, GitHub Pages deployment |
| What would you do differently in a real production app? | Future Improvements, above |

### Retrospective — did the plan hold up?
Broadly, yes. The repository structure never needed restructuring, only
additions — every new folder was added when its phase actually needed it,
never earlier. The one real pivot (Python over TypeScript) happened
because of genuinely new information, was caught while the cost was still
one afternoon, and is a permanent, honest entry in the decision log
instead of a silently erased mistake. Three genuine, reproducible bugs
were found through deliberate adversarial testing, not simulated for the
sake of having content — and one investigation was left honestly
unresolved rather than forced to a tidy conclusion, which is itself a
demonstration of the same discipline: knowing when continuing to dig has
diminishing returns is as real a skill as the digging itself.

### Where the living detail actually lives
This README summarizes; these files are the current, continuously-updated
source of truth behind every claim above:
- [`docs/decision-log.md`](docs/decision-log.md) — 17 real decisions, made and revised as they happened
- [`docs/traceability-matrix.md`](docs/traceability-matrix.md) — requirement → test → bug mapping
- [`docs/risk-analysis.md`](docs/risk-analysis.md) — why effort isn't spread evenly
- [`docs/test-plan.md`](docs/test-plan.md) / [`docs/test-strategy.md`](docs/test-strategy.md) — scope and approach in full
- [`docs/bugs/`](docs/bugs/) — every bug and investigation, full detail

</details>
