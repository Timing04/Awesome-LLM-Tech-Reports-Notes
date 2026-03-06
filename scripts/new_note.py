#!/usr/bin/env python3
"""Create a new note from a repository template."""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_MAP = {
    "model": REPO_ROOT / "templates" / "model_note_template.md",
    "paper": REPO_ROOT / "templates" / "paper_note_template.md",
    "topic": REPO_ROOT / "templates" / "topic_template.md",
}


def build_topics_block(topics: list[str]) -> str:
    if not topics:
        return "  - todo"
    return "\n".join(f"  - {topic}" for topic in topics)


def build_replacements(args: argparse.Namespace) -> dict[str, str]:
    return {
        "{{TITLE}}": args.title,
        "{{FAMILY}}": args.family or "unknown",
        "{{CATEGORY}}": args.category or "unknown",
        "{{RELEASE_DATE}}": args.release_date or str(date.today()),
        "{{MODEL_SCOPE}}": args.model_scope or "base + instruct",
        "{{PARAMS}}": args.params or "unknown",
        "{{TOPICS_BLOCK}}": build_topics_block(args.topics or []),
        "{{SOURCE_KIND}}": args.source_kind or "arxiv",
        "{{SOURCE_REF}}": args.source_ref or "TBD",
        "{{OFFICIAL_URL}}": args.official_url or "",
        "{{SOURCE_STATUS}}": args.source_status or "to_verify",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--kind", choices=sorted(TEMPLATE_MAP), required=True)
    parser.add_argument("--path", required=True, help="Note path relative to repo root")
    parser.add_argument("--title", required=True)
    parser.add_argument("--family")
    parser.add_argument("--category")
    parser.add_argument("--release-date")
    parser.add_argument("--model-scope")
    parser.add_argument("--params")
    parser.add_argument("--topics", nargs="*")
    parser.add_argument("--source-kind")
    parser.add_argument("--source-ref")
    parser.add_argument("--official-url")
    parser.add_argument("--source-status")
    args = parser.parse_args()

    template_path = TEMPLATE_MAP[args.kind]
    target_path = REPO_ROOT / args.path
    if target_path.exists():
        raise SystemExit(f"Refusing to overwrite existing file: {target_path}")

    content = template_path.read_text(encoding="utf-8")
    replacements = build_replacements(args)
    for old, new in replacements.items():
        content = content.replace(old, new)

    target_path.parent.mkdir(parents=True, exist_ok=True)
    target_path.write_text(content, encoding="utf-8")
    print(f"Created {target_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
