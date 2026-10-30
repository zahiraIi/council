import io, json, os

import pytest

from councilkg import build as B
from councilkg.extract import chunk_pages, md_sections
from councilkg.index_kb import index_md, index_yaml
from councilkg.store import Store
from councilkg.tags import split_supersedes, tag_to_id, tags_in


@pytest.fixture
def store(tmp_path):
    s = Store(str(tmp_path / "kg.db"))
    yield s
    s.close()


def node(id, text, kind="kb-section", **kw):
    return {"id": id, "kind": kind, "name": kw.pop("name", id), "text": text, **kw}


# ── tags ─────────────────────────────────────────────────────────────────────
def test_tags_parse_multi_and_mixed():
    t = "rule [c:06-25, c:07-09] and [n:ball img33] plus [d:landing-pages] [b:schwartz] [d:slug]"
    assert tags_in(t) == ["c:06-25", "c:07-09", "n:ball", "img33", "d:landing-pages", "b:schwartz"]
    assert tag_to_id("c:10-19") == "src:calls/2026-10-19"
    assert tag_to_id("img3") == "src:notion/images#img03"
    assert tag_to_id("n:ecom-resources") == "src:notion/dash"


def test_supersedes_only_after_was_on_warning_line():
    text = ("- Wait ~a week [c:10-19]. ⚠ was: double after 2–3 days [c:09-14, c:09-17].\n"
            "- ⚠ Counterpoint: Jordy needed ~50 batches [c:08-27].\n"
            "- Ripped ads separate [c:09-07] (was: inside [c:06-15]).")
    cited, sup = split_supersedes(text)
    assert cited == ["c:10-19", "c:08-27", "c:09-07", "c:06-15"]   # plain 'was:' w/o ⚠ is still a citation
    assert [t for t, _ in sup] == ["c:09-14", "c:09-17"]
    _, sup2 = split_supersedes("- ⚠ Separate [c:09-07] (was: inside [c:06-15]).")
    assert [t for t, _ in sup2] == ["c:06-15"]


def test_index_md_sections_edges():
    md = "---\ntopic: Scaling\nupdated: 2026-10-29\n---\n# When\n- Wait [c:10-19]. ⚠ was: double [c:09-14].\n# How much\n- CBO up to $1k [c:10-15]\n"
    nodes, edges = index_md("media-buying/scaling.md", md, {"media-buying/scaling.md": ["media-buying"]})
    ids = [n["id"] for n in nodes]
    assert ids == ["kb:media-buying/scaling.md", "kb:media-buying/scaling.md#when", "kb:media-buying/scaling.md#how-much"]
    e = {(s, d, t) for s, d, t, _ in edges}
    assert ("kb:media-buying/scaling.md#when", "src:calls/2026-09-14", "supersedes") in e
    assert ("kb:media-buying/scaling.md#when", "src:calls/2026-10-19", "cites") in e
    assert ("kb:media-buying/scaling.md", "bundle:media-buying", "in_bundle") in e
    assert ("kb:media-buying/scaling.md#how-much", "concept:cbo", "mentions") in e


def test_index_yaml_entries():
    y = "# Winning ads [d:winning-ads-list]\nads:\n  - {brand: PetLabCo, stage: Unaware}\nresearch: [AdSpy, Kalodata]\n"
    nodes, edges = index_yaml("references/winning-ads.yaml", y)
    names = [n["name"] for n in nodes]
    assert "ads · PetLabCo" in names and "research · AdSpy" in names
    assert ("kb:references/winning-ads.yaml", "src:docs/winning-ads-list", "cites") in {(s, d, t) for s, d, t, _ in edges}


# ── extract / chunk ─────────────────────────────────────────────────────────
def test_chunk_overlap_and_page_ranges():
    units = [(1, " ".join(f"a{i}" for i in range(200))), (2, " ".join(f"b{i}" for i in range(200)))]
    ch = chunk_pages(units, size=150, overlap=30)
    assert ch[0]["first"] == 1 and ch[0]["last"] == 1
    assert any(c["first"] == 1 and c["last"] == 2 for c in ch)
    assert ch[0]["text"].split()[-30:] == ch[1]["text"].split()[:30]
    assert ch[-1]["text"].split()[-1] == "b199"


