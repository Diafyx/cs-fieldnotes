# Most Frequent Travellers

A trip table records one row per trip. Join it to travellers, count trips per person, then sort by count to find the most frequent travellers.

## The question

Return the top two travellers with their trip counts. Break equal counts by name, then by user ID. Include people with zero trips when making the ranked list.

```sql
CREATE TEMP TABLE travellers (
  user_id integer PRIMARY KEY,
  name text NOT NULL
);
CREATE TEMP TABLE trips (
  trip_id integer PRIMARY KEY,
  user_id integer NOT NULL
);

INSERT INTO travellers VALUES
  (1, 'Asha'), (2, 'Ben'), (3, 'Cara'), (4, 'Dev');
INSERT INTO trips VALUES
  (10, 1), (11, 1),
  (12, 2), (13, 2),
  (14, 3);
```

## A solution

```sql
SELECT u.user_id, u.name,
       COUNT(t.trip_id) AS trip_count
FROM travellers AS u
LEFT JOIN trips AS t ON t.user_id = u.user_id
GROUP BY u.user_id, u.name
ORDER BY trip_count DESC, u.name, u.user_id
LIMIT 2;
```

The answer is Asha with 2 trips, then Ben with 2 trips. Their equal counts are settled by name. Cara has 1; Dev has 0. `COUNT(t.trip_id)` ignores the missing trip row created by Dev's left join. `COUNT(*)` would call that one trip.

`LIMIT 2` returns exactly two rows when at least two travellers exist. If the task wanted *everyone tied* for second place, a plain limit would be wrong. A rank-based rule would be needed. A date range or trip status can also change what counts as a trip; put such restrictions in the join condition if zero-trip travellers must remain.

## Check your understanding

1. Why does Asha come before Ben?
2. Why does Dev have count zero with `COUNT(t.trip_id)`?
3. What changes if all travellers tied for second place must be shown?

## Further reading

- [PostgreSQL joined tables](https://www.postgresql.org/docs/current/queries-table-expressions.html#QUERIES-JOIN)
- [PostgreSQL sorting and limits](https://www.postgresql.org/docs/current/queries-order.html)
