# La cartella data

*[English version](README.md)*

Qui c'è tutto quello che WyrmDelve pesca a caso, in file di testo JSON: `wyrmdelve.py` contiene solo la logica. Ogni testo è scritto in italiano e in inglese, come `{"it": "…", "en": "…"}`. Fai una copia di un file prima di modificarlo; il capitolo 7 del [README](../README.it.md#7-cambiare-le-parole-dei-dungeon) spiega come.

| File | Cosa contiene | Chi lo usa |
|---|---|---|
| `names.json` | sillabe e desinenze per i nomi di luoghi e persone | nomi |
| `dungeon_types/` | gli 11 tipi di dungeon, un file per tipo, numerati nell'ordine del menu: nomi, come si impilano, pianta, fondatori, stanze, ingressi | mappa e storia |
| `second_age.json` | chi venne dopo (strato II) e le sue stanze | storia |
| `present_day.json` | gli abitanti di oggi (strato III) e le loro stanze | storia, mostri |
| `places.json` | grotte naturali, dove si trova il dungeon, il pozzo dalla superficie | mappa e storia |
| `events.json` | cosa chiuse ogni epoca | storia |
| `history.json` | le frasi della storia e le parole da cui pescano | storia |
| `monsters.json` | i 245 mostri, con il loro tipo di tesoro | mostri, tesori |
| `clues.json` | gli indizi che i mostri lasciano nelle stanze vuote | mostri |
| `quirks.json` | perché un mostro è fuori posto | mostri |
| `traps.json` | le trappole già pronte e gli inneschi, i meccanismi e le varianti con cui se ne montano di nuove (facoltativo) | trappole |
| `treasure.json` | le tabelle dei tesori (facoltativo) | tesori |
| `factions.json` | nomi, origini, scopi, metodi, capi, segreti, atteggiamenti e rapporti delle fazioni (facoltativo) | fazioni |
| `npcs.json` | ruoli, legami con il luogo, desideri, paure, segreti, modi, offerte e rapporti dei personaggi non giocanti (facoltativo) | PNG |
| `rumours.json` | fonti e affermazioni delle dicerie, vere e false (facoltativo) | dicerie |

Ogni file `.json` di questa cartella aggiunge le sue sezioni alle tabelle, tranne `traps.json`, `treasure.json`, `factions.json`, `npcs.json` e `rumours.json`, che vengono letti a parte: senza, il programma fa dungeon senza trappole, tesori, fazioni, PNG o dicerie. Un tipo nuovo va in `dungeon_types/` con il numero successivo.

Come li usa il programma: [docs](../docs).

## Fonti e licenze

- Alcune voci (caratteristiche delle stanze, grotte, luoghi, nomi dei siti, minacce, guai degli insediamenti) sono tradotte e adattate da *Ironsworn* e *Ironsworn: Delve* di Shawn Tomkin ([ironswornrpg.com](https://ironswornrpg.com)), con licenza [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/); così anche le sillabe dei nomi di Ironsworn.
- Le sillabe e le desinenze in stile Tolkien di `names.json` sono statistiche di frequenza ricavate dalla lista di nomi di Angband; la lista non è copiata.
- `monsters.json` è stato ricavato confrontando *OSR Bestiary* v1.2 di bucolian e il *Monstrous Bestiary* di *Aketon* di Reese Surles: da questi vengono solo i nomi generici e i Dadi Vita (per il livello di pericolo); le descrizioni sono scritte per WyrmDelve. L'aboleth viene dal System Reference Document 5.1 di Wizards of the Coast LLC, con licenza [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
- `treasure.json` e le lettere dei tipi di tesoro in `monsters.json` sono Open Game Content con [Open Game License 1.0a](../LICENSE-OGL.txt), adattati e tradotti dall'*Old-School Essentials System Reference Document* © 2019 Gavin Norman.
- Le trappole segnate `"source": "srd35"` in `traps.json` sono Open Game Content con [Open Game License 1.0a](../LICENSE-OGL.txt), adattate dalle trappole di esempio del *System Reference Document 3.5* © 2000-2003 Wizards of the Coast, Inc. Le altre trappole, gli inneschi, i meccanismi e le varianti sono scritti per WyrmDelve, seguendo i principi di *Some Traps* di Arnold K. (Goblin Punch).
- Tutto il resto è scritto per WyrmDelve e ha la licenza [GPL 3.0](../LICENSE) come il programma.
