---
name: ecom-angles
description: "Build a product's unique mechanism, extract mass desires, and create ad angles using the user's course prompts in ~/council (Mechanism Prompt, Desire Extraction Prompt 1, Angle Creation Prompt 2), including the long-form native ad story. Use when the user asks for a mechanism, why-it-works positioning, desires, angles, ad concepts, or a native ad story for an avatar."
---

# ecom-angles

Follow `~/council/kb/skill-protocol.md`. Usual order: mechanism → desires → angles. Skip any step that's already `chosen` in state, unless the user wants to redo it.

## 1. Mechanism (bundle `mechanism`, `kb/angles/mechanisms.md`)
- Ensure `product.yaml` has features → benefits → desires filled from facts. Ask for missing facts; don't invent.
- Run Parts 1–4:
  1. Customer and failed-solutions table, each failure with a provable reason.
  2. Differentiators table.
  3. Fresh mechanism angles; discard any competitors already use (check `product.yaml → competitors`).
  4. Final statement in the exact template, plus 2–3 problem-aware hook directions.
- Grade it on the 4-point checklist. Flag claims that need proof.
- Write → `mechanism.yaml`.

## 2. Desires (bundle `desires`, `kb/angles/desires.md`)
- Needs a filled avatar profile; if missing, offer `ecom-avatar` first.
- Output 4–8 desires in the exact format, each with its fit rating.
- Write → `desires.yaml` (ids D1…).

## 3. Angles (bundle `angles`, `kb/angles/angles.md`)
- Generate 3–5 angles in the exact format. Each must pass the differentiation checklist and be built from real quotes.
- Feed the chosen mechanism into "unique root cause".
- Check `creatives.yaml` so you don't repeat dead angles, and mine any winner first.
- The user picks one. Ask whether they have reference story copy.
- **Native image ad:** write the 1,100–1,400-word primary-text story (step 2 rules). Self-check it against `foundations/house-rules.md`.
- Write → `angles.yaml` (ids A1…, status `idea`).

## Next
`ecom-script` (video), `ecom-pages` (advertorial/listicle), or `ecom-script` ad-copy mode (primary text + headlines).
