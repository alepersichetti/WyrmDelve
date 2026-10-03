# How to add monsters to the bestiary

*[Versione italiana](add_monsters_to_bestiary.md)*

This guide explains, step by step, how to add your own monsters to WyrmDelve. No programming is needed: just a text editor and a little care with quotes.

> How the program uses the monsters (wandering monster tables, rooms, clues, out-of-place monsters) is explained in [monsters.en.md](monsters.en.md). This guide only explains how to write them.

## Contents

1. [Where the monsters are](#1-where-the-monsters-are)
2. [What a monster looks like](#2-what-a-monster-looks-like)
3. [The fields one by one](#3-the-fields-one-by-one)
4. [Adding a monster, step by step](#4-adding-a-monster-step-by-step)
5. [Ready-to-copy examples](#5-ready-to-copy-examples)
6. [Adding clues](#6-adding-clues)
7. [Adding reasons for out-of-place monsters](#7-adding-reasons-for-out-of-place-monsters)
8. [Trying the result](#8-trying-the-result)
9. [Common mistakes](#9-common-mistakes)
10. [Licenses: what you may copy](#10-licenses-what-you-may-copy)

---

## 1. Where the monsters are

All the monsters are in the file **`wyrmdelve_tables.json`**, in the same folder as `wyrmdelve.py`, under `"monsters"`. Each monster is **one line**.

Before you start:

1. **Make a copy** of the file (for example `wyrmdelve_tables_copy.json`): if something goes wrong, you put it back.
2. Open the file with a plain text editor: Notepad on Windows, TextEdit on a Mac (in "plain text" mode), or an editor like Visual Studio Code, which colours the text and points out mistakes.
3. Search for `"monsters"` (Ctrl+F on Windows, Cmd+F on a Mac).

---

## 2. What a monster looks like

Here is a real monster, taken from the file:

```json
{"name": {"it": "ghoul", "en": "ghouls"}, "text": {"it": "morti affamati di carne; i loro artigli paralizzano", "en": "dead hungry for flesh; their claws paralyse"}, "where": ["tomb", "temple", "prison"], "danger": 1, "kind": "undead", "number": "2d6"},
```

In plain English: *ghouls are dead hungry for flesh, they are found in tombs, temples and prisons, they are not very dangerous (1), they are undead, and you meet 2d6 of them.*

In the dungeon key it becomes:

```
  Wandering monsters (d6)
    3. Ghouls: dead hungry for flesh; their claws paralyse.

  1-04 Monsters: Ghouls (2d6).
  1-05 Empty. Clue: bones gnawed by human teeth (from 1-04).
```

---

## 3. The fields one by one

| Field | What it holds | Required | Example |
|---|---|---|---|
| `name` | the name, in Italian (`it`) and in English (`en`) | yes | `{"it": "ghoul", "en": "ghouls"}` |
| `text` | a one-line description, in both languages | yes | `{"it": "morti affamati di carne…", "en": "dead hungry for flesh…"}` |
| `where` | which **dungeon types** it can appear in | no (without it: everywhere) | `["tomb", "temple"]` or `["*"]` |
| `danger` | how **dangerous** it is, 1 to 4 | no (without it: 2) | `1` |
| `kind` | what **creature** it is: it decides the clues and the reasons for being out of place | no (without it: no clue) | `"undead"` |
| `number` | **how many** you meet | no (without it: no number) | `"2d6"` |

### `where`: dungeon types

Write one or more of these names, in quotes and separated by commas:

| Name | Type | Name | Type |
|---|---|---|---|
| `palace` | Palace | `wizard` | Arcane laboratory |
| `prison` | Prison | `academy` | Academy |
| `tower` | Tower | `fortress` | Border fortress |
| `castle` | Castle | `tomb` | Tomb |
| `temple` | Temple | `underdark` | Underdark |
| `city` | City | `*` | **everywhere** |

A monster appears in a level's tables only if that level is of a listed type. The more types you list, the more often it comes up.

### `danger`: the danger

| Value | Danger | Usually appears on | Examples |
|---|---|---|---|
| `1` | low | the first level | giant rats, goblins, skeletons |
| `2` | medium | the second level | ghast, ogre, gelatinous cube |
| `3` | high | the third level | troll, mummy, basilisk |
| `4` | deadly | the deepest levels | dragons, lich, iron golem |

How the monsters' danger is matched to the depth of the levels is explained in chapter 2 of [monsters.en.md](monsters.en.md#2-danger-grows-with-depth).

### `kind`: what creature it is

| `kind` | Creatures | Typical clue |
|---|---|---|
| `vermin` | insects, spiders, rats, bats | empty husks, webs |
| `beast` | animals, reptiles | tufts of fur, claw marks |
| `aquatic` | water creatures | puddles and slimy trails |
| `ooze` | oozes and jellies | walls strangely clean |
| `fungus` | fungi, moulds, plants | glowing spores |
| `magical` | magical beasts (basilisk, mimic…) | statues with a look of terror |
| `dragon` | dragons | scales the size of shields |
| `giant` | giants, ogres, trolls | huge footprints |
| `humanoid` | people and humanoids | the remains of a fire |
| `undead` | undead with a body | dirty bandages, a smell of the grave |
| `spirit` | spirits and ghosts | candles that go out by themselves |
| `construct` | golems, statues, automatons | an empty pedestal |
| `elemental` | elementals and genies | a broken summoning circle |
| `demon` | demons and devils | burned symbols, sulphur |

You can invent a new `kind`: in that case add its clues too (chapter 6), otherwise the monster leaves no clues.

### `number`: how many

A dice expression such as `"1"`, `"1d3"`, `"1d6"`, `"2d6"`, `"3d6"`. Leave `""` for swarms and things that can't be counted (a cloud of bats, an insect swarm). The program writes it next to the name: `Ghouls (2d6)`.

A simple rule: danger 1 → `"2d6"`, danger 2 → `"1d6"`, danger 3 → `"1d3"`, danger 4 → `"1"`.

---

## 4. Adding a monster, step by step

Let's add the **crypt leech**, an invented monster.

**1. Find the last monster of the list.** It's the line just before `  ],` and `"clues"`:

```json
    {"name": {"it": "megera marina", "en": "sea hag"}, …, "number": "1d6"}
  ],
  "clues": {
```

**2. Add a comma at the end of the last line**, because another one follows:

```json
    {"name": {"it": "megera marina", "en": "sea hag"}, …, "number": "1d6"},
```

**3. Write your monster below**, with no comma at the end (now it's the last one):

```json
    {"name": {"it": "sanguisuga delle cripte", "en": "crypt leech"}, "text": {"it": "si nasconde nei sarcofagi e succhia il calore dei vivi", "en": "hides in sarcophagi and drains the warmth of the living"}, "where": ["tomb"], "danger": 2, "kind": "undead", "number": "1d6"}
  ],
  "clues": {
```

**4. Save the file** and try the program (chapter 8).

You can also put the monster **in the middle** of the list: then your line must end with a comma, like all the others.

---

## 5. Ready-to-copy examples

One monster for each typical situation. Copy the line, change the words, save.

**A swarm found everywhere** (no number):

```json
{"name": {"it": "sciame di falene", "en": "moth swarm"}, "text": {"it": "falene grigie che spengono le torce e lasciano polvere negli occhi", "en": "grey moths that put out torches and leave dust in the eyes"}, "where": ["*"], "danger": 1, "kind": "vermin", "number": ""},
```

**A group of people in the city**:

```json
{"name": {"it": "contrabbandieri", "en": "smugglers"}, "text": {"it": "spostano merci proibite attraverso le fogne", "en": "move forbidden goods through the sewers"}, "where": ["city", "prison"], "danger": 1, "kind": "humanoid", "number": "2d6"},
```

**A water creature** (it can also appear "out of place", come up from the flooded caves):

```json
{"name": {"it": "anguilla delle cisterne", "en": "cistern eel"}, "text": {"it": "un'anguilla pallida e cieca che morde le caviglie", "en": "a pale, blind eel that bites at ankles"}, "where": ["underdark", "city"], "danger": 1, "kind": "aquatic", "number": "1d6"},
```

**A guardian built by the founders** (it can appear "out of place" in the founders' halls):

```json
{"name": {"it": "cavaliere di bronzo", "en": "bronze knight"}, "text": {"it": "una statua equestre che carica chi non conosce la parola d'ordine", "en": "an equestrian statue that charges anyone without the password"}, "where": ["castle", "palace", "fortress"], "danger": 3, "kind": "construct", "number": "1"},
```

**A unique, deadly monster of the deep**:

```json
{"name": {"it": "verme della memoria", "en": "memory worm"}, "text": {"it": "un verme lungo un corridoio che divora i ricordi di chi tocca", "en": "a worm as long as a corridor that devours the memories of whoever it touches"}, "where": ["underdark"], "danger": 4, "kind": "magical", "number": "1"},
```

---

## 6. Adding clues

Clues are under `"clues"`, grouped by `kind`. Every time a monster lives in a room, the program picks a clue of its `kind` and puts it in a nearby empty room.

```json
  "clues": {
    "undead": [
      {"it": "un freddo innaturale e impronte di piedi scalzi nella polvere", "en": "an unnatural cold and bare footprints in the dust"},
      {"it": "bende sporche e un odore di tomba", "en": "dirty bandages and a smell of the grave"},
      {"it": "ossa rosicchiate da denti umani", "en": "bones gnawed by human teeth"}
    ],
```

To add a clue, add a line to the right list (with a comma between one line and the next). Write something you can **see, hear or smell**, without naming the monster: it should raise a suspicion, not give everything away. In the key it becomes:

```
  1-05 Empty. Clue: bones gnawed by human teeth (from 1-04).
```

For a new `kind`, add a new list:

```json
    "insect_queen": [
      {"it": "celle di cera vuote e un ronzio profondo", "en": "empty wax cells and a deep humming"}
    ],
```

---

## 7. Adding reasons for out-of-place monsters

When and how out-of-place monsters appear is explained in chapter 5 of [monsters.en.md](monsters.en.md#5-out-of-place-monsters). The reasons are under `"quirks"`:

```json
{"when": "water", "kinds": ["aquatic"], "text": {"it": "le grotte allagate{from} arrivano fin sotto questa stanza, attraverso una vasca", "en": "the flooded caves{from} reach up under this room, through a pool"}},
```

| Field | What it holds |
|---|---|
| `when` | **when** the reason is possible: `water`, `portal`, `below`, `founders` or `any` (the conditions are in the table of chapter 5 of [monsters.en.md](monsters.en.md#5-out-of-place-monsters)) |
| `kinds` | which monster `kind`s it can apply to (`[]` = all) |
| `text` | the reason, in both languages |

The placeholders you can use in the text depend on `when`:

| `when` | Placeholder |
|---|---|
| `water` | `{from}` = " of level 3" (with the space in front) |
| `portal` | `{room}` = the portal's room, for example `1-04` |
| `below` | `{level}` = the number of the level below, for example `3` |
| `founders`, `any` | none |

In the key:

```
  2-03 Monsters: Aboleth (1). Out of place: the flooded caves of level 3 reach up under this room, through a pool.
```

**One important rule:** write the reason about the **place**, not the monster. The monster may be a single one or a group (*an aboleth*, *wolves*): a sentence like "it came through the portal" wouldn't work with *wolves*. Write instead "the portal in {room} now and then lets something through". In Italian this matters even more, because verbs and adjectives change with gender and number.

---

## 8. Trying the result

After saving, make a dungeon of the right type with monsters. Example for a 3-level tomb:

```
python wyrmdelve.py --type 10 --levels 3 --content monsters
```

(`--type 10` is the tomb: the number is its place in the type menu, 1 to 11.)

Then open the `_key.txt` file in the dungeon's folder and look for your monster. If it isn't there, make a few more dungeons without `--seed`: monsters are drawn at random among those that fit, and with 245 monsters not all of them come up every time.

---

## 9. Common mistakes

If the JSON file has a mistake, the program stops at once and says which line to look at:

```
C'è un errore nel file wyrmdelve_tables.json / There is a mistake in wyrmdelve_tables.json:
  Expecting ',' delimiter: line 3912 column 5
```

| Error | Usual cause | How to fix it |
|---|---|---|
| `Expecting ',' delimiter` | the comma at the end of the line **before** is missing | add the comma |
| `Expecting property name` | there's one comma too many after the **last** line of a list | remove the comma before `]` |
| `Expecting value` | missing quotes, or `'` instead of `"` | always use double quotes `"` |
| `Invalid control character` | a line break inside a text | write the text on a single line |
| the monster never comes up | wrong `where` (for example `"tombs"` instead of `"tomb"`) | check the table in chapter 3 |
| no clue near the monster | its `kind` has no clues | add them under `clues` |

Inside a text you can use the apostrophe (`today's`) with no problem. If you need a double quote, write it like this: `\"`.

---

## 10. Licenses: what you may copy

WyrmDelve is released under the GPL 3.0, and anyone can copy it. That's why, in the JSON file:

- **you may** write your own monsters, in your own words;
- **you may** use material under a **Creative Commons BY** license (for example the SRD 5.1 or Ironsworn), remembering to **credit the source** in the JSON file's `credits` and in the README's Sources section;
- **don't copy** descriptions from books or PDFs without an open license: you can take the **idea** of a monster and its name, if it is generic (a ghoul, a giant spider), and describe it in your own words. That's what was done with the two bestiaries credited in the README;
- **avoid** names registered by others: for example *beholder*, *mind flayer*, *displacer beast*, *umber hulk*, *carrion crawler*, *githyanki*, *yuan-ti*.
