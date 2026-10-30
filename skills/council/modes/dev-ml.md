# Mode: dev-ml (software engineering, ML projects)
No ecom KB. Gather into the briefing: the task; relevant source files or excerpts (Read/Grep); the git diff if reviewing a change; configs, logs, metrics, error traces; dataset description (size, splits, leakage risks); compute budget; the project's README/CLAUDE.md conventions. Trim to what bears on the task.
Seats may Read/Grep the project's files (add the project path to their allowed paths); no web, no running code.
Plan format: the answer or approach, concrete code/config where useful, and how to verify it (tests or experiments with expected outcomes).

Seat focus:
- Builder: the pragmatic solution that fits the existing code and conventions.
- Prosecutor: break it: bugs, edge cases, numerical issues, data leakage, eval contamination, a simpler approach that makes it unnecessary, or prior work showing it doesn't work.
- Auditor: verify claims against the actual code and logs; flag unverifiable claims about libraries or papers; check the verification plan would really catch failure.

Rubric: correctness; fits the codebase; experimental rigor (baselines, seeds, held-out eval); cost; simplicity; verifiability.
Verdict format: OUTCOME, pros/cons table, then the final answer or implementation sketch and the verification plan.
Write-back: none; offer to implement if PASSED.
