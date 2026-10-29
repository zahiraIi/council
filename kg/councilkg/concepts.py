"""Concept vocabulary: the frameworks and metrics the KB reasons with. Each concept
becomes a node, and any section/chunk that names it (or an alias) gets a `mentions`
edge, so kg_neighbors(concept) lists everywhere it's discussed."""
import re

# name: aliases (matched case-insensitively on word boundaries)
CONCEPTS = {
    "Unaware": ["unaware"],
    "Problem Aware": ["problem aware", "problem-aware"],
    "Solution Aware": ["solution aware", "solution-aware"],
    "Product Aware": ["product aware", "product-aware"],
    "Most Aware": ["most aware", "most-aware"],
    "Market awareness": ["market awareness", "awareness level", "awareness stage"],
    "Market sophistication": ["sophistication"],
    "Mass desire": ["mass desire", "core desire"],
    "Avatar": ["avatar", "sub-avatar", "sub avatar"],
    "Angle": ["angle", "angles"],
    "Mechanism": ["mechanism", "unique mechanism"],
    "Belief shift": ["belief shift"],
    "Hook": ["hook", "hooks", "hook rate"],
    "Hold rate": ["hold rate"],
    "Script": ["script", "scripts"],
    "B-roll + voiceover": ["b-roll", "broll", "voiceover"],
    "UGC": ["ugc", "ai ugc"],
    "Static / image ad": ["static", "statics", "image ad", "native image"],
    "Ripped ad": ["ripped ad", "ripped ads", "ripped"],
    "Primary text / headline": ["primary text", "headline", "headlines"],
    "Advertorial": ["advertorial", "advertorials"],
    "Listicle": ["listicle", "listicles"],
    "PDP": ["pdp", "product page", "product detail page"],
    "Pre-lander": ["pre-lander", "prelander", "pre-landers"],
    "Offer": ["offer", "offers", "bundle", "bogo"],
    "Upsell / AOV": ["upsell", "post-purchase", "aov", "average order value"],
    "Subscription": ["subscription", "subscriptions", "churn"],
    "Guarantee": ["guarantee", "money-back"],
    "CBO": ["cbo"],
    "ABO": ["abo"],
    "Batch testing": ["batch", "batches", "3x3", "3×3"],
    "Scaling": ["scale", "scaling", "raise budget", "budget increase"],
    "Descaling / killing": ["descale", "kill", "cut", "turn off"],
    "ROAS / break-even": ["roas", "beroas", "break-even", "breakeven"],
    "CPA": ["cpa", "cost per purchase"],
    "CTR / CPC": ["ctr", "cpc", "cpm"],
    "CVR": ["cvr", "conversion rate"],
    "Creative fatigue": ["fatigue", "fatigued"],
    "Black Friday / Q4": ["black friday", "bfcm", "q4", "holiday"],
    "Email / retention": ["email", "klaviyo", "retention", "flows"],
    "Product research": ["product research", "winning product"],
    "Validation / TAM": ["validation", "validate", "tam"],
    "Competitor research": ["competitor", "competitors", "ad library", "spy"],
    "Store audit": ["store audit", "audit"],
    "Account ops": ["ad account", "business manager", "pixel", "payment"],
}


def concept_id(name):
    return "concept:" + re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


_PATTERNS = [(concept_id(n), re.compile(r"(?<![\w-])(" + "|".join(re.escape(a) for a in al) + r")(?![\w-])", re.I))
             for n, al in CONCEPTS.items()]


def mentions(text):
    """Concept ids named in `text`."""
    return [cid for cid, pat in _PATTERNS if pat.search(text or "")]


def nodes():
    return [{"id": concept_id(n), "kind": "concept", "name": n,
             "text": f"{n} (also: {', '.join(al)})", "meta": {"aliases": al}}
            for n, al in CONCEPTS.items()]


def fingerprint():
    import hashlib, json
    return hashlib.sha256(json.dumps(CONCEPTS, sort_keys=True).encode()).hexdigest()
