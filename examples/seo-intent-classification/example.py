#!/usr/bin/env python3
"""Run the repository's intent classifier against deterministic examples."""

from __future__ import annotations

import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
RESOURCE_DIR = REPO_ROOT / "google-trends-to-pages" / "resources"
sys.path.insert(0, str(RESOURCE_DIR))

from intent_classifier import analyze_keyword, classify_intent  # noqa: E402


CASES = (
    ("how to get six eyes jujutsu infinite", 40, "+50%", "Informational"),
    ("yba codes april 2026", 80, "+120%", "Transactional"),
    ("best stands in yba tier list", 55, "+20%", "Commercial"),
    ("jujutsu infinite trading value list", 35, "+15%", "Navigational"),
)


def main() -> int:
    output = []
    for keyword, volume, growth, expected_intent in CASES:
        intent = classify_intent(keyword)
        analysis = analyze_keyword(keyword, volume, growth)
        assert intent == expected_intent
        assert analysis["intent"] == intent
        output.append(
            {
                "keyword": keyword,
                "intent": intent,
                "priority": analysis["priority"],
                "schema_type": analysis["schema_type"],
            }
        )

    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
