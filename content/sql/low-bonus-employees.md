# Low Bonus Employees

An employee may have a bonus row or no bonus row. This exercise treats a missing bonus row as zero and asks for employees whose bonus is below 1000.

## The question

Return employee ID, name, and bonus amount for everyone with an amount under 1000. Sort by employee ID.

```sql
CREATE TEMP TABLE employees (
  employee_id integer PRIMARY KEY,
  name text NOT NULL
);
CREATE TEMP TABLE bonuses (
  employee_id integer PRIMARY KEY,
  bonus numeric(12, 2) NOT NULL
);

INSERT INTO employees VALUES
  (1, 'Asha'), (2, 'Ben'), (3, 'Cara'), (4, 'Dev');
INSERT INTO bonuses VALUES (1, 500.00), (2, 1500.00), (4, 0.00);
```

## A solution

```sql
SELECT e.employee_id, e.name,
       COALESCE(b.bonus, 0) AS bonus
FROM employees AS e
LEFT JOIN bonuses AS b ON b.employee_id = e.employee_id
WHERE COALESCE(b.bonus, 0) < 1000
ORDER BY e.employee_id;
```

The rows are Asha with 500, Cara with 0, and Dev with 0. Ben's 1500 does not qualify. Cara has no bonus record, while Dev has a recorded zero bonus. This report displays both as zero under its stated rule, but the stored situations differ.

If missing bonus records should mean "unknown" instead of zero, do not use `COALESCE` here. Decide whether those employees belong in the result. The bonus table has one row per employee, so the join does not create several rows for one person.

## Check your understanding

1. Why is Cara included?
2. How do Cara's and Dev's stored data differ?
3. What would change if a missing bonus meant unknown rather than zero?

## Further reading

- [PostgreSQL joined tables](https://www.postgresql.org/docs/current/queries-table-expressions.html#QUERIES-JOIN)
- [PostgreSQL COALESCE](https://www.postgresql.org/docs/current/functions-conditional.html#FUNCTIONS-COALESCE-NVL-IFNULL)
