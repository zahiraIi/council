"""kb/*.md -> kb-file + kb-section nodes; kb/references/*.yaml -> kb-entry nodes.
Edges: part_of (section->file), in_bundle (file->bundle), cites / supersedes
(section->source, from tags), mentions (section->concept)."""
import re

import yaml

from . import concepts
from .extract import md_sections
from .tags import split_supersedes, tag_to_id, tags_in


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", (s or "").lower()).strip("-") or "section"


def bundles_by_file(index):
    """kb-relative path -> [bundle names] from kb/index.yaml."""
    out = {}
    for name, b in (index.get("bundles") or {}).items():
        for f in b.get("kb") or []:
            out.setdefault(f, []).append(name)
    for f in index.get("always") or []:
        out.setdefault(f, []).append("always")
    return out


def bundle_nodes(index):
    return [{"id": f"bundle:{name}", "kind": "bundle", "name": f"bundle {name}",
             "text": f"Task bundle '{name}': kb {', '.join(b.get('kb') or [])}; state {', '.join(b.get('state') or [])}",
             "meta": {"kb": b.get("kb") or [], "state": b.get("state") or []}}
            for name, b in (index.get("bundles") or {}).items()]


def _source_edges(nid, text):
    cited, superseded = split_supersedes(text)
    edges = [(nid, tag_to_id(t), "cites", {"tag": t}) for t in cited if tag_to_id(t)]
    edges += [(nid, tag_to_id(t), "supersedes", {"tag": t, "line": line})
              for t, line in superseded if tag_to_id(t)]
    edges += [(nid, c, "mentions", None) for c in concepts.mentions(text)]
    return edges


def _frontmatter(text):
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            try:
                return yaml.safe_load(text[3:end]) or {}, text[end + 4:]
            except yaml.YAMLError:
                pass
    return {}, text


def index_md(rel, text, bundles):
    """rel is kb-relative ('media-buying/scaling.md'). Returns (nodes, edges)."""
    fm, body = _frontmatter(text)
    topic = fm.get("topic") or rel
    fid = f"kb:{rel}"
    fbundles = bundles.get(rel, [])
    nodes = [{"id": fid, "kind": "kb-file", "name": topic, "date": str(fm.get("updated") or "") or None,
              "text": f"{topic}. Load when: {fm.get('load_when') or ''}",
              "meta": {"path": f"kb/{rel}", "bundles": fbundles}}]
    edges = [(fid, f"bundle:{b}", "in_bundle", None) for b in fbundles if b != "always"]
    seen = {}
    context = f"\n(From: {topic}. Use when: {fm.get('load_when') or ''})"
    for heading, sec in md_sections(body):
        s = slug(re.sub(r"\[[^\]]*\]|\([^)]*\)", "", heading))      # ids without tags/asides
        seen[s] = seen.get(s, 0) + 1
        nid = f"{fid}#{s}" + (f"-{seen[s]}" if seen[s] > 1 else "")
        # the file's topic/load_when travel with each section: short sections ("# When")
        # otherwise embed with almost no meaning
        nodes.append({"id": nid, "kind": "kb-section", "name": f"{topic}: {heading}",
                      "text": sec + context, "date": None,
                      "meta": {"path": f"kb/{rel}", "heading": heading, "bundles": fbundles,
                               "tags": tags_in(sec)}})
        edges.append((nid, fid, "part_of", None))
        edges += _source_edges(nid, sec)
    return nodes, edges


_NAME_KEYS = ("brand", "name", "title", "stage", "type")


def index_yaml(rel, text):
    data = yaml.safe_load(text) or {}
    fid = f"kb:{rel}"
    head = " ".join(l.lstrip("# ") for l in text.splitlines() if l.startswith("#"))
    nodes = [{"id": fid, "kind": "kb-file", "name": rel, "text": head,
              "meta": {"path": f"kb/{rel}", "tags": tags_in(head)}}]
    edges = [(fid, tag_to_id(t), "cites", {"tag": t}) for t in tags_in(head) if tag_to_id(t)]
    for key, items in data.items():
        if not isinstance(items, list):
            continue
        for i, it in enumerate(items, start=1):
            if isinstance(it, dict):
                label = next((str(it[k]) for k in _NAME_KEYS if it.get(k)), f"{key} {i}")
                body = "; ".join(f"{k}: {v}" for k, v in it.items() if v not in ("", None))
            else:
                label, body = str(it)[:60], str(it)
            nid = f"{fid}#{key}-{i}"
            nodes.append({"id": nid, "kind": "kb-entry", "name": f"{key} · {label}",
                          "text": f"{key}: {body}", "meta": {"path": f"kb/{rel}", "list": key}})
            edges.append((nid, fid, "part_of", None))
            edges += _source_edges(nid, body)
    return nodes, edges
