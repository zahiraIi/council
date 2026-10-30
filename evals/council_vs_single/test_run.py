"""Checks for the eval harness (no pytest needed): python evals/council_vs_single/test_run.py"""
import os, sys

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from run import numbered, score  # noqa: E402

assert score("maybe line 3...\nBUG LINE: 3\nactually\nBUG LINE: 9", [9]) == (True, 9)
assert score("**BUG LINE:** 6", [6]) == (True, 6)
assert score("BUG LINE: **6**", [6]) == (True, 6)
assert score("no verdict", [1]) == (False, None)

for fname in ("tasks.yaml", "tasks_hard.yaml"):
    tasks = yaml.safe_load(open(os.path.join(HERE, fname)))["tasks"]
    assert len({t["id"] for t in tasks}) == len(tasks), fname
    for t in tasks:
        n = len(t["code"].rstrip("\n").split("\n"))
        assert t["lines"] and all(1 <= l <= n for l in t["lines"]), t["id"]
        assert numbered(t["code"]).startswith(" 1| ")
print("eval harness OK")
