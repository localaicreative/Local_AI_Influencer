#!/usr/bin/env python3
"""
Knowledge Migrator — Move inbox notes to knowledge/ with synthesis & backlinks.

Usage:
    python3 migrate_to_knowledge.py [vault_path] [--dry-run]
    python3 migrate_to_knowledge.py /path/to/vault --topic "deepseek"  # Migrate specific topic
    python3 migrate_to_knowledge.py /path/to/vault --auto              # Auto-migrate high-score notes

Example:
    python3 migrate_to_knowledge.py "/home/bobadmin/projects/Local_AI_Influencer/research-vault/" --auto
"""

import argparse
import re
from datetime import datetime
from pathlib import Path
from collections import defaultdict


# ─── MIGRATION CRITERIA ──────────────────────────────────────────

MIN_SCORE_AUTO = 35          # Auto-migrate wenn Score >= 35 (realistisch ohne Reddit Engagement)
MIN_NOTES_FOR_SYNTHESIS = 2  # Synthese nur wenn >= 2 Notes zum gleichen Topic
MAX_AGE_DAYS = 14            # Notes älter als 14 Tage werden nicht auto-migriert


# ─── TOPIC EXTRACTION (improved) ────────────────────────────────

def extract_topic_v2(title):
    """Extract main topic entity from title — improved version."""
    cleaned = re.sub(r'^(?:new |update: |release: |announced: )', '', title.lower())
    cleaned = re.sub(r'(?: using| with| on| in| for| vs\.?| and ).*$', '', cleaned)

    # Known entities (models, tools, companies, concepts)
    entities = []
    known = {
        "qwen": "Qwen", "llama": "Llama", "mistral": "Mistral", "gemma": "Gemma",
        "glm": "GLM", "fable": "Fable", "mixtral": "Mixtral", "ollama": "Ollama",
        "claude": "Claude", "deepseek": "DeepSeek", "phi": "Phi", "yi": "Yi",
        "command r": "Command R", "llama.cpp": "llama.cpp", "webgpu": "WebGPU",
        "comfyui": "ComfyUI", "lm studio": "LM Studio", "vllm": "vLLM",
        "deepmind": "DeepMind", "nvidia": "NVIDIA", "anthropic": "Anthropic",
        "hashicorp": "HashiCorp", "huggingface": "HuggingFace",
    }

    for kw, name in known.items():
        if kw in cleaned:
            entities.append(name)

    # Hardware keywords
    hw = ["rtx 4090", "rtx 3090", "consumer gpu", "webgpu inference"]
    for h in hw:
        if h in cleaned:
            entities.append(h.title())

    if not entities:
        words = re.findall(r'\w{3,}', cleaned)
        # Filter out common stop words
        stops = {"the", "new", "update", "release", "using", "with", "how", "why",
                 "what", "when", "where", "stop", "don't", "should", "we", "i"}
        meaningful = [w for w in words if w not in stops]
        entities = meaningful[:2]

    return " + ".join(entities) if entities else "General"


# ─── NOTE PARSING ──────────────────────────────────────────────

def parse_inbox_note(filepath):
    """Parse an inbox note and extract metadata."""
    try:
        content = filepath.read_text(encoding='utf-8')
    except Exception:
        return None

    # Extract frontmatter fields
    def get_field(name, default=""):
        match = re.search(rf'^{name}:\s*(.+)$', content, re.MULTILINE)
        return match.group(1).strip() if match else default

    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else filepath.stem

    score_str = get_field("attention-score", "0")
    try:
        score = int(score_str)
    except ValueError:
        score = 0

    return {
        "title": title,
        "file": str(filepath),
        "path": filepath,
        "score": score,
        "blog_potential": get_field("blog-potential", "low"),
        "source_type": get_field("source-type", "unknown"),
        "source_name": get_field("source", ""),
        "tags": get_field("attention-tags", ""),
        "created": get_field("created", ""),
        "url": get_field("video-url", "") or get_field("url", ""),
        "content": content,
    }


# ─── INBOX SCANNING ─────────────────────────────────────────────

