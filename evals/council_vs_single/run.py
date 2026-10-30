"""Council vs single model on seeded-bug tasks, via headless Claude Code (`claude -p`).

Conditions
  single:<model>   one model, no tools, one call
  council          `/council dev-ml:` (4 members + 3 stages + chairman, via subagents)

Scoring is objective: the answer's LAST "BUG LINE: <n>" must be one of the task's
accepted lines. Cost and latency come from Claude Code's JSON output (total_cost_usd is
the API-equivalent cost Claude Code reports; on a subscription it is usage, not a bill).

  uv run --project kg python evals/council_vs_single/run.py --conditions single:opus single:sonnet
  uv run --project kg python evals/council_vs_single/run.py --conditions council --tasks binary-search,dedupe-order
  uv run --project kg python evals/council_vs_single/run.py --report
"""
import argparse, json, os, re, subprocess, sys, time

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(HERE, "results.jsonl")

PROMPT = """Find the single bug in this Python code. Lines are numbered.

{numbered}

Explain the bug and the fix briefly. End your answer with exactly one line in this format:
BUG LINE: <line number>"""


def numbered(code):
    return "\n".join(f"{i:>2}| {line}" for i, line in enumerate(code.rstrip("\n").split("\n"), start=1))


def score(text, accepted):
    found = re.findall(r"BUG LINE:\s*\**\s*(\d+)", text or "")
    if not found:
        return False, None
    line = int(found[-1])
    return line in accepted, line


def run_claude(args, prompt, timeout):
    t0 = time.time()
    try:
        p = subprocess.run(["claude", "-p", *args, "--output-format", "json", "--no-session-persistence", prompt],
                           capture_output=True, text=True, timeout=timeout)
        out = json.loads(p.stdout) if p.stdout.strip().startswith("{") else {"result": p.stdout, "is_error": True,
                                                                             "stderr": p.stderr[-500:]}
    except subprocess.TimeoutExpired:
        out = {"result": "", "is_error": True, "stderr": "timeout"}
    out["wall_s"] = round(time.time() - t0, 1)
    return out


def condition_args(cond):
    if cond.startswith("single:"):
        # no tools: a pure single-model answer
        return ["--model", cond.split(":", 1)[1], "--tools", ""], "{prompt}", 300
    if cond == "council":
        # the council skill orchestrates subagents; allow only what it needs
        return (["--model", "opus", "--allowedTools", "Skill", "Agent", "Read", "Write"],
                "/council dev-ml: [full council] {prompt}", 1800)
    raise SystemExit(f"unknown condition {cond}")


# A real council run spawns members, reviewers and a chairman. Fewer orchestrator turns
# means it answered directly (pilot 2026-10-29: 1 turn, 6 s), so the row isn't a council result.
MIN_COUNCIL_TURNS = 5


def is_valid(r):
    if r.get("error"):
        return False
    return r["condition"] != "council" or (r.get("num_turns") or 0) >= MIN_COUNCIL_TURNS


def run(conditions, task_ids, tasks_file="tasks.yaml"):
    tasks = yaml.safe_load(open(os.path.join(HERE, tasks_file)))["tasks"]
    task_set = tasks_file.rsplit(".", 1)[0]
    if task_ids:
        tasks = [t for t in tasks if t["id"] in task_ids]
    for cond in conditions:
        args, template, timeout = condition_args(cond)
        for t in tasks:
            prompt = template.format(prompt=PROMPT.format(numbered=numbered(t["code"])))
            out = run_claude(args, prompt, timeout)
            ok, line = score(out.get("result", ""), t["lines"])
            row = {"ts": time.time(), "set": task_set, "condition": cond, "task": t["id"], "correct": ok,
                   "answered_line": line,
                   "accepted": t["lines"], "cost_usd": out.get("total_cost_usd"),
                   "duration_s": round((out.get("duration_ms") or 0) / 1000, 1) or out["wall_s"],
                   "num_turns": out.get("num_turns"), "error": out.get("is_error"),
                   "answer_tail": (out.get("result") or "")[-400:]}
            row["valid"] = is_valid(row)
            with open(RESULTS, "a", encoding="utf-8") as f:
                f.write(json.dumps(row) + "\n")
            print(f"{cond:14s} {t['id']:28s} {'OK ' if ok else 'BAD'} line={line} turns={row['num_turns']} "
                  f"cost=${row['cost_usd'] or 0:.3f} {row['duration_s']}s{'' if row['valid'] else '  INVALID'}",
                  flush=True)


def report():
    rows = [json.loads(l) for l in open(RESULTS, encoding="utf-8")] if os.path.exists(RESULTS) else []
    latest = {}
    skipped = 0
    for r in rows:                                   # latest valid run per (condition, task)
        if not is_valid(r):
            skipped += 1
            continue
        latest[(r.get("set", "tasks"), r["condition"], r["task"])] = r
    if skipped:
        print(f"({skipped} invalid rows excluded: errors or council runs that didn't convene)\n")
    by = {}
    for (s, c, _), r in latest.items():
        by.setdefault((s, c), []).append(r)
    print("| Task set | Condition | Tasks | Accuracy | Avg cost (USD, API-equiv.) | Avg latency (s) |")
    print("|---|---|---:|---:|---:|---:|")
    for (s, c), rs in sorted(by.items()):
        n = len(rs)
        acc = sum(r["correct"] for r in rs) / n
        cost = sum(r["cost_usd"] or 0 for r in rs) / n
        lat = sum(r["duration_s"] or 0 for r in rs) / n
        print(f"| {s} | {c} | {n} | {acc:.0%} | {cost:.3f} | {lat:.0f} |")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--conditions", nargs="+", default=["single:opus"])
    ap.add_argument("--tasks", help="comma-separated task ids (default: all)")
    ap.add_argument("--tasks-file", default="tasks.yaml", help="tasks.yaml (easy) or tasks_hard.yaml")
    ap.add_argument("--report", action="store_true")
    a = ap.parse_args()
    if a.report:
        return report()
    run(a.conditions, set(a.tasks.split(",")) if a.tasks else None, a.tasks_file)
    report()


if __name__ == "__main__":
    main()
