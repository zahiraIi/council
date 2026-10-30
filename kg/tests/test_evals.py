import os, sys

import yaml

EVAL_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "evals", "council_vs_single")
sys.path.insert(0, EVAL_DIR)
from run import numbered, score  # noqa: E402


def test_score_uses_last_bug_line():
    assert score("maybe line 3...\nBUG LINE: 3\nactually\nBUG LINE: 9", [9]) == (True, 9)
    assert score("**BUG LINE:** 6", [6]) == (True, 6)          # markdown bold variants still parse
    assert score("BUG LINE: **6**", [6]) == (True, 6)
    assert score("no verdict", [1]) == (False, None)


import pytest


@pytest.mark.parametrize("fname", ["tasks.yaml", "tasks_hard.yaml"])
def test_tasks_have_valid_answer_keys(fname):
    tasks = yaml.safe_load(open(os.path.join(EVAL_DIR, fname)))["tasks"]
    assert len({t["id"] for t in tasks}) == len(tasks)
    for t in tasks:
        n = len(t["code"].rstrip("\n").split("\n"))
        assert t["lines"] and all(1 <= l <= n for l in t["lines"]), t["id"]
        assert numbered(t["code"]).startswith(" 1| ")