def scan_inbox(inbox_dir):
    """Scan all inbox notes and return parsed list."""
    notes = []

    if not inbox_dir.exists():
        return notes

    for day_dir in sorted(inbox_dir.iterdir()):
        if not day_dir.is_dir() or day_dir.name.startswith("curation_"):
            continue

        for note_file in day_dir.glob("*.md"):
            parsed = parse_inbox_note(note_file)
            if parsed:
                parsed["date"] = day_dir.name
                notes.append(parsed)

    return notes


# ─── CLUSTERING ────────────────────────────────────────────────

def cluster_notes(notes):
    """Group notes by topic."""
    clusters = defaultdict(list)

    for note in notes:
        topic = extract_topic_v2(note["title"])
        clusters[topic].append(note)

    # Sort each cluster by score descending
    for topic in clusters:
        clusters[topic].sort(key=lambda x: x["score"], reverse=True)

    return clusters


# ─── MIGRATION DECISION ENGINE ──────────────────────────────────

def should_migrate(cluster_name, notes, mode="auto"):
    """Decide whether a cluster should be migrated to knowledge/."""
    if mode == "manual":
        return True  # User explicitly requested it

    if mode == "topic" and cluster_name:
        return True  # User specified this topic

    # Auto-mode criteria
    avg_score = sum(n["score"] for n in notes) / len(notes)
    max_score = max(n["score"] for n in notes)

    # Criteria 1: High enough score
    if max_score >= MIN_SCORE_AUTO and avg_score >= 30:
        return True

    # Criteria 2: Multiple notes on same topic (established theme)
    if len(notes) >= MIN_NOTES_FOR_SYNTHESIS and avg_score >= 25:
        return True

    # Criteria 3: Medium or high blog potential
    if any(n["blog_potential"] in ["high", "medium"] for n in notes):
        return True

    return False


def determine_knowledge_folder(cluster_name, notes):
    """Determine which knowledge/ subfolder to use."""
    all_titles = " ".join(n["title"].lower() for n in notes)
    topic_lower = cluster_name.lower()

    # Hardware-related?
    hw_keywords = ["gpu", "rtx", "hardware", "setup", "benchmark", "webgpu", "inference speed"]
    if any(kw in all_titles or kw in topic_lower for kw in hw_keywords):
        return "hardware"

    # Model-related?
    model_keywords = ["qwen", "llama", "mistral", "gemma", "glm", "fable", "deepseek",
                       "claude", "model", "release"]
    if any(kw in all_titles or kw in topic_lower for kw in model_keywords):
        return "models"

    # Use-case related?
    uc_keywords = ["tutorial", "guide", "how to", "use case", "application", "code assistant"]
    if any(kw in all_titles for kw in uc_keywords):
        return "use-cases"

    # Default: topics (general themes)
    return "topics"


# ─── KNOWLEDGE NOTE GENERATION ──────────────────────────────────

