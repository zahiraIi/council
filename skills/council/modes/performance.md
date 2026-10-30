# Mode: performance (kill / keep / scale decisions, test plans, store and funnel audits)
Bundles: ad decisions → `media-buying` (+ `offer` for conversion problems). Store audit → `store-audit`.
Owner evidence required: Ads Manager numbers per campaign/ad set/ad (spend, purchases, ROAS, CPC, CPM, hook/hold rate, days live) and break-even ROAS from `product.yaml → economics`. Store audits: Shopify funnel (sessions → add to cart → checkout → purchase) and the live page. Missing → NEEDS DATA.
Plan format: decision table (entity | action | KB rule | why), budget plan, and when to re-check. For audits: fixes ranked by expected impact (severity | evidence | KB rule | exact change).

Seat focus:
- Builder: the best plan for profit and growth at the current spend stage, citing the latest dated KB rules.
- Prosecutor: argue the opposite action (if the plan scales, argue it's noise or will break; if it kills, argue it's cutting a winner early), and find the cheaper explanation (creative vs offer vs page vs tracking).
- Auditor: is the sample large enough to mean anything at this spend (`media-buying/benchmarks.yaml`)? Is break-even computed from real economics? Are cited rules current (not marked `⚠ was:`)?

Rubric: correct spend stage identified; latest dated rules applied; signal vs noise judged; economics from real numbers.
Verdict format: OUTCOME, pros/cons table, decision table, budget plan, re-check date.
Write-back: verdicts into `creatives.yaml`; `log.md`.
