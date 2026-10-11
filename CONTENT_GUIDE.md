# Content guide

The goal is a set of notes that answers the question a learner actually has. A page should make one concept clear, show it working, and name the cases where it breaks or changes. Length follows the concept. Extra words do not make an article complete.

## Writing rules

- Use simple English and short sentences. Write as a careful teacher would speak.
- Use the exact topic title from the inventory as the first heading.
- State the database or language version when behavior differs between systems.
- Show a small example that can be checked. Explain the expected result, not just the syntax.
- Explain at least one common mistake or edge case when the topic has one.
- Use Python or Java for application code. Use PostgreSQL for SQL examples unless the article says otherwise.
- Link to primary documentation for facts that depend on a product or version.
- Ask practice questions that test understanding. Do not repeat a sentence from the article as a question.
- Write original prose. Do not copy a course lesson or documentation page.
- Do not use em dashes, en dashes, decorative icons, emojis, or filler phrases.
- Do not claim an example was run unless it was run.

## Review before calling a page ready

1. Can a reader say what the concept means after the first two paragraphs?
2. Does the example match the explanation and the named SQL dialect?
3. Are important cases such as `NULL`, ties, transactions, or concurrent work covered when they matter?
4. Are broad claims supported by current primary documentation?
5. Could a beginner follow every variable and table in the example?
6. Is the page linked to every matching course heading without hiding a distinct topic?
7. Does the page avoid repeated paragraphs that only make it longer?

## Shared pages

Exact titles shared by courses automatically point to one article. Titles that look similar are reviewed by hand before they are combined. Two labels can sound alike and still ask different questions. Keep both in the inventory until the shared article covers both fully.

## Current writing order

Start with SQL, then DBMS, operating systems, computer networks, object-oriented programming, and low-level design. Work through foundations before advanced topics and practice problems. Practice problems need a clear question, test data, a reasoned solution, and checks for edge cases.
