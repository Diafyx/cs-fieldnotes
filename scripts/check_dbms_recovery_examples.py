"""Check the SQL rollback and the two DBMS recovery timelines."""

from pathlib import Path
import re
import sqlite3


CONTENT = Path(__file__).resolve().parents[1] / "content" / "dbms"


def article(slug):
    return (CONTENT / f"{slug}.md").read_text(encoding="utf-8")


def recover(initial, updates, committed):
    """Repeat history, then undo uncommitted updates in reverse order."""
    state = initial.copy()
    history = []
    for tx, item, new_value in updates:
        history.append((tx, item, state[item]))
        state[item] = new_value
    for tx, item, old_value in reversed(history):
        if tx not in committed:
            state[item] = old_value
    return state


def main():
    text = article("failures-storage-and-recovery-goals")
    blocks = re.findall(r"```sql\n(.*?)\n```", text, re.DOTALL)
    assert len(blocks) == 1, "Expected one rollback example"
    setup, query = blocks[0].rsplit("\nSELECT ", 1)
    with sqlite3.connect(":memory:") as db:
        db.executescript(setup)
        balance = db.execute("SELECT " + query).fetchone()[0]
    assert balance == 120, f"Rollback example returned {balance}"

    text = article("log-based-recovery-and-write-ahead-logging")
    rows = re.findall(
        r"\| \d+ \| (T\d+) \| Set ([AB]) from `(\d+)` to `(\d+)`\.",
        text,
    )
    assert len(rows) == 3, "Expected three WAL changes"
    updates = []
    state = {"A": 100, "B": 50}
    for tx, item, old, new in rows:
        assert state[item] == int(old), f"Wrong before value at {tx}, {item}"
        state[item] = int(new)
        updates.append((tx, item, int(new)))
    assert state == {"A": 89, "B": 70}
    assert recover({"A": 100, "B": 50}, updates, {"T1"}) == {"A": 80, "B": 70}

    text = article("checkpoints-and-aries-intuition")
    rows = re.findall(r"\| \d+ \| (T\d+) sets ([AB]) to `(\d+)`\. \|", text)
    assert len(rows) == 3, "Expected three ARIES changes"
    updates = [(tx, item, int(value)) for tx, item, value in rows]
    assert recover({"A": 100, "B": 50}, updates, {"T1"}) == {"A": 80, "B": 50}

    print("Checked recovery rollback, WAL timeline, and ARIES timeline.")


if __name__ == "__main__":
    main()