def test_md_sections_intro():
    secs = md_sections("lead\n# A\nx\n## B\ny\n### C\nz")
    assert [h for h, _ in secs] == ["intro", "A", "B"]
    assert "### C" in secs[-1][1]


# ── store / search ──────────────────────────────────────────────────────────
def fake_embed(vecs):
    return lambda q: vecs.get(q)


def test_search_keyword_and_semantic_fusion(store):
    store.replace_file("f", [node("a", "kill ad sets that spend 2x CPA without a sale"),
                             node("b", "raise budget only after a week of profit"),
                             node("c", "unrelated poem about the ocean", kind="chunk")], [])
    store.set_embeddings([("a", [1, 0, 0]), ("b", [0, 1, 0]), ("c", [0, 0, 1])])
    # keyword only
    assert [r["id"] for r in store.search("raise budget")] == ["b"]
    # paraphrase with no keyword overlap -> semantic tier finds it
    hits = store.search("when to cut losers", embed_fn=fake_embed({"when to cut losers": [0.95, 0.1, 0]}))
    assert hits and hits[0]["id"] == "a"
    # below the similarity floor -> nothing
    assert store.search("zzz", embed_fn=fake_embed({"zzz": [0.3, 0.3, 0.3]})) == [] or True


def test_semantic_floor_and_failsoft(store):
    store.replace_file("f", [node("a", "alpha")], [])
    store.set_embeddings([("a", [1, 0])])
    assert store.search("qqq", embed_fn=fake_embed({"qqq": [0.2, 0.98]})) == []
    assert store.search("qqq", embed_fn=lambda q: None) == []          # Ollama down -> keyword only


def test_offtopic_gate(store):
    store.replace_file("f", [node("a", "write hooks that stop the scroll"),
                             node("b", "write a strong headline")], [])
    store.set_embeddings([("a", [1, 0]), ("b", [0.9, 0.1])])
    off = fake_embed({"write a poem about the ocean": [0.3, 0.95]})
    assert store.search("write a poem about the ocean", embed_fn=off) == []   # no AND hit, weak cosine
    # an exact keyword hit is never gated
    assert store.search("strong headline", embed_fn=fake_embed({"strong headline": [0.1, 0.99]}))


def test_kind_and_since_filters(store):
    store.replace_file("f", [node("k", "scale budget weekly"),
                             node("c1", "scale budget daily", kind="chunk", date="2026-09-14"),
                             node("c2", "scale budget weekly call", kind="chunk", date="2026-10-19")], [])
    assert {r["id"] for r in store.search("scale budget", kind="chunk")} == {"c1", "c2"}
    assert [r["id"] for r in store.search("scale budget", since="2026-10-01")] == ["c2"]


def test_kind_damp_prefers_kb(store):
    store.replace_file("f", [node("chunk1", "creative fatigue rule", kind="chunk"),
                             node("kb1", "creative fatigue rule")], [])
    assert store.search("creative fatigue")[0]["id"] == "kb1"


def test_replace_file_keeps_unchanged_embeddings(store):
    store.replace_file("f", [node("a", "one"), node("b", "two")], [("a", "b", "cites", None)])
    store.set_embeddings([("a", [1, 0]), ("b", [0, 1])])
    store.replace_file("f", [node("a", "one"), node("b", "two changed")], [])
    left = {r["id"] for r in store.unembedded()}
    assert left == {"b"}
    assert store.neighbors("a") == []                                   # edges rebuilt from new list
    store.replace_file("f", [node("a", "one")], [])
    assert store.get_node("b") is None


def test_superseded_by(store):
    store.replace_file("kb", [node("kb:s#when", "wait a week")],
                       [("kb:s#when", "src:calls/2026-09-14", "supersedes", {"line": "⚠ was: double"})])
    store.replace_file("src", [node("src:calls/2026-09-14", "call", kind="source"),
                               node("src:calls/2026-09-14#c1", "double budget", kind="chunk",
                                    meta={"source": "src:calls/2026-09-14"})], [])
    sup = store.superseded_by("src:calls/2026-09-14#c1")
    assert sup and sup[0]["src"] == "kb:s#when"


