# ROUND() and ABS()

`ROUND` changes the number of decimal places in a result. `ABS` removes a number's sign. They answer different questions. `ROUND` is for presentation or a rule that requires rounded values. `ABS` is for size without direction.

## Round a decimal value

```sql
SELECT ROUND(42.4382::numeric, 2) AS cents,
       ROUND(1234.56::numeric, -1) AS nearest_ten;
```

PostgreSQL returns 42.44 and 1230. A positive second argument means decimal places. A negative one means places to the left of the decimal point.

For PostgreSQL `numeric`, a value exactly halfway between two rounded results is rounded away from zero. For example, `ROUND(2.5::numeric)` is 3 and `ROUND(-2.5::numeric)` is -3. Floating point values can behave differently because their tie rule depends on the platform. Use `numeric` when an exact decimal rule matters.

## Find magnitude with ABS

```sql
SELECT ABS(-17.4::numeric) AS magnitude,
       ABS(17.4::numeric) AS same_magnitude;
```

Both values are 17.4. `ABS` does not say whether the original value was a gain or a loss. If that direction matters, keep the original signed column too.

## Rounding before or after a total

Rounding each line first can give a different sum from rounding the final sum. For two values of 1.005, rounding each to two places gives 1.01 + 1.01 = 2.02 in PostgreSQL `numeric`. Adding first gives 2.010, which rounds to 2.01. A billing rule must say which order to use. Do not move `ROUND` around an aggregate without checking the rule.

If the input is `NULL`, either function returns `NULL`. `ROUND` does not turn missing data into zero.

## Check your understanding

1. What does a negative second argument to `ROUND` change?
2. Why can rounding each line differ from rounding the total?
3. What information does `ABS(-17.4)` lose?

## Further reading

- [PostgreSQL mathematical functions](https://www.postgresql.org/docs/current/functions-math.html)
- [PostgreSQL numeric types](https://www.postgresql.org/docs/current/datatype-numeric.html)
