-- Local SQLite schema mirroring ParaBank's data model, used to validate
-- data consistency without needing real access to ParaBank's actual
-- database — the public demo doesn't expose one. See DEC-003.
--
-- Field names loosely follow what's confirmed from the real customer
-- record returned by playwright-tests/tests/api/auth/test_login_api.py
-- (id, firstName, lastName, address, phoneNumber, ssn).

CREATE TABLE customer (
    id INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    street TEXT,
    city TEXT,
    state TEXT,
    zip_code TEXT,
    phone_number TEXT,
    ssn TEXT,
    username TEXT UNIQUE NOT NULL
);

CREATE TABLE account (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customer(id),
    type TEXT NOT NULL CHECK (type IN ('CHECKING', 'SAVINGS')),
    balance REAL NOT NULL DEFAULT 0
);

-- Named account_transaction, not transaction — TRANSACTION is a
-- reserved keyword in SQLite (used in BEGIN TRANSACTION).
CREATE TABLE account_transaction (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id INTEGER NOT NULL REFERENCES account(id),
    type TEXT NOT NULL CHECK (type IN ('CREDIT', 'DEBIT')),
    amount REAL NOT NULL,
    description TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
