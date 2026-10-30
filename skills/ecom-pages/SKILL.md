---
name: ecom-pages
description: Build and audit landing pages, advertorials, listicles, product pages (PDP), and offers using your playbook in ~/council/kb; can read and (with confirmation) edit a live Shopify store. Use when the user asks for an advertorial, listicle, pre-lander, landing page, PDP copy, hero image direction, page headlines, offer/bundle/pricing design, matching an ad to a landing page, or to audit their store.
---

# ecom-pages

Follow `~/council/skills/protocol.md`.

| Mode | Bundle |
|---|---|
| Advertorial / listicle / pre-lander / PDP | `page` (+ `offer` for PDP) |
| Offer / pricing / bundles | `offer` |
| Store audit | `store-audit` |

## Page
1. Get the ad it pairs with: angle (`angles.yaml`), awareness level, hook. If unknown, ask.
2. Follow `pages/landing-pages.md`: start at the ad's awareness level and continue the ad's emotion.
3. Deliver page type and why, hero direction, headlines, lead copy and CTA plan; ask before writing the full page.
4. Where the KB has no rule (e.g. listicle structure), say so and model a real example the user supplies or names.
5. **Gate:** offer `/council creative:`. Write → `pages.yaml` (status `draft`).

## Offer
Read live variants and prices (Shopify, if connected). Design or compare offers per `pages/offers.md`, showing the break-even impact from `product.yaml → economics` (ask for COGS if missing). Write → `offers.yaml`.

## Store audit
- Live data: product and variants, and the funnel. ShopifyQL:
  - `FROM sessions SHOW sessions, sessions_with_cart_additions, sessions_that_reached_checkout, sessions_that_completed_checkout, conversion_rate SINCE -30d UNTIL today`
  - `FROM sales SHOW orders, gross_sales, average_order_value GROUP BY product_title SINCE -90d UNTIL today`
- Fetch the live page text and run `pages/store-audit-checklist.md`. Each finding: severity | evidence | KB rule | fix, ranked by expected impact.

## Editing the live store
Show the exact before → after, apply it only after the user approves that diff, then log it to `log.md` and `pages.yaml` / `offers.yaml`.
