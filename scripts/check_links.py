"""Fail if any Markdown file links or embeds a relative path that does not exist."""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATTERN = re.compile(r'(?:\]\(|src="|srcset=")([^)"#\s]+)')


def main() -> int:
    broken = []
    for md in ROOT.rglob("*.md"):
        if ".git" in md.parts:
            continue
        for target in PATTERN.findall(md.read_text(encoding="utf-8")):
            if target.startswith(("http://", "https://", "mailto:")):
                continue
            if not (md.parent / target).resolve().exists():
                broken.append(f"{md.relative_to(ROOT)} -> {target}")
    for b in broken:
        print("broken link:", b)
    print(f"checked links, {len(broken)} broken")
    return 1 if broken else 0


if __name__ == "__main__":
    sys.exit(main())
