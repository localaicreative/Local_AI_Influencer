#!/usr/bin/env python3
"""Final comprehensive fix for all remaining lektorat errors."""

from pathlib import Path

BASE = Path(__file__).parent / "episodes"

def fix_ep3(content):
    # Line 37: Samson thinking about WASSERZEIT -> show behavior
    old1 = 'Samson hatte den Badesteg noch nie gesehen – und für ihn bedeutete das nur eines: WASSERZEIT!'
    new1 = ('Samson hatte den Badesteg noch nie gesehen. Sein ganzer Körper spannte sich an, '
            'sein Schwanz wedelte wild – er wollte ins Wasser!')
    if old1 in content:
        content = content.replace(old1, new1)
        print("  ✅ Ep3: WASSERZEIT-Gedanke -> Verhalten")
    
    # Line 55: "auch er hatte heute viel gelernt" -> show behavior
    old2 = 'auch er hatte heute viel gelernt.'
    new2 = 'auch er war heute müde und zufrieden.'
    if old2 in content:
        content = content.replace(old2, new2)
        print("  ✅ Ep3: 'viel gelernt' -> Verhalten")
    
    return content

def fix_ep4(content):
    # Line 61: Samson spürte Torges Gedanken -> show behavior
    old1 = 'aber er spürte, dass Torge etwas Wichtiges dachte.'
    new1 = 'aber er spürte, dass Torge nachdachte. Also setzte er sich neben ihn und legte seinen warmen Kopf auf Torges Knie.'
    if old1 in content:
        content = content.replace(old1, new1)
        print("  ✅ Ep4: Samsons Gedanken-Spüren -> Verhalten")
    
    # Line 45/65: "einsam/Einsamkeit" too abstract for 6-year-olds
    old2 = 'furchtbar einsam'
    new2 = 'ganz allein und traurig'
    if old2 in content:
        content = content.replace(old2, new2)
        print("  ✅ Ep4: 'einsam' vereinfacht")
    
    old3 = 'Einsamkeit ist nicht das Schlimmste'
    new3 = 'Allein sein ist nicht das Schlimmste'
    if old3 in content:
        content = content.replace(old3, new3)
        print("  ✅ Ep4: 'Einsamkeit' vereinfacht")
    
    return content

def fix_ep5(content):
    # Four instances of "als würde er sagen:" -> rephrase as Torge's interpretation
    
    fixes = [
        ('als würde er sagen: *Das war einfach!*', ', als wollte er sagen: *Das war einfach!*'),
        ('als würde er sagen: *Das ist unser Boot!*', ', als wollte er sagen: *Das ist unser Boot!*'),
        ('als würde er sagen: *Das war toll!*', ', als wollte er sagen: *Das war toll!*'),
        ('als würde er sagen: *Noch mal! Noch mal!*', ', als wollte er sagen: *Noch mal! Noch mal!*'),
    ]
    
    for old, new in fixes:
        if old in content:
            content = content.replace(old, new)
            print("  ✅ Ep5: Samson-Sagen -> Interpretation")
    
    return content

def fix_ep6(content):
    # Line 21: "nabeln" -> "nagen" (different context than expected!)
    old1 = 'an Opas Hand zu nabeln'
    new1 = 'an Opas Hand zu nagen'
    if old1 in content:
        content = content.replace(old1, new1)
        print("  ✅ Ep6: nabeln -> nagen")
    
    # Line 33: Samson "wusste" complex things -> show behavior  
    old2 = 'Er wusste: Wenn Oma backt,'
    new2 = 'Er wusste nicht genau, was passierte. Aber er spürte: Jetzt wurde es spannend!'
    if old2 in content:
        content = content.replace(old2, new2)
        print("  ✅ Ep6: Samsons Wissen -> Verhalten")
    
    # Line 47: "als würde er sagen: *Lecker!*" -> rephrase as Torge's interpretation
    old3 = 'als würde er sagen: *Lecker!*'
    new3 = ', als wollte er sagen: *Lecker!*'
    if old3 in content:
        content = content.replace(old3, new3)
        print("  ✅ Ep6: Samson-Sagen Lecker -> Interpretation")
    
    # Line 63: Torge schmeckt Samsons Maul-Inhalt (unphysikalisch)
    old4 = 'schmeckte wie ein Traum!'
    new4 = 'sah aus wie ein Traum!'
    if old4 in content:
        content = content.replace(old4, new4)
        print("  ✅ Ep6: schmecken -> sehen")
    
    return content

