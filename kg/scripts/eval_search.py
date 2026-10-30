"""Known-item retrieval eval for kg search (after ATLAS scripts/eval_search.py).
Each query lists acceptable ids (prefix match). Reports hit@1 / hit@5 for keyword-only
vs hybrid, plus how many results off-topic controls return (should be 0).

  uv run python scripts/eval_search.py            # current settings
  uv run python scripts/eval_search.py --sweep    # grid over SIM_FLOOR
"""
import argparse, functools, os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from councilkg import DB_PATH, embeddings  # noqa: E402
from councilkg.store import Store  # noqa: E402

K = "kb:"
CASES = [
    # paraphrases of KB rules
    ("when should I raise the budget on a winning ad set", [K + "media-buying/scaling.md#when", K + "media-buying/scaling.md#how-much"]),
    ("how much can I increase spend per day once I'm above a thousand", [K + "media-buying/scaling.md#how-much"]),
    ("when do I cut a losing ad set", [K + "media-buying/testing.md#kill-rules", "src:notion/images#img19"]),
    ("how many ads should go in each ad set when testing", [K + "media-buying/testing.md#structure"]),
    ("what daily budget should I test new creatives with", [K + "media-buying/testing.md#budget"]),
    ("how often should I launch new batches", [K + "media-buying/testing.md#cadence"]),
    ("people click but nobody buys", [K + "media-buying/growth-review.md#diagnosis-rules-of-thumb", K + "pages/offers.md#checkout-diagnostic", K + "media-buying/growth-review.md#scale-hold-fix-pause"]),
    ("lots of add to carts and checkouts but zero purchases", [K + "pages/offers.md#checkout-diagnostic"]),
    ("what goes in the first three seconds of a video ad", [K + "creative/script-standards.md#2-hook", K + "creative/hooks.md#types"]),
    ("hooks for people who don't know they have the problem", [K + "creative/hooks.md#unaware-hooks", K + "creative/hooks.md#types"]),
    ("how do I transition from the hook into the body of the script", [K + "creative/hooks.md#bridges", K + "creative/script-standards.md#3-bridge"]),
    ("break down a competitor's winning video ad", [K + "creative/ad-deconstruction.md"]),
    ("what makes a good unique mechanism", [K + "angles/mechanisms.md#quality-checklist", K + "angles/mechanisms.md#4-types"]),
    ("difference between an angle and a hook", [K + "angles/angles.md#what-an-angle-is", K + "angles/angles.md#working-formula"]),
    ("how many stages of market sophistication are there", [K + "foundations/sophistication-desire.md#sophistication-stages"]),
    ("which landing page type for problem aware traffic", [K + "pages/landing-pages.md#page-type-awareness-matrix", K + "pages/landing-pages.md#match-the-page-to-the-ad"]),
    ("advertorial headline and hero image", [K + "pages/landing-pages.md#advertorial-3-critical-elements"]),
    ("post purchase upsell only shows in store currency", [K + "pages/offers.md#cart-and-post-purchase-aov", "src:notion/images#img34"]),
    ("should I charge for shipping", [K + "pages/offers.md#cart-and-post-purchase-aov", "src:notion/images#img36"]),
    ("bundle and BOGO offer examples", [K + "pages/offers.md#offer-types"]),
    ("black friday offer timing", [K + "pages/offers.md#holiday-bf"]),
    ("subscription churn rate", [K + "pages/offers.md#subscriptions"]),
    ("email popup and welcome flow", [K + "ops/email-retention.md"]),
    ("minimum markup and AOV for a product to be viable", [K + "research/product-research.md#unit-economics-gate"]),
    ("how do I know if it's a creative problem or a product problem", [K + "research/validation.md#ad-problem-or-product-problem"]),
    ("score a sub avatar before deep diving", [K + "research/validation.md#sub-avatar-scorecard", K + "avatars/avatar-workflow.md#step-2-score"]),
    ("who should I hire first", [K + "ops/operations.md#hiring-order"]),
    ("where to find UGC creators and what to pay them", [K + "creative/script-brief.md#sourcing-ugc", K + "creative/script-brief.md#content-sourcing-path"]),
    # raw-source questions
    ("what did the guest speaker say about batches", ["src:calls/2026-08-27"]),
    ("Schwartz on the mass desire that already exists in the market", ["src:books/schwartz", K + "foundations/sophistication-desire.md#mass-desire"]),
    ("worldwide campaign country exclusions", [K + "media-buying/testing.md", "src:notion/dash"]),
]
OFF_TOPIC = ["write a poem about the ocean", "what is the capital of France",
             "fix the segfault in my C firmware", "best pizza recipe"]

