# WyrmDelve

<div align="center">

[Italiano](README.it.md) · **English**

</div>

<table align="center"><tr><td><pre>
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
. . . . . .   =====(_(≡=====(((≡=XXXX&gt;  . . . . . . . . . . . .
:       :      ||         ||    ´/    \      `  :       :
=============  ||         ||     `----´  =======================
    /      /   /\          \\   |      \      \   | σ       \
  /         /  ¯¯            ¯¯           \       ´√))θ       \
      /            /            |            \     / \    \
</pre></td></tr></table>

<div align="center">

<img src="img_examples/OSR%20LOGO.png" alt="OSR logo" width="25%"><br>
Works with any analogue "OSR" roleplaying game. Sibling of [WyrmHex](https://github.com/alepersichetti/WyrmHex).

</div>

### WyrmDelve v0.0.1

**WyrmDelve** draws random dungeons and labyrinths for old school (OSR) campaigns, made only of letters and symbols like the roguelikes NetHack, Angband, ADOM, Brogue, Caves of Qud and Dwarf Fortress.

Every dungeon has a **layered history**, and the walls show it:

| Walls | Stratum |
|---|---|
| `#` (irregular caves) | **N** — natural caves, older than any building |
| `═║╔╗` | **I** — the founders (kings, knights, priests, wizards, legions, dwarves…) |
| `─│┌┐` | **II** — those who came next (cultists, smugglers, a necromancer, goblins, monks) |
| `#` (rough-hewn rooms) | **III** — today's dwellers (an ogre, orcs, the undead, spiders, troglodytes) |

Rooms are numbered **level-room**: `1-01`, `2-07`, and `1a-01` on a sub-level. The dungeon key tells what each room was for in each age (e.g. *Throne hall; II: gambling den; III: ogre's lair*).

Every level is one of **11 dungeon types**, each with its own floor plan, rooms, builders and entrances:

| # | Type | Floor plan |
|---|---|---|
| 1 | Ancient palace | symmetrical about an axis, the throne hall in the middle, wings in mirrored pairs |
| 2 | Dungeon or prison of intelligent or arcane creatures | rows of small cells, guard rooms at the ends, a pit in the middle |
| 3 | Tower | round rooms packed around a central stair |
| 4 | Castle | buildings around a courtyard, round towers at the corners, the keep |
| 5 | Temple | a long nave on the axis with the apse at its head, side chapels in pairs |
| 6 | City | packed buildings, streets between them, a square in the middle |
| 7 | Wizard's alchemical or arcane dungeon | round and octagonal rooms around a summoning circle |
| 8 | Magical or religious academy | identical classrooms around a cloister, a library and a great hall |
| 9 | Border fortress | a long walled line, bastions at the ends, the keep in the middle, the gate |
| 10 | Tomb or crypt | a processional axis from the antechamber to the burial chamber, niches in pairs |
| 11 | Underdark or underground caves | natural caverns anywhere, one great cavern |

The levels **stack coherently**: a tower can stand on a castle but never under a cave, a crypt lies under a temple and never above a castle, and the Underdark is always at the bottom. The main entrance is on the ground level (the lowest building above ground, or the top level underground).

The layout **always** follows Jennell Jaquays' principles as Justin Alexander describes them in *Xandering the Dungeon*: multiple entrances, loops, multiple and discontinuous level connections, secret and unusual paths (secret doors and passages, hidden stairs, flooded passages, cave-ins, portals), sub-levels, divided levels, minor elevation shifts, midpoint entries, nested dungeons. When it's done, the program checks that every room can be reached and prints which principles it applied.

---

## 1. What you need

Put these files in the **same folder**, for example a folder called `dungeons` on your Desktop:

- `wyrmdelve.py` (the program)
- `wyrmdelve_tables.json` (the words the dungeons are made of: names, rooms, history; see chapter 7)
- `requirements.txt` (the list of what the program needs)
- `README.md` (this guide) and `README.it.md` (the same guide in Italian)

You don't need to create anything else: the program creates the `dungeons_generated` folder, where your dungeons are saved, the first time you use it.

You also need **Python**, the program that runs `.py` files: version **3.8 or newer** (the latest one is best).

---

## 2. Installation

You do this only **once**. It takes about five minutes.

### Step 1 — Install Python

- **Windows and macOS:** go to <https://www.python.org/downloads/>, download the latest version and install it like any other program.
  - On Windows, if the installer shows a box called **"Add python.exe to PATH"**, tick it.
- **Linux:** Python is usually already installed.

### Step 2 — Open the terminal in the folder with the files

The terminal is a window where you type commands. Don't worry: you'll only ever copy and paste the commands in this guide. After pasting a command, press **Enter** to run it.

- **Windows 11:** open the `dungeons` folder, right-click an empty spot and choose **"Open in Terminal"**.
- **Windows 10:** open the `dungeons` folder, click the address bar at the top, type `cmd` and press Enter.
- **macOS:** open the **Terminal** app (in Applications → Utilities). Type `cd` followed by a space, drag the `dungeons` folder into the window and press Enter.
- **Linux:** open the folder, right-click an empty spot and choose **"Open in Terminal"**.

### Step 3 — Create the virtual environment (recommended)

The program gets a private space inside the folder, called a *virtual environment*: a hidden subfolder named `.venv`, which you should leave alone. That way the libraries it needs don't mix with the rest of your computer, and if something goes wrong you can just delete `.venv` and start again. Type:

**Windows**
```
py -m venv .venv
```

**macOS and Linux**
```
python3 -m venv .venv
```

Nothing shows up on screen: that's normal. You only do this once.

### Step 4 — Activate the virtual environment

Activating it tells the terminal to use the Python inside `.venv`. Type:

**Windows**
```
.venv\Scripts\activate
```

**macOS and Linux**
```
source .venv/bin/activate
```

From now on, the line where you type starts with `(.venv)`: that's how you know it's active. You need to activate it again every time you open a new terminal (see chapter 3).

### Step 5 — Install the libraries

With the virtual environment active, download **Pillow**, the library that creates the pictures. The command is the same on every system:

```
pip install -r requirements.txt
```

If you see a line starting with `Successfully installed` at the end, you're all set. You only do this once.

---

## 3. Making a dungeon

Open the terminal in the folder, as in step 2. First activate the virtual environment (as in step 4), then start the program:

**Windows**
```
.venv\Scripts\activate
python wyrmdelve.py
```

**macOS and Linux**
```
source .venv/bin/activate
python wyrmdelve.py
```

You only need to activate it once each time you open a terminal: while the line starts with `(.venv)`, it is active and you can make as many dungeons as you like with `python wyrmdelve.py`. When you're done, type `deactivate` or just close the terminal. If you've just finished the installation in the same window, the environment is already active.

The program asks you a few questions. **Every question has a ready-made answer in square brackets: if you're happy with it, just press Enter.**

1. **Language:** type `1` for Italian or `2` for English (pressing Enter keeps Italian). From then on the questions, the messages and the texts on the map are in the language you chose.
2. **The ogre shows up in his dungeon.** Press **Enter** for a fully random dungeon, type **P** to choose the parameters yourself, or **R** to rebuild a dungeon you already made (see chapter 4).
3. With **P** you choose: number of levels, number of rooms (at least 2 per level), number of entrances/exits to the area, number of secret doors and passages. Then the **dungeon type** (see the table at the top; `0` = at random). With more than one level, the program first asks whether **all levels are of the same type** or **each level has its own type**: in that case you choose them one by one from the top, and for each level the list only shows the types that can stand below the one above.

   With **Enter** (fully random dungeon) the program chooses the types by itself, always in a coherent order.
4. **Colours:**
   1. black symbols on white (the ready-made answer, best for printing)
   2. white symbols on light blue
   3. white symbols on black
5. **Do you want a name on the map?** If not, the map has no title. If so, choose whether it's **randomly generated** (e.g. *Tomb of Zordur*, the ready-made answer) or whether **you type it**.

Now the program builds the dungeon. It shows each step with a bar that fills up:

```
[████░░░░░░]  4/10  Corridors and loops
```

Then it asks the last three questions:

6. **How to lay out the levels:**
   1. all levels on **one sheet** (the ready-made answer)
   2. **one level per sheet**, in separate files

   With a single level this question is skipped.
7. **Which files you want:** a **PNG** image (one per sheet) or a **PDF** (with one level per sheet, a single PDF holding every sheet: handy for printing everything at once).
8. **Print format:** the program shows a table with **A4, A3, A2 and A1**: for each, how big the letters will be and whether they're easy to read. The ready-made answer in brackets is the **suggested format**, the smallest sheet where the map reads well. Press Enter to accept it or type another format, for example `A3`. For example:

   ```
   · A4  landscape  levels 2x2   1.29 mm letters   small
   · A3  landscape  levels 2x2   1.88 mm letters   readable   <- suggested
   · A2  landscape  levels 2x2   2.71 mm letters   readable
   · A1  landscape  levels 2x2   3.89 mm letters   readable
   ```

   The picture is always **600 dpi** and the sheet turns portrait or landscape by itself.

At the end the program says where it saved the files and `Done in ... s`.

---

## 4. Rebuilding a dungeon you already made

Every dungeon has a **seed**, a code like `3-24-2-5-CDK-K7Q2MB` (levels-rooms-entrances-secrets-types-code). The types are one letter per level from the top, `A` to `K` in the order of the table at the top (`CDK` = tower, castle, Underdark); a single letter means every level is of that type. Seeds from older versions, without the types, still work. It's printed under the title of the map, and it's also the name of the dungeon's folder inside `dungeons_generated`. **The same seed always gives the same dungeon.**

To make it again (for example on another paper format, or with other colours), start the program, type **R** on the ogre screen and write the seed. Capitals don't matter, and O and 0, or I, L and 1, count as the same character.

---

## 5. The files you get

Everything goes in `dungeons_generated/<seed>/`, one folder per dungeon:

| File | What's in it |
|---|---|
| `<seed>_gm.png` | the **game master's map**: room numbers, secret doors `S` and secret passages `░` |
| `<seed>_players.png` | the **players' map**: same map, without numbers and secrets |
| `<seed>_key.txt` | the **dungeon key**: history, strata, entrances, level connections, what's in each room, Jaquays check |
| `.txt` next to each map | the same map as plain text, to open with any text editor |

With **one level per sheet** the PNG names get the level: `<seed>_gm_L1.png`, `<seed>_gm_L2a.png`… All sheets use the same letter size, so the levels keep the same scale. With **PDF** you get `<seed>_gm.pdf` and `<seed>_players.pdf` instead (one page per sheet, 600 dpi, no loss of quality), each with its `.txt`.

### Symbols

| Symbol | Meaning | Symbol | Meaning |
|---|---|---|---|
| `.` | floor | `+` | door |
| `S` | secret door (GM only) | `░` | secret passage (GM only) |
| `<` `>` | stairs up / down | `≡` | steps, same level |
| `○` | shaft or chimney between levels (may skip some) | `Ω` | magic portal |
| `≈` | water | `∴` | cave-in |
| `■` | pillar | `[A]` | entrance (solid box on the map) |

---

## 6. Printing

The pictures already have the exact size of the paper you chose, at 600 dpi: they print sharp even on big sheets.

- Print on **the paper size you chose**, with the sheet the same way round as the picture (portrait or landscape).
- In the print options choose **"Actual size"** or **"100%"**. Avoid "Fit to page", which shrinks the map.
- White on black uses a lot of ink: it's meant for screens (tablets, virtual tabletops) rather than paper.
- If your printer only goes up to A4, a print shop can do A3, A2 and A1: bring the PNG or PDF file as it is.

---

## 7. Changing the words of the dungeons

The program's logic is in `wyrmdelve.py`; the **words** it draws at random are in `wyrmdelve_tables.json`, **in the same folder as `wyrmdelve.py`**: a text file you can open and change with any text editor (Notepad, TextEdit…). It holds about 3,000 entries (rooms, builders, occupants, caves, events, places, entrances, name syllables), which combine into billions of different stories:

| Section | What it holds |
|---|---|
| `name_syllables` | the syllables names are made of (*Zordur*, *Ishem*…) |
| `dungeon_types` | the 11 types (stratum I): their names, how they stack, their floor plan, who built them, the map's name, their rooms and their entrances (see below) |
| `second_age` | who came next (stratum II) and their rooms |
| `present_day` | today's dwellers (stratum III) and their rooms |
| `natural_rooms` | the natural caves (stratum N) |
| `events` | what ended each age |
| `areas` | where the dungeon is: `surface` for buildings above ground, `underground` for the others |
| `surface_shaft` | the entrance used when no wall of the level can take one |
| `history` | the sentences of the story at the top of the key |

Each type in `dungeon_types` has:

| Field | What it means |
|---|---|
| `id`, `code` | its internal name and the letter used in the seed |
| `menu`, `name` | its name in the type question and its short name on the map |
| `surface` | `true` if it stands above ground (tower, castle…) |
| `below` | **the types that can lie directly below it**: this is what keeps the levels coherent |
| `eras` | how likely each stratum is in its rooms: natural caves, founders, second age, today |
| `pattern` | its floor plan (one of the 11 plans in the table at the top) |
| `loops`, `portal` | how many corridors close a loop, how likely a magic portal is |
| `builders`, `built`, `titles` | who built it, what they built, the map's name |
| `rooms` | its rooms |
| `special` | the names of its key rooms (the throne hall, the apse, the cloister…) |
| `entrances`, `side_entrances` | the main entrances, and the ones on the other levels |
| `shaft_entrance` | (optional) its own entrance for when no wall can take one |

Every text is written in both languages, like this:

```
{"it": "sala del trono", "en": "throne hall"},
```

You can change the words or add new lines by copying an existing one. Builders must be written in the plural (*the counts of {n}*, *Baron {n} and their vassals*), because the history says "{f} built…". `{n}` is where the program puts a random name; in `history`, `{f}`, `{built}`, `{area}`, `{e1}`, `{s}`, `{e2}` and `{p}` are the founders, what they built, the place, the first event, the second age, the second event and today's dwellers.

Make a **copy** of the file before you edit it. Keep the quotes `"`, the commas between lines and the brackets exactly as they are: if something is out of place, the program tells you which line to check (see chapter 9). Changing the file changes the dungeons: the same seed may then give a different story than before.

---

## 8. For people in a hurry: the options

Instead of answering the questions, you can type everything on one line. Whatever you leave out is chosen at random (or asked, for the paper format). Examples, with the virtual environment active (see chapter 3):

```
python wyrmdelve.py --language en --levels 3 --rooms 24 --entrances 2 --secrets 5
python wyrmdelve.py --language en --seed 3-24-2-5-CDK-K7Q2MB --format A3 --pdf
python wyrmdelve.py --language en --type 3,4,11 --rooms 24
python wyrmdelve.py --language en --per-level --pdf --title "The Ogre's Lair"
```

Without `--language en` the messages and the texts on the map are in Italian. Every option also has an Italian name (after the slash `/`), and you can mix them as you like.

| Option | What it does | Example |
|---|---|---|
| `--language` / `--lingua` | Language: `en` or `it` | `--language en` |
| `--levels` / `--livelli` | Number of levels, 1 to 10 | `--levels 3` |
| `--rooms` / `--stanze` | Number of rooms, 3 to 200 (at least 2 per level) | `--rooms 24` |
| `--entrances` / `--ingressi` | Entrances/exits to the area, 1 to 9 | `--entrances 2` |
| `--secrets` / `--segreti` | Secret doors and passages, 0 to 60 | `--secrets 5` |
| `--type` / `--tipo` | Dungeon type, 1 to 11 as in the table at the top: one number for every level, or one per level from the top, separated by commas (the levels must stack coherently) | `--type 4` or `--type 3,4,11` |
| `--seed` / `--seme` | Rebuilds the dungeon of that seed | `--seed 3-24-2-5-CDK-K7Q2MB` |
| `--colors` / `--colori` | 1 black on white, 2 white on light blue, 3 white on black | `--colors 2` |
| `--format` / `--formato` | Paper: `A4`, `A3`, `A2` or `A1`; without it, the program asks | `--format A2` |
| `--per-level` / `--per-livello` | One level per sheet | `--per-level` |
| `--one-sheet` / `--un-foglio` | All levels on one sheet | `--one-sheet` |
| `--pdf` / `--png` | Save as PDF or as PNG | `--pdf` |
| `--title` / `--titolo` | Name on the map (default: a random one) | `--title "The Ogre's Lair"` |
| `--no-title` / `--senza-titolo` | Map without a name | `--no-title` |
| `--ascii-only` / `--solo-ascii` | Only plain keyboard characters (`# ~ = o`) | `--ascii-only` |
| `--font` | A font file of your choice (all its letters must be the same width) | `--font consola.ttf` |
| `--output` / `--uscita` | Folder to save in instead of `dungeons_generated` | `--output my_maps` |

To see the full list, type `python wyrmdelve.py --language en --help`.

### Limits

Levels 1–10, rooms 3–200 (at least 2 per level), entrances 1–9, secrets 0–60. If you ask for more secrets than there are corridors and connections, the program says so and places what it can. Some Jaquays techniques need room: one level has no level connections, sub-levels appear from 8 rooms up, divided levels need levels with 6+ rooms.

---

## 9. Common problems

**"py" / "python3" is not recognized as a command.**
Python isn't installed, or on Windows it wasn't added to the PATH. Reinstall it with "Add python.exe to PATH" ticked, then close and reopen the terminal.

**"Pillow is missing".**
The virtual environment isn't active: the line where you type doesn't start with `(.venv)`. Activate it (step 4 of the installation) and start the program again. If it still happens, the libraries aren't installed yet: do step 5.

**"No such file or directory" / "can't open file 'wyrmdelve.py'".**
The terminal isn't open in the folder with the files. Close it and open it again as in step 2.

**Windows: activating gives an error saying that "running scripts is disabled on this system".**
Windows' PowerShell terminal blocks scripts until you allow them. Type the line below, answer `Y`, then activate again. You only need to do this once.

```
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

**macOS: `python wyrmdelve.py` says "command not found: python".**
The virtual environment isn't active. On macOS the `python` command only exists inside the virtual environment (outside it there's only `python3`). Activate it (step 4) and try again.

**macOS and Linux: `source .venv/bin/activate` gives an error, or the line doesn't start with `(.venv)`.**
Your terminal may use a less common shell, which needs its own activation command. With **fish** type `source .venv/bin/activate.fish`; with **csh** or **tcsh** type `source .venv/bin/activate.csh`. The usual terminals of macOS (zsh) and Linux (bash) use `source .venv/bin/activate`, as in step 4.

**Linux: `python3 -m venv .venv` gives an error that mentions `ensurepip` or `venv`.**
A piece of Python is missing. On Ubuntu and Debian install it with the line below, then repeat step 3.

```
sudo apt install python3-venv
```

**Something got messed up during the installation.**
Delete the `.venv` folder (it's hidden: on Windows enable "Hidden items" in the View menu, on macOS press Cmd+Shift+. in Finder) and start again from step 3. Your dungeons in `dungeons_generated` are not touched.

**"wyrmdelve_tables.json is missing".**
The file with the words of the dungeons isn't in the folder. Put it next to `wyrmdelve.py`.

**"There is a mistake in wyrmdelve_tables.json".**
After you edited the file, something is out of place: the message says at which line and column (`line 12 column 5`). Usually it's a missing comma between two lines, an extra comma after the last line in a list, or a missing quote `"`. Fix it, or put back the copy you made before editing.

**"This seed is not valid".**
One of the characters of the seed is wrong or missing. Compare it with the name of the dungeon's folder or with the line under the map's title. It must have six parts separated by dashes, like `3-24-2-5-CDK-K7Q2MB` (five for seeds from older versions).

**"Level 1 (Castle) can't stand above level 2 (Tower)".**
The types you chose with `--type` don't stack coherently. Change their order or choose other types: the higher ones go first (a tower above a castle, a castle above a crypt, the Underdark last).

**The program says "Very small letters".**
The dungeon is too big for the format you chose: the map will print, but it'll be hard to read. Choose a bigger format (the suggested one), or put one level per sheet.

**Some symbols turned into plain letters.**
The font installed on your computer doesn't have those symbols. The program swaps them by itself and tells you. You can pick another font with `--font`, for example `--font DejaVuSansMono.ttf`, if it's installed.

**"No monospaced font found".**
The program looks for a font whose letters are all the same width (Consolas on Windows, Menlo on macOS, DejaVu Sans Mono on Linux). If none is there, install DejaVu Sans Mono (free) and give it with `--font DejaVuSansMono.ttf`.

**The printed map is smaller than the sheet, or off-center.**
In the print options choose "Actual size" or "100%", not "Fit to page".

**The ogre picture looks cut off on the right.**
The terminal window is too narrow. Make it wider and start the program again.

**I want to stop the program halfway.**
Press **Ctrl+C**. Nothing breaks: just start it again.

---

## Sources

- Justin Alexander, [Xandering the Dungeon](https://thealexandrian.net/wordpress/13085/roleplaying-games/xandering-the-dungeon) (parts 1–5) and [Xandering on the Small Scale](https://thealexandrian.net/wordpress/34950/roleplaying-games/thought-of-the-day-xandering-on-the-small-scale)