def generate_knowledge_note(cluster_name, notes, folder):
    """Generate a knowledge synthesis note from clustered inbox notes."""
    avg_score = sum(n["score"] for n in notes) / len(notes)
    max_score = max(n["score"] for n in notes)
    sources = set(n["source_type"] for n in notes)

    # Determine blog category suggestion
    all_titles_lower = " ".join(n["title"].lower() for n in notes)
    if any(p in all_titles_lower for p in ["stop using", "don't use", "banned", "controversial"]):
        blog_cat = "Opinion Piece"
    elif any(kw in all_titles_lower for kw in ["tutorial", "guide", "how to"]):
        blog_cat = "Practical Guide"
    elif len(notes) >= 2:
        blog_cat = "Trend Analysis"
    else:
        blog_cat = "Model Spotlight"

    # Build sources section with backlinks
    sources_section = ""
    for note in notes:
        inbox_ref = f"_inbox/{note['date']}/{note['path'].name}"
        pot_marker = " ⭐" if note["blog_potential"] == "high" else ""
        sources_section += f"- [[{note['title']}]] ({inbox_ref}) — {note['score']}pts{pot_marker}\n"

    # Build summary from top note's content (first 5 sentences)
    top_note = notes[0]
    summary_match = re.search(r'## Zusammenfassung\n\n(.+?)(?:\n\n|\n##)', top_note["content"], re.DOTALL)
    summary_text = summary_match.group(1).strip() if summary_match else "Zusammenfassung pending — manuell ergänzen."

    # Extract transcript/post content for richer context
    extra_context = ""
    for note in notes[:2]:  # Top 2 notes
        transcript_match = re.search(r'## Vollstndiges Transkript\n\n> (.+?)(?:\n\n|\n##)', note["content"], re.DOTALL)
        if transcript_match:
            extra_context += f"\n### Kontext aus \"{note['title']}\"\n\n{transcript_match.group(1).strip()[:500]}...\n"

    content = f"""---
topic: {cluster_name}
status: reviewed
last-updated: {datetime.now().strftime('%Y-%m-%d')}
sources_count: {len(notes)}
attention_avg: {avg_score:.0f}
attention_max: {max_score}
folder: {folder}
---

# {cluster_name.title()} — Was wir wissen

## Zusammenfassung

{summary_text}

{extra_context}

## Quellen ({len(notes)} Inbox-Notes)

{sources_section}

## Hardware-Kontext

[Manuell ergnzen: Welche GPU/RAM/Storage wird gebraucht? Laeuft auf Consumer-Hardware?]

## Community-Stimmung

[Manuell ergnzen: Positiv / Negativ / Gemischt — Kontroversen?]

## Blog-Potenzial

- **Kategorie-Vorschlag:** {blog_cat}
- **Blog-Potenzial:** {"HOCH" if any(n['blog_potential'] in ['high', 'medium'] for n in notes) else "NIEDRIG"}
- **Warum:** {len(notes)} Notes zum Thema, Max Score: {max_score}pts

## Verwandte Topics

- [[ ]]
- [[ ]]

---
*Knowledge Note erstellt am {datetime.now().strftime('%Y-%m-%d %H:%M')} — auto-migriert aus Inbox*
"""

    return content


# ─── MIGRATION EXECUTION ────────────────────────────────────────

def migrate_cluster(cluster_name, notes, vault_path, dry_run=False):
    """Execute migration: create knowledge note + move inbox notes."""
    folder = determine_knowledge_folder(cluster_name, notes)
    knowledge_dir = vault_path / "knowledge" / folder
    knowledge_dir.mkdir(parents=True, exist_ok=True)

    # Generate slug for knowledge note
    slug = re.sub(r'[^\w\s-]', '', cluster_name.lower())
    slug = re.sub(r'[\s_]+', '-', slug)[:50]
    filename = f"{slug}.md"
    filepath = knowledge_dir / filename

    # Check if already exists
    if filepath.exists():
        print(f"  [SKIP] Knowledge note exists: {filepath.name}")
        return False

    # Generate content
    content = generate_knowledge_note(cluster_name, notes, folder)

    if dry_run:
        print(f"  [DRY-RUN] Would create: knowledge/{folder}/{filename}")
        for note in notes:
            print(f"    → {note['path'].name} ({note['score']}pts)")
        return False

    # Write knowledge note
    filepath.write_text(content, encoding='utf-8')
    print(f"  [OK] Created: knowledge/{folder}/{filename}")

    # Move inbox notes to _inbox/archive/ (don't delete — keep history)
    archive_dir = vault_path / "_inbox" / "archive"
    archive_dir.mkdir(parents=True, exist_ok=True)

    for note in notes:
        src = Path(note["path"])
        dst = archive_dir / src.name
        # Rename if conflict
        counter = 1
        while dst.exists():
            dst = archive_dir / f"{src.stem}_{counter}{src.suffix}"
            counter += 1
        src.rename(dst)
        print(f"    Archived: {src.name} → _inbox/archive/")

    return True


# ─── REPORTING ──────────────────────────────────────────────────

