#!/usr/bin/env python3
"""Validate the independent A/B scoring payload used by the Skill."""
from __future__ import annotations

import json
import sys
from pathlib import Path

WEIGHTS = {
    "A": {
        "research_value": 15,
        "innovation": 25,
        "question_clarity": 15,
        "design_fit": 20,
        "analysis_depth": 15,
        "application_value": 10,
    },
    "B": {
        "data_access": 30,
        "skills_match": 20,
        "time": 20,
        "budget": 15,
        "implementation_channels": 15,
    },
}


def validate_dimension(payload: dict, name: str) -> dict:
    if not isinstance(payload, dict):
        raise ValueError(f"{name} must be an object")
    expected = WEIGHTS[name]
    items = payload.get("items")
    if not isinstance(items, dict):
        raise ValueError(f"{name}.items must be an object")
    extra = set(items) - set(expected)
    missing = set(expected) - set(items)
    if extra or missing:
        raise ValueError(f"{name} item keys mismatch; extra={sorted(extra)}, missing={sorted(missing)}")
    total = 0.0
    known_weight = 0
    details = {}
    for key, weight in expected.items():
        item = items[key]
        if not isinstance(item, dict):
            raise ValueError(f"{name}.{key} must be an object")
        anchor = item.get("anchor")
        if anchor is not None and (not isinstance(anchor, int) or anchor < 0 or anchor > 5):
            raise ValueError(f"{name}.{key}.anchor must be an integer 0..5 or null")
        weighted = 0 if anchor is None else weight * anchor / 5
        if "weighted" in item and abs(float(item["weighted"]) - weighted) > 1e-9:
            raise ValueError(f"{name}.{key}.weighted does not match weight*anchor/5")
        if anchor is not None:
            known_weight += weight
            total += weighted
        details[key] = {"weight": weight, "anchor": anchor, "weighted": weighted, "status": "unknown" if anchor is None else "scored"}
    status = "complete" if known_weight == sum(expected.values()) else "partial"
    return {
        "status": status,
        "score": total,
        "known_points": total,
        "max_known_points": known_weight,
        "evidence_coverage": known_weight / sum(expected.values()),
        "items": details,
    }


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_scores.py SCORE.json", file=sys.stderr)
        return 2
    try:
        data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
        result = {name: validate_dimension(data.get(name), name) for name in ("A", "B")}
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (OSError, json.JSONDecodeError, ValueError, TypeError) as exc:
        print(f"score validation failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
