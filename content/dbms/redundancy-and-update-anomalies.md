# Redundancy and Update Anomalies

Redundancy means storing the same fact in more than one place. It is sometimes useful, but it can make a database disagree with itself. If a department name is copied into every employee row, changing that name means changing every copy.

Suppose each employee belongs to one department, and a department ID always has one name. A wide table might look like this:

| employee_id | employee_name | department_id | department_name |
| --- | --- | --- | --- |
| 1 | Mina | 10 | Support |
| 2 | Dev | 10 | Support |
| 3 | Lee | 20 | Research |

The fact `10 = Support` appears twice. The table can suffer three common problems:

| Problem | What could happen |
| --- | --- |
| Update anomaly | One employee row says `Support`; another says `Customer Support`. |
| Insert anomaly | You cannot store a new department until it has an employee, unless you allow an incomplete employee row. |
| Delete anomaly | Deleting the last employee in Research also loses the only stored fact about that department. |

## Store each fact once

Put department facts in `departments` and employee facts in `employees`. The employee row stores the department ID, not a copy of the department name. A foreign key makes sure that the ID points to a real department.

```sql
CREATE TEMP TABLE departments (
    department_id INTEGER PRIMARY KEY,
    department_name TEXT NOT NULL
);

CREATE TEMP TABLE employees (
    employee_id INTEGER PRIMARY KEY,
    employee_name TEXT NOT NULL,
    department_id INTEGER NOT NULL REFERENCES departments(department_id)
);

INSERT INTO departments VALUES
    (10, 'Support'),
    (20, 'Research'),
    (30, 'Legal');

INSERT INTO employees VALUES
    (1, 'Mina', 10),
    (2, 'Dev', 10),
    (3, 'Lee', 20);

SELECT e.employee_name, d.department_name
FROM employees AS e
JOIN departments AS d ON d.department_id = e.department_id
ORDER BY e.employee_id;
```

The result is `(Mina, Support)`, `(Dev, Support)`, and `(Lee, Research)`. Legal has no employee yet, but it is still stored. Updating department `10` changes one row in `departments`; later joins show its new name for both employees.

This design follows the rule `department_id -> department_name`: one department ID determines one department name. The rule is about the meaning of the data. A few sample rows cannot prove it. Ask the business owner whether IDs can be reused or names can change before treating it as a permanent rule.

## When repeated data is intentional

Sometimes a copied value is a separate historical fact. For example, an order line may store the price charged at purchase time even if today's product price changes. That is not an accidental duplicate of the current price. It has a different meaning. A cached total or a materialized view can also repeat data for speed, but then you need a clear update or refresh rule.

Splitting tables can add joins, so check the queries that matter. Still, do not keep conflicting copies merely to avoid a join. First decide which facts exist and what determines each fact.

## Try it yourself

1. Which anomaly occurs if the only employee in Legal is deleted from the wide table?
2. Why does the two-table design allow a department with no employees?
3. Is an order's original purchase price a duplicate of the product's current price? Explain the difference.

## References

- [MIT Database Systems lecture on schema design](https://ocw.mit.edu/courses/6-830-database-systems-fall-2010/a9c47ed7d80c1bfc51d0baf7ac545398_MIT6_830F10_lec03.pdf)
- [PostgreSQL foreign key constraints](https://www.postgresql.org/docs/current/ddl-constraints.html#DDL-CONSTRAINTS-FK)
