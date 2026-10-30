---
name: ecom-script
description: Write, clone, and check video ad scripts and Meta ad copy using your playbook in ~/council/kb. Modes - deconstruct a winning ad transcript, build a script (clone a winner's structure or write from scratch), check a script, write primary text + headlines, and package an editor brief. Use when the user says deconstruct/break down this ad, write the script, check my script, script audit, write hooks, primary text, headlines, or ad copy.
---

# ecom-script

Follow `~/council/skills/protocol.md`. Pick the mode, then load its bundle.

| Mode | Bundle | Core file |
|---|---|---|
| Deconstruct a winning ad | `deconstruct` | `creative/ad-deconstruction.md` |
| Build a script | `script` | `creative/script-build.md` |
| Check a script | `script-check` | `creative/script-standards.md` |
| Primary text + headlines | `ad-copy` | `creative/primary-text-headlines.md` |
| Editor brief | `brief` | `creative/script-brief.md` |

- **Deconstruct:** needs a timestamped transcript (fetch it if the user gives a link, else ask them to paste one). Follow the core file's steps; end with its confirmation question and stop.
- **Build:** needs the chosen angle, avatar, mechanism and product facts from state; if any is missing, say which and offer `ecom-angles` / `ecom-avatar`. Clone a confirmed deconstruction, or write from scratch per the core file. Output 3 hooks + body. Run the full `script-standards.md` rubric on your draft and fix every ❌ before showing it.
- **Check:** score every rubric item ✅/❌, then "OVERALL: X/Y" and the fixes.
- **Ad copy:** per the core file. Meta limits: primary text ≤125 characters, headline ≤40; count and confirm.
- **Brief:** fill the core file's template; log each ad to `creatives.yaml` after confirmation.

**Gate:** before anything goes to an editor or into Ads Manager, offer `/council creative:` to vote on it.
