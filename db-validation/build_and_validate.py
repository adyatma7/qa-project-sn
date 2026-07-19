"""
Builds the local SQLite database from schema.sql + seed-data.json, then
runs the reconciliation query. Self-contained proof that the simulation
actually works — not just that the .sql files parse without error.
Fully offline: no ParaBank access needed, nothing here depends on the
live site being reachable.
"""
import json
import sqlite3
from pathlib import Path

BASE = Path(__file__).parent


def build_db() -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    conn.executescript((BASE / "schema.sql").read_text())

    seed = json.loads((BASE / "seed-data.json").read_text())
    for c in seed["customers"]:
        conn.execute(
            "INSERT INTO customer (id, first_name, last_name, street, city, "
            "state, zip_code, phone_number, ssn, username) VALUES "
            "(:id, :first_name, :last_name, :street, :city, :state, "
            ":zip_code, :phone_number, :ssn, :username)",
            c,
        )
    for a in seed["accounts"]:
        conn.execute(
            "INSERT INTO account (id, customer_id, type, balance) VALUES "
            "(:id, :customer_id, :type, :balance)",
            a,
        )
    for t in seed.get("transactions", []):
        conn.execute(
            "INSERT INTO account_transaction (account_id, type, amount, "
            "description) VALUES (:account_id, :type, :amount, :description)",
            t,
        )
    conn.commit()
    return conn


def run_reconciliation(conn: sqlite3.Connection) -> list:
    query = (BASE / "queries" / "reconciliation.sql").read_text()
    return conn.execute(query).fetchall()


if __name__ == "__main__":
    connection = build_db()
    mismatches = run_reconciliation(connection)
    if mismatches:
        print(f"MISMATCH FOUND: {mismatches}")
        raise SystemExit(1)
    print("Reconciliation OK — account balance matches its transaction history.")