def fix_ep7(content):
    # Line 23: Möwen "als würden sie sagen:" -> rephrase as Torge's interpretation
    old1 = 'als würden sie sagen: *Hallo, kleiner Hund!*'
    new1 = ', als wollte er meinen: *Hallo, kleiner Hund!*'
    if old1 in content:
        content = content.replace(old1, new1)
        print("  ✅ Ep7: Möwen-Sagen #1 -> Interpretation")
    
    # Line 35: Möwe "als würde sie sagen:" -> rephrase as Torge's interpretation
    old2 = 'als würde sie sagen: *Na, na, kleiner Hund, nicht so laut!*'
    new2 = ', als wollte er meinen: *Na, na, kleiner Hund, nicht so laut!*'
    if old2 in content:
        content = content.replace(old2, new2)
        print("  ✅ Ep7: Möwen-Sagen #2 -> Interpretation")
    
    return content

def fix_ep8(content):
    # Already mostly clean from first script. Check for remaining issues
    
    # Line 57: "als würde er tanzen wollen" - Samson behavior, this is fine (it's Torge's interpretation)
    # No changes needed if already fixed
    
    return content

def fix_ep9(content):
    # Multiple instances of "als wollte sie/er sagen:" -> rephrase as Torge's interpretation
    
    fixes = [
        ('als wollte sie sagen: *Ich bin hier die Chefin!*', ', als dachte er: *Die ist wohl die Chefin!*'),
        ('als wollte er sagen: *Hallo, große Möwe!*', ', als dachte er: *Hallo, große Möwe!*'),
        ('als wollte sie sagen: *Ich bleibe hier, weil du nett bist!*', ', als dachte er: *Sie bleibt hier, weil wir nett sind!*'),
        ('als wollte sie sagen: *Das ist nett.*', ', als dachte er: *Das gefällt ihr!*'),
        ('als wollte er sagen: *Ich habe eine neue Freundin!*', ', als dachte er: *Ich hab wohl eine neue Freundin!*'),
    ]
    
    for old, new in fixes:
        if old in content:
            content = content.replace(old, new)
            print("  ✅ Ep9: Möwen/Samson-Sagen -> Torges Interpretation")
    
    return content

def fix_ep10(content):
    # Line 19: Samson "als würde er sagen:" -> rephrase as Torge's interpretation
    old1 = 'als würde er sagen: *Ja, ja!*'
    new1 = ', als dachte er: *Ja, genau!*'
    if old1 in content:
        content = content.replace(old1, new1)
        print("  ✅ Ep10: Samson-Sagen #1 -> Interpretation")
    
    # Line 35: Samson "als würde er sagen:" -> rephrase as Torge's interpretation
    old2 = 'als würde er sagen: *Und es gab noch mehr!*'
    new2 = ', als dachte er: *Und es gab noch viel mehr!*'
    if old2 in content:
        content = content.replace(old2, new2)
        print("  ✅ Ep10: Samson-Sagen #2 -> Interpretation")
    
    # Line 47: Meta-reference "in Episode 4" breaks fourth wall
    old3 = 'genau wie in Episode 4'
    new3 = 'genau wie damals im Kerker'
    if old3 in content:
        content = content.replace(old3, new3)
        print("  ✅ Ep10: Episode-Referenz entfernt")
    
    # Line 59: Samson "als würde er sagen:" -> rephrase as Torge's interpretation
    old4 = 'als würde er sagen: *Ich weiß!*'
    new4 = ', als dachte er: *Das weiß ich auch!*'
    if old4 in content:
        content = content.replace(old4, new4)
        print("  ✅ Ep10: Samson-Sagen #3 -> Interpretation")
    
    return content

# Map episodes to fix functions
episodes = {
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

print("\n🎉 Alle Lektorat-Fixes abgeschlossen!")
