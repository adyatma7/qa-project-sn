# Playwright Tests — Primary Automation Suite

Primary framework for this project (see root README's Tech Stack and
`docs/decision-log.md` DEC-001/DEC-006 for why). Covers UI + API, full
positive/negative/adversarial coverage — not just the critical-path
subset that `selenium-tests/` intentionally limits itself to.

## Structure
```
playwright-tests/
├── requirements.txt
├── pytest.ini            # base_url, tracing, screenshot/video on failure, HTML report
├── conftest.py
├── pages/                 # Page Object Model — one class per ParaBank page
├── utils/
│   └── test_data_generator.py
└── tests/
    ├── ui/
    │   ├── auth/
    │   ├── transfer/
    │   └── bill-pay/
    └── api/
        └── auth/
```

## How to run
```bash
python3 -m venv .venv && source .venv/bin/activate   # macOS/Linux
# .\.venv\Scripts\Activate.ps1                        # Windows PowerShell
pip install -r requirements.txt
playwright install --with-deps
pytest -v
```

## Known quirks worth knowing before touching this code
- **`base_url` needs a trailing slash, and `goto()` calls must NOT start
  with `/`.** Getting this backwards silently drops the `/parabank` path
  segment and every test times out looking for elements on the wrong
  page. Full story: `docs/decision-log.md` DEC-008.
- **Negative assertions need a settle-time wait before checking.**
  `expect(...).not_to_be_visible()` can early-exit as "not visible yet"
  if a delayed success page hasn't finished rendering — this exact race
  condition hid [BUG-002](../docs/bugs/BUG-002.md) for a while. See
  DEC-012.
- **Known bugs are `xfail`, not deleted or rewritten.** Tests for
  BUG-001/002/003 keep asserting the *correct* expected behavior and stay
  marked `xfail(strict=False)` — they're meant to keep "failing"
  (harmlessly, by design) until ParaBank actually fixes the underlying
  issue.

## Where the real depth lives
- Line-by-line explainers for the trickier code: `../learning-notes/`
- Why each tool/pattern was chosen: `../docs/decision-log.md`
- What's tested and why: `../docs/test-strategy.md`, `../docs/risk-analysis.md`
