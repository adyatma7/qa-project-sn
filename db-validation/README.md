# DB Validation — SQLite Simulation

## Why simulation, not a live database connection
ParaBank's public demo doesn't expose its database externally — there's
no connection string to point at. Claiming live DB validation without
real access would be dishonest, and an interviewer asking "which
database?" would expose it immediately. See DEC-003 in
`docs/decision-log.md`.

## What this actually validates
A local SQLite database, built fresh from `schema.sql` + `seed-data.json`,
mirroring ParaBank's data model closely enough to demonstrate real SQL
validation reasoning — specifically, that an account's stored balance
reconciles with the sum of its transaction history. `seed-data.json` uses
the real customer record (id 12212, "John Smith") confirmed earlier in
this project by `playwright-tests/tests/api/auth/test_login_api.py`,
rather than invented data.

## Proof this isn't just SQL that happens to parse
`test_reconciliation.py` has two cases: one confirming the seed data
reconciles cleanly, and one that deliberately corrupts a stored balance
and confirms the query actually catches it. A validation script that only
ever says "OK" isn't proven to validate anything.

## How to run
```bash
cd db-validation
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python build_and_validate.py   # standalone demo
pytest -v                       # the actual test cases
```

## Optional stretch (Phase 6, not required for MVP)
Self-hosting ParaBank's official Docker image (it uses an embedded
HyperSQL database) would allow genuine DB-level validation against the
real application instead of a simulation. Noted in `future-ideas.md`, not
attempted here — see DEC-003.
