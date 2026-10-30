# Agent instructions

This repo is a set of skills for building a DTC ecommerce funnel end to end (Shopify + Meta ads), plus a voting council that gates each decision. Paths are relative to the repo root (installed at `~/council`).

## Routing
1. Pick the skill that fits the request and read its `SKILL.md`:
   - product research, validation, competitor coaching → `skills/ecom-research/`
   - customer avatars → `skills/ecom-avatar/`
   - mechanism, desires, angles, native ad story → `skills/ecom-angles/`
   - scripts, hooks, primary text, headlines, editor brief → `skills/ecom-script/`
   - landing pages, advertorials, listicles, PDP, offers, store audit → `skills/ecom-pages/`
   - test/scale/kill decisions, creative log → `skills/ecom-media-buying/`
   - judging a plan, artifact or decision (ecom, code/ML, anything) → `skills/council/` (+ `modes/<mode>.md`)
2. Follow `skills/protocol.md`: resolve the product, load the task's bundle from `kb/index.yaml` (plus `kb/foundations/house-rules.md`), and nothing else by default.
3. For a question no bundle covers, use the `files` catalog in `kb/index.yaml`, then grep `kb/` (and `_sources/text/` if present) before writing GAP.

## Hard rules
- Cite the KB file or source tag for every rule you apply. Where the KB says `GAP:`, say so; never invent rules, claims, reviews, quotes or data. Unknown → `NEEDS DATA:`.
- Market evidence (trends, demand, competitors, metrics) comes from the user. Ask for exactly what's missing; don't estimate it.
- Write to `products/<slug>/*` and to any live store **only after the user confirms the exact change**.
- `kb/`, `products/<slug>/` and `_sources/` are private and git-ignored. Never commit them or copy their contents into tracked files.
- If your tool can't run subagents, run each council seat as a separate isolated pass, in order.
