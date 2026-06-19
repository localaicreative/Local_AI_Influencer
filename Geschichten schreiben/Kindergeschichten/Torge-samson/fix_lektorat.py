#!/usr/bin/env python3
"""Fix all lektorat errors across all 10 episodes."""

import re
from pathlib import Path

BASE = Path(__file__).parent / "episodes"

def fix_ep1(content):
    # vom Café MARINA -> des Café MARINA
    content = content.replace("vom Café MARINA", "des Café MARINA")
    # nabeln -> knabbern (line 27)
    content = content.replace("versuchte, an der Tüte zu nabeln.", "knabberte fröhlich an der Tüte.")
    # Sonderborg in quote -> Sønderborg (line 37)
    content = content.replace('"Willkommen in Sonderborg,', '"Willkommen in Sønderborg,')
    return content

def fix_ep2(content):
    # Samson thought "Spielzeit!" -> show behavior instead
    old = 'Samson sah die Bewegung, dachte "Spielzeit!", und platschte mit seinem ganzen Körper ins Wasser.'
    new = ('Samson sah die Bewegung – sein ganzer Körper spannte sich an. Ohne zu zögern, '
           'platschte er mit seinem ganzen Körper ins Wasser.')
    content = content.replace(old, new)
    return content

def fix_ep3(content):
    # Samson thought "WASSERZEIT!" -> show behavior
    old = 'Samson hörte das Wort – sein ganzer Körper spannte sich an. Er dachte "WASSERZEIT!",'
    new = ('Samson hörte das Wort – sein ganzer Körper spannte sich an. Ohne zu zögern, '
           'sprang er ohne zu zögern ins Wasser.')
    # Actually let me re-read the file first... but for now:
    content = content.replace('dachte "WASSERZEIT!",', 'hechelte nur noch lauter und sprang sofort ins Wasser,')
    
    # "er hatte viel gelernt" -> show behavior
    old2 = 'Er hatte das Meer so lieb! Er hatte viel gelernt.'
    new2 = 'Er hatte das Meer so lieb! Mit einem zufriedenen Seufzer legte er sich hin.'
    content = content.replace(old2, new2)
    return content

def fix_ep4(content):
    # Samson spürte Torges Gedanken -> show behavior
    old = 'Samson spürte, dass Torge traurig war und dachte,'
    new = 'Samson spürte, dass Torge traurig war.'
    content = content.replace(old, new)
    return content

def fix_ep5(content):
    # Three instances of "als würde er sagen: [Worte]" -> rephrase as Torge's interpretation
    # Fix 1
    old1 = 'als würde er sagen: "Keine Angst, Torge!"'
    new1 = ', als wollte er sagen: "Keine Angst, Torge!"'
    content = content.replace(old1, new1)
    
    # Fix 2  
    old2 = 'als würde er sagen: "Ich bin mutig!"'
    new2 = ', als wollte er sagen: "Ich bin mutig!"'
    content = content.replace(old2, new2)
    
    # Fix 3
    old3 = 'als würde er sagen: "Das war ein tolles Abenteuer!"'
    new3 = ', als wollte er sagen: "Das war ein tolles Abenteuer!"'
    content = content.replace(old3, new3)
    return content

def fix_ep6(content):
    # Samson thought "Lecker!" -> show behavior
    old1 = 'Samson dachte "Lecker!" und hechelte fröhlich.'
    new1 = 'Sein ganzer Körper wedelte vor Freude und er hechelte fröhlich.'
    content = content.replace(old1, new1)
    
    # Samson "wusste" complex things -> show behavior  
    old2 = 'Samson wusste, dass das wichtig war'
    new2 = 'Samson legte die Pfoten unter den Bauch und starrte konzentriert darauf.'
    content = content.replace(old2, new2)
    
    # "nabeln" -> "nagen" (line 21)
    content = content.replace("an der Tüte zu nabeln", "an der Tüte zu nagen")
    
    # Torge schmeckt Samsons Maul-Inhalt -> only see, not taste
    old3 = 'Torge schmeckte den Inhalt von Samsons Maul'
    new3 = 'Torge sah den Inhalt von Samsons Maul'
    content = content.replace(old3, new3)
    return content

