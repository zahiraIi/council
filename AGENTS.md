# Agent instructions

This repo is a knowledge base plus skills for running DTC ecommerce stores (Shopify + Meta ads) and an LLM council. Paths below are relative to the repo root (installed at `~/council`).

## Routing
1. Pick the skill that fits the request and read its `SKILL.md`:
   - research / validation / competitor coaching → `skills/ecom-research/`
   - customer avatars → `skills/ecom-avatar/`
   - mechanism, desires, angles, native ad story → `skills/ecom-angles/`
   - scripts, hooks, primary text, headlines, editor brief → `skills/ecom-script/`
   - landing pages, advertorials, listicles, PDP, offers, store audit → `skills/ecom-pages/`
   - test/scale/kill decisions, creative log → `skills/ecom-media-buying/`
   - multi-model debate or review of any of the above, or of code/ML → `skills/council/` (+ `modes/<mode>.md`)
2. Follow `kb/skill-protocol.md`: resolve the product, load the task's bundle from `kb/index.yaml`, and always load `kb/foundations/house-rules.md`.
3. Load only the bundle's files, not the whole KB. Don't open `_sources/` directly: query the knowledge graph instead.
4. **Knowledge graph** (MCP server `council-kg`, or the CLI `cd kg && uv run kg search "<q>"`): `kg_search` does hybrid keyword + semantic search over every KB section and the raw course sources. `kg_sources("<tag>")` resolves a citation, and `kg_neighbors` follows edges (cites, supersedes, mentions). Use it when a bundle doesn't cover the question, and before declaring a GAP.

## Hard rules
- Cite KB source tags for rules you apply. Where the KB says `GAP:`, say so; don't invent course rules, claims, reviews or data.
- Write to `products/<slug>/*` and to any live store (Shopify) **only after the user confirms the exact change**.
- Competitor research is the owner's manual task: coach them through it, and fetch a competitor page only when the user names a specific URL.
- `products/<slug>/` and `_sources/` are private and git-ignored. Never commit them, and never copy their contents into tracked files.
- If your tool can't run subagents, run council members as separate isolated passes. Keep Stage 2 reviews anonymized ("Response A/B/…").
