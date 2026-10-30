---
name: ecom-research
description: Ecommerce product research and validation using your playbook in ~/council/kb - evaluate a product or new angle, check demand and competition from the evidence you collect (Google Trends, ad library, marketplace data), decide whether to pivot, and coach competitor research. Use when the user wants to find or evaluate a product, check demand/TAM, decide whether to pivot, or research competitors. For auditing the user's OWN store use ecom-pages (audit mode).
---

# ecom-research

Follow `~/council/skills/protocol.md`. Bundles (`~/council/kb/index.yaml`): `research`, `validate`, `competitor`.

## Evidence comes from the owner
You don't estimate demand or scout competitors yourself. Give the owner a capture checklist tailored to the product, then analyze what they bring back:
1. Google Trends for the core terms: 12-month and 5-year screenshots.
2. A demand proxy: marketplace best-seller ranks or review counts, search volume, recent community activity.
3. Competition: how many advertisers or stores run this product or angle, and what they claim, price and offer (an empty table matching `product.yaml → competitors`).
4. Economics: price, COGS, shipping, fees.

Read screenshots with the Read tool, transcribe the numbers, and keep the file paths. Fetch a competitor page only when the owner names the URL.

## Modes
- **Evaluate a product or angle** (`research`): apply the KB's product criteria and economics gate to the evidence. Output a table: criterion | evidence | KB rule | verdict, then go / no-go / NEEDS DATA.
- **Validate or pivot** (`validate`): score candidates on the KB's validation scorecard; for pivots, read `creatives.yaml` and apply the KB's stage thresholds. Say plainly whether the creative was good enough for the test to count.
- **Competitors** (`competitor`): coach the owner through the KB checklist, then analyze their findings for gaps, untapped sub-avatars, unused angles, pricing and offer patterns.

Before betting on the result, offer `/council market:` with the evidence. Then: ecom-avatar → ecom-angles → ecom-script / ecom-pages → ecom-media-buying.
