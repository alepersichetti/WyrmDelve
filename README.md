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
| `═║╔╗` | **I** — the founders (dwarves, priests, a wizard, a legion, an imperial tomb) |
| `─│┌┐` | **II** — those who came next (cultists, smugglers, a necromancer, goblins, monks) |
| `#` (rough-hewn rooms) | **III** — today's dwellers (an ogre, orcs, the undead, spiders, troglodytes) |

Rooms are numbered **level-room**: `1-01`, `2-07`, and `1a-01` on a sub-level. The dungeon key tells what each room was for in each age (e.g. *Throne hall; II: gambling den; III: ogre's lair*).

The layout **always** follows Jennell Jaquays' principles as Justin Alexander describes them in *Xandering the Dungeon*: multiple entrances, loops, multiple and discontinuous level connections, secret and unusual paths (secret doors and passages, hidden stairs, flooded passages, cave-ins, portals), sub-levels, divided levels, minor elevation shifts, midpoint entries, nested dungeons. When it's done, the program checks that every room can be reached and prints which principles it applied.

---

## 1. What you need

Put in the **same folder**:

- `wyrmdelve.py` (the program)
- `requirements.txt`
- `README.md` and `README.it.md`

The `dungeons_generated` folder is created by the program.

You need Python 3.8 or later and the Pillow library:

```
pip install -r requirements.txt
```

## 2. How to use it

```
python wyrmdelve.py
```

1. Choose the language (Italian or English).
2. The ogre shows up in his dungeon. Press **ENTER** for a fully random dungeon, type **P** to choose the parameters yourself, or **R** to rebuild a dungeon from its seed.
3. With **P** you choose: number of levels, number of rooms (at least 2 per level), number of entrances/exits to the area, number of secret doors and passages.
4. Either way you choose the colours:
   1. black symbols on white (default)
   2. white symbols on light blue
   3. white symbols on black
5. The program builds the dungeon and shows a table with **A4, A3, A2 and A1**: for each, the letter size and whether it's readable. It suggests the smallest sheet where the map reads well; press Enter to accept it or type another format. The picture is always **600 dpi** and the sheet turns portrait or landscape by itself.

## 3. What you get

In `dungeons_generated/<seed>/`:

| File | Content |
|---|---|
| `<seed>_gm.png` / `.txt` | game master map: room numbers, secret doors `S` and passages `░` |
| `<seed>_players.png` / `.txt` | same map without numbers and secrets |
| `<seed>_key.txt` | history, strata, entrances, level connections, room-by-room key, Jaquays check |

The **seed** (e.g. `3-24-2-5-K7Q2MB` = levels-rooms-entrances-secrets-code) holds the whole dungeon: the same seed always gives the same dungeon.

## 4. Symbols

| Symbol | Meaning | Symbol | Meaning |
|---|---|---|---|
| `.` | floor | `+` | door |
| `S` | secret door (GM only) | `░` | secret passage (GM only) |
| `<` `>` | stairs up / down | `≡` | steps, same level |
| `○` | shaft or chimney between levels (may skip some) | `Ω` | magic portal |
| `≈` | water | `∴` | cave-in |
| `■` | pillar | `[A]` | entrance (solid box on the map) |

## 5. Command line options

Every option has an Italian and an English name. Whatever you leave out is chosen at random.

```
python wyrmdelve.py --levels 3 --rooms 24 --entrances 2 --secrets 5
python wyrmdelve.py --colors 2                   (1 black/white, 2 white/light blue, 3 white/black)
python wyrmdelve.py --seed 3-24-2-5-K7Q2MB       rebuild a dungeon
python wyrmdelve.py --format A2                  skip the paper question
python wyrmdelve.py --title "The Ogre's Lair"
python wyrmdelve.py --ascii-only                 keyboard characters only (# ~ = o)
python wyrmdelve.py --font MyFont.ttf
python wyrmdelve.py --language en
python wyrmdelve.py --help
```

## 6. Limits

Levels 1–10, rooms 3–200 (at least 2 per level), entrances 1–9, secrets 0–60. If you ask for more secrets than there are corridors and connections, the program says so and places what it can. Some Jaquays techniques need room: one level has no level connections, sub-levels appear from 8 rooms up, divided levels need levels with 6+ rooms.

## Sources

- Justin Alexander, [Xandering the Dungeon](https://thealexandrian.net/wordpress/13085/roleplaying-games/xandering-the-dungeon) (parts 1–5) and [Xandering on the Small Scale](https://thealexandrian.net/wordpress/34950/roleplaying-games/thought-of-the-day-xandering-on-the-small-scale)
