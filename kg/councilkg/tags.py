"""KB source tags ([c:10-19], [d:offers-that-convert], [b:schwartz], [n:ball img33] …)
and the ⚠ was: convention, mapped to graph source ids."""
import re

_BRACKET = re.compile(r"\[([^\[\]]*)\]")
_TAG = re.compile(r"(?<![\w:])(c:\d\d-\d\d|d:[a-z0-9][a-z0-9-]*|b:[a-z]+|n:[a-z][a-z-]*|img\d+)")
_WAS = re.compile(r"\bwas:", re.I)

NOTION = {"n:ball": "src:notion/ball", "n:dash": "src:notion/dash",
          "n:ecom-resources": "src:notion/dash"}
IGNORE = {"d:slug"}          # placeholder in docs, not a real source


def tags_in(text):
    """Every source tag inside square brackets, in order, de-duplicated."""
    out = []
    for inner in _BRACKET.findall(text or ""):
        for t in _TAG.findall(inner):
            if t not in out and t not in IGNORE:
                out.append(t)
    return out


def tag_to_id(tag):
    if tag.startswith("c:"):
        return "src:calls/2026-" + tag[2:]
    if tag.startswith("d:"):
        return "src:docs/" + tag[2:]
    if tag.startswith("b:"):
        return "src:books/" + tag[2:]
    if tag.startswith("img"):
        return "src:notion/images#img%02d" % int(tag[3:])
    return NOTION.get(tag)


def split_supersedes(text):
    """(cited_tags, superseded) where superseded is [(tag, line)] for tags that sit
    after 'was:' on a ⚠ line: the older advice the KB keeps only as history."""
    cited, superseded = [], []
    for line in (text or "").splitlines():
        m = _WAS.search(line) if "⚠" in line else None
        before, after = (line[:m.start()], line[m.end():]) if m else (line, "")
        for t in tags_in(before):
            if t not in cited:
                cited.append(t)
        for t in tags_in(after):
            superseded.append((t, line.strip()[:300]))
    return cited, superseded
