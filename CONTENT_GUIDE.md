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

## Workflow for each content module

1. Work on one module at a time. Read its headings in `source-topics.md`, the related finished pages, and the relevant primary documentation before writing.
2. Account for every included heading. DSA and C++ are outside this site's content scope. Keep distinct concepts separate. Use one shared page only when it fully answers each heading that points to it.
3. Plan the module's coverage before writing. Include the basic idea, how it works, a checked example, important rules and limits, common mistakes, and useful practice. Give a broad topic enough space to answer the questions its title raises. Do not add length just to make a page look complete.
4. Keep the article pattern: exact source title as the first heading, a direct opening explanation, small worked examples with their expected results, clear sections for the important cases, `Try it yourself`, and `References`. Add sections when the concept needs them.
5. Use plain, human English throughout the articles, examples, headings, and site text. Prefer short sentences and familiar words. Avoid stock introductions, filler, em dashes, en dashes, decorative symbols, and claims that are stronger than the evidence.
6. Check calculations, timelines, and code outputs before publishing them. Add a focused checker for new kinds of worked examples when it helps catch real errors. Say what was checked. Do not say SQL or code ran when it did not.
7. Run `python build.py` and the relevant scripts in `scripts` after a module. Review the build summary and resolve missing links, duplicate headings, and checker failures before calling the module done.

All project work stays inside this workspace. The owner runs Git commands and pushes changes. Do not run Git commands while working on this project.
