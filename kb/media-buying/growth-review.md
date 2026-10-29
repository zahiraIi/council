---
topic: Growth system: KPI definitions, weekly review, experiment brief, scale/hold/fix/pause, ad diagnosis rules of thumb
load_when: weekly reviews, writing a test hypothesis, deciding scale/hold/fix/pause, diagnosing engagement vs conversion
sources: [n:dash Growth & Analytics, n:ball "Reviewing Ads Once Launched"]
updated: 2026-10-29
---
# Diagnosis rules of thumb [n:ball]
- Good engagement (CPC < $2 or CTR > 10%) + low CVR → improve the OFFER.
- Bad engagement (high CPC, low CTR) + no sales → improve the ADS and/or offer, or try a new landing page.
- Break-even after offer tweaks → research a NEW AVATAR (this is how the owner's course product turned profitable).

# KPI dictionary (use these definitions in every report)
| Metric | Definition | Cadence |
|---|---|---|
| Revenue | gross OR net; label which | weekly |
| Contribution margin | revenue − variable product, fulfillment, payment, refund, and ad costs | weekly |
| AOV | revenue / orders | weekly |
| CVR | orders / sessions | weekly |
| CAC / CPA | acquisition cost / new customers or conversions | weekly |
| ROAS | attributed revenue / ad spend | weekly |
| Refund rate | refunds / orders | weekly-monthly |
| Repeat purchase rate | customers with another purchase in the window | monthly |
| Email revenue share | email revenue / total | weekly |

# Weekly growth review
1. Revenue, contribution margin, cash impact.
2. Funnel: sessions → product views → ATC → checkout → purchase (Shopify analytics).
3. Channel: spend, CPM, CTR, CPC, CVR, CAC, ROAS.
4. Creative: launches, winners, fatigue, learnings.
5. Product: best sellers, refunds, reviews, stock risk.
6. Retention: email/SMS capture, flows, repeat purchase.
7. Decisions: scale / hold / fix / test / stop.

# Experiment brief (every test)
- Fields: hypothesis · store · channel · audience · asset/LP · ONE primary variable (hook, angle, offer, proof, format, audience, or LP) · primary metric · guardrail metrics · budget · window · decision rule · result · next action.
- Record the learning in the creative tracker: products/<p>/creatives.yaml (the owner also keeps a Google Sheet tracker; see products/<p>/product.yaml → links).
- Note: "one primary variable" applies once a concept is winning. Early tests take big swings (testing.md). Test ladder: many hooks and angles cheaply → controlled variations of winners → offer, LP, and audience around the winner → scale once margin and fulfillment allow.

# Feedback loop: run after every batch [n:ball img20-24]
Loop: action → result → analysis → improved action. Not learning from winners and losers is the #1 reason people stall after early sales.

- Before launch, document each creative:
  - test #, date, creative type/format;
  - the NEW variable, angle, problem/desire, avatar, mechanism, awareness level;
  - hypothesis.
  Store it in products/<p>/creatives.yaml.
- Losers:
  - In a CBO, no spend = a bad ad. "Don't cope with hook rate or CTR."
  - Write 1–3 specific learnings, e.g. "led with product before benefit", "assumed they knew the mechanism".
  - If the ad was modeled on a winner, compare against it to find what broke.
- Winners, after a couple of weeks of spend:
  - What messaging resonated?
  - What desire, fear, or belief did it tap that the losers didn't?
  - Note specifics, e.g. "before/after hook overlay → 80% hook rate".
- A winning ad is 5–6 variables stacked together. Mine them out one at a time so you can replicate on purpose.
- Rule of thumb: small swings on winners (isolate 1–2 variables), big swings on losers (change several things, to test faster).

# Scale / Hold / Fix / Pause
- Scale: profitable on CONTRIBUTION MARGIN, repeatable, and fulfillment can keep up.
- Hold: promising, but volume or data quality is insufficient.
- Fix: the bottleneck is clear (creative, offer, LP, checkout, tracking, fulfillment).
- Pause: losses past the agreed threshold, customer-harm risk, or ops can't support it.

# Reporting conventions
- One naming convention for campaigns, ad sets, ads, UTMs, and creative IDs.
- Platform metrics stay separate from finance-reconciled numbers.
- Record the attribution window and date; note tracking gaps and one-off events.
