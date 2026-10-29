---
name: ecom-media-buying
description: Plan and manage Meta (Facebook) ad testing and scaling using the user's course rules in ~/council - test budgets, CBO 3x3 campaign structure, batch cadence, kill/scale/descale decisions, reading ad metrics, and keeping the creative log. Use when the user asks how to launch or structure a test, whether to kill or scale an ad/ad set, what budget to use, why ads aren't converting, or to log ad results.
---

# ecom-media-buying

Follow `~/council/kb/skill-protocol.md`. Bundle: `media-buying` (plus `offer` for conversion problems).

## Always establish the stage first
The rules differ by stage, so name it in the answer:
- testing (no consistent sales)
- < $1k/day
- $1k–3k/day
- > $3k/day

## Modes
- **Launch plan:**
  - Campaign structure (CBO, 3 ad sets = 3 angles, 3 ads each, 2PT/2HL).
  - Budget: $75–100/day, $25–30 per ad set.
  - Geo: latest rule.
  - Batch cadence.
  - Which angles and creatives to use, from `angles.yaml` / `creatives.yaml`.
  Output a checklist the user can follow in Ads Manager.
- **Decision (kill / keep / scale / descale):**
  - Get the metrics (spend, purchases, ROAS, CPC, CPM, hook/hold rate, days live, AOV, break-even ROAS).
  - Apply the stage-specific rules and benchmarks, and cite each rule tag.
  - Flag "⚠ was:" rules when the user is following old advice.
  - Never recommend a cut after one bad day once profitable.
- **Diagnose "not converting":**
  - Walk soft → hard metrics.
  - Pull the Shopify funnel (sessions → ATC → checkout → purchase).
  - Separate a creative problem from an offer/page problem (incongruence, offer, checkout).
  - Hand page and offer fixes to `ecom-pages`.
- **Log results:**
  - Update `creatives.yaml` rows: spend, purchases, ROAS, rates, verdict, learning.
  - Add a dated `log.md` entry. Both after confirmation.
  - Winners → set the angle status to `winner` in `angles.yaml`, and recommend iterations.

Break-even ROAS/CPA must come from `product.yaml → economics`. If it's TODO, ask for COGS, shipping and fees and compute it. Don't guess.
