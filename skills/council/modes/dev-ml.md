# Mode: dev-ml (software engineering, deep learning / ML projects)
No ecom KB. Context to gather into the packet before Stage 1 (members have no tools):
- the question; relevant source files or excerpts (Read/Grep), git diff if reviewing a change;
- configs/hyperparameters, training/eval logs and metrics, error traces, dataset description (size, splits, leakage risks), hardware/compute budget;
- the project's CLAUDE.md/README conventions.
Trim to the parts that bear on the question.

Roles:
1. Implementer (pragmatic, idiomatic solution matching the codebase).
2. Reviewer (bugs, edge cases, numerical issues, data leakage, eval contamination, reproducibility).
3. Researcher (relevant literature and known baselines; flags when an idea is known not to work).
4. Systems/perf engineer (compute cost, memory, throughput, simplicity).

Member output: answer, or a recommended approach with trade-offs, concrete code/config where useful, and how to verify it.
Rubric: correctness; fits the existing code and conventions; experimental rigor (baselines, seeds, held-out eval, ablations); cost; simplicity; verifiability. Penalize unverifiable claims about libraries or papers.
Chairman format: recommendation, implementation sketch, risks, and a verification plan (tests or experiments with expected outcomes).
Write-back: none by default; offer to implement.
