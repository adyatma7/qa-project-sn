# Learning Notes: `test_login.py`

Companion notes for `playwright-tests/tests/ui/auth/test_login.py` and
`playwright-tests/pages/login_page.py`. This file is allowed to be messy —
the actual test code stays clean (see blueprint DEC-004). Read this next to
the two real files, not instead of them.

---

## `from pages.login_page import LoginPage`
This import only resolves because two things are true: `pages/__init__.py`
exists (makes `pages` a real Python package, even though the file is empty),
and pytest is run from inside `playwright-tests/` — `conftest.py` sitting at
that root is what tells pytest "this directory is the project root," which
is what puts it on the import path. Move `conftest.py` and this import
breaks; that's the first thing to check if it ever does.

## Why a Page Object at all?
Everything that knows about ParaBank's actual HTML (`input[name="username"]`,
etc.) lives inside `LoginPage`, never inside the test itself. If ParaBank
ever renames that field, there's exactly one file to fix. A small project
doesn't strictly need this to survive — but it's the habit that scales, and
it's also just what a reviewer expects to see.

## `def test_user_can_log_in_and_reach_accounts_overview(page):`
No `import` needed for `page` — it's a **pytest fixture**, injected
automatically by the `pytest-playwright` plugin just by naming it as a
function argument. That's a different mechanism than the JS/TS version
(where `page` came from Playwright Test's own `test()` wrapper); in pytest,
fixtures are pytest's own dependency-injection system, and plugins like
`pytest-playwright` register fixtures with it. Function name matters too:
pytest auto-discovers any function starting with `test_` in a file starting
with `test_` — no decorator required, unlike some other frameworks.

## `login_page = LoginPage(page)`
`page` here is Playwright's live browser-tab object. Passing it into
`LoginPage.__init__` is what lets every method on the class drive that same
tab through `self.page`.

## `login_page.goto()`
Inside `LoginPage.goto()`: `self.page.goto("/index.htm")`. That path is
*relative* — it resolves against the `base-url` set in `pytest.ini`'s
`addopts`. Override it per-run without touching any file:
`pytest --base-url=http://localhost:8080/parabank`.

## `login_page.login("john", "demo")`
`john` / `demo` is ParaBank's own long-standing public demo login, not
something invented for this project. Chosen deliberately for Phase 0 instead
of registering a fresh user, because Phase 0 is supposed to be the smallest
reliable slice possible (blueprint Section 9, Rule 1) — fresh, unique,
self-registered users are explicitly Phase 1's job, alongside
`test_data_generator.py`.

**Honest known risk:** this is a *shared* public credential. If it's ever
changed by someone else poking at the same account, this test breaks through
no fault of the code here. That's exactly the test-data fragility Section 6
of the blueprint warns about — and exactly why Phase 1 replaces this with
self-generated, collision-proof users instead of leaning on a shared login
long-term.

### Inside `LoginPage.login()`
```python
self.page.locator('input[name="username"]').fill(username)
```
`.locator()` doesn't grab the element immediately — it's a description that
Playwright re-resolves right before it acts. That's *why* Playwright mostly
doesn't need explicit waits the way Selenium does; the "wait for it to exist
and be ready" step is baked into every action automatically. Same behavior
in the Python API as the JS one — this part of Playwright's design doesn't
change across languages.

`.fill()` clears the field first, then sets the value — more reliable for
form inputs than simulating individual keystrokes.

```python
self.page.locator('input[value="Log In"]').click()
```
ParaBank's login button is a literal `<input type="submit" value="Log In">`,
not a `<button>` tag with visible text. That's why this matches on the
`value` attribute rather than using something like
`get_by_role("button", name="Log In")`, which expects an actual button
element or accessible role.

## `login_page.expect_logged_in()`
Inside: `expect(self.page).to_have_title("ParaBank | Accounts Overview")`.
Deliberately checks the page **title**, not visible text on the page.
Titles tend to survive a visual redesign that changes on-page wording, so
this assertion should stay valid longer than one that greps for text in the
body. Note the Python API's naming convention: `to_have_title`, snake_case —
the JS/TS equivalent was `toHaveTitle`, camelCase. Same assertion library
underneath (`expect`), different per-language naming convention on top.

---

**Next time this file gets touched:** Phase 1 adds a negative-login test
(wrong password) right next to this one in the same file, plus an
equivalent note appended below this line.

---

## Phase 1 additions

### `test_invalid_password_shows_error`
Same `LoginPage`, new method: `expect_login_error()`. The selector
`.error` targets ParaBank's actual CSS class for its login-failure banner —
confirmed against a real working example, not guessed. The exact message
text ("The username and password could not be verified.") is asserted with
`to_contain_text`, not `to_have_text` — `contain` survives ParaBank wrapping
the message in extra markup or whitespace; `have_text` would break on any
tiny formatting difference that doesn't actually matter.

### `test_empty_credentials_are_rejected`
Uses `expect_login_failed()` instead of `expect_login_error()` on purpose —
a *weaker* assertion (just "didn't reach Accounts Overview"), because the
exact behavior for blank fields genuinely isn't confirmed yet. This is the
test Section 7's bug-hunting tactic is talking about: it might just pass
quietly (good, robust app), or it might reveal something worth a real bug
report. Either outcome is a legitimate finding — see `docs/bugs/README.md`.

### `test_valid_login_returns_customer_via_api` (in `tests/api/auth/`)
Different fixture pattern: `page.request.get(...)` instead of `page.goto(...)`.
Same `page` fixture, but `.request` is Playwright's HTTP client sitting
alongside the browser — no browser rendering involved, just a raw HTTP call
and a JSON response. This is what "API test" means concretely: check the
data, not a rendered page. Flagged with `@pytest.mark.api` so these can
later be run separately from UI tests (`pytest -m api`) once there are
enough of them to matter.

**Important honesty note carried over from the test file itself:** the
endpoint path used here was not independently confirmed against ParaBank's
own Swagger docs this session — see DEC-007 in `docs/decision-log.md`. If
this test fails when actually run, checking the Swagger UI in a browser is
the first debugging step, not assuming the test code has a typo.

---

## The actual first run (real bugs, not hypothetical)

Ran all 4 tests for real. All 4 failed. Both failures turned out to be
genuinely useful — this section exists because "it failed and I fixed it"
is worth more in an interview than "it passed first try."

### Every UI test timed out on the same line
```
TimeoutError: Locator.fill: Timeout 30000ms exceeded.
waiting for locator("input[name=\"username\"]")
```
First instinct might be "wrong selector." It wasn't. The actual page URL
in the failure log was the giveaway:
`page = <Page url='https://parabank.parasoft.com/index.htm'>` — missing
`/parabank` entirely. The username field was never found because the
browser was never even on the login page.

**Why the URL came out wrong:** this is standard URL-resolution behavior
(WHATWG URL spec), not a ParaBank or Playwright quirk. Two rules combine
badly here:
- A relative path starting with `/` is *absolute from the domain root* —
  it discards whatever path the base URL had.
- A base URL *without* a trailing slash treats its last path segment as a
  "file," not a "directory," so even a relative path without a leading
  slash would replace that segment instead of appending to it.

Original code: `base_url = ".../parabank"` (no trailing slash) +
`goto("/index.htm")` (leading slash) → both rules point the same wrong
way → `https://parabank.parasoft.com/index.htm`.

**Fix:** `base_url = ".../parabank/"` (trailing slash makes it a
directory) + `goto("index.htm")` (no leading slash, so it appends instead
of resetting) → correctly resolves to `.../parabank/index.htm`.

**The bigger lesson:** all three UI tests failed with the identical error.
That's a strong signal to look for *one* shared root cause before
debugging each test as a separate problem — three failures with the exact
same stack trace shape almost never mean three different bugs.

### The API test failed on `.json()`, not on the request itself
```
json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
```
The response body, visible in the failure log, was real customer XML:
`<customer><id>12212</id><firstName>John</firstName>...`. That's actually
good news hiding inside a failure — it proves the endpoint path guess
(never independently confirmed, see DEC-007) was correct all along. The
server just returns XML by default instead of JSON. Fixed by parsing with
`xml.etree.ElementTree` instead of assuming JSON.

**Lesson:** an assertion failure isn't always "the test is wrong" or "the
app is wrong" — sometimes it's "my assumption about the response shape was
wrong," and the failure log itself usually contains the evidence needed to
tell which one it was, if you read past the exception name.

