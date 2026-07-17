# Decision Log

One entry per real decision, written when made, not backfilled. Entries get
appended and superseded, never silently rewritten.

## DEC-001: Playwright as Primary Framework
**Options considered:** Playwright, Cypress, Selenium
**Chosen:** Playwright
**Reasoning:** Auto-wait removes most flaky-test causes without manual wait
logic; built-in API testing means no separate Postman/RestAssured dependency;
parallel execution out of the box.
**Trade-off accepted:** Smaller cross-browser edge-case community than
Selenium — mitigated by keeping Selenium as a secondary framework for
critical paths.
**Superseded in part by DEC-006** (language, not framework, changed).

## DEC-002: Only 5-8 Selenium Test Cases, Not a Full Port
**Reasoning:** Risk-based prioritization (see risk-analysis.md) — port only
the highest-impact flows (login, transfer), not the full suite.
**Trade-off accepted:** Lower raw "Selenium coverage number," in exchange for
demonstrating prioritization instead of checkbox-ticking.

## DEC-003: SQLite Simulation Instead of Live DB Connection
**Reasoning:** ParaBank's public demo doesn't expose its database externally.
Claiming live DB validation without real access would be dishonest.
**Chosen approach:** Local SQLite schema mirroring ParaBank's data model,
used to validate API response consistency.
**Optional stretch:** Self-host ParaBank's official Docker image (embedded
HyperSQL DB) for genuine DB-level validation — Phase 6, not required for MVP.

## DEC-004: Line-by-Line Comments Live in learning-notes/, Not in Test Files
**Reasoning:** Production-style test code should be self-documenting; full
line-by-line explanation is a genuinely useful personal learning aid, but a
different audience than a code reviewer.
**Resolution:** learning-notes/ mirrors the test folder structure 1:1 and
holds the verbose explainer version. Test files stay clean.

## DEC-005: Jira Is the Single Source of Truth for Test Cases
**Reasoning:** Maintaining detailed test cases in both Jira and markdown
would drift out of sync within weeks. Jira is also the actual tool the job
market asks about.
**Resolution:** docs/traceability-matrix.md only stores ID-level mapping.

## DEC-006: Switched Primary Language from TypeScript to Python (post-Phase-0)
**Context:** DEC-001 originally paired Playwright with TypeScript. After
Phase 0 was already built and verified, new information changed the
calculus: Python is understood deeply enough to read AND write
independently; JavaScript is read fluently but written mostly AI-assisted.
**Reasoning:** The point of this project is real, defensible skill — not
just code that runs. Consolidating to one language across this project and
a personal ML side project also removes constant context-switching cost.
**Trade-off accepted:** JavaScript is marginally more frequent in the local
job market; Python + Playwright/Selenium are both mature, well-documented
combinations regardless.
**Cost of the pivot:** Caught early, before Phase 1 existed — only Phase 0's
five files needed rewriting.

## DEC-007: API Login Endpoint — Confirmed Correct, Response Format Fixed
**Original context:** `test_login_api.py` used
`/services/bank/login/{username}/{password}` without independent
verification against ParaBank's Swagger docs.
**Update, confirmed by an actual run against the live site:** the endpoint
is correct — it returns a real customer record (id 12212, John Smith,
Beverly Hills CA 90210). The test originally failed anyway, because it
called `response.json()` and the endpoint returns **XML by default**, not
JSON — `JSONDecodeError: Expecting value: line 1 column 1`.
**Fix:** parse with `xml.etree.ElementTree` instead of `.json()`.
**Resolution:** endpoint path confirmed correct and no longer flagged as
unverified. This is exactly what a decision log is for — the entry got
updated with real evidence instead of silently deleted.

## DEC-008: Fixed base_url Path Resolution Dropping "/parabank"
**Found by:** running the suite for real — all three Phase 1 UI tests
timed out waiting for the username field, and the failure log showed the
actual page URL as `https://parabank.parasoft.com/index.htm` instead of
`.../parabank/index.htm`.
**Root cause:** standard URL-resolution behavior (not a ParaBank bug, not
a Playwright bug) — when `base_url` doesn't end in `/` and the relative
path passed to `goto()` starts with `/`, the leading slash makes the path
absolute from the domain root, discarding the base URL's own path segment
(`/parabank`).
**Fix:** `base_url` now ends in `/parabank/` (trailing slash), and
`LoginPage.goto()` now calls `self.page.goto("index.htm")` with no leading
slash, so it correctly appends instead of resetting.
**Why this matters beyond the fix itself:** every UI test in Phase 1 failed
for this one shared reason, not three separate problems — worth checking
for a single root cause across similar failures before debugging each test
individually.
