---
name: ecom-avatar
description: Build customer avatars and sub-avatars from real research (Reddit, reviews, YouTube comments, forums) using your playbook in ~/council/kb - find sub-avatars, score them, deep-dive into a full profile. Use when the user says build my avatar, sub-avatar, customer research, who is my customer, avatar breakdown, or research my target market.
---

# ecom-avatar

Follow `~/council/skills/protocol.md`. Bundle: `avatar`. The steps, scorecard and quality bar are in `kb/avatars/avatar-workflow.md`; the profile shape is `kb/avatars/avatar-schema.yaml`.

1. **Find sub-avatars.** Start from the core problem in `product.yaml`. Research customer language with WebSearch/WebFetch (`site:reddit.com "<problem>"`, marketplace reviews, YouTube comments, forums). Group real quotes into specific sub-avatars (who + problem + what they want to become). No generic avatars.
2. **Score** each on the KB scorecard. Market-size and competition scores use the owner's evidence (see `ecom-research`); otherwise mark them NEEDS DATA. Recommend the most distinct candidates and let the user choose.
3. **Deep dive** the chosen one into the schema: real quotes only, each with its source link; patterns only when the KB's minimum number of people say it; missing data → "No direct data found – manual research needed".
4. **Quality check** against the workflow file's checklist.
5. **Gate:** offer `/council market:` on the chosen sub-avatar before writing angles.
6. **Write back** after confirmation: `products/<p>/avatars/<slug>.yaml` + `log.md`. Next: `ecom-angles`.
