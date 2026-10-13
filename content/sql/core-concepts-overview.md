# Core Concepts (Overview)

A relational database holds tables. Each table has columns with types, and each row gives values for those columns. A table should have a clear meaning for one row. Keys identify rows and connect tables. Constraints make some invalid states impossible to store.

## Read a small schema

```sql
CREATE TEMP TABLE departments (
  department_id integer PRIMARY KEY,
  name text NOT NULL UNIQUE
);

CREATE TEMP TABLE employees (
  employee_id integer PRIMARY KEY,
  department_id integer REFERENCES departments(department_id),
  email text NOT NULL UNIQUE,
  salary numeric(10, 2) NOT NULL CHECK (salary >= 0)
);

INSERT INTO departments VALUES (10, 'Support');
INSERT INTO employees VALUES
  (1, 10, 'ada@example.test', 50000),
  (2, NULL, 'ben@example.test', 45000);

SELECT e.employee_id, d.name AS department_name
FROM employees AS e
LEFT JOIN departments AS d ON d.department_id = e.department_id
ORDER BY e.employee_id;
```

The query returns `(1, Support)` and `(2, NULL)`. Ada is linked to Support. Ben has no department yet. The nullable foreign key allows that, while a non-null department ID must match a department row. The left join keeps both employees.

`employee_id` is a primary key: it is unique and cannot be null. `email` is another unique value, but it is not the chosen primary key. `department_id` in `employees` is a foreign key. `salary` has a numeric type and a check that rejects negative values. The `CHECK` alone would not reject SQL `NULL`, so `NOT NULL` is also present.

## Terms to keep separate

An entity is something the system tracks, such as an employee. An attribute is a fact about it, such as email. A relationship connects entities, such as an employee belonging to a department. A key identifies a row. A constraint is an enforced rule. A query asks for rows or changes them. An index is a structure that may make some queries faster; it is not the same thing as a relationship or a business rule.

SQL tables are not pure mathematical relations in every detail. SQL can contain nulls and can return duplicate rows unless a query or constraint rules them out. That is why a clear row meaning and explicit constraints matter in a real database.

## Check your understanding

1. Why can Ben's department be null but Ada's department ID must match a row?
2. Which rule stops two employees from sharing an email?
3. Why does the salary column need both `NOT NULL` and `CHECK`?

## Further reading

- [PostgreSQL table basics](https://www.postgresql.org/docs/current/ddl-basics.html)
- [PostgreSQL constraints](https://www.postgresql.org/docs/current/ddl-constraints.html)
