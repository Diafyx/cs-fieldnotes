# Fundamental Relational Algebra

Relational algebra is a small language for building a new relation from existing relations. Each operation takes one or two relations and returns a relation. This is called closure. It lets us build larger expressions from smaller ones.

The classic operations work on sets of tuples. SQL often works on results that contain duplicates, so a direct SQL translation may need `DISTINCT`.

| Operation | What it does | Usual SQL form |
| --- | --- | --- |
| Selection | Keeps rows that meet a condition. | `WHERE` |
| Projection | Keeps named attributes and removes duplicate tuples. | `SELECT DISTINCT` |
| Rename | Changes relation or attribute names. | Table and column aliases |
| Cartesian product | Pairs every row from one relation with every row from another. | `CROSS JOIN` |
| Union | Includes tuples found in either relation. | `UNION` |
| Difference | Keeps tuples in the first relation but not the second. | `EXCEPT` |

Union and difference need compatible inputs: the same number of attributes, with matching domains in corresponding positions. PostgreSQL checks that the SQL result columns can be combined with compatible types. Attribute names alone do not line rows up. Column position matters.

## Read an expression from the inside out

Suppose `Employees(employee_id, department_id, salary)` holds employee records. This expression finds the departments with an employee earning at least 50,000:

```text
project department_id (
    select salary >= 50000 (Employees)
)
```

First, selection keeps qualifying employees. Then projection keeps their department IDs and removes repeats.

```sql
CREATE TEMP TABLE employees (
    employee_id INTEGER PRIMARY KEY,
    department_id INTEGER NOT NULL,
    salary INTEGER NOT NULL
);

INSERT INTO employees VALUES
    (1, 10, 60000),
    (2, 10, 55000),
    (3, 20, 40000),
    (4, 30, 70000);

SELECT DISTINCT department_id
FROM employees
WHERE salary >= 50000
ORDER BY department_id;
```

The result is `10` and `30`. Without `DISTINCT`, department `10` appears twice. `ORDER BY` makes the display order predictable; order is not part of the relation itself.

## Build more from the basics

An intersection can be written as `R - (R - S)`. A join can be built by taking a Cartesian product, selecting matching pairs, and projecting the wanted attributes. In real SQL, write `JOIN ... ON ...` because it states the match clearly. If the left side of a product has 3 rows and the right side has 4, the product has 12 rows before a filter removes any.

SQL has several differences to remember. `UNION` and `EXCEPT` remove duplicate rows by default; `UNION ALL` and `EXCEPT ALL` keep counts. `WHERE` drops rows where the condition is false or unknown because of `NULL`. Classic relational algebra does not include `NULL` or an ordering operation.

## Try it yourself

1. What changes in the example if `DISTINCT` is removed?
2. Write an expression using selection and projection for IDs of employees in department `10`.
3. Why is `SELECT department_id FROM employees` not always the same as relational projection?

## References

- [MIT Database Systems lecture on relational algebra](https://ocw.mit.edu/courses/6-830-database-systems-fall-2010/8d7652b95f032eab2dcd6320d8a9f1c7_MIT6_830F10_lec02.pdf)
- [PostgreSQL combining queries](https://www.postgresql.org/docs/current/queries-union.html)
