---
name: ecom-pages
description: Build and audit landing pages, advertorials, listicles, product pages (PDP), and offers for the user's Shopify stores using the course knowledge base in ~/council; can read and (with confirmation) edit the live Shopify store. Use when the user asks for an advertorial, listicle, pre-lander, landing page, PDP copy, hero image direction, headlines for a page, offer/bundle/pricing design, matching an ad to a landing page, or to audit/review their store.
---

# ecom-pages

Follow `~/council/kb/skill-protocol.md`.

| Mode | Bundle |
|---|---|
| Advertorial / listicle / pre-lander | `page` |
| PDP copy or redesign | `page` + `offer` |
| Offer / pricing / bundles | `offer` |
| Store audit | `store-audit` |

## Page (advertorial, listicle, PDP)
1. Get the ad it pairs with: angle (`angles.yaml`), awareness level, hook. If the user doesn't know, ask which level the ad targets.
2. Start the page at that level and walk down the stages (`foundations/awareness.md` table).
3. Deliver:
   - page type and why;
   - hero image direction (continues the ad's emotion; not a product shot);
   - 3–5 headlines from the templates in customer language;
   - 150–300-word lead copy (agitate → validate → hope, solution not yet revealed);
   - CTA placement.
   Ask whether to continue to the full page.
4. Listicle structure is a known GAP. Say so, then model a Pagedeck example or a competitor's listicle (fetch it) rather than inventing a course rule.
5. Write → `pages.yaml` (status `draft`).

## Offer
- Read live variants and prices from Shopify. Design or compare offers with `pages/offers.md`: types, economics (show the break-even ROAS impact using `product.yaml → economics`; ask for COGS if it's TODO), the 2-offer testing rule.
- Write → `offers.yaml`.

## Store audit
- Pull live data: Shopify product and variants, plus the analytics funnel. Use these ShopifyQL queries:
  - `FROM sessions SHOW sessions, sessions_with_cart_additions, sessions_that_reached_checkout, sessions_that_completed_checkout, conversion_rate SINCE -30d UNTIL today`
  - `FROM sales SHOW orders, gross_sales, average_order_value GROUP BY product_title SINCE -90d UNTIL today`
- Fetch the live PDP text.
- Run the 11-point `pages/store-audit-checklist.md`. Each finding gets: severity | evidence | KB rule (tag) | fix. Rank by expected impact; offer first.

## Editing the live store
- Show the exact before → after (title, description HTML, variant names/prices, etc.).
- Apply it with Shopify tools only after the user says yes to that specific diff.
- Log it to `log.md` and `pages.yaml` / `offers.yaml`.
