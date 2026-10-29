---
topic: Avatar workflow: find sub-avatars → score → deep dive
load_when: building or choosing avatars/sub-avatars; any customer research
sources: [d:avatar-research-prompt, d:avatar-build-scorecard, d:avatar-deep-dive-prompt, d:avatar-breakdown-template, c:06-18, c:06-25, c:07-06, c:08-06, c:08-24, c:08-27, c:09-17, c:10-12, c:10-15]
updated: 2026-10-29
---
# Step 1: Find sub-avatars [d:avatar-research-prompt]
- Input: the core problem.
- Goal: groups "large enough to allow us to scale to 1 million dollars a month… but specific enough that we can create ads that really speak to them."
- Mine Amazon reviews, Facebook groups, Reddit, YouTube comments, TikTok comments, forums.
- Extract "short, powerful sentences" directly about the problem; drop anything unconnected.
- Group by: who they are + their specific problem + what they want to become.
- Ban generic avatars ("Busy Professional", "Fitness Enthusiasts"). Define by past experiences, emotions, failed solutions, desired outcomes.

# Step 2: Score [d:avatar-build-scorecard]
- Per sub-avatar: demographic, what they want, awareness stage, failed solutions, real quotes with links.
- Then score with the 4-criterion scorecard in research/validation.md.
- Big swings when testing new avatars: distinct avatar types, not fine slices [c:06-18, c:06-25, c:08-06].

# Step 3: Deep dive → fill avatars/avatar-schema.yaml [d:avatar-deep-dive-prompt]
- Inputs: schema, raw research/reviews, sub-avatar description.
- Research Reddit, YouTube comments, forums, blogs. Multiple sources.
- Rules:
  1. Real quotes only, in quotes. If none: "No direct data found – manual research needed". Never infer quotes.
  2. Pattern = 3+ people saying similar things.
  3. Organize exactly by schema sections.
  4. Prioritize emotional depth: the WHY behind the frustration.
  5. Capture exact phrases and metaphors (these become hooks).
  6. No personal bias.
- Output per section: Key Findings (patterns) + Supporting Quotes ("quote" – source context). Analysis in 8th-grade language.

# From the owner's notes [n:ball]
- Don't target the broad avatar (e.g. "dry skin"): more people with the problem means more sellers. Go to sub-avatars, e.g. menopausal women, eczema, healthcare workers, Black women, male office workers.
- Chain each one: sub-avatar → desired outcome → who they want to become. E.g. menopausal dry skin → moisturized skin → feel younger and confident → stop comparing herself to her younger self.
- Find as many sub-avatars as possible, filter, then deep-dive ONE. Keep the profiles worth a deep dive; delete the rest.
- A new underserved avatar can turn a break-even product profitable even with ripped ads. Example: the same product sold to parents of kids with sensory issues, found by searching the product + "kids" on TikTok.
- Tools: VOC.AI (export Amazon reviews), youtube-transcript.io, TikTok search for people with the issue.

# Course heuristics
- Manual research beats AI. Train a dedicated Google account's YouTube feed on the niche [c:10-12]. Text/SMS existing customers [c:09-17]. Combine data with "empathetic imagination" to find hidden beliefs [c:07-06].
- Iterate deep on a WINNING avatar (many ads per sub-avatar) before diversifying [c:06-25, c:10-15].
- Congruence across ad, PDP, testimonials, imagery, and language for the sub-avatar [c:06-25]. Listicle headlines tailored per avatar [c:08-27].
- A mechanism that works for one group can be repositioned to another (acne: African American customers → gym-goers) [c:08-24].
- New desire vs another sub-avatar on the same desire: depends on scaling ceiling and TAM. If several batches tested it conclusively, move to a new desire [c:06-18].
- Format by avatar: younger audiences want fast pacing, relatable people, cultural cues, raw UGC [c:06-29, c:08-06]. Otherwise test [c:09-07].
