---
name: council
description: Run a question through an LLM Council (after karpathy/llm-council) using only Claude Code subagents, no OpenRouter or API key. Members answer independently with task-specific roles, anonymously peer-review each other against a task rubric, and a chairman synthesizes. Has modes for ecommerce work backed by the ~/council knowledge base (research, avatar, angles, script, copy, page, offer, store-audit, media-buying) and for software/ML (dev-ml), plus general. Use when the user says "/council", "ask the council", "run this through a council", or wants multiple models to debate, compare, or review options.
---

# LLM Council

Input: `$ARGUMENTS`, in the form `[mode:] question`. If it's empty, ask for the question.

## Step 0: Mode and context packet
1. **Mode.** Take the explicit prefix (`/council script: …`) or infer it from the question. Ask only if two modes fit equally. The mode files are in `modes/` next to this file:
   `research`, `avatar`, `angles`, `script`, `copy`, `page`, `offer`, `store-audit`, `media-buying`, `dev-ml`, `general`.
   Read the chosen mode file.
2. **Context.**
   - **Ecom modes:** follow `~/council/kb/skill-protocol.md` steps 1–3. Resolve the product, load the mode's bundle(s) from `~/council/kb/index.yaml` (kb files + `always` + product state), and pull any live data the mode lists (Shopify, WebFetch).
   - **dev-ml:** gather what the mode file lists.
   - **general:** use only what's in the conversation.
3. **Packet.** Write one context packet to the scratchpad (`council-packet.md`) with these sections:
   - `## Task` (the question verbatim)
   - `## Product state`
   - `## Knowledge base rules` (the loaded files; strip their frontmatter)
   - `## Live data`
   - `## Artifacts under review` (scripts, pages, ads, code)

   Keep it under ~12k tokens. Trim the least relevant KB files first, never the task or the artifacts. Tell the user in one line which mode, product and files were loaded.

## Council
- Members: `opus`, `sonnet`, `haiku`, `fable`. Each is a fresh subagent via the Agent tool with `model` set; `subagent_type: general-purpose`. Chairman: a fresh `opus`.
- Members get no tools and no conversation context. The packet is pasted in full into every member prompt.
- Assign the mode's roles to members in the order listed: opus = role 1, sonnet = role 2, haiku = role 3, fable = role 4. `general` has no roles.
- If a member fails, drop it. Abort only if fewer than 2 answered.

## Stage 1: Independent answers
In ONE message, spawn all members in parallel. Prompt:

```
You are {role} on an advisory council. {role description from mode file}
Answer the task below using the context packet. Follow every rule in "Knowledge base rules"; when you rely on one, cite its tag (e.g. [c:10-19]). Never invent facts, quotes, prices, or metrics; write NEEDS DATA: instead.
Output format: {mode's member output format}
Do not use tools.

{packet}
```

## Stage 2: Anonymous peer review
1. Shuffle the successful answers and label them `Response A`, `Response B`, …. Keep a private label → model/role map. Reviewers never see model names or roles.
2. In ONE message, spawn every member again in parallel:

```
You are evaluating responses to this task.

{packet}

Responses (anonymized):

Response A:
...

Rubric: score each response against these criteria and the knowledge base rules:
{mode's rubric}

Your task:
1. Evaluate each response individually against the rubric: strengths, weaknesses, any rule violations or invented facts.
2. Then, at the very end, give a final ranking.

IMPORTANT: Your final ranking MUST be formatted EXACTLY as follows:
- Start with the line "FINAL RANKING:" (all caps, with colon)
- Then list the responses from best to worst as a numbered list
- Each line: number, period, space, then ONLY the response label (e.g. "1. Response C")
- Do not add any other text after the ranking section

Do not use tools.
```

3. Parse each `FINAL RANKING:` section. If one doesn't parse, fall back to the order in which `Response X` labels appear; if nothing parses, skip that reviewer.
4. Aggregate: average rank position per label (1 = best), sorted ascending. Map labels back to model and role.

## Stage 3: Chairman
Spawn one `opus` with: the packet, all Stage 1 answers (model and role named), all Stage 2 evaluations, and the aggregate ranking. Instruction:

```
You are the Chairman of an LLM Council. Synthesize one final answer in the mode's chairman format: {format}.
- Weigh the peer rankings, resolve disagreements explicitly, and keep every claim traceable to the packet (cite KB tags).
- Remove anything a reviewer flagged as invented or rule-breaking.
- Note genuine uncertainty and what data would resolve it.
Do not use tools.
```

## Output to the user
1. The final answer (chairman).
2. Aggregate ranking table: rank, model (role), average position, votes.
3. Notable disagreements: 2–4 bullets.
4. An offer to show any raw answer or evaluation.

## Step 4: Write-back (ecom modes)
Propose the state updates the mode file lists (e.g. a chosen angle into `angles.yaml`, a dated `log.md` entry "council <mode>: decision, why"). Write only after the user confirms. Never edit Shopify from the council; hand that to `ecom-pages` with an explicit diff.

## Notes
- Cost is about 9 subagent calls plus a large packet ×9. For trivial questions, say the council is overkill and answer directly, or suggest the matching ecom-* skill.
- The council is for judgment calls and quality passes (choose, compare, critique, decide). Step-by-step production belongs to the ecom-* skills; the council can review their output.
- Claude-only council: reviewers may recognize their own style, so anonymization reduces self-preference but doesn't remove it.
