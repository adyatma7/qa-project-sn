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

## DEC-010: Transfer/Bill Pay Selectors Used With Partial Confidence
**Context:** Phase 2 needed form field selectors for `transfer.htm` and
`billpay.htm` without direct live-DOM access this session.
**What's confirmed:** Transfer's field names (`fromAccountId`,
`toAccountId`, `amount`) are confirmed against ParaBank's own REST service
source code (github.com/parasoft/parabank). Bill Pay's field name pattern
(`payee.name`, `payee.address.street`, etc.) is inferred from the
confirmed REST API's XML payload structure plus the established
`customer.firstName`-style naming pattern already proven correct on the
registration page.
**What's not confirmed:** neither form's exact live HTML has been
inspected this session. Same category of risk as DEC-007 before it was
confirmed by an actual run.
**Resolution:** ship the tests, expect the first real run might need a
selector fix, update this entry with the outcome either way — that's the
process, not a failure of it.
**Update, confirmed by an actual run:** all selectors for both forms were
correct on the first try — no fixes needed. Confidence from the source-code
cross-reference (rather than a live DOM inspection) held up in this case.

## DEC-011: GitHub Pages for the Report, Not Just a CI Artifact
**Context:** Phase 3's goal (blueprint Section 9) is a report a stranger
can open without cloning the repo. A CI artifact download requires a
GitHub account and several clicks — not "just open a link."
**Chosen:** deploy `reports/report.html` to GitHub Pages on every push to
`main`, via a second CI job (`deploy-report`) using GitHub's official
`actions/deploy-pages` action rather than pushing to a `gh-pages` branch
manually.
**Trade-off accepted:** requires a one-time manual setting change in the
repo (Settings → Pages → Source: GitHub Actions) that can't be done from
a workflow file — documented plainly in the README rather than assumed.
**Also:** `deploy-report` runs with `if: always()` so a failing test run
still publishes its report — a failure is exactly the moment a reader
most wants to see the detail, not the moment to hide it.
**Update, confirmed by an actual run:** worked on the first try — both
`test` and `deploy-report` succeeded, live report publicly reachable at
`https://adyatma7.github.io/qa-project-sn/report.html`, including full
detail on the `xfail`ed BUG-001 regression test.

## DEC-012: Fixed a Race Condition in `expect_not_completed()` (Both Frameworks)
**Found by:** cross-tool testing — the Selenium port of
`test_empty_payee_name_is_rejected` failed, revealing "Bill Payment
Complete" actually appears for an empty payee name, contradicting the
Playwright version's apparent pass on the same case.
**Root cause:** `not_to_be_visible()` in Playwright can early-exit as
"not visible YET" if checked immediately after submission, before a
delayed success page finishes rendering — a false pass, not a real
rejection. The Selenium version happened to include a 2-second sleep
(for an unrelated reason — no clean "assert absence" primitive, see
`selenium-tests/README.md`) and incidentally avoided the race.
**Fix:** both `TransferPage.expect_not_completed()` and
`BillPayPage.expect_not_completed()` in `playwright-tests/pages/` now
wait 2 seconds before asserting, matching the Selenium behavior
deliberately instead of by accident.
**Why this matters beyond the fix itself:** a test that passes isn't
automatically a test that's *correct* — this one gave a false sense of
confirmed behavior for two features (`XFER-02`, `BILL-02`) until a
second, differently-built tool exposed the gap. Cross-tool validation
caught something single-tool testing missed, which is itself the
strongest argument found so far for having ported anything to Selenium
at all.
**Status:** `XFER-02` and `BILL-02` marked for re-verification in
`traceability-matrix.md` — not yet re-run with the fix.
**Update, confirmed by an actual re-run:** `XFER-02` is now resolved —
the fixed assertion confirms the transfer genuinely completes, filed as
[BUG-002](bugs/BUG-002.md). `BILL-02` is NOT resolved — the two
frameworks now disagree with each other on the same scenario even with
the fix applied. See `OBSERVATION-002.md` for the ongoing investigation;
not treating "conflicting results" as license to guess which one is
right.

## DEC-013: Selenium's `select_by_index()` Doesn't Work Reliably, Worked Around
**Found by:** running the Selenium Transfer tests for real —
`NoSuchElementException: Could not locate element with index 0` on a
`<select>` element that visibly has options.
**Root cause:** `Select.select_by_index()` matches against the option's
`index` HTML *attribute*. Browsers don't literally write `index="0"` into
option markup — `index` is a computed DOM *property*, not a source
attribute — so the match never succeeds on modern Selenium/browser
combinations. A known category of Selenium 4.x behavior change, not a
mistake in ParaBank's page.
**Fix:** `TransferPage` selects options via
`Select(...).options[index].click()` instead — operates on the actual
option `WebElement`, bypassing the broken attribute-matching path
entirely.

## DEC-014: Fixed a Second Selenium Timing Bug on the Very Next Run
**Found by:** running the (already once-fixed) Selenium Transfer tests —
`IndexError: list index out of range` on `Select(...).options[0]`.
**Root cause:** the `<select>` element was present in the DOM (satisfying
the wait for the `#amount` field elsewhere on the page), but its
`<option>` children hadn't finished populating yet at the moment
`.options` was accessed — a separate timing issue from DEC-013's
attribute-matching bug, not a re-occurrence of it.
**Fix:** added an explicit wait for
`presence_of_element_located((By.CSS_SELECTOR, "#fromAccountId option"))`
before touching `.options` at all.
**Why this is here as its own entry, not folded into DEC-013:** two
different Selenium timing/API issues surfaced back to back on the same
page object. Worth keeping them separately logged rather than merging,
since "Selenium needs more explicit waiting than Playwright" is a general
theme (see selenium-tests/README.md) but each concrete instance of it is
a distinct, specific thing that had to be found and fixed on its own.

