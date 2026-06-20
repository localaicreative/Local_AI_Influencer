#!/usr/bin/env python3
"""
Inbox Router — Move new notes from trends/ into _inbox/YYYY-MM-DD/
and assign attention scores to notes that lack them.

Usage:
    python3 inbox_router.py [vault_path] [--dry-run]

This script is the bridge between research collection (which writes to trends/)
and the curation pipeline (which expects _inbox/DATE/*.md with attention-score).

Run this after research cronjobs have written new notes to trends/.
"""

import argparse
import re
from datetime import datetime
from pathlib import Path


# ─── ATTENTION SCORING ──────────────────────────────────────────

def calculate_attention_score(content, source_type, title):
    """Calculate attention score for a note that lacks one.

    Scoring breakdown (max 50pts):
      - Source type: Video=15, Community=10, News=8, Other=5
      - Content length bonus: >2000 chars = +10, >500 = +5
      - Has transcript/full content: +10
      - Controversial keywords: +5 each (max +15)
      - Model/company mentions: +3 each (max +9)
    """
    score = 0

    # Source type base score
    source_scores = {
        "video": 15,
        "community": 10,
        "news": 8,
        "blog": 7,
        "unknown": 5,
    }
    score += source_scores.get(source_type.lower(), 5)

    # Content length bonus
    content_length = len(content)
    if content_length > 2000:
        score += 10
    elif content_length > 500:
        score += 5

    # Has transcript or substantial content
    if "transkript" in content.lower() or "vollstndiges" in content.lower():
        score += 10
    elif content_length > 1000:
        score += 5

    # Controversial/engaging keywords (max +15)
    controversial = ["banned", "stop using", "don't use", "controversial",
                     "jailbreak", "uncensored", "takedown", "forced"]
    controversy_score = sum(5 for kw in controversial if kw.lower() in content.lower())
    score += min(controversy_score, 15)

    # Model/company mentions (max +9)
    entities = ["qwen", "llama", "deepseek", "claude", "nvidia", "anthropic",
                "deepmind", "glm", "fable", "mythos", "mistral", "gemma"]
    entity_count = sum(1 for e in entities if e.lower() in content.lower())
    score += min(entity_count * 3, 9)

    return min(score, 50)  # Cap at 50


def ensure_attention_score(content):
    """Add or update attention-score in frontmatter if missing."""
    has_score = bool(re.search(r'^attention-score:\s*\d+', content, re.MULTILINE))

    if has_score:
        return content  # Already has a score

    # Extract title for scoring context
    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else ""

    # Extract source-type
    source_match = re.search(r'^source-type:\s*(.+)$', content, re.MULTILINE)
    source_type = source_match.group(1).strip() if source_match else "unknown"

    score = calculate_attention_score(content, source_type, title)

    # Insert attention-score after the 'status:' line or at end of frontmatter
    if 'status:' in content:
        content = re.sub(
            r'(status:\s*.+)$',
            r'\1\nattention-score: ' + str(score),
            content,
            count=1,
            flags=re.MULTILINE,
        )
    elif content.startswith('---'):
        # Insert before closing ---
        content = re.sub(
            r'(^---\s*$)',
            r'attention-score: ' + str(score) + r'\n\1',
            content,
            count=1,
            flags=re.MULTILINE,
        )

    return content


# ─── ROUTING ─────────────────────────────────────────────────────

def route_trends_to_inbox(vault_path, dry_run=False):
    """Move new notes from trends/ to _inbox/YYYY-MM-DD/ with scores."""
    trends_dir = vault_path / "trends"
    inbox_dir = vault_path / "_inbox"

    if not trends_dir.exists():
        print("trends/ nicht gefunden — nichts zu routen.")
        return 0

    # Get today's date for inbox subdirectory
    today = datetime.now().strftime("%Y-%m-%d")
    day_dir = inbox_dir / today
    day_dir.mkdir(parents=True, exist_ok=True)

    moved = 0
    skipped = 0

    for note_file in sorted(trends_dir.glob("*.md")):
        # Skip synthesis templates and non-note files
        if note_file.name.startswith("_") or note_file.name.startswith("curation_"):
            continue

        try:
            content = note_file.read_text(encoding='utf-8')
        except Exception:
            continue

        # Ensure it has an attention score
        content = ensure_attention_score(content)

        dest = day_dir / note_file.name

        # Handle filename conflicts
        if dest.exists():
            stem = note_file.stem
            suffix = note_file.suffix
            counter = 1
            while dest.exists():
                dest = day_dir / f"{stem}_{counter}{suffix}"
                counter += 1

        if dry_run:
            # Show what would happen
            score_match = re.search(r'attention-score:\s*(\d+)', content)
            score = score_match.group(1) if score_match else "?"
            print(f"  [DRY-RUN] {note_file.name} → _inbox/{today}/ (score: {score})")
            moved += 1
        else:
            # Write to inbox with updated content
            dest.write_text(content, encoding='utf-8')
            # Remove from trends/ (it's now in the proper pipeline)
            note_file.unlink()
            score_match = re.search(r'attention-score:\s*(\d+)', content)
            score = score_match.group(1) if score_match else "?"
            print(f"  [MOVED] {note_file.name} → _inbox/{today}/ (score: {score})")
            moved += 1

    return moved


# ─── MAIN ────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Inbox Router — trends/ → _inbox/DATE/")
    parser.add_argument("vault_path", nargs="?", default=".", help="Path to research vault")
    parser.add_argument("--dry-run", action="store_true", help="Show plan without moving files")
    args = parser.parse_args()

    vault_path = Path(args.vault_path)
    trends_dir = vault_path / "trends"

    if not trends_dir.exists():
        print(f"Fehler: {trends_dir} nicht gefunden.")
        return

    trend_files = list(trends_dir.glob("*.md"))
    # Filter out templates/curation files
    routable = [f for f in trend_files if not f.name.startswith("_") and not f.name.startswith("curation_")]

    print(f"\nInbox Router — {len(routable)} Notes in trends/")

    if not routable:
        print("  Keine neuen Notes zum Routen.")
        return

    moved = route_trends_to_inbox(vault_path, dry_run=args.dry_run)

    if args.dry_run:
        print(f"\n[DRY-RUN] {moved} Notes wuerden geroutet werden.")
    else:
        print(f"\n[DONE] {moved} Notes nach _inbox/{datetime.now().strftime('%Y-%m-%d')}/ verschoben.")


if __name__ == "__main__":
    main()
