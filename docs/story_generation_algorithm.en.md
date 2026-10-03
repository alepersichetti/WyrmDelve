# How the dungeon story is made

*[Versione italiana](story_generation_algorithm.md)*

This document explains, in plain words and with real examples, how WyrmDelve invents the story of a dungeon: who built it, who came after, who lives there today, what is told about it and what is in each room.

Every text in this document was written by the program, not by hand. You can make them again with the seeds given.

> How the map is made (rooms, corridors, stairs, secrets) is explained in a separate document: [dungeon_map_generation.en.md](dungeon_map_generation.en.md).

## Contents

1. [The idea: a layered story](#1-the-idea-a-layered-story)
2. [Where the words come from](#2-where-the-words-come-from)
3. [The story's dice](#3-the-storys-dice)
4. [The ingredients](#4-the-ingredients)
5. [Invented names](#5-invented-names)
6. [The history: parts and shape](#6-the-history-parts-and-shape)
7. [A history taken apart piece by piece](#7-a-history-taken-apart-piece-by-piece)
8. [Three more histories, three different shapes](#8-three-more-histories-three-different-shapes)
9. [How many different stories?](#9-how-many-different-stories)
10. [The strata](#10-the-strata)
11. [Room descriptions](#11-room-descriptions)
12. [Entrances, exits and connections](#12-entrances-exits-and-connections)
13. [Where the story ends up: the key and the PDF](#13-where-the-story-ends-up-the-key-and-the-pdf)
14. [Writing new sentences without mistakes](#14-writing-new-sentences-without-mistakes)

---

## 1. The idea: a layered story

An interesting dungeon isn't made all at once. Someone builds it, then leaves; others arrive, refit it, open new passages; then a catastrophe, a collapse, and today someone else lives among the ruins.

WyrmDelve tells every dungeon this way, in **four ages**:

| Age | Tag | Who |
|---|---|---|
| Natural | **N** | the caves that were already there, before anyone |
| First age | **I** | the **founders**, who built the dungeon |
| Second age | **II** | those who arrived after the first catastrophe |
| Third age | **III** | those who live there **today**, after the second catastrophe |

The ages aren't just words: they show on the map (double walls for the founders, single walls for the second age, `#` for caves and the third age) and every room says which age it belongs to and how it changed over time.

---

## 2. Where the words come from

All the words are in the file **`wyrmdelve_tables.json`**, next to the program. Every text is written in Italian and in English:

```json
{"it": "la caduta di un meteorite", "en": "the fall of a meteorite"}
```

The file can be edited (see chapter 7 of the README and [chapter 14](#14-writing-new-sentences-without-mistakes) of this document). Here is what it holds, in numbers:

| Table | What it holds | How many |
|---|---|---|
| `dungeon_types` | the 11 types, each with its founders, what they built, titles, rooms, special rooms, entrances | 12 founders, 6 buildings, 12–13 titles, about 90–107 rooms per type |
| `second_age` | the second-age groups, each with its rooms | 35 groups |
| `present_day` | today's dwellers, each with their rooms | 45 groups |
| `natural_rooms` | the natural caves | 144 |
| `events` | the catastrophes that end an age | 147 |
| `areas` | where the dungeon lies | 66 above ground, 58 underground |
| `history` | the sentences of the history and the lists they draw from | 97 sentences; 30 goals, 30 relics, 25 visitors |
| `name_syllables` | syllables and endings for names | 238 syllables, 9 families of endings |

---

## 3. The story's dice

With the same seed (for example `3-21-2-4-CDK-000F62`) you always get the same story. The story uses two of the separate "bags of dice" the program makes from the seed (explained in chapter 2 of [dungeon_map_generation.en.md](dungeon_map_generation.en.md#separate-dice)):

- one for the story's **ingredients** and the room names;
- one for the **shape and the sentences of the history**.

So the sentences of the history don't change the room names, and vice versa; and neither of them changes the map.

---

## 4. The ingredients

Before writing a single line, the program picks the **ingredients**. Here are those of seed `3-21-2-4-CDK-000F62` (tower, castle, Underdark):

| Ingredient | Placeholder | How it is chosen | Example |
|---|---|---|---|
| the **founders** | `{f}` | one of the 12 builders of the **ground level**'s type (here the castle), with an invented name | *the counts of Norin* |
| what they **built** | `{built}` | one building for each different type in the dungeon, joined with commas and "and" | *a tower, a castle and an outpost among the caves* |
| **where** | `{area}` | a place above ground if at least one level is above ground, otherwise an underground place | *in the firefly marshes* |
| the **first catastrophe** | `{e1}` | one of the 147 events | *the death of a lesser god* |
| the **second age** | `{s}` | one of the 35 groups, with an invented name | *the refugees of Eskrin* |
| the **second catastrophe** | `{e2}` | another event, never the same as the first | *a flood* |
| **today's dwellers** | `{p}` | one of the 45 groups, with an invented name | *the bugbears of Inchalville* |
| the **title** | | one of the titles of the ground level's type, with an invented name | *The Citadel of Sullenis* |

The founders come from the type of the **ground level**, the one with the main entrance (explained in chapter 3 of [dungeon_map_generation.en.md](dungeon_map_generation.en.md#the-ground-level)): in this example the tower stands on top of the castle, but the founders are those of a castle.

The history also needs four **extra ingredients**, picked with the history's dice:

| Ingredient | Placeholder | From | Example |
|---|---|---|---|
| a **goal** | `{goal}` | 30 goals | *bury a king with all his treasures* |
| a **relic** | `{relic}` | 30 relics | *a lamp that never goes out* |
| some **visitors** | `{visitors}` | 25 passing groups | *treasure hunters* |
| a **lost adventurer** | `{hero}` | an invented name | *Naljormont* |

---

## 5. Invented names

Every `{n}` in the tables (for example *the counts of {n}*) becomes an invented name. The program builds it from the syllables in the JSON file:

- 6 times out of 10: one or two syllables plus an **ending** from a family of languages (Arabic, Danish, Old French, Persian, Greek, Latin, German, Russian, or Tolkien-style names);
- the other times: two or three syllables.

The name must be 3 to 12 letters long, and it never repeats within the same dungeon.

Some names made by the program:

> Vensilen · Meheqar · Zalbryn · Ulnzor · Varirniya · Cistan · Kethov · Borhard · Sabalo · Halburg · Bareul · Eirbert · Quenev

The endings come from statistics on names in those languages and in the game Angband (its code was not copied).

---

## 6. The history: parts and shape

The history is a paragraph made of **parts**. Each part has several possible sentences, and the program picks one. The parts always come in this order:

| # | Part | Name in the JSON | When it's there | Sentences |
|---|---|---|---|---|
| 1 | **opening** | `opening`, `opening_legend` or `opening_place` | sometimes (see below) | 4 + 4 + 4 |
| 2 | the founding | `founded` | always | 7 |
| 3 | the founders' goal | `purpose` | sometimes | 5 |
| 4 | the caves | `caves` | only if the dungeon has natural caves | 4 |
| 5 | the golden age | `golden` | sometimes | 6 |
| 6 | ill omens | `omen` | sometimes | 4 |
| 7 | the second age | `second` | always | 6 |
| 8 | what the newcomers did | `second_detail` | sometimes | 5 |
| 9 | the end of the second age | `fall` | always | 5 |
| 10 | the abandonment | `aftermath` | sometimes | 4 |
| 11 | the founders' fate | `fate` | sometimes | 4 |
| 12 | who passed through | `interlude` | sometimes | 4 |
| 13 | today's dwellers | `present` | always, unless the opening already speaks of them | 4 |
| 14 | a detail about the present | `present_detail` | sometimes | 4 |
| 15 | the newer tunnels | `crude` | only if the dungeon has third-age rooms | 3 |
| 16 | **closing** | `legend`, `warning` or `hook` | sometimes (see below) | 8 + 4 + 5 |

### The opening

The program rolls a five-sided die:

- 2 faces: **no opening**, the history starts with the founding;
- **today's dwellers** (`opening`): *"Those who enter today find the ratfolk swarm of Chalcahun, but to understand these halls one must go back centuries."* In this case part 13 is skipped, because it has already been said;
- **a rumour** (`opening_legend`): *"The last expedition to go down there, led by one Eskmorrup, never came back; but to understand why one must start from the beginning."*;
- **the place** (`opening_place`): *"Few know where it lies, and fewer still what it hides."*

### The optional parts

The eight "sometimes" parts (goal, golden age, omens, newcomers, abandonment, founders' fate, visitors, present detail) are decided one by one: each is there **4 times out of 10**.

### The closing

A four-sided die:

- **no closing**;
- **a legend** (`legend`): *"It is said that a golden idol still lies in the deepest halls."*;
- **a warning** (`warning`): *"An old local saying warns: what is buried down there wants to stay buried."*;
- **an adventure hook** (`hook`): *"Now someone is offering a reward to whoever brings back a broken crown."*

If the history opens with a rumour, it doesn't close with a legend: that would be two pieces of gossip in a row.

### The parts echo each other

The extra ingredients are picked only once per dungeon, so several parts can speak of the same thing. The relic whispered about at the start is the same one someone offers a reward for at the end; the adventurer of the lost expedition is the same one an heir is looking for.

### Capitals

Many sentences begin with a placeholder (*"{f} wanted {built}…"*). The program capitalises the first letter of every sentence after filling it in: *"The counts of Norin wanted…"*.

---

## 7. A history taken apart piece by piece

Here is the history of seed `3-21-2-4-CDK-000F62`. The shape drawn is: an opening with today's dwellers, no optional part except the abandonment, the founders' fate and the present detail, a closing with a warning. The dungeon has natural caves, but no third-age room.

| Part | Sentence chosen (with placeholders) | Result |
|---|---|---|
| opening `opening` | Treasure hunters know well who haunts those corridors today: `{p}`. Few, though, know how it all began. | Treasure hunters know well who haunts those corridors today: *the bugbears of Inchalville*. Few, though, know how it all began. |
| founding | Many generations ago, `{area}`, `{f}` built `{built}`. | Many generations ago, *in the firefly marshes*, *the counts of Norin* built *a tower, a castle and an outpost among the caves*. |
| caves | They made use of the natural caves that already opened in the rock, widening them and joining them to their halls. | (the same) |
| second age | With `{e1}`, the founders vanished. In their place came `{s}`, who opened new passages and hid some of them. | With *the death of a lesser god*, the founders vanished. In their place came *the refugees of Eskrin*, who opened new passages and hid some of them. |
| end | Their time ended too: with `{e2}`, that age came to a close, and part of the passages collapsed. | Their time ended too: with *a flood*, that age came to a close, and part of the passages collapsed. |
| abandonment | The ruins lay silent for a long time. | (the same) |
| founders' fate | The founders' last words are still carved beside a walled-up door. | (the same) |
| ~~today's dwellers~~ | | skipped: the opening already named them |
| present detail | Those who live nearby keep their distance. | (the same) |
| ~~newer tunnels~~ | | skipped: no third-age room |
| closing `warning` | Whoever decides to go down had better bring rope, torches and a good reason to come back. | (the same) |

The result, as it appears in the key:

> Treasure hunters know well who haunts those corridors today: the bugbears of Inchalville. Few, though, know how it all began. Many generations ago, in the firefly marshes, the counts of Norin built a tower, a castle and an outpost among the caves. They made use of the natural caves that already opened in the rock, widening them and joining them to their halls. With the death of a lesser god, the founders vanished. In their place came the refugees of Eskrin, who opened new passages and hid some of them. Their time ended too: with a flood, that age came to a close, and part of the passages collapsed. The ruins lay silent for a long time. The founders' last words are still carved beside a walled-up door. Those who live nearby keep their distance. Whoever decides to go down had better bring rope, torches and a good reason to come back.

---

## 8. Three more histories, three different shapes

**The simplest shape**: no opening, no optional part, no closing. Seed `2-10-3-1-J-0GC50N` (a tomb):

> The oldest chronicles recall that the architects of Emperor Pyrka built a crypt beneath a forest of giant mushrooms. After the poisoning of the leader the halls stood empty; the dwarf miners of Ishaud found them so, took them over and opened passages kept hidden. Their rule did not last: after the loss of the heartstone the place fell into ruin and some passages collapsed. The few who came back to tell say that today's dwellers are a band of rival adventurers led by Rosina.

**A rumour as opening, a hook as closing**, with goal and golden age. Seed `1-11-2-2-I-04P6X8` (a border fortress):

> The last expedition to go down there, led by one Eskmorrup, never came back; but to understand why one must start from the beginning. Many generations ago, along the old imperial road, the dwarf wardens of Rosir built a fortified line. They did it to guard a secret, or so the chronicles say. In those years its halls rang with voices, songs and footsteps. It was a crusade that drove the founders out. Soon after came the witch hunters of Gloithette: they refitted the old halls and dug new tunnels, some of them secret. Then an invasion from the deep ended that age too, and some passages collapsed. Now those halls belong to whoever took them last: the gnolls of the Ethjun pack. The newest occupants dug the roughest tunnels and the latest entrances. A merchant in the nearby town pays well for any map of its halls.

**The place as opening, a legend as closing**, with omens and a present detail; there are caves and third-age rooms, so those two parts appear too. Seed `4-36-1-1-CCIK-01PANT` (tower, fortress, Underdark):

> On maps it is just a name, and those who live nearby would rather not say it. It all began when Ormia's mercenaries chose to build a tower, a border fortress and a network of tunnels in the middle of a jungle. They made use of the natural caves that already opened in the rock, widening them and joining them to their halls. The first cracks, in the walls and among the people, soon appeared. When a curse on the waters ended the founders' rule, the goblins of the Griminus tribe took possession of the place and changed it, opening passages known only to them. Their rule did not last: after the coming of a dragon the place fell into ruin and some passages collapsed. Now those halls belong to whoever took them last: the ghosts of the miners of Cuvar. Those who live nearby keep their distance. The roughest tunnels and the newest entrances date from this last age. It is said that Ormia's mercenaries hid something in the deepest halls, and that no one has found it yet.

---

## 9. How many different stories?

Let's count only the **shape**, that is, which parts are there:

- openings and closings: 4 openings × 4 closings = 16 combinations, minus 1 (rumour + legend) = **15**;
- optional parts: 8 parts, each there or not = 2⁸ = **256**;
- in all: 15 × 256 = **3,840 different shapes**.

Then each part has 3 to 8 possible sentences: multiplying them gives **thousands of billions** of sentence combinations. And we haven't counted the ingredients yet: 12 founders per type, 147 events, 35 second-age groups, 45 present-day groups, 124 places, the invented names… In practice, two dungeons with the same story never come out.

The program itself can count the shapes: the function `history_patterns()` returns 3,840 with the current JSON file. Add a new optional part to the code and the number doubles.

---

## 10. The strata

Below the history, the key lists the **strata**, oldest first:

```
STRATA (oldest first)
  N   Natural caves, older than any building  [#]
  I   the counts of Norin — a tower, a castle and an outpost among the caves  [═║]
  II  the refugees of Eskrin  [─│]
  III today: the bugbears of Inchalville  [#]
```

The square brackets hold the walls each age is drawn with on the map. If an age has no rooms (for instance no caves), *(no rooms)* appears next to it: the story remembers it, but the map doesn't show it.

---

## 11. Room descriptions

Every room has a **layered description**: what it was at first, and what the later ages made of it.

### The oldest layer

It depends on the room's age (decided by the map):

| Room's age | Where the name comes from |
|---|---|
| **N** natural cave | the 144 natural caves (*Fumarole cavern*) |
| **I** founders | the rooms of **its level's type** (*Flying books room* in a tower) |
| **II** second age | the rooms of the second-age group (*Underground garden*) |
| **III** today | the rooms of today's dwellers |

The **special rooms** of the floor plan take their name from a list of their own for their type: a castle's corner tower is called *Corner tower* or *Prison tower*, a tomb's burial chamber has a burial-chamber name, a tower's core is a *Wind stair*.

Names are drawn as from a **deck of cards**: until the deck runs out, the same name never comes up twice. Only when all have come up is the deck reshuffled.

### The later layers

Then the program rolls to see whether the room was reused:

| Room's age | Refitted in the second age | Reused today |
|---|---|---|
| N cave | 15% | 25% |
| I founders | 40% | 30% |
| II second age | — | 30% |
| III today | — | — |

Each added layer draws from that age's deck.

### How to read it

```
1-04 [I] Cloud room; II: makeshift shrine; III: goblin slave pen.
```

- `[I]`: the room belongs to the founders, who built it as a *Cloud room*;
- `II:` in the second age it became a *makeshift shrine*;
- `III:` today it is a *goblin slave pen*.

More examples from the same dungeon:

```
1-02 [I] Flying books room.
2a-01 [II] Underground garden.
3-03 [N] Great cavern; III: bunkroom.
3-08 [N] Singing stone cave; III: trap room.
```

The game master can read a room like a small archaeological dig: what is left of the founders, what the others added, what is there today.

---

## 12. Entrances, exits and connections

### Entrances

Each entrance has a description taken from the type of its level: from the **main entrances** if it is on the ground level, from the **side entrances** if it is on another level. If an entrance is a shaft from the surface, the type may have a description of its own, otherwise a generic one is used.

```
ENTRANCES AND EXITS
  A  tower gate (level 2) → 2-01
  B  natural chimney (level 3, midpoint entry) → 3-05
```

### The exits of each room

Below each room, the key lists **where you can go** and what the way is like:

```
2-01 [I] Prison tower; III: bugbear den.
       exits: → 2-03 (opening); → 2-02 (secret passage); > stairs down → 3-02; entrance A
```

| Text | Meaning |
|---|---|
| `→ 2-03 (door)` | a corridor with a door |
| `(opening)` | an opening without a door |
| `(secret door)` | the door on this side is secret |
| `(secret passage)` | the whole corridor is hidden |
| `(flooded)`, `(cave-in)`, `(steps)` | the corridor has water, a cave-in to climb over or steps |
| `> stairs down → 3-02`, `< stairs up` | a staircase to another level |
| `○ shaft → 3-08, skips one level` | a shaft that skips one or more levels |
| `Ω portal → 3-07` | a magic portal |
| `entrance A` | from here you go out into the open |

### Connections between levels

```
LEVEL CONNECTIONS
  1-03   ↔ 2-03   stairs
  1-02   ↔ 3-08   shaft/chimney
  1-04   ↔ 3-07   magic portal
```

A **hidden** staircase, shaft or portal is marked as such: the players don't see it on their map. How stairs, shafts, portals and entrances are chosen is explained in chapters 10 and 11 of [dungeon_map_generation.en.md](dungeon_map_generation.en.md#10-stairs-shafts-portals-and-sub-levels); here only how they appear in the key matters.

---

## 13. Where the story ends up: the key and the PDF

If you choose the story (alone or with monsters and traps), the program writes two files with the same content:

- **`<seed>_key.txt`**, the key as plain text, 100 letters wide: title, seed, type, scale, history, strata, entrances, connections, every room level by level, and finally the check of Jaquays' principles; with monsters and traps, also what [monsters.en.md](monsters.en.md) and [trap.en.md](trap.en.md) explain;
- **`<seed>_story.pdf`**, the same key as a book on A4 pages: headings in **Sebaldus-Gotisch**, text in **Crimson Text**, page numbers at the bottom.

The language is the one you chose at the start: every text exists in Italian and in English, and the program takes the right version.

If you don't choose the story, it is invented anyway (it is needed for the title and the names), but not written; with monsters or traps without the story, the key has no history, no strata and no room descriptions, and the PDF is called `<seed>_key.pdf`.

---

## 14. Writing new sentences without mistakes

You can add sentences to any part of `history`, and items to any list, by copying an existing line. The program draws from yours too. A few rules, so that sentences work with **any** ingredient — in both languages, because every sentence has an Italian and an English version:

| Placeholder | What it looks like | Rule | Right | Wrong |
|---|---|---|---|---|
| `{f}` founders | plural, with an article (*the counts of Norin*, *Queen Ysa and her court*) | plural verb | *{f} built…* | *{f} was…* |
| `{s}` second age | plural, with an article | plural verb | *in their place came {s}* | *{s} was…* |
| `{p}` today's dwellers | **singular or plural** (*a cult*, *the kobolds*) | no verb agreeing with them | *whoever goes down there meets {p}* | *today {p} live there* → "today a cult live there" |
| `{e1}`, `{e2}` events | singular, with an article (*the fall…*, *an eclipse*) | singular verb | *{e1} emptied the place* | *{e1} were…* |
| `{built}` | with "a"/"an", maybe several things (*a tower and a crypt*) | | *built {built}* | |
| `{area}` | starts with a preposition (*on a hill*, *in the desert*) | use it as it is | *built {built} {area}* | *in {area}* |
| `{goal}` | a bare verb phrase (*guard a secret*) | after "to" | *their purpose was to {goal}* | |
| `{relic}` | singular with "a"/"an" (*a broken crown*) | | *revolves around {relic}* | relics with *the* |
| `{visitors}` | plural **without** an article (*fugitive brigands*) | | *later {visitors} passed through* | |
| `{hero}` | a proper name | | *the heir of {hero}* | |

Italian adds a golden rule: **no preposition in front of a placeholder that starts with a definite article**, because the program can't turn "di i" into "dei" or "a la" into "alla". The Italian version of this document has the details.

A sentence can only use placeholders that exist: if it uses an unknown one (or the list it would draw from is missing), the program simply never picks it. An old JSON file, with one sentence per part and without the new parts, still works: the missing parts are skipped.
