#!/usr/bin/env python3
"""Final polish - catch any remaining 'spürte' patterns and verify all fixes."""

from pathlib import Path

BASE = Path(__file__).parent / "episodes"

# Remaining issues to fix:
# Ep7 line 43: "er spürte: Torge war glücklich" -> show behavior
# Ep8 line 75: "er spürte: Torge war glücklich" -> same pattern  
# Ep9 line 73: "er spürte: Torge war glücklich" -> same pattern

remaining_fixes = {
    "episode_07_Die_Klappbruecke_geht_auf.md": [
        ('aber er spürte: Torge war glücklich. Und das war genug für ihn!', 'und fand das toll. Das war genug für ihn!'),
    ],
    "episode_08_Sturm_und_Sternschnuppen.md": [
        ('aber er spürte: Torge war glücklich. Und das war genug für ihn!', 'und fand das toll. Das war genug für ihn!'),
    ],
    "episode_09_Die_Koenigsmoewe_in_Graesten.md": [
        ('aber er spürte: Torge war glücklich. Und das war genug für ihn!', 'und fand das toll. Das war genug für ihn!'),
    ],
}

total_changes = 0

for filename, fixes in remaining_fixes.items():
    filepath = BASE / filename
    if not filepath.exists():
        print(f"⚠️  {filename} nicht gefunden!")
        continue
    
    content = filepath.read_text(encoding='utf-8')
    original = content
    
    for old, new in fixes:
        if old in content:
            content = content.replace(old, new)
            print(f"  ✅ {filename}: 'spürte' -> Verhalten")
    
    if content != original:
        filepath.write_text(content, encoding='utf-8')
        changes = sum(1 for a, b in zip(original.splitlines(), content.splitlines()) if a != b)
        total_changes += changes
        print(f"✅ {filename} — {changes} Zeilen geändert\n")
    else:
        print(f"⏭️  {filename} — keine Änderungen nötig\n")

# Now verify all episodes are consistent - check for any remaining "dachte" patterns on Samson
print("🔍 Prüfung auf verbliebene 'dachte'-Muster bei Samson...")
for ep_file in BASE.glob("episode_*.md"):
    content = ep_file.read_text(encoding='utf-8')
    
    # Look for Samson thinking patterns
    lines = content.splitlines()
    for i, line in enumerate(lines, 1):
        if 'Samson' in line and ('dachte' in line or 'spürte' in line) and 'Torge' not in line:
            # Check if it's Samson thinking (not Torge thinking about Samson)
            if 'er dachte' in line.lower() or 'er spürte' in line.lower():
                print(f"  ⚠️  {ep_file.name} Zeile {i}: {line.strip()}")

print("\n🔍 Prüfung auf 'als würde sagen'-Muster...")
for ep_file in BASE.glob("episode_*.md"):
    content = ep_file.read_text(encoding='utf-8')
    if 'als würde' in content and ('sagen' in content or 'sagte' in content):
        # More specific check
        for line in content.splitlines():
            if 'als würde' in line:
                print(f"  ⚠️  {ep_file.name}: {line.strip()}")

print("\n🔍 Prüfung auf 'nabeln'-Muster...")
for ep_file in BASE.glob("episode_*.md"):
    content = ep_file.read_text(encoding='utf-8')
    if 'nabeln' in content:
        for line in content.splitlines():
            if 'nabeln' in line:
                print(f"  ⚠️  {ep_file.name}: {line.strip()}")

print("\n🔍 Prüfung auf englische Wörter...")
for ep_file in BASE.glob("episode_*.md"):
    content = ep_file.read_text(encoding='utf-8')
    for line in content.splitlines():
        if 'outside' in line.lower() or 'inside' in line.lower():
            print(f"  ⚠️  {ep_file.name}: {line.strip()}")

print("\n🔍 Prüfung auf Episode-Referenzen...")
for ep_file in BASE.glob("episode_*.md"):
    content = ep_file.read_text(encoding='utf-8')
    for line in content.splitlines():
        if 'Episode' in line and 'in Episode' in line:
            print(f"  ⚠️  {ep_file.name}: {line.strip()}")

print("\n✅ Finale Prüfung abgeschlossen!")
