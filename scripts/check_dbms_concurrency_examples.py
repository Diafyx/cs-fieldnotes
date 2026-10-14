"""Check deterministic SQL, Python, and schedule examples in DBMS concurrency.

SQLite checks single-session results. It cannot replace the two-session
PostgreSQL deadlock and isolation exercises.
"""

from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
import re
import sqlite3


CONTENT = Path(__file__).resolve().parents[1] / "content" / "dbms"
SQL_EXPECTED = {
    "transaction-concepts-acid-and-states": [(1, 70), (2, 80)],
    "lock-based-protocols-and-two-phase-locking": [("PEN", 4)],
    "timestamp-ordering-optimistic-control-and-mvcc": [(1, 0, 1)],
}


def blocks(slug, language):
    article = (CONTENT / f"{slug}.md").read_text(encoding="utf-8")
    return re.findall(rf"```{language}\n(.*?)\n```", article, flags=re.DOTALL)


def operations(text):
    return [(kind, int(tx), item) for kind, tx, item in
            re.findall(r"([rwca])(\d+)(?:\(([A-Z])\))?", text)]


def conflict_edges(ops):
    edges = set()
    for i, (first_kind, first_tx, first_item) in enumerate(ops):
        if first_kind not in "rw":
            continue
        for second_kind, second_tx, second_item in ops[i + 1:]:
            if (second_kind in "rw" and first_tx != second_tx
                    and first_item == second_item
                    and "w" in (first_kind, second_kind)):
                edges.add((first_tx, second_tx))
    return edges


def schedule_classes(ops):
    commits = {tx: i for i, (kind, tx, _) in enumerate(ops) if kind == "c"}
    finishes = {tx: i for i, (kind, tx, _) in enumerate(ops) if kind in "ca"}
    latest_writer = {}
    recoverable = cascadeless = strict = True
    for i, (kind, tx, item) in enumerate(ops):
        if kind in "rw" and item in latest_writer:
            writer, _ = latest_writer[item]
            if writer != tx and i < finishes.get(writer, float("inf")):
                strict = False
            if kind == "r" and writer != tx:
                if commits.get(writer, float("inf")) > i:
                    cascadeless = False
                if commits.get(writer, float("inf")) > commits.get(tx, float("inf")):
                    recoverable = False
        if kind == "w":
            latest_writer[item] = (tx, i)
    return recoverable, cascadeless, strict


def main():
    for slug, expected in SQL_EXPECTED.items():
        sql = blocks(slug, "sql")
        assert len(sql) == 1, f"Expected one SQL block in {slug}"
        portable = sql[0].replace(" FOR UPDATE", "")
        setup, query = portable.rsplit("\nSELECT ", 1)
        with sqlite3.connect(":memory:") as db:
            db.executescript(setup)
            actual = db.execute("SELECT " + query).fetchall()
            if slug.startswith("timestamp-ordering"):
                update = re.search(r"UPDATE seats\n.*?;", portable, re.DOTALL).group(0)
                assert db.execute(update).rowcount == 0, "Stale version changed a seat"
        assert actual == expected, f"Wrong result in {slug}: {actual}"

    model = blocks("schedules-and-concurrency-anomalies", "python")
    assert len(model) == 1
    output = StringIO()
    with redirect_stdout(output):
        exec(compile(model[0], "lost update model", "exec"), {})
    assert output.getvalue().strip() == "80"

    graphs = blocks("conflict-and-view-serializability", "text")
    assert len(graphs) == 3
    assert conflict_edges(operations(graphs[0])) == {(1, 2)}
    assert conflict_edges(operations(graphs[1])) == {(1, 2), (2, 1)}
    assert conflict_edges(operations(graphs[2])) == {(1, 2), (2, 1)}

    schedules = blocks("recoverable-cascadeless-and-strict-schedules", "text")
    assert len(schedules) == 1
    expected = {
        "A": (False, False, False),
        "B": (True, False, False),
        "C": (True, True, True),
        "D": (True, True, False),
    }
    for line in schedules[0].splitlines():
        label, trace = line.split(": ", 1)
        assert schedule_classes(operations(trace)) == expected[label], label

    print("Checked 3 SQL results, a lost update, conflict graphs, and schedule classes.")


if __name__ == "__main__":
    main()
