---
name: ecom-research
description: Ecommerce product research, validation, competitor research, and winning-store review using the user's course knowledge base in ~/council. Use when the user wants to find or evaluate a product, check demand/TAM, decide whether to pivot a product, research or spy on competitors, estimate competitor revenue, find inspiration ads/landers, or review a winning store. For auditing the user's OWN store pages use ecom-pages (audit mode).
---

# ecom-research

Follow `~/council/kb/skill-protocol.md` (product resolution, context loading, house rules, write-back).

## Pick a mode → bundle (in `~/council/kb/index.yaml`)
- **Product research** (find or evaluate a product or new angle) → `research`
- **Validate / pivot** (TAM, demand signals, believability, "is it the ad or the product?") → `validate`
- **Competitor / winning store** → `competitor`

## Steps
1. **Product research:** apply the unit-economics gate and "what to look for" (`research/product-research.md`). Gather demand evidence with WebSearch/WebFetch: Amazon best sellers, Reddit/YouTube activity in the last 3–5 months, Google Trends. Spying on competitor ads and stores is the owner's manual job (step 3). Output a go / no-go / needs-data table: criterion | evidence (with link) | KB rule | verdict.
2. **Validate:**
   - Score each candidate sub-avatar on the 4-criterion scorecard.
   - Check believability.
   - For pivots, read `creatives.yaml` and apply the stage-dependent thresholds, including the ⚠ counterpoint.
   - Say plainly whether the creative quality was good enough for the test to count.
3. **Competitor (COACH ONLY; owner rule).** The owner does competitor research manually: "do not use AI to look for this… just guide me."
   - Do NOT browse competitor ads or stores, or build the ad bank yourself.
   - Instead:
     - give a step-by-step plan from the checklist (`research/competitor-store-review.md`), tailored to the product: where to look, what to save, what to note;
     - hand over an empty table to fill in, matching `product.yaml → competitors` (name, url, price, offer, angles, mechanism, avatar, review complaints, notes);
     - once the owner pastes findings back, analyze them: gaps, untapped avatars, unused angles, pricing position, offer patterns.
   - Write the findings into `product.yaml` with confirmation.
   - Only fetch a page if the owner explicitly asks you to look at a specific URL.
4. Close with the next step in the pipeline: research → ecom-avatar → ecom-angles → ecom-script / ecom-pages → ecom-media-buying.
