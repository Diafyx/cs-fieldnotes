# Fieldnotes

Fieldnotes is a personal study site for SQL, DBMS, operating systems, computer networks, object-oriented programming, and low-level design. The site is built from Markdown and plain Python. It has no package installation step.

## Run it locally

From this directory:

```text
python build.py
python -m http.server 8000 --directory dist
```

Open `http://localhost:8000` in a browser. Stop the server with `Ctrl+C`. Run `python build.py` again after editing a note.

## How the content is organized

- `source-topics.md` is the course inventory for this site. It contains the included subjects and leaves out DSA and C++.
- `content/<subject>/<topic>.md` holds reviewed articles. Each file starts with the exact topic heading.
- `build.py` maps every included heading to a page. An exact title repeated in several courses uses one article. SQL topics repeated in DBMS also use one article.
- `dist/` is the generated static site. It can be served by any host that serves plain files.
- `scripts/check.py` checks inventory counts, generated links, duplicate HTML IDs, and the writing rules.

The subject pages list every heading, including those that still need an article. Planned headings are clearly marked. The coverage page shows how many articles are ready. This keeps gaps visible while the writing continues.

## Writing a new article

1. Find the exact title in `source-topics.md`.
2. Find its generated slug in `dist/catalog.json` or use the lowercase words joined with hyphens.
3. Add `content/<subject>/<slug>.md` with that exact title as the first heading.
4. Follow `CONTENT_GUIDE.md`.
5. Run `python build.py`, `python scripts/check.py`, `python scripts/check_examples.py`, `python scripts/check_querying_examples.py`, `python scripts/check_aggregation_examples.py`, `python scripts/check_functions_examples.py`, `python scripts/check_modification_examples.py`, `python scripts/check_set_examples.py`, `python scripts/check_join_examples.py`, `python scripts/check_transaction_examples.py`, `python scripts/check_subquery_examples.py`, `python scripts/check_cte_examples.py`, `python scripts/check_date_examples.py`, `python scripts/check_window_examples.py`, `python scripts/check_json_examples.py`, and `python scripts/check_design_examples.py`.

The site uses PostgreSQL for SQL examples unless an article says otherwise. Python and Java are the application languages used in examples. No C++ examples are planned.

## Deploy with GitHub and Cloudflare Pages

Make this `tuf-study` directory the root of a new GitHub repository. Create an empty repository on GitHub first. Leave its README, license, and `.gitignore` options unchecked because this directory already has a README and `.gitignore`.

Run the Git commands yourself from this directory. The first push should go to the repository's `main` branch. Then, in Cloudflare, open **Workers & Pages**, create a **Pages** application, and import the GitHub repository. Use these settings:

| Setting | Value |
| --- | --- |
| Production branch | `main` |
| Framework preset | `None` |
| Root directory | Leave blank |
| Build command | `python3 build.py` |
| Build output directory | `dist` |

Cloudflare builds `dist/` from the source files on each push. The generated directory is ignored by Git. There are no package dependencies to install.
