# Special Bonus Calculation

This exercise gives an employee a bonus equal to their salary when two rules are true: their ID is odd, and their name does not start with the capital letter `M`. All other employees get zero.

## The question

Return every employee ID and the calculated `bonus`, sorted by ID. The calculation does not update salary.

```sql
CREATE TEMP TABLE bonus_employees (
  employee_id integer PRIMARY KEY,
  name text NOT NULL,
  salary numeric(12, 2) NOT NULL
);

INSERT INTO bonus_employees (employee_id, name, salary) VALUES
  (1, 'Anya', 1000.00),
  (2, 'Ben', 1200.00),
  (3, 'Mina', 900.00),
  (5, 'Moe', 700.00),
  (7, 'Cara', 1500.00);
```

## A solution

```sql
SELECT employee_id,
       CASE
         WHEN employee_id % 2 = 1
          AND name NOT LIKE 'M%' THEN salary
         ELSE 0
       END AS bonus
FROM bonus_employees
ORDER BY employee_id;
```

The bonuses for IDs 1, 2, 3, 5, and 7 are 1000, 0, 0, 0, and 1500. ID 2 is even. IDs 3 and 5 have names starting with `M`. The result for an eligible employee is a bonus amount equal to salary, not salary plus bonus.

The rule names a capital `M`. Under an ordinary case-sensitive collation, a name starting with lowercase `m` is different. If the rule should ignore case, decide that explicitly and use an appropriate comparison. The sample uses positive IDs and non-null names.

## Check your understanding

1. Why does employee 3 receive zero?
2. Would `employee_id % 2 = 0` select the right employees?
3. Does this query change employee salaries?

## Further reading

- [LeetCode Calculate Special Bonus](https://leetcode.com/problems/calculate-special-bonus/)
- [PostgreSQL pattern matching](https://www.postgresql.org/docs/current/functions-matching.html)
