# How the rumours are made

*[Versione italiana](rumours.md)*

This document explains how WyrmDelve prepares the rumour table: the rumours, true and false, the adventurers hear about the dungeon before going in, with real examples made by the program.

> Rumours appear only if at the start, at "What do you want to make?", you also tick the **rumours** (or `--content rumours`, also together with other things: `--content treasure,npcs,rumours`). What they are about depends on what else you chose: see chapter 3.

## Contents

1. [The idea: a table for the referee](#1-the-idea-a-table-for-the-referee)
2. [How many, how many true](#2-how-many-how-many-true)
3. [What they are about](#3-what-they-are-about)
4. [How the program knows a rumour is true](#4-how-the-program-knows-a-rumour-is-true)
5. [Who tells them](#5-who-tells-them)
6. [How many different rumours](#6-how-many-different-rumours)
7. [In the key](#7-in-the-key)
8. [A complete example](#8-a-complete-example)
9. [Changing the tables](#9-changing-the-tables)

---

## 1. The idea: a table for the referee

Before going down, the adventurers ask around: at the inn, in the village, whoever hires them. The referee rolls on the rumour table and tells them what comes up. Some rumours are true and really help (treasure in a certain room, an NPC's secret); others are false and can cost dearly. In the key every rumour is marked **true** or **false**: only the referee knows.

Rumours come **after** everything else and use dice of their own (made from the seed with the label `rumours`): the map, the story, the monsters, the traps, the treasure, the factions and the NPCs of a seed don't change whether you choose rumours or not.

---

## 2. How many, how many true

The table is a **d8**, with two more rumours (d10) if the dungeon has at least 14 rooms and two more (d12) if it has at least 3 main levels.

About **a third** of the rumours are false: a third of the table, rounded down, plus one half of the time. A d12 table has 4 or 5 false rumours, a d8 one 2 or 3. True and false ones are shuffled at random.

---

## 3. What they are about

| Subject | When | Example |
|---|---|---|
| the **history** | always | "The village physician, cleaning the instruments, remarks: first came the miners of Beard; then the vanishing of the patron god swept their age away." |
| how many **levels** | always, one rumour at most | "The place has two levels, and anyone who claims to have seen more is lying." |
| how many **entrances** | always, one rumour at most | "Anyone who wants to get in has two entrances to choose from." |
| a **treasure** | if you chose treasure | "A fine haul waits in room 1-02, inside a hollow statue." |
| where an **NPC** is | if you chose NPCs | "You can only talk with Linex in room 2-03, and only after laying down your weapons." |
| an NPC's **secret** | if you chose NPCs | "One night, deep in the wine, Ishdravig said too much: she is the only one who knows the word that opens the door of room 1-05, and says it in her sleep." |
| where a **faction** is | if you chose factions | "If you are looking for the Silence of Esnar, look in room 3-01." |
| a faction's **secret** | if you chose factions | "There is a reason the Oath of Thalkorglo trusts no one: the name it bears is stolen: it belonged to the sworn enemies of the founders." |

The subjects are drawn from a deck where the history counts three times, the treasure twice, NPC and faction secrets twice: so a table mixes a bit of everything. The same treasure, NPC or faction never comes back in two rumours of the same kind.

---

## 4. How the program knows a rumour is true

The **history** sentences are written already true or already false: the true ones only say what holds in every dungeon (who built it, what ended each age, who lives there today, the legend of the relic and of the lost hero); the false ones swap the ages, deny the facts or invent certainties ("the hero came back rich and lives in the city").

All the other sentences are **neutral**: they become true or false depending on the facts the program fills them with.

| Subject | True | False |
|---|---|---|
| treasure | a room that really holds treasure, with its hiding place and its value (rounded, as rumours do) | a room without treasure, with an invented hiding place and value |
| where an NPC or faction is | their real room | another room |
| an NPC's or faction's secret | their real secret (the same as in their section of the key) | a secret from the table they don't have |
| levels, entrances | the real number | a close but wrong number |

A true rumour about a secret is possible only for someone who has a secret; one about a treasure's value only if the treasure is worth at least 10 gold pieces (otherwise the sentence uses the hiding place).

---

## 5. Who tells them

One rumour in two starts with **who tells it**: "An old miner swears:", "The tavern keeper, wiping a mug that never gets clean, maintains:", "A green-fingered herbalist assures you:". The others are the rumour alone. The source says nothing about the truth: even the barefoot child can be right.

---

## 6. How many different rumours

**Content.** There are 209 statements (42 true and 42 false about the history, 30 about treasure, 18 + 17 about NPCs, 17 + 17 about factions, 13 about levels, 13 about entrances), and each can be told by one of the 78 sources or by none: 209 × 79 = **16,511** different rumours, without counting the facts they are filled with (rooms, names, secrets, hiding places, values, the words of the history). A d8 table puts 8 together: more than 10²⁹ different tables.

**Form.** Every rumour has 2 forms (with or without a source), and the false ones can be in any position: a d8 table has 2⁸ × (28 + 56) = **21,504** forms, a d10 one **337,920**, a d12 one **5,271,552**.

---

## 7. In the key

Rumours have a section of their own, **RUMOURS**, after the NPCs and before the entrances; in the PDF it is a chapter with the number in bold and "true" or "false" in italics:

```
RUMOURS
  Roll 1d10 for each rumour the adventurers hear before going in (at the tavern, in the village,
  from whoever hires them). Only the referee knows which are true.
    1. [true] A green-fingered herbalist assures you: anyone who wants to get in has two entrances
       to choose from.
    …
```

While generating, the program says what the table is like: `Rumours: d10, 6 true and 4 false`.

---

## 8. A complete example

Seed `2-14-2-1-C-02SFP3`, with everything: 2 levels and 14 rooms, so a d10 table. It is the same dungeon as the examples in [factions.en.md](factions.en.md) and [npcs.en.md](npcs.en.md).

| d10 | | Rumour | Why |
|---|---|---|---|
| 1 | true | A green-fingered herbalist assures you: anyone who wants to get in has two entrances to choose from. | there are 2 entrances |
| 2 | false | For anyone dealing with the Pact of Dratuchal, only one thing matters: in truth a seed from an extinct tree lies above ground, under the altar of the village church. | not the Pact's secret |
| 3 | false | The place has had a single master in all its history, and still does: the ghouls of the Thalmorn pack. | false history: the hermits and the hobgoblins came first |
| 4 | true | An old woman who boasts of the founders' blood swears: one night, deep in the wine, Ishdravig said too much: she is the only one who knows the word that opens the door of room 1-05, and says it in her sleep. | Ishdravig's secret |
| 5 | true | The place has two levels, and anyone who claims to have seen more is lying. | there are 2 main levels |
| 6 | false | A wizard's apprentice hunting for ingredients claims: anyone who has seen the Den of Peldi up close knows appearances deceive: it keeps Dubiiya in chains in room 1a-02, and tells everyone a different story. | not the Den's secret |
| 7 | false | You can only talk with Linex in room 2-03, and only after laying down your weapons. | Linex is in room 2-02 |
| 8 | true | The survivor of an old expedition, staring at nothing, repeats: a hoard worth 110 gold pieces in room 1a-02: that is what those walls really hide. | room 1a-02 holds 110 gp of treasure |
| 9 | true | A fine haul waits in room 1-02, inside a hollow statue. | room 1-02 holds treasure, right there |
| 10 | true | They say that at some point shepherds caught in a storm took shelter down there too. | history: they passed through |

You can see that the table gives the adventurers two true leads to treasure, one of the Pact's halls (room 1-05) through Ishdravig's secret, and two traps: a false secret that could set them against the Den of Peldi, and the wrong room for Linex.

---

## 9. Changing the tables

Everything is in `data/rumours.json`. Make a copy of the file before you edit it.

| Entry | What it holds | Placeholders |
|---|---|---|
| `sources` | who tells the rumour, without final punctuation (the program adds ":") | the history's |
| `history_true`, `history_false` | true and false statements about the history | the history's |
| `treasure` | treasure in a room | `{room}` and `{where}` (the hiding place) or `{value}` ("2,700 gold pieces") |
| `npc_room`, `faction_room` | where an NPC, a faction is | `{npc}` or `{faction}`, and `{room}` |
| `npc_secret`, `faction_secret` | an NPC's, a faction's secret | `{npc}` or `{faction}`, and at the end `: {secret}` |
| `levels`, `entrances` | how many levels, how many entrances | `{levels}` ("four levels", "a single level"), `{entrances}` ("two entrances", "a single entrance") |

The history's placeholders are those of the factions (see [factions.en.md](factions.en.md#4-the-sentences-of-a-faction)). A sentence:

```json
{"it": "Se cercate {faction}, guardate nella sala {room}.", "en": "If you are looking for {faction}, look in room {room}."}
```

`history_true` sentences must be true in **any** dungeon: nothing about where the relic is or whether the hero is dead. In English, no *he* or *she*. The rules for the Italian sentences are in [rumours.md](rumours.md#9-cambiare-le-tabelle).

If `data/rumours.json` is missing or has a mistake, the program says so and makes the dungeon without rumours.
