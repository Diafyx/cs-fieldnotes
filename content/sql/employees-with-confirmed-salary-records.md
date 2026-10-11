# Employees With Confirmed Salary Records

Salary history can include draft and confirmed records. A join should return only confirmed records when that is what the report asks for.

## The question

Return each employee name and confirmed salary amount. An employee can have more than one salary record, but this sample has at most one confirmed record per employee. Sort by employee ID.

```sql
CREATE TEMP TABLE employees (
  employee_id integer PRIMARY KEY,
  name text NOT NULL
);
CREATE TEMP TABLE salary_records (
  record_id integer PRIMARY KEY,
  employee_id integer NOT NULL,
  amount numeric(12, 2) NOT NULL,
  status text NOT NULL
);

INSERT INTO employees VALUES (1, 'Asha'), (2, 'Ben'), (3, 'Cara');
INSERT INTO salary_records VALUES
  (10, 1, 50000.00, 'confirmed'),
  (11, 1, 55000.00, 'draft'),
  (12, 2, 60000.00, 'confirmed');
```

## A solution

```sql
SELECT e.employee_id, e.name, s.amount
FROM employees AS e
JOIN salary_records AS s
  ON s.employee_id = e.employee_id
 AND s.status = 'confirmed'
ORDER BY e.employee_id;
```

The result is `(1, Asha, 50000)` and `(2, Ben, 60000)`. Asha's draft amount is excluded. Cara has no confirmed salary record, so the inner join excludes her. Putting the status condition in `WHERE` would give the same result for this inner join.

If an employee has two confirmed records, this query returns two rows for that employee. It does not choose the newest one. A report asking for the current salary needs an effective date or another rule that picks one record. Do not hide the extra row with `DISTINCT`, since two different confirmed amounts are important data.

## Check your understanding

1. Why is Asha's draft salary absent?
2. Why is Cara absent?
3. What extra field and rule would help select a current salary from several confirmed records?

## Further reading

- [PostgreSQL joined tables](https://www.postgresql.org/docs/current/queries-table-expressions.html#QUERIES-JOIN)
