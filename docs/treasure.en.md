# How the treasure is made

*[Versione italiana](treasure.md)*

This document explains how WyrmDelve decides which rooms hold treasure, what it holds and where it is hidden, with real examples made by the program.

> Treasure appears only if at the start, at "What do you want to make?", you also tick the **treasure** (or `--content treasure`, also together with other things: `--content monsters,treasure`). How the monsters and traps that guard it are made is explained in [monsters.en.md](monsters.en.md) and [trap.en.md](trap.en.md).

## Contents

1. [The idea: the Old-School Essentials rules](#1-the-idea-the-old-school-essentials-rules)
2. [Which rooms hold treasure](#2-which-rooms-hold-treasure)
3. [Monster treasure: types A to V](#3-monster-treasure-types-a-to-v)
4. [Unguarded treasure: it depends on the level](#4-unguarded-treasure-it-depends-on-the-level)
5. [Coins, gems and jewellery](#5-coins-gems-and-jewellery)
6. [Magic items](#6-magic-items)
7. [Where it is hidden](#7-where-it-is-hidden)
8. [In the key](#8-in-the-key)
9. [A complete example](#9-a-complete-example)
10. [Changing the tables](#10-changing-the-tables)

---

## 1. The idea: the Old-School Essentials rules

WyrmDelve follows the dungeon room stocking rules of *Old-School Essentials* (the *Designing a Dungeon* and *Treasure* chapters of the System Reference Document). The tables are in `data/treasure.json`: they are **Open Game Content** under the OGL 1.0a (see `LICENSE-OGL.txt`), read from the Markdown edition [Old-School-Essentials-Markdown](https://github.com/Obsidian-TTRPG-Community/Old-School-Essentials-Markdown) and translated into Italian.

Treasure comes **last**, after monsters and traps, and uses dice of its own (made from the seed with the label `treasure`): the map, the story, the monsters and the traps of a seed don't change whether you choose treasure or not.

---

## 2. Which rooms hold treasure

In the rules, the referee rolls 1d6 to find out what is in a room, then another d6 to find out whether there is treasure:

| d6 | Contents | Treasure |
|---|---|---|
| 1–2 | empty | 1 in 6 |
| 3–4 | monsters | 3 in 6 |
| 5 | special | never |
| 6 | trap | 2 in 6 |

WyrmDelve doesn't roll the first die: what is in every room is already decided by the monsters ([monsters.en.md](monsters.en.md)) and the traps ([trap.en.md](trap.en.md)). For each room, in order:

1. if **monsters** live there, it is a room with monsters;
2. otherwise, if it has a **trap**, it is a room with a trap;
3. otherwise it is **empty** (even if it holds a clue).

Then it rolls the treasure d6 with the chance in the table. WyrmDelve has no "special" rooms, so they never take a treasure away.

If you didn't choose monsters or traps, those rooms don't exist: every room counts as empty (or with a trap), and treasure is rarer. A 24-room dungeon with everything else chosen usually has 3 to 9 treasures (5 halfway).

---

## 3. Monster treasure: types A to V

In a room with monsters, the treasure is their **treasure type**, a letter written in the `treasure` field of every monster in `data/monsters.json`:

- for monsters with the same name in *Old-School Essentials* (orcs, ghouls, dragons…), the letter is the one in its stats;
- for the others, a letter chosen by analogy with a similar monster;
- for creatures that keep nothing (animals, oozes, swarms), no letter: no treasure, even if the die says yes;
- **today's dwellers** (the lairs of stratum III) always have type `D`.

Each type is a list of lines, each with its own chance. For instance type **C** (average value 1,000 gp):

| Chance | What |
|---|---|
| 20% | 1d12 × 1,000 copper pieces |
| 30% | 1d4 × 1,000 silver pieces |
| 10% | 1d4 × 1,000 electrum pieces |
| 25% | 1d4 gems |
| 25% | 1d4 pieces of jewellery |
| 10% | 2 magic items of any kind |

| Types | What they are | Average value |
|---|---|---|
| A–O | **lair hoards**: the wealth of a large monster or of a community | from 25 gp (J) to 60,000 gp (H); N and O hold magic items only |
| P–T | **individual** treasure, for every creature | from 0.1 to 17 gp |
| U–V | **group** treasure, carried all together | 160 and 330 gp |

WyrmDelve rolls the type **once per room**, for the whole group, U and V included.

---

## 4. Unguarded treasure: it depends on the level

In empty rooms or rooms with a trap the treasure depends on the **dungeon level**: the deeper, the richer.

| Level | Silver | Gold | Gems | Jewellery | Magic items |
|---|---|---|---|---|---|
| 1 | 1d6 × 100 | 50%: 1d6 × 10 | 5%: 1d6 | 2%: 1d6 | 2%: 1 any |
| 2–3 | 1d12 × 100 | 50%: 1d6 × 100 | 10%: 1d6 | 5%: 1d6 | 8%: 1 any |
| 4–5 | 1d6 × 1,000 | 1d6 × 200 | 20%: 1d6 | 10%: 1d6 | 10%: 1 any |
| 6–7 | 1d6 × 2,000 | 1d6 × 500 | 30%: 1d6 | 15%: 1d6 | 15%: 1 any |
| 8 and beyond | 1d6 × 5,000 | 1d6 × 1,000 | 40%: 1d12 | 20%: 1d12 | 20%: 1 any |

A **sub-level** counts as the level below it: sub-level 1a uses the level 2 row.

---

## 5. Coins, gems and jewellery

**Coins.** Five metals, with their value in gold pieces:

| Coin | Short | Value |
|---|---|---|
| copper | cp | 1/100 gp |
| silver | sp | 1/10 gp |
| electrum | ep | 1/2 gp |
| gold | gp | 1 gp |
| platinum | pp | 5 gp |

**Gems.** Each gem is worth what a d20 says:

| d20 | Value |
|---|---|
| 1–4 | 10 gp |
| 5–9 | 50 gp |
| 10–15 | 100 gp |
| 16–19 | 500 gp |
| 20 | 1,000 gp |

**Jewellery.** Each piece is worth 3d6 × 100 gp.

In the key, gems and jewellery of the same value are grouped: `5 gems (2×50 gp, 3×100 gp)` are two gems worth 50 and three worth 100.

---

## 6. Magic items

First the **type** of item is rolled, then the item on that type's table. The rules have two columns: **B** (Basic) for characters of levels 1 to 3, **X** (Expert) from level 4 up. WyrmDelve uses the **dungeon level** instead of the characters' level: column B down to level 3, column X from level 4.

| B (d%) | X (d%) | Type |
|---|---|---|
| 01–10 | 01–10 | armour and shields |
| 11–15 | 11–15 | miscellaneous items (bags, boots, cloaks…) |
| 16–40 | 16–35 | potions |
| 41–45 | 36–40 | rings |
| 46–50 | 41–45 | rods, staves and wands |
| 51–70 | 46–75 | scrolls and treasure maps |
| 71–90 | 76–95 | swords |
| 91–100 | 96–100 | other weapons |

In column B each table is rolled with a small die (for instance 1d8 for potions) and holds only the simpler items; in column X d% is rolled on the whole table. Magic armour also has a kind, with 1d8: 1–2 leather, 3–6 chainmail, 7–8 plate mail (*Chainmail armour +1*).

Some treasure types ask for particular items:

| Request | How it is chosen |
|---|---|
| any | the types table |
| potion, scroll | that table directly |
| weapon or armour (type B) | the types table, rerolling until armour, a sword or a weapon comes up |
| not a weapon (type F) | the types table, rerolling swords and weapons |

Magic items have no set price: they are not counted in the treasure's value.

---

## 7. Where it is hidden

Every treasure has a hiding place, written for WyrmDelve:

- in **monster lairs**: "heaped up in the lair", "hidden under the bedding", "in a stolen chest", "scattered among the refuse and the bones", "kept by the strongest of the group", "buried under the floor of the lair";
- in **other rooms**: twelve hiding places, such as "under a floor slab that lifts", "inside a hollow statue", "in the false bottom of an old trunk", "at the bottom of a pool of murky water".

If the room has a **working trap**, the key adds "The room's trap guards it": it's the rules' *treasure trap*, which goes off when someone tampers with the treasure. A broken trap (the lesson, see [trap.en.md](trap.en.md)) guards nothing.

---

## 8. In the key

The treasure is the last line of the room, after the monsters and the trap:

```
  1a-02 Empty. Clue: deep furrows in the floor and the smell of an unknown beast (from 1a-01).
         Trap (^): Burst of burning oil (counterweighted floor). …
         Treasure (110 gp): 1,100 sp, Dagger +1; behind a loose brick. The room's trap guards it.
```

- in brackets, the **value** in gold pieces of the coins, gems and jewellery (without the magic items); if it is less than 1 gp, it isn't shown;
- then the **coins**, from the least to the most valuable, the **gems**, the **jewellery** and the **magic items**;
- after the semicolon, the **hiding place**.

While generating, the program says how many treasures it placed: `Treasure hoards: 5, worth 9,300 gp in coins, gems and jewellery; magic items: 1`.

Treasure doesn't show on the maps: it is only in the key.

---

## 9. A complete example

Seed `2-14-2-1-C-02SFP3`: a two-level castle with sub-level 1a, with monsters, traps and treasure. The treasures:

| Room | Contents | Chance | Table | Treasure |
|---|---|---|---|---|
| 1-02 | empty | 1 in 6 | level 1 | 600 sp (60 gp), inside a hollow statue |
| 1-03 | today's dwellers, in their lair | 3 in 6 | type D | 5,000 cp, 6,000 gp, 5 gems (6,450 gp), under the bedding |
| 1a-01 | an out-of-place couatl | 3 in 6 | type B | 6,000 cp, 1,000 ep, 2,000 gp (2,560 gp), among the refuse and the bones |
| 1a-02 | working trap (and a clue) | 2 in 6 | level 2 (the sub-level counts as the level below) | 1,100 sp and a Dagger +1 (110 gp), behind a loose brick; the trap guards it |
| 2-03 | empty, with a clue | 1 in 6 | level 2 | 1,200 sp (120 gp), in a box hanging inside a crack in the ceiling |

You can see that:

- the lairs have the richest treasure: that's where monsters hoard;
- the empty rooms have a few silver pieces, as the table of the first levels says;
- room 1-03 has a trap, but it is the lesson (broken): the treasure is there because of the monsters, and the trap doesn't guard it;
- the only magic item is a simple weapon from column B, because the dungeon is shallow.

---

## 10. Changing the tables

Everything is in `data/treasure.json`. Make a copy of the file before you edit it.

| Entry | What it holds |
|---|---|
| `room_chance` | the chances in 6 for an `empty`, `monster`, `special` or `trap` room |
| `dwellers_type` | today's dwellers' treasure type (`"D"`) |
| `unguarded` | the unguarded treasure: for every group of levels (`levels`: first and last) its lines |
| `types` | types A to V: for each, its average value (`average`) and its lines |
| `coins`, `coin_value` | the coins' short names in both languages and their value in gold |
| `gems`, `jewellery` | the value of gems (d20) and of jewellery (dice × multiplier) |
| `magic_types`, `magic` | the types table (columns `b` and `x`) and the item tables, with the column B die (`basic_die`) |
| `armour_kinds` | the kind of magic armour (d8) |
| `hiding` | the hiding places: `lair` in lairs, `loose` in other rooms |

A line of a treasure type looks like this:

```json
{"chance": 25, "dice": "1d6", "times": 1000, "what": "cp"}
```

that is: a 25% chance of 1d6 × 1,000 copper pieces. `what` can be a coin (`cp`, `sp`, `ep`, `gp`, `pp`), `gems`, `jewellery` or `magic`, which has a list of items:

```json
{"chance": 15, "what": "magic", "items": [{"count": 2, "kind": "any"}, {"count": 1, "kind": "potion"}]}
```

`kind` can be `any`, `potion`, `scroll`, `weapon_armour` or `not_weapon`; instead of `count` you can write `dice` (for instance `"2d4"`).

To change a monster's treasure, change the letter in its `treasure` field in `data/monsters.json` (see [add_monsters_to_bestiary.en.md](add_monsters_to_bestiary.en.md)).

If `data/treasure.json` is missing or has a mistake, the program says so and makes the dungeon without treasure.
