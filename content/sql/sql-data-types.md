# SQL Data Types

A column's data type tells the database what values it can hold and what operations make sense. A price, a sentence, and a time are different kinds of data. Choosing a type is part of designing the meaning of a table, not just a way to save space.

These examples use PostgreSQL names. Other databases have similar ideas but do not always use the same type names or rules.

## Common choices

- `integer` and `bigint` hold whole numbers. Use `bigint` when the expected range may exceed `integer`.
- `numeric(precision, scale)` holds exact decimal values. It suits money amounts when the required number of digits is known.
- `double precision` holds approximate floating point values. It suits measurements where a small representation error is acceptable.
- `text` holds variable-length strings. `varchar(n)` adds a length limit when the limit is a real rule.
- `boolean` holds true or false, and can also hold `NULL` unless you add `NOT NULL`.
- `date` holds a calendar date. `timestamptz` holds a point in time with time zone handling.
- `uuid` holds a UUID. `jsonb` holds JSON data that PostgreSQL can query and index.

## A table with deliberate types

```sql
CREATE TABLE payments (
    payment_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    customer_id bigint NOT NULL,
    amount numeric(12, 2) NOT NULL CHECK (amount >= 0),
    currency_code varchar(3) NOT NULL,
    paid_at timestamptz,
    refunded boolean NOT NULL DEFAULT false
);
```

`amount` has two decimal places and must be non-negative. `paid_at` is nullable because a payment may exist before it is completed. `refunded` has a clear default. The `currency_code` length limit does not prove that the code is valid. You would need another rule, such as a check or a reference table, for that.

## Exact and approximate numbers

Binary floating point cannot represent every decimal fraction exactly. If you add a number like `0.1` many times, a floating point result may contain a tiny error. Use `numeric` for exact decimal accounting. Use floating point for scientific measurements when its range and speed are useful and the approximation is understood.

Do not store a price as text. Text sorting would put values in string order, and arithmetic would require conversion. Do not store a calendar date as text unless you have a strong reason. A date type makes invalid dates harder to store and supports date operations directly.

## Time is a design decision

In PostgreSQL, `timestamp` without a qualifier means a date and clock time without time zone information. `timestamptz` represents a specific instant. PostgreSQL stores it in a time zone independent form and displays it according to the session time zone. If an event happened at a real moment, such as a payment or login, `timestamptz` is usually the clearer choice. A shop's opening time, which repeats at a local wall clock time, is a different problem.

## Check your understanding

1. Why is `numeric(12, 2)` a better starting point than `double precision` for a billed amount?
2. Should a birthday be a `date` or a `timestamptz`? Why?
3. Does `varchar(3)` prove that a currency code is real?

## Further reading

- [PostgreSQL data types](https://www.postgresql.org/docs/current/datatype.html)
- [PostgreSQL numeric types](https://www.postgresql.org/docs/current/datatype-numeric.html)
- [PostgreSQL date and time types](https://www.postgresql.org/docs/current/datatype-datetime.html)
