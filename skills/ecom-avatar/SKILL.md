---
name: ecom-avatar
description: "Build customer avatars and sub-avatars from real research (Reddit, reviews, YouTube comments, forums) using the user's course workflow in ~/council: find sub-avatars, score them, deep-dive into a full profile. Use when the user says build my avatar, sub-avatar, customer research, who is my customer, avatar breakdown, or research my target market."
---

# ecom-avatar

Follow `~/council/kb/skill-protocol.md`. Bundle: `avatar` (`~/council/kb/index.yaml`).

## Steps (from `kb/avatars/avatar-workflow.md`)
1. **Find sub-avatars.**
   - Start from the core problem in `product.yaml`.
   - Research with WebSearch/WebFetch: `site:reddit.com "<problem>"`, Amazon reviews of competitors, YouTube comments, forums, Facebook group posts where visible.
   - Pull short, powerful sentences and group them into 3–6 specific sub-avatars (who + problem + what they want to become).
   - No generic avatars.
2. **Score** each sub-avatar on the 4-criterion scorecard (desire strength, competition, TAM for $1M/mo, product fit), with evidence links. Recommend 1–3 distinct sub-avatars to deep-dive (big swings, not slices). Let the user choose.
3. **Deep dive** the chosen sub-avatar into `kb/avatars/avatar-schema.yaml`, following the deep-dive rules:
   - Real quotes only, with source. A pattern needs 3+ people. Organize by schema section.
   - Emotional depth first. Capture 10–15 exact phrases.
   - Missing data → "No direct data found – manual research needed".
4. **Quality check:**
   - Real quotes.
   - Patterns flagged.
   - 10–15 phrases.
   - Awareness level justified.
   - A vivid day-in-the-life.
   - Scorecard filled.
5. **Write back** (after confirmation): `products/<p>/avatars/<slug>.yaml` plus a `log.md` entry.
6. **Next step:** `ecom-angles` (mechanism → desires → angles) for this avatar.
