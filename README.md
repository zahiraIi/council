# council

An LLM council plus ecommerce workflow skills. Both are backed by a compact knowledge base distilled from a DTC/Meta-ads course, and they track per-product state.

- **`/council`**: one question goes to several model "members". Each answers independently, they rank each other's answers anonymously against a task rubric, and a chairman synthesizes the result (after [karpathy/llm-council](https://github.com/karpathy/llm-council), using Claude Code subagents instead of OpenRouter).
- **`ecom-*` skills**: step-by-step production for research, avatars, angles/mechanisms, scripts/ad copy, landing pages/offers and media buying.
- **`kb/`**: about 26k tokens of rules and checklists. Every rule carries a source tag. `kb/index.yaml` maps each task to the 3–6 files to load.

```
AGENTS.md        entry point for any LLM agent (Claude Code also reads it via CLAUDE.md)
kb/              knowledge base. START at kb/index.yaml; shared rules in kb/skill-protocol.md
skills/          council/ (SKILL.md + modes/*.md) and ecom-research|avatar|angles|script|pages|media-buying
products/
  _template/     shapes for a new product (product.yaml, state.yaml, log.md)
  <slug>/        live state per product (git-ignored: private store data)
_sources/        original course files, call summaries, Notion export (git-ignored: paid/copyrighted)
scripts/         install.sh: symlink the skills into ~/.claude/skills
```

## Install (Claude Code)
```sh
git clone https://github.com/zahiraIi/council ~/council   # skills expect the repo at ~/council
~/council/scripts/install.sh
```
If you clone somewhere else, `install.sh` symlinks `~/council` to that location.

## Using it with other LLMs
- **Any agent that reads `AGENTS.md`** (Codex, Cursor, Gemini CLI, …): open the repo and ask for a task. `AGENTS.md` routes the agent through `kb/index.yaml` and the matching `skills/*/SKILL.md`, which are plain-language procedures.
- **Chat UIs** (ChatGPT, Gemini, Claude.ai): paste or upload `kb/foundations/house-rules.md`, the bundle files listed in `kb/index.yaml` for your task, and the matching `SKILL.md`.
- **Council on other models:** members must run in isolation and review anonymously. Without subagents, run each member in a separate chat, or use karpathy/llm-council with the context packet described in `skills/council/SKILL.md` step 0.

## Source tags in kb/
`[c:MM-DD]` coaching-call summary · `[d:slug]` course doc · `[b:schwartz]` Breakthrough Advertising · `[n:ball]`/`[n:dash]`/`[n:ecom-resources]` owner's Notion notes · `[imgNN]` Notion image. The files they point to are in `_sources/`, which is not committed. `_sources/README.md` maps the original filenames.

## Adding knowledge
1. Drop the new file into `_sources/`.
2. Ask the agent to merge it into `kb/`. It must cite the file, follow the "latest dated call wins; keep superseded rules as `⚠ was:`" rule, write `GAP:` lines instead of inventing, and update the token counts in `kb/index.yaml`.
