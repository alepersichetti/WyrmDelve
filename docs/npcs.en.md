# How the NPCs are made

*[Versione italiana](npcs.md)*

This document explains how WyrmDelve invents the non-player characters (NPCs) the adventurers can meet in the dungeon: how many there are, who they are, how they are tied to the history of the place and to the factions, where they are and what they want, with real examples made by the program.

> NPCs appear only if at the start, at "What do you want to make?", you also tick the **NPCs** (or `--content npcs`, also together with other things: `--content factions,npcs`). The history of the place is explained in [story_generation_algorithm.en.md](story_generation_algorithm.en.md), the factions in [factions.en.md](factions.en.md).

## Contents

1. [The idea: people with a reason to be there](#1-the-idea-people-with-a-reason-to-be-there)
2. [How many and who they are](#2-how-many-and-who-they-are)
3. [Name, gender, role and room](#3-name-gender-role-and-room)
4. [The sentences of an NPC](#4-the-sentences-of-an-npc)
5. [Relations between NPCs](#5-relations-between-npcs)
6. [How many different NPCs](#6-how-many-different-npcs)
7. [In the key](#7-in-the-key)
8. [A complete example](#8-a-complete-example)
9. [Changing the tables](#9-changing-the-tables)

---

## 1. The idea: people with a reason to be there

A WyrmDelve NPC is not a random encounter: they are in the dungeon **for something to do with the place**. They descend from the founders, serve today's dwellers, seek the relic of the legend, know what happened to the lost hero, or belong to one of the factions. Their sentences use the same names as the history and the factions, so the referee gets a web of people who know each other, hate each other and owe each other favours.

NPCs come **after** everything else and use dice of their own (made from the seed with the label `npcs`): the map, the story, the monsters, the traps, the treasure and the factions of a seed don't change whether you choose NPCs or not.

---

## 2. How many and who they are

There are **3 to 5** NPCs: 3 to start with, one more if the dungeon has at least 14 rooms, another if it has at least 3 main levels.

If you also chose the **factions**, some NPCs belong to them: at most all but two, at least one, and never more than the factions. Each of them belongs to a different faction and, one time in two, is its **leader**, if the faction has a named one: then they have the very name of the leader in the factions section.

The other NPCs are **loners**, each tied to a different piece of the history:

| Kind | Who they are | Example |
|---|---|---|
| `present` | tied to **today's dwellers**: they serve them, worship them, are their prisoners | "Venera gli uomini fungo di Balabad come dei viventi, e lascia offerte che nessuno ha mai chiesto." |
| `heirs` | tied to the **founders**: they descend from them, keep their memory | "He was raised by the last faithful of the founders, the hermits of Lumjorthor, and knows their prayers by heart." |
| `second` | tied to those of the **second age** | "Sua nonna era tra gli hobgoblin mercanti di schiavi di Leebek e, a sentire i vecchi, fu proprio lei a scatenare una crociata." |
| `relic` | drawn by the **relic** | "She heard in a tavern that a seed from an extinct tree cures every ailment, and has a sick daughter at home." |
| `outsiders` | come **from outside**: the village, the city, a failed expedition | "Insegue un debitore che è scappato laggiù con la cassa di una confraternita." |
| `member` | **members** of a faction | "She has fought for the Den of Peldi ever since she lost an eye in a clash with the ghouls of the Thalmorn pack." |
| `leader` | **leaders** of a faction | "Fu eletta per acclamazione, e ora guida il Branco di Rinu senza sapere bene come si faccia." |

The loners' kinds are drawn at random, without repeating.

---

## 3. Name, gender, role and room

**The name** is invented with the same syllables as places and people, and is never the lost hero's, a faction leader's (unless the NPC is that leader) or another NPC's.

**The gender** is rolled for every NPC: it decides the Italian word endings ("innamorata", "riconosciuto") and the English pronouns (*he*, *she*).

**The role** says what they do or what they are: *former slave*, *ratcatcher*, *fallen priest*, *librarian*. Every role suits only some kinds.

**The room:**

| Kind | Where they are |
|---|---|
| `member`, `leader` | at their faction's base (outside the dungeon, if the faction lives outside) |
| `present` | in a room of today's dwellers (stratum III) |
| `heirs` | in a room of the founders (stratum I) |
| `second` | in a room of the second age (stratum II) |
| `relic` | in any room |
| `outsiders` | in one of the three rooms closest to an entrance, or (one time in three) **outside the dungeon** |

Loners never share a room with each other, nor with a faction's base. An NPC outside the dungeon never draws sentences that name their room or only make sense for those living down there.

---

## 4. The sentences of an NPC

Every NPC is a paragraph of sentences, drawn from `data/npcs.json`:

1. **their tie to the place** (`origins`, for their kind): always first;
2. **what they want** (`wants`), **how they come across** (`manners`: looks, habits, a detail to play) and **what they can offer** the adventurers (`offers`): these three in random order;
3. 6 times in 10, **what they fear** (`fears`), after the first of those three;
4. one time in two, **a secret** (`secrets`): in the key it starts with "Secret:", so the referee spots it at once;
5. **what they think of another NPC** (`relations`, see chapter 5).

The placeholders are those of the factions (see [factions.en.md](factions.en.md#4-the-sentences-of-a-faction)), plus:

| Placeholder | What it becomes |
|---|---|
| `{npc}` | the NPC's name |
| `{faction}` | their faction, with a lowercase article: *the Den of Peldi* |
| `{other}` | another NPC's name |
| `{room}` | their room |
| `{o}` | in Italian, `o` or `a` by gender: "riconosciut{o}" |
| `{He}`, `{he}`, `{him}`, `{his}`, `{His}` | in English, the pronouns by gender |

Every table's deck is shuffled once per dungeon: two NPCs of the same dungeon never share a want, manner, offer, fear or secret.

---

## 5. Relations between NPCs

Like the factions, the NPCs are linked in a **ring**: the first has feelings about the second, the second about the third, and the last about the first. A relation can be a debt, a secret love, a hatred, blackmail:

> She owes Rokael a hot meal and a stitched wound, and always pays her debts.

Relations cross the factions: a member of one faction can be in love with a member of another, and a loner can blackmail a faction's leader.

---

## 6. How many different NPCs

**Content.** Multiplying the possible choices for one NPC:

| Part | Choices |
|---|---|
| role | 58 |
| tie to the place | 96 |
| want | 51 |
| manner | 51 |
| offer | 35 |
| fear, or none | 35 + 1 = 36 |
| secret, or none | 41 + 1 = 42 |
| relation | 30 |

58 × 96 × 51 × 51 × 35 × 36 × 42 × 30 = **22,992,207,436,800** different NPCs (almost 23 trillion), without counting the gender, the invented names and the words of the history and the factions, which change in every dungeon.

**Form.** Want, manner and offer in random order give 6 orders; with or without a fear, with or without a secret: 6 × 2 × 2 = **24 shapes** of the paragraph.

---

## 7. In the key

NPCs have a section of their own, **NON-PLAYER CHARACTERS**, after the factions and before the entrances; in the PDF it is a chapter with each NPC's name in bold. Next to the name come the role, the room and, for those who belong to one, the faction:

```
NON-PLAYER CHARACTERS
  Ishdravig, former slave (room 1-05; the Pact of Dratuchal)
    Within the Pact of Dratuchal she is known as the only one who is not afraid of the dark. …
```

While generating, the program says how many NPCs it made: `NPCs: 4 (Ishdravig, Rokael, Nulunim and Linex)`.

NPCs don't show on the maps: they are only in the key.

---

## 8. A complete example

Seed `2-14-2-1-C-02SFP3`, with the factions: the two-level watchtower whose factions are in [factions.en.md](factions.en.md#8-a-complete-example). The founders are the hermits of Lumjorthor, the second age the hobgoblin legionaries of Wyria, today's dwellers the ghouls of the Thalmorn pack; the relic is a seed from an extinct tree and the lost hero is Dubiiya. Its 14 rooms give 4 NPCs:

> **Ishdravig, former slave (room 1-05; the Pact of Dratuchal)**
> Within the Pact of Dratuchal she is known as the only one who is not afraid of the dark. Like a horse, she sleeps standing up against a wall. For fear that the second masters, the hobgoblin legionaries of Wyria, might return, she has bricked up three doors with her own hands. Rat bones tell her the future, and sometimes they get it right. Bringing Dubiiya home is her aim, or at least Dubiiya's sword. Secret: she is the only one who knows the word that opens the door of room 1-05, and says it in her sleep. She owes Rokael a hot meal and a stitched wound, and always pays her debts.
>
> **Rokael, ratcatcher (room 1a-02; the Den of Peldi)**
> She has fought for the Den of Peldi ever since she lost an eye in a clash with the ghouls of the Thalmorn pack. Out of revenge she wants to bring the deepest halls down on the current masters, the ghouls of the Thalmorn pack. She is afraid Dubiiya will come back: unlike the others, she knows why the expedition failed. In a little diary she notes every wrong suffered, with date and culprit. Anyone hunting werewolves can have her silver arrows, gladly given. She distrusts Nulunim, who speaks too well and never sweats.
>
> **Nulunim, librarian (room 1-02)**
> He was raised by the last faithful of the founders, the hermits of Lumjorthor, and knows their prayers by heart. He can translate the inscriptions of the founders, the hermits of Lumjorthor, but only by day: at night the letters move. He has a three-legged dog that growls at liars. Proof is what he is after: proof that the hermits of Lumjorthor themselves brought about the awakening of a volcano. Secret: out of jealousy, he killed Dubiiya with his own hands. Every month he pays Linex to keep quiet about a certain night.
>
> **Linex, fallen priest (room 2-02)**
> She heard in a tavern that a seed from an extinct tree cures every ailment, and has a sick daughter at home. She only ever whispers, and grows angry with anyone who raises their voice. Mirrors and still water terrify her: the face reflected there is not her own. Room 2-02 is a safe shelter for one night, where no monster ever enters, and she gladly shares it. Her plan is simple: get rich, and she is not ashamed to say so. She admires Ishdravig beyond all reason, and even copies Ishdravig's walk.

You can see that:

- **Ishdravig** and **Rokael** belong to two factions and live at their bases (the Pact keeps the bones of the second age in room 1-05, and Ishdravig fears their return);
- **Nulunim** is an `heirs` loner, raised among the founders' faithful; **Linex** is a `relic` loner, drawn by the seed from an extinct tree;
- the secrets tie into the history and into each other: Nulunim killed the lost hero, and pays Linex to keep quiet about "a certain night", while Ishdravig wants to bring Dubiiya home and Rokael knows why the expedition failed;
- the relations make a ring across the factions: Ishdravig (Pact) owes Rokael (Den), who distrusts Nulunim, who pays Linex, who admires Ishdravig.

---

## 9. Changing the tables

Everything is in `data/npcs.json`. Make a copy of the file before you edit it.

| Entry | What it holds |
|---|---|
| `roles` | the roles: `it` as a [masculine, feminine] pair, `en`, and `kinds`, the NPC kinds the role suits |
| `origins` | the tie to the place, for each kind: `present` (uses `{p}`), `heirs` (`{f}`), `second` (`{s}`), `relic` (`{relic}`), `outsiders`, `member` and `leader` (`{faction}`) |
| `wants`, `fears`, `secrets` | what they want, fear, hide |
| `manners` | how they come across: looks, habits, a detail to play |
| `offers` | what they can give or do for the adventurers, and at what price |
| `relations` | what they think of another NPC (uses `{other}`) |

The conditions are those of the factions, plus one:

| Condition | What it means |
|---|---|
| `"inside": true` | only for an NPC who lives in the dungeon |
| `"not": ["outsiders", …]` | not for these kinds |
| `"faction": true` | only for an NPC who belongs to a faction (required on sentences with `{faction}`) |

A role and a sentence:

```json
{"it": ["cartografo rinnegato", "cartografa rinnegata"], "en": "renegade cartographer", "kinds": ["outsiders", "member"]}
{"it": "Desidera soltanto essere dimenticat{o} da tutti, a cominciare dai creditori.", "en": "All {he} wants is to be forgotten by everyone, starting with the creditors."}
```

In English, write the NPC's pronouns as placeholders (`{he}`, `{his}`…), never *he* or *she*. The rules for the Italian sentences are in [npcs.md](npcs.md#9-cambiare-le-tabelle).

If `data/npcs.json` is missing or has a mistake, the program says so and makes the dungeon without NPCs.
