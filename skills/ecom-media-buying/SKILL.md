---
name: ecom-media-buying
description: Plan and manage Meta (Facebook) ad testing and scaling using your playbook in ~/council/kb - test budgets, campaign structure, batch cadence, kill/scale/descale decisions, reading ad metrics, and keeping the creative log. Use when the user asks how to launch or structure a test, whether to kill or scale an ad/ad set, what budget to use, why ads aren't converting, or to log ad results.
---

# ecom-media-buying

Follow `~/council/skills/protocol.md`. Bundle: `media-buying` (+ `offer` for conversion problems). Structure, budgets, cadence, stage thresholds and kill/scale rules all come from `kb/media-buying/*`; cite the rule you apply.

**Establish the spend stage first** (the KB's stage definitions) and name it, since the rules differ by stage.

- **Launch plan:** campaign structure, budget, geo and batch cadence per `testing.md`; angles and creatives from `angles.yaml` / `creatives.yaml`. Output a checklist to follow in Ads Manager.
- **Decision (kill / keep / scale / descale):** get the numbers (spend, purchases, ROAS, CPC, CPM, hook/hold rate, days live, AOV). Apply the stage rules and `benchmarks.yaml`; cite each rule; flag `⚠ was:` rules the user is still following. Never cut a profitable ad set after one bad day.
- **Diagnose "not converting":** walk soft → hard metrics; pull the Shopify funnel; separate creative problems from offer/page problems; hand page and offer fixes to `ecom-pages`.
- **Log results:** update `creatives.yaml` rows and add a dated `log.md` entry, after confirmation. Winners → angle status `winner`, and recommend iterations.

Break-even ROAS/CPA comes from `product.yaml → economics`; if missing, ask for COGS, shipping and fees and compute it. For a budget decision with real money at stake, offer `/council performance:`.