## DEC-015: Recognized a Tool-Consistency Pattern That Ruled Out a Hypothesis
**Context:** OBSERVATION-002 (empty payee name) had two competing
explanations: shared-account balance depletion, or a tool-specific
interaction difference.
**Key observation:** re-running both suites showed each tool internally
consistent across multiple runs (Playwright 2/2 one way, Selenium 3/3 the
other), rather than inconsistent within either. Shared, globally-changing
state (like account balance) would be expected to cause noise *within*
each tool's repeated runs too, not a clean split that lines up exactly
with which tool was used.
**Resolution:** discarded the balance-depletion hypothesis in favor of a
more specific one — `Selenium's send_keys("")` dispatches no keyboard
events at all for an empty string, unlike Playwright's `.fill("")`, which
sets the value and fires input/change events regardless. If ParaBank has
any client-side validation gated on a field being touched-and-left-empty,
Selenium's version of this test may not be exercising the app the way a
real user would.
**Why this is logged even though nothing is resolved yet:** the reasoning
process that ruled out one hypothesis and proposed a sharper one is the
valuable part, independent of which explanation turns out to be right —
this is what distinguishes noticing a pattern in results from just
re-running a test and hoping.

## DEC-016: Dropped webdriver-manager, Use Selenium's Built-In Manager Instead
**Found by:** running the suite for real —
`zipfile.BadZipFile: File is not a zip file` inside `webdriver-manager`'s
own driver-download/cache logic, unrelated to any test or page object
code.
**Root cause:** `webdriver-manager` (a third-party package) downloads and
unpacks a ChromeDriver archive itself; the download was interrupted or
corrupted, and it cached the bad file.
**Fix, chosen deliberately over just clearing the cache and retrying:**
Selenium 4.6+ ships "Selenium Manager," a built-in driver-resolution tool
that detects the installed Chrome version and downloads a matching driver
automatically — `webdriver.Chrome(options=options)` alone is enough, no
`Service`/`ChromeDriverManager` needed.
**Why remove the dependency instead of patching around the failure:**
the bug lived entirely inside a package that turned out to be
unnecessary — Selenium had already solved this problem natively for
several years. One fewer dependency is one fewer thing that can fail this
way again.

## DEC-016: `webdriver-manager` Was Accidentally Missing From requirements.txt
**Found by:** the person running this project locally hit
`zipfile.BadZipFile: File is not a zip file` — initially looked like a
corrupted download, but checking the actual repo file revealed
`webdriver-manager` had been dropped from `selenium-tests/requirements.txt`
during an earlier rewrite of that file, an authoring mistake, not an app
or environment bug.
**Fix:** restored `webdriver-manager==4.1.2` to requirements.txt, and
verified with a completely fresh venv install afterward rather than
assuming the fix was correct.
**Also added while fixing this:** `pytest-html`, so `selenium-tests/`
produces a real report artifact matching `playwright-tests/`, needed for
the CI job added in the same change (Selenium tests are now part of CI,
not just run locally).
**Why this is logged even though it's my own mistake, not ParaBank's:** a
decision log that only records app findings and never the project's own
errors would be a curated highlight reel, not an honest record. This one
cost real debugging time on the other end before the actual cause was
found — worth being explicit about that cost, not just the fix.

## DEC-017: BUG-003 Likely Shares a Root Cause With BUG-002
**Context:** `test_bill_pay_amount_exceeds_balance` (from the AI-assisted
exercise) confirmed Bill Pay also accepts a wildly oversized amount, same
symptom as BUG-002 on Transfer.
**Filed separately, not merged:** as `BUG-003.md`, because the
reproduction steps and UI involved are genuinely different features —
but both bug reports explicitly cross-reference each other and note the
likely shared cause (a missing balance-validation layer affecting both
money-moving features, not two independent, coincidental bugs).
**Why this distinction matters:** treating two related symptoms as one
root cause versus two isolated bugs changes what a fix would actually
look like — this is worth being able to explain, not just filing two
reports and moving on.

## DEC-018: Corrected an Earlier Wrong Hypothesis About the CI Timeouts, Bumped Selenium Timeouts
**Context:** two previously-reliable happy-path Selenium tests
(`test_valid_transfer_completes`, `test_valid_bill_payment_completes`)
started timing out in CI waiting for form fields. Initial hypothesis was
that the shared `john` account's balance had gone to some extreme value
(from repeated confirmed BUG-002/BUG-003 large-amount transfers),
breaking page rendering.
**Checked, and the hypothesis was wrong.** A manual check of Accounts
Overview showed no extreme balances — the account genuinely has **14
separate accounts** (almost certainly created by other people's testing
against this same long-standing public demo login over the years, not
primarily by this project), with balances in normal ranges. Two accounts
are negative (-$2590.00, -$100.00) — real, if not attributable to this
project's specific test runs — which does still qualitatively corroborate
BUG-002/BUG-003 (a real balance check would never allow a negative
balance), just not in the dramatic way originally guessed.
**Better explanation:** `transfer.htm` and `billpay.htm` now have to
render a dropdown populated from 14 accounts instead of however few
existed when these tests were first written — more server-side work per
page load, on a heavily-shared public server, against a fixed 10-second
`WebDriverWait`. Bumped to 20 seconds in both `TransferPage` and
`BillPayPage` (not `LoginPage`, which isn't affected by account count).
**Logged even though the first guess was wrong:** an incorrect hypothesis
that gets checked and corrected is a normal, healthy part of
investigation — the decision log records the actual process, not just
the version that turned out right.
