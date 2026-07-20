# Test Plan — QA Automation Portfolio (ParaBank)

## Objective
Validate the core user-facing flows of ParaBank's banking application
through automated UI and API testing, producing a portfolio artifact that
demonstrates real QA process — not just scripts that happen to run. Full
project goal and audience: see the root `README.md`, "Business Goal" section.

## Scope

**In scope (see risk-analysis.md for why these, in this order):**
- Login / Authentication — done, Phase 1
- Fund Transfer — Phase 2
- Bill Pay — Phase 2
- REST API: login endpoint — done, Phase 1

**Out of scope, explicitly:**
- Load/performance testing at scale (one optional script at most, Phase 6)
- Security penetration testing beyond basic adversarial input
- Native mobile app testing (none exists for ParaBank)
- Full cross-browser matrix (Chromium only)
- White-box/source-code testing (black-box only, no server access)
- Full list and reasoning: blueprint Section 1.4

## Test Approach
- **UI automation:** Playwright (Python, `pytest-playwright`), Page Object
  Model, one page class per ParaBank page under test
- **API automation:** Playwright's request context, hitting ParaBank's
  REST services directly (`/parabank/services/bank/...`)
- **Coverage shape per feature:** positive, negative, boundary — see
  `test-strategy.md` for the full reasoning
- **Bug hunting:** deliberate adversarial input on top of standard negative
  cases, not just boundary-value padding — this is what surfaced BUG-001

## Environment
- Target: `https://parabank.parasoft.com/parabank/` (public demo instance)
- Browser: Chromium only (see Out of Scope)
- CI: GitHub Actions, Ubuntu runner, Python 3.12
- Local: any OS with Python 3.12+ and a Chromium-capable Playwright install

## Entry Criteria
- Feature's page structure/selectors confirmed against the live app (or
  documented as unverified with a plan to confirm — see decision-log.md
  for examples of both)
- `risk-analysis.md` updated with the feature before writing its tests

## Exit Criteria (per feature)
- Positive, negative, and at least one boundary/adversarial case automated
- Result — pass or a filed, reproducible bug — recorded in
  `traceability-matrix.md`
- Any genuine finding written up per the process in `docs/bugs/README.md`
  (reproduce before filing, don't fabricate, don't skip if reproducible)

## Risks & Assumptions
Full table: `risk-analysis.md`. Key assumption carried since Phase 1: the
public demo's shared accounts (`john`/`demo`) are convenient but not fully
reliable test fixtures under concurrent load from other testers — accepted
for now, revisited if it causes real problems (see DEC-006).

## Schedule
Phased, not dated — see the root `README.md`'s "Phase-by-Phase Status"
table (inside the collapsed planning reference section) for the full
roadmap and the explicit MVP cutoff after Phase 2.
