# Knowledge base template

`scripts/install.sh` copies this folder to `kb/` (git-ignored, private). Fill `kb/` with your own playbook:
- one rule per bullet, each with a source tag (`[book:title ch3]`, `[call:2026-01-15]`, `[test:B4]`) so agents can cite it;
- the newest dated rule wins; keep the old one as `⚠ was: …` so it's visible as history;
- write `GAP:` where you have no rule; agents will say so instead of inventing one.

`index.yaml` routes each task to 3–6 files, so agents load a few thousand tokens instead of the whole KB.
Run `python scripts/check_kb.py` after editing to confirm every routed file exists and parses.
