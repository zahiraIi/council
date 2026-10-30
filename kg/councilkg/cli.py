import argparse, json, os, sys

from . import DB_PATH, api
from .build import build
from .store import Store


def main(argv=None):
    p = argparse.ArgumentParser(prog="kg", description="Council knowledge graph")
    sub = p.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build", help="index kb/ and _sources/ (incremental), then embed")
    b.add_argument("--force", action="store_true")
    b.add_argument("--no-embed", action="store_true")
    s = sub.add_parser("search")
    s.add_argument("query")
    s.add_argument("--kind")
    s.add_argument("--since")
    s.add_argument("--limit", type=int, default=8)
    g = sub.add_parser("get")
    g.add_argument("id")
    t = sub.add_parser("sources")
    t.add_argument("tag")
    sub.add_parser("stat")
    tr = sub.add_parser("trace", help="summarize MCP tool-call traces (latency, zero-result rate)")
    tr.add_argument("--hours", type=float, help="only the last N hours")
    a = p.parse_args(argv)

    if a.cmd == "trace":
        import time
        from . import trace
        rows = trace.load(since=time.time() - a.hours * 3600 if a.hours else None)
        print(json.dumps(trace.summary(rows), indent=1))
        return

    if a.cmd == "build":
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        st = Store(DB_PATH)
        stats = build(st, force=a.force, embed=not a.no_embed)
        bad = stats.pop("unresolved_tags")
        print(json.dumps(stats))
        print(json.dumps(st.stat(), indent=1))
        if bad:
            print(f"{len(bad)} unresolved citations:", file=sys.stderr)
            for e in bad[:20]:
                print(f"  {e['src']} -{e['type']}-> {e['dst']}", file=sys.stderr)
        return
    if a.cmd == "search":
        for h in api.kg_search(a.query, kind=a.kind, since=a.since, limit=a.limit):
            print(f"{h['id']}  [{h['kind']}]  {h['name']}\n    {h['text'][:200]}")
        return
    out = {"get": lambda: api.kg_get(a.id), "sources": lambda: api.kg_sources(a.tag),
           "stat": api.kg_stat}[a.cmd]()
    print(json.dumps(out, indent=1, default=str))


if __name__ == "__main__":
    main()
