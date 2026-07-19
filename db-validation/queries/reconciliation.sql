-- Validates that an account's stored balance matches the sum of its
-- recorded transactions. An empty result set means everything reconciles;
-- any row returned is a real, specific mismatch to investigate.
SELECT
    a.id AS account_id,
    a.balance AS stored_balance,
    COALESCE(SUM(
        CASE WHEN t.type = 'CREDIT' THEN t.amount ELSE -t.amount END
    ), 0) AS computed_balance
FROM account a
LEFT JOIN account_transaction t ON t.account_id = a.id
GROUP BY a.id
HAVING stored_balance != computed_balance;
