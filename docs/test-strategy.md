# Test Strategy — QA Automation Portfolio (ParaBank)

Where `test-plan.md` covers *what* and *when*, this covers *how* and *why*.

## Test Pyramid Shape

```
        UI (fewest)
      API API API
  Setup/Teardown/Contracts (most)
```
More weight on API: faster to run, far less flaky, cheaper to maintain. UI
tests are reserved for flows where the actual rendered page matters — a
button being clickable isn't verifiable from an API response alone.
Current state (end of Phase 1): 3 UI tests, 1 API test — the ratio will
shift further toward API as Transfer and Bill Pay add setup/teardown calls
in Phase 2.

## Coverage Shape Per Feature

Minimum for any High/Medium-risk feature (see `risk-analysis.md`):

| Type | Purpose |
|---|---|
| Positive | Confirms the feature works as intended |
| Negative — empty input | Required-field handling |
| Negative — invalid format | Type/format validation |
| Negative — business rule | Domain rule enforcement (e.g. insufficient funds) |
| Boundary / adversarial | Deliberately pushes edge values to surface real bugs |

The last row isn't decorative — it's how BUG-001 was found. A mature,
stable demo app won't hand over a bug from happy-path clicking alone.

## Test Data Strategy
`playwright-tests/utils/test_data_generator.py` produces unique
username/password pairs so tests don't collide with each other or with
everyone else's automation hitting the same public demo. Not yet wired
into Auth (which still uses the shared `john`/`demo` login deliberately,
per DEC-006) — Phase 2's Transfer/Bill Pay tests are expected to be the
first to actually consume it, once account creation is part of the flow.

## Bug-Hunting Process
1. Write the standard positive/negative/boundary cases first.
2. Add at least one deliberately adversarial case per feature (negative
   amounts, overflow, injected characters — see `test-strategy.md`
   precedent from Auth's empty-credentials test).
3. If something looks wrong, **reproduce before filing** — run it 2-3
   times in isolation. Consistent → real bug, write it up
   (`docs/bugs/README.md` has the template and process). Intermittent →
   likely environmental (shared demo account under load), note it in
   Lessons Learned instead of filing a formal bug.
4. Don't rewrite a failing test to match buggy behavior. Mark it
   `xfail(strict=True)` with a reason pointing at the bug report — see
   `test_invalid_password_shows_error` for the working example.

## Reporting
`pytest-html` generates a self-contained HTML report on every run
(`reports/report.html`), uploaded as a CI artifact on every push. Trend
history across runs (Allure) is a Phase 6 stretch goal, not required for
the MVP.

## Tools
| Purpose | Tool |
|---|---|
| UI + API automation | Playwright (`pytest-playwright`) |
| Secondary framework | Selenium (Phase 4, 5-8 critical-path tests only) |
| Test runner | pytest |
| Reporting | pytest-html |
| CI | GitHub Actions |
| Test case management | Jira (see DEC-005 — not duplicated here) |

Full reasoning behind every tool choice: `docs/decision-log.md`.
