# Advanced CASE Usage

The hard part of `CASE` is usually the rule order. When several conditions can be true, the first true branch wins. Use that fact on purpose, and keep the rules easy to inspect.

## Put the most specific rule first

```sql
SELECT account_id, balance,
       CASE
         WHEN balance IS NULL THEN 'unknown'
         WHEN balance < 0 THEN 'overdrawn'
         WHEN balance = 0 THEN 'empty'
         WHEN balance >= 1000 THEN 'high'
         ELSE 'positive'
       END AS balance_band
FROM accounts;
```

These branches cover missing, negative, zero, high, and other positive balances. If `balance >= 0` came before `balance >= 1000`, high balances would never reach the high branch.

## Turn rows into grouped columns

Suppose each `sales` row has `store_id`, `status`, and `amount`:

```sql
SELECT store_id,
       SUM(CASE WHEN status = 'paid' THEN amount ELSE 0 END) AS paid_amount,
       SUM(CASE WHEN status = 'refunded' THEN amount ELSE 0 END) AS refunded_amount
FROM sales
GROUP BY store_id;
```

This makes separate totals for two statuses. It assumes every `amount` is present and positive, including refund amounts. If refund rows store negative values, the second sum will be negative. Decide whether the report should show a signed net value or a positive refund amount. `ELSE 0` makes nonmatching rows add nothing; it does not fix missing amounts in matching rows.

## Keep complex rules maintainable

If one `CASE` has many branches, give each rule a clear name in a separate query or view. Check boundary values and `NULL` for every branch. A `CASE` inside another `CASE` can be valid, but flat rules are often easier to test.

PostgreSQL normally evaluates only the chosen result branch at run time. Do not rely on `CASE` to protect a constant expression such as `1 / 0`; PostgreSQL can detect that error while planning the query. For a row-dependent denominator, use `NULLIF(denominator, 0)` when a missing result is acceptable.

## Check your understanding

1. Why must `balance IS NULL` have its own branch?
2. What would change if `balance >= 0` were placed before the high-balance rule?
3. Why must the sign of refund amounts be defined before making a refund total?

## Further reading

- [PostgreSQL CASE expression](https://www.postgresql.org/docs/current/functions-conditional.html#FUNCTIONS-CASE)
- [PostgreSQL expression evaluation rules](https://www.postgresql.org/docs/current/sql-expressions.html#SYNTAX-EXPRESS-EVAL)