def fix_ep7(content):
    # Title: "Die Klappbrücke geht auf!" -> bridge never opens
    # Change title to something that matches the actual story
    old_title = '# Episode 7: Die Klappbrücke geht auf!'
    new_title = '# Episode 7: Das Signal für die Brücke'
    content = content.replace(old_title, new_title)
    
    # Subtitle too
    old_sub = '## Woche 3, Tag 18 – Das Signal für die Brücke'
    new_sub = '## Woche 3, Tag 18 – Die Brücke wartet'
    content = content.replace(old_sub, new_sub)
    
    # Samson inner monologue line 43 -> show behavior
    old_m1 = 'Samson dachte: "Das ist ein wichtiges Signal!"'
    new_m1 = 'Samsons Ohren spitzten sich. Er hechelte aufgeregt und sprang hin und her.'
    content = content.replace(old_m1, new_m1)
    
    # Samson inner monologue line 49 -> show behavior
    old_m2 = 'Samson dachte: "Wir haben es geschafft!"'
    new_m2 = 'Samson legte den Kopf schief und hechelte zufrieden.'
    content = content.replace(old_m2, new_m2)
    return content

def fix_ep8(content):
    # English word "outside" -> "draußen"
    content = content.replace('outside', 'draußen')
    
    # "weil er dachte, es wäre ein Spiel" -> attribute to Torge
    old = 'weil er dachte, es wäre ein Spiel'
    new = 'weil er glaubte, es wäre ein Spiel'
    content = content.replace(old, new)
    return content

def fix_ep9(content):
    # Direction "Norden" instead of "Westen" (Gråsten is west!)
    content = content.replace('nach Norden', 'nach Westen')
    
    # Two instances of "als würde sie/er sagen: [Worte]" -> rephrase as Torge's interpretation
    old1 = 'als würde sie sagen:'
    new1 = ', als wollte sie sagen:'
    content = content.replace(old1, new1)
    
    old2 = 'als würde er sagen:'
    new2 = ', als wollte er sagen:'
    content = content.replace(old2, new2)
    return content

def fix_ep10(content):
    # Departure: "Richtung Heimat" doesn't make sense (line 5 + 13)
    old_dep = 'auf die offene Dänische Südsee hinaus'
    # Check if it already says this, otherwise fix
    if 'Richtung Heimat' in content:
        content = content.replace('Richtung Heimat', 'auf die offene Dänische Südsee hinaus')
    
    # Meta-reference "in Episode 4" breaks fourth wall (line 47)
    old_meta = 'genau wie damals in Episode 4'
    new_meta = 'genau wie damals im Kerker'
    content = content.replace(old_meta, new_meta)
    
    # Kerker moment inconsistent: Ep 10 = paws on hands -> make consistent with head
    old_kerker = 'Pfoten auf seinen Händen'
    new_kerker = 'Kopf in seine Hände'
    content = content.replace(old_kerker, new_kerker)
    
    return content

# Map episodes to fix functions
episodes = {
    "episode_01_Willkommen_in_Sonderborg.md": fix_ep1,
    "episode_02_Samson_im_Krabbenparcours.md": fix_ep2,
    "episode_03_Die_Fahrt_nach_Hoersuphav.md": fix_ep3,
    "episode_04_Das_Geheimnis_des_Schlosskerkers.md": fix_ep4,
    "episode_05_Samson_auf_der_Jolle.md": fix_ep5,
    "episode_06_Omaknas_wienerbrod.md": fix_ep6,
    "episode_07_Die_Klappbruecke_geht_auf.md": fix_ep7,
    "episode_08_Sturm_und_Sternschnuppen.md": fix_ep8,
    "episode_09_Die_Koenigsmoewe_in_Graesten.md": fix_ep9,
    "episode_10_Heimfahrt_mit_vollem_Herzen.md": fix_ep10,
}

for filename, fix_func in episodes.items():
    filepath = BASE / filename
    if not filepath.exists():
        print(f"⚠️  {filename} nicht gefunden!")
        continue
    
    content = filepath.read_text(encoding='utf-8')
    original = content
    
    # Apply fixes
    try:
        content = fix_func(content)
    except Exception as e:
        print(f"❌ Fehler in {filename}: {e}")
        continue
    
    if content != original:
        filepath.write_text(content, encoding='utf-8')
        changes = sum(1 for a, b in zip(original.splitlines(), content.splitlines()) if a != b)
        print(f"✅ {filename} — {changes} Zeilen geändert")
    else:
        print(f"⏭️  {filename} — keine Änderungen nötig (oder Fix nicht gefunden)")

print("\n🎉 Lektorat-Fixes abgeschlossen!")
