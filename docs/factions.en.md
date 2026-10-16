# How the factions are made

*[Versione italiana](factions.md)*

This document explains how WyrmDelve invents the groups that fight over the dungeon: how many there are, where they come from, where they live, what they want and what they think of each other, with real examples made by the program.

> Factions appear only if at the start, at "What do you want to make?", you also tick the **factions** (or `--content factions`, also together with other things: `--content story,factions`). The history of the place, which they are born from, is explained in [story_generation_algorithm.en.md](story_generation_algorithm.en.md).

## Contents

1. [The idea: every faction is born from the history](#1-the-idea-every-faction-is-born-from-the-history)
2. [How many and where they come from](#2-how-many-and-where-they-come-from)
3. [The name and the base](#3-the-name-and-the-base)
4. [The sentences of a faction](#4-the-sentences-of-a-faction)
5. [Relations between factions](#5-relations-between-factions)
6. [How many different factions](#6-how-many-different-factions)
7. [In the key](#7-in-the-key)
8. [A complete example](#8-a-complete-example)
9. [Changing the tables](#9-changing-the-tables)

---

## 1. The idea: every faction is born from the history

Every WyrmDelve dungeon has a layered history: the **founders** who built it, those who came in the **second age**, **today's dwellers**, the events that ended each age, a **relic** of the legend and a lost **hero**. The factions are the groups moving through those ruins today, and each one is tied to a piece of that history: their sentences use the same names as the history, so players who read about "the disappearance of the children" or "a seed from an extinct tree" meet them again in the factions' plans.

Factions come **after** everything else and use dice of their own (made from the seed with the label `factions`): the map, the story, the monsters, the traps and the treasure of a seed don't change whether you choose factions or not.

---

## 2. How many and where they come from

There are **2 to 4** factions: 2 to start with, one more if the dungeon has at least 14 rooms, another if it has at least 3 main levels.

Every faction has an **origin**, the piece of history it is born from:

| Origin | Who they are | Example |
|---|---|---|
| `present` | groups living with **today's dwellers**: they serve them, pay them, spy on them or want them gone | "It serves the ghouls of the Thalmorn pack as court and shield, in exchange for crumbs from the loot." |
| `heirs` | the **heirs of the founders**, who keep their rites or want the place back | "It descends from the founders of the place, the kings of the Ulmar dynasty, and still keeps their oaths." |
| `second` | the last of the **second age**, or those who copy their ways | "It venerates the former masters of the place, the hobgoblin legionaries of Wyria, as saints, and keeps their bones in room 1-05." |
| `relic` | those who seek the **relic** of the legend | "It was born around a prophecy: whoever holds a seed from an extinct tree will rule all the deep places." |
| `outsiders` | **outsiders** from elsewhere: villagers, scholars, treasure hunters | "Its members come from the nearest village, sick of paying tribute and counting the missing." |

There is **always** a `present` faction, because today's dwellers are the heart of the dungeon; the other origins are drawn at random, without repeating.

---

## 3. The name and the base

**The name.** A word saying what kind of group it is, plus a name invented with the same syllables as places and people: *the Den of Peldi*, *the Church of Bekthalra*, *the Academy of Junippos*. Every name suits only some origins: a "Den" can be `present` or `second`, an "Academy" only `outsiders` or `relic`, and so on.

**The base.** Every faction has a room of its own, chosen among those of its age:

| Origin | Where it lives |
|---|---|
| `present` | a room of today's dwellers (stratum III) |
| `heirs` | a room of the founders (stratum I) |
| `second` | a room of the second age (stratum II) |
| `relic` | any room |
| `outsiders` | one of the three rooms closest to an entrance, or (one time in two) **outside the dungeon** |

Two factions never share a base. If there are no rooms of its age left, the faction takes another free one. Some sentences name the base ("keeps their bones in room 1-05") or only make sense for those living in the dungeon ("It patrols the corridors in pairs…", "…away from its halls"): a faction living outside the dungeon never draws them, and a relation of this kind ("have fought for a corridor") only links two factions that are both inside.

---

## 4. The sentences of a faction

Every faction is a paragraph of sentences, drawn from `data/factions.json`:

1. **where it comes from** (`origins`): always first;
2. **what it wants** (`goals`), **how it gets it** (`methods`) and, 7 times in 10, **who leads it** (`leaders`): these three in random order;
3. 6 times in 10, **a secret** (`secrets`): a truth the players can find out; in the key it starts with "Secret:", so the referee spots it at once;
4. **how it treats adventurers** (`attitudes`);
5. **what it thinks of another faction** (`relations`), if there is another one (see chapter 5).

The sentences have placeholders in braces, filled in with the dungeon's words:

| Placeholder | What it becomes | Example |
|---|---|---|
| `{f}`, `{s}`, `{p}` | the founders, those of the second age, today's dwellers | *the ghouls of the Thalmorn pack* |
| `{e1}`, `{e2}` | the events that ended the two ages | *the disappearance of the children* |
| `{built}`, `{area}`, `{title}` | what was built, where, the name of the place | *a watchtower* |
| `{relic}`, `{hero}`, `{goal}`, `{visitors}` | the relic, the lost hero, the founders' purpose, who passed through | *a seed from an extinct tree*, *Dubiiya* |
| `{faction}`, `{other}` | the name of the faction and of the other faction | *the Den of Peldi* |
| `{leader}` | the leader's name, invented | *Duncalme* |
| `{room}` | the room of the base | *1-05* |

Some `present` origins say the faction **serves** today's dwellers ("It serves … as court and shield"): these have `"leader": false`, and the faction has no leader of its own, because its leader is the dwellers' one.

Every table's deck is shuffled once per dungeon: two factions of the same dungeon never share a goal, method, leader, secret or attitude.

---

## 5. Relations between factions

The factions are linked in a **ring**: the first has an opinion of the second, the second of the third, and the last of the first. With two factions there is a single relation, from the first to the second. A relation can be an alliance, a truce, a debt, a coming betrayal:

> To get a seed from an extinct tree, the Pact of Dratuchal would betray the Church of Bekthalra without a second thought.

This way every faction has at least one tie to another, and the referee always has a lever to set the groups against each other.

---

## 6. How many different factions

**Content.** Multiplying the possible choices for one faction:

| Part | Choices |
|---|---|
| name | 44 |
| origin, with or without one of the 24 leaders | 65 origins × 25 + 2 origins with no leader = 1,627 |
| goal | 37 |
| method | 32 |
| secret, or none | 29 + 1 = 30 |
| attitude | 19 |

44 × 1,627 × 37 × 32 × 30 × 19 = **48,313,309,440** different factions, without counting the invented names, the relations (20) and the history's words, which change in every dungeon.

**Form.** Goal, method and leader in random order give 6 orders with a leader and 2 without; with or without a secret: (6 + 2) × 2 = **16 shapes** of the paragraph.

---

## 7. In the key

Factions have a section of their own, **FACTIONS**, after the history and the strata and before the entrances; in the PDF it is a chapter with each faction's name in bold:

```
FACTIONS
  The Den of Peldi (base: 1a-02)
    It serves the ghouls of the Thalmorn pack as court and shield, in exchange for crumbs from the
    loot. It has sworn to avenge Dubiiya, and has already decided whom to blame. …
```

While generating, the program says how many factions it made: `Factions: 3 (The Den of Peldi, The Pact of Dratuchal and The Church of Bekthalra)`.

Factions don't show on the maps: they are only in the key.

---

## 8. A complete example

Seed `2-14-2-1-C-02SFP3`: a two-level watchtower with sub-level 1a. Its history: the hermits of Lumjorthor built it at the foot of a volcano; the volcano's waking emptied it; the hobgoblin legionaries of Wyria took it until the disappearance of the children ended their age; today the ghouls of the Thalmorn pack live there. Its 14 rooms give 3 factions:

> **The Den of Peldi (base: 1a-02)**
> It serves the ghouls of the Thalmorn pack as court and shield, in exchange for crumbs from the loot. It has sworn to avenge Dubiiya, and has already decided whom to blame. It patrols the corridors in pairs, with shuttered lanterns and a bone whistle. Secret: its gold is false: gilded lead, struck in a workshop hidden in room 1a-02. It sets a bounty on any adventurer who fails to report to its leader first. For years the Den of Peldi has believed the Pact of Dratuchal was on its side; the betrayal is near, and nobody expects it.
>
> **The Pact of Dratuchal (base: 1-05)**
> It venerates the former masters of the place, the hobgoblin legionaries of Wyria, as saints, and keeps their bones in room 1-05. It poisons the wells and cisterns it does not use, and leaves a blue-painted skull on the rim. It is looking for Dubiiya, or whatever is left, and above all for the map Dubiiya carried. Its fate rests with Duncalme, who always carries the journal of Dubiiya and quotes it like scripture. It demands a toll of ten silver coins a head, then lets anyone pass with no questions. To get a seed from an extinct tree, the Pact of Dratuchal would betray the Church of Bekthalra without a second thought.
>
> **The Church of Bekthalra (base: 2-01)**
> It owns the only faithful drawing of a seed from an extinct tree, and shows it only to the sworn. In charge now is Bahal, who killed the previous chief at a feast and reminds everyone of it at every meal. It aims to turn the place into an underground market, with the ghouls of the Thalmorn pack standing guard for a fee. It wages war with fire: barrels of pitch, torches and smoke to drive out whoever hides. Secret: most of its members are straw dummies dressed and armed: there are four of them in flesh and blood. It fears adventurers and flees, but writes down their names and their weapons. Whenever the Den of Peldi loses a member, the Church of Bekthalra gains one: the deserters always change sides in the same direction.

You can see that:

- **the Den** is the `present` faction: it serves the ghouls, so it has no leader of its own, and its secret is hidden right in its base;
- **the Pact** is `second`: it venerates the hobgoblins of the second age and has its base in one of their halls; it seeks the lost hero of the history;
- **the Church** is `relic`: everything turns around the seed from an extinct tree, the relic of the legend;
- the relations make a ring: the Den trusts the Pact, which will betray it; the Pact would betray the Church; the Church steals members from the Den.

---

## 9. Changing the tables

Everything is in `data/factions.json`. Make a copy of the file before you edit it.

| Entry | What it holds |
|---|---|
| `names` | the names: `it` and `en` with `{n}` for the invented name, and `origins`, the origins the name suits |
| `origins` | where a faction comes from, for each origin: `present` (uses `{p}`), `heirs` (`{f}`), `second` (`{s}`), `relic` (`{relic}`), `outsiders`; `"leader": false` for those who serve today's dwellers |
| `goals`, `methods` | what it wants and how it gets it |
| `leaders` | who leads it (uses `{leader}`) |
| `secrets` | the secrets |
| `attitudes` | how it treats adventurers |
| `relations` | what it thinks of another faction (uses `{faction}` and `{other}`) |

Next to `it` and `en`, every sentence can have conditions:

| Condition | What it means |
|---|---|
| `"inside": true` | only for a faction with its base in the dungeon (for a relation: both factions) |
| `"not": ["outsiders"]` | not for these origins (here: not for outsiders, who for instance don't know the founders' language) |
| `"leader": false` | origins only: the faction has no leader of its own |

A name and a sentence:

```json
{"it": "l'Ordine di {n}", "en": "the Order of {n}", "origins": ["heirs", "relic", "outsiders"]}
{"it": "Vuole recuperare {relic} prima di chiunque altro.", "en": "It wants to recover {relic} before anyone else does."}
{"it": "Pattuglia i corridoi a coppie, …", "en": "It patrols the corridors in pairs, …", "inside": true}
```

In English, faction names start with a lowercase `the` (the program capitalises it when needed), a sentence doesn't start with `{faction}` or `{other}`, and there is no *he* or *she*: leaders can be anyone. The rules for the Italian sentences are in [factions.md](factions.md#9-cambiare-le-tabelle).

If `data/factions.json` is missing or has a mistake, the program says so and makes the dungeon without factions.
