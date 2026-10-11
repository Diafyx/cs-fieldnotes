# Find Salaries Outside the Expected Range

This practice question checks a lower and upper limit. A salary exactly on either limit is expected. Only values below the lower limit or above the upper limit are outside the range.

## The question

For this exercise, the expected yearly salary is from 40,000 through 120,000, including both ends. Return `employee_id` and `salary` for salaries outside that range. A missing salary needs review but is not a known value outside the range, so leave it out of this result.

```sql
CREATE TEMP TABLE employee_pay (
  employee_id integer PRIMARY KEY,
  salary numeric(12, 2)
);

INSERT INTO employee_pay (employee_id, salary) VALUES
  (1, 39999.99),
  (2, 40000.00),
  (3, 75000.00),
  (4, 120000.00),
  (5, 120000.01),
  (6, NULL);
```

## A solution

```sql
SELECT employee_id, salary
FROM employee_pay
WHERE salary NOT BETWEEN 40000 AND 120000
ORDER BY employee_id;
```

The output contains employees 1 and 5. `BETWEEN` includes 40,000 and 120,000, so `NOT BETWEEN` excludes those boundary values. Employee 6 is not returned because a comparison with `NULL` is unknown.

The same known-value rule can be written as `salary < 40000 OR salary > 120000`. If you want one report for all pay records needing review, add `OR salary IS NULL` and show the missing records clearly. Do not treat a missing salary as zero, since zero is a real number with a different meaning.

## Check your understanding

1. Does 120,000.00 count as outside the range?
2. Why does the query omit employee 6?
3. How would you include missing salaries in a review report?

## Further reading

- [PostgreSQL BETWEEN predicates](https://www.postgresql.org/docs/current/functions-comparison.html)
