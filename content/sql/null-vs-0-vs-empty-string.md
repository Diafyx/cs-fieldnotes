# NULL vs 0 vs Empty String

`NULL`, `0`, and `''` mean different things. `NULL` means the value is missing or unknown. `0` is a known number. `''` is a known text value with no characters. Treating them as interchangeable hides information and often changes query results.

Suppose an `employees` table has a `bonus` column. A bonus of `0` means the employee has a known bonus amount of zero. A `NULL` bonus might mean no amount has been entered yet. That is a different fact.

## Comparisons with NULL

Ordinary comparisons with `NULL` do not return true or false. They return unknown. That includes `bonus = NULL` and `bonus <> NULL`. Use `IS NULL` or `IS NOT NULL` instead:

```sql
SELECT employee_id
FROM employees
WHERE bonus IS NULL;
```

A `WHERE` clause keeps rows only when its condition is true. It drops rows when the condition is false or unknown. This explains a common surprise:

```sql
SELECT employee_id
FROM employees
WHERE bonus <> 0;
```

This query does not include rows where `bonus` is `NULL`. If you want known nonzero bonuses, that is correct. If you also want missing bonuses, state that explicitly with `OR bonus IS NULL`.

## Empty text is still a value

In PostgreSQL, `''` is an empty string and is different from `NULL`. A form might submit an empty string for an optional nickname. Decide whether that should mean "the user chose an empty nickname" or "we do not know the nickname". If both forms mean the same thing in your application, normalize them before or when you store the value.

```sql
SELECT NULLIF(TRIM(nickname), '') AS cleaned_nickname
FROM profiles;
```

`TRIM` removes surrounding spaces. `NULLIF` returns `NULL` when the trimmed result is empty. Use this only if blank input really should count as missing.

## Aggregates and defaults

`COUNT(*)` counts rows. `COUNT(bonus)` counts rows with a non-`NULL` bonus. Many aggregates ignore `NULL` input values. `COALESCE(bonus, 0)` can replace a missing value for a calculation, but it does not prove the missing bonus was actually zero.

```sql
SELECT COUNT(*) AS employees,
       COUNT(bonus) AS known_bonuses,
       SUM(bonus) AS total_known_bonuses
FROM employees;
```

## Check your understanding

1. If five employees exist and two have `NULL` bonuses, what do `COUNT(*)` and `COUNT(bonus)` return?
2. Why does `bonus = NULL` fail to find missing bonuses?
3. When might an empty string carry meaning that `NULL` does not?

## Further reading

- [PostgreSQL comparison with NULL](https://www.postgresql.org/docs/current/functions-comparison.html)
- [PostgreSQL conditional expressions](https://www.postgresql.org/docs/current/functions-conditional.html)
- [PostgreSQL aggregate functions](https://www.postgresql.org/docs/current/functions-aggregate.html)
