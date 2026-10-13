# Entity and Attributes

An entity is a thing the system needs to track. An attribute is a fact about that thing. A person can be an entity; their name and birth date can be attributes. The names of tables and columns should say what one row and one value mean.

## One person, several phone numbers

```sql
CREATE TEMP TABLE people (
  person_id integer PRIMARY KEY,
  name text NOT NULL,
  birth_date date
);

CREATE TEMP TABLE person_phones (
  person_id integer NOT NULL REFERENCES people(person_id),
  phone_number text NOT NULL,
  PRIMARY KEY (person_id, phone_number)
);

INSERT INTO people VALUES (1, 'Ada', '1998-05-12'), (2, 'Ben', NULL);
INSERT INTO person_phones VALUES
  (1, '+1-555-0101'), (1, '+1-555-0102');

SELECT p.person_id, p.name, ph.phone_number
FROM people AS p
LEFT JOIN person_phones AS ph ON ph.person_id = p.person_id
ORDER BY p.person_id, ph.phone_number;
```

Ada appears twice, once for each phone number. Ben appears once with SQL `NULL` for `phone_number`. The person row does not need `phone_1` and `phone_2` columns. The phone table allows any number of phones and prevents the same exact number from appearing twice for one person.

An attribute can be required or optional. `name` is required here; `birth_date` is optional. SQL `NULL` for birth date means the database has no value, not that the person has no birth date in real life. Use the right type for each value. A phone number is text because it may contain `+`, leading zeros, and formatting. It is not a quantity to add.

Some attributes are derived. Age changes as time passes, so storing age beside birth date creates a value that can become stale. Calculate it when needed. Some values are historical instead: an address used for a shipped order may need to stay on that order even after a person changes their current address.

Do not assume names identify people. Two people can share a name, and one person can change theirs. The primary key gives each person a stable row identity. Before marking an attribute `UNIQUE`, ask whether the real business rule truly guarantees uniqueness.

## Check your understanding

1. Why is a phone number stored as text?
2. Why does Ben still appear in the left join result?
3. Why is `name` a poor primary key for people?

## Further reading

- [Chen's entity and relationship model](https://doi.org/10.1145/320434.320440)
- [PostgreSQL column types](https://www.postgresql.org/docs/current/datatype.html)
