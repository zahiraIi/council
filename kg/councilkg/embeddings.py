"""Ollama embeddings (nomic-embed-text). Same fail-soft contract as ATLAS
atlas/embeddings.py: any failure returns None, never raises."""
import json, os, urllib.request

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
EMBED_MODEL = os.getenv("KG_EMBED_MODEL", "nomic-embed-text")
MAX_CHARS = 6000            # nomic-embed-text context is 2048 tokens (~8k chars); leave headroom

# nomic-embed-text is trained with task prefixes; documents and queries embed differently.
DOC_PREFIX = "search_document: "
QUERY_PREFIX = "search_query: "


def _http_post(url, data):
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read().decode())


def embed_many(texts, prefix=DOC_PREFIX, http=None):
    """list[str] -> list[vector] of the same length, or None on any failure.
    Empty texts are not allowed by the caller (filter first)."""
    if not texts:
        return []
    payload = json.dumps({"model": EMBED_MODEL,
                          "input": [prefix + t[:MAX_CHARS] for t in texts]}).encode()
    try:
        resp = (http or _http_post)(f"{OLLAMA_HOST}/api/embed", payload)
        vecs = resp.get("embeddings")
        return vecs if vecs and len(vecs) == len(texts) else None
    except Exception:
        return None


def embed_query(text, http=None):
    """One query vector, or None (empty text, Ollama down, timeout, bad response)."""
    if not (text or "").strip():
        return None
    vecs = embed_many([text], prefix=QUERY_PREFIX, http=http)
    return vecs[0] if vecs else None
