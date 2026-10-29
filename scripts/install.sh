#!/bin/sh
# Symlink this repo's skills into ~/.claude/skills and make sure ~/council points at the repo.
set -e
ROOT="$(cd "$(dirname "$0")/.." && pwd)"

if [ "$ROOT" != "$HOME/council" ]; then
  if [ -e "$HOME/council" ] && [ ! -L "$HOME/council" ]; then
    echo "~/council exists and is not this repo; skills reference ~/council paths. Move it or clone here." >&2
    exit 1
  fi
  ln -sfn "$ROOT" "$HOME/council"
fi

mkdir -p "$HOME/.claude/skills"
for dir in "$ROOT"/skills/*/; do
  name="$(basename "$dir")"
  target="$HOME/.claude/skills/$name"
  if [ -e "$target" ] && [ ! -L "$target" ]; then
    echo "skip $name: $target exists and is not a symlink" >&2
    continue
  fi
  ln -sfn "$HOME/council/skills/$name" "$target"
  echo "linked $name"
done

# Knowledge graph MCP server (needs uv; build the graph with: cd ~/council/kg && uv run kg build)
if command -v claude >/dev/null 2>&1 && command -v uv >/dev/null 2>&1; then
  if claude mcp get council-kg >/dev/null 2>&1; then
    echo "council-kg MCP server already registered"
  else
    claude mcp add council-kg -s user -- uv run --project "$HOME/council/kg" python "$HOME/council/kg/mcp_server.py" \
      && echo "registered council-kg MCP server"
  fi
else
  echo "skip MCP registration: needs the claude CLI and uv" >&2
fi
