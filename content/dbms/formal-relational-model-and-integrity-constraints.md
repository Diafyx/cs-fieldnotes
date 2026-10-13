# Formal Relational Model and Integrity Constraints

The relational model describes data as relations. A relation has a name, a fixed set of named attributes, and a set of tuples. In a SQL table, these roughly correspond to a table, columns, and rows. The relation schema says which attributes exist and what values they can hold. A relation instance is the set of tuples at one point in time.

For example, `Employee(employee_id, name, department_id)` is a schema. `(7, 'Mina', 2)` is one tuple. The allowed values for an attribute form its domain. In practice, a SQL type is only part of a domain. A `CHECK` constraint can narrow it further.

## Keys and constraints

| Term | Meaning |
| --- | --- |
| Superkey | Attributes that uniquely identify a tuple. It may contain extra attributes. |
| Candidate key | A superkey with no unnecessary attribute. |
| Primary key | The candidate key chosen as the main identifier. |
| Alternate key | Another candidate key, often enforced with `UNIQUE`. |
| Foreign key | Attributes that refer to a key in another relation. |

If `employee_id` uniquely identifies an employee, both `{employee_id}` and `{employee_id, name}` are superkeys. Only `{employee_id}` is minimal, so it is a candidate key. A composite key uses more than one attribute, such as `(order_id, line_number)`.

Integrity constraints keep invalid states out of the database. A primary key provides uniqueness and forbids `NULL`. A foreign key checks a reference. `NOT NULL` requires a value. `CHECK` tests a condition. Some business rules, such as a department's total pay staying below a budget, involve several rows and need more than a simple row check.

```sql
CREATE TEMP TABLE departments (
    department_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

CREATE TEMP TABLE employees (
    employee_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    department_id INTEGER NOT NULL REFERENCES departments(department_id),
    salary INTEGER NOT NULL CHECK (salary >= 0)
);

INSERT INTO departments VALUES (1, 'Support'), (2, 'Research');
INSERT INTO employees VALUES
    (7, 'Mina', 2, 60000),
    (8, 'Dev', 1, 45000);

SELECT e.employee_id, e.name, d.name AS department
FROM employees AS e
JOIN departments AS d ON d.department_id = e.department_id
ORDER BY e.employee_id;
```

The query returns `(7, Mina, Research)` and `(8, Dev, Support)`. An employee with department `3` would fail the foreign key check. A negative salary would fail the `CHECK`. A second employee with ID `7` would fail the primary key check.

## The model and SQL differ

A mathematical relation is a set. It has no duplicate tuples and no row order. SQL query results usually keep duplicates unless you ask for `DISTINCT`, and their order is only promised with `ORDER BY`. SQL also has `NULL`, which is not an ordinary domain value. Comparisons with `NULL` usually give an unknown result.

A nullable foreign key permits a missing reference. Add `NOT NULL` when every row must have a parent. In PostgreSQL, a `CHECK` passes when its expression is true **or unknown**. Use `NOT NULL` as well if `NULL` must be rejected. A normal `UNIQUE` constraint can also allow multiple `NULL` values. These details matter when turning a paper schema into SQL tables.

## Try it yourself

1. If `(order_id, line_number)` identifies an order line, is `order_id` alone a superkey? Explain with two example rows.
2. What would change if `department_id` in `employees` were nullable?
3. Why does `SELECT DISTINCT` sometimes matter when translating a relational expression into SQL?

## References

- [PostgreSQL constraints](https://www.postgresql.org/docs/current/ddl-constraints.html)
- [PostgreSQL sorting rows](https://www.postgresql.org/docs/current/queries-order.html)
