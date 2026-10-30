# Protocol for the ecom-* skills and /council

Paths are relative to `~/council` (the repo; `scripts/install.sh` links it there).

1. **Resolve the product.**
   - Use the one the user names. Otherwise, if `products/` has exactly one non-template folder, use it. Otherwise ask.
   - New product: copy `products/_template/` to `products/<slug>/` and fill `product.yaml` from facts the user gives.
2. **Load context.** Read `kb/index.yaml`, then:
   - the bundle's `kb` files plus `always`, and the bundle's `state` files from `products/<slug>/`;
   - `<chosen>` means the avatar the user picked. If there are several and none is picked, ask.
   - Nothing else by default. For a question no bundle covers, use the `files` catalog, then Grep `kb/` (and `_sources/text/` if it exists) before writing GAP.
   - Large reference files (`references/*.yaml`): Grep, don't read whole.
3. **Evidence.**
   - Own store: Shopify tools (products, variants, analytics funnel), if connected.
   - Market evidence (Google Trends, ad library counts, competitor stores, sales metrics) comes from the **user**: screenshots and numbers they collect. Read screenshots with the Read tool and transcribe the numbers. If evidence is missing, list exactly what to capture; don't search competitors or estimate demand yourself. Fetch a competitor page only when the user names the URL.
   - Customer language (Reddit, reviews, forums, YouTube comments): WebSearch/WebFetch is fine; quote with links.
4. **No invention.** Follow `kb/foundations/house-rules.md`. Every fact, quote, number and claim traces to the user, product state, the KB (cite the file or tag) or a linked source. Otherwise write `NEEDS DATA:`. Where the KB says `GAP:`, say so.
5. **Write back with consent.** Propose exact updates to `products/<slug>/` files and a dated `log.md` entry (newest first). Write only after the user confirms. Never change a live store without explicit confirmation of the exact diff.
6. **Gate with the council.** Before committing money or production to a decision (avatar, angle, offer, script, page, kill/scale), offer `/council <mode>:` for a vote.
