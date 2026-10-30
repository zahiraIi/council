---
name: ecom-angles
description: Build a product's unique mechanism, extract mass desires, and create ad angles using your playbook in ~/council/kb, including the long-form native ad story. Use when the user asks for a mechanism, why-it-works positioning, desires, angles, ad concepts, or a native ad story for an avatar.
---

# ecom-angles

Follow `~/council/skills/protocol.md`. Order: mechanism → desires → angles. Skip a step that's already `chosen` in state unless the user wants to redo it.

## 1. Mechanism (bundle `mechanism`, `kb/angles/mechanisms.md`)
- `product.yaml` needs features → benefits → desires from facts. Ask for missing facts.
- Follow the KB file's steps and output template; discard mechanisms competitors already use (`product.yaml → competitors`, from the owner's research).
- Grade it on the KB checklist and flag every claim that needs proof. Write → `mechanism.yaml`.

## 2. Desires (bundle `desires`, `kb/angles/desires.md`)
- Needs a filled avatar profile; if missing, offer `ecom-avatar` first.
- Output desires in the KB format with fit ratings. Write → `desires.yaml` (ids D1…).

## 3. Angles (bundle `angles`, `kb/angles/angles.md`)
- Generate angles in the KB format, built from real quotes and passing the KB's differentiation checklist. Feed the chosen mechanism into the root cause.
- Check `creatives.yaml`: don't repeat dead angles; mine winners first.
- Native image ad: write the long-form story per the KB, then self-check against `foundations/house-rules.md`.
- **Gate:** offer `/council market:` on the angles you'd test, with the owner's competition evidence. Write → `angles.yaml` (status `idea`; `chosen` only after the user picks).

Next: `ecom-script` (video, ad copy) or `ecom-pages` (advertorial, listicle).
