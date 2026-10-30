---
topic: "Meta testing: budgets, structure, batch cadence, kill rules"
load_when: planning a launch/test, structuring campaigns, deciding what to kill
sources: [d:campaign-structure, n:ecom-resources, c:06-15, c:06-18, c:06-25, c:07-06, c:07-09, c:07-16, c:07-20, c:07-23, c:08-03, c:08-06, c:08-10, c:08-13, c:08-17, c:08-24, c:09-07, c:09-14, c:09-17, c:09-21, c:10-05, c:10-08, c:10-12, c:10-19]
updated: 2026-10-29
---
# Structure (current standard)
- CBO campaign → 3 ad sets, one ANGLE per ad set → 3 ads each (+ optional ads 4–5). Each ad has 2 PT / 2 HL [d:campaign-structure]. "3×3" [n:ecom-resources].
- Start with 3 ad sets on 3 distinct angles; add a 4th later [c:08-10].
- Alternative "Structure 2: ABO + scaling CBO" [n:ball img11-17]:
  - ABO campaign A holds ripped ads (1 ad per ad set).
  - ABO campaign B holds custom angles (batches of 3 ads per ad set).
  - Any ad set performing ≥ 20% above break-even ROAS graduates (same post ID) into a scaling CBO.
  - Pros: finds winners faster, isolated tests, quick decisions, rescues ads that a CBO starved.
  - Cons: costs more, won't beat a plain CBO long-term, adds complexity, can distract from making better ads.
  - Default for beginners stays CBO [c:08-24].
- Max 5 ads per ad set [n:ball]. Ripped-ad ad sets can run at $20/day. Always launch with post IDs [n:ball].
- CBO for beginners [c:08-24].
- New ads go in NEW ad sets; never edit live ones [c:07-09, c:09-07]. A fresh campaign per new batch; don't delete old campaigns [c:09-14].
- Images and video in separate ad sets [c:06-18, c:08-03, c:10-12].
- ⚠ Ripped ads in a SEPARATE campaign from originals [c:09-07] (was: 1 ripped ad set inside [c:06-15, c:07-16, c:08-24]). They fatigue fast and stunt skill-building [c:10-22].
- Broad targeting beats fragmented ad sets. To force spend on a segment, make a new campaign. Use exclusions where needed (e.g. female-only for shapewear). Turn off unwanted Meta AI toggles [c:09-14].
- Optimize for PURCHASE, not ATC [c:07-06, c:07-23].
- Launch at midnight [c:08-10]. Option: launch 1 ad set, wait 24h, then the rest [c:08-13].
- ⚠ Min-spend per ad set: dropped [c:09-21] (was: $5 minimums [c:07-20, c:08-03]).
- Geo (latest): one US campaign + one worldwide-excluding-US campaign, excluding Asia, Russia, Africa (keep South America). Run both only if budget supports both. Reuse the same post ID across campaigns [c:10-19]. ⚠ was: one campaign per country/language [c:07-06, c:09-14] → US + top 4–5 combined [c:09-24]. The full WW exclusion list (~130 countries) is in `_sources/notion/dashboard-pages.md` [n:dash]. ⚠ That list (edited 10-07) also excludes Argentina and Brazil; the later call says keep South America [c:10-19]. Confirm with the owner before applying.

# Budget
- Minimum $75–100/day CBO, over 2–3 days [c:08-10, c:07-23, c:09-14, c:10-05]. ($50/day only with ≤2 ad sets and images; it can't reach break-even CPA at a $55–65 AOV [c:08-10].)
- ~$25–30 per active ad set, so $100 supports 3–4 ad sets (fewer is better) [c:10-19]. Higher AOV justifies a higher test budget [c:07-16].
- Before any sales, cap at $100–150/day [c:10-12].

# Cadence
- Batch = 3 ads. 4–5 batches/week, spaced across days [c:07-06, c:09-14]. Mix: 1 iteration batch + 4 new-concept batches [c:07-23]. 3 variations per angle per ad set [c:09-07].
- Hit rate ~12–15% of ads become winners [c:08-06]. A "winner" sustains or dominates spend at scale, not one that gets occasional sales [c:10-05].
- Big swings (different concept, avatar, or offer) until an ad reaches ~$300–400/day; then isolate variables [c:10-19, c:10-05, c:07-06, c:09-14]. ⚠ was: one variable at a time [c:07-23, c:08-06].
- Keep a creative/feedback tracker: hypothesis, angle, avatar, format, hook, metrics, verdict (products/<p>/creatives.yaml) [c:08-17].
- Engagement campaigns for ~2 weeks can warm audiences [c:08-17].

# Kill rules (by stage)
- Course module flowchart, per ad set on a $100/day test [n:ball img18-19]:
  - Day 1, at $50 spent:
    - CPC < $5 or 1 sale → leave running.
    - CPC > $5 and no sales → cut.
  - Day 2:
    - 30–40% of budget spent, still no sales → cut.
    - ROAS within ±5–15% of break-even → keep running.
    - ROAS ≥ 25% below break-even → cut.
    - ROAS 30–40% above break-even → scale. ⚠ Superseded for scaling: wait ~a week and judge on 7 days [c:10-19]. The day-2 cut rules still match the calls.
  - Day 3: repeat.
  - CBO with multiple ad sets: after 7 days, cut ad sets with $0 or only minimum spend.
- Testing:
  - No sales and no ATC by day 2 → kill [c:07-16].
  - No sales after 2 days → kill, unless near break-even [c:07-20, c:07-23].
  - Give CBO 2–3 full days [c:09-07].
  - Ad set ROAS ~0.2 → cut [c:07-09].
- < $1k/day: cut unprofitable ad sets quickly; budget concentrates on the best [c:07-09].
- At scale:
  - Keep top-of-funnel ad sets.
  - Cut only if an ad set takes ≥30% of budget AND campaign ROAS stays below break-even for several days.
  - Review weekly [c:08-13]. Don't kill winners prematurely [c:09-17].
- Non-spending ads: off after 7 days [c:10-05, c:10-08]. Some winners appeared in week 3, so 1–2 weeks is acceptable [c:09-21].
- Judge on 7 days; never cut after one bad day once profitable [c:10-19].

# Effort split
- 70–80% creative, 20–30% LP and offer [c:09-24]. Hard metrics (purchases, ROAS) over soft (CTR, CPC, ATC) [c:06-18].
