"""Check a knowledge base folder: every file index.yaml routes to exists and parses,
every KB file is routed somewhere, and markdown files have complete frontmatter.

  python scripts/check_kb.py            # checks kb/ (or kb.example/ if kb/ doesn't exist)
  python scripts/check_kb.py kb.example
Needs PyYAML: `uv run --no-project --with pyyaml python scripts/check_kb.py`, or pip install pyyaml. Exit code 1 on any problem.
"""
import os, sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTMATTER = ("topic", "load_when", "sources")


def check(kb):
    problems = []
    index = yaml.safe_load(open(os.path.join(kb, "index.yaml"), encoding="utf-8"))
    routed = set(index.get("always", []))
    for name, b in index["bundles"].items():
        routed.update(b.get("kb", []))
    routed.update(index.get("files", {}))
    for rel in sorted(routed):
        if not os.path.exists(os.path.join(kb, rel)):
            problems.append(f"routed but missing: {rel}")

    for d, _, files in os.walk(kb):
        for f in files:
            rel = os.path.relpath(os.path.join(d, f), kb)
            path = os.path.join(kb, rel)
            if f.endswith((".yaml", ".yml")):
                try:
                    yaml.safe_load(open(path, encoding="utf-8"))
                except yaml.YAMLError as e:
                    problems.append(f"bad YAML: {rel}: {e}")
            if not f.endswith(".md") or f == "README.md":
                continue
            if rel not in routed:
                problems.append(f"not routed by index.yaml: {rel}")
            text = open(path, encoding="utf-8").read()
            if not text.startswith("---\n"):
                problems.append(f"no frontmatter: {rel}")
                continue
            try:
                meta = yaml.safe_load(text.split("---\n", 2)[1]) or {}
            except yaml.YAMLError as e:
                problems.append(f"bad frontmatter: {rel}: {e}")
                continue
            missing = [k for k in FRONTMATTER if k not in meta]
            if missing:
                problems.append(f"frontmatter missing {missing}: {rel}")
    return problems


def main():
    arg = sys.argv[1] if len(sys.argv) > 1 else ("kb" if os.path.isdir(os.path.join(ROOT, "kb")) else "kb.example")
    kb = os.path.join(ROOT, arg)
    problems = check(kb)
    for p in problems:
        print(p)
    print(f"{arg}: {'OK' if not problems else f'{len(problems)} problem(s)'}")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
