# Multivalued Dependencies, 4NF, Join Dependencies, and 5NF

Functional dependencies say one value determines another value. A multivalued dependency, or MVD, says one value determines a **set** of values that varies independently from the other attributes. This can cause repeated combinations even when a table is in BCNF.

## Independent lists and 4NF

Suppose a person has several languages and several hobbies, and every language can appear with every hobby. `PersonActivity(person, language, hobby)` might contain:

| person | language | hobby |
| --- | --- | --- |
| Mina | English | Chess |
| Mina | English | Cycling |
| Mina | Hindi | Chess |
| Mina | Hindi | Cycling |

The rule is `person ->> language`, read as "person multidetermines language." Because the language choices are independent of hobbies, `person ->> hobby` holds too. If there are two languages and two hobbies, the combined table needs four rows. Adding one new language means adding a row for every hobby. The table can be in BCNF when it has no nontrivial FDs, yet it still repeats facts.

An MVD `X ->> Y` is nontrivial when `Y` is not already inside `X` and `X` together with `Y` does not cover all attributes. A relation is in **4NF** when every nontrivial MVD has a superkey on its left side. `person` is not a key for the three-column example, so the MVD breaks 4NF.

Split the table into `PersonLanguage(person, language)` and `PersonHobby(person, hobby)`. Their join recreates the four combinations if independence is a real rule. The following PostgreSQL example shows the split:

```sql
CREATE TEMP TABLE person_languages (
    person TEXT NOT NULL,
    language TEXT NOT NULL,
    PRIMARY KEY (person, language)
);

CREATE TEMP TABLE person_hobbies (
    person TEXT NOT NULL,
    hobby TEXT NOT NULL,
    PRIMARY KEY (person, hobby)
);

INSERT INTO person_languages VALUES
    ('Mina', 'English'),
    ('Mina', 'Hindi');

INSERT INTO person_hobbies VALUES
    ('Mina', 'Chess'),
    ('Mina', 'Cycling');

SELECT l.person, l.language, h.hobby
FROM person_languages AS l
JOIN person_hobbies AS h ON h.person = l.person
ORDER BY l.person, l.language, h.hobby;
```

The result is the four rows in the table above, ordered by language and hobby. If a language-hobby pair is itself a real fact, such as a person's ability to discuss a hobby in that language, the two lists are **not** independent. Splitting them would invent combinations. The meaning of the data decides whether the MVD holds.

## Join dependencies and 5NF

A join dependency says a relation can always be recovered by joining specified projections of itself. An MVD is a two-piece case of this idea. **5NF**, also called projection-join normal form, rules out nontrivial join dependencies that are not implied by candidate keys. It addresses cases where three or more projections are needed to remove repetition.

Consider `Allowed(agent, product, company)`. Suppose a triple is allowed exactly when all three pair facts hold: the agent represents the company, the company carries the product, and the agent is qualified for the product. Then the triple relation can be rebuilt from `AgentCompany(agent, company)`, `CompanyProduct(company, product)`, and `AgentProduct(agent, product)`. For one agent, two companies, and two products, the pair facts may produce `(A, P, X)`, `(A, Q, X)`, and `(A, P, Y)` but not `(A, Q, Y)` if company `Y` does not carry `Q`. This is a three-piece join dependency, not a claim that every agent-company pair combines with every product.

This split is valid only if the three pair facts completely decide whether a triple is allowed. If each triple is a separate contract or approval, joining the pairs may invent a false approval. Keep the triple table in that case. Higher normal forms depend on rules about **all valid states**, not just a pattern in current rows.

4NF and 5NF are useful when independent sets or reconstructable triples cause real duplication. They are not instructions to split every three-column table. Check the intended meaning, the lossless join, and the constraints needed to keep the pieces valid.

## Try it yourself

1. If Mina adds a third independent hobby, how many rows must the combined language-hobby table add? How many rows must the split tables add?
2. What false row might appear if a language and hobby are linked by a real qualification rule?
3. In the agent example, what extra business rule makes the three pair tables enough to decide every allowed triple?

## References

- [UIC database design slides on MVDs and join dependencies](https://www.cs.uic.edu/~bglavic/cs480/2025-spring/pdfs/slides/ch06-db-design-handout.pdf)
- [Duke normalization lecture notes](https://courses.cs.duke.edu/fall18/cps216/Lectures/Lecture-5-Normalization-notes.pdf)
