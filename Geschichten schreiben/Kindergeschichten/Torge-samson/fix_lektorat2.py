#!/usr/bin/env python3
"""Fix all lektorat errors across episodes 2-6 and remaining issues."""

from pathlib import Path

BASE = Path(__file__).parent / "episodes"

def fix_ep2(content):
    # Line 17: Samson thought "Spielzeit!" -> show behavior instead
    old = 'Samson sah die Bewegung, dachte „Spielzeit!", und platschte mit seinem ganzen Körper ins Wasser.'
    new = ('Samson sah die Bewegung – sein ganzer Körper spannte sich an. Ohne zu zögern, '
           'platschte er mit seinem ganzen Körper ins Wasser.')
    if old in content:
        content = content.replace(old, new)
        print("  ✅ Ep2: Samson dachte -> Verhalten")
    else:
        print("  ⚠️  Ep2: Suchstring nicht gefunden")
    return content

def fix_ep3(content):
    # Line 37: Samson thought "WASSERZEIT!" -> show behavior
    old1 = 'dachte „WASSERZEIT!",'
    if old1 in content:
        content = content.replace(old1, 'hechelte nur noch lauter und sprang sofort ins Wasser,')
        print("  ✅ Ep3: Samson dachte WASSERZEIT -> Verhalten")
    
    # Line 55: "er hatte viel gelernt" -> show behavior
    old2 = 'Er hatte das Meer so lieb! Er hatte viel gelernt.'
    new2 = 'Er hatte das Meer so lieb! Mit einem zufriedenen Seufzer legte er sich hin.'
    if old2 in content:
        content = content.replace(old2, new2)
        print("  ✅ Ep3: 'viel gelernt' -> Verhalten")
    
    return content

def fix_ep4(content):
    # Line 61: Samson spürte Torges Gedanken -> show behavior
    old = 'Samson spürte, dass Torge traurig war und dachte,'
    new = 'Samson spürte, dass Torge traurig war.'
    if old in content:
        content = content.replace(old, new)
        print("  ✅ Ep4: Samsons Gedanken -> Verhalten")
    
    # Line 65: "Einsamkeit" too abstract for 6-year-olds
    old2 = 'Eine tiefe Einsamkeit'
    new2 = 'Ein trauriges Gefühl'
    if old2 in content:
        content = content.replace(old2, new2)
        print("  ✅ Ep4: 'Einsamkeit' vereinfacht")
    
    return content

def fix_ep5(content):
    # Three instances of "als würde er sagen: [Worte]" -> rephrase as Torge's interpretation
    
    # Fix 1 - line 23
    old1 = 'als würde er sagen: "Keine Angst, Torge!"'
    new1 = ', als wollte er sagen: "Keine Angst, Torge!"'
    if old1 in content:
        content = content.replace(old1, new1)
        print("  ✅ Ep5: Samson-Sagen #1 -> Interpretation")
    
    # Fix 2 - line 33
    old2 = 'als würde er sagen: "Ich bin mutig!"'
    new2 = ', als wollte er sagen: "Ich bin mutig!"'
    if old2 in content:
        content = content.replace(old2, new2)
        print("  ✅ Ep5: Samson-Sagen #2 -> Interpretation")
    
    # Fix 3 - line 45
    old3 = 'als würde er sagen: "Das war ein tolles Abenteuer!"'
    new3 = ', als wollte er sagen: "Das war ein tolles Abenteuer!"'
    if old3 in content:
        content = content.replace(old3, new3)
        print("  ✅ Ep5: Samson-Sagen #3 -> Interpretation")
    
    return content

def fix_ep6(content):
    # Line 47: Samson thought "Lecker!" -> show behavior
    old1 = 'Samson dachte „Lecker!" und hechelte fröhlich.'
    new1 = 'Sein ganzer Körper wedelte vor Freude und er hechelte fröhlich.'
    if old1 in content:
        content = content.replace(old1, new1)
        print("  ✅ Ep6: Samson dachte Lecker -> Verhalten")
    
    # Line 33: Samson "wusste" complex things -> show behavior  
    old2 = 'Samson wusste, dass das wichtig war'
    new2 = 'Samson legte die Pfoten unter den Bauch und starrte konzentriert darauf.'
    if old2 in content:
        content = content.replace(old2, new2)
        print("  ✅ Ep6: Samsons Wissen -> Verhalten")
    
    # Line 21: "nabeln" -> "nagen" (already fixed? check)
    if 'an der Tüte zu nabeln' in content:
        content = content.replace('an der Tüte zu nabeln', 'an der Tüte zu nagen')
        print("  ✅ Ep6: nabeln -> nagen")
    
    # Line 63: Torge schmeckt Samsons Maul-Inhalt -> only see, not taste
    old3 = 'Torge schmeckte den Inhalt von Samsons Maul'
    new3 = 'Torge sah den Inhalt von Samsons Maul'
    if old3 in content:
        content = content.replace(old3, new3)
        print("  ✅ Ep6: schmecken -> sehen")
    
    return content

