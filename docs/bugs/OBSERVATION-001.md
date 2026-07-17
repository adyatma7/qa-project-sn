# OBSERVATION-001 — RESOLVED, promoted to BUG-001

**Status: confirmed.** Re-run twice per the checklist below; both runs
showed the identical symptom shape (auth bypass + "internal error"
banner), with the second run ruling out the shared-account-collision
theory by showing the account's real name intact. See `BUG-001.md` for
the full write-up.

Original investigation notes kept below for the record — this is what a
"confirm before filing" process actually looks like end to end, not just
the tidy conclusion.

---

**Found:** running `test_invalid_password_shows_error` against the live
demo, 2026-07-16.

**What happened:** submitting `john` / (deliberately wrong password)
resulted in the page landing on `overview.htm` — Accounts Overview —
showing account data under the name "ObtsznF enb" instead of "John Smith",
with a `.error` element simultaneously containing "An internal error has
occurred and has been logged." instead of the expected clean rejection
message.

**Two competing explanations at the time:** a real ParaBank bug, or
shared-account collision (see DEC-006 / blueprint Section 6). Resolved by
reproduction: the second run showed the correct account name but the
identical failure symptom, which is only consistent with explanation one.
