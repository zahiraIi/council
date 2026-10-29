"""_sources files -> one `source` node + ~350-token `chunk` nodes each.
Ids line up with tags.tag_to_id so KB citations resolve to them."""
import os, re

from . import concepts
from .extract import chunk_pages, md_sections, pages

SKIP_DIRS = {"images"}
SKIP_FILES = {"README.md"}
TEXT_EXT = {"pdf", "docx", "pptx", "md"}
IMAGE_EXT = {"png", "jpg", "jpeg"}           # source node only, so citations resolve; no text


def describe(rel):
    """_sources-relative path -> (source id, tags, date, type, title), or None to skip."""
    parts = rel.split("/")
    base = parts[-1].rsplit(".", 1)[0]
    if parts[0] == "calls":
        m = re.match(r"(2026-(\d\d-\d\d))-?(.*)", base)
        if not m:
            return None
        date, mmdd, rest = m.groups()
        if rest.startswith("guest-"):
            title = f"Guest speaker call {date} ({rest[6:].title()})"
        else:
            title = f"Coaching call {date}" + (f" ({rest.replace('-', ' ')})" if rest and rest != "call" else "")
        return f"src:calls/{date}", [f"c:{mmdd}"], date, "call", title
    if parts[0] == "docs":
        return f"src:docs/{base}", [f"d:{base}"], None, "doc", f"Course doc: {base.replace('-', ' ')}"
    if parts[0] == "books":
        key = "schwartz" if "schwartz" in base else base
        return f"src:books/{key}", [f"b:{key}"], None, "book", "Breakthrough Advertising (Eugene Schwartz)"
    if parts[0] == "notion":
        return {
            "ecom-ball-knowledge": ("src:notion/ball", ["n:ball"], None, "notion", "Notion: ECOM BALL KNOWLEDGE (owner notes)"),
            "dashboard-pages": ("src:notion/dash", ["n:dash", "n:ecom-resources"], None, "notion",
                                "Notion: dashboard pages + ECOM Resources"),
            "images-transcribed": ("src:notion/images", ["n:ball-img"], None, "notion",
                                   "Notion: ECOM BALL KNOWLEDGE image transcriptions"),
        }.get(base)
    return None


def walk(sources_dir):
    for root, dirs, files in os.walk(sources_dir):
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS)
        for f in sorted(files):
            if f in SKIP_FILES or f.rsplit(".", 1)[-1].lower() not in TEXT_EXT | IMAGE_EXT:
                continue
            yield os.path.relpath(os.path.join(root, f), sources_dir)


def _chunk(src, title, date, tags, i, text, first, last):
    pages_ = f"p{first}" if first == last else f"p{first}-{last}"
    if isinstance(first, str):                       # markdown: label is a heading
        pages_ = first if first == last else f"{first} … {last}"
    return {"id": f"{src}#c{i}", "kind": "chunk", "name": f"{title} [{pages_}]", "text": text,
            "date": date, "meta": {"source": src, "tags": tags, "pages": [first, last]}}


def index_source(sources_dir, rel):
    d = describe(rel)
    if not d:
        return [], []
    src, tags, date, typ, title = d
    path = os.path.join(sources_dir, rel)
    if typ == "notion" and src == "src:notion/images":
        return _index_images(path, src, title, tags)
    if rel.rsplit(".", 1)[-1].lower() in IMAGE_EXT:
        return [{"id": src, "kind": "source", "name": title + " (image)", "date": date,
                 "text": f"{title}: image file, no extractable text; see the KB sections citing it.",
                 "meta": {"path": f"_sources/{rel}", "type": "image", "tags": tags, "chunks": 0}}], []
    units = pages(path)
    chunks = chunk_pages(units)
    lead = " ".join(" ".join(t for _, t in units).split()[:120])
    nodes = [{"id": src, "kind": "source", "name": title, "text": lead, "date": date,
              "meta": {"path": f"_sources/{rel}", "type": typ, "tags": tags, "chunks": len(chunks)}}]
    edges = []
    for i, c in enumerate(chunks, start=1):
        n = _chunk(src, title, date, tags, i, c["text"], c["first"], c["last"])
        nodes.append(n)
        edges.append((n["id"], src, "part_of", None))
        edges += [(n["id"], cid, "mentions", None) for cid in concepts.mentions(c["text"])]
    return nodes, edges


def _index_images(path, src, title, tags):
    """One chunk per transcribed image ('## 33 page-type-matrix'), id ...#img33, so
    KB tags like [img33] resolve straight to the transcription."""
    with open(path, encoding="utf-8") as f:
        secs = md_sections(f.read())
    nodes = [{"id": src, "kind": "source", "name": title, "text": title,
              "meta": {"path": f"_sources/notion/{os.path.basename(path)}", "type": "notion", "tags": tags}}]
    edges = []
    for heading, body in secs:
        m = re.match(r"(\d+)\s*(.*)", heading)
        if not m:
            continue
        nid = f"{src}#img{int(m.group(1)):02d}"
        nodes.append({"id": nid, "kind": "chunk", "name": f"Notion image {m.group(1)}: {m.group(2)}",
                      "text": body, "meta": {"source": src, "tags": tags + [f"img{int(m.group(1))}"]}})
        edges.append((nid, src, "part_of", None))
        edges += [(nid, cid, "mentions", None) for cid in concepts.mentions(body)]
    return nodes, edges
