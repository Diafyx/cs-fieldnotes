# Visitors Without Transactions

A visit can exist without a purchase. Start with visits, left join transactions, and keep visits whose transaction side is missing.

## The question

Return each customer ID and the number of their visits with no transaction. Customers with no such visits should not appear. Sort by customer ID.

```sql
CREATE TEMP TABLE visits (
  visit_id integer PRIMARY KEY,
  customer_id integer NOT NULL,
  visited_on date NOT NULL
);
CREATE TEMP TABLE transactions (
  transaction_id integer PRIMARY KEY,
  visit_id integer NOT NULL,
  amount numeric(10, 2) NOT NULL
);

INSERT INTO visits VALUES
  (1, 10, '2026-01-01'),
  (2, 10, '2026-01-02'),
  (3, 20, '2026-01-03'),
  (4, 30, '2026-01-04');
INSERT INTO transactions VALUES (100, 2, 15.00), (101, 4, 20.00);
```

## A solution

```sql
SELECT v.customer_id, COUNT(*) AS visits_without_transactions
FROM visits AS v
LEFT JOIN transactions AS t ON t.visit_id = v.visit_id
WHERE t.transaction_id IS NULL
GROUP BY v.customer_id
ORDER BY v.customer_id;
```

The result is customer 10 with one visit and customer 20 with one visit. Visit 1 and visit 3 have no transaction. Visit 2 and visit 4 are removed by the `WHERE` test. Since only unmatched visit rows reach `GROUP BY`, `COUNT(*)` correctly counts visits here.

A visit may have several transactions in some systems. That does not affect this no-transaction test: any match means the visit is excluded. Use a non-null right-side key for the test. Checking a nullable amount could wrongly treat a real transaction as missing.

## Check your understanding

1. Which of customer 10's visits is counted?
2. Why is `COUNT(*)` correct after the missing-match filter?
3. Why is `t.transaction_id` safer to test than a nullable transaction field?

## Further reading

- [PostgreSQL outer joins](https://www.postgresql.org/docs/current/queries-table-expressions.html#QUERIES-JOIN)
