#!/usr/bin/env python3
"""Fix the broken sentence in episode 6."""

from pathlib import Path

BASE = Path(__file__).parent / "episodes"

filepath = BASE / "episode_06_Omaknas_wienerbrod.md"
content = filepath.read_text(encoding='utf-8')

# Fix the broken concatenation on line 33
broken = ('Samson saß neben seinem Platz und schaute aufrecht wie ein kleiner Professor. '
          'Er wusste nicht genau, was passierte. Aber er spürte: Jetzt wurde es spannend! '
          'dann gibt es immer etwas für ihn – aber nur, wenn er sich gut benimmt.')

fixed = ('Samson saß neben seinem Platz und schaute aufrecht wie ein kleiner Professor. '
         'Er wusste nicht genau, was passierte. Aber er spürte: Jetzt wurde es spannend!')

if broken in content:
    content = content.replace(broken, fixed)
    filepath.write_text(content, encoding='utf-8')
    print("✅ Episode 6 Zeile 33 repariert!")
else:
    print("⚠️  Broken string not found - checking what's there...")
    # Try to find the line anyway
    for i, line in enumerate(content.splitlines(), 1):
        if 'Professor' in line and 'spannend' in line:
            print(f"  Zeile {i}: {line}")
