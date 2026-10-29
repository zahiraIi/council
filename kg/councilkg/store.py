"""SQLite + FTS5 graph store with hybrid search. Ported from ATLAS atlas/store.py:
same tiers (exact AND, quorum OR, semantic cosine) fused by weighted reciprocal rank,
plus kind/date filters and a per-file fingerprint table for incremental builds."""
import json, sqlite3, time

import numpy as np

SCHEMA = """
CREATE TABLE IF NOT EXISTS nodes(
  id TEXT PRIMARY KEY, kind TEXT, file TEXT, name TEXT, text TEXT,
  date TEXT, meta TEXT, embedding BLOB);
CREATE TABLE IF NOT EXISTS edges(
  src TEXT, dst TEXT, type TEXT, meta TEXT, PRIMARY KEY(src,dst,type));
CREATE TABLE IF NOT EXISTS files(path TEXT PRIMARY KEY, fingerprint TEXT);
CREATE INDEX IF NOT EXISTS nodes_file ON nodes(file);
CREATE INDEX IF NOT EXISTS edges_dst ON edges(dst);
CREATE VIRTUAL TABLE IF NOT EXISTS nodes_fts USING fts5(
  id UNINDEXED, name, text, tokenize='porter unicode61');
"""


class Store:
    # Search tuning, from scripts/eval_search.py (31 known-item queries, 2026-10-29):
    # ATLAS defaults (3,1,1)/floor 0.60 gave hit@5 0.74; semantic-heavier (2,0.5,2) with
    # chunks damped 0.4 and floor 0.62 gives hit@5 0.90, hit@1 0.61. nomic scores are
    # compressed: on-topic tops ~0.64-0.76, off-topic ~0.52-0.64.
    RRF_K = 60
    POOL = 50
    SIM_FLOOR = 0.62
    # With embeddings on and no exact-AND hit, a query whose best cosine is under GATE is
    # treated as off-topic and returns nothing (keyword OR alone is too noisy to trust).
    GATE = 0.62
    WEIGHTS = (2.0, 0.5, 2.0)          # (exact AND, quorum OR, semantic)
    QUORUM_CAP = 2
    # Curated KB rules outrank raw source text and bare concept/structure nodes.
    KIND_DAMP = {"chunk": 0.4, "concept": 0.5, "kb-file": 0.5, "source": 0.5, "bundle": 0.3}
    EMB_TTL = 600

    _STOPWORDS = {
        "a", "an", "and", "are", "as", "at", "be", "by", "can", "do", "does", "for", "from",
        "how", "i", "if", "in", "into", "is", "it", "its", "many", "my", "of", "on", "or",
        "should", "that", "the", "there", "this", "to", "was", "we", "were", "what", "when",
        "where", "which", "who", "why", "will", "with", "you", "your",
    }

    def __init__(self, path):
        self.db = sqlite3.connect(path, timeout=60)
        self.db.row_factory = sqlite3.Row
        self.db.execute("PRAGMA busy_timeout=60000")
        self.db.execute("PRAGMA journal_mode=WAL")
        self.db.executescript(SCHEMA)

    # ── rows ─────────────────────────────────────────────────────────────────
    @staticmethod
    def _row(r):
        d = dict(r)
        d["meta"] = json.loads(d.get("meta") or "{}")
        d.pop("embedding", None)
        return d

    @staticmethod
    def vec_to_blob(vec):
        return None if vec is None else np.asarray(vec, dtype="float32").tobytes()

    def upsert_node(self, node):
        with self.db:
            self.db.execute(
                "INSERT INTO nodes(id,kind,file,name,text,date,meta,embedding) VALUES(?,?,?,?,?,?,?,NULL)"
                " ON CONFLICT(id) DO UPDATE SET kind=excluded.kind,file=excluded.file,name=excluded.name,"
                "text=excluded.text,date=excluded.date,meta=excluded.meta,"
                # keep the embedding only if the text didn't change
                "embedding=CASE WHEN nodes.text IS excluded.text AND nodes.name IS excluded.name"
                " THEN nodes.embedding ELSE NULL END",
                (node["id"], node["kind"], node.get("file"), node.get("name") or "",
                 node.get("text") or "", node.get("date"), json.dumps(node.get("meta") or {})))
            self.db.execute("DELETE FROM nodes_fts WHERE id=?", (node["id"],))
            self.db.execute("INSERT INTO nodes_fts(id,name,text) VALUES(?,?,?)",
                            (node["id"], node.get("name") or "", node.get("text") or ""))

    def get_node(self, node_id):
        r = self.db.execute("SELECT * FROM nodes WHERE id=?", (node_id,)).fetchone()
        return self._row(r) if r else None

    def add_edge(self, src, dst, type_, meta=None):
        with self.db:
            self.db.execute("INSERT OR REPLACE INTO edges(src,dst,type,meta) VALUES(?,?,?,?)",
                            (src, dst, type_, json.dumps(meta or {})))

    def neighbors(self, node_id, etype=None):
        q = "SELECT * FROM edges WHERE (src=? OR dst=?)"
        args = [node_id, node_id]
        if etype:
            q += " AND type=?"
            args.append(etype)
        out = []
        for r in self.db.execute(q, args):
            e = dict(r)
            e["meta"] = json.loads(e["meta"] or "{}")
            out.append(e)
        return out

    # ── incremental build bookkeeping ───────────────────────────────────────
    def file_fingerprint(self, path):
        r = self.db.execute("SELECT fingerprint FROM files WHERE path=?", (path,)).fetchone()
        return r["fingerprint"] if r else None

    def set_file_fingerprint(self, path, fp):
        with self.db:
            self.db.execute("INSERT OR REPLACE INTO files(path,fingerprint) VALUES(?,?)", (path, fp))

    def replace_file(self, path, nodes, edges):
        """Swap in the nodes/edges built from one file. Nodes whose text is unchanged
        keep their embedding (upsert), so an edit to one section re-embeds only that
        section. Edges are owned by their src node and rebuilt wholesale."""
        old = {r[0] for r in self.db.execute("SELECT id FROM nodes WHERE file=?", (path,))}
        for n in nodes:
            self.upsert_node(dict(n, file=path))
        new = {n["id"] for n in nodes}
        with self.db:
            for nid in old | new:
                self.db.execute("DELETE FROM edges WHERE src=?", (nid,))
            for nid in old - new:
                self.db.execute("DELETE FROM nodes_fts WHERE id=?", (nid,))
                self.db.execute("DELETE FROM nodes WHERE id=?", (nid,))
        for src, dst, type_, meta in edges:
            self.add_edge(src, dst, type_, meta)
        return {"nodes": len(new), "removed": len(old - new)}

    def drop_file(self, path):
        """Remove a file that no longer exists: its nodes and their outgoing edges."""
        removed = self.replace_file(path, [], [])["removed"]
        with self.db:
            self.db.execute("DELETE FROM files WHERE path=?", (path,))
        return removed

    def file_paths(self):
        return [r[0] for r in self.db.execute("SELECT path FROM files")]

    def unembedded(self, limit=None):
        q = "SELECT id, name, text FROM nodes WHERE embedding IS NULL AND length(trim(text))>0"
        if limit:
            q += f" LIMIT {int(limit)}"
        return [dict(r) for r in self.db.execute(q)]

    def set_embeddings(self, pairs):
        with self.db:
            for nid, vec in pairs:
                self.db.execute("UPDATE nodes SET embedding=? WHERE id=?", (self.vec_to_blob(vec), nid))

    # ── search ───────────────────────────────────────────────────────────────
    @staticmethod
    def _fts_query(query, joiner=" "):
        """Quote each token as an FTS5 phrase so '-', ':' etc. are literal (ATLAS fix)."""
        tokens = [t for t in (query or "").split() if t]
        return joiner.join('"' + t.replace('"', '""') + '"' for t in tokens)

    def _filter_sql(self, kind, since):
        clauses, args = [], []
        if kind:
            kinds = [kind] if isinstance(kind, str) else list(kind)
            clauses.append(f"n.kind IN ({','.join('?' * len(kinds))})")
            args += kinds
        if since:
            clauses.append("n.date IS NOT NULL AND n.date >= ?")
            args.append(since)
        return (" AND " + " AND ".join(clauses)) if clauses else "", args

    def _fts_ids(self, match, k, kind=None, since=None):
        where, args = self._filter_sql(kind, since)
        return [r[0] for r in self.db.execute(
            "SELECT f.id FROM nodes_fts f JOIN nodes n ON n.id=f.id"
            f" WHERE nodes_fts MATCH ?{where} ORDER BY f.rank LIMIT ?", [match, *args, k])]

    def _quorum_or_ids(self, query, k, kind=None, since=None):
        tokens = [t for t in (query or "").split() if t and t.lower() not in self._STOPWORDS]
        if len(tokens) < 2:
            return []
        where, args = self._filter_sql(kind, since)
        rows = self.db.execute(
            "SELECT n.id, n.name, n.text FROM nodes_fts f JOIN nodes n ON n.id=f.id"
            f" WHERE nodes_fts MATCH ?{where} ORDER BY f.rank LIMIT ?",
            [self._fts_query(" ".join(tokens), joiner=" OR "), *args, max(k, 60)]).fetchall()
        # at least 2 words must match: a single shared word ("capital", "write") is noise
        needed = max(2, min(-(-len(tokens) // 2), self.QUORUM_CAP))
        import re
        # whole-word prefix match ("budget" matches "budgets"), never a bare substring:
        # 'c' must not match every text that contains the letter c
        pats = [re.compile(r"\b" + re.escape(t.lower())) for t in tokens]
        scored = []
        for i, r in enumerate(rows):
            text = f"{r['name'] or ''} {r['text'] or ''}".lower()
            overlap = sum(1 for p in pats if p.search(text))
            if overlap >= needed:
                scored.append((-overlap, i, r["id"]))
        scored.sort()
        return [nid for _, _, nid in scored[:k]]

    def _emb_matrix(self):
        n = self.db.execute("SELECT count(*) FROM nodes WHERE embedding IS NOT NULL").fetchone()[0]
        c = getattr(self, "_emb_cache", None)
        if c and c[0] == n and time.time() - c[1] < self.EMB_TTL:
            return c[2], c[3]
        rows = self.db.execute("SELECT id, embedding FROM nodes WHERE embedding IS NOT NULL").fetchall()
        if not rows:
            self._emb_cache = (n, time.time(), [], None)
            return [], None
        ids = [r["id"] for r in rows]
        m = np.stack([np.frombuffer(r["embedding"], dtype="float32") for r in rows])
        mn = m / (np.linalg.norm(m, axis=1, keepdims=True) + 1e-9)
        self._emb_cache = (n, time.time(), ids, mn)
        return ids, mn

    def semantic_scores(self, query, embed_fn):
        """[(id, cosine)] sorted descending, no floor applied. Empty if no embedder/vectors."""
        qvec = embed_fn(query) if embed_fn else None
        if qvec is None:
            return []
        ids, mn = self._emb_matrix()
        if not ids:
            return []
        qv = np.asarray(qvec, dtype="float32")
        if qv.shape[0] != mn.shape[1]:
            return []
        sims = mn @ (qv / (np.linalg.norm(qv) or 1.0))
        order = np.argsort(-sims)
        return [(ids[i], float(sims[i])) for i in order]

    def _semantic_ids(self, query, k, embed_fn, kind=None, since=None):
        """(ids above SIM_FLOOR, best cosine or None when no embedder/vectors)."""
        all_scored = self.semantic_scores(query, embed_fn)
        best = all_scored[0][1] if all_scored else None
        scored = [(nid, s) for nid, s in all_scored if s >= self.SIM_FLOOR]
        if not scored:
            return [], best
        if kind or since:
            where, args = self._filter_sql(kind, since)
            cand = [nid for nid, _ in scored[: k * 10]]
            ph = ",".join("?" * len(cand))
            ok = {r[0] for r in self.db.execute(
                f"SELECT n.id FROM nodes n WHERE n.id IN ({ph}){where}", [*cand, *args])}
            scored = [(nid, s) for nid, s in scored if nid in ok]
        return [nid for nid, _ in scored[:k]], best

    def search(self, query, limit=8, embed_fn=None, kind=None, since=None):
        """Hybrid search; degrades to keyword-only when embed_fn is None or returns None."""
        and_match = self._fts_query(query)
        if not and_match:
            return []
        exact = self._fts_ids(and_match, self.POOL, kind, since)
        sem, best = self._semantic_ids(query, self.POOL, embed_fn, kind, since)
        if not exact and best is not None and best < self.GATE:
            return []
        lists = (exact, self._quorum_or_ids(query, self.POOL, kind, since), sem)
        score = {}
        for w, ids in zip(self.WEIGHTS, lists):
            for rank, nid in enumerate(ids):
                score[nid] = score.get(nid, 0.0) + w / (self.RRF_K + rank + 1)
        if not score:
            return []
        ph = ",".join("?" * len(score))
        for r in self.db.execute(f"SELECT id, kind FROM nodes WHERE id IN ({ph})", list(score)):
            score[r["id"]] *= self.KIND_DAMP.get(r["kind"], 1.0)
        top = sorted(score, key=lambda nid: -score[nid])[: int(limit)]
        ph = ",".join("?" * len(top))
        by_id = {r["id"]: self._row(r) for r in
                 self.db.execute(f"SELECT * FROM nodes WHERE id IN ({ph})", top)}
        return [by_id[i] for i in top if i in by_id]

    # ── graph helpers used by the MCP layer ─────────────────────────────────
    def source_for_tag(self, tag):
        for r in self.db.execute("SELECT * FROM nodes WHERE kind='source'"):
            if tag in json.loads(r["meta"] or "{}").get("tags", []):
                return self._row(r)
        return None

    def superseded_by(self, node_id):
        """KB sections that mark this node's source as superseded advice (⚠ was:)."""
        node = self.get_node(node_id)
        if not node:
            return []
        src = node["meta"].get("source") or (node_id if node["kind"] == "source" else None)
        if not src:
            return []
        return [dict(src=r["src"], **json.loads(r["meta"] or "{}")) for r in self.db.execute(
            "SELECT src, meta FROM edges WHERE dst=? AND type='supersedes'", (src,))]

    def stat(self):
        return {
            "nodes": self.db.execute("SELECT count(*) FROM nodes").fetchone()[0],
            "edges": self.db.execute("SELECT count(*) FROM edges").fetchone()[0],
            "embedded": self.db.execute("SELECT count(*) FROM nodes WHERE embedding IS NOT NULL").fetchone()[0],
            "by_kind": {r[0]: r[1] for r in self.db.execute(
                "SELECT kind, count(*) FROM nodes GROUP BY kind ORDER BY 2 DESC")},
            "edges_by_type": {r[0]: r[1] for r in self.db.execute(
                "SELECT type, count(*) FROM edges GROUP BY type ORDER BY 2 DESC")},
        }

    def close(self):
        self.db.close()
