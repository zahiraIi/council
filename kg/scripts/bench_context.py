"""Context-size benchmark: how many tokens each context strategy loads for the same
20 council/skill tasks, and whether the rules each task needs ("gold") are in context.

Setups
  full    every kb/ file (what you'd paste with no routing)
  bundle  the hand-written index.yaml bundle for the task + `always` files
  graph   `always` files + top-k kg_search hits (full node text)

Tokens are counted with tiktoken cl100k_base as a proxy for Claude's tokenizer (counts
differ by roughly ±15%; the ratios between setups are what matter). Gold recall is a
retrieval-quality proxy, not a measure of final answer quality.

  uv run python scripts/bench_context.py [--k 8] [--md results/context.md]
"""
import argparse, functools, os, sys

import tiktoken
import yaml

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from councilkg import DB_PATH, REPO_ROOT, embeddings  # noqa: E402
from councilkg.store import Store  # noqa: E402

K = "kb:"
# (task, bundle, gold id prefixes: rules a good answer must use)
TASKS = [
    ("An ad set is at 1.3x break-even ROAS after 3 days. Should I scale it now?", "media-buying",
     [K + "media-buying/scaling.md#when"]),
    ("CTR is 2%, CPC $1, but CVR is 0.4%. Kill the ad, iterate, or fix the page?", "media-buying",
     [K + "media-buying/growth-review.md#diagnosis", K + "media-buying/testing.md#kill-rules"]),
    ("Plan the structure and daily budget for my next creative test batch.", "media-buying",
     [K + "media-buying/testing.md#structure", K + "media-buying/testing.md#budget"]),
    ("Write 3 hooks for problem-aware dog owners scared of hurting their dog's nails.", "script",
     [K + "creative/hooks.md#types", K + "foundations/awareness.md"]),
    ("Check this script's bridge and call to action.", "script-check",
     [K + "creative/script-standards.md#3-bridge", K + "creative/script-standards.md#9-cta"]),
    ("Deconstruct this competitor's winning video ad transcript.", "deconstruct",
     [K + "creative/ad-deconstruction.md"]),
    ("Write primary text and headlines for a static image ad.", "ad-copy",
     [K + "creative/primary-text-headlines.md#rules"]),
    ("Build the unique mechanism for a quiet pet nail grinder.", "mechanism",
     [K + "angles/mechanisms.md#workflow", K + "angles/mechanisms.md#quality-checklist"]),
    ("Generate 3 distinct ad angles for nervous dog owners.", "angles",
     [K + "angles/angles.md#step-1"]),
    ("Extract the mass desires from these Reddit quotes about trimming pet nails.", "desires",
     [K + "angles/desires.md"]),
    ("Which landing page type should a problem-aware ad send traffic to?", "page",
     [K + "pages/landing-pages.md#page-type-awareness-matrix"]),
    ("Write the advertorial headline, hero image direction and lead copy.", "page",
     [K + "pages/landing-pages.md#advertorial-3-critical-elements"]),
    ("Design a bundle offer that raises AOV for a durable tool.", "offer",
     [K + "pages/offers.md#offer-types", K + "pages/offers.md#economics"]),
    ("Should I add a post-purchase upsell and shipping protection?", "offer",
     [K + "pages/offers.md#cart-and-post-purchase-aov"]),
    ("Audit my product page for conversion problems.", "store-audit",
     [K + "pages/store-audit-checklist.md"]),
    ("Is a $40 nail grinder with $8 COGS worth testing?", "research",
     [K + "research/product-research.md#unit-economics-gate"]),
    ("Is the 'senior dog owners' sub-avatar big and distinct enough to target?", "validate",
     [K + "research/validation.md#sub-avatar-scorecard"]),
    ("Find sub-avatars for a pet nail grinder.", "avatar",
     [K + "avatars/avatar-workflow.md#step-1"]),
    ("Plan my Black Friday offer and timing.", "offer",
     [K + "pages/offers.md#holiday-bf"]),
    ("Set up an email popup and the core automated flows.", "ops",
     [K + "ops/email-retention.md#popups", K + "ops/email-retention.md#flows"]),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--k", type=int, default=8)
    ap.add_argument("--md", help="also write a markdown results table here")
    a = ap.parse_args()
    enc = tiktoken.get_encoding("cl100k_base")
    tok = functools.lru_cache(maxsize=None)(lambda text: len(enc.encode(text)))
    kb = os.path.join(REPO_ROOT, "kb")
    index = yaml.safe_load(open(os.path.join(kb, "index.yaml"), encoding="utf-8"))

    def file_text(rel):
        return open(os.path.join(kb, rel), encoding="utf-8").read()

    all_files = sorted(os.path.relpath(os.path.join(d, f), kb) for d, _, fs in os.walk(kb) for f in fs
                       if f.endswith((".md", ".yaml")) and f != "index.yaml")
    full_tokens = sum(tok(file_text(f)) for f in all_files)
    always = index.get("always") or []
    always_tokens = sum(tok(file_text(f)) for f in always)

    s = Store(DB_PATH)
    emb = embeddings.embed_query
    rows = []
    for task, bundle, gold in TASKS:
        bfiles = list(dict.fromkeys((index["bundles"][bundle]["kb"] or []) + always))
        b_tokens = sum(tok(file_text(f)) for f in bfiles)
        b_recall = sum(any(g[len(K):].split("#")[0] == f for f in bfiles) for g in gold) / len(gold)
        hits = s.search(task, limit=a.k, embed_fn=emb)
        g_tokens = always_tokens + sum(tok(f"{h['name']}\n{h['text']}") for h in hits)
        g_recall = sum(any(h["id"].startswith(g) for h in hits) for g in gold) / len(gold)
        # hybrid (what the council does): bundle baseline + graph hits from outside the bundle
        extra = [h for h in hits if (h.get("meta") or {}).get("path", "")[3:] not in bfiles]
        h_tokens = b_tokens + sum(tok(f"{h['name']}\n{h['text']}") for h in extra)
        h_recall = max(b_recall, g_recall)
        rows.append((task, bundle, b_tokens, b_recall, g_tokens, g_recall, h_tokens, h_recall, len(extra)))

    n = len(rows)
    avg = lambda i: sum(r[i] for r in rows) / n
    b_tok, b_rec, g_tok, g_rec, h_tok, h_rec, h_extra = avg(2), avg(3), avg(4), avg(5), avg(6), avg(7), avg(8)
    lines = [
        f"Context benchmark: {n} tasks, graph top-k={a.k}, tokens = tiktoken cl100k (proxy)",
        "",
        "| Setup | Avg tokens loaded | vs full KB | Gold-rule recall |",
        "|---|---:|---:|---:|",
        f"| Full KB (all {len(all_files)} files) | {full_tokens:,} | — | 100% |",
        f"| Hand-written bundles (index.yaml) | {b_tok:,.0f} | -{100 * (1 - b_tok / full_tokens):.0f}% | {100 * b_rec:.0f}% |",
        f"| Graph retrieval (always + top-{a.k}) | {g_tok:,.0f} | -{100 * (1 - g_tok / full_tokens):.0f}% | {100 * g_rec:.0f}% |",
        f"| Bundle + graph evidence (council design) | {h_tok:,.0f} | -{100 * (1 - h_tok / full_tokens):.0f}% | {100 * h_rec:.0f}% |",
        "",
        f"Bundle + graph adds {h_extra:.1f} out-of-bundle nodes per task on average (raw-source chunks and",
        "cross-bundle rules the bundle can't reach).",
        "",
        "Per task (bundle tokens / recall · graph tokens / recall):",
    ]
    for task, bundle, bt, br, gt, gr, *_ in rows:
        lines.append(f"- [{bundle}] {task[:70]} — {bt:,} / {br:.0%} · {gt:,} / {gr:.0%}")
    out = "\n".join(lines)
    print(out)
    if a.md:
        os.makedirs(os.path.dirname(os.path.abspath(a.md)), exist_ok=True)
        with open(a.md, "w", encoding="utf-8") as f:
            f.write(out + "\n")


if __name__ == "__main__":
    main()
