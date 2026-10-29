---
name: ecom-script
description: Write, clone, and check video ad scripts and Meta ad copy using the user's course knowledge base in ~/council. Modes - deconstruct a winning ad transcript, build a script (clone a winner's structure or write from scratch), check/audit a script, write primary text + headlines, and package an editor brief. Use when the user says deconstruct/break down this ad, write the script, script this ad, check my script, script audit, write hooks, primary text, headlines, or ad copy.
---

# ecom-script

Follow `~/council/kb/skill-protocol.md`. Pick the mode, then load its bundle from `~/council/kb/index.yaml`.

| Mode | Bundle | Core file |
|---|---|---|
| Deconstruct a winning ad | `deconstruct` | `creative/ad-deconstruction.md` |
| Build a script | `script` | `creative/script-build.md` |
| Check a script | `script-check` | `creative/script-standards.md` |
| Primary text + headlines | `ad-copy` | `creative/primary-text-headlines.md` |
| Editor brief | `brief` | `creative/script-brief.md` |

## Deconstruct
- Need a timestamped transcript. If the user gives a link, try to fetch a transcript; otherwise ask them to paste one.
- To find inspiration, grep `references/winning-ads.yaml` by awareness level and format.
- Follow steps 1–4 exactly. End with the confirmation question and stop.

## Build
- Needs: the chosen angle (`angles.yaml`), avatar, mechanism, product facts. If any are missing, say which and offer `ecom-angles` / `ecom-avatar`.
- **Clone mode** if there's a confirmed deconstruction; otherwise **from-scratch 7-part**. Never half-clone.
- Output 3 hooks plus the body.
- If the user wants to co-write, go line by line, asking for approval after each line.
- Run the full `script-standards.md` rubric on your own draft and fix every ❌ before showing it.
- Offer `/council script:` to compare or choose between variations.

## Check
- Ask for the script, its awareness level, product and avatar (use state if available).
- Score every rubric item ✅/❌. Output "OVERALL: X/Y", the fixes, and the closing line.

## Ad copy
- 2 primary texts (≤125 chars) + 2 headlines (≤40 chars) per ad, each with a psychology note.
- Count characters and confirm they're under the limits.

## Brief
- Fill the template with 3 variations.
- Log each ad to `creatives.yaml` (status `testing`, `launched` date TBD) after confirmation.
