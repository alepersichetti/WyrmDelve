# The data folder

*[Versione italiana](README.it.md)*

Everything WyrmDelve draws at random is here, as JSON text files: `wyrmdelve.py` holds only the logic. Every text is written in Italian and in English, as `{"it": "…", "en": "…"}`. Make a copy of a file before you edit it; chapter 7 of the [README](../README.md#7-changing-the-words-of-the-dungeons) explains how.

| File | What it holds | Used by |
|---|---|---|
| `names.json` | syllables and endings for the names of places and people | names |
| `dungeon_types/` | the 11 dungeon types, one file each, numbered in menu order: names, how they stack, floor plan, founders, rooms, entrances | map and story |
| `second_age.json` | who came next (stratum II) and their rooms | story |
| `present_day.json` | today's dwellers (stratum III) and their rooms | story, monsters |
| `places.json` | natural caves, where the dungeon is, the shaft from the surface | map and story |
| `events.json` | what ended each age | story |
| `history.json` | the sentences of the history and the words they draw from | story |
| `monsters.json` | the 245 monsters, with their treasure type | monsters, treasure |
| `clues.json` | the clues monsters leave in empty rooms | monsters |
| `quirks.json` | why a monster is out of place | monsters |
| `traps.json` | ready-made traps and the triggers, mechanisms and twists new ones are assembled from (optional) | traps |
| `treasure.json` | the treasure tables (optional) | treasure |
| `factions.json` | names, origins, goals, methods, leaders, secrets, attitudes and relations of the factions (optional) | factions |
| `npcs.json` | roles, ties to the place, wants, fears, secrets, manners, offers and relations of the non-player characters (optional) | NPCs |
| `rumours.json` | sources and statements of the rumours, true and false (optional) | rumours |

Every `.json` file in this folder adds its sections to the tables, except `traps.json`, `treasure.json`, `factions.json`, `npcs.json` and `rumours.json`, which are read on their own: without them the program makes dungeons without traps, treasure, factions, NPCs or rumours. A new type goes in `dungeon_types/` with the next number.

How the program uses them: [docs](../docs).

## Sources and licenses

- Some entries (room features, caves, places, site names, threats, settlement troubles) are translated and adapted from *Ironsworn* and *Ironsworn: Delve* by Shawn Tomkin ([ironswornrpg.com](https://ironswornrpg.com)), licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/); Ironsworn name syllables likewise.
- The Tolkien-style syllables and endings in `names.json` are frequency statistics derived from Angband's name list; the list itself is not copied.
- `monsters.json` was drawn up by comparing *OSR Bestiary* v1.2 by bucolian and *Aketon*'s *Monstrous Bestiary* by Reese Surles: only the generic names and the Hit Dice (for the danger level) come from them; the descriptions are written for WyrmDelve. The aboleth comes from the System Reference Document 5.1 by Wizards of the Coast LLC, licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
- `treasure.json` and the treasure type letters in `monsters.json` are Open Game Content under the [Open Game License 1.0a](../LICENSE-OGL.txt), adapted and translated from the *Old-School Essentials System Reference Document* © 2019 Gavin Norman.
- The traps marked `"source": "srd35"` in `traps.json` are Open Game Content under the [Open Game License 1.0a](../LICENSE-OGL.txt), adapted from the sample traps of the *System Reference Document 3.5* © 2000-2003 Wizards of the Coast, Inc. The other traps, the triggers, the mechanisms and the twists are written for WyrmDelve, following the principles of Arnold K.'s *Some Traps* (Goblin Punch).
- Everything else is written for WyrmDelve and covered by the [GPL 3.0](../LICENSE) like the program.
