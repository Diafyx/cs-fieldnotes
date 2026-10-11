# BETWEEN and NOT BETWEEN

`BETWEEN` checks whether a value lies inside a range, including both ends. `NOT BETWEEN` checks whether it lies outside. A missing value makes either test unknown.

## Both bounds count

```sql
SELECT employee_id, salary
FROM employees
WHERE salary BETWEEN 50000 AND 80000;
```

This includes salaries of exactly 50000 and 80000. It is the same as `salary >= 50000 AND salary <= 80000`. The lower bound goes first. If the first bound is greater than the second, ordinary values will not match.

To find salaries outside that range:

```sql
SELECT employee_id, salary
FROM employees
WHERE salary NOT BETWEEN 50000 AND 80000;
```

This keeps 49999 and 80001. It does not keep a `NULL` salary. Add `OR salary IS NULL` if missing salaries should be reported too.

## Dates and timestamps need different care

For a `date` column, inclusive bounds can be natural:

```sql
WHERE order_date BETWEEN DATE '2026-01-01' AND DATE '2026-01-31'
```

For a timestamp, the end of a day has many possible fractions of a second. Use a half-open interval:

```sql
WHERE placed_at >= TIMESTAMPTZ '2026-01-01 00:00:00+00'
  AND placed_at < TIMESTAMPTZ '2026-02-01 00:00:00+00'
```

This includes every instant in January in UTC. If the report uses a local time zone, build the start and end instants for that zone. Do not assume a local day is always 24 hours when clocks change.

## Ranges over text

`BETWEEN` can compare text, but the active collation decides order. A range such as `name BETWEEN 'A' AND 'M'` is not a reliable way to mean "names starting with A through M" across databases and collations. State a text matching rule separately.

## Check your understanding

1. Does `BETWEEN 10 AND 20` include 20?
2. Why is a February 1 exclusive bound safer for January timestamps?
3. Does `salary NOT BETWEEN 50000 AND 80000` return a row with `NULL` salary?

## Further reading

- [PostgreSQL BETWEEN predicates](https://www.postgresql.org/docs/current/functions-comparison.html)
- [PostgreSQL date and time types](https://www.postgresql.org/docs/current/datatype-datetime.html)
- [PostgreSQL collations](https://www.postgresql.org/docs/current/collation.html)
