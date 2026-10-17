"""Check CPU scheduling timelines, arithmetic, and the module article map."""

from collections import deque
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from build import read_inventory


JOBS = {"P1": (0, 8), "P2": (1, 4), "P3": (2, 2), "P4": (3, 1)}


def article(slug):
    return (ROOT / "content" / "os" / f"{slug}.md").read_text(encoding="utf-8")


def timeline(slug):
    rows = re.findall(r"^\| (\d+)-(\d+) \| ([A-Z]\d?) \|", article(slug), re.MULTILINE)
    assert rows, f"No timeline in {slug}"
    return [(int(start), int(end), job) for start, end, job in rows]


def measures(slug, jobs):
    rows = timeline(slug)
    assert rows[0][0] == 0
    assert all(left[1] == right[0] for left, right in zip(rows, rows[1:])), slug
    assert rows[-1][1] == sum(burst for _, burst in jobs.values()), slug
    used = {job: 0 for job in jobs}
    first = {}
    finished = {}
    for start, end, job in rows:
        assert job in jobs and end > start and start >= jobs[job][0], slug
        first.setdefault(job, start)
        used[job] += end - start
        finished[job] = end
    assert used == {job: burst for job, (_, burst) in jobs.items()}, slug
    result = {
        job: (
            finished[job],
            finished[job] - arrival,
            finished[job] - arrival - burst,
            first[job] - arrival,
        )
        for job, (arrival, burst) in jobs.items()
    }
    listed = re.findall(
        r"^\| (P[1-4]) \| (\d+) \| (\d+) \| (\d+) \| (\d+) \|$",
        article(slug),
        re.MULTILINE,
    )
    if listed:
        assert {job: tuple(map(int, values)) for job, *values in listed} == result, slug
    return rows, result


def nonpreemptive(jobs, rule):
    remaining = set(jobs)
    now = 0
    rows = []
    while remaining:
        ready = [job for job in remaining if jobs[job][0] <= now]
        if not ready:
            now = min(jobs[job][0] for job in remaining)
            ready = [job for job in remaining if jobs[job][0] <= now]
        if rule == "fcfs":
            chosen = min(ready, key=lambda job: (jobs[job][0], job))
        elif rule == "sjf":
            chosen = min(ready, key=lambda job: (jobs[job][1], jobs[job][0], job))
        else:
            chosen = min(
                ready,
                key=lambda job: (
                    -(now - jobs[job][0] + jobs[job][1]) / jobs[job][1],
                    jobs[job][1],
                    jobs[job][0],
                    job,
                ),
            )
        end = now + jobs[chosen][1]
        rows.append((now, end, chosen))
        now = end
        remaining.remove(chosen)
    return rows


def preemptive(jobs, rule, priorities=None):
    remaining = {job: burst for job, (_, burst) in jobs.items()}
    ticks = []
    for now in range(sum(remaining.values())):
        ready = [job for job in jobs if jobs[job][0] <= now and remaining[job] > 0]
        current = ticks[-1] if ticks else None
        if rule == "srtf":
            chosen = min(ready, key=lambda job: (remaining[job], job != current, jobs[job][0], job))
        else:
            chosen = min(ready, key=lambda job: (priorities[job], job != current, jobs[job][0], job))
        ticks.append(chosen)
        remaining[chosen] -= 1
    rows = []
    for now, job in enumerate(ticks):
        if rows and rows[-1][2] == job:
            rows[-1] = (rows[-1][0], now + 1, job)
        else:
            rows.append((now, now + 1, job))
    return rows


def round_robin(jobs, quantum):
    remaining = {job: burst for job, (_, burst) in jobs.items()}
    waiting = deque()
    added = set()
    now = 0
    rows = []
    while any(remaining.values()):
        for job in sorted(jobs, key=lambda name: (jobs[name][0], name)):
            if job not in added and jobs[job][0] <= now:
                waiting.append(job)
                added.add(job)
        if not waiting:
            now = min(jobs[job][0] for job in jobs if job not in added)
            continue
        job = waiting.popleft()
        end = now + min(quantum, remaining[job])
        rows.append((now, end, job))
        remaining[job] -= end - now
        now = end
        for newcomer in sorted(jobs, key=lambda name: (jobs[name][0], name)):
            if newcomer not in added and jobs[newcomer][0] <= now:
                waiting.append(newcomer)
                added.add(newcomer)
        if remaining[job]:
            waiting.append(job)
    return rows


def main():
    slugs = {
        "fcfs": "first-come-first-serve-fcfs-scheduling",
        "sjf": "shortest-job-first-sjf-scheduling",
        "srtf": "shortest-remaining-time-first-srtf-scheduling",
        "rr": "round-robin-rr-scheduling",
        "priority": "priority-scheduling",
    }
    checked = {name: measures(slug, JOBS) for name, slug in slugs.items()}
    assert checked["fcfs"][0] == nonpreemptive(JOBS, "fcfs")
    assert checked["sjf"][0] == nonpreemptive(JOBS, "sjf")
    assert checked["srtf"][0] == preemptive(JOBS, "srtf")
    assert checked["rr"][0] == round_robin(JOBS, 2)
    priorities = {"P1": 3, "P2": 1, "P3": 2, "P4": 0}
    assert checked["priority"][0] == preemptive(JOBS, "priority", priorities)
    assert sum(x[2] for x in checked["fcfs"][1].values()) / 4 == 7
    assert sum(x[2] for x in checked["sjf"][1].values()) / 4 == 5.5
    assert sum(x[2] for x in checked["srtf"][1].values()) / 4 == 2.75
    assert sum(x[2] for x in checked["rr"][1].values()) / 4 == 5

    hrrn_jobs = {"A": (0, 4), "B": (0, 8), "C": (3, 2), "D": (5, 2)}
    hrrn, hrrn_result = measures("highest-response-ratio-next-hrrn-scheduling", hrrn_jobs)
    assert hrrn == nonpreemptive(hrrn_jobs, "hrrn")
    assert [hrrn_result[job][2] for job in "ABCD"] == [0, 6, 1, 9]
    assert measures("multilevel-queue-mlq-scheduling", {"B": (0, 6), "F": (2, 2)})[0] == [
        (0, 2, "B"), (2, 4, "F"), (4, 8, "B")
    ]
    assert measures("multilevel-feedback-queue-mlfq-scheduling", {"A": (0, 8), "B": (2, 1)})[0] == [
        (0, 2, "A"), (2, 3, "B"), (3, 7, "A"), (7, 9, "A")
    ]

    module = "Module-3 (CPU Scheduling Algorithms in Operating System))"
    topics = [
        topic for topic in read_inventory()
        if any(p["course"] == "Operating Systems" and p["sections"][0] == module for p in topic["placements"])
    ]
    assert len(topics) == 11
    for topic in topics:
        path = ROOT / "content" / topic["subject"] / f'{topic["slug"]}.md'
        assert path.exists(), topic["title"]
        assert path.read_text(encoding="utf-8").splitlines()[0] == f'# {topic["title"]}'

    print("Checked eight scheduling timelines, their arithmetic, and all 11 module articles.")


if __name__ == "__main__":
    main()
