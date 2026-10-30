"""Incremental build: index changed files (sha256 fingerprints), drop deleted ones,
then embed any node without a vector."""
import hashlib, os

import yaml

from . import REPO_ROOT, concepts, embeddings
from .index_kb import bundle_nodes, bundles_by_file, index_md, index_yaml
from .index_sources import index_source, walk
from .store import Store

EMBED_BATCH = 32
INDEX_VERSION = "3"     # bump when indexing logic changes so every file is rebuilt


def _sha(*paths):
    h = hashlib.sha256(INDEX_VERSION.encode())
    for p in paths:
        with open(p, "rb") as f:
            h.update(f.read())
    return h.hexdigest()


def build(store: Store, root=REPO_ROOT, force=False, embed=True, log=print, embed_many=None):
    kb_dir, src_dir = os.path.join(root, "kb"), os.path.join(root, "_sources")
    index_path = os.path.join(kb_dir, "index.yaml")
    with open(index_path, encoding="utf-8") as f:
        index = yaml.safe_load(f) or {}
    bundles = bundles_by_file(index)
    stats = {"indexed": 0, "skipped": 0, "removed": 0}
    seen = set()

    def update(key, fp, make):
        seen.add(key)
        if not force and store.file_fingerprint(key) == fp:
            stats["skipped"] += 1
            return
        nodes, edges = make()
        store.replace_file(key, nodes, edges)
        store.set_file_fingerprint(key, fp)
        stats["indexed"] += 1
        log(f"  indexed {key}: {len(nodes)} nodes")

    update("@concepts", concepts.fingerprint(), lambda: (concepts.nodes(), []))
    update("@bundles", _sha(index_path), lambda: (bundle_nodes(index), []))

    for dirpath, dirs, files in os.walk(kb_dir):
        dirs.sort()
        for f in sorted(files):
            full = os.path.join(dirpath, f)
            rel = os.path.relpath(full, kb_dir)
            if f == "index.yaml":
                continue
            with open(full, encoding="utf-8") as fh:
                text = fh.read()
            if f.endswith(".md"):
                # bundle membership lives in index.yaml, so it's part of the fingerprint
                update(f"kb/{rel}", _sha(full, index_path), lambda: index_md(rel, text, bundles))
            elif f.endswith((".yaml", ".yml")):
                update(f"kb/{rel}", _sha(full), lambda: index_yaml(rel, text))

    if os.path.isdir(src_dir):
        calls = []
        for rel in walk(src_dir):
            full = os.path.join(src_dir, rel)
            update(f"_sources/{rel}", _sha(full), lambda: index_source(src_dir, rel))
            if rel.startswith("calls/"):
                calls.append(rel)
        _link_calls(store, src_dir, calls)
    else:
        log("  _sources/ not found: indexing kb/ only")

    for key in set(store.file_paths()) - seen:
        stats["removed"] += store.drop_file(key)
        log(f"  removed {key}")

    if embed:
        stats.update(embed_pending(store, log=log, embed_many=embed_many))
    stats["unresolved_tags"] = unresolved(store)
    return stats


def _link_calls(store, src_dir, calls):
    """`follows` edges between consecutive calls (chronology for 'latest wins')."""
    from .index_sources import describe
    ids = sorted(describe(r)[0] for r in calls if describe(r))
    for prev, cur in zip(ids, ids[1:]):
        store.add_edge(cur, prev, "follows", None)


def embed_pending(store, log=print, embed_many=None):
    fn = embed_many or embeddings.embed_many
    todo = store.unembedded()
    done = 0
    for i in range(0, len(todo), EMBED_BATCH):
        batch = todo[i:i + EMBED_BATCH]
        vecs = fn([f"{r['name']}\n{r['text']}" for r in batch])
        if vecs is None:
            log(f"  embeddings unavailable (is Ollama running?): {len(todo) - done} nodes left unembedded; "
                "search falls back to keywords")
            break
        store.set_embeddings([(r["id"], v) for r, v in zip(batch, vecs)])
        done += len(batch)
        if done % (EMBED_BATCH * 10) == 0:
            log(f"  embedded {done}/{len(todo)}")
    return {"embedded_now": done, "unembedded": len(todo) - done}


def unresolved(store):
    """Citation edges whose target node doesn't exist (a KB tag with no source)."""
    return [dict(r) for r in store.db.execute(
        "SELECT e.src, e.dst, e.type FROM edges e LEFT JOIN nodes n ON n.id=e.dst"
        " WHERE n.id IS NULL AND e.type IN ('cites','supersedes')")]
