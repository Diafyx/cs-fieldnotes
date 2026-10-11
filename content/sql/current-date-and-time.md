# Current Date and Time

PostgreSQL has several meanings of “now.” `CURRENT_DATE` is today's date in the session time zone. `CURRENT_TIMESTAMP` and `now()` give the start time of the current transaction. They stay the same even when a long transaction runs several statements.

## Check the transaction time

```sql
SELECT CURRENT_TIMESTAMP = now() AS same_transaction_time;
```

PostgreSQL returns `true`. Both expressions refer to the same transaction start. This result is stable even though the exact timestamp changes from one transaction to another. `CURRENT_TIMESTAMP` includes time zone information in its type. `LOCALTIMESTAMP` does not.

## Choose the clock you mean

`statement_timestamp()` gives the time the current statement started. `clock_timestamp()` reads the actual clock when it is called and can change inside one statement. Use the transaction time when all writes in one transaction should share a timestamp. Use the wall clock when you need the time of a later action inside a long transaction.

`CURRENT_DATE` comes from the transaction's start time in the session time zone. If a transaction crosses local midnight, it can still report the earlier date. For a report about a local calendar day, name the intended zone rather than assuming every session uses the same one. A stored `timestamp with time zone` is displayed using the session's zone, so two sessions can print different clock times for the same instant.

For an insert time, a column default such as `DEFAULT CURRENT_TIMESTAMP` gives each inserted row a transaction-time value. Avoid treating a timestamp string written into a saved view definition as a live clock. Prefer the function or SQL keyword when a value must be current at execution.

## Check your understanding

1. Why does the example return true?
2. Which function can change during one statement?
3. What date can `CURRENT_DATE` report after a long transaction crosses midnight?

## Further reading

- [PostgreSQL current date and time functions](https://www.postgresql.org/docs/current/functions-datetime.html#FUNCTIONS-DATETIME-CURRENT)
- [PostgreSQL time zone behavior](https://www.postgresql.org/docs/current/datatype-datetime.html)
