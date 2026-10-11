# Safe Investment Countries

For this exercise, a country qualifies when the average duration of calls involving its people is higher than the average duration of all calls. Count a call for the caller's country and for the receiver's country. A call between countries belongs to both countries' averages.

## Sample data

```sql
CREATE TEMP TABLE countries (country_id integer PRIMARY KEY, name text NOT NULL);
CREATE TEMP TABLE people (person_id integer PRIMARY KEY, country_id integer NOT NULL);
CREATE TEMP TABLE calls (caller_id integer, receiver_id integer, duration integer NOT NULL);
INSERT INTO countries VALUES (1, 'North'), (2, 'South');
INSERT INTO people VALUES (1, 1), (2, 1), (3, 2), (4, 2);
INSERT INTO calls VALUES (1, 2, 10), (2, 1, 20), (3, 4, 80), (1, 3, 20);
```

## Solution

```sql
SELECT c.country_id, c.name
FROM countries AS c
JOIN people AS p ON p.country_id = c.country_id
JOIN calls AS cl ON cl.caller_id = p.person_id
                OR cl.receiver_id = p.person_id
GROUP BY c.country_id, c.name
HAVING AVG(cl.duration) > (SELECT AVG(duration) FROM calls)
ORDER BY c.country_id;
```

The answer is South. The overall average is 32.5 because each call appears once in `calls`. North's country average is 16: its two internal calls each count for both participants, and the cross-country call counts once. South's average is 60: its internal call counts twice, and the cross-country call counts once. The scalar subquery gives the same global benchmark to every country group.

A country with no calls involving its people has no group in this query. If the rule needs to show those countries with a special value, start from `countries` with an outer join and decide what an undefined average means. The sample stores each person's country directly; a version with phone number prefixes needs a separate lookup from prefix to country.

## Check your understanding

1. Why does the cross-country call count once for each country?
2. Why does an internal call count twice in its country's average?
3. Should a country with no calls qualify under the stated rule?

## Further reading

- [PostgreSQL aggregate functions](https://www.postgresql.org/docs/current/functions-aggregate.html)
- [PostgreSQL grouping](https://www.postgresql.org/docs/current/queries-table-expressions.html#QUERIES-GROUP)
- [Related investment countries problem](https://leetcode.com/problems/countries-you-can-safely-invest-in/)