# HELD-OUT set: written 2026-10-29 after Store settings were frozen (weights (2,0.5,2),
# floor/gate 0.62, chunk damp 0.4). Never tune on these; report them as the headline number.
# "kb" cases are answered by KB nodes alone (what a public clone without _sources can do).
B = K + "media-buying/benchmarks.yaml#"
HELDOUT = [
    ("what hook rate should my videos hit", [B + "hook-rate-min", K + "creative/script-standards.md#post-launch"], "kb"),
    ("how much should each ad set get per day", [B + "budget-per-ad-set", K + "media-buying/testing.md#budget"], "kb"),
    ("what percent of launched ads become winners", [B + "winner-hit-rate"], "kb"),
    ("is a high CPM on a new ad account a problem", [B + "cpm"], "kb"),
    ("what opt-in rate should my email popup get", [B + "email-popup-optin-target", K + "ops/email-retention.md#popups"], "kb"),
    ("which emails should be automated after signup or an abandoned checkout", [K + "ops/email-retention.md#flows"], "kb"),
    ("how do I write the ad copy that goes above the video", [K + "creative/primary-text-headlines.md"], "kb"),
    ("can I make up testimonials or doctor claims", [K + "foundations/house-rules.md#integrity"], "kb"),
    ("which AI-sounding phrases should I avoid in copy", [K + "foundations/house-rules.md#language"], "kb"),
    ("what are the five awareness levels", [K + "foundations/awareness.md#awareness-levels"], "kb"),
    ("how do I pull the deep emotional want out of customer reviews", [K + "angles/desires.md"], "kb"),
    ("my ad account got restricted", [K + "media-buying/account-ops.md"], "kb"),
    ("where do I find trending products", [K + "research/product-research.md#sources"], "kb"),
    ("is the market too saturated for my product", [K + "research/validation.md#saturation"], "kb"),
    ("how do I analyze a top competitor's store", [K + "research/competitor-store-review.md#checklist-per-competitor",
                                                    K + "research/competitor-store-review.md#reviewing-winning-stores"], "kb"),
    ("steps to write a product mechanism", [K + "angles/mechanisms.md#workflow"], "kb"),
    ("what should the call to action at the end of a script do", [K + "creative/script-standards.md#9-cta"], "kb"),
    ("examples of winning ads aimed at unaware audiences", [K + "references/winning-ads.yaml#ads"], "kb"),
    ("an example listicle page to model", [K + "references/reference-pages.yaml#pages-4", K + "pages/landing-pages.md#gaps"], "kb"),
    ("should I split test two different prices", [K + "pages/offers.md#testing-offers", K + "pages/offers.md#pricing"], "kb"),
    ("what goes in the weekly performance review", [K + "media-buying/growth-review.md#weekly-growth-review",
                                                     K + "media-buying/growth-review.md#kpi-dictionary"], "kb"),
    ("tool to export Amazon reviews", [K + "references/tools.yaml#research"], "kb"),
    ("what's the maximum chargeback rate", [B + "chargebacks-max", "src:calls/2026-07-20"], "source"),
    ("Schwartz on the stages of market sophistication", ["src:books/schwartz", K + "foundations/sophistication-desire.md#sophistication-stages"], "source"),
    ("how many batches did Jordy need before his first winner", ["src:calls/2026-08-27", K + "research/validation.md"], "source"),
    ("what did the October 19 call say about targeting South America", ["src:calls/2026-10-19", K + "media-buying/testing.md"], "source"),
]
OFF_TOPIC_HELDOUT = ["how do I train a neural network", "what's the weather tomorrow",
                     "translate hello into Spanish"]
KB_KINDS = ["kb-section", "kb-entry", "kb-file"]


def hit_at(results, accept, k):
    return any(any(r["id"].startswith(a) for a in accept) for r in results[:k])


def run(store, embed_fn, cases=None, off_topic=None, kind=None):
    cases = CASES if cases is None else cases
    off_topic = OFF_TOPIC if off_topic is None else off_topic
    h1 = h5 = 0
    misses = []
    for case in cases:
        q, accept = case[0], case[1]
        res = store.search(q, limit=8, embed_fn=embed_fn, kind=kind)
        h1 += hit_at(res, accept, 1)
        ok5 = hit_at(res, accept, 5)
        h5 += ok5
        if not ok5:
            misses.append((q, [r["id"] for r in res[:3]]))
    noise = sum(len(store.search(q, limit=8, embed_fn=embed_fn, kind=kind)) for q in off_topic)
    n = max(1, len(cases))
    return h1 / n, h5 / n, noise, misses


def heldout_report(store, emb, verbose=False):
    kb_cases = [c for c in HELDOUT if c[2] == "kb"]
    rows = [("held-out, keyword-only", run(store, None, HELDOUT, OFF_TOPIC_HELDOUT)),
            ("held-out, hybrid", run(store, emb, HELDOUT, OFF_TOPIC_HELDOUT)),
            ("held-out KB-only cases, hybrid, KB-only index", run(store, emb, kb_cases, OFF_TOPIC_HELDOUT, kind=KB_KINDS))]
    print(f"\nHELD-OUT: {len(HELDOUT)} queries ({len(kb_cases)} KB-only), {len(OFF_TOPIC_HELDOUT)} off-topic controls")
    for label, r in rows:
        print(f"{label:48s} hit@1 {r[0]:.2f}  hit@5 {r[1]:.2f}  off-topic results {r[2]}")
        if verbose:
            for q, got in r[3]:
                print(f"   MISS {q!r} -> {got}")
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sweep", action="store_true")
    ap.add_argument("-v", action="store_true", help="print misses")
    a = ap.parse_args()
    s = Store(DB_PATH)
    emb = functools.lru_cache(maxsize=None)(lambda q: tuple(embeddings.embed_query(q) or ()) or None)
    print(f"TUNE: {len(CASES)} queries, {len(OFF_TOPIC)} off-topic controls (settings were tuned on these)")
    r = run(s, None)
    print(f"keyword-only          hit@1 {r[0]:.2f}  hit@5 {r[1]:.2f}  off-topic results {r[2]}")
    floors = [0.60, 0.62, 0.64, 0.65, 0.66, 0.68, 0.70] if a.sweep else [s.SIM_FLOOR]
    for f in floors:
        s.SIM_FLOOR = f
        r = run(s, emb)
        print(f"hybrid floor {f:.2f}     hit@1 {r[0]:.2f}  hit@5 {r[1]:.2f}  off-topic results {r[2]}")
        if a.v:
            for q, got in r[3]:
                print(f"   MISS {q!r} -> {got}")
    s.SIM_FLOOR = Store.SIM_FLOOR
    heldout_report(s, emb, verbose=a.v)


if __name__ == "__main__":
    main()
