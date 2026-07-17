# Bugs

No `BUG-001.md` yet — and that's honest, not lazy. Per blueprint Section 7:
a fabricated bug is worse than no bug yet.

I (Claude) can't execute these tests against the live ParaBank site from
this sandbox — no network access to `parabank.parasoft.com` here. The
adversarial test in `test_empty_credentials_are_rejected` was written
specifically to probe for a real finding, but someone has to actually run
`pytest` and read the result.

## What to do next
1. Run `pytest -v` locally.
2. If `test_empty_credentials_are_rejected` passes cleanly — that's still a
   legitimate, documented finding ("tested empty-field submission, handled
   correctly, no bug found") per Section 7's honest-fallback rule. Note it
   in `docs/test-strategy.md` once that file exists, no fabricated bug
   needed.
3. If it fails, or if ParaBank behaves unexpectedly (ugly stack trace,
   inconsistent error, anything not a clean rejection) — that's BUG-001.
   Copy the template from the blueprint (Section 8.4) into `BUG-001.md`
   here, fill it in from what you actually observed, and link the
   regression test.
4. Also worth trying manually once, outside the automated suite: decimal
   overflow or script-tag input in fields elsewhere in the app (Transfer,
   Bill Pay) once those exist in Phase 2 — per the bug-hunting tactic, a
   mature stable app like this won't hand you a bug from happy-path
   clicking alone.
