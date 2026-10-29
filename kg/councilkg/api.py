"""Tool implementations shared by the MCP server and the CLI."""
from . import DB_PATH, embeddings
from .store import Store

SEARCH_LIMIT = 8
SEARCH_CLIP = 320

_store = None


def store():
    global _store
    if _store is None:
        _store = Store(DB_PATH)
    return _store


def _clip(text, n):
    text = " ".join((text or "").split())
    return text if len(text) <= n else text[:n].rstrip() + "…"


def _hit(s, r):
    m = r.get("meta") or {}
    hit = {"id": r["id"], "kind": r["kind"], "name": r["name"], "text": _clip(r.get("text"), SEARCH_CLIP)}
    if r.get("date"):
        hit["date"] = r["date"]
    if m.get("tags"):
        hit["tags"] = m["tags"]
    if m.get("path"):
        hit["path"] = m["path"]
    sup = s.superseded_by(r["id"]) if r["kind"] in ("chunk", "source") else []
    if sup:
        hit["superseded_on"] = [{"by": x["src"], "kb_line": x.get("line")} for x in sup]
    return hit


def kg_search(query, kind=None, since=None, limit=SEARCH_LIMIT):
    s = store()
    rows = s.search(query, limit=int(limit), embed_fn=embeddings.embed_query, kind=kind or None,
                    since=since or None)
    return [_hit(s, r) for r in rows]


def kg_get(id):
    s = store()
    node = s.get_node(id)
    if node is None:
        return None
    edges = s.neighbors(id)
    node["edges"] = {
        "out": [{"type": e["type"], "to": e["dst"]} for e in edges if e["src"] == id][:40],
        "in": [{"type": e["type"], "from": e["src"]} for e in edges if e["dst"] == id][:40],
    }
    sup = s.superseded_by(id)
    if sup:
        node["superseded_on"] = sup
    return node


def kg_neighbors(id, type=None):
    s = store()
    out = []
    for e in s.neighbors(id, etype=type):
        other = e["dst"] if e["src"] == id else e["src"]
        n = s.get_node(other)
        out.append({"type": e["type"], "direction": "out" if e["src"] == id else "in", "id": other,
                    "name": n["name"] if n else None, "kind": n["kind"] if n else None,
                    **({"line": e["meta"]["line"]} if e["meta"].get("line") else {})})
    return out[:80]


def kg_sources(tag):
    """Resolve a KB tag like 'c:10-19' or 'd:landing-pages' to its source, chunks and citing KB sections."""
    from .tags import tag_to_id
    s = store()
    sid = tag_to_id(tag.strip("[] "))
    node = s.get_node(sid) if sid else None
    if node is None:
        return {"error": f"no source for tag {tag!r}"}
    edges = s.neighbors(sid)
    chunks = [e["src"] for e in edges if e["type"] == "part_of" and e["dst"] == sid]
    citing = sorted({e["src"] for e in edges if e["type"] in ("cites", "supersedes") and e["dst"] == sid})
    return {"source": {k: node[k] for k in ("id", "name", "date") if node.get(k)} | {"path": node["meta"].get("path")},
            "chunks": [{"id": c, "name": (s.get_node(c) or {}).get("name")} for c in chunks],
            "cited_by": citing,
            "superseded_on": s.superseded_by(sid)}


def kg_stat():
    return store().stat()
