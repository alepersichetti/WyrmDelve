#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WyrmDelve v0.0.1 - random dungeons and labyrinths for OSR games, all in ASCII.

WyrmHex's sibling. It looks like an old roguelike (NetHack, Angband, ADOM,
Brogue, Caves of Qud, Dwarf Fortress). Every dungeon has a layered history
(natural caves, the founders, later occupants, today's inhabitants) that
shows in its walls: ═║ founders, ─│ second age, # caves and crude tunnels.
Rooms are numbered level-room: 1-01, 2-07, and 1a-01 on a sub-level.

Every level is one of 11 dungeon types (palace, prison, tower, castle,
temple, city, arcane laboratory, academy, border fortress, tomb, Underdark),
each with its own floor plan, rooms, builders and entrances. The levels
stack coherently: a tower stands above a castle, never below a cave.

The layout always follows Jennell Jaquays' principles as described by Justin
Alexander ("Xandering the Dungeon"): multiple entrances, loops, multiple and
discontinuous level connections, secret and unusual paths, sub-levels,
divided levels, minor elevation shifts, midpoint entries, nested complexes.

Prints on A4, A3, A2 or A1 at 600 dpi; the best paper is suggested. All
levels go on one sheet, or one level per sheet; PNG files or a PDF. Three
colour schemes: black on white, white on light blue, white on black.

Output goes to dungeons_generated/<seed>/ next to this file (or --output):
  <seed>_gm.png/.txt        game master map: room numbers and secrets
  <seed>_players.png/.txt   same map without numbers and secrets
  <seed>_key.txt            history, room key, level connections, Jaquays check
  <seed>_story.pdf          the same key as an A4 book page (Sebaldus-Gotisch headings, Crimson Text)
All fonts come from the fonts/ folder next to this file.
One level per sheet adds the level to the PNG names (<seed>_gm_L1.png ...);
with PDF every map is a single <seed>_gm.pdf / <seed>_players.pdf.

The seed (e.g. 3-24-2-5-CDK-K7Q2MB = levels-rooms-entrances-secrets-types-code)
holds the whole dungeon: the same seed always gives the same dungeon. Types
are one letter per level, A-K in menu order (one letter = every level).

Usage. Every option has an Italian and an English name, use whichever:
  python wyrmdelve.py                                interactive
  python wyrmdelve.py --livelli 3 --stanze 24       / --levels 3 --rooms 24
  python wyrmdelve.py --ingressi 3 --segreti 6      / --entrances 3 --secrets 6
  python wyrmdelve.py --colori 2                    / --colors 2
      (1 black on white, 2 white on light blue, 3 white on black)
  python wyrmdelve.py --tipo 3,4,11                 / --type 3,4,11  (tower, castle, Underdark)
  python wyrmdelve.py --seme 3-24-2-5-CDK-K7Q2MB    / --seed 3-24-2-5-CDK-K7Q2MB
  python wyrmdelve.py --formato A2                  / --format A2
  python wyrmdelve.py --per-livello                 / --per-level  (one level per sheet)
  python wyrmdelve.py --un-foglio                   / --one-sheet  (all levels on one sheet)
  python wyrmdelve.py --pdf                         / --png
  python wyrmdelve.py --titolo "La Tana dell'Orco"  / --title "The Ogre's Lair"
  python wyrmdelve.py --senza-titolo                / --no-title  (map without a name)
  python wyrmdelve.py --senza-storia                / --no-story  (only the maps, no key and no story PDF)
  python wyrmdelve.py --solo-ascii                  / --ascii-only
  python wyrmdelve.py --lingua en                   / --language en  (default: Italian)
  python wyrmdelve.py --help
Parameters you leave out are chosen at random.

Code and comments are in English, the UI is Italian or English. The words
the dungeons are made of (dungeon types and how they stack, names,
builders, occupants, rooms, events, entrances, history) are data, not code:
they live in wyrmdelve_tables.json.
"""

import argparse
import heapq
import json
import math
import os
import random
import string
import sys
import time
import zlib
from collections import Counter, deque

try:
    from PIL import Image, ImageDraw, ImageFont
    from PIL.PngImagePlugin import PngInfo
except ImportError:
    sys.exit("Manca la libreria Pillow. Installala con:  pip install -r requirements.txt\n"
             "Pillow is missing. Install it with:   pip install -r requirements.txt")

# A1 at 600 dpi is ~279 Mpx, way over Pillow's decompression bomb limit.
# They're our own maps, so just turn the check off.
Image.MAX_IMAGE_PIXELS = None


# --- settings ---

VERSION = "0.0.1"
DPI = 600
MARGIN_MM = 10.0
MAX_CHAR_MM = 3.2           # cap on A4; bigger sheets scale it up
GOOD_CHAR_MM = 1.3          # readable
SMALL_CHAR_MM = 1.1         # too small below this
PAPERS = {"A4": (210, 297), "A3": (297, 420), "A2": (420, 594), "A1": (594, 841)}
SETTINGS_KEY = "wyrmdelve-settings"

# (ink, paper) in RGB. Change the light blue here if your printer wants another shade.
COLOR_SCHEMES = {
    1: ((0, 0, 0), (255, 255, 255)),          # black symbols on white
    2: ((255, 255, 255), (72, 156, 214)),     # white symbols on light blue
    3: ((255, 255, 255), (0, 0, 0)),          # white symbols on black
}

MIN_PER_LEVEL = 5          # rooms on every main level
LOOP_ROOMS = 3             # a loop needs 3 rooms: the least for a sub-level or half a divided level
LIMITS = {"levels": (1, 10), "rooms": (MIN_PER_LEVEL, 200), "entrances": (1, 9), "secrets": (0, 60)}
DEFAULTS = {"levels": 3, "rooms": 20, "entrances": 2, "secrets": 4}

# Each level is a grid of slots; a slot holds at most one room. Letters are
# about twice as tall as wide, so 24 x 11 letters is roughly square on paper.
SLOT_W, SLOT_H = 24, 11
ASPECT_GUESS = 2.0          # used while generating, so the dungeon never depends on the font
PANEL_MX = 4                # letters left and right of a level, room for the [A] entrance tags
GAP_X, GAP_Y = 3, 1         # between level panels on the page

MONO_FONTS = [
    ("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
     "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"),
    (("/System/Library/Fonts/Menlo.ttc", 0), ("/System/Library/Fonts/Menlo.ttc", 1)),   # macOS
    ("/System/Library/Fonts/Supplemental/Courier New.ttf",                    # macOS
     "/System/Library/Fonts/Supplemental/Courier New Bold.ttf"),
    ("C:/Windows/Fonts/consola.ttf", "C:/Windows/Fonts/consolab.ttf"),       # Windows
    ("/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf",
     "/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf"),
]


def mm(value):
    return value / 25.4 * DPI


# --- language ---
# Everything the user reads is (it, en). LANG is set once at startup,
# from the first question or from --lingua/--language.
LANGUAGES = ("it", "en")
LANG = "it"

TEXTS = {
    # console: general
    "done": ("Completato in {s:.1f} s.", "Done in {s:.1f} s."),
    "interrupted": ("\n\nInterrotto.", "\n\nStopped."),
    "invalid_value": ("    Valore non valido, riprova.", "    Invalid value, try again."),
    "value_range": ("    Il valore deve essere tra {lo} e {hi}.", "    The value must be between {lo} and {hi}."),
    # welcome
    "welcome_subtitle": ("generatore di dungeon e labirinti per campagne OSR",
                         "dungeon and labyrinth generator for OSR campaigns"),
    "press_enter": ("  INVIO = dungeon casuale   ·   P = scelgo io i parametri   ·   R = rifaccio un dungeon dal seme: ",
                    "  ENTER = random dungeon   ·   P = I'll choose the parameters   ·   R = rebuild a dungeon from its seed: "),
    "letter_params": ("p", "p"),
    "letter_rebuild": ("r", "r"),
    "orc_says": ("L'orco apre la porta del dungeon...", "The ogre opens the dungeon door..."),
    "enter_accepts": ("  Premi Invio per accettare il valore tra parentesi\n",
                      "  Press Enter to accept the value in brackets\n"),
    "q_levels": ("Numero di livelli del dungeon", "Number of dungeon levels"),
    "q_rooms": ("Numero di stanze (almeno 5 per livello)", "Number of rooms (at least 5 per level)"),
    "q_entrances": ("Numero di ingressi/uscite dall'area", "Number of entrances/exits to the area"),
    "q_secrets": ("Numero di porte e passaggi segreti", "Number of secret doors and passages"),
    "ask_seed": ("  Seme del dungeon da rifare (è anche il nome della sua cartella, es. {example}): ",
                 "  Seed of the dungeon to rebuild (it is also the name of its folder, e.g. {example}): "),
    "seed_invalid": ("    Questo seme non è valido: controlla di averlo scritto bene (es. {example}).",
                     "    This seed is not valid: check that you typed it correctly (e.g. {example})."),
    "colors_intro": ("\n  Combinazione di colori:", "\n  Colour scheme:"),
    "color_1": ("    1 = simboli neri su sfondo bianco", "    1 = black symbols on white"),
    "color_2": ("    2 = simboli bianchi su sfondo celeste", "    2 = white symbols on light blue"),
    "color_3": ("    3 = simboli bianchi su sfondo nero", "    3 = white symbols on black"),
    "choice": ("Scelta", "Choice"),
    "types_same_intro": ("\n  I livelli sono tutti dello stesso tipo?", "\n  Are all levels of the same type?"),
    "types_same": ("    1 = sì, stesso tipo per tutti", "    1 = yes, the same type for all"),
    "types_each": ("    2 = no, ogni livello ha il suo tipo", "    2 = no, each level has its own type"),
    "types_intro": ("\n  Tipo di dungeon:", "\n  Dungeon type:"),
    "types_level_intro": ("\n  Tipo del livello {n} (sotto: {above}):", "\n  Type of level {n} (below: {above}):"),
    "types_level_first": ("\n  Tipo del livello 1 (il più in alto):", "\n  Type of level 1 (the top one):"),
    "type_random": ("     0 = a caso", "     0 = at random"),
    "type_not_allowed": ("    Questo tipo non può stare lì sotto: scegline uno dell'elenco.",
                         "    This type can't go down there: choose one from the list."),
    "name_intro": ("\n  Vuoi un nome per la mappa del dungeon?", "\n  Do you want a name on the dungeon map?"),
    "name_yes": ("    1 = sì", "    1 = yes"),
    "name_no": ("    2 = no, mappa senza nome", "    2 = no, a map without a name"),
    "name_how": ("\n  Come scegliere il nome?", "\n  How should the name be chosen?"),
    "name_random": ("    1 = generato a caso", "    1 = randomly generated"),
    "name_mine": ("    2 = lo scelgo io", "    2 = I'll choose it"),
    "q_name": ("  Nome della mappa: ", "  Map name: "),
    "name_empty": ("    Scrivi un nome.", "    Type a name."),
    "content_intro": ("\n  Cosa vuoi generare?", "\n  What do you want to make?"),
    "content_1": ("    1 = solo le mappe", "    1 = only the maps"),
    "content_2": ("    2 = mappe e storia (chiave delle stanze in PDF e TXT)", "    2 = maps and story (room key as PDF and TXT)"),
    "content_3": ("    3 = mappe e mostri (tabelle dei mostri erranti, mostri e indizi nelle stanze)",
                  "    3 = maps and monsters (wandering monster tables, monsters and clues in the rooms)"),
    "content_4": ("    4 = mappe, storia e mostri", "    4 = maps, story and monsters"),
    "units_intro": ("\n  Unità di misura della griglia (ogni lettera della mappa è una casella)?",
                    "\n  Grid units (every letter of the map is one square)?"),
    "units_1": ("    1 = imperiale (piedi): 1 casella = 5 ft", "    1 = imperial (feet): 1 square = 5 ft"),
    "units_2": ("    2 = metrica (metri): 1 casella = 1,5 m", "    2 = metric (meters): 1 square = 1.5 m"),
    # parameter names and checks
    "name_levels": ("livelli", "levels"),
    "name_rooms": ("stanze", "rooms"),
    "name_entrances": ("ingressi", "entrances"),
    "name_secrets": ("segreti", "secrets"),
    "err_range": ("Il numero di {what} deve essere tra {lo} e {hi}.", "The number of {what} must be between {lo} and {hi}."),
    "err_rooms_levels": ("Con {l} livelli servono almeno {n} stanze (almeno 5 per livello).",
                         "{l} levels need at least {n} rooms (at least 5 per level)."),
    "err_entrances": ("Gli ingressi non possono essere più delle stanze.",
                      "There can't be more entrances than rooms."),
    "err_seed": ("Seme non valido: {s}", "Invalid seed: {s}"),
    "err_types_count": ("Hai indicato {n} tipi per {l} livelli: indicane uno solo (per tutti) o uno per livello.",
                        "You gave {n} types for {l} levels: give just one (for all) or one per level."),
    "err_types_order": ("Il livello {i} ({a}) non può stare sopra il livello {j} ({b}).",
                        "Level {i} ({a}) can't stand above level {j} ({b})."),
    "err_type_value": ("Tipo di dungeon non valido: {s} (usa numeri da 1 a {n}, separati da virgole).",
                       "Invalid dungeon type: {s} (use numbers from 1 to {n}, separated by commas)."),
    "err_no_font": ("Nessun font monospazio trovato: controlla che la cartella fonts sia accanto a wyrmdelve.py, "
                    "oppure indica un file .ttf con --font (es. DejaVuSansMono.ttf).",
                    "No monospaced font found. Give a .ttf file with --font (e.g. DejaVuSansMono.ttf)."),
    "err_size": ("{path}: {size} non è un foglio A4, A3, A2 o A1 a 600 dpi",
                 "{path}: {size} is not an A4, A3, A2 or A1 sheet at 600 dpi"),
    "err_units": ("«{s}» non è un'unità: usa imperiale o metrica", "“{s}” is not a unit: use imperial or metric"),
    "err_build": ("Non riesco a costruire un dungeon con questi parametri, prova con un altro seme.",
                  "Cannot build a dungeon with these settings, try another seed."),
    # steps
    "step_settings": ("Impostazioni", "Settings"),
    "info_seed": ("Seme: {s}", "Seed: {s}"),
    "info_params": ("{l} livelli, {r} stanze, {e} ingressi, {x} porte/passaggi segreti",
                    "{l} levels, {r} rooms, {e} entrances, {x} secret doors/passages"),
    "info_random": ("Parametri scelti a caso", "Parameters chosen at random"),
    "info_types": ("Tipo di dungeon: {t}", "Dungeon type: {t}"),
    "types_all": (" (tutti i livelli)", " (every level)"),
    "info_colors": ("Colori: {c}", "Colours: {c}"),
    "info_name_mine": ("Nome della mappa: «{t}»", "Map name: “{t}”"),
    "info_name_none": ("Mappa senza nome", "Map without a name"),
    "info_content_1": ("Solo le mappe", "Only the maps"),
    "info_content_2": ("Mappe e storia", "Maps and story"),
    "info_content_3": ("Mappe e mostri", "Maps and monsters"),
    "info_content_4": ("Mappe, storia e mostri", "Maps, story and monsters"),
    "info_units": ("Griglia: {s}", "Grid: {s}"),
    "info_folder": ("Cartella: {folder}", "Folder: {folder}"),
    "info_font": ("Font: {name}{fake}, cella {a:.2f} volte più alta che larga",
                  "Font: {name}{fake}, letter cell {a:.2f} times taller than wide"),
    "fake_bold": (" (grassetto simulato)", " (fake bold)"),
    "step_story": ("Storia a strati", "Layered history"),
    "info_title": ("«{t}»", "“{t}”"),
    "step_rooms": ("Stanze e strati", "Rooms and strata"),
    "info_level_rooms": ("Livello {n} ({t}): {r} stanze{extra}", "Level {n} ({t}): {r} rooms{extra}"),
    "info_divided": (" (diviso in due)", " (divided in two)"),
    "info_sub": (" (sottolivello)", " (sub-level)"),
    "step_corridors": ("Corridoi e anelli", "Corridors and loops"),
    "info_corridors": ("{c} corridoi, di cui {l} chiudono un anello", "{c} corridors, {l} of them close a loop"),
    "step_links": ("Collegamenti tra livelli e ingressi", "Level connections and entrances"),
    "info_links": ("{s} scale, {p} pozzi, {g} portali; {e} ingressi", "{s} stairs, {p} shafts, {g} portals; {e} entrances"),
    "step_secrets": ("Passaggi segreti e insoliti", "Secret and unusual paths"),
    "info_secrets": ("{d} porte segrete, {p} passaggi segreti, {h} scale/pozzi nascosti, {w} allagati, {r} crolli, "
                     "{s} dislivelli",
                     "{d} secret doors, {p} secret passages, {h} hidden stairs/shafts, {w} flooded, {r} cave-ins, "
                     "{s} elevation shifts"),
    "warn_secrets": ("Solo {n} segreti possibili su {want} richiesti: mancano corridoi adatti.",
                     "Only {n} secrets possible out of {want}: not enough suitable corridors."),
    "step_check": ("Verifica dei principi di Jaquays", "Checking Jaquays' principles"),
    "info_reach": ("Tutte le {n} stanze sono raggiungibili", "All {n} rooms can be reached"),
    "info_retry": ("Tentativo {n} non riuscito, ricostruisco", "Attempt {n} failed, building again"),
    "step_paper": ("Formato di stampa", "Print format"),
    "info_paper_intro": ("Il dungeon occupa {nc} x {nr} caratteri. Formati possibili:",
                         "The dungeon takes {nc} x {nr} letters. Possible formats:"),
    "info_paper_option": ("{paper}  {o:<11}  livelli {pc}x{pr}   caratteri da {mm:.2f} mm   {v}{note}",
                          "{paper}  {o:<9}  levels {pc}x{pr}   {mm:.2f} mm letters   {v}{note}"),
    "v_good": ("leggibile", "readable"),
    "v_small": ("piccolo", "small"),
    "v_too_small": ("troppo piccolo", "too small"),
    "suggested": ("   <- consigliato", "   <- suggested"),
    "paper_choice": ("  Scegli il formato (premi Invio per quello consigliato).",
                     "  Choose the format (press Enter for the suggested one)."),
    "q_paper": ("  Formato di stampa (A4, A3, A2, A1) [{default}]: ", "  Print format (A4, A3, A2, A1) [{default}]: "),
    "paper_retry": ("    Scrivi A4, A3, A2 oppure A1.", "    Type A4, A3, A2 or A1."),
    "sheets_intro": ("\n  Come impaginare i livelli?", "\n  How should the levels be laid out?"),
    "sheets_1": ("    1 = tutti i livelli in un solo foglio", "    1 = all levels on one sheet"),
    "sheets_2": ("    2 = un livello per foglio, su file separati", "    2 = one level per sheet, in separate files"),
    "output_intro": ("\n  Che file vuoi?", "\n  Which files do you want?"),
    "output_png_one": ("    1 = immagine PNG", "    1 = PNG image"),
    "output_pdf_one": ("    2 = PDF", "    2 = PDF"),
    "output_png_many": ("    1 = un'immagine PNG per ogni foglio", "    1 = one PNG image per sheet"),
    "output_pdf_many": ("    2 = tutti i fogli in un solo PDF", "    2 = all sheets in one PDF"),
    "info_sheets_one": ("Impaginazione: tutti i livelli in un foglio, {f}", "Layout: all levels on one sheet, {f}"),
    "info_files": ("File: {f}", "Files: {f}"),
    "info_sheets_levels": ("Impaginazione: un livello per foglio ({n} fogli), {f}",
                           "Layout: one level per sheet ({n} sheets), {f}"),
    "info_paper_intro_levels": ("Un livello per foglio, il più grande occupa {nc} x {nr} caratteri. Formati possibili:",
                                "One level per sheet, the biggest takes {nc} x {nr} letters. Possible formats:"),
    "info_paper_option_levels": ("{paper}  {n} fogli   caratteri da {mm:.2f} mm   {v}{note}",
                                 "{paper}  {n} sheets   {mm:.2f} mm letters   {v}{note}"),
    "info_sheet_level": ("{lv}: foglio {paper} {o} ({w} x {h} px)", "{lv}: {paper} sheet, {o} ({w} x {h} px)"),
    "info_sheet": ("Foglio {paper} {o} ({w} x {h} px a {dpi} dpi), caratteri da {mm:.2f} mm",
                   "{paper} sheet, {o} ({w} x {h} px at {dpi} dpi), {mm:.2f} mm letters"),
    "info_letters": ("Caratteri da {mm:.2f} mm su tutti i fogli ({dpi} dpi)", "{mm:.2f} mm letters on every sheet ({dpi} dpi)"),
    "warn_tiny": ("Caratteri molto piccoli: scegli un formato più grande se puoi.",
                  "Very small letters: choose a bigger format if you can."),
    "step_gm": ("Mappa del master ({paper}, {dpi} dpi, {f} + TXT)", "Game master map ({paper}, {dpi} dpi, {f} + TXT)"),
    "step_players": ("Mappa dei giocatori e chiave del dungeon", "Players' map and dungeon key"),
    "step_players_only": ("Mappa dei giocatori", "Players' map"),
    "saved": ("Salvate: {a}  +  {b}", "Saved: {a}  +  {b}"),
    "saved_key": ("Chiave: {a}", "Key: {a}"),
    "saved_story": ("Storia: {a}", "Story: {a}"),
    "saved_monsters": ("Mostri: {a}", "Monsters: {a}"),
    "err_story_fonts": ("ERRORE: manca il font {f} nella cartella {d}, quindi il PDF della storia non viene creato "
                        "(le mappe e la chiave .txt sì). Rimetti il file nella cartella fonts accanto a wyrmdelve.py.",
                        "ERROR: the font {f} is missing from the folder {d}, so the story PDF is not made "
                        "(the maps and the .txt key are). Put the file back in the fonts folder next to wyrmdelve.py."),
    "err_no_fpdf": ("ERRORE: manca la libreria fpdf2, quindi il PDF della storia non viene creato (la chiave .txt sì). "
                    "Con l'ambiente virtuale attivo scrivi: pip install -r requirements.txt",
                    "ERROR: the fpdf2 library is missing, so the story PDF is not made (the .txt key is). "
                    "With the virtual environment active, type: pip install -r requirements.txt"),
    "err_old_fpdf": ("ERRORE: è installata la vecchia libreria «fpdf» {v} al posto di «fpdf2», quindi il PDF della storia "
                     "non viene creato. Con l'ambiente virtuale attivo scrivi: pip uninstall -y fpdf fpdf2  e poi: "
                     "pip install -r requirements.txt",
                     "ERROR: the old «fpdf» library {v} is installed instead of «fpdf2», so the story PDF is not made. "
                     "With the virtual environment active, type: pip uninstall -y fpdf fpdf2  and then: "
                     "pip install -r requirements.txt"),
    "err_story_pdf": ("ERRORE: il PDF della storia non è stato creato: {e}", "ERROR: the story PDF was not made: {e}"),
    "pdf_history": ("Storia", "History"),
    "pdf_strata": ("Strati, dal più antico", "Strata, oldest first"),
    "pdf_entrances": ("Ingressi e uscite", "Entrances and exits"),
    "pdf_links": ("Collegamenti tra livelli", "Level connections"),
    "pdf_jaquays": ("I principi di Jaquays", "Jaquays' principles"),
    "pdf_level": ("Livello {n}", "Level {n}"),
    "pdf_sublevel": ("Sottolivello {n}", "Sub-level {n}"),
    "pdf_sub_between": ("tra il livello {a} e il livello {b}", "between level {a} and level {b}"),
    "pdf_sub_below": ("sotto il livello 1", "below level 1"),
    "warn_missing_glyphs": ("Il font non ha questi glifi, sostituiti con ASCII: {g}",
                            "The font lacks these symbols, replaced with ASCII: {g}"),
    "pb_drawing": ("disegno", "drawing"),
    "pb_saving": ("salvataggio", "saving"),
    "pb_done": ("fatto", "done"),
    "orientation_portrait": ("verticale", "portrait"),
    "orientation_landscape": ("orizzontale", "landscape"),
    "color_name_1": ("nero su bianco", "black on white"),
    "color_name_2": ("bianco su celeste", "white on light blue"),
    "color_name_3": ("bianco su nero", "white on black"),
    # page
    "level_header": ("LIVELLO {n}", "LEVEL {n}"),
    "sub_header": ("SOTTOLIVELLO {n}", "SUB-LEVEL {n}"),
    "divided_header": (" · diviso", " · divided"),
    "subtitle": ("Seme {seed} · {l} livelli · {r} stanze · {e} ingressi",
                 "Seed {seed} · {l} levels · {r} rooms · {e} entrances"),
    "subtitle_one": ("Seme {seed} · 1 livello · {r} stanze · {e} ingressi",
                     "Seed {seed} · 1 level · {r} rooms · {e} entrances"),
    "players_title": ("{t} — mappa dei giocatori", "{t} — players' map"),
    "players_title_plain": ("Mappa dei giocatori", "Players' map"),
    # legend
    "lg_floor": ("pavimento", "floor"),
    "lg_door": ("porta", "door"),
    "lg_secret_door": ("porta segreta", "secret door"),
    "lg_hidden": ("passaggio segreto", "secret passage"),
    "lg_stairs": ("scale su/giù", "stairs up/down"),
    "lg_steps": ("gradini (stesso livello)", "steps (same level)"),
    "lg_shaft": ("pozzo/camino tra livelli", "shaft/chimney between levels"),
    "lg_portal": ("portale magico", "magic portal"),
    "lg_water": ("acqua", "water"),
    "lg_rubble": ("crollo", "cave-in"),
    "lg_pillar": ("colonna", "pillar"),
    "lg_entrance": ("ingresso", "entrance"),
    "lg_room": ("stanza (livello-numero)", "room (level-number)"),
    "lg_scale": ("Scala:", "Scale:"),
    "scale_imperial": ("1 casella = 5 ft (piedi)", "1 square = 5 ft"),
    "scale_metric": ("1 casella = 1,5 m", "1 square = 1.5 m"),
    "lg_era1": ("mura dei fondatori (I)", "founders' walls (I)"),
    "lg_era2": ("mura della II epoca", "second-age walls (II)"),
    "lg_era0": ("grotte e cunicoli (N, III)", "caves and tunnels (N, III)"),
    # key file
    "key_seed": ("Seme", "Seed"),
    "key_history": ("STORIA", "HISTORY"),
    "key_types": ("Tipo", "Type"),
    "key_scale": ("Scala", "Scale"),
    "key_strata": ("STRATI (dal più antico)", "STRATA (oldest first)"),
    "key_entrances": ("INGRESSI E USCITE", "ENTRANCES AND EXITS"),
    "key_links": ("COLLEGAMENTI TRA LIVELLI", "LEVEL CONNECTIONS"),
    "key_level": ("LIVELLO {n}", "LEVEL {n}"),
    "key_sublevel": ("SOTTOLIVELLO {n} (tra il livello {a} e il livello {b})",
                     "SUB-LEVEL {n} (between level {a} and level {b})"),
    "key_sublevel_one": ("SOTTOLIVELLO {n} (sotto il livello 1)", "SUB-LEVEL {n} (below level 1)"),
    "key_divided": ("Livello diviso: la parte ovest e la parte est non sono collegate su questo livello; "
                    "si passa dall'una all'altra solo attraverso altri livelli.",
                    "Divided level: the west and east parts are not connected on this level; "
                    "you can only cross through other levels."),
    "key_exits": ("uscite", "exits"),
    "key_wander": ("Mostri erranti (d6)", "Wandering monsters (d6)"),
    "wander_dwellers": ("gli abitanti di oggi, in giro per le sale", "today's dwellers, roaming the halls"),
    "wander_quirk": (" (fuori posto: vedi {r})", " (out of place: see {r})"),
    "room_monsters": ("Mostri: {m}.", "Monsters: {m}."),
    "room_lair": ("Mostri: {m}: è la loro tana.", "Monsters: {m}: this is their lair."),
    "room_quirk": ("Fuori posto: {r}.", "Out of place: {r}."),
    "room_clue": ("Vuota. Indizio: {c} (da {r}).", "Empty. Clue: {c} (from {r})."),
    "room_empty": ("Vuota.", "Empty."),
    "quirk_from": (" del livello {n}", " of level {n}"),
    "key_entrance_line": ("{l}  {kind} (livello {lv}{mid}) → {room}",
                          "{l}  {kind} (level {lv}{mid}) → {room}"),
    "key_midpoint": (", ingresso a metà dungeon", ", midpoint entry"),
    "key_jaquays": ("PRINCIPI DI JAQUAYS (Xandering the Dungeon)", "JAQUAYS' PRINCIPLES (Xandering the Dungeon)"),
    "ex_door": ("porta", "door"),
    "ex_open": ("apertura", "opening"),
    "ex_secret": ("porta segreta", "secret door"),
    "ex_hidden": ("passaggio segreto", "secret passage"),
    "ex_water": ("allagato", "flooded"),
    "ex_rubble": ("crollo", "cave-in"),
    "ex_steps": ("gradini", "steps"),
    "ex_down": ("> scale giù", "> stairs down"),
    "ex_up": ("< scale su", "< stairs up"),
    "ex_shaft": ("○ pozzo", "○ shaft"),
    "ex_portal": ("Ω portale", "Ω portal"),
    "ex_entrance": ("ingresso {l}", "entrance {l}"),
    "ex_skips": (", salta {n} livelli", ", skips {n} levels"),
    "ex_skips_one": (", salta un livello", ", skips one level"),
    "link_stairs": ("scale", "stairs"),
    "link_shaft": ("pozzo/camino", "shaft/chimney"),
    "link_portal": ("portale magico", "magic portal"),
    # Jaquays report
    "jq_entrances": ("Ingressi multipli: {n}", "Multiple entrances: {n}"),
    "jq_entrances_one": ("Ingressi multipli: uno solo, come richiesto (gli anelli e i livelli compensano)",
                         "Multiple entrances: just one, as asked (loops and levels make up for it)"),
    "jq_midpoint": ("Ingresso a metà dungeon: {n}", "Midpoint entry: {n}"),
    "jq_loops": ("Anelli (numero ciclomatico del dungeon): {n}; su ogni livello: {d}",
                 "Loops (cyclomatic number of the dungeon): {n}; on each level: {d}"),
    "jq_multi": ("Collegamenti multipli tra livelli: {d}", "Multiple level connections: {d}"),
    "jq_disc": ("Collegamenti discontinui (saltano livelli): {n}", "Discontinuous level connections (skip levels): {n}"),
    "jq_secret": ("Percorsi segreti e insoliti: {d} porte segrete, {p} passaggi segreti, {h} scale/pozzi nascosti, "
                  "{w} allagati, {r} crolli, {g} portali",
                  "Secret and unusual paths: {d} secret doors, {p} secret passages, {h} hidden stairs/shafts, "
                  "{w} flooded, {r} cave-ins, {g} portals"),
    "ex_hidden_link": (" (nascosto)", " (hidden)"),
    "jq_sub": ("Sottolivelli: {n}", "Sub-levels: {n}"),
    "jq_divided": ("Livelli divisi: {n}", "Divided levels: {n}"),
    "jq_shifts": ("Dislivelli interni (gradini nello stesso livello): {n}", "Minor elevation shifts (steps on the same level): {n}"),
    "jq_nested": ("Dungeon annidati: grotte naturali e complesso costruito collegati in {n} punti",
                  "Nested dungeons: natural caves and built complex linked at {n} points"),
    "jq_na": ("{what}: non applicabile ({why})", "{what}: not applicable ({why})"),
    "jq_why_one": ("un solo livello", "a single level"),
    "jq_why_two": ("servono almeno 3 livelli", "needs at least 3 levels"),
    "jq_why_entr": ("serve più di un ingresso", "needs more than one entrance"),
    "jq_why_small": ("troppe poche stanze per livello", "too few rooms per level"),
    "jq_why_caves": ("nessuna grotta naturale", "no natural caves"),
    "jq_nested_kinds": ("Dungeon annidati: costruzioni di tipo diverso collegate in {n} punti",
                        "Nested dungeons: buildings of different types joined in {n} places"),
    "jq_nested_ages": ("Dungeon annidati: opera dei fondatori e ampliamenti successivi collegati in {n} punti",
                       "Nested dungeons: the founders' work and later additions joined in {n} places"),
    "jq_t_multi": ("Collegamenti multipli tra livelli", "Multiple level connections"),
    "jq_t_disc": ("Collegamenti discontinui", "Discontinuous level connections"),
    "jq_t_mid": ("Ingresso a metà dungeon", "Midpoint entry"),
    "jq_t_sub": ("Sottolivelli", "Sub-levels"),
    "jq_t_div": ("Livelli divisi", "Divided levels"),
    "jq_t_nest": ("Dungeon annidati", "Nested dungeons"),
    # help
    "h_description": ("WyrmDelve: genera dungeon casuali per giochi OSR in stile ASCII roguelike, "
                      "seguendo i principi di Jennell Jaquays. PNG o PDF a 600 dpi (A4, A3, A2, A1) + TXT.",
                      "WyrmDelve: makes random dungeons for OSR games in ASCII roguelike style, "
                      "following Jennell Jaquays' principles. 600 dpi PNG or PDF (A4, A3, A2, A1) + TXT."),
    "h_epilog": ("Senza opzioni parte la modalità interattiva. I parametri non indicati sono scelti a caso.",
                 "Without options the interactive mode starts. Parameters you leave out are chosen at random."),
    "h_levels": ("numero di livelli (1-10)", "number of levels (1-10)"),
    "h_rooms": ("numero di stanze (5-200, almeno 5 per livello)", "number of rooms (5-200, at least 5 per level)"),
    "h_entrances": ("ingressi/uscite dall'area (1-9)", "entrances/exits to the area (1-9)"),
    "h_secrets": ("porte e passaggi segreti (0-60)", "secret doors and passages (0-60)"),
    "h_colors": ("1 nero su bianco (default), 2 bianco su celeste, 3 bianco su nero",
                 "1 black on white (default), 2 white on light blue, 3 white on black"),
    "h_seed": ("seme completo (es. 3-24-2-5-CDK-K7Q2MB) per rifare un dungeon", "full seed (e.g. 3-24-2-5-CDK-K7Q2MB) to rebuild a dungeon"),
    "h_format": ("formato di stampa; senza, viene suggerito e chiesto", "print format; without it, it is suggested and asked"),
    "h_per_level": ("un livello per foglio, su file separati", "one level per sheet, in separate files"),
    "h_one_sheet": ("tutti i livelli in un solo foglio", "all levels on one sheet"),
    "h_pdf": ("salva le mappe in PDF (un solo file anche con più fogli)", "save the maps as PDF (one file even with many sheets)"),
    "h_png": ("salva le mappe in PNG (un file per foglio)", "save the maps as PNG (one file per sheet)"),
    "h_type": ("tipo di dungeon, da 1 a 11: uno per tutti i livelli (es. 4) o uno per livello dall'alto "
               "(es. 3,4,11). 1 palazzo, 2 prigione, 3 torre, 4 castello, 5 tempio, 6 città, 7 laboratorio "
               "arcano, 8 accademia, 9 fortezza di confine, 10 tomba, 11 underdark",
               "dungeon type, 1 to 11: one for every level (e.g. 4) or one per level from the top (e.g. 3,4,11). "
               "1 palace, 2 prison, 3 tower, 4 castle, 5 temple, 6 city, 7 arcane laboratory, 8 academy, "
               "9 border fortress, 10 tomb, 11 underdark"),
    "h_title": ("titolo della mappa (default: il nome del dungeon)", "map title (default: the dungeon's name)"),
    "h_no_title": ("mappa senza nome", "map without a name"),
    "h_no_story": ("solo le mappe, come --contenuto mappa", "only the maps, like --content map"),
    "h_content": ("cosa generare: mappa (solo le mappe), storia (mappe e storia), mostri (mappe e mostri), "
                  "tutto (mappe, storia e mostri; di base)",
                  "what to make: map (only the maps), story (maps and story), monsters (maps and monsters), "
                  "all (maps, story and monsters; the default)"),
    "err_content": ("«{s}» non è una scelta valida: usa mappa, storia, mostri o tutto",
                    "“{s}” is not a valid choice: use map, story, monsters or all"),
    "h_units": ("unità della griglia: imperiale (1 casella = 5 ft) o metrica (1 casella = 1,5 m); "
                "di base metrica in italiano, imperiale in inglese",
                "grid units: imperial (1 square = 5 ft) or metric (1 square = 1.5 m); "
                "by default imperial in English, metric in Italian"),
    "h_ascii": ("solo caratteri base della tastiera", "only basic keyboard characters"),
    "h_font": ("file .ttf monospazio da usare", "monospaced .ttf font file to use"),
    "h_output": ("cartella in cui salvare (default: dungeons_generated accanto allo script)",
                 "folder to save into (default: dungeons_generated next to the script)"),
    "h_language": ("lingua dei testi: it (italiano) o en (inglese)", "language of the texts: it (Italian) or en (English)"),
}


def tr(key, **values):
    text = TEXTS[key][LANGUAGES.index(LANG)]
    return text.format(**values) if values else text


def pick(pair):
    return pair[LANGUAGES.index(LANG)]


def normalize_language(value):
    """Map "1", "it", "italiano"... to "it" (same for "en"). None if unknown."""
    value = (value or "").strip().lower()
    if value in ("1", "it", "ita", "italiano", "italian"):
        return "it"
    if value in ("2", "en", "eng", "english", "inglese"):
        return "en"
    return None


def ask_language():
    global LANG
    print("\n  Lingua / Language:")
    print("    1 = Italiano")
    print("    2 = English")
    while True:
        choice = normalize_language(input("  Scelta / Choice [1]: ") or "1")
        if choice:
            LANG = choice
            return
        print("    1 / 2")


def language_from_options(argv):
    """Peek at --lingua/--language before argparse runs, so that --help
    comes out in the right language too."""
    global LANG
    for i, arg in enumerate(argv):
        for name in ("--lingua", "--language"):
            if arg == name and i + 1 < len(argv):
                LANG = normalize_language(argv[i + 1]) or LANG
            elif arg.startswith(name + "="):
                LANG = normalize_language(arg.split("=", 1)[1]) or LANG


# --- console output ---
def bar(fraction, cells):
    full = round(max(0.0, min(1.0, fraction)) * cells)
    return "[" + "█" * full + "░" * (cells - full) + "]"


class LiveBar:
    """Progress bar that keeps redrawing the same line. Silent when stdout isn't a tty."""

    def __init__(self):
        self.live = sys.stdout.isatty()
        self.shown = None

    def update(self, fraction, label):
        percent = int(fraction * 100)
        if self.live and (percent, label) != self.shown:
            self.shown = (percent, label)
            print(f"\r        {bar(fraction, 30)} {percent:>3}%  {label:<14}", end="", flush=True)

    def finish(self):
        if self.live:
            print(f"\r        {bar(1, 30)} 100%  {tr('pb_done'):<14}")


class Log:

    def __init__(self, total_steps):
        self.total_steps, self.step_number, self.start_time = total_steps, 0, time.perf_counter()

    def step(self, message):
        self.step_number += 1
        progress = bar(self.step_number / self.total_steps, self.total_steps)
        print(f"\n{progress} {self.step_number:>2}/{self.total_steps}  {message}")

    def info(self, message):
        print(f"        · {message}")

    def warn(self, message):
        print(f"        ! {message}")

    def error(self, message):
        print(f"        ✗ {message}")

    def done(self):
        print("\n" + tr("done", s=time.perf_counter() - self.start_time))


class QuietLog:

    def info(self, message):
        pass

    def warn(self, message):
        pass


# --- seed ---
# levels-rooms-entrances-secrets-TYPES-CODE: TYPES is one letter per level
# (or a single letter when every level is of that type), CODE = 6 symbols,
# 30 random bits. Older seeds without TYPES still work: their types come
# from CODE.
SEED_SYMBOLS = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"   # no I, L, O, U: too easy to misread
CODE_LENGTH = 6


def new_number():
    return int.from_bytes(os.urandom(4), "big") % (len(SEED_SYMBOLS) ** CODE_LENGTH)


def to_code(number):
    out = []
    for _ in range(CODE_LENGTH):
        number, r = divmod(number, len(SEED_SYMBOLS))
        out.append(SEED_SYMBOLS[r])
    return "".join(reversed(out))


def from_code(text):
    text = text.strip().upper().replace("O", "0").replace("I", "1").replace("L", "1")
    if len(text) != CODE_LENGTH or any(c not in SEED_SYMBOLS for c in text):
        return None
    number = 0
    for c in text:
        number = number * len(SEED_SYMBOLS) + SEED_SYMBOLS.index(c)
    return number


def make_seed(p):
    return (f"{p['levels']}-{p['rooms']}-{p['entrances']}-{p['secrets']}-{types_code(p['types'])}-"
            f"{to_code(p['number'])}")


def read_seed(text):
    parts = (text or "").strip().split("-")
    if len(parts) not in (5, 6):
        return None
    try:
        levels, rooms, entrances, hidden = (int(x) for x in parts[:4])
    except ValueError:
        return None
    number = from_code(parts[-1])
    if number is None:
        return None
    p = {"levels": levels, "rooms": rooms, "entrances": entrances, "secrets": hidden, "number": number}
    if check_params(p):
        return None
    p["types"] = read_types(parts[4], levels) if len(parts) == 6 else default_types(levels, number)
    return None if p["types"] is None or check_params(p) else p


def seed_problem(text):
    """Why a well-formed seed can't be used (e.g. too few rooms per level), or None."""
    parts = (text or "").strip().split("-")
    if len(parts) not in (5, 6):
        return None
    try:
        levels, rooms, entrances, hidden = (int(x) for x in parts[:4])
    except ValueError:
        return None
    p = {"levels": levels, "rooms": rooms, "entrances": entrances, "secrets": hidden}
    error = check_params(p)
    if error is None and len(parts) == 6:
        types = read_types(parts[4], levels)
        if types is not None:
            error = check_params({**p, "types": types})
    return error


def example_seed():
    return "3-24-2-5-CDK-K7Q2MB"


def check_params(p):
    """Error message, or None if the parameters are fine."""
    for key, (lo, hi) in LIMITS.items():
        if not lo <= p[key] <= hi:
            return tr("err_range", what=tr("name_" + key), lo=lo, hi=hi)
    if p["rooms"] < MIN_PER_LEVEL * p["levels"]:
        return tr("err_rooms_levels", n=MIN_PER_LEVEL * p["levels"], l=p["levels"])
    if p["entrances"] > p["rooms"]:
        return tr("err_entrances")
    types = p.get("types")
    if types is not None:
        if len(types) != p["levels"]:
            return tr("err_types_count", n=len(types), l=p["levels"])
        wrong = stack_error(types)
        if wrong:
            a, b = wrong
            return tr("err_types_order", a=type_name(types[a]), b=type_name(types[b]), i=a + 1, j=b + 1)
    return None


def random_params(number, fixed=None):
    """Random parameters from the seed number; `fixed` ones are kept as they are."""
    fixed = fixed or {}
    r = random.Random(f"wyrmdelve-params-{number}")
    p = {"levels": r.choices([1, 2, 3, 4, 5, 6], weights=[2, 4, 4, 3, 1, 1])[0]}
    p.update({k: v for k, v in fixed.items() if k == "levels"})
    p["rooms"] = p["levels"] * r.randint(MIN_PER_LEVEL, 10) + r.randint(0, 3)
    p["entrances"] = r.choices([1, 2, 3, 4], weights=[1, 4, 3, 2])[0]
    p.update(fixed)
    if "rooms" not in fixed:
        p["rooms"] = max(MIN_PER_LEVEL * p["levels"], min(p["rooms"], LIMITS["rooms"][1]))
    if "levels" not in fixed and p["rooms"] < MIN_PER_LEVEL * p["levels"]:
        p["levels"] = max(1, p["rooms"] // MIN_PER_LEVEL)
    if "entrances" not in fixed:
        p["entrances"] = min(p["entrances"], p["rooms"])
    if "secrets" not in fixed:
        p["secrets"] = r.randint(1, max(2, p["rooms"] // 5))
    if "types" in fixed and len(fixed["types"]) == 1:
        p["types"] = fixed["types"] * p["levels"]
    elif "types" not in fixed:
        p["types"] = default_types(p["levels"], number)
    p["number"] = number
    return p


# --- story tables ---
# The words the dungeons are made of (dungeon types, names, later occupants,
# rooms, events, places, entrances, the history) live in wyrmdelve_tables.json,
# next to this file. Every text there is {"it": ..., "en": ...}; here it
# becomes (it, en).
TABLES_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "wyrmdelve_tables.json")


def from_json(value):
    if isinstance(value, dict) and set(value) == {"it", "en"}:
        return value["it"], value["en"]
    if isinstance(value, dict):
        return {k: from_json(v) for k, v in value.items()}
    if isinstance(value, list):
        return [from_json(v) for v in value]
    return value


TABLE_KEYS = ("name_syllables", "dungeon_types", "second_age", "present_day", "natural_rooms", "events", "areas",
              "surface_shaft", "history")
TYPE_KEYS = ("id", "code", "menu", "name", "surface", "below", "eras", "pattern", "builders", "built", "titles",
             "rooms", "entrances", "side_entrances")


def load_tables(path=TABLES_FILE):
    name = os.path.basename(path)
    try:
        with open(path, encoding="utf-8") as f:
            tables = from_json(json.load(f))
    except OSError:
        sys.exit(f"Manca il file {name}: mettilo nella stessa cartella di wyrmdelve.py.\n"
                 f"{name} is missing: put it in the same folder as wyrmdelve.py.")
    except ValueError as e:
        sys.exit(f"C'è un errore nel file {name} / There is a mistake in {name}:\n  {e}")
    missing = [k for k in TABLE_KEYS if k not in tables]
    for t in tables.get("dungeon_types", []):
        missing += [f"{t.get('id', '?')}.{k}" for k in TYPE_KEYS if k not in t]
    if missing:
        sys.exit(f"Nel file {name} mancano / {name} lacks: {', '.join(missing)}")
    ids = {t["id"] for t in tables["dungeon_types"]}
    wrong = [f"{t['id']}.below: {b}" for t in tables["dungeon_types"] for b in t["below"] if b not in ids]
    if wrong:
        sys.exit(f"Nel file {name} ci sono tipi sconosciuti / {name} names unknown types: {', '.join(wrong)}")
    return tables


TABLES = load_tables()
NAMES = TABLES["name_syllables"]
if isinstance(NAMES, list):                     # older files: just a list of syllables
    NAMES = {"syllables": NAMES, "endings": {}}
NAME_SYLLABLES = NAMES["syllables"]
NAME_ENDINGS = {k: v for k, v in NAMES.get("endings", {}).items() if v}   # language -> endings
TYPES = TABLES["dungeon_types"]                 # in menu order
TYPE = {t["id"]: t for t in TYPES}
TYPE_BY_CODE = {t["code"]: t["id"] for t in TYPES}
SECOND = TABLES["second_age"]
PRESENT = TABLES["present_day"]
NATURAL_ROOMS = TABLES["natural_rooms"]
EVENTS = TABLES["events"]
AREAS = TABLES["areas"]
SURFACE_SHAFT = TABLES["surface_shaft"]
# every part of the history is a list of variants (older files: a single sentence);
# "words" holds the lists its sentences draw from: {goal}, {relic}, {visitors}
HISTORY = {k: v if isinstance(v, list) else [v] for k, v in TABLES["history"].items() if k != "words"}
HISTORY_WORDS = TABLES["history"].get("words", {})
HISTORY_PARTS = ("founded", "caves", "second", "fall", "present", "crude")
HISTORY_OPENINGS = ("opening", "opening_legend", "opening_place")    # or none
HISTORY_CLOSINGS = ("legend", "warning", "hook")                     # or none
HISTORY_EXTRAS = ("purpose", "golden", "omen", "second_detail", "fate", "aftermath", "interlude", "present_detail")
WORD_TABLES = {"goal": "goals", "relic": "relics", "visitors": "visitors"}
STORY_FIELDS = {"f", "built", "area", "e1", "s", "e2", "p"}
missing = [k for k in HISTORY_PARTS if not HISTORY.get(k)]
if missing:
    sys.exit(f"Nel file {os.path.basename(TABLES_FILE)} mancano / {os.path.basename(TABLES_FILE)} lacks: "
             + ", ".join("history." + k for k in missing))

# monsters (optional tables): name, text, where (type ids or "*"), danger 1-4, kind, number;
# clues by kind, for the empty rooms near a monster; quirks: why an unexpected monster is here
MONSTERS = [m for m in TABLES.get("monsters", []) if m.get("name") and m.get("text")]
CLUES = {k: v for k, v in TABLES.get("clues", {}).items() if v}
QUIRKS = [q for q in TABLES.get("quirks", []) if q.get("text")]

ERA_TAGS = {0: "N", 1: "I", 2: "II", 3: "III"}


# --- dungeon types and how they stack ---
# Every type lists the types that may lie directly below it ("below"), so the
# levels always make sense from top to bottom: a tower stands on a castle, a
# crypt lies under a temple, the Underdark is at the bottom of everything.
def stack_error(types):
    """(upper index, lower index) of the first pair that can't be stacked, or None."""
    for k in range(len(types) - 1):
        if types[k + 1] not in TYPE[types[k]]["below"]:
            return k, k + 1
    return None


def random_types(levels, rng):
    """All levels of one type, or a coherent mix, top to bottom."""
    ids = [t["id"] for t in TYPES]
    if levels == 1 or rng.random() < 0.4:
        return [rng.choice(ids)] * levels
    chain = [rng.choice(ids)]
    while len(chain) < levels:
        below = TYPE[chain[-1]]["below"]
        chain.append(chain[-1] if rng.random() < 0.4 else rng.choice(below))
    return chain


def default_types(levels, number):
    return random_types(levels, random.Random(f"wyrmdelve-types-{number}"))


def types_code(types):
    codes = [TYPE[t]["code"] for t in types]
    return codes[0] if len(set(codes)) == 1 else "".join(codes)


def read_types(text, levels):
    ids = [TYPE_BY_CODE.get(ch) for ch in text.strip().upper()]
    if not ids or None in ids:
        return None
    if len(ids) == 1:
        ids = ids * levels
    return ids if len(ids) == levels else None


def ground_index(types):
    """The level at ground level: the lowest building above ground, or else
    the top one. The main entrances are there."""
    above = [k for k, t in enumerate(types) if TYPE[t]["surface"]]
    return above[-1] if above else 0


def type_name(kind):
    return pick(TYPE[kind]["name"])


def types_text(types):
    """"Castle (every level)" or "1 Tower, 2 Castle, 3 Underdark"."""
    if len(set(types)) == 1:
        return type_name(types[0]) + (tr("types_all") if len(types) > 1 else "")
    return ", ".join(f"{k + 1} {type_name(t)}" for k, t in enumerate(types))


# --- the story ---
def fmt(pair, **values):
    return tuple(t.format(**values) for t in pair)


def join_pairs(pairs):
    """[(it, en), ...] -> ("a, b e c", "a, b and c")"""
    out = []
    for lang, word in enumerate((" e ", " and ")):
        words = [p[lang] for p in pairs]
        out.append(words[0] if len(words) == 1 else ", ".join(words[:-1]) + word + words[-1])
    return tuple(out)


def make_name(rng, used):
    """2-3 syllables, or 1-2 syllables and the ending of one language
    (Arabic, Danish, Old French, Persian, Greek, Latin, German, Russian,
    Tolkien-ish...)."""
    languages = sorted(NAME_ENDINGS)
    while True:
        if languages and rng.random() < 0.6:
            endings = NAME_ENDINGS[rng.choice(languages)]
            name = "".join(rng.choice(NAME_SYLLABLES) for _ in range(rng.choice((1, 1, 2)))) + rng.choice(endings)
        else:
            name = "".join(rng.choice(NAME_SYLLABLES) for _ in range(rng.choice((2, 2, 3))))
        name = name.capitalize()
        if name not in used and 3 <= len(name) <= 12:
            used.add(name)
            return name


class Deck:
    """Draws without repeats until the deck is empty, then reshuffles."""

    def __init__(self, items, rng):
        self.items, self.rng, self.pool = list(items), rng, []

    def draw(self):
        if not self.pool:
            self.pool = self.items[:]
            self.rng.shuffle(self.pool)
        return self.pool.pop()


def make_story(rng, types):
    """Who built the dungeon (the type of its ground level decides), who came
    next, who lives there today; one deck of room names per type and role."""
    used = set()
    primary = TYPE[types[ground_index(types)]]
    kinds = list(dict.fromkeys(types))
    second, present = rng.choice(SECOND), rng.choice(PRESENT)
    e1, e2 = rng.sample(EVENTS, 2)
    outdoors = any(TYPE[t]["surface"] for t in types)
    story = {
        "types": types, "second": second, "present": present,
        "f_who": fmt(rng.choice(primary["builders"]), n=make_name(rng, used)),
        "built": join_pairs([rng.choice(TYPE[t]["built"]) for t in kinds]),
        "s_who": fmt(second["who"], n=make_name(rng, used)),
        "p_who": fmt(present["who"], n=make_name(rng, used)),
        "area": rng.choice(AREAS["surface" if outdoors else "underground"]), "e1": e1, "e2": e2,
    }
    story["title"] = fmt(rng.choice(primary["titles"]), n=make_name(rng, used))
    decks = {0: Deck(NATURAL_ROOMS, rng), 2: Deck(second["rooms"], rng), 3: Deck(present["rooms"], rng)}
    for t in kinds:
        decks[t] = Deck(TYPE[t]["rooms"], rng)
        for role, names in TYPE[t].get("special", {}).items():
            decks[(t, role)] = Deck(names, rng)
    story["decks"] = decks
    return story


def fields(pair):
    """The {names} a sentence needs."""
    return {name for text in pair for _, name, _, _ in string.Formatter().parse(text) if name}


def plan_history(rng):
    """The shape of the history (how it opens, which extra parts it tells, how
    it ends) and the sentence for each part. It has its own random numbers, so
    the maps and the rooms never change with it."""
    hero = make_name(rng, set())
    words = {"hero": (hero, hero)}
    for key, table in WORD_TABLES.items():
        if HISTORY_WORDS.get(table):
            words[key] = rng.choice(HISTORY_WORDS[table])
    known = STORY_FIELDS | set(words)
    plan = {"words": words}
    for part, variants in HISTORY.items():
        usable = [v for v in variants if fields(v) <= known]
        if usable:
            plan[part] = rng.choice(usable)
    opening = rng.choice([None, None] + [k for k in HISTORY_OPENINGS if k in plan])
    closings = [k for k in HISTORY_CLOSINGS if k in plan and not (k == "legend" and opening == "opening_legend")]
    closing = rng.choice([None] + closings)
    extras = {k for k in HISTORY_EXTRAS if k in plan and rng.random() < 0.4}
    plan["shape"] = {"opening": opening, "closing": closing, "extras": extras}
    return plan


def history_patterns():
    """How many shapes the history can take (caves and crude tunnels aside)."""
    openings = [k for k in HISTORY_OPENINGS if HISTORY.get(k)]
    closings = [k for k in HISTORY_CLOSINGS if HISTORY.get(k)]
    pairs = sum(1 + len([c for c in closings if not (c == "legend" and o == "opening_legend")])
                for o in [None] + openings)
    return pairs * 2 ** len([k for k in HISTORY_EXTRAS if HISTORY.get(k)])


def capitalized(text):
    return text[:1].upper() + text[1:]


def history_text(dungeon):
    """The history in the key, sentence by sentence: caves and crude tunnels
    are only mentioned if the dungeon has them."""
    s, plan = dungeon.story, dungeon.story["history"]
    shape = plan["shape"]
    eras = {r.era for r in dungeon.rooms}

    def extra(*names):
        return [k for k in names if k in shape["extras"]]
    parts = [shape["opening"]] if shape["opening"] else []
    parts += ["founded"] + extra("purpose") + (["caves"] if 0 in eras else []) + extra("golden", "omen")
    parts += ["second"] + extra("second_detail") + ["fall"] + extra("aftermath", "fate", "interlude")
    parts += [] if shape["opening"] == "opening" else ["present"]    # that opening already says who lives there
    parts += extra("present_detail") + (["crude"] if 3 in eras else [])
    parts += [shape["closing"]] if shape["closing"] else []
    out = []
    for i in range(2):
        values = dict(f=s["f_who"][i], built=s["built"][i], area=s["area"][i], e1=s["e1"][i], s=s["s_who"][i],
                      e2=s["e2"][i], p=s["p_who"][i])
        values.update({k: v[i] for k, v in plan["words"].items()})
        out.append(" ".join(capitalized(plan[k][i].format(**values)) for k in parts))
    return tuple(out)


def describe_room(room, story, rng):
    """The room's strata: [(era, (it, en)), ...], oldest first. Special rooms
    (a throne hall, a cloister...) take their name from their role."""
    decks, kind = story["decks"], room.level.kind
    if room.role and (kind, room.role) in decks:
        first = decks[(kind, room.role)].draw()
    elif room.era == 1:
        first = decks[kind].draw()
    else:
        first = decks[room.era].draw()
    layers = [(room.era, first)]
    if room.era == 0:
        if rng.random() < 0.15:
            layers.append((2, decks[2].draw()))
        if rng.random() < 0.25:
            layers.append((3, decks[3].draw()))
    elif room.era == 1:
        if rng.random() < 0.4:
            layers.append((2, decks[2].draw()))
        if rng.random() < 0.3:
            layers.append((3, decks[3].draw()))
    elif room.era == 2 and rng.random() < 0.3:
        layers.append((3, decks[3].draw()))
    return layers


# --- dungeon model ---
DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))
AROUND = [(dx, dy) for dy in (-1, 0, 1) for dx in (-1, 0, 1) if dx or dy]

ROCK, ROOM, CORRIDOR, DOORWAY = 0, 1, 2, 3


class Room:

    def __init__(self, uid, level, era, slot, comp, spec=None):
        self.uid, self.level, self.era, self.slot, self.comp = uid, level, era, slot, comp
        spec = spec or Spec(slot)
        self.span, self.shape, self.role = spec.span, spec.shape, spec.role
        self.forced = spec.era is not None      # its era comes from the layout (a throne hall is the founders')
        self.mirror_of = None                   # the room it mirrors, in symmetric layouts
        self.cells = set()
        self.ring = set()
        self.box = None             # floor bounding box x0, y0, x1, y1
        self.number, self.label = 0, ""
        self.layers = []
        self.doors = []             # Door objects of this room

    @property
    def center(self):
        x0, y0, x1, y1 = self.box
        return (x0 + x1) / 2, (y0 + y1) / 2

    def physical(self):
        x, y = self.center
        return x, y * ASPECT_GUESS


class Door:

    def __init__(self, room, cell, out, direction, kind):
        self.room, self.cell, self.out, self.direction, self.kind = room, cell, out, direction, kind
        self.uses = 0


class Corridor:

    def __init__(self, a, b, cells, door_a, door_b, era, kind):
        self.a, self.b, self.cells, self.door_a, self.door_b = a, b, cells, door_a, door_b
        self.era, self.kind = era, kind     # kind: tree, loop or fix
        self.feature = None                 # hidden, water, rubble, steps
        self.secret_door = None

    def door_of(self, room):
        return self.door_a if room is self.a else self.door_b

    def other(self, room):
        return self.b if room is self.a else self.a


class Link:
    """Connection between two rooms on different levels (or a portal)."""

    def __init__(self, kind, a, b):
        self.kind, self.a, self.b = kind, a, b      # stairs, shaft, portal
        self.cells = []                             # (level, cell index) of both ends
        self.secret = False                         # hidden stairs, trapdoor, concealed shaft

    def other(self, room):
        return self.b if room is self.a else self.a


class Level:

    def __init__(self, name, depth, cols, rows, sub=False, kind="underdark"):
        self.name, self.depth, self.sub, self.kind = name, depth, sub, kind
        self.cols, self.rows = cols, rows
        self.W, self.H = cols * SLOT_W + 2, rows * SLOT_H + 2
        size = self.W * self.H
        self.floor = bytearray(size)
        self.era = bytearray(size)
        self.blocked = bytearray(size)      # rooms, their walls and the border
        self.rooms = []
        self.doors = {}                     # cell index -> Door
        self.feat = {}                      # cell index -> up, down, shaft, portal, pillar, water, rubble, steps, hidden
        self.labels = {}                    # cell index -> letter of a room number
        self.hidden_feats = set()           # stairs/shafts the players can't see
        self.exits = []                     # (letter, (x, y), (dx, dy))
        self.inner_tags = []                # (letter, (x, y)) next to a shaft from the surface
        self.split = None                   # column that divides the level, or None
        self.corridors = []
        for x in range(self.W):
            self.blocked[x] = self.blocked[(self.H - 1) * self.W + x] = 1
        for y in range(self.H):
            self.blocked[y * self.W] = self.blocked[y * self.W + self.W - 1] = 1

    def i(self, x, y):
        return y * self.W + x

    def inside(self, x, y):
        return 0 <= x < self.W and 0 <= y < self.H

    def region(self, comp):
        """x range a component may dig in (a divided level keeps its halves apart)."""
        if self.split is None:
            return 1, self.W - 2
        return (1, self.split - 1) if comp == 0 else (self.split + 1, self.W - 2)

    def header(self):
        kind = " · " + type_name(self.kind).upper()
        if self.sub:
            return tr("sub_header", n=self.name) + kind
        return tr("level_header", n=self.name) + kind + (tr("divided_header") if self.split is not None else "")


class Dungeon:

    def __init__(self, params, story):
        self.params, self.story = params, story
        self.levels, self.rooms, self.corridors, self.links, self.entrances = [], [], [], [], []
        self.stats = Counter()

    def mains(self):
        return [lv for lv in self.levels if not lv.sub]


# --- room shapes ---
BIG_ROLES = {"hall", "court", "nave", "plaza", "cloister", "keep", "grotto", "burial", "library", "lab"}
OPEN_ROLES = {"court", "plaza"}             # yards and squares: no pillars


def slot_box(slot, span=(1, 1)):
    """Floor area a room may use inside its slots (inclusive)."""
    c, r = slot
    w, h = span
    ox, oy = 1 + c * SLOT_W, 1 + r * SLOT_H
    return ox + 2, oy + 2, ox + w * SLOT_W - 3, oy + h * SLOT_H - 3


def cave_cells(x0, y0, x1, y1, rng):
    """A natural cave: an ellipse with a wobbly edge, always connected."""
    w, h = x1 - x0 + 1, y1 - y0 + 1
    cx, cy, rx, ry = (x0 + x1) / 2, (y0 + y1) / 2, w / 2, h / 2
    waves = [(k, rng.uniform(0.04, 0.13), rng.uniform(0, 2 * math.pi)) for k in (2, 3, 5)]
    cells = set()
    for x in range(x0, x1 + 1):
        for y in range(y0, y1 + 1):
            u, v = (x - cx) / rx, (y - cy) / ry
            limit = 0.97 + sum(a * math.sin(k * math.atan2(v, u) + ph) for k, a, ph in waves)
            if u * u + v * v <= min(1.0, max(0.55, limit)) ** 2:
                cells.add((x, y))
    return largest_part(cells, (round(cx), round(cy)))


def crude_cells(x0, y0, x1, y1, box, rng):
    """Dug in a hurry: corners chipped off and bumps along the sides."""
    bx0, by0, bx1, by1 = box
    w, h = x1 - x0 + 1, y1 - y0 + 1
    cells = {(x, y) for x in range(x0, x1 + 1) for y in range(y0, y1 + 1)}
    for corner in ((x0, y0), (x1, y0), (x0, y1), (x1, y1)):
        if rng.random() < 0.5:
            cells.discard(corner)
    for _ in range(rng.randint(1, 4)):
        side = rng.randrange(4)
        if side < 2 and w >= 6:
            y = y0 - 1 if side == 0 else y1 + 1
            if by0 <= y <= by1:
                a = rng.randint(x0 + 1, x1 - 3)
                cells |= {(x, y) for x in range(a, a + rng.randint(2, 3))}
        elif side >= 2 and h >= 3:
            x = x0 - 1 if side == 2 else x1 + 1
            if bx0 <= x <= bx1:
                cells.add((x, rng.randint(y0 + 1, y1 - 1)))
    return cells


def round_cells(x0, y0, x1, y1):
    """A round room (letters are about twice as tall as wide)."""
    cx, cy, rx, ry = (x0 + x1) / 2, (y0 + y1) / 2, (x1 - x0 + 1) / 2, (y1 - y0 + 1) / 2
    cells = {(x, y) for x in range(x0, x1 + 1) for y in range(y0, y1 + 1)
             if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1.08}
    return largest_part(cells, (round(cx), round(cy)))


def octagon_cells(x0, y0, x1, y1):
    k = max(1, min(x1 - x0 + 1, 2 * (y1 - y0 + 1)) // 5)
    return {(x, y) for x in range(x0, x1 + 1) for y in range(y0, y1 + 1)
            if min(x - x0, x1 - x) + 2 * min(y - y0, y1 - y) >= k}


def shape_room(room, rng):
    box = bx0, by0, bx1, by1 = slot_box(room.slot, room.span)
    level = room.level
    if room.mirror_of is not None:
        # symmetric layouts: the mirror image of its twin across the level's axis
        cells = {(level.W - 1 - x, y) for x, y in room.mirror_of.cells}
    else:
        maxw, maxh = bx1 - bx0 + 1, by1 - by0 + 1
        big = room.role in BIG_ROLES
        shape = room.shape
        if room.era == 0:
            shape = "cave"
        elif room.era == 3 and not room.forced and shape in ("rect", "uniform"):
            shape = "crude"
        if shape == "small":
            w, h = rng.randint(5, 7), rng.randint(2, 3)
        elif shape == "uniform":
            w, h = maxw - 4, maxh - 2
        elif shape == "round":
            w = min(maxw, 2 * maxh)
            w = max(7, round(w * (1.0 if big else rng.uniform(0.7, 1.0))))
            h = max(4, min(maxh, round(w / ASPECT_GUESS)))
        elif shape == "cave":
            w = rng.randint(min(maxw, max(10, round(maxw * 0.5))), maxw)
            h = rng.randint(min(maxh, max(5, round(maxh * 0.7))), maxh)
        elif big:
            w, h = rng.randint(round(maxw * 0.75), maxw), rng.randint(round(maxh * 0.75), maxh)
        elif room.era == 1:
            w, h = rng.randint(round(maxw * 0.4), maxw), rng.randint(min(maxh, 4), maxh)
        else:
            w, h = rng.randint(6, max(6, round(maxw * 0.68))), rng.randint(3, max(3, round(maxh * 0.7)))
        w, h = min(w, maxw), min(h, maxh)
        if shape == "small":
            x0, y0 = bx0 + (maxw - w) // 2, by0 + (maxh - h) // 2      # cells line up in rows
        else:
            x0, y0 = rng.randint(bx0, bx1 - w + 1), rng.randint(by0, by1 - h + 1)
        x1, y1 = x0 + w - 1, y0 + h - 1
        if shape == "cave":
            cells = cave_cells(x0, y0, x1, y1, rng)
        elif shape == "crude":
            cells = crude_cells(x0, y0, x1, y1, box, rng)
        elif shape == "round":
            cells = round_cells(x0, y0, x1, y1)
        elif shape == "octagon":
            cells = octagon_cells(x0, y0, x1, y1)
        else:
            cells = {(x, y) for x in range(x0, x1 + 1) for y in range(y0, y1 + 1)}
    room.cells = cells
    xs, ys = [x for x, _ in cells], [y for _, y in cells]
    room.box = (min(xs), min(ys), max(xs), max(ys))
    room.ring = {(x + dx, y + dy) for x, y in cells for dx, dy in AROUND} - cells


def largest_part(cells, start):
    """The 4-connected part of `cells` holding `start` (or the biggest one)."""
    if start not in cells:
        start = min(cells, key=lambda c: abs(c[0] - start[0]) + abs(c[1] - start[1]))
    seen, todo = {start}, [start]
    while todo:
        x, y = todo.pop()
        for dx, dy in DIRS:
            n = (x + dx, y + dy)
            if n in cells and n not in seen:
                seen.add(n)
                todo.append(n)
    return seen


def put_room(level, room):
    for x, y in room.cells:
        i = level.i(x, y)
        level.floor[i], level.era[i], level.blocked[i] = ROOM, room.era, 1
    for x, y in sorted(room.ring):
        level.blocked[level.i(x, y)] = 1


def place_label(level, room):
    """Room number in the middle of the room, in bold on the GM map."""
    cx, cy = room.center
    text = room.label
    for dy in (0, -1, 1, -2, 2):
        y = round(cy) + dy
        sx = round(cx - (len(text) - 1) / 2)
        for shift in (0, -1, 1, -2, 2):
            if all((sx + shift + k, y) in room.cells for k in range(len(text))):
                for k, ch in enumerate(text):
                    level.labels[level.i(sx + shift + k, y)] = ch
                return


def place_pillars(level, room):
    """Founders' big halls get two rows of pillars, kept symmetrical."""
    x0, y0, x1, y1 = room.box
    grand = room.role in BIG_ROLES - OPEN_ROLES or (room.role is None and room.shape == "rect")
    if room.era != 1 or room.shape not in ("rect", "uniform") or not grand or x1 - x0 + 1 < 10 or y1 - y0 + 1 < 5:
        return
    xs = list(range(x0 + 2, x1 - 1, 3))
    shift = ((x1 - 2) - xs[-1]) // 2
    for y in (y0 + 1, y1 - 1):
        for x in xs:
            i = level.i(x + shift, y)
            if (x + shift, y) in room.cells and i not in level.labels:
                level.feat[i] = "pillar"


# --- layouts: every dungeon type has its own floor plan ---
# A layout places the rooms of one level on a grid of slots (a slot holds one
# room, a big room may span several). Corridors, loops, level connections,
# entrances and secrets come afterwards and are the same for every type, so
# every layout keeps Jaquays' principles.
class Spec:
    """Where a room goes and what it is: slot, span, shape, role, a fixed era,
    the index of the room it mirrors."""

    def __init__(self, slot, span=(1, 1), shape="rect", role=None, era=None, mirror=None):
        self.slot, self.span, self.shape, self.role, self.era, self.mirror = slot, span, shape, role, era, mirror

    def slots(self):
        c, r = self.slot
        return [(c + i, r + j) for i in range(self.span[0]) for j in range(self.span[1])]


def grid_for(n, spare=None):
    """Slot columns and rows for n rooms with some empty slots, about square on paper."""
    slots = n + (math.ceil(n * 0.35) + 1 if spare is None else spare)
    cols = max(2, round(math.sqrt(slots * 1.25)))
    rows = max(1, math.ceil(slots / cols))
    return cols, rows


def all_slots(cols, rows):
    return [(c, r) for r in range(rows) for c in range(cols)]


def free_slots(cols, rows, specs):
    used = {s for spec in specs for s in spec.slots()}
    return [s for s in all_slots(cols, rows) if s not in used]


def mirror_pairs(specs, cols, rows, pairs, rng, shape_of, role_of=lambda c: None):
    """`pairs` rooms on the left half and their mirror images on the right,
    closest to the axis first."""
    axis = cols // 2
    left = [s for s in free_slots(cols, rows, specs) if s[0] < axis]
    left.sort(key=lambda s: (axis - s[0]) + rng.random() * 1.6)
    for c, r in left[:pairs]:
        specs.append(Spec((c, r), shape=shape_of(c), role=role_of(c)))
        specs.append(Spec((cols - 1 - c, r), shape=specs[-1].shape, role=specs[-1].role, mirror=len(specs) - 1))


def lay_scatter(n, rng):
    """Underdark and caves: rooms anywhere, one great cavern if there's room."""
    cols, rows = grid_for(n)
    specs = []
    if n >= 8 and cols >= 3:
        specs.append(Spec((rng.randrange(cols - 1), rng.randrange(rows)), (2, 1), "cave", "grotto", era=0))
    for slot in rng.sample(free_slots(cols, rows, specs), n - len(specs)):
        specs.append(Spec(slot))
    return cols, rows, specs


def lay_palace(n, rng):
    """Symmetric about a north-south axis, the throne hall in the middle."""
    cols, rows = grid_for(n)
    cols += 1 - cols % 2
    rows = max(rows, 2)
    while True:
        hall_h = 2 if rows >= 3 and n >= 6 else 1
        options = [c for c in range(rows - hall_h + 1) if (n - 1 - c) % 2 == 0 and (n - 1 - c) // 2 <= (cols // 2) * rows]
        if options:
            break
        rows += 1
    axis, centre = cols // 2, options[0]
    r0 = (rows - hall_h) // 2
    specs = [Spec((axis, r0), (1, hall_h), "rect", "hall", era=1)]
    spare = [(axis, r) for r in range(rows) if not r0 <= r < r0 + hall_h]
    for k, slot in enumerate(rng.sample(spare, centre)):
        specs.append(Spec(slot, role="court" if k == 0 else None))
    mirror_pairs(specs, cols, rows, (n - 1 - centre) // 2, rng, lambda c: rng.choice(("rect", "rect", "octagon")))
    return cols, rows, specs


def lay_temple(n, rng):
    """A long nave on the axis, the apse at its head, side chapels in pairs."""
    cols, rows = grid_for(n)
    cols += 1 - cols % 2
    rows = max(rows, 2)
    axis = cols // 2
    while True:
        extra = (n - 2) % 2                     # one more room on the axis keeps the rest in pairs
        nave_h = rows - 1 - extra
        if nave_h >= 1 and (n - 2 - extra) // 2 <= axis * rows:
            break
        rows += 1
    specs = [Spec((axis, 0), shape="round", role="apse", era=1),
             Spec((axis, 1), (1, nave_h), "rect", "nave", era=1)]
    if extra:
        specs.append(Spec((axis, rows - 1)))
    mirror_pairs(specs, cols, rows, (n - 2 - extra) // 2, rng, lambda c: "rect",
                 lambda c: "chapel" if c == axis - 1 and rng.random() < 0.6 else None)
    return cols, rows, specs


def lay_tomb(n, rng):
    """A processional axis: antechamber, halls, burial chamber at the far end;
    burial niches in pairs on both sides."""
    cols = 3 if n <= 9 else 5 if n <= 25 else 7
    rows = max(2, math.ceil((n + math.ceil(n * 0.35) + 1) / cols))
    axis = cols // 2
    while True:
        options = [c for c in range(2, min(rows, n) + 1) if (n - c) % 2 == 0 and (n - c) // 2 <= axis * rows]
        if options:
            break
        rows += 1
    centre = max(c for c in options if c <= max(2, n // 2 + 1)) if any(c <= max(2, n // 2 + 1) for c in options) \
        else options[0]
    middle = sorted(rng.sample(range(1, rows - 1), centre - 2))
    specs = [Spec((axis, 0), role="antechamber", era=1), Spec((axis, rows - 1), role="burial", era=1)]
    specs += [Spec((axis, r)) for r in middle]
    mirror_pairs(specs, cols, rows, (n - centre) // 2, rng, lambda c: "small" if c == axis - 1 else "rect",
                 lambda c: "niche" if c == axis - 1 else None)
    return cols, rows, specs


def grow_rect(slot, free, cols, rows, rng, inner=True):
    """The biggest rectangle of free slots grown from `slot` (away from the outer ring if `inner`)."""
    ok = (lambda s: s in free and (not inner or 0 < s[0] < cols - 1 and 0 < s[1] < rows - 1))
    c0 = c1 = slot[0]
    r0 = r1 = slot[1]
    grown = True
    while grown:
        grown = False
        for d in rng.sample(range(4), 4):
            if d == 0 and all(ok((c1 + 1, r)) for r in range(r0, r1 + 1)):
                c1 += 1
            elif d == 1 and all(ok((c0 - 1, r)) for r in range(r0, r1 + 1)):
                c0 -= 1
            elif d == 2 and all(ok((c, r1 + 1)) for c in range(c0, c1 + 1)):
                r1 += 1
            elif d == 3 and all(ok((c, r0 - 1)) for c in range(c0, c1 + 1)):
                r0 -= 1
            else:
                continue
            grown = True
    return (c0, r0), (c1 - c0 + 1, r1 - r0 + 1)


def lay_ring(n, rng, kind):
    """Castles and academies: buildings around a courtyard (or cloister), the
    outer ring first; a castle has towers at the corners."""
    cols, rows = grid_for(n)
    cols, rows = max(cols, 3), max(rows, 3)
    corners = {(0, 0), (cols - 1, 0), (0, rows - 1), (cols - 1, rows - 1)}

    def ring(s):
        return min(s[0], s[1], cols - 1 - s[0], rows - 1 - s[1])
    order = sorted(all_slots(cols, rows), key=lambda s: (ring(s), s not in corners, rng.random()))
    taken, free = order[:n - 1], set(order[n - 1:])
    centre = min(free, key=lambda s: (s[0] - (cols - 1) / 2) ** 2 + (s[1] - (rows - 1) / 2) ** 2 + rng.random() * 0.1)
    slot, span = grow_rect(centre, free, cols, rows, rng)
    castle = kind == "castle"
    specs = [Spec(slot, span, "rect" if castle else "uniform", "court" if castle else "cloister", era=1)]
    outer = [s for s in taken if ring(s) == 0 and s not in corners]
    rng.shuffle(outer)
    special = (["keep"] if castle else ["library", "hall"])[:len(outer)]
    for s in taken:
        if castle and s in corners:
            specs.append(Spec(s, shape="round", role="corner", era=1))
        elif s in outer[:len(special)]:
            specs.append(Spec(s, shape="rect" if castle else "uniform", role=special[outer.index(s)], era=1))
        else:
            specs.append(Spec(s, shape="rect" if castle else "uniform"))
    return cols, rows, specs


def lay_radial(n, rng, kind):
    """Towers and wizards' lairs: a round core and the rest packed around it."""
    cols, rows = grid_for(n, 1 + n // (5 if kind == "tower" else 3))
    cx, cy = (cols - 1) / 2, (rows - 1) / 2
    order = sorted(all_slots(cols, rows), key=lambda s: (s[0] - cx) ** 2 + (s[1] - cy) ** 2 + rng.random() * 0.8)
    tower = kind == "tower"
    specs = [Spec(order[0], shape="round", role="core" if tower else "circle", era=1)]
    for k, s in enumerate(order[1:n]):
        if tower:
            specs.append(Spec(s, shape="round"))
        elif k == 0:
            specs.append(Spec(s, shape="octagon", role="lab", era=1))
        else:
            specs.append(Spec(s, shape=rng.choice(("round", "octagon", "rect"))))
    return cols, rows, specs


def lay_prison(n, rng):
    """Blocks of cells in rows, guard rooms at the ends, a pit in the middle."""
    guards, pit = max(1, round(n / 8)), int(n >= 12)
    cells = n - guards - pit
    slots = math.ceil(n * 1.2) + 1
    rows = max(1, round(math.sqrt(slots / 2)))
    cols = max(3, math.ceil(slots / rows))
    specs = []
    if pit:
        specs.append(Spec((cols // 2, rows // 2), shape="round", role="pit", era=1))
    ends = [(0, r) for r in range(rows)] + [(cols - 1, r) for r in range(rows)]
    ends = [s for s in ends if s not in {sp.slot for sp in specs}]
    step = max(1, len(ends) // guards)
    for s in ends[::step][:guards]:
        specs.append(Spec(s, role="guard", era=1))
    for s in free_slots(cols, rows, specs)[:cells]:
        specs.append(Spec(s, shape="small", role="cell"))
    return cols, rows, specs


def lay_city(n, rng):
    """Packed buildings with streets between them and a square in the middle."""
    cols, rows = grid_for(n, 2 + n // 6)
    pw, ph = (2, 2) if n >= 10 and cols >= 4 and rows >= 3 else (2, 1) if n >= 5 and cols >= 3 else (1, 1)
    plaza = Spec(((cols - pw) // 2, (rows - ph) // 2), (pw, ph), "rect", "plaza", era=1)
    specs = [plaza]
    free = free_slots(cols, rows, specs)
    if n >= 6:
        near = min(free, key=lambda s: abs(s[0] - plaza.slot[0]) + abs(s[1] - plaza.slot[1]) + rng.random())
        specs.append(Spec(near, role="hall", era=1))
    for s in rng.sample(free_slots(cols, rows, specs), n - len(specs)):
        specs.append(Spec(s))
    return cols, rows, specs


def lay_fortress(n, rng):
    """A long walled line: bastions at the ends, the keep in the middle, a gate."""
    slots = math.ceil(n * 1.35) + 1
    rows = max(1, round(math.sqrt(slots / 3)))
    cols = max(3, math.ceil(slots / rows))
    while True:
        specs = [Spec((cols // 2, 0), (1, rows) if n >= 6 else (1, 1), "rect", "keep", era=1)]
        ends = [(0, 0), (cols - 1, rows - 1), (cols - 1, 0), (0, rows - 1)]
        for s in list(dict.fromkeys(ends))[:(4 if n >= 12 and rows >= 2 else 2) if n >= 4 else 0]:
            specs.append(Spec(s, shape="round", role="bastion", era=1))
        free = free_slots(cols, rows, specs)
        if len(free) >= n - len(specs):
            break
        cols += 1
    if n >= 5:
        gate = min(free, key=lambda s: (s[1] != rows - 1, abs(s[0] - 1), rng.random()))
        specs.append(Spec(gate, role="gate", era=1))
    for s in rng.sample(free_slots(cols, rows, specs), n - len(specs)):
        specs.append(Spec(s))
    return cols, rows, specs


LAYOUTS = {
    "palace": lay_palace, "temple": lay_temple, "tomb": lay_tomb, "prison": lay_prison, "city": lay_city,
    "fortress": lay_fortress, "underdark": lay_scatter,
    "castle": lambda n, rng: lay_ring(n, rng, "castle"), "academy": lambda n, rng: lay_ring(n, rng, "academy"),
    "tower": lambda n, rng: lay_radial(n, rng, "tower"), "wizard": lambda n, rng: lay_radial(n, rng, "wizard"),
}


def lay_out(kind, n, rng):
    """(cols, rows, specs) for n rooms of a type; plain scatter if the plan doesn't fit."""
    cols, rows, specs = LAYOUTS.get(TYPE[kind]["pattern"], lay_scatter)(n, rng)
    used = [s for spec in specs for s in spec.slots()]
    if len(specs) != n or len(used) != len(set(used)) or any(not (0 <= c < cols and 0 <= r < rows) for c, r in used):
        return lay_scatter(n, rng)
    return cols, rows, specs


def divide(specs, cols):
    """Split a level in two halves that don't connect (Jaquays: divided
    levels): components per room, or None if a half would be too small."""
    half = cols // 2
    for spec in specs:
        if spec.slot[0] < half < spec.slot[0] + spec.span[0]:
            spec.span = (half - spec.slot[0], spec.span[1])
    comps = [0 if spec.slot[0] < half else 1 for spec in specs]
    return comps if min(comps.count(0), comps.count(1)) >= LOOP_ROOMS else None


# --- room layout and strata ---
def split_rooms(params, rng):
    """Rooms per main level and on the sub-level (0 if none)."""
    levels, rooms = params["levels"], params["rooms"]
    sub = 0
    if rooms >= MIN_PER_LEVEL * levels + LOOP_ROOMS:
        sub = LOOP_ROOMS                    # a small hideout, still with its own loop
    rest = rooms - sub
    counts = [rest // levels] * levels
    for k in rng.sample(range(levels), rest % levels):
        counts[k] += 1
    # a little variety, never below MIN_PER_LEVEL
    for _ in range(levels):
        a, b = rng.randrange(levels), rng.randrange(levels)
        if a != b and counts[a] > MIN_PER_LEVEL:
            counts[a] -= 1
            counts[b] += 1
    return counts, sub


def assign_eras(slots, cols, rows, weights, rng):
    """Eras grow in patches (each patch is the work of one age), so the strata
    read on the map: every room takes the era of the nearest patch seed."""
    k = max(2, round(len(slots) / 3))
    seeds = [((rng.uniform(0, cols - 1), rng.uniform(0, rows - 1)), rng.choices(range(4), weights)[0])
             for _ in range(k)]

    def nearest(slot):
        return min(seeds, key=lambda s: (s[0][0] - slot[0]) ** 2 + ((s[0][1] - slot[1]) * 1.1) ** 2)[1]
    return [nearest(s) for s in slots]


def level_eras(specs, cols, rows, kind, rng):
    eras = assign_eras([s.slot for s in specs], cols, rows, TYPE[kind]["eras"], rng)
    for k, spec in enumerate(specs):
        if spec.era is not None:
            eras[k] = spec.era
        elif spec.mirror is not None:
            eras[k] = eras[spec.mirror]
    return eras


def build_rooms(dungeon, rng, log):
    params, story = dungeon.params, dungeon.story
    types = params["types"]
    counts, sub_rooms = split_rooms(params, rng)
    L = params["levels"]

    # divided level: needs 6+ rooms and never next to another divided one
    divided = set()
    candidates = [d for d in range(L) if counts[d] >= 6] if L >= 2 else []
    rng.shuffle(candidates)
    for d in candidates:
        if len(divided) >= max(1, L // 3):
            break
        if d - 1 not in divided and d + 1 not in divided:
            divided.add(d)

    uid = 0
    for d in range(L):
        kind = types[d]
        cols, rows, specs = lay_out(kind, counts[d], rng)
        level = Level(str(d + 1), d, cols, rows, kind=kind)
        comps = divide(specs, cols) if d in divided else None
        if comps:
            level.split = 1 + (cols // 2) * SLOT_W
        comps = comps or [0] * len(specs)
        eras = level_eras(specs, cols, rows, kind, rng)
        for spec, comp, era in zip(specs, comps, eras):
            level.rooms.append(Room(uid, level, era, spec.slot, comp, spec))
            uid += 1
        for room, spec in zip(level.rooms, specs):
            if spec.mirror is not None:
                room.mirror_of = level.rooms[spec.mirror]
        dungeon.levels.append(level)

    # every story needs its founders, and every dungeon shows at least two ages
    mains = dungeon.levels
    free = [r for lv in mains for r in lv.rooms if not r.forced]
    if not any(r.era == 1 for lv in mains for r in lv.rooms) and free:
        rng.choice(free).era = 1
    if len({r.era for lv in mains for r in lv.rooms}) < 2:
        # tiny levels made only of key rooms: one of them was refitted later
        room = rng.choice(free or [r for lv in mains for r in lv.rooms[1:]] or mains[0].rooms)
        weights = TYPE[room.level.kind]["eras"]
        room.era = rng.choice([e for e in (0, 2, 3) if weights[e] > 0] or [2])

    # the sub-level: a small hideout between two levels (or below the only one)
    if sub_rooms:
        d = rng.randrange(L - 1) if L >= 2 else 0
        kind = types[d]
        sc, sr = 3, 2                       # 3 rooms in 6 slots: room for a loop around them
        level = Level(f"{d + 1}a", d + 0.5, sc, sr, sub=True, kind=kind)
        era = rng.choice((0, 2, 2) if TYPE[kind]["eras"][0] > 0 else (2,))
        for slot in rng.sample([(c, r) for c in range(sc) for r in range(sr)], sub_rooms):
            level.rooms.append(Room(uid, level, era, slot, 0))
            uid += 1
        dungeon.levels.append(level)
        dungeon.levels.sort(key=lambda lv: lv.depth)

    for level in dungeon.levels:
        for room in level.rooms:
            shape_room(room, rng)
            put_room(level, room)
            room.layers = describe_room(room, story, rng)
        # numbers in reading order
        for n, room in enumerate(sorted(level.rooms, key=lambda r: (r.slot[1], r.slot[0])), 1):
            room.number, room.label = n, f"{level.name}-{n:02d}"
            place_label(level, room)
            place_pillars(level, room)
        dungeon.rooms += level.rooms
        extra = tr("info_sub") if level.sub else (tr("info_divided") if level.split is not None else "")
        log.info(tr("info_level_rooms", n=level.name, t=type_name(level.kind), r=len(level.rooms), extra=extra))


# --- corridors ---
def gabriel_edges(rooms):
    """Pairs of rooms with no third room inside the circle between them:
    near neighbours, and corridors that don't cut across other rooms."""
    pts = [r.physical() for r in rooms]
    edges = []
    for a in range(len(rooms)):
        for b in range(a + 1, len(rooms)):
            (ax, ay), (bx, by) = pts[a], pts[b]
            mx, my = (ax + bx) / 2, (ay + by) / 2
            r2 = ((ax - bx) ** 2 + (ay - by) ** 2) / 4
            if all((pts[c][0] - mx) ** 2 + (pts[c][1] - my) ** 2 >= r2 for c in range(len(rooms)) if c not in (a, b)):
                edges.append((math.sqrt(r2) * 2, a, b))
    return sorted(edges)


def spanning_tree(n, edges):
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    tree, rest = [], []
    for e in edges:
        ra, rb = find(e[1]), find(e[2])
        if ra != rb:
            parent[ra] = rb
            tree.append(e)
        else:
            rest.append(e)
    return tree, rest


def door_options(level, room, region, rng, toward):
    """Possible doors toward a point: (score, cell, out, direction), existing doors first."""
    lo, hi = region
    tx, ty = toward
    options = []
    for door in room.doors:
        ox, oy = door.out
        options.append((math.hypot(ox - tx, (oy - ty) * ASPECT_GUESS) - 4 + rng.random() * 3, door))
    used = {d.cell for d in room.doors}
    for x, y in sorted(room.ring):
        if not (lo <= x <= hi and 0 < y < level.H - 1):
            continue
        if any((x + dx, y + dy) in used for dx, dy in AROUND):
            continue
        for dx, dy in DIRS:
            if (x - dx, y - dy) not in room.cells:
                continue
            ox, oy = x + dx, y + dy
            if not (lo <= ox <= hi and 0 < oy < level.H - 1) or level.blocked[level.i(ox, oy)]:
                continue
            # rectangular rooms: doors only in the middle of a straight wall
            if room.era in (1, 2) and not ((x + dy, y + dx) in room.ring and (x - dy, y - dx) in room.ring):
                continue
            score = math.hypot(ox - tx, (oy - ty) * ASPECT_GUESS) + rng.random() * 3
            options.append((score, (x, y), (ox, oy), (dx, dy)))
    options.sort(key=lambda o: o[0])
    return options


def new_door(level, room, cell, out, direction, rng, kind=None):
    if kind is None:
        kind = "door" if room.era in (1, 2) and rng.random() < 0.75 else "open"
    door = Door(room, cell, out, direction, kind)
    i = level.i(*cell)
    level.floor[i], level.era[i] = DOORWAY, room.era
    level.doors[i] = door
    room.doors.append(door)
    return door


def astar(level, start, goal, region):
    """Cheapest 4-way path through rock: straight runs, reusing existing
    corridors, keeping away from running alongside them."""
    W, H, blocked, floor = level.W, level.H, level.blocked, level.floor
    lo, hi = region

    def free(x, y):
        return lo <= x <= hi and 0 < y < H - 1 and not blocked[y * W + x]
    if not free(*start) or not free(*goal):
        return None
    gx, gy = goal
    sx, sy = start
    heap = [(0.0, 0.0, sx, sy, 4)]
    best = {(sx, sy, 4): 0.0}
    came = {}
    while heap:
        _, g, x, y, d = heapq.heappop(heap)
        if (x, y) == goal:
            path, key = [(x, y)], (x, y, d)
            while key in came:
                key = came[key]
                path.append((key[0], key[1]))
            return path[::-1]
        if g > best.get((x, y, d), 1e18):
            continue
        for nd, (dx, dy) in enumerate(DIRS):
            nx, ny = x + dx, y + dy
            if not free(nx, ny):
                continue
            if floor[ny * W + nx] == CORRIDOR:
                step = 0.6
            else:
                step = 1.0
                for ex, ey in DIRS:
                    px, py = nx + ex, ny + ey
                    if (px, py) != (x, y) and floor[py * W + px] == CORRIDOR:
                        step += 1.5
                        break
            if d != 4 and nd != d:
                step += 0.5
            ng = g + step
            key = (nx, ny, nd)
            if ng < best.get(key, 1e18):
                best[key] = ng
                came[key] = (x, y, d)
                heapq.heappush(heap, (ng + 0.6 * (abs(nx - gx) + abs(ny - gy)), ng, nx, ny, nd))
    return None


def corridor_era(a, b):
    """Later diggers connect to older work, so a corridor belongs to the younger room."""
    return max(a.era, b.era)


def dig(level, a, b, rng, kind, region):
    """Corridor from room a to room b. Returns the Corridor or None."""
    opts_a = door_options(level, a, region, rng, b.center)[:4]
    opts_b = door_options(level, b, region, rng, a.center)[:4]
    tries = [(oa, ob) for oa in opts_a[:2] for ob in opts_b[:2]] + list(zip(opts_a[2:], opts_b[2:]))
    for oa, ob in tries:
        start = oa[1].out if isinstance(oa[1], Door) else oa[2]
        goal = ob[1].out if isinstance(ob[1], Door) else ob[2]
        path = astar(level, start, goal, region)
        if not path:
            continue
        da = oa[1] if isinstance(oa[1], Door) else new_door(level, a, oa[1], oa[2], oa[3], rng)
        db = ob[1] if isinstance(ob[1], Door) else new_door(level, b, ob[1], ob[2], ob[3], rng)
        era = corridor_era(a, b)
        for x, y in path:
            i = level.i(x, y)
            if level.floor[i] == ROCK:
                level.floor[i], level.era[i] = CORRIDOR, era
        da.uses += 1
        db.uses += 1
        corridor = Corridor(a, b, path, da, db, era, kind)
        level.corridors.append(corridor)
        return corridor
    return None


def connect_level(level, rng):
    """Spanning tree plus loops in every part of the level (Jaquays: loops)."""
    for comp in sorted({r.comp for r in level.rooms}):
        rooms = [r for r in level.rooms if r.comp == comp]
        region = level.region(comp)
        edges = gabriel_edges(rooms)
        tree, rest = spanning_tree(len(rooms), edges)
        n = len(rooms)
        want = 0 if n < 3 else max(1, round(n * TYPE[level.kind].get("loops", 0.3)))
        if want and not rest:
            # tiny or lined-up rooms: Gabriel has no spare edge, use any other pair
            tree_pairs = {(a, b) for _, a, b in tree}
            rest = sorted((math.dist(rooms[a].physical(), rooms[b].physical()), a, b)
                          for a in range(n) for b in range(a + 1, n) if (a, b) not in tree_pairs)
        pool = rest[:max(want * 2, want + 1)]
        rng.shuffle(pool)
        loops = pool[:want]
        for _, a, b in tree:
            dig(level, rooms[a], rooms[b], rng, "tree", region)
        dug = sum(1 for _, a, b in loops if dig(level, rooms[a], rooms[b], rng, "loop", region))
        if want and not dug:
            # every part of a level gets at least one loop: try the other pairs until one can be dug
            tree_pairs = {(a, b) for _, a, b in tree} | {(a, b) for _, a, b in loops}
            others = sorted((math.dist(rooms[a].physical(), rooms[b].physical()), a, b)
                            for a in range(n) for b in range(a + 1, n) if (a, b) not in tree_pairs)
            for _, a, b in others:
                if dig(level, rooms[a], rooms[b], rng, "loop", region):
                    break


# --- level connections and entrances ---
def free_spot(level, room, rng):
    """A floor cell for stairs, shafts and portals: not on the room number,
    not in front of a door, not next to another feature."""
    near_doors = {(d.cell[0] + dx, d.cell[1] + dy) for d in room.doors for dx, dy in AROUND}
    spots = []
    for x, y in room.cells:
        i = level.i(x, y)
        if i in level.feat or i in level.labels or (x, y) in near_doors:
            continue
        if any(level.i(x + dx, y + dy) in level.labels or level.feat.get(level.i(x + dx, y + dy)) not in (None, "pillar")
               for dx, dy in AROUND):
            continue
        spots.append((x, y))
    if not spots:
        spots = [c for c in room.cells if level.i(*c) not in level.feat and level.i(*c) not in level.labels]
    return rng.choice(sorted(spots)) if spots else None


def add_link(dungeon, kind, a, b, rng):
    ca, cb = free_spot(a.level, a, rng), free_spot(b.level, b, rng)
    if ca is None or cb is None:
        return None
    if kind == "stairs":
        upper, lower = (a, b) if a.level.depth < b.level.depth else (b, a)
        cu, cl = (ca, cb) if upper is a else (cb, ca)
        upper.level.feat[upper.level.i(*cu)] = "down"
        lower.level.feat[lower.level.i(*cl)] = "up"
    else:
        a.level.feat[a.level.i(*ca)] = kind
        b.level.feat[b.level.i(*cb)] = kind
    link = Link(kind, a, b)
    link.cells = [(a.level, a.level.i(*ca)), (b.level, b.level.i(*cb))]
    dungeon.links.append(link)
    return link


def plan_links(dungeon, rng):
    """Jaquays: several connections between each pair of levels, some that
    skip levels, a sub-level off the main sequence, sometimes a portal."""
    mains = dungeon.mains()
    used = Counter()
    linked = set()                          # pairs of rooms already joined by a link

    def choose(level, comp=None, avoid=()):
        """The least used room (of a part of the level), outside `avoid` if possible."""
        part = [r for r in level.rooms if comp is None or r.comp == comp]
        rooms = [r for r in part if r not in avoid] or part or level.rooms
        room = min(rooms, key=lambda r: (used[r.uid], rng.random()))
        used[room.uid] += 1
        return room

    def link(kind, a, b):
        linked.add(frozenset((a.uid, b.uid)))
        return add_link(dungeon, kind, a, b, rng)

    def partners(room):
        return {r for r in dungeon.rooms if frozenset((room.uid, r.uid)) in linked}

    for d in range(len(mains) - 1):
        up, down = mains[d], mains[d + 1]
        comps_up = sorted({r.comp for r in up.rooms})
        comps_down = sorted({r.comp for r in down.rooms})
        k = 2 + (len(up.rooms) >= 8 and len(down.rooms) >= 8 and rng.random() < 0.6)
        taken = set()                       # each connection between two levels uses rooms of its own
        for n in range(max(k, len(comps_up), len(comps_down))):
            a = choose(up, comps_up[n % len(comps_up)], taken)
            b = choose(down, comps_down[n % len(comps_down)], taken | partners(a))
            taken |= {a, b}
            link("stairs", a, b)

    if len(mains) >= 3:
        for _ in range(1 + (len(mains) >= 6)):
            d = rng.randrange(len(mains) - 2)
            jump = 3 if d + 3 < len(mains) and rng.random() < 0.3 else 2
            a = choose(mains[d])
            link("shaft", a, choose(mains[d + jump], avoid=partners(a)))

    for sub in [lv for lv in dungeon.levels if lv.sub]:
        d = int(sub.depth)
        a, b = sorted(sub.rooms, key=lambda r: r.number)[0], sorted(sub.rooms, key=lambda r: r.number)[-1]
        link("stairs", choose(mains[d]), a)
        below = mains[d + 1] if d + 1 < len(mains) else mains[d]
        link("shaft", b, choose(below, avoid=partners(b)))

    chance = max(TYPE[lv.kind].get("portal", 0.4) for lv in mains)
    if len(dungeon.rooms) >= (8 if chance >= 1 else 15) and rng.random() < chance:
        if len(mains) >= 2:
            # a portal joins far-away places: levels at least two apart when there are three or more
            pairs = [(x, y) for x in range(len(mains)) for y in range(x + 1, len(mains)) if y - x >= 2]
            x, y = rng.choice(pairs) if pairs else (0, 1)
            a = choose(mains[x])
            link("portal", a, choose(mains[y], avoid=partners(a)))
        else:
            a = choose(mains[0])
            far = max(mains[0].rooms, key=lambda r: math.dist(r.physical(), a.physical()))
            used[far.uid] += 1
            link("portal", a, far)


def neighbours(dungeon):
    """room uid -> the rooms (and "out") it can be reached from."""
    out = {r.uid: set() for r in dungeon.rooms}
    for level in dungeon.levels:
        for c in level.corridors:
            out[c.a.uid].add(c.b.uid)
            out[c.b.uid].add(c.a.uid)
    for link in dungeon.links:
        out[link.a.uid].add(link.b.uid)
        out[link.b.uid].add(link.a.uid)
    for e in dungeon.entrances:
        out[e["room"].uid].add("out")
    return out


def no_dead_ends(dungeon, rng):
    """Xandering: no room with a single way in. A room reached from one place
    only gets a corridor to the nearest room of its part of the level that it
    isn't joined to yet."""
    for room in dungeon.rooms:
        near = neighbours(dungeon)[room.uid]
        if len(near) >= 2:
            continue
        level = room.level
        others = sorted([r for r in level.rooms if r.comp == room.comp and r is not room and r.uid not in near],
                        key=lambda r: math.dist(r.physical(), room.physical()))
        for other in others:
            if dig(level, room, other, rng, "loop", level.region(room.comp)):
                break


def exit_ray(level, room, rng, region, spacing=6):
    """Straight corridor from a door of the room to the edge of the map:
    (length, cell, out, direction, ray cells) or None."""
    lo, hi = region
    best = None
    for x, y in sorted(room.ring):
        for dx, dy in DIRS:
            f = (x - dx, y - dy)
            if f not in room.cells or level.i(*f) in level.feat:
                continue
            if room.era in (1, 2) and not ((x + dy, y + dx) in room.ring and (x - dy, y - dx) in room.ring):
                continue
            if any((x + ex, y + ey) in {d.cell for d in room.doors} for ex, ey in AROUND):
                continue
            ray, cx, cy = [], x + dx, y + dy
            ok = True
            while True:
                if not (lo <= cx <= hi or cx in (0, level.W - 1)) or not level.inside(cx, cy):
                    ok = False
                    break
                border = cx in (0, level.W - 1) or cy in (0, level.H - 1)
                if border:
                    ray.append((cx, cy))
                    break
                if level.blocked[level.i(cx, cy)]:
                    ok = False
                    break
                ray.append((cx, cy))
                cx, cy = cx + dx, cy + dy
            if not ok:
                continue
            # keep exits apart from each other
            ex_, ey_ = ray[-1]
            if any(abs(ex_ - px) + abs(ey_ - py) < spacing for _, (px, py), _ in level.exits):
                continue
            score = len(ray) * (ASPECT_GUESS if dy else 1) + rng.random() * 4
            if best is None or score < best[0]:
                best = (score, (x, y), ray[0], (dx, dy), ray)
    return best


def place_entrances(dungeon, rng):
    """The main entrance is on the ground level (the lowest building above
    ground, or the top level underground); the second one is a midpoint entry
    on another level (Jaquays), the others anywhere, mostly on the ground."""
    mains = dungeon.mains()
    want = dungeon.params["entrances"]
    ground = ground_index([lv.kind for lv in mains])
    below = [k for k in range(len(mains)) if k > ground]
    above = [k for k in range(len(mains)) if k < ground]
    midpoint = below[(len(below) - 1) // 2] if below else above[0] if above else ground
    targets = []
    for n in range(want):
        if n == 0:
            targets.append(ground)
        elif n == 1 and len(mains) >= 2:
            targets.append(midpoint)
        else:
            targets.append(ground if rng.random() < 0.6 else rng.randrange(len(mains)))
    taken = set()
    for n, d in enumerate(targets):
        letter = "ABCDEFGHJ"[n]
        order = [(k, spacing) for spacing in (6, 2) for k in [d] + [k for k in range(len(mains)) if k != d]]
        placed = False
        for k, spacing in order:
            level = mains[k]
            rooms = sorted(level.rooms, key=lambda r: (min(r.box[0], level.W - r.box[2],
                                                           (r.box[1]) * ASPECT_GUESS, (level.H - r.box[3]) * ASPECT_GUESS)
                                                       + rng.random() * 8))
            found = None
            for room in [r for r in rooms if r.uid not in taken]:
                ray = exit_ray(level, room, rng, level.region(room.comp), spacing)
                if ray:
                    found = (room, ray)
                    break
            if not found:
                continue
            room, (_, cell, out, direction, cells) = found
            kind = "door" if room.era in (1, 2) else "open"
            door = new_door(level, room, cell, out, direction, rng, kind)
            door.uses += 1
            for x, y in cells:
                i = level.i(x, y)
                if level.floor[i] == ROCK:
                    level.floor[i], level.era[i] = CORRIDOR, max(room.era, 3 if room.era == 0 else room.era)
            level.exits.append((letter, cells[-1], direction))
            taken.add(room.uid)
            table = TYPE[level.kind]["entrances" if k == ground else "side_entrances"]
            dungeon.entrances.append({"letter": letter, "room": room, "level": level, "kind": rng.choice(table),
                                      "midpoint": k != ground, "cells": cells})
            placed = True
            break
        if not placed:
            # every edge is taken: a shaft from the surface straight into a room
            level = mains[d]
            rooms = [r for r in level.rooms if r.uid not in taken] or level.rooms
            room = rng.choice(rooms)
            spot = free_spot(level, room, rng)
            if spot is None:
                continue
            level.feat[level.i(*spot)] = "shaft"
            tag = next(((x, y) for x, y in ((spot[0] + 1, spot[1]), (spot[0] - 1, spot[1]))
                        if (x, y) in room.cells and level.i(x, y) not in level.feat
                        and level.i(x, y) not in level.labels), None)
            if tag:
                level.inner_tags.append((letter, tag))
                level.feat[level.i(*tag)] = "tag"
            taken.add(room.uid)
            kind = TYPE[level.kind].get("shaft_entrance", SURFACE_SHAFT)
            dungeon.entrances.append({"letter": letter, "room": room, "level": level, "kind": kind,
                                      "midpoint": d != ground, "cells": []})


# --- secret and unusual paths ---
def straight_run(cells, length):
    """Index of the middle of the first straight run of `length` cells, or None."""
    for s in range(len(cells) - length + 1):
        seg = cells[s:s + length]
        if len({x for x, _ in seg}) == 1 or len({y for _, y in seg}) == 1:
            return s + length // 2
    return None


def secret_and_unusual(dungeon, rng, log):
    """Secret doors and passages (asked by the user), flooded passages,
    cave-ins and minor elevation shifts (Jaquays: secret & unusual paths)."""
    usage = Counter()
    for level in dungeon.levels:
        for c in level.corridors:
            for cell in c.cells:
                usage[(level.name, cell)] += 1
        for e in [e for e in dungeon.entrances if e["level"] is level]:
            for cell in e["cells"]:
                usage[(level.name, cell)] += 1

    def exclusive(level, c):
        return [cell for cell in c.cells if usage[(level.name, cell)] == 1]

    corridors = [(lv, c) for lv in dungeon.levels for c in lv.corridors]
    degree = Counter()
    for _, c in corridors:
        degree[c.a.uid] += 1
        degree[c.b.uid] += 1
    linked = {r.uid for link in dungeon.links for r in (link.a, link.b)} | {e["room"].uid for e in dungeon.entrances}

    def priority(item):
        level, c = item
        leaf = (degree[c.a.uid] == 1 and c.a.uid not in linked) or (degree[c.b.uid] == 1 and c.b.uid not in linked)
        return (0 if c.kind == "loop" else 1 if leaf else 2, rng.random())
    corridors.sort(key=priority)

    want = dungeon.params["secrets"]
    passages_wanted = round(want / 3)
    stats = dungeon.stats
    # secret passages: the whole corridor is hidden, both doors are secret
    for level, c in corridors:
        if stats["hidden"] >= passages_wanted:
            break
        cells = exclusive(level, c)
        if (c.feature or len(cells) != len(c.cells) or len(cells) < 3
                or c.door_a.uses != 1 or c.door_b.uses != 1 or c.kind == "tree" and level.sub):
            continue
        c.feature = "hidden"
        for cell in cells:
            level.feat[level.i(*cell)] = "hidden"
        c.door_a.kind = c.door_b.kind = "secret"
        stats["hidden"] += 1
    # secret doors on the other corridors, loops first
    for level, c in corridors:
        if stats["hidden"] + stats["secret_doors"] >= want:
            break
        if c.feature == "hidden":
            continue
        doors = [d for d in (c.door_a, c.door_b) if d.kind != "secret"]
        doors.sort(key=lambda d: (d.uses, rng.random()))
        if doors:
            doors[0].kind = "secret"
            c.secret_door = doors[0]
            stats["secret_doors"] += 1
    # more secrets than corridors: the other door of a corridor, then hidden level connections
    for level, c in corridors:
        if stats["hidden"] + stats["secret_doors"] >= want:
            break
        for d in (c.door_a, c.door_b):
            if d.kind != "secret" and c.feature != "hidden":
                d.kind = "secret"
                stats["secret_doors"] += 1
                break
    for link in sorted(dungeon.links, key=lambda k: (k.kind == "portal", rng.random())):
        if stats["hidden"] + stats["secret_doors"] + stats["secret_links"] >= want:
            break
        link.secret = True
        for level, i in link.cells:
            level.hidden_feats.add(i)
        stats["secret_links"] += 1
    got = stats["hidden"] + stats["secret_doors"] + stats["secret_links"]
    if got < want:
        log.warn(tr("warn_secrets", n=got, want=want))

    # unusual paths on visible corridors, loops first
    visible = [(lv, c) for lv, c in corridors if c.feature is None]
    loops = [(lv, c) for lv, c in visible if c.kind == "loop"]

    def mark(level, c, feature, length):
        cells = exclusive(level, c)
        mid = straight_run(cells, length) if feature == "steps" else (len(cells) // 2 if len(cells) >= length + 2 else None)
        if mid is None:
            return False
        span = cells[mid - length // 2: mid - length // 2 + length]
        if any(level.i(*cell) in level.feat for cell in span):
            return False
        for cell in span:
            level.feat[level.i(*cell)] = feature
        c.feature = feature
        return True

    for feature, how_many, length in (("water", 1 + (len(dungeon.rooms) >= 40), 3),
                                      ("rubble", 1 + (len(dungeon.rooms) >= 30), 1)):
        for level, c in loops + [x for x in visible if x not in loops]:
            if stats[feature] >= how_many:
                break
            if c.feature is None and mark(level, c, feature, length):
                stats[feature] += 1
    # minor elevation shifts: steps in a corridor, about one per main level
    for level in dungeon.levels:
        if level.sub:
            continue
        target = 1 + (len(level.rooms) >= 8)
        done = 0
        pool = [c for c in level.corridors if c.feature is None]
        rng.shuffle(pool)
        for c in pool:
            if done >= target:
                break
            if mark(level, c, "steps", 2):
                done += 1
        if not done:
            # no straight stretch: a single step in a corridor, or else a raised dais in a room
            for c in pool:
                if c.feature is None and mark(level, c, "steps", 1):
                    done = 1
                    break
        if not done:
            for room in sorted(level.rooms, key=lambda r: -len(r.cells)):
                spot = free_spot(level, room, rng)
                if spot:
                    level.feat[level.i(*spot)] = "steps"
                    done = 1
                    break
        stats["steps"] += done

    # pools of water in some caves
    for room in dungeon.rooms:
        if room.era != 0 or rng.random() > 0.4:
            continue
        level = room.level
        x0, y0, x1, y1 = room.box
        cx, cy = rng.randint(x0 + 2, max(x0 + 2, x1 - 2)), rng.choice((y0 + 1, y1 - 1))
        near_doors = {(d.cell[0] + dx, d.cell[1] + dy) for d in room.doors for dx, dy in AROUND}
        for x in range(cx - 2, cx + 3):
            for y in (cy, cy + (1 if cy == y0 + 1 else -1)) if rng.random() < 0.5 else (cy,):
                i = level.i(x, y)
                if (x, y) in room.cells and (x, y) not in near_doors and i not in level.feat and i not in level.labels:
                    level.feat[i] = "water"


# --- checks ---
def traversal_graph(dungeon):
    """Rooms plus "outside": corridors, level links and entrances as edges."""
    edges = []
    for level in dungeon.levels:
        for c in level.corridors:
            edges.append((c.a.uid, c.b.uid))
    for link in dungeon.links:
        edges.append((link.a.uid, link.b.uid))
    for e in dungeon.entrances:
        edges.append(("out", e["room"].uid))
    return edges


def reachable(dungeon):
    graph = {}
    for a, b in traversal_graph(dungeon):
        graph.setdefault(a, set()).add(b)
        graph.setdefault(b, set()).add(a)
    seen, todo = {"out"}, deque(["out"])
    while todo:
        n = todo.popleft()
        for m in graph.get(n, ()):
            if m not in seen:
                seen.add(m)
                todo.append(m)
    return seen


def repair(dungeon, rng):
    """Join any room the corridors missed (A* can fail in a crowded corner)."""
    for _ in range(len(dungeon.rooms) * 2):
        seen = reachable(dungeon)
        lost = [r for r in dungeon.rooms if r.uid not in seen]
        if not lost:
            return True
        room = lost[0]
        level = room.level
        near = sorted([r for r in level.rooms if r.uid in seen and r.comp == room.comp],
                      key=lambda r: math.dist(r.physical(), room.physical()))
        if near and dig(level, room, near[0], rng, "fix", level.region(room.comp)):
            continue
        others = [r for lv in dungeon.levels if lv is not level and abs(lv.depth - level.depth) <= 1
                  for r in lv.rooms if r.uid in seen]
        if not others:
            return False
        add_link(dungeon, "stairs", room, rng.choice(others), rng)
    return not [r for r in dungeon.rooms if r.uid not in reachable(dungeon)]


def jaquays_report(dungeon):
    """Lines describing how each technique was applied."""
    mains = dungeon.mains()
    L = len(mains)
    edges = traversal_graph(dungeon)
    nodes = len(dungeon.rooms) + 1
    loops = len(edges) - nodes + 1
    st = dungeon.stats
    lines = []
    E = len(dungeon.entrances)
    lines.append(("ok", tr("jq_entrances", n=E)) if E >= 2 else ("~", tr("jq_entrances_one")))
    per_level = []
    for level in dungeon.levels:
        parent = {r.uid: r.uid for r in level.rooms}

        def find(x):
            while parent[x] != x:
                x = parent[x]
            return x
        for c in level.corridors:
            parent[find(c.a.uid)] = find(c.b.uid)
        parts = len({find(r.uid) for r in level.rooms})
        per_level.append((level.name, len(level.corridors) - len(level.rooms) + parts))
    every = all(n >= 1 for _, n in per_level)
    lines.append(("ok" if every else "~", tr("jq_loops", n=loops, d=", ".join(f"{name}: {n}" for name, n in per_level))))
    if L >= 2:
        pairs = []
        for d in range(L - 1):
            n = sum(1 for k in dungeon.links if {k.a.level.name, k.b.level.name} == {mains[d].name, mains[d + 1].name})
            pairs.append(f"{d + 1}↔{d + 2}: {n}")
        lines.append(("ok", tr("jq_multi", d=", ".join(pairs))))
    else:
        lines.append(("-", tr("jq_na", what=tr("jq_t_multi"), why=tr("jq_why_one"))))
    disc = [k for k in dungeon.links if not k.a.level.sub and not k.b.level.sub
            and abs(k.a.level.depth - k.b.level.depth) >= 2]
    if L >= 3:
        lines.append(("ok", tr("jq_disc", n=len(disc))))
    else:
        lines.append(("-", tr("jq_na", what=tr("jq_t_disc"), why=tr("jq_why_two") if L == 2 else tr("jq_why_one"))))
    lines.append(("ok", tr("jq_secret", d=st["secret_doors"], p=st["hidden"], h=st["secret_links"], w=st["water"], r=st["rubble"],
                           g=sum(1 for k in dungeon.links if k.kind == "portal"))))
    subs = [lv for lv in dungeon.levels if lv.sub]
    if subs:
        lines.append(("ok", tr("jq_sub", n=", ".join(lv.name for lv in subs))))
    else:
        lines.append(("-", tr("jq_na", what=tr("jq_t_sub"), why=tr("jq_why_small"))))
    div = [lv.name for lv in mains if lv.split is not None]
    if div:
        lines.append(("ok", tr("jq_divided", n=", ".join(div))))
    else:
        lines.append(("-", tr("jq_na", what=tr("jq_t_div"), why=tr("jq_why_one") if L == 1 else tr("jq_why_small"))))
    lines.append(("ok", tr("jq_shifts", n=st["steps"])))
    mid = sum(1 for e in dungeon.entrances if e["midpoint"])
    if mid:
        lines.append(("ok", tr("jq_midpoint", n=mid)))
    else:
        lines.append(("-", tr("jq_na", what=tr("jq_t_mid"), why=tr("jq_why_one") if L == 1 else tr("jq_why_entr"))))
    contacts = sum(1 for lv in dungeon.levels for c in lv.corridors if (c.a.era == 0) != (c.b.era == 0))
    contacts += sum(1 for k in dungeon.links if (k.a.era == 0) != (k.b.era == 0))
    kinds = sum(1 for k in dungeon.links if k.a.level.kind != k.b.level.kind)
    ages = sum(1 for lv in dungeon.levels for c in lv.corridors if c.a.era != c.b.era)
    ages += sum(1 for k in dungeon.links if k.a.era != k.b.era)
    if contacts and any(r.era == 0 for r in dungeon.rooms):
        lines.append(("ok", tr("jq_nested", n=contacts)))
    elif kinds:
        lines.append(("ok", tr("jq_nested_kinds", n=kinds)))
    elif ages:
        lines.append(("ok", tr("jq_nested_ages", n=ages)))
    else:
        lines.append(("-", tr("jq_na", what=tr("jq_t_nest"), why=tr("jq_why_caves"))))
    return lines


def generate(params, log):
    """The whole dungeon, deterministic for a given seed."""
    seed = make_seed(params)
    for attempt in range(8):
        rng = random.Random(f"wyrmdelve-{seed}-{attempt}")
        story = make_story(random.Random(f"wyrmdelve-story-{seed}"), params["types"])
        story["history"] = plan_history(random.Random(f"wyrmdelve-history-{seed}"))
        dungeon = Dungeon(params, story)
        quiet = log if attempt == 0 else QuietLog()
        if attempt == 0:
            log.step(tr("step_story"))
            log.info(tr("info_title", t=pick(story["title"])))
            log.step(tr("step_rooms"))
        build_rooms(dungeon, rng, quiet)
        if attempt == 0:
            log.step(tr("step_corridors"))
        for level in dungeon.levels:
            connect_level(level, rng)
        plan_links(dungeon, rng)
        place_entrances(dungeon, rng)
        no_dead_ends(dungeon, rng)
        if not repair(dungeon, rng) or len(dungeon.entrances) == 0:
            log.warn(tr("info_retry", n=attempt + 1))
            continue
        secret_and_unusual(dungeon, rng, QuietLog() if attempt else log)
        dungeon.corridors = [c for lv in dungeon.levels for c in lv.corridors]
        return dungeon
    sys.exit(tr("err_build"))


# --- fonts ---
def open_font(spec, size):
    path, index = spec if isinstance(spec, tuple) else (spec, 0)
    return ImageFont.truetype(path, size, index=index)


def find_font(chosen=None):
    """Returns (regular, bold or None)."""
    candidates = []
    if chosen:
        candidates.append((chosen, None))
    candidates.append((font_file("DejaVuSansMono.ttf"), font_file("DejaVuSansMono-Bold.ttf")))    # fonts/
    candidates += MONO_FONTS
    try:
        import matplotlib
        base = os.path.join(matplotlib.get_data_path(), "fonts", "ttf")
        candidates.append((os.path.join(base, "DejaVuSansMono.ttf"), os.path.join(base, "DejaVuSansMono-Bold.ttf")))
    except Exception:
        pass
    for regular, bold in candidates:
        try:
            open_font(regular, 20)
        except OSError:
            continue
        try:
            if bold is None:
                raise OSError
            open_font(bold, 20)
        except OSError:
            bold = None
        return regular, bold
    sys.exit(tr("err_no_font"))


def font_name(spec):
    return os.path.basename(spec[0] if isinstance(spec, tuple) else spec)


def font_metrics(spec):
    """Advance and line height, as fractions of the font size."""
    f = open_font(spec, 200)
    ascent, descent = f.getmetrics()
    return f.getlength("M") / 200, (ascent + descent) / 200


def font_has_glyph(font, ch):
    """A missing glyph renders as the .notdef box, so compare with a
    character that surely isn't in the font."""
    def fingerprint(c):
        img = Image.new("L", (80, 80), 0)
        ImageDraw.Draw(img).text((10, 10), c, font=font, fill=255)
        return img.tobytes()
    missing = fingerprint("\U0010FFFD")
    return fingerprint(ch) != missing and any(fingerprint(ch))


class Glyphs:
    """G("≈", "~") -> "≈", or "~" with --ascii-only or if the font lacks ≈."""

    def __init__(self, font, ascii_only):
        self.ascii_only = ascii_only
        self.missing = set()
        self._cache = {}
        self.font = font

    def __call__(self, fancy, plain):
        if self.ascii_only:
            return plain
        if fancy not in self._cache:
            self._cache[fancy] = all(c.isascii() or font_has_glyph(self.font, c) for c in fancy)
            if not self._cache[fancy]:
                self.missing.add(fancy)
        return fancy if self._cache[fancy] else plain


# --- canvas ---
class Canvas:
    """Grid of characters, each with a style: n normal, b bold, i white on black."""

    def __init__(self, width, height):
        self.width, self.height = width, height
        self.chars = [[" "] * width for _ in range(height)]
        self.styles = [["n"] * width for _ in range(height)]

    def put(self, x, y, ch, style="n"):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.chars[y][x], self.styles[y][x] = ch, style

    def write(self, x, y, text, style="n"):
        for i, c in enumerate(text):
            self.put(x + i, y, c, style)

    def paste(self, other, ox, oy):
        for y in range(other.height):
            for x in range(other.width):
                if other.chars[y][x] != " " or other.styles[y][x] != "n":
                    self.put(ox + x, oy + y, other.chars[y][x], other.styles[y][x])

    def lines(self):
        return ["".join(row).rstrip() for row in self.chars]


# box drawing by connections: N=1, E=2, S=4, W=8
DOUBLE_WALLS = " ║═╚║║╔╠═╝═╩╗╣╦╬"
SINGLE_WALLS = " │─└││┌├─┘─┴┐┤┬┼"
WALL_DEFAULTS = {1: "═", 2: "─"}

FEATURE_GLYPHS = {
    "up": ("<", "<"), "down": (">", ">"), "shaft": ("○", "o"), "portal": ("Ω", "&"),
    "pillar": ("■", "O"), "water": ("≈", "~"), "rubble": ("∴", "%"), "steps": ("≡", "="), "hidden": ("░", ":"),
}


def panel_canvas(level, gm, G):
    """One level, framed by its header and the margins for the entrance tags."""
    W, H = level.W, level.H
    floor, era, doors, feat = level.floor, level.era, level.doors, level.feat
    # what can be seen on this map: 1 floor, 2 doorway
    shown = bytearray(W * H)
    for i in range(W * H):
        if floor[i] in (ROOM, CORRIDOR):
            shown[i] = 0 if (not gm and feat.get(i) == "hidden") else 1
        elif floor[i] == DOORWAY:
            shown[i] = 0 if (not gm and doors[i].kind == "secret") else 2

    def is_shown(x, y, what=(1, 2)):
        return 0 <= x < W and 0 <= y < H and shown[y * W + x] in what

    wall = bytearray(W * H)
    for y in range(H):
        for x in range(W):
            if not shown[y * W + x] and any(is_shown(x + dx, y + dy) for dx, dy in AROUND):
                wall[y * W + x] = 1

    def wallish(x, y):
        return 0 <= x < W and 0 <= y < H and (wall[y * W + x] or shown[y * W + x] == 2)

    def wall_era(x, y):
        rooms, corridors = [], []
        for dx, dy in AROUND:
            nx, ny = x + dx, y + dy
            if is_shown(nx, ny):
                j = ny * W + nx
                (rooms if floor[j] in (ROOM, DOORWAY) else corridors).append(era[j])
        for group in (rooms, corridors):
            built = [e for e in group if e in (1, 2)]
            if built:
                return min(built)
            if group:
                return 0
        return 0

    def wall_char(x, y):
        e = wall_era(x, y)
        if e not in (1, 2):
            return "#"
        mask = 0
        if wallish(x, y - 1) and any(is_shown(x + dx, y + dy, (1,)) for dx in (-1, 1) for dy in (0, -1)):
            mask |= 1
        if wallish(x + 1, y) and any(is_shown(x + dx, y + dy, (1,)) for dx in (0, 1) for dy in (-1, 1)):
            mask |= 2
        if wallish(x, y + 1) and any(is_shown(x + dx, y + dy, (1,)) for dx in (-1, 1) for dy in (0, 1)):
            mask |= 4
        if wallish(x - 1, y) and any(is_shown(x + dx, y + dy, (1,)) for dx in (0, -1) for dy in (-1, 1)):
            mask |= 8
        table = DOUBLE_WALLS if e == 1 else SINGLE_WALLS
        ch = table[mask] if mask else WALL_DEFAULTS[e]
        fallback = "#"
        return G(ch, fallback)

    canvas = Canvas(W + 2 * PANEL_MX, H + 3)
    canvas.write(PANEL_MX, 0, level.header(), "b")
    oy = 2
    for y in range(H):
        for x in range(W):
            i = y * W + x
            px, py = PANEL_MX + x, oy + y
            if wall[i]:
                canvas.put(px, py, wall_char(x, y))
            elif shown[i] == 2:
                kind = doors[i].kind
                if kind == "door":
                    canvas.put(px, py, "+")
                elif kind == "secret":
                    canvas.put(px, py, "$", "b")
                else:
                    canvas.put(px, py, ".")
            elif shown[i] == 1:
                if gm and i in level.labels:
                    canvas.put(px, py, level.labels[i], "b")
                elif feat.get(i) == "tag":
                    pass
                elif i in feat and (gm or (feat[i] != "hidden" and i not in level.hidden_feats)):
                    fancy, plain = FEATURE_GLYPHS[feat[i]]
                    canvas.put(px, py, G(fancy, plain), "b" if feat[i] in ("up", "down", "shaft", "portal") else "n")
                else:
                    canvas.put(px, py, ".")
    for letter, (x, y) in level.inner_tags:
        canvas.put(PANEL_MX + x, oy + y, letter, "i")
    for letter, (x, y), (dx, dy) in level.exits:
        tag = f"[{letter}]"
        if dx == -1:
            canvas.write(PANEL_MX - 4, oy + y, tag, "i")
        elif dx == 1:
            canvas.write(PANEL_MX + W + 1, oy + y, tag, "i")
        elif dy == -1:
            canvas.write(PANEL_MX + x - 1, oy - 1, tag, "i")
        else:
            canvas.write(PANEL_MX + x - 1, oy + H, tag, "i")
    return canvas


def content_bounds(canvas):
    rows = [y for y in range(1, canvas.height) if any(c != " " for c in canvas.chars[y])]
    cols = [x for x in range(canvas.width) for y in rows if canvas.chars[y][x] != " "]
    return min(cols), min(rows), max(cols), max(rows)


def trim_panel(canvas, bounds):
    """Drop the empty rock around the level: header on top, then the drawing.
    Both maps use the GM map's bounds, so they line up."""
    x0, y0, x1, y1 = bounds
    header = "".join(canvas.chars[0]).strip()
    out = Canvas(max(x1 - x0 + 1, len(header)), y1 - y0 + 3)
    out.write(0, 0, header, "b")
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            out.put(x - x0, y - y0 + 2, canvas.chars[y][x], canvas.styles[y][x])
    return out


# --- grid scale: only written on the maps and in the key, the dungeon doesn't change ---
UNIT_NAMES = {"imperial": "imperial", "imperiale": "imperial", "feet": "imperial", "foot": "imperial", "ft": "imperial",
              "piedi": "imperial", "metric": "metric", "metrica": "metric", "metrico": "metric", "meters": "metric",
              "metres": "metric", "metri": "metric", "m": "metric"}


def read_units(text):
    units = UNIT_NAMES.get(text.strip().lower())
    if units is None:
        raise argparse.ArgumentTypeError(tr("err_units", s=text))
    return units


def default_units():
    return "metric" if LANG == "it" else "imperial"


def scale_text(units):
    return tr("scale_metric" if units == "metric" else "scale_imperial")


def legend_entries(dungeon, gm, G, units):
    """[(text, style), ...] per entry; only what this dungeon actually has."""
    feats = {f for lv in dungeon.levels for f in lv.feat.values()}
    kinds = {d.kind for lv in dungeon.levels for d in lv.doors.values()}
    eras = {r.era for r in dungeon.rooms} | {c.era for c in dungeon.corridors}
    out = []
    if 1 in eras:
        out.append([(G("═║", "##"), "n"), (" " + tr("lg_era1"), "n")])
    if 2 in eras:
        out.append([(G("─│", "##"), "n"), (" " + tr("lg_era2"), "n")])
    if eras & {0, 3}:
        out.append([("#", "n"), (" " + tr("lg_era0"), "n")])
    out.append([(".", "n"), (" " + tr("lg_floor"), "n")])
    if "door" in kinds:
        out.append([("+", "n"), (" " + tr("lg_door"), "n")])
    if gm and "secret" in kinds:
        out.append([("$", "b"), (" " + tr("lg_secret_door"), "n")])
    if gm and "hidden" in feats:
        out.append([(G("░", ":"), "n"), (" " + tr("lg_hidden"), "n")])
    if feats & {"up", "down"}:
        out.append([("< >", "b"), (" " + tr("lg_stairs"), "n")])
    for key, label in (("steps", "lg_steps"), ("shaft", "lg_shaft"), ("portal", "lg_portal"), ("water", "lg_water"),
                       ("rubble", "lg_rubble"), ("pillar", "lg_pillar")):
        if key in feats:
            fancy, plain = FEATURE_GLYPHS[key]
            out.append([(G(fancy, plain), "b" if key in ("shaft", "portal") else "n"), (" " + tr(label), "n")])
    out.append([("[A]", "i"), (" " + tr("lg_entrance"), "n")])
    if gm:
        mains = dungeon.mains()
        out.append([(f"{mains[0].name}-01", "b"), (" " + tr("lg_room"), "n")])
    out.append([(tr("lg_scale"), "b"), (" " + scale_text(units), "n")])
    return out


def pack_legend(entries, width):
    lines, line, used = [], [], 0
    for entry in entries:
        w = sum(len(t) for t, _ in entry)
        extra = w + (4 if line else 0)
        if line and used + extra > width:
            lines.append(line)
            line, used = [], 0
            extra = w
        line.append(entry)
        used += extra
    if line:
        lines.append(line)
    return lines


def legend_width(line):
    return sum(len(t) for entry in line for t, _ in entry) + 4 * (len(line) - 1)


class Layout:
    """How the page is put together: panel grid, legend, size in letters."""

    def __init__(self, dungeon, panels, pc, legend, title, subtitle):
        self.panels, self.pc = panels, pc
        self.pr = math.ceil(len(panels) / pc)
        self.panel_w = max(p.width for p in panels)
        self.panel_h = max(p.height for p in panels)
        grid_w = pc * self.panel_w + (pc - 1) * GAP_X
        grid_h = self.pr * self.panel_h + (self.pr - 1) * GAP_Y
        inner = max(grid_w, len(title) + 4, len(subtitle) + 4, 60)
        self.legend = pack_legend(legend, inner)
        self.title, self.subtitle = title, subtitle
        self.grid_w, self.grid_h = grid_w, grid_h
        self.cols = inner + 4
        self.top = 4 if title else 3            # no name: the subtitle moves up a row
        self.rows = self.top + 1 + grid_h + 1 + len(self.legend) + 1


def page_layouts(dungeon, panels, legend, title, subtitle):
    out = []
    n = len(panels)
    for pc in range(1, n + 1):
        if pc > 1 and math.ceil(n / pc) == math.ceil(n / (pc - 1)):
            continue
        out.append(Layout(dungeon, panels, pc, legend, title, subtitle))
    return out


def compose_page(layout):
    page = Canvas(layout.cols, layout.rows)
    t, s = layout.title, layout.subtitle
    if t:
        page.write((layout.cols - len(t)) // 2, 1, t, "b")
    page.write((layout.cols - len(s)) // 2, layout.top - 2, s)
    x0, y0 = (layout.cols - layout.grid_w) // 2, layout.top
    for k, panel in enumerate(layout.panels):
        r, c = divmod(k, layout.pc)
        px = x0 + c * (layout.panel_w + GAP_X) + (layout.panel_w - panel.width) // 2
        py = y0 + r * (layout.panel_h + GAP_Y)
        page.paste(panel, px, py)
    y = y0 + layout.grid_h + 1
    for line in layout.legend:
        x = (layout.cols - legend_width(line)) // 2
        for n, entry in enumerate(line):
            if n:
                x += 4
            for text, style in entry:
                page.write(x, y, text, style)
                x += len(text)
        y += 1
    return page


# --- paper ---
def paper_pixels(paper, orientation):
    w_mm, h_mm = PAPERS[paper]
    if orientation == "landscape":
        w_mm, h_mm = h_mm, w_mm
    return round(mm(w_mm)), round(mm(h_mm))


VALID_SIZES = {paper_pixels(p, o) for p in PAPERS for o in ("portrait", "landscape")}


def fit(layout, paper, aspect):
    """Best orientation for one layout on one paper: (char_mm, fill, orientation)."""
    short, long_ = PAPERS[paper]
    max_char = MAX_CHAR_MM * short / PAPERS["A4"][0]
    best = None
    for name, (w_mm, h_mm) in (("portrait", (short, long_)), ("landscape", (long_, short))):
        page_w, page_h = w_mm - 2 * MARGIN_MM, h_mm - 2 * MARGIN_MM
        char_mm = min(page_w / layout.cols, page_h / (layout.rows * aspect), max_char)
        filled = (layout.cols * char_mm) * (layout.rows * char_mm * aspect) / (page_w * page_h)
        option = (char_mm, filled, name)
        if best is None or char_mm > best[0] * 1.08 or (char_mm >= best[0] * 0.92 and filled > best[1]):
            best = option
    return best


def choose_sheet(layouts, paper, aspect):
    """Best (layout, char_mm, orientation) for a paper: biggest letters, then fuller sheet."""
    best = None
    for layout in layouts:
        char_mm, filled, orientation = fit(layout, paper, aspect)
        if best is None or char_mm > best[1] * 1.03 or (char_mm >= best[1] * 0.97 and filled > best[3]):
            best = (layout, char_mm, orientation, filled)
    return best[:3]


def choose_sheets(sheets, paper, aspect):
    """Best (layout, char_mm, orientation) for every sheet on one paper. All
    sheets get the smallest of their letter sizes, so they match."""
    picks = [choose_sheet(layouts, paper, aspect) for layouts in sheets]
    char_mm = min(char for _, char, _ in picks)
    return [(layout, char_mm, orientation) for layout, _, orientation in picks]


def suggest_paper(sheets, aspect):
    options = {paper: choose_sheets(sheets, paper, aspect) for paper in PAPERS}
    readable = [p for p in PAPERS if options[p][0][1] >= GOOD_CHAR_MM]
    return (readable[0] if readable else list(PAPERS)[-1]), options


def ask_paper(sheets, aspect, wanted, ask_user, log):
    """sheets: for every sheet, the layouts it may use. Returns the paper and,
    for every sheet, (layout, char_mm, orientation)."""
    suggested, options = suggest_paper(sheets, aspect)
    if len(sheets) == 1:
        any_layout = options[suggested][0][0]
        log.info(tr("info_paper_intro", nc=any_layout.cols, nr=any_layout.rows))
    else:
        biggest = max((layout for layout, _, _ in options[suggested]), key=lambda lay: lay.cols * lay.rows)
        log.info(tr("info_paper_intro_levels", nc=biggest.cols, nr=biggest.rows))
    for paper, picks in options.items():
        layout, char_mm, orientation = picks[0]
        if char_mm < SMALL_CHAR_MM:
            verdict = tr("v_too_small")
        elif char_mm < GOOD_CHAR_MM:
            verdict = tr("v_small")
        else:
            verdict = tr("v_good")
        note = tr("suggested") if paper == suggested else ""
        if len(sheets) == 1:
            log.info(tr("info_paper_option", paper=paper, o=tr("orientation_" + orientation), pc=layout.pc,
                        pr=layout.pr, mm=char_mm, v=verdict, note=note))
        else:
            log.info(tr("info_paper_option_levels", paper=paper, n=len(picks), mm=char_mm, v=verdict, note=note))
    default = wanted or suggested
    if ask_user:
        print()
        print(tr("paper_choice"))
        while True:
            answer = input(tr("q_paper", default=default)).strip().upper()
            if not answer:
                break
            if answer in PAPERS:
                default = answer
                break
            print(tr("paper_retry"))
    return default, options[default]


# --- rendering and saving ---
def pixel_layout(layout, paper, orientation, char_mm, fonts):
    font_spec, bold_spec, advance_em, _ = fonts
    width, height = paper_pixels(paper, orientation)
    area_w, area_h = width - 2 * mm(MARGIN_MM), height - 2 * mm(MARGIN_MM)
    size = max(6, int(mm(char_mm) / advance_em))
    while True:
        regular = open_font(font_spec, size)
        char_w = regular.getlength("M")
        ascent, descent = regular.getmetrics()
        char_h = ascent + descent
        if (layout.cols * char_w <= area_w and layout.rows * char_h <= area_h) or size <= 6:
            break
        size -= 1
    bold = open_font(bold_spec, size) if bold_spec else None
    ox, oy = (width - layout.cols * char_w) / 2, (height - layout.rows * char_h) / 2
    return regular, bold, char_w, char_h, size, width, height, ox, oy


def render(canvas, regular, bold, char_w, char_h, size, width, height, ox, oy, progress=None):
    """Rasterise in grayscale: 0 = ink, 255 = paper (colours come later)."""
    img = Image.new("L", (width, height), 255)
    d = ImageDraw.Draw(img)
    thicken = max(1, size // 22)
    real_bold = bold is not None
    probe = bold.font_variant(size=40) if real_bold else None
    bold_can_draw = {}

    def draw_bold(px, py, ch):
        if real_bold:
            if ch not in bold_can_draw:
                bold_can_draw[ch] = ch.isascii() or font_has_glyph(probe, ch)
            if bold_can_draw[ch]:
                d.text((px, py), ch, font=bold, fill=0, anchor="la")
                return
        d.text((px, py), ch, font=regular, fill=0, anchor="la")
        d.text((px + thicken, py), ch, font=regular, fill=0, anchor="la")

    for y in range(canvas.height):
        py = oy + y * char_h
        for x in range(canvas.width):
            ch, style = canvas.chars[y][x], canvas.styles[y][x]
            if ch == " " and style != "i":
                continue
            px = ox + x * char_w
            if style == "i":
                # the [ ] only make sense in the .txt
                d.rectangle([px, py, px + char_w + 0.5, py + char_h + 0.5], fill=0)
                if ch not in "[] ":
                    d.text((px, py), ch, font=bold or regular, fill=255, anchor="la")
            elif style == "b":
                draw_bold(px, py, ch)
            else:
                d.text((px, py), ch, font=regular, fill=0, anchor="la")
        if progress:
            progress((y + 1) / canvas.height)
    return img


def colorize(img, scheme):
    """Grey levels become a blend from ink to paper, so the antialiasing
    survives. Turns the picture into a palette PNG in place: no extra memory."""
    if scheme == 1:
        return img
    ink, paper = COLOR_SCHEMES[scheme]
    palette = []
    for v in range(256):
        t = v / 255
        palette += [round(ink[k] * (1 - t) + paper[k] * t) for k in range(3)]
    img.putpalette(palette)
    return img


def check_size(img, path):
    """Every sheet must be exactly A4/A3/A2/A1 at 600 dpi."""
    if img.size not in VALID_SIZES:
        raise ValueError(tr("err_size", path=path, size=img.size))


def save_png(img, path, settings=None):
    check_size(img, path)
    info = PngInfo()
    if settings:
        info.add_itxt(SETTINGS_KEY, json.dumps(settings, ensure_ascii=False))
    img.save(path, dpi=(DPI, DPI), pnginfo=info)


def pdf_text(text):
    return "<" + ("\ufeff" + text).encode("utf-16-be").hex().upper() + ">"


class PdfFile:
    """A minimal PDF, one 600 dpi picture per page, Flate-compressed so it stays
    lossless (Pillow's own PDF saves greys as JPEG and palettes uncompressed).
    Pages are written as they come, so only one sheet is in memory at a time."""

    def __init__(self, path, settings=None):
        self.path, self.settings = path, settings
        self.f = open(path, "wb")
        self.f.write(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
        self.offsets = {}
        self.next_id = 3            # 1 catalog, 2 page tree
        self.pages = []

    def new_id(self):
        self.next_id += 1
        return self.next_id - 1

    def begin(self, oid):
        self.offsets[oid] = self.f.tell()
        self.f.write(f"{oid} 0 obj\n".encode())

    def obj(self, oid, body):
        self.begin(oid)
        self.f.write(body.encode("latin-1") + b"\nendobj\n")

    def add_page(self, img):
        check_size(img, self.path)
        w, h = img.size
        if img.mode == "P":
            palette = bytes(img.getpalette()[:768]).ljust(768, b"\0")
            space = f"[/Indexed /DeviceRGB 255 <{palette.hex().upper()}>]"
        else:
            img = img.convert("L")
            space = "/DeviceGray"
        image_id, length_id = self.new_id(), self.new_id()
        self.begin(image_id)
        self.f.write((f"<< /Type /XObject /Subtype /Image /Width {w} /Height {h} /ColorSpace {space} "
                      f"/BitsPerComponent 8 /Filter /FlateDecode /Length {length_id} 0 R >>\nstream\n").encode())
        start, packer = self.f.tell(), zlib.compressobj(6)
        for y in range(0, h, 256):
            self.f.write(packer.compress(img.crop((0, y, w, min(h, y + 256))).tobytes()))
        self.f.write(packer.flush())
        length = self.f.tell() - start
        self.f.write(b"\nendstream\nendobj\n")
        self.obj(length_id, str(length))
        pw, ph = w / DPI * 72, h / DPI * 72
        draw = f"q {pw:.3f} 0 0 {ph:.3f} 0 0 cm /Im0 Do Q"
        content_id, page_id = self.new_id(), self.new_id()
        self.obj(content_id, f"<< /Length {len(draw)} >>\nstream\n{draw}\nendstream")
        self.obj(page_id, f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {pw:.3f} {ph:.3f}] "
                          f"/Resources << /XObject << /Im0 {image_id} 0 R >> >> /Contents {content_id} 0 R >>")
        self.pages.append(page_id)

    def close(self):
        kids = " ".join(f"{p} 0 R" for p in self.pages)
        self.obj(2, f"<< /Type /Pages /Kids [{kids}] /Count {len(self.pages)} >>")
        self.obj(1, "<< /Type /Catalog /Pages 2 0 R >>")
        info_id = self.new_id()
        info = f"/Creator {pdf_text('WyrmDelve v' + VERSION)}"
        if self.settings:
            info += f" /Subject {pdf_text(json.dumps(self.settings, ensure_ascii=False))}"
        self.obj(info_id, f"<< {info} >>")
        xref = self.f.tell()
        self.f.write(f"xref\n0 {self.next_id}\n0000000000 65535 f \n".encode())
        for oid in range(1, self.next_id):
            self.f.write(f"{self.offsets[oid]:010d} 00000 n \n".encode())
        self.f.write(f"trailer\n<< /Size {self.next_id} /Root 1 0 R /Info {info_id} 0 R >>\n"
                     f"startxref\n{xref}\n%%EOF\n".encode())
        self.f.close()


def draw_sheet(canvas, pixels, scheme):
    live = LiveBar()
    drawing = tr("pb_drawing")
    img = render(canvas, *pixels, progress=lambda done: live.update(0.85 * done, drawing))
    live.update(0.85, tr("pb_saving"))
    return colorize(img, scheme), live


def write_text(path, canvases):
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n\n\n".join("\n".join(c.lines()) for c in canvases) + "\n")


def save_map(pages, base, pdf, scheme, settings, log):
    """pages: (canvas, pixels, suffix) for every sheet. PNG: one PNG + TXT per
    sheet. PDF: one PDF with every sheet, and one TXT."""
    if pdf:
        doc = PdfFile(base + ".pdf", settings)
        for canvas, pixels, _ in pages:
            img, live = draw_sheet(canvas, pixels, scheme)
            doc.add_page(img)
            del img
            live.finish()
        doc.close()
        write_text(base + ".txt", [canvas for canvas, _, _ in pages])
        log.info(tr("saved", a=short_path(base + ".pdf"), b=short_path(base + ".txt")))
        return
    for canvas, pixels, suffix in pages:
        img, live = draw_sheet(canvas, pixels, scheme)
        save_png(img, base + suffix + ".png", settings)
        del img
        write_text(base + suffix + ".txt", [canvas])
        live.finish()
        log.info(tr("saved", a=short_path(base + suffix + ".png"), b=short_path(base + suffix + ".txt")))


# --- the key ---
def wrap(text, width, indent=""):
    words, lines, line = text.split(), [], indent
    for w in words:
        if len(line) + len(w) + 1 > width and line.strip():
            lines.append(line.rstrip())
            line = indent
        line += w + " "
    if line.strip():
        lines.append(line.rstrip())
    return lines


def room_text(room):
    first_era, first = room.layers[0]
    text = pick(first)
    text = text[0].upper() + text[1:]
    for era, layer in room.layers[1:]:
        text += f"; {ERA_TAGS[era]}: {pick(layer)}"
    return f"[{ERA_TAGS[first_era]}] {text}."


def room_exits(dungeon, room):
    out = []
    level = room.level
    for c in level.corridors:
        if room not in (c.a, c.b):
            continue
        door = c.door_of(room)
        how = [tr("ex_" + ("secret" if door.kind == "secret" else door.kind))]
        if c.feature == "hidden":
            how = [tr("ex_hidden")]
        elif c.feature in ("water", "rubble", "steps"):
            how.append(tr("ex_" + c.feature))
        out.append(f"→ {c.other(room).label} ({', '.join(how)})")
    for link in dungeon.links:
        if room not in (link.a, link.b):
            continue
        other = link.other(room)
        if link.kind == "stairs":
            what = tr("ex_down") if other.level.depth > room.level.depth else tr("ex_up")
        else:
            what = tr("ex_" + link.kind)
        gap = abs(other.level.depth - room.level.depth)
        skip = ""
        if link.kind != "portal" and gap >= 2 and not other.level.sub and not room.level.sub:
            skip = tr("ex_skips_one") if gap == 2 else tr("ex_skips", n=int(gap - 1))
        hidden = tr("ex_hidden_link") if link.secret else ""
        out.append(f"{what} → {other.label}{skip}{hidden}")
    for e in dungeon.entrances:
        if e["room"] is room:
            out.append(tr("ex_entrance", l=e["letter"]))
    return out


def fits_level(monster, kind):
    where = monster.get("where", ["*"])
    return "*" in where or kind in where


def monster_label(monster):
    name = capitalized(pick(monster["name"]))
    return f"{name} ({monster['number']})" if monster.get("number") else name


def find_quirk(dungeon, level, danger, taken, rng):
    """An unexpected monster for this level and the reason it is here, from
    what the dungeon really has (flooded caves, a portal, a deeper level...):
    (monster index, reason (it, en)) or None."""
    mains = dungeon.mains()
    wet = sorted((lv for lv in dungeon.levels if lv is not level and "water" in lv.feat.values()
                  and any(r.era == 0 for r in lv.rooms)),
                 key=lambda lv: (lv.depth < level.depth, abs(lv.depth - level.depth)))   # deeper ones first
    portals = [r for k in dungeon.links if k.kind == "portal" for r in (k.a, k.b) if r.level is not level]
    d = int(level.depth)
    below = mains[d + 1] if d + 1 < len(mains) and mains[d + 1].kind != level.kind else None
    options = []
    for quirk in QUIRKS:
        when, values = quirk.get("when", "any"), {"from": ("", ""), "room": ("", ""), "level": ("", "")}
        home = None
        if when == "water":
            if not wet:
                continue
            values["from"] = tuple(TEXTS["quirk_from"][i].format(n=wet[0].name) for i in range(2))
        elif when == "portal":
            if not portals:
                continue
            values["room"] = (portals[0].label, portals[0].label)
        elif when == "below":
            if below is None:
                continue
            values["level"] = (below.name, below.name)
            home = below.kind
        elif when == "founders":
            if not any(r.era == 1 for r in level.rooms):
                continue
        elif when != "any":
            continue
        options.append((quirk, values, home))
    rng.shuffle(options)
    for quirk, values, home in options:
        kinds = quirk.get("kinds") or []
        pool = [k for k, m in enumerate(MONSTERS) if k not in taken and (not kinds or m.get("kind") in kinds)
                and not fits_level(m, level.kind) and (home is None or fits_level(m, home))
                and m.get("danger", 2) <= danger + 2]
        if pool:
            reason = tuple(quirk["text"][i].format(**{k: v[i] for k, v in values.items()}) for i in range(2))
            return rng.choice(sorted(pool)), reason
    return None


def plan_monsters(dungeon, seed):
    """For every level: a d6 table of wandering monsters (today's dwellers, then
    monsters that fit the level's type, more dangerous the deeper the level,
    sometimes one out of place) and what is in every room: monsters (in about a
    third of the rooms, never in all), a clue in an empty room near each of
    them, or nothing. Its own random numbers: map and story never change."""
    rng = random.Random(f"wyrmdelve-monsters-{seed}")
    step = min(1.0, 3 / max(1, len(dungeon.mains()) - 1))     # danger grows by at most one per level
    dwellers = capitalized(pick(dungeon.story["p_who"]))
    used = set()
    wander, rooms = {}, {}
    for level in dungeon.levels:
        danger = 1 + round(level.depth * step)
        fits = [k for k, m in enumerate(MONSTERS) if fits_level(m, level.kind)]
        chosen = []
        # the right danger first, then one step off, then anything of this type, then anything at all
        for pool in ([k for k in fits if MONSTERS[k].get("danger", 2) == danger],
                     [k for k in fits if abs(MONSTERS[k].get("danger", 2) - danger) == 1], fits, range(len(MONSTERS))):
            fresh = [k for k in pool if k not in chosen and k not in used]
            again = [k for k in pool if k not in chosen and k in used]
            for group in (fresh, again):
                rng.shuffle(group)
                chosen += group[:5 - len(chosen)]
            if len(chosen) >= 5:
                break
        quirk = find_quirk(dungeon, level, danger, used | set(chosen), rng) if rng.random() < 0.3 else None
        used.update(chosen)

        # rooms: about a third with monsters, at least a third always empty
        order = sorted(level.rooms, key=lambda r: r.number)
        rng.shuffle(order)
        n = len(order)
        busy = min(max(1, round(n * 0.35)), n - max(1, math.ceil(n / 3)))
        homes = []                                  # (room, what, kind, reason)
        lairs = [r for r in order if any(era == 3 for era, _ in r.layers)]
        for room in lairs[:max(1, busy // 2) - (1 if quirk and busy == 1 else 0)]:     # an odd guest needs a room too
            homes.append((room, ("dwellers", dwellers), "dwellers", None))
        free = [r for r in order if r not in [h[0] for h in homes]]
        if quirk and len(homes) < busy and free:
            k, reason = quirk
            built = [r for r in free if r.era in (1, 2)] or free
            homes.append((built[0], ("monster", k), MONSTERS[k].get("kind"), reason))
            used.add(k)
            free.remove(built[0])
        for k in chosen:
            if len(homes) >= busy or not free:
                break
            homes.append((free.pop(0), ("monster", k), MONSTERS[k].get("kind"), None))
        for room, what, kind, reason in homes:
            if what[0] == "dwellers":
                text = tr("room_lair", m=f"{pick(dungeon.story['p_who'])} (2d6)")
            else:
                text = tr("room_monsters", m=monster_label(MONSTERS[what[1]]))
                if reason:
                    text += " " + tr("room_quirk", r=pick(reason))
            rooms[room.uid] = text
        # a clue in an empty room close to every monster: joined by a corridor if possible
        for room, what, kind, _ in homes:
            near = {c.other(room) for c in level.corridors if room in (c.a, c.b)}
            empty = [r for r in order if r.uid not in rooms]
            if not empty or not CLUES.get(kind):
                continue
            spot = min(empty, key=lambda r: (r not in near, r.comp != room.comp,
                                             math.dist(r.physical(), room.physical())))
            rooms[spot.uid] = tr("room_clue", c=pick(rng.choice(CLUES[kind])), r=room.label)
        for room in order:
            rooms.setdefault(room.uid, tr("room_empty"))

        rows = [(dwellers, tr("wander_dwellers"))]
        rows += [(capitalized(pick(MONSTERS[k]["name"])), pick(MONSTERS[k]["text"])) for k in chosen]
        if quirk:
            k = quirk[0]
            home = next(r.label for r, what, _, _ in homes if what == ("monster", k)) if any(
                what == ("monster", k) for _, what, _, _ in homes) else level.name
            rows[-1] = (capitalized(pick(MONSTERS[k]["name"])), pick(MONSTERS[k]["text"]) + tr("wander_quirk", r=home))
        wander[level.name] = rows
    return wander, rooms


def key_blocks(dungeon, seed, title, units, story_on=True, monsters_on=True):
    """The dungeon key as blocks, shared by the .txt and the PDF:
    ("title", text) ("meta", text) ("h", txt, pdf) ("p", text) ("stratum", tag, text, walls, note)
    ("entrance", text) ("link", a, b, kind) ("level", txt, pdf, note) ("note", text) ("wander", rows)
    ("room", label, text, exits, extra) ("check", mark, text). Without the story there is no
    history, no strata and no room descriptions; without monsters, no tables and no room contents."""
    story = dungeon.story
    blocks = [("title", title), ("meta", f"{tr('key_seed')}: {seed}"),
              ("meta", f"{tr('key_types')}: {types_text(dungeon.params['types'])}"),
              ("meta", f"{tr('key_scale')}: {scale_text(units)}")]
    if story_on:
        blocks += [("h", tr("key_history"), tr("pdf_history")), ("p", pick(history_text(dungeon)))]
        blocks.append(("h", tr("key_strata"), tr("pdf_strata")))
        eras = {r.era for r in dungeon.rooms}
        strata = [(0, pick(("Grotte naturali, più antiche di ogni costruzione", "Natural caves, older than any building")), "#"),
                  (1, pick(story["f_who"]) + " — " + pick(story["built"]), "═║"),
                  (2, pick(story["s_who"]), "─│"),
                  (3, pick(("oggi: ", "today: ")) + pick(story["p_who"]), "#")]
        for era, text, walls in strata:
            note = "" if era in eras or era == 3 else pick(("nessuna stanza", "no rooms"))
            blocks.append(("stratum", ERA_TAGS[era], text, walls, note))
    blocks.append(("h", tr("key_entrances"), tr("pdf_entrances")))
    for e in dungeon.entrances:
        mid = tr("key_midpoint") if e["midpoint"] else ""
        blocks.append(("entrance", tr("key_entrance_line", l=e["letter"], kind=pick(e["kind"]), lv=e["level"].name,
                                      mid=mid, room=e["room"].label)))
    if dungeon.links:
        blocks.append(("h", tr("key_links"), tr("pdf_links")))
        for link in dungeon.links:
            a, b = sorted((link.a, link.b), key=lambda r: r.level.depth)
            hidden = tr("ex_hidden_link") if link.secret else ""
            blocks.append(("link", a.label, b.label, tr("link_" + link.kind) + hidden))
    mains = dungeon.mains()
    wandering, contents = plan_monsters(dungeon, seed) if monsters_on and MONSTERS else ({}, {})
    for level in dungeon.levels:
        kind = type_name(level.kind)
        if level.sub:
            d = int(level.depth)
            txt = (tr("key_sublevel", n=level.name, a=mains[d].name, b=mains[d + 1].name) if d + 1 < len(mains)
                   else tr("key_sublevel_one", n=level.name))
            note = (tr("pdf_sub_between", a=mains[d].name, b=mains[d + 1].name) if d + 1 < len(mains)
                    else tr("pdf_sub_below"))
            blocks.append(("level", txt + " — " + kind.upper(), tr("pdf_sublevel", n=level.name) + " — " + kind, note))
        else:
            blocks.append(("level", tr("key_level", n=level.name) + " — " + kind.upper(),
                           tr("pdf_level", n=level.name) + " — " + kind, ""))
        if level.split is not None:
            blocks.append(("note", tr("key_divided")))
        if level.name in wandering:
            blocks.append(("wander", wandering[level.name]))
        for room in sorted(level.rooms, key=lambda r: r.number):
            text = room_text(room) if story_on else ""
            extra = [contents[room.uid]] if room.uid in contents else []
            blocks.append(("room", room.label, text, room_exits(dungeon, room), extra))
    blocks.append(("h", tr("key_jaquays"), tr("pdf_jaquays")))
    for mark, text in jaquays_report(dungeon):
        blocks.append(("check", mark, text))
    return blocks


def write_key(blocks, path):
    """The key as plain text, 100 letters wide."""
    width = 100
    lines = []
    for block in blocks:
        kind = block[0]
        if kind in ("h", "level"):
            lines += ["", block[1]]
        elif kind == "title":
            lines.append(f"WyrmDelve v{VERSION}" + (f" — {block[1]}" if block[1] else ""))
        elif kind == "meta":
            lines.append(block[1])
        elif kind in ("p", "note"):
            lines += wrap(block[1], width, "  ")
        elif kind == "stratum":
            _, tag, text, walls, note = block
            lines.append(f"  {tag:<4}{text}  [{walls}]" + (f"  ({note})" if note else ""))
        elif kind == "entrance":
            lines.append("  " + block[1])
        elif kind == "link":
            _, a, b, what = block
            lines.append(f"  {a:<6} ↔ {b:<6} {what}")
        elif kind == "room":
            _, label, text, exits, extra = block
            if not text and extra:
                text, extra = extra[0], extra[1:]
            lines += wrap(f"{label:<6} {text}", width, "  ")
            for line in extra:
                lines += wrap(line, width, "         ")
            if exits:
                lines += wrap(tr("key_exits") + ": " + "; ".join(exits), width, "         ")
        elif kind == "wander":
            lines.append("  " + tr("key_wander"))
            for n, (name, text) in enumerate(block[1], 1):
                rows = wrap(f"{name}: {text}.", width - 7, "       ")
                lines += [f"    {n}. " + rows[0].strip()] + rows[1:]
        elif kind == "check":
            mark, text = block[1], block[2]
            lines.append(f"  {'✓' if mark == 'ok' else '~' if mark == '~' else '–'} {text}")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


# --- the story PDF ---
FONT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")


def font_file(name):
    return os.path.join(FONT_DIR, name)


STORY_FONTS = ("Sebaldus-Gotisch.ttf", "CrimsonText-Regular.ttf", "CrimsonText-Italic.ttf", "CrimsonText-Bold.ttf",
               "CrimsonText-BoldItalic.ttf", "DejaVuSans.ttf")


def missing_story_fonts():
    return [name for name in STORY_FONTS if not os.path.isfile(font_file(name))]


def story_pdf_problem():
    """Why the story PDF can't be made (missing fonts, missing or old fpdf2), or None."""
    missing = missing_story_fonts()
    if missing:
        return tr("err_story_fonts", f=", ".join(missing), d=short_path(FONT_DIR))
    try:
        import fpdf
    except ImportError:
        return tr("err_no_fpdf")
    version = getattr(fpdf, "__version__", None) or getattr(fpdf, "FPDF_VERSION", "")
    try:
        numbers = tuple(int(x) for x in version.split(".")[:3])
    except ValueError:
        numbers = (0,)
    # the old PyFPDF uses the same module name; fpdf2 2.7.6+ has what we need
    if numbers < (2, 7, 6) or not hasattr(fpdf.FPDF, "set_fallback_fonts"):
        return tr("err_old_fpdf", v=version or "?")
    return None


def write_story_pdf(blocks, path, settings):
    """The key as an A4 book page: Sebaldus-Gotisch headings, Crimson Text body.
    Needs fpdf2 (in requirements.txt); fonts come only from fonts/."""
    from fpdf import FPDF

    class Page(FPDF):
        def footer(self):
            self.set_y(-14)
            self.set_font("crimson", "I", 9)
            self.set_text_color(90)
            self.cell(0, 6, f"WyrmDelve v{VERSION} · {self.page_no()}", align="C")
            self.set_text_color(0)

    pdf = Page(format="A4", unit="mm")
    pdf.set_margins(22, 20, 22)
    pdf.set_auto_page_break(True, 20)
    pdf.add_font("gothic", "", font_file("Sebaldus-Gotisch.ttf"))
    for style, name in (("", "Regular"), ("I", "Italic"), ("B", "Bold"), ("BI", "BoldItalic")):
        pdf.add_font("crimson", style, font_file(f"CrimsonText-{name}.ttf"))
    pdf.add_font("dejavu", "", font_file("DejaVuSans.ttf"))
    pdf.set_fallback_fonts(["dejavu"], exact_match=False)
    pdf.set_creator(f"WyrmDelve v{VERSION}")
    pdf.set_subject(json.dumps(settings, ensure_ascii=False))
    pdf.add_page()
    width = pdf.w - pdf.l_margin - pdf.r_margin

    def rule():
        y = pdf.get_y() + 1
        pdf.set_draw_color(120)
        pdf.line(pdf.l_margin + width * 0.3, y, pdf.l_margin + width * 0.7, y)
        pdf.set_draw_color(0)
        pdf.ln(4)

    for block in blocks:
        kind = block[0]
        if kind == "title":
            pdf.set_title(block[1] or "WyrmDelve")
            pdf.set_font("gothic", "", 30)
            pdf.multi_cell(0, 13, block[1] or "WyrmDelve", align="C", new_x="LMARGIN", new_y="NEXT")
            pdf.ln(2)
        elif kind == "meta":
            pdf.set_font("crimson", "I", 11)
            pdf.multi_cell(0, 5.5, block[1], align="C", new_x="LMARGIN", new_y="NEXT")
        elif kind == "h":
            if block[1] == tr("key_history"):
                pdf.ln(2)
                rule()
            pdf.ln(3)
            pdf.set_font("gothic", "", 19)
            pdf.multi_cell(0, 9, block[2], new_x="LMARGIN", new_y="NEXT")
            pdf.ln(1)
        elif kind == "level":
            pdf.ln(4)
            pdf.set_font("gothic", "", 16)
            pdf.multi_cell(0, 8, block[2], new_x="LMARGIN", new_y="NEXT")
            if block[3]:
                pdf.set_font("crimson", "I", 10.5)
                pdf.multi_cell(0, 5, block[3], new_x="LMARGIN", new_y="NEXT")
            pdf.ln(1)
        elif kind == "p":
            pdf.set_font("crimson", "", 12)
            pdf.multi_cell(0, 6, block[1], align="J", new_x="LMARGIN", new_y="NEXT")
            pdf.ln(1)
        elif kind == "note":
            pdf.set_font("crimson", "I", 10.5)
            pdf.multi_cell(0, 5, block[1], new_x="LMARGIN", new_y="NEXT")
            pdf.ln(1)
        elif kind == "stratum":
            _, tag, text, walls, note = block
            pdf.set_font("crimson", "", 11.5)
            extra = f"  __({note})__" if note else ""
            pdf.multi_cell(0, 6, f"**{tag}**  {text}  {walls}{extra}", markdown=True, new_x="LMARGIN", new_y="NEXT")
        elif kind == "entrance":
            pdf.set_font("crimson", "", 11.5)
            pdf.multi_cell(0, 6, block[1], new_x="LMARGIN", new_y="NEXT")
        elif kind == "link":
            _, a, b, what = block
            pdf.set_font("crimson", "", 11.5)
            pdf.multi_cell(0, 6, f"**{a}** ↔ **{b}**  {what}", markdown=True, new_x="LMARGIN", new_y="NEXT")
        elif kind == "room":
            _, label, text, exits, extra = block
            if not text and extra:
                text, extra = extra[0], extra[1:]
            pdf.set_font("crimson", "", 11.5)
            pdf.multi_cell(0, 5.8, f"**{label}**  {text}", markdown=True, new_x="LMARGIN", new_y="NEXT")
            for line in extra:
                pdf.set_x(pdf.l_margin + 8)
                pdf.set_font("crimson", "", 10.5)
                pdf.multi_cell(width - 8, 5.2, line, new_x="LMARGIN", new_y="NEXT")
            if exits:
                pdf.set_x(pdf.l_margin + 8)
                pdf.set_font("crimson", "I", 10)
                pdf.multi_cell(width - 8, 5, tr("key_exits").capitalize() + ": " + "; ".join(exits), new_x="LMARGIN", new_y="NEXT")
            pdf.ln(1.2)
        elif kind == "wander":
            pdf.set_font("crimson", "BI", 11)
            pdf.multi_cell(0, 6, tr("key_wander"), new_x="LMARGIN", new_y="NEXT")
            pdf.set_font("crimson", "", 10.5)
            for n, (name, text) in enumerate(block[1], 1):
                pdf.set_x(pdf.l_margin + 4)
                pdf.multi_cell(width - 4, 5.2, f"**{n}.** {name}: {text}.", markdown=True,
                               new_x="LMARGIN", new_y="NEXT")
            pdf.ln(2)
        elif kind == "check":
            mark, text = block[1], block[2]
            pdf.set_font("crimson", "", 10.5)
            pdf.multi_cell(0, 5.2, f"{'✓' if mark == 'ok' else '~' if mark == '~' else '–'} {text}", new_x="LMARGIN", new_y="NEXT")
    pdf.output(path)


# --- files and folders ---
OUTPUT_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dungeons_generated")


def short_path(path):
    try:
        rel = os.path.relpath(path)
    except ValueError:
        return path
    return rel if not rel.startswith("..") else path


# --- welcome screen and questions ---
TITLE_ART = r"""
 _       __                     ____       __
| |     / /_  ___________ ___  / __ \___  / /   _____
| | /| / / / / / ___/ __ `__ \/ / / / _ \/ / | / / _ \
| |/ |/ / /_/ / /  / / / / / / /_/ /  __/ /| |/ /  __/
|__/|__/\__, /_/  /_/ /_/ /_/_____/\___/_/ |___/\___/
       /____/
"""

ORCO_DUNGEON = r"""
      *         :       :       :       :       :          *
  . (     . . . . .           . . . . . . . . . . . .  . (    .
   ) )  *   :       :  (__)         :   `   :    /  :   ) )  *
  ( ( )  .. . . .   _--) _(__   . . . . . . . . . . .  ( ( )  .
 ` )`(      ;    /¯¯  ( {φ}) \  :       :       :     ` )`(
  \~~~/   . .   /(  )  \ ~/  ))   . . . . . . . . . .  \~~~/  .
   |≡|   ´  :  / |`´).  ¯¯. / )    /:       :       :   |≡|   ´
. .\_/. .\. .  | | /       /\ |   . . . . . . . . . . . \_/ . .
:   |   :      | ||       |  ||  .      :       :       :|
. .[=]. . . .  ├ππ\\ππ¢ππππ┤ ||  |\   . . . . . . . . . [=] . .
    |       :  |   \\---.  | ||  | \        :       :    |  :
. . . . . .   =====(_(≡=====(((≡=XXXX>  . . . . . . . . . . . .
:       :      ||         ||    ´/    \      `  :       :
=============  ||         ||     `----´  =======================
    /      /   /\          \\   |      \      \   | σ       \
  /         /  ¯¯            ¯¯           \       ´√))θ       \
      /            /            |            \     / \    \
"""


def terminal_width():
    try:
        return os.get_terminal_size(sys.stdout.fileno()).columns
    except (OSError, ValueError):
        return None


def show_welcome():
    """Title, the ogre in his dungeon, and the first question: Enter = random."""
    art = ORCO_DUNGEON.strip("\n").split("\n")
    title = TITLE_ART.strip("\n").split("\n")
    subtitle = f"v{VERSION}  ·  " + tr("welcome_subtitle")
    width = max(max(len(line) for line in art), max(len(line) for line in title), len(subtitle)) + 4
    columns = terminal_width()
    if columns and columns <= width:
        width = columns - 1
    title_width = max(len(line) for line in title)
    art_width = max(len(line) for line in art)
    screen = [
        "═" * width,
        "",
        *[" " * max(0, (width - title_width) // 2) + line for line in title],
        "",
        " " * max(0, (width - len(subtitle)) // 2) + subtitle,
        "",
        "═" * width,
        *[(" " * max(0, (width - art_width) // 2) + line)[:width] for line in art],
        "═" * width,
    ]
    print("\n" + "\n".join(line.rstrip() for line in screen) + "\n")
    answer = input(tr("press_enter")).strip().lower()
    print()
    if answer.startswith(tr("letter_params")):
        return "params"
    if answer.startswith(tr("letter_rebuild")):
        return "rebuild"
    return "random"


def ask(question, default, kind=int, lowest=None, highest=None):
    """Keep asking until the answer is valid. Enter = default."""
    while True:
        answer = input(f"  {question} [{default}]: ").strip()
        if not answer:
            return default
        try:
            value = kind(answer)
        except ValueError:
            print(tr("invalid_value"))
            continue
        if (lowest is not None and value < lowest) or (highest is not None and value > highest):
            print(tr("value_range", lo=lowest, hi=highest))
            continue
        return value


def ask_colors(default=1):
    print(tr("colors_intro"))
    for k in (1, 2, 3):
        print(tr(f"color_{k}"))
    return ask(tr("choice"), default, int, 1, 3)


def ask_output(levels, per_level, pdf):
    """Before the paper: all levels on one sheet or one per sheet, then PNG or
    PDF. None means ask (only on a terminal; otherwise one sheet, PNG)."""
    asking = sys.stdin.isatty()
    if levels < 2:
        per_level = False
    elif per_level is None:
        per_level = False
        if asking:
            print(tr("sheets_intro"))
            print(tr("sheets_1"))
            print(tr("sheets_2"))
            per_level = ask(tr("choice"), 1, int, 1, 2) == 2
    if pdf is None:
        pdf = False
        if asking:
            many = "many" if per_level else "one"
            print(tr("output_intro"))
            print(tr("output_png_" + many))
            print(tr("output_pdf_" + many))
            pdf = ask(tr("choice"), 1, int, 1, 2) == 2
    return per_level, pdf


def print_types(allowed):
    for k, t in enumerate(TYPES, 1):
        if t["id"] in allowed:
            print(f"    {k:>2} = {pick(t['menu'])}")
    print(tr("type_random"))


def ask_type(allowed, rng):
    """One type among the allowed ones; 0 = at random."""
    print_types(allowed)
    while True:
        k = ask(tr("choice"), 0, int, 0, len(TYPES))
        if k == 0:
            return rng.choice(allowed)
        if TYPES[k - 1]["id"] in allowed:
            return TYPES[k - 1]["id"]
        print(tr("type_not_allowed"))


def ask_types(levels):
    """The type of every level, top to bottom: the same for all, or one each
    (only the types that can stand below the previous level are offered)."""
    rng = random.Random()
    every = [t["id"] for t in TYPES]
    if levels > 1:
        print(tr("types_same_intro"))
        print(tr("types_same"))
        print(tr("types_each"))
        if ask(tr("choice"), 1, int, 1, 2) == 2:
            types = []
            for d in range(levels):
                if types:
                    print(tr("types_level_intro", n=d + 1, above=type_name(types[-1])))
                else:
                    print(tr("types_level_first"))
                types.append(ask_type(TYPE[types[-1]]["below"] if types else every, rng))
            return types
    print(tr("types_intro"))
    return [ask_type(every, rng)] * levels


def ask_name():
    """None = a random name (the dungeon's own), "" = no name, else the user's."""
    print(tr("name_intro"))
    print(tr("name_yes"))
    print(tr("name_no"))
    if ask(tr("choice"), 1, int, 1, 2) == 2:
        return ""
    print(tr("name_how"))
    print(tr("name_random"))
    print(tr("name_mine"))
    if ask(tr("choice"), 1, int, 1, 2) == 1:
        return None
    while True:
        name = input(tr("q_name")).strip()
        if name:
            return name
        print(tr("name_empty"))


CONTENTS = {1: (False, False), 2: (True, False), 3: (False, True), 4: (True, True)}    # (story, monsters)
CONTENT_NAMES = {"mappa": 1, "map": 1, "storia": 2, "story": 2, "mostri": 3, "monsters": 3, "tutto": 4, "all": 4}


def read_content(text):
    choice = CONTENT_NAMES.get(text.strip().lower())
    if choice is None:
        raise argparse.ArgumentTypeError(tr("err_content", s=text))
    return choice


def ask_content():
    """(story, monsters)."""
    print(tr("content_intro"))
    for k in CONTENTS:
        print(tr(f"content_{k}"))
    return CONTENTS[ask(tr("choice"), 4, int, 1, 4)]


def ask_units():
    print(tr("units_intro"))
    print(tr("units_1"))
    print(tr("units_2"))
    default = 2 if default_units() == "metric" else 1
    return "metric" if ask(tr("choice"), default, int, 1, 2) == 2 else "imperial"


def ask_settings():
    ask_language()
    mode = show_welcome()
    print(tr("enter_accepts"))
    p = {"title": None, "ascii_only": False, "font": None, "paper": None, "output": OUTPUT_FOLDER, "story": True,
         "monsters": True,
         "per_level": None, "pdf": None, "units": None}
    if mode == "rebuild":
        while True:
            text = input(tr("ask_seed", example=example_seed()))
            seed = read_seed(text)
            if seed:
                break
            print(tr("seed_invalid", example=example_seed()))
            problem = seed_problem(text)
            if problem:
                print("    " + problem)
        p.update(seed)
        p["randomized"] = False
    elif mode == "params":
        lo, hi = LIMITS["levels"]
        levels = ask(tr("q_levels"), DEFAULTS["levels"], int, lo, hi)
        rooms = ask(tr("q_rooms"), max(DEFAULTS["rooms"], MIN_PER_LEVEL * levels), int, MIN_PER_LEVEL * levels,
                    LIMITS["rooms"][1])
        entrances = ask(tr("q_entrances"), min(DEFAULTS["entrances"], rooms), int, 1, min(LIMITS["entrances"][1], rooms))
        hidden = ask(tr("q_secrets"), DEFAULTS["secrets"], int, *LIMITS["secrets"])
        types = ask_types(levels)
        p.update({"levels": levels, "rooms": rooms, "entrances": entrances, "secrets": hidden, "types": types,
                  "number": new_number(), "randomized": False})
    else:
        p.update(random_params(new_number()))
        p["randomized"] = True
    p["colors"] = ask_colors()
    p["title"] = ask_name()
    p["story"], p["monsters"] = ask_content()
    p["units"] = ask_units()
    p["ask_paper"] = sys.stdin.isatty()
    return p


def settings_from_options(argv):
    """Command line. Every option has an Italian and an English name;
    --help lists the current language's first."""
    language_from_options(argv)

    def names(italian, english):
        return (f"--{italian}", f"--{english}") if LANG == "it" else (f"--{english}", f"--{italian}")
    ap = argparse.ArgumentParser(description=tr("h_description"), epilog=tr("h_epilog"))
    ap.add_argument(*names("lingua", "language"), dest="language", default=LANG, metavar="{it,en}",
                    help=tr("h_language"))
    ap.add_argument(*names("livelli", "levels"), dest="levels", type=int, default=None, help=tr("h_levels"))
    ap.add_argument(*names("stanze", "rooms"), dest="rooms", type=int, default=None, help=tr("h_rooms"))
    ap.add_argument(*names("ingressi", "entrances"), dest="entrances", type=int, default=None, help=tr("h_entrances"))
    ap.add_argument(*names("segreti", "secrets"), dest="secrets", type=int, default=None, help=tr("h_secrets"))
    ap.add_argument(*names("colori", "colors"), dest="colors", type=int, choices=(1, 2, 3), default=1,
                    help=tr("h_colors"))
    ap.add_argument(*names("seme", "seed"), dest="seed", default=None, help=tr("h_seed"))
    ap.add_argument(*names("tipo", "type"), dest="types", default=None, metavar="N[,N...]", help=tr("h_type"))
    ap.add_argument(*names("formato", "format"), dest="paper", type=str.upper, choices=list(PAPERS), default=None,
                    help=tr("h_format"))
    sheets = ap.add_mutually_exclusive_group()
    sheets.add_argument(*names("per-livello", "per-level"), dest="per_level", action="store_const", const=True,
                        default=None, help=tr("h_per_level"))
    sheets.add_argument(*names("un-foglio", "one-sheet"), dest="per_level", action="store_const", const=False,
                        help=tr("h_one_sheet"))
    files = ap.add_mutually_exclusive_group()
    files.add_argument("--pdf", dest="pdf", action="store_const", const=True, default=None, help=tr("h_pdf"))
    files.add_argument("--png", dest="pdf", action="store_const", const=False, help=tr("h_png"))
    naming = ap.add_mutually_exclusive_group()
    naming.add_argument(*names("titolo", "title"), dest="title", default=None, help=tr("h_title"))
    naming.add_argument(*names("senza-titolo", "no-title"), dest="title", action="store_const", const="",
                        help=tr("h_no_title"))
    ap.add_argument(*names("contenuto", "content"), dest="content", type=read_content, default=None,
                    metavar="{map,story,monsters,all}" if LANG == "en" else "{mappa,storia,mostri,tutto}",
                    help=tr("h_content"))
    ap.add_argument(*names("senza-storia", "no-story"), dest="no_story", action="store_true", help=tr("h_no_story"))
    ap.add_argument(*names("unita", "units"), dest="units", type=read_units, default=None,
                    metavar="{imperial,metric}" if LANG == "en" else "{imperiale,metrica}", help=tr("h_units"))
    ap.add_argument(*names("solo-ascii", "ascii-only"), dest="ascii_only", action="store_true", help=tr("h_ascii"))
    ap.add_argument("--font", default=None, metavar="FILE", help=tr("h_font"))
    ap.add_argument(*names("uscita", "output"), dest="output", default=OUTPUT_FOLDER, help=tr("h_output"))
    a = ap.parse_args(argv)
    p = {"title": a.title, "ascii_only": a.ascii_only, "font": a.font, "paper": a.paper, "output": a.output,
         "colors": a.colors, "per_level": a.per_level, "pdf": a.pdf, "units": a.units}
    p["story"], p["monsters"] = CONTENTS[1 if a.no_story else a.content or 4]
    fixed = {k: v for k, v in (("levels", a.levels), ("rooms", a.rooms), ("entrances", a.entrances),
                               ("secrets", a.secrets)) if v is not None}
    if a.types:
        try:
            numbers = [int(x) for x in a.types.replace(" ", "").split(",")]
        except ValueError:
            numbers = [0]
        if any(not 1 <= k <= len(TYPES) for k in numbers):
            ap.error(tr("err_type_value", s=a.types, n=len(TYPES)))
        fixed["types"] = [TYPES[k - 1]["id"] for k in numbers]
        if len(numbers) > 1:
            fixed.setdefault("levels", len(numbers))
    if a.seed:
        seed = read_seed(a.seed)
        if seed:
            p.update(seed)
            p["randomized"] = False
        else:
            number = from_code(a.seed) if not a.seed.isdigit() else int(a.seed) % (32 ** CODE_LENGTH)
            if number is None:
                problem = seed_problem(a.seed)
                ap.error(tr("err_seed", s=a.seed) + (" — " + problem if problem else ""))
            p.update(random_params(number, fixed))
            p["randomized"] = len(fixed) < 4
    else:
        p.update(random_params(new_number(), fixed))
        p["randomized"] = len(fixed) < 4
    error = check_params(p)
    if error:
        ap.error(error)
    p["ask_paper"] = a.paper is None and sys.stdin.isatty()
    return p


# --- main ---
def main():
    interactive = len(sys.argv) == 1
    params = ask_settings() if interactive else settings_from_options(sys.argv[1:])
    log = Log(10)

    # 1: settings
    log.step(tr("step_settings"))
    seed = make_seed(params)
    log.info(tr("info_seed", s=seed))
    log.info(tr("info_params", l=params["levels"], r=params["rooms"], e=params["entrances"], x=params["secrets"]))
    if params.get("randomized"):
        log.info(tr("info_random"))
    log.info(tr("info_types", t=types_text(params["types"])))
    log.info(tr("info_colors", c=tr(f"color_name_{params['colors']}")))
    if params["title"] == "":
        log.info(tr("info_name_none"))
    units = params.get("units") or default_units()
    log.info(tr("info_units", s=scale_text(units)))
    keyed = params["story"] or params["monsters"]
    log.info(tr("info_content_" + str({v: k for k, v in CONTENTS.items()}[(params["story"], params["monsters"])])))
    if keyed and story_pdf_problem():
        log.error(story_pdf_problem())      # say it now too, not only at the end
    if params["title"]:
        log.info(tr("info_name_mine", t=params["title"]))
    folder = os.path.join(params["output"], seed)
    os.makedirs(folder, exist_ok=True)
    log.info(tr("info_folder", folder=short_path(folder)))
    font_spec, bold_spec = find_font(params["font"])
    advance_em, line_em = font_metrics(font_spec)
    aspect = line_em / advance_em
    log.info(tr("info_font", name=font_name(font_spec), fake="" if bold_spec else tr("fake_bold"), a=aspect))

    # 2-4: story, rooms, corridors
    dungeon = generate(params, log)
    loops = sum(1 for c in dungeon.corridors if c.kind == "loop")
    log.info(tr("info_corridors", c=len(dungeon.corridors), l=loops))

    # 5: level connections and entrances
    log.step(tr("step_links"))
    kinds = Counter(k.kind for k in dungeon.links)
    log.info(tr("info_links", s=kinds["stairs"], p=kinds["shaft"], g=kinds["portal"], e=len(dungeon.entrances)))

    # 6: secrets
    log.step(tr("step_secrets"))
    st = dungeon.stats
    log.info(tr("info_secrets", d=st["secret_doors"], p=st["hidden"], h=st["secret_links"], w=st["water"], r=st["rubble"], s=st["steps"]))

    # 7: Jaquays
    log.step(tr("step_check"))
    log.info(tr("info_reach", n=len(dungeon.rooms)))
    for mark, text in jaquays_report(dungeon):
        log.info(("✓ " if mark == "ok" else "~ " if mark == "~" else "– ") + text)

    # 8: paper
    log.step(tr("step_paper"))
    G = Glyphs(open_font(font_spec, 40), params["ascii_only"])
    title = pick(dungeon.story["title"]) if params["title"] is None else params["title"]
    L = len(dungeon.mains())
    subtitle = (tr("subtitle", seed=seed, l=L, r=len(dungeon.rooms), e=len(dungeon.entrances)) if L > 1 else
                tr("subtitle_one", seed=seed, r=len(dungeon.rooms), e=len(dungeon.entrances)))
    gm_full = [panel_canvas(lv, True, G) for lv in dungeon.levels]
    bounds = [content_bounds(p) for p in gm_full]
    gm_panels = [trim_panel(p, b) for p, b in zip(gm_full, bounds)]
    per_level, pdf = ask_output(len(dungeon.levels), params["per_level"], params["pdf"])
    params["per_level"], params["pdf"] = per_level, pdf
    files = "PDF" if pdf else "PNG"
    if per_level:
        log.info(tr("info_sheets_levels", n=len(dungeon.levels), f=files))
        groups = [[k] for k in range(len(dungeon.levels))]
    else:
        log.info(tr("info_sheets_one", f=files) if len(dungeon.levels) > 1 else tr("info_files", f=files))
        groups = [list(range(len(dungeon.levels)))]
    gm_legend = legend_entries(dungeon, True, G, units)
    sheets = [page_layouts(dungeon, [gm_panels[k] for k in group], gm_legend, title, subtitle) for group in groups]
    paper, picks = ask_paper(sheets, aspect, params["paper"], params.pop("ask_paper", False), log)
    params["paper"] = paper
    fonts = (font_spec, bold_spec, advance_em, aspect)
    gm_pixels = [pixel_layout(layout, paper, orientation, char_mm, fonts) for layout, char_mm, orientation in picks]
    printed_mm = min(pixels[2] for pixels in gm_pixels) / DPI * 25.4
    if per_level:
        log.info(tr("info_letters", mm=printed_mm, dpi=DPI))
        for group, (_, _, orientation), pixels in zip(groups, picks, gm_pixels):
            log.info(tr("info_sheet_level", lv=dungeon.levels[group[0]].header(), paper=paper,
                        o=tr("orientation_" + orientation), w=pixels[5], h=pixels[6]))
    else:
        orientation, pixels = picks[0][2], gm_pixels[0]
        log.info(tr("info_sheet", paper=paper, o=tr("orientation_" + orientation), w=pixels[5], h=pixels[6],
                    dpi=DPI, mm=printed_mm))
    if printed_mm < SMALL_CHAR_MM:
        log.warn(tr("warn_tiny"))
    settings = {"seed": seed, "colors": params["colors"], "paper": paper, "title": params["title"],
                "language": LANG, "ascii_only": params["ascii_only"], "per_level": per_level, "pdf": pdf,
                "units": units, "version": VERSION}
    suffixes = [f"_L{dungeon.levels[g[0]].name}" if per_level else "" for g in groups]

    # 9: GM map
    log.step(tr("step_gm", paper=paper, dpi=DPI, f=files))
    gm_pages = [(compose_page(layout), pixels, suffix)
                for (layout, _, _), pixels, suffix in zip(picks, gm_pixels, suffixes)]
    save_map(gm_pages, os.path.join(folder, f"{seed}_gm"), pdf, params["colors"], settings, log)
    del gm_pages

    # 10: players' map (same layout and letter size) and key
    log.step(tr("step_players" if keyed else "step_players_only"))
    pl_panels = [trim_panel(panel_canvas(lv, False, G), b) for lv, b in zip(dungeon.levels, bounds)]
    pl_legend = legend_entries(dungeon, False, G, units)
    pl_pages = []
    for group, (layout, char_mm, orientation), suffix in zip(groups, picks, suffixes):
        pl_layout = Layout(dungeon, [pl_panels[k] for k in group], layout.pc, pl_legend,
                           tr("players_title", t=title) if title else tr("players_title_plain"), subtitle)
        pl_pages.append((compose_page(pl_layout), pixel_layout(pl_layout, paper, orientation, char_mm, fonts), suffix))
    save_map(pl_pages, os.path.join(folder, f"{seed}_players"), pdf, params["colors"], settings, log)
    if keyed:
        blocks = key_blocks(dungeon, seed, title, units, params["story"], params["monsters"])
        key_path = os.path.join(folder, f"{seed}_key.txt")
        write_key(blocks, key_path)
        log.info(tr("saved_key", a=short_path(key_path)))
        # the book: the story, or (maps and monsters only) the monster key
        story_path = os.path.join(folder, f"{seed}_{'story' if params['story'] else 'monsters'}.pdf")
        problem = story_pdf_problem()
        if problem:
            log.error(problem)
        else:
            try:
                write_story_pdf(blocks, story_path, settings)
                log.info(tr("saved_story" if params["story"] else "saved_monsters", a=short_path(story_path)))
            except Exception as e:          # never lose the maps and the key over the PDF
                log.error(tr("err_story_pdf", e=f"{type(e).__name__}: {e}"))
    if G.missing:
        log.warn(tr("warn_missing_glyphs", g=" ".join(sorted(G.missing))))
    log.done()


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(errors="replace")
    except AttributeError:
        pass
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print(tr("interrupted"))
        sys.exit(1)
