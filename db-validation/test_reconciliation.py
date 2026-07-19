"""
Tests for the reconciliation simulation itself — proves the query
actually catches a mismatch, not just that it passes on already-correct
seed data. Fully offline, no ParaBank access needed.
"""
from build_and_validate import build_db, run_reconciliation


def test_seed_data_reconciles_cleanly():
    conn = build_db()
    assert run_reconciliation(conn) == []


def test_reconciliation_catches_a_real_mismatch():
    conn = build_db()
    # Deliberately corrupt the stored balance with no matching
    # transaction, to prove the query detects a mismatch rather than
    # trivially passing no matter what.
    conn.execute("UPDATE account SET balance = 999999 WHERE id = 13344")
    conn.commit()
    mismatches = run_reconciliation(conn)
    assert len(mismatches) == 1
    assert mismatches[0][0] == 13344