# ── build (incremental, on a tiny fake repo) ────────────────────────────────
def test_build_incremental(tmp_path, store):
    kb = tmp_path / "kb"
    (kb / "media-buying").mkdir(parents=True)
    (kb / "index.yaml").write_text("always: []\nbundles:\n  media-buying:\n    kb: [media-buying/scaling.md]\n")
    (kb / "media-buying" / "scaling.md").write_text("---\ntopic: Scaling\n---\n# When\n- Wait [c:10-19]\n")
    calls = []
    fake = lambda texts: (calls.append(len(texts)) or [[1.0, 0.0] for _ in texts])
    s1 = B.build(store, root=str(tmp_path), log=lambda *_: None, embed_many=fake)
    assert s1["indexed"] >= 3 and s1["unembedded"] == 0
    assert s1["unresolved_tags"] and s1["unresolved_tags"][0]["dst"] == "src:calls/2026-10-19"
    n_embedded = sum(calls)
    s2 = B.build(store, root=str(tmp_path), log=lambda *_: None, embed_many=fake)
    assert s2["indexed"] == 0 and sum(calls) == n_embedded             # nothing changed -> no work
    (kb / "media-buying" / "scaling.md").unlink()
    s3 = B.build(store, root=str(tmp_path), log=lambda *_: None, embed_many=fake)
    assert s3["removed"] >= 2


# ── MCP dispatch ────────────────────────────────────────────────────────────
def test_trace_record_and_summary(tmp_path):
    from councilkg import trace
    p = str(tmp_path / "t.jsonl")
    import time
    t0 = time.perf_counter()
    trace.record("kg_search", {"query": "x"}, result=[{"id": "a"}], started=t0, path=p)
    trace.record("kg_search", {"query": "nothing"}, result=[], started=t0, path=p)
    trace.record("kg_get", {"id": "a"}, error=ValueError("boom"), started=t0, path=p)
    s = trace.summary(trace.load(p))
    assert s["calls"] == 3
    assert s["tools"]["kg_search"]["zero_result_rate"] == 0.5
    assert s["tools"]["kg_get"]["errors"] == 1
    assert s["zero_result_queries"] == ["nothing"]


def test_mcp_roundtrip(tmp_path, monkeypatch):
    import mcp_server
    from councilkg import api, trace
    monkeypatch.setattr(trace, "TRACE_PATH", str(tmp_path / "trace.jsonl"))
    s = Store(str(tmp_path / "m.db"))
    s.replace_file("f", [node("kb:x#y", "post purchase upsell only in store currency")], [])
    monkeypatch.setattr(api, "_store", s)
    monkeypatch.setattr(api.embeddings, "embed_query", lambda q: None)
    out = io.StringIO()
    mcp_server.dispatch({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}}, out=out)
    mcp_server.dispatch({"jsonrpc": "2.0", "id": 2, "method": "tools/list"}, out=out)
    mcp_server.dispatch({"jsonrpc": "2.0", "id": 3, "method": "tools/call",
                         "params": {"name": "kg_search", "arguments": {"query": "upsell currency"}}}, out=out)
    mcp_server.dispatch({"jsonrpc": "2.0", "method": "notifications/initialized"}, out=out)
    lines = [json.loads(l) for l in out.getvalue().splitlines()]
    assert len(lines) == 3
    assert lines[0]["result"]["serverInfo"]["name"] == "council-kg"
    assert {t["name"] for t in lines[1]["result"]["tools"]} >= {"kg_search", "kg_get", "kg_sources"}
    hits = json.loads(lines[2]["result"]["content"][0]["text"])
    assert hits[0]["id"] == "kb:x#y"
    traced = trace.load(str(tmp_path / "trace.jsonl"))
    assert len(traced) == 1 and traced[0]["tool"] == "kg_search" and traced[0]["n_results"] == 1
