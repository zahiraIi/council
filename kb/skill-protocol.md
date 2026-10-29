# Protocol for ecom-* skills and /council ecom modes

1. **Resolve the product.**
   - Use the one the user names. Otherwise, if `~/council/products/` has exactly one non-template folder, use it. Otherwise ask.
   - For a new product: copy `products/_template/` into `products/<slug>/`, seed `product.yaml` from facts, and split `state.yaml` into the per-file stubs.
2. **Load context.** Read `~/council/kb/index.yaml`, then:
   - the bundle's `kb` files plus `always`;
   - the bundle's `state` files from `products/<slug>/`;
   - `<chosen>` means the avatar the user picked. If there are several and none is picked, ask.
   - Don't load other KB files unless the task needs them; use the `files` catalog.
   - `references/winning-ads.yaml` is large: filter it with grep by stage or format instead of reading it whole.
   - When the bundle doesn't cover the question, or you need the original wording behind a tag, search the knowledge graph before writing GAP: `kg_search` (MCP `council-kg`) covers every KB section plus the raw calls, docs, Notion notes and Schwartz; `kg_sources("c:10-19")` resolves a tag. Hits flagged `superseded_on` are history, not current advice.
3. **Live data beats stale state.**
   - Own store: Shopify tools (products, variants, analytics funnel).
   - Competitor research is the OWNER'S MANUAL TASK: coach and analyze what they bring back; don't browse competitors unless they name a specific URL to look at [n:ball].
   - Reference pages the owner lists in the KB: WebFetch. If rate-limited, use `curl -A "Mozilla/5.0"` into the scratchpad and strip the HTML.
   - Customer research: WebSearch and WebFetch on Reddit, YouTube comments, forums, Amazon reviews.
4. **Follow `foundations/house-rules.md`.**
   - Never invent facts, quotes, or numbers. Write `NEEDS DATA:` or `TODO`.
   - When a rule conflicts or a GAP applies, say which rule you followed.
5. **Cite KB rules** in reviews and recommendations, using their source tag (e.g. "[c:10-19] judge on 7 days"), so the user can trace them.
6. **Write back with consent.**
   - At the end, propose specific updates to state files and a `log.md` entry (newest first).
   - Write only after the user confirms. Never write to Shopify (product, page, or price edits) without explicit confirmation of the exact change.
7. **Escalate judgment calls.** For high-stakes choices (which avatar or angle to bet on, an offer change, a kill/scale call, final script selection), offer `/council <mode>:` for a multi-model review.
