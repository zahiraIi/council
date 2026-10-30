"""JSONL tracing for MCP tool calls and a small summary view (`kg trace`).
One line per call: ts, tool, args, latency_ms, n_results, top_ids, error, pid."""
import json, os, time

from . import KG_DIR

TRACE_PATH = os.environ.get("KG_TRACE", os.path.join(KG_DIR, "data", "traces", "mcp.jsonl"))


def _count(result):
    if result is None:
        return 0
    if isinstance(result, list):
        return len(result)
    if isinstance(result, dict) and "chunks" in result:
        return len(result["chunks"])
    return 1


def record(tool, args, result=None, error=None, started=None, path=None):
    """Append one trace line. Tracing must never break a tool call, so failures are swallowed."""
    path = path or TRACE_PATH
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        line = {
            "ts": round(time.time(), 3),
            "tool": tool,
            "args": {k: (v[:200] if isinstance(v, str) else v) for k, v in (args or {}).items()},
            "latency_ms": round((time.perf_counter() - started) * 1000, 1) if started else None,
            "n_results": _count(result),
            "top_ids": [r.get("id") for r in result[:3]] if isinstance(result, list) else None,
            "error": str(error)[:300] if error else None,
            "pid": os.getpid(),
        }
        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps(line, ensure_ascii=False) + "\n")
    except Exception:
        pass


def load(path=None, since=None):
    path = path or TRACE_PATH
    if not os.path.exists(path):
        return []
    out = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                continue
            if since is None or r.get("ts", 0) >= since:
                out.append(r)
    return out


def _pct(xs, p):
    if not xs:
        return None
    xs = sorted(xs)
    return xs[min(len(xs) - 1, int(round(p / 100 * (len(xs) - 1))))]


def summary(rows):
    by_tool = {}
    for r in rows:
        by_tool.setdefault(r["tool"], []).append(r)
    tools = {}
    for tool, rs in sorted(by_tool.items()):
        lat = [r["latency_ms"] for r in rs if r.get("latency_ms") is not None]
        tools[tool] = {
            "calls": len(rs),
            "p50_ms": _pct(lat, 50), "p95_ms": _pct(lat, 95),
            "zero_result_rate": round(sum(1 for r in rs if not r.get("n_results")) / len(rs), 3),
            "errors": sum(1 for r in rs if r.get("error")),
            "sessions": len({r.get("pid") for r in rs}),
        }
    zero = [r["args"].get("query") for r in rows if r["tool"] == "kg_search" and not r.get("n_results")]
    return {"calls": len(rows), "tools": tools, "zero_result_queries": zero[-10:]}
