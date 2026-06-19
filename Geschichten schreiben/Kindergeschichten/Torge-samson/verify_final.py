#!/usr/bin/env python3
"""Final comprehensive verification of all lektorat fixes."""

from pathlib import Path

BASE = Path(__file__).parent / "episodes"

print("=" * 60)
print("🔍 FINALE VERIFIKATION – Alle 10 Episoden")
print("=" * 60)

issues_found = 0
episodes_checked = 0

for ep_file in sorted(BASE.glob("episode_*.md")):
    if '_status' in ep_file.name or 'master_plan' in ep_file.name:
        continue
    
    episodes_checked += 1
    content = ep_file.read_text(encoding='utf-8')
    lines = content.splitlines()
    
    file_issues = []
    
    # Check 1: "nabeln" (should be "nagen")
    for i, line in enumerate(lines, 1):
        if 'nabeln' in line:
            file_issues.append(f"Zeile {i}: 'nabeln' statt 'nagen': {line.strip()[:80]}")
    
    # Check 2: English words
    for i, line in enumerate(lines, 1):
        if 'outside' in line.lower():
            file_issues.append(f"Zeile {i}: Englisches Wort 'outside': {line.strip()[:80]}")
    
    # Check 3: Episode references (meta)
    for i, line in enumerate(lines, 1):
        if 'in Episode' in line and ep_file.name not in ['episode_10_status.md']:
            file_issues.append(f"Zeile {i}: Meta-Referenz: {line.strip()[:80]}")
    
    # Check 4: Samson "dachte" patterns (direct thought attribution)
    for i, line in enumerate(lines, 1):
        if 'Samson' in line and ('dachte "' in line or 'dachte \'' in line):
            file_issues.append(f"Zeile {i}: Samson dachte: {line.strip()[:80]}")
    
    # Check 5: "als würde er/sie sagen:" patterns (direct speech attribution)
    for i, line in enumerate(lines, 1):
        if 'als würde' in line and ('sagen:' in line or 'sagte:' in line):
            file_issues.append(f"Zeile {i}: 'als würde sagen': {line.strip()[:80]}")
    
    # Check 6: "Sonderborg" without ø (inconsistent spelling)
    for i, line in enumerate(lines, 1):
        if 'Sonderborg' in line and 'ø' not in line.lower():
            # Only flag if it's the city name context, not part of a proper compound
            if 'in Sonderborg' in line or 'nach Sonderborg' in line or 'zu Sonderborg' in line:
                file_issues.append(f"Zeile {i}: 'Sonderborg' statt 'Sønderborg': {line.strip()[:80]}")
    
    # Check 7: "Richtung Heimat" (wrong departure direction)
    for i, line in enumerate(lines, 1):
        if 'Richtung Heimat' in line:
            file_issues.append(f"Zeile {i}: 'Richtung Heimat': {line.strip()[:80]}")
    
    # Check 8: "Pfoten auf seinen Händen" (inconsistent kerker moment)
    for i, line in enumerate(lines, 1):
        if 'Pfoten auf' in line and 'Händen' in line:
            file_issues.append(f"Zeile {i}: Inkonsistenter Kerker-Moment: {line.strip()[:80]}")
    
    # Check 9: "als würde man von einem Berggipfel" - this is actually fine (not animal)
    # Skip these as they're acceptable literary devices
    
    status = "✅ OK" if not file_issues else f"⚠️ {len(file_issues)} Probleme"
    print(f"\n{ep_file.name}: {status}")
    
    for issue in file_issues:
        print(f"  🔴 {issue}")
        issues_found += 1

print("\n" + "=" * 60)
print(f"📊 Ergebnis: {episodes_checked} Episoden geprüft, {issues_found} Probleme gefunden")
if issues_found == 0:
    print("🎉 ALLE KRITISCHEN FEHLER BESEITIGT!")
else:
    print(f"\n⚠️  {issues_found} verbleibende Probleme (meistens stilistische 'als würde'-Muster)")
print("=" * 60)
