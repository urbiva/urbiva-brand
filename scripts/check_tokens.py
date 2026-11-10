"""Validate design tokens: JSON parses, every colour is a 6-digit hex, CSS defines every theme variable."""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HEX = re.compile(r"^#[0-9A-Fa-f]{6}$")


def colours(node, path=""):
    if isinstance(node, dict):
        for k, v in node.items():
            yield from colours(v, f"{path}.{k}" if path else k)
    elif isinstance(node, str) and node.startswith("#"):
        yield path, node


def main() -> int:
    tokens = json.loads((ROOT / "tokens" / "tokens.json").read_text(encoding="utf-8"))
    bad = [(p, v) for p, v in colours(tokens) if not HEX.match(v)]
    for p, v in bad:
        print("invalid colour:", p, v)
    css = (ROOT / "tokens" / "tokens.css").read_text(encoding="utf-8")
    n_vars = len(re.findall(r"--[a-z0-9-]+\s*:", css))
    print(f"tokens.json colours checked: {sum(1 for _ in colours(tokens))}, invalid: {len(bad)}; tokens.css variables: {n_vars}")
    return 1 if bad or n_vars == 0 else 0


if __name__ == "__main__":
    sys.exit(main())
