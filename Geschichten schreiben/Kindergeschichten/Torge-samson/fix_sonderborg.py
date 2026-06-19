#!/usr/bin/env python3
"""Fix remaining 'Sonderborg' -> 'Sønderborg' inconsistencies."""

from pathlib import Path

BASE = Path(__file__).parent / "episodes"

fixes = {
    "episode_01_Willkommen_in_Sonderborg.md": [
        ("Willkommen in Sonderborg!", "Willkommen in Sønderborg!"),
        ('„Willkommen in Sonderborg,', '"Willkommen in Sønderborg,'),
    ],
    "episode_06_Omaknas_wienerbrod.md": [
        ('Warum? Wir sind doch schon in Sonderborg!', 'Warum? Wir sind doch schon in Sønderborg!'),
        ('Weißt du noch, was Opa immer sagt? Die *Sonderborg-Regel*: Wenn man in Sonderborg ist,', 'Weißt du noch, was Opa immer sagt? Die *Sønderborg-Regel*: Wenn man in Sønderborg ist,'),
    ],
}

for filename, fix_list in fixes.items():
    filepath = BASE / filename
    content = filepath.read_text(encoding='utf-8')
    
    for old, new in fix_list:
        if old in content:
            content = content.replace(old, new)
            print(f"  ✅ {filename}: '{old[:40]}...' -> '{new[:40]}...'")
    
    filepath.write_text(content, encoding='utf-8')

print("\n✅ Alle 'Sonderborg' -> 'Sønderborg' Fixes angewendet!")