def print_migration_plan(clusters, mode="auto"):
    """Print what would be migrated."""
    print(f"\n{'='*60}")
    print(f"  KNOWLEDGE MIGRATION PLAN")
    print(f"{'='*60}\n")

    migrate_count = 0
    skip_count = 0

    for topic, notes in sorted(clusters.items(), key=lambda x: len(x[1]), reverse=True):
        avg_score = sum(n["score"] for n in notes) / len(notes)
        max_score = max(n["score"] for n in notes)
        folder = determine_knowledge_folder(topic, notes)

        will_migrate = should_migrate(topic, notes, mode=mode)

        status = "→ MIGRATE" if will_migrate else "→ SKIP"
        reason = ""
        if will_migrate:
            if max_score >= MIN_SCORE_AUTO:
                reason = f"(Score {max_score}pts >= {MIN_SCORE_AUTO})"
            elif len(notes) >= MIN_NOTES_FOR_SYNTHESIS:
                reason = f"({len(notes)} Notes, etabliertes Thema)"
            elif any(n["blog_potential"] in ["high", "medium"] for n in notes):
                reason = "(Blog-Potenzial: medium/high)"
        else:
            reason = f"(Avg {avg_score:.0f}pts < threshold)"

        marker = "✓" if will_migrate else "○"
        print(f"  [{marker}] {topic.title()} ({len(notes)} Notes, Avg: {avg_score:.0f}, Max: {max_score})")
        print(f"      → knowledge/{folder}/ | {status} {reason}")

        for note in notes[:3]:
            pot = "⭐" if note["blog_potential"] == "high" else ""
            print(f"         • [{note['score']}pts] {note['title']}{pot}")

        if len(notes) > 3:
            print(f"         ... und {len(notes)-3} weitere")

        print()

        if will_migrate:
            migrate_count += 1
        else:
            skip_count += 1

    print(f"{'='*60}")
    print(f"  Zusammenfassung: {migrate_count} Topics migrieren, {skip_count} überspringen")
    print(f"{'='*60}\n")

    return migrate_count


# ─── MAIN ────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Knowledge Migrator — Inbox → Knowledge/")
    parser.add_argument("vault_path", help="Path to Obsidian vault")
    parser.add_argument("--dry-run", action="store_true", help="Show plan without executing")
    parser.add_argument("--auto", action="store_true", help="Auto-migrate based on criteria")
    parser.add_argument("--topic", type=str, default=None, help="Migrate specific topic only")
    args = parser.parse_args()

    vault_path = Path(args.vault_path)
    inbox_dir = vault_path / "_inbox"

    if not inbox_dir.exists():
        print("Fehler: _inbox/ nicht gefunden. Fuehre zuerst run_research.py aus.")
        return

    # Scan inbox (exclude archive/)
    notes = scan_inbox(inbox_dir)

    if not notes:
        print("Inbox ist leer — nichts zu migrieren.")
        return

    print(f"\nGefunden: {len(notes)} Inbox-Notes")

    # Cluster by topic
    clusters = cluster_notes(notes)

    # Filter to specific topic if requested
    if args.topic:
        target_topic = None
        for topic in clusters:
            if args.topic.lower() in topic.lower():
                target_topic = topic
                break

        if target_topic:
            print(f"Topic gefiltert: {target_topic}")
            clusters = {target_topic: clusters[target_topic]}
        else:
            print(f"Fehler: Topic '{args.topic}' nicht gefunden.")
            print("Verfuegbare Topics:")
            for t in sorted(clusters.keys()):
                print(f"  - {t} ({len(clusters[t])} Notes)")
            return

    # Determine mode
    mode = "topic" if args.topic else ("auto" if args.auto else "manual")

    # Show plan
    migrate_count = print_migration_plan(clusters, mode=mode)

    if args.dry_run:
        print("[DRY-RUN] Keine Aenderungen vorgenommen.")
        return

    # Execute migration
    if mode == "auto":
        for topic, notes_list in clusters.items():
            if should_migrate(topic, notes_list, mode="auto"):
                migrate_cluster(topic, notes_list, vault_path, dry_run=False)
    elif mode == "topic":
        for topic, notes_list in clusters.items():
            migrate_cluster(topic, notes_list, vault_path, dry_run=False)
    else:  # manual — ask user (not applicable in CLI script, default to auto behavior)
        print("Interaktiver Modus nicht verfuegbar im Script-Modus.")
        print("Benutze --auto fuer automatische Migration oder --topic 'Name' fuer spezifisches Topic.")
        return

    # Summary
    knowledge_dirs = vault_path / "knowledge"
    total_knowledge = sum(1 for f in knowledge_dirs.rglob("*.md") if not f.name.startswith("_"))
    print(f"\n[DONE] Knowledge Vault: {total_knowledge} Notes gesamt")


if __name__ == "__main__":
    main()
