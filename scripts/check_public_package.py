#!/usr/bin/env python3
"""Block private corpus and obvious personal data from a public Skill package."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

BLOCKED_PARTS = {"国赛论文", "local_private_corpus", "extracted_text"}
BLOCKED_EXTENSIONS = {".pdf"}
TEXT_EXTENSIONS = {".md", ".txt", ".csv", ".json", ".yaml", ".yml", ".py"}
CONTACT_PATTERNS = {
    "phone_like": re.compile(r"(?<!\d)1[3-9]\d{9}(?!\d)"),
    "email_like": re.compile(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}"),
    "wechat_like": re.compile(r"(?:加微信|微信号|wechat)\s*[:：]?\s*[A-Za-z0-9_-]{5,}", re.I),
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("package_root", type=Path)
    parser.add_argument("--allow-public-case-index", action="store_true")
    args = parser.parse_args()
    root = args.package_root.resolve()
    if not root.is_dir():
        print(f"package root not found: {root}", file=sys.stderr)
        return 2
    failures: list[str] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if path.name == Path(__file__).name:
            continue
        rel_parts = {p.lower() for p in path.relative_to(root).parts}
        if any(part in {x.lower() for x in BLOCKED_PARTS} for part in rel_parts):
            failures.append(f"blocked private path: {path.relative_to(root)}")
            continue
        if path.suffix.lower() in BLOCKED_EXTENSIONS:
            failures.append(f"PDF/full report is not allowed: {path.relative_to(root)}")
            continue
        if path.suffix.lower() not in TEXT_EXTENSIONS:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError as exc:
            failures.append(f"unreadable file: {path.relative_to(root)} ({exc})")
            continue
        for label, pattern in CONTACT_PATTERNS.items():
            if pattern.search(text):
                failures.append(f"{label} in {path.relative_to(root)}")
        if not args.allow_public_case_index and "cases_2025_2026" in path.name.lower():
            failures.append(f"case index requires --allow-public-case-index: {path.relative_to(root)}")
    if failures:
        print("PUBLIC PACKAGE BLOCKED")
        print("\n".join(f"- {x}" for x in failures))
        return 1
    print(f"PUBLIC PACKAGE OK: {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