def fix_ep7(content):
    # Title already fixed. Check for remaining issues
    
    # Line 43: Samson inner monologue -> show behavior
    old_m1 = 'Samson dachte: "Das ist ein wichtiges Signal!"'
    new_m1 = 'Samsons Ohren spitzten sich. Er hechelte aufgeregt und sprang hin und her.'
    if old_m1 in content:
        content = content.replace(old_m1, new_m1)
        print("  ✅ Ep7: Samson-Gedanke #1 -> Verhalten")
    
    # Line 49: Samson inner monologue -> show behavior
    old_m2 = 'Samson dachte: "Wir haben es geschafft!"'
    new_m2 = 'Samson legte den Kopf schief und hechelte zufrieden.'
    if old_m2 in content:
        content = content.replace(old_m2, new_m2)
        print("  ✅ Ep7: Samson-Gedanke #2 -> Verhalten")
    
    return content

def fix_ep8(content):
    # Line 41: "weil er dachte" -> "weil er glaubte" (already fixed?)
    if 'weil er dachte, es wäre ein Spiel' in content:
        content = content.replace('weil er dachte, es wäre ein Spiel', 'weil er glaubte, es wäre ein Spiel')
        print("  ✅ Ep8: dachte -> glaubte")
    
    # Line 15: English "outside" -> German (already fixed?)
    if 'outside' in content.lower():
        content = content.replace('outside', 'draußen')
        print("  ✅ Ep8: outside -> draußen")
    
    return content

def fix_ep9(content):
    # Direction already fixed. Check remaining issues
    
    # Line 41: "als würde sie sagen:" -> rephrase (already partially fixed)
    if 'als würde sie sagen:' in content:
        content = content.replace('als würde sie sagen:', ', als wollte sie sagen:')
        print("  ✅ Ep9: Möwe-Sagen #1 -> Interpretation")
    
    # Line 63: "als würde er sagen:" -> rephrase (already partially fixed)
    if 'als würde er sagen:' in content:
        content = content.replace('als würde er sagen:', ', als wollte er sagen:')
        print("  ✅ Ep9: Samson-Sagen #2 -> Interpretation")
    
    return content

def fix_ep10(content):
    # Line 5+13: "Richtung Heimat" -> correct departure direction (already fixed?)
    if 'Richtung Heimat' in content:
        content = content.replace('Richtung Heimat', 'auf die offene Dänische Südsee hinaus')
        print("  ✅ Ep10: Richtung Heimat -> Dänische Südsee")
    
    # Line 47: Meta-reference "in Episode 4" (already fixed?)
    if 'genau wie damals in Episode 4' in content:
        content = content.replace('genau wie damals in Episode 4', 'genau wie damals im Kerker')
        print("  ✅ Ep10: Episode-Referenz entfernt")
    
    # Line 51: Kerker moment inconsistent (already fixed?)
    if 'Pfoten auf seinen Händen' in content:
        content = content.replace('Pfoten auf seinen Händen', 'Kopf in seine Hände')
        print("  ✅ Ep10: Pfoten -> Kopf (Kerker-Konsistenz)")
    
    return content

# Map episodes to fix functions
episodes = {
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
        import traceback
        traceback.print_exc()
        continue
    
    if content != original:
        filepath.write_text(content, encoding='utf-8')
        changes = sum(1 for a, b in zip(original.splitlines(), content.splitlines()) if a != b)
        print(f"✅ {filename} — {changes} Zeilen geändert\n")
    else:
        print(f"⏭️  {filename} — keine Änderungen nötig (oder Fix nicht gefunden)\n")

print("\n🎉 Lektorat-Fixes abgeschlossen!")
