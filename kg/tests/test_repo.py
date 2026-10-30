"""Repo integrity checks (run in CI): the KB routing table and files are consistent."""
import os

import yaml

from councilkg import REPO_ROOT

KB = os.path.join(REPO_ROOT, "kb")


def load_index():
    with open(os.path.join(KB, "index.yaml"), encoding="utf-8") as f:
        return yaml.safe_load(f)


def test_index_paths_exist():
    index = load_index()
    missing = []
    for f in index.get("always") or []:
        if not os.path.exists(os.path.join(KB, f)):
            missing.append(("always", f))
    for name, b in (index.get("bundles") or {}).items():
        for f in b.get("kb") or []:
            if not os.path.exists(os.path.join(KB, f)):
                missing.append((name, f))
    for f in (index.get("files") or {}):
        if not os.path.exists(os.path.join(KB, f)):
            missing.append(("files", f))
    assert not missing, f"index.yaml points at missing files: {missing}"


def test_every_kb_file_is_routed():
    index = load_index()
    routed = set(index.get("always") or []) | set(index.get("files") or {})
    for b in (index.get("bundles") or {}).values():
        routed |= set(b.get("kb") or [])
    on_disk = {os.path.relpath(os.path.join(d, f), KB) for d, _, fs in os.walk(KB) for f in fs
               if f.endswith((".md", ".yaml")) and f != "index.yaml"}
    unrouted = on_disk - routed - {"skill-protocol.md"}
    assert not unrouted, f"KB files no bundle or catalog entry reaches: {sorted(unrouted)}"


def test_all_yaml_parses_and_md_has_frontmatter():
    bad = []
    for d, _, fs in os.walk(KB):
        for f in fs:
            p = os.path.join(d, f)
            text = open(p, encoding="utf-8").read()
            if f.endswith(".yaml"):
                try:
                    yaml.safe_load(text)
                except yaml.YAMLError as e:
                    bad.append((p, str(e)[:80]))
            elif f.endswith(".md") and f != "skill-protocol.md":
                if not text.startswith("---"):
                    bad.append((p, "no frontmatter"))
                    continue
                fm = yaml.safe_load(text[3:text.find("\n---", 3)]) or {}
                for key in ("topic", "load_when", "sources"):
                    if not fm.get(key):
                        bad.append((p, f"frontmatter missing {key}"))
    assert not bad, bad
