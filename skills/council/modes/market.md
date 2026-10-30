# Mode: market (product, sub-avatar, angle, offer: is this worth betting on?)
Bundles: pick by subject. Product: `research`, `validate`. Sub-avatar: `avatar`, `validate`. Angle or mechanism: `angles`, `mechanism`. Offer: `offer`.
Plan format: the thesis in one sentence ("<who> will buy <what> because <why>, and the market is <open/crowded> because <evidence>"), the specific choice (product / sub-avatar / angle / offer), and the cheapest test that would prove it.

Evidence checklist (from the owner; the Auditor marks each present or missing):
1. Google Trends for the core search term(s): 12-month and 5-year views (direction, seasonality).
2. Demand proxy: marketplace best-seller ranks or review counts, search volume, or community activity in the last 3–5 months.
3. Competition density: how many advertisers or stores run this product/angle (e.g. ad library count) and what they claim.
4. Customer voice: real quotes behind the sub-avatar or desire (3+ separate people per pattern), with links.
5. Economics: price, COGS, shipping, fees → break-even ROAS (or NEEDS DATA).

Seat focus:
- Builder: why this is a real, reachable market with an untapped angle; the sharpest version of the thesis.
- Prosecutor: kill it on market grounds: falling or seasonal trend, demand too small to scale, saturated (many advertisers making the same claim), quotes that are generic or from too few people, product that can't credibly deliver, economics that don't clear break-even.
- Auditor: score the checklist and the KB's validation scorecard (`research/validation.md`, plus `angles/angles.md` or `pages/offers.md` when relevant); flag claims with no evidence behind them.

Rubric: the KB rules in the loaded bundles; evidence quality (owner data > KB rule > reasoning); untapped vs saturated judged from competition evidence, not assumed; economics shown.
Verdict format: OUTCOME, pros/cons table, evidence scorecard, and the cheapest next test (budget, duration, success metric) if passed.
Write-back: the decision into the relevant state file (`product.yaml`, `avatars/`, `angles.yaml`, `offers.yaml`) with status `chosen` only if PASSED; `log.md`.
