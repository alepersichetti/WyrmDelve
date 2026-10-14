# Come nascono i tesori

*[English version](treasure.en.md)*

Questo documento spiega come WyrmDelve decide quali stanze hanno un tesoro, cosa contiene e dove è nascosto, con esempi veri generati dal programma.

> I tesori compaiono solo se all'inizio, a «Cosa vuoi generare?», segni anche i **tesori** (oppure `--contenuto tesori`, anche insieme ad altro: `--contenuto mostri,tesori`). Come nascono i mostri e le trappole che custodiscono i tesori è spiegato in [monsters.md](monsters.md) e [trap.md](trap.md).

## Indice

1. [L'idea: le regole di Old-School Essentials](#1-lidea-le-regole-di-old-school-essentials)
2. [Quali stanze hanno un tesoro](#2-quali-stanze-hanno-un-tesoro)
3. [Il tesoro dei mostri: i tipi dalla A alla V](#3-il-tesoro-dei-mostri-i-tipi-dalla-a-alla-v)
4. [Il tesoro incustodito: dipende dal livello](#4-il-tesoro-incustodito-dipende-dal-livello)
5. [Monete, gemme e gioielli](#5-monete-gemme-e-gioielli)
6. [Gli oggetti magici](#6-gli-oggetti-magici)
7. [Dove è nascosto](#7-dove-è-nascosto)
8. [Nella chiave](#8-nella-chiave)
9. [Un esempio completo](#9-un-esempio-completo)
10. [Cambiare le tabelle](#10-cambiare-le-tabelle)

---

## 1. L'idea: le regole di Old-School Essentials

WyrmDelve segue le regole per riempire le stanze di un dungeon di *Old-School Essentials* (capitolo *Designing a Dungeon* e capitolo *Treasure* del System Reference Document). Le tabelle stanno in `data/treasure.json`: sono **Open Game Content** con licenza OGL 1.0a (vedi `LICENSE-OGL.txt`), tradotte e lette dall'edizione Markdown [Old-School-Essentials-Markdown](https://github.com/Obsidian-TTRPG-Community/Old-School-Essentials-Markdown).

I tesori arrivano **per ultimi**, dopo mostri e trappole, e usano dadi propri (ricavati dal seme con l'etichetta `treasure`): la mappa, la storia, i mostri e le trappole di un seme non cambiano se scegli o no i tesori.

---

## 2. Quali stanze hanno un tesoro

Nelle regole, l'arbitro tira 1d6 per sapere cosa c'è in una stanza, e poi un altro d6 per sapere se c'è un tesoro:

| d6 | Contenuto | Tesoro |
|---|---|---|
| 1–2 | vuota | 1 su 6 |
| 3–4 | mostri | 3 su 6 |
| 5 | speciale | mai |
| 6 | trappola | 2 su 6 |

WyrmDelve non tira il primo dado: il contenuto di ogni stanza lo decidono già i mostri ([monsters.md](monsters.md)) e le trappole ([trap.md](trap.md)). Per ogni stanza, in ordine:

1. se ci abitano dei **mostri**, è una stanza con mostri;
2. altrimenti, se ha una **trappola**, è una stanza con trappola;
3. altrimenti è **vuota** (anche se c'è un indizio).

Poi tira il d6 del tesoro con la probabilità della tabella. Le stanze «speciali» non esistono in WyrmDelve, quindi non tolgono mai un tesoro.

Se non hai scelto i mostri o le trappole, quelle stanze non esistono: tutte le stanze contano come vuote (o con trappola), e i tesori sono più rari. Con un dungeon di 24 stanze e tutto il resto scelto ci sono, di solito, da 3 a 9 tesori (5 a metà strada).

---

## 3. Il tesoro dei mostri: i tipi dalla A alla V

In una stanza con mostri, il tesoro è quello del loro **tipo di tesoro**, una lettera scritta nel campo `treasure` di ogni mostro in `data/monsters.json`:

- per i mostri che hanno lo stesso nome in *Old-School Essentials* (orchi, ghoul, draghi…), la lettera è quella delle sue statistiche;
- per gli altri, una lettera scelta per analogia con un mostro simile;
- per chi non tiene niente (animali, melme, sciami), nessuna lettera: niente tesoro, anche se il dado dice sì;
- gli **abitanti di oggi** (le tane dello strato III) hanno sempre il tipo `D`.

Ogni tipo è un elenco di righe, ciascuna con la sua probabilità. Per esempio il tipo **C** (valore medio 1.000 mo):

| Probabilità | Cosa |
|---|---|
| 20% | 1d12 × 1.000 monete di rame |
| 30% | 1d4 × 1.000 monete d'argento |
| 10% | 1d4 × 1.000 monete d'elettro |
| 25% | 1d4 gemme |
| 25% | 1d4 gioielli |
| 10% | 2 oggetti magici qualsiasi |

| Tipi | Cosa sono | Valore medio |
|---|---|---|
| A–O | **tesori di tana**: la ricchezza di un mostro grande o di una comunità | da 25 mo (J) a 60.000 mo (H); N e O hanno solo oggetti magici |
| P–T | tesoro **individuale**, per ogni creatura | da 0,1 a 17 mo |
| U–V | tesoro **di gruppo**, portato tutto insieme | 160 e 330 mo |

WyrmDelve tira il tipo **una volta per stanza**, per tutto il gruppo, anche per U e V.

---

## 4. Il tesoro incustodito: dipende dal livello

Nelle stanze vuote o con trappola il tesoro dipende dal **livello del dungeon**: più si scende, più è ricco.

| Livello | Argento | Oro | Gemme | Gioielli | Oggetti magici |
|---|---|---|---|---|---|
| 1 | 1d6 × 100 | 50%: 1d6 × 10 | 5%: 1d6 | 2%: 1d6 | 2%: 1 qualsiasi |
| 2–3 | 1d12 × 100 | 50%: 1d6 × 100 | 10%: 1d6 | 5%: 1d6 | 8%: 1 qualsiasi |
| 4–5 | 1d6 × 1.000 | 1d6 × 200 | 20%: 1d6 | 10%: 1d6 | 10%: 1 qualsiasi |
| 6–7 | 1d6 × 2.000 | 1d6 × 500 | 30%: 1d6 | 15%: 1d6 | 15%: 1 qualsiasi |
| 8 e oltre | 1d6 × 5.000 | 1d6 × 1.000 | 40%: 1d12 | 20%: 1d12 | 20%: 1 qualsiasi |

Un **sottolivello** conta come il livello sotto di lui: il sottolivello 1a usa la riga del livello 2.

---

## 5. Monete, gemme e gioielli

**Le monete.** Cinque metalli, con il loro valore in monete d'oro:

| Moneta | Sigla | Valore |
|---|---|---|
| rame | mr | 1/100 mo |
| argento | ma | 1/10 mo |
| elettro | me | 1/2 mo |
| oro | mo | 1 mo |
| platino | mp | 5 mo |

**Le gemme.** Ogni gemma vale quanto dice un d20:

| d20 | Valore |
|---|---|
| 1–4 | 10 mo |
| 5–9 | 50 mo |
| 10–15 | 100 mo |
| 16–19 | 500 mo |
| 20 | 1.000 mo |

**I gioielli.** Ogni gioiello vale 3d6 × 100 mo.

Nella chiave, le gemme e i gioielli dello stesso valore sono raggruppati: `5 gemme (2×50 mo, 3×100 mo)` sono due gemme da 50 e tre da 100.

---

## 6. Gli oggetti magici

Prima si tira il **tipo** di oggetto, poi l'oggetto nella tabella di quel tipo. Le regole hanno due colonne: **B** (Basic) per i personaggi dal 1° al 3° livello, **X** (Expert) dal 4° in su. WyrmDelve usa il **livello del dungeon** al posto di quello dei personaggi: la colonna B fino al livello 3, la colonna X dal livello 4.

| B (d%) | X (d%) | Tipo |
|---|---|---|
| 01–10 | 01–10 | armature e scudi |
| 11–15 | 11–15 | oggetti vari (borse, stivali, mantelli…) |
| 16–40 | 16–35 | pozioni |
| 41–45 | 36–40 | anelli |
| 46–50 | 41–45 | verghe, bastoni e bacchette |
| 51–70 | 46–75 | pergamene e mappe del tesoro |
| 71–90 | 76–95 | spade |
| 91–100 | 96–100 | altre armi |

Nella colonna B ogni tabella si tira con un dado piccolo (per esempio 1d8 per le pozioni) e contiene solo gli oggetti più semplici; nella colonna X si tira d% su tutta la tabella. Le armature magiche hanno anche un tipo, con 1d8: 1–2 di cuoio, 3–6 di maglia, 7–8 a piastre (*Armatura di maglia +1*).

Alcuni tipi di tesoro chiedono oggetti precisi:

| Richiesta | Come si sceglie |
|---|---|
| qualsiasi | tabella dei tipi |
| pozione, pergamena | direttamente quella tabella |
| arma o armatura (tipo B) | tabella dei tipi, ritirando finché esce armatura, spada o arma |
| non un'arma (tipo F) | tabella dei tipi, ritirando spade e armi |

Gli oggetti magici non hanno un prezzo fisso: non entrano nel valore del tesoro.

---

## 7. Dove è nascosto

Ogni tesoro ha un nascondiglio, scritto per WyrmDelve:

- nelle **tane dei mostri**: «ammucchiato nella tana», «nascosto sotto il giaciglio», «in un forziere rubato», «sparso tra i rifiuti e le ossa», «custodito dal più forte del gruppo», «sepolto sotto il pavimento della tana»;
- nelle **altre stanze**: dodici nascondigli, come «sotto una lastra del pavimento che si solleva», «dentro una statua cava», «nel doppiofondo di un vecchio baule», «sul fondo di una pozza d'acqua torbida».

Se nella stanza c'è una **trappola funzionante**, la chiave aggiunge «La trappola della stanza lo protegge»: è la *trappola del tesoro* delle regole, che scatta quando qualcuno tocca il tesoro. Una trappola rotta (la lezione, vedi [trap.md](trap.md)) non protegge niente.

---

## 8. Nella chiave

Il tesoro è l'ultima riga della stanza, dopo i mostri e la trappola:

```
  1a-02 Vuota. Indizio: solchi profondi nel pavimento e un odore di bestia sconosciuta (da 1a-01).
         Trappola (^): Vampata d'olio (pavimento a contrappeso). …
         Tesoro (110 mo): 1.100 ma, Pugnale +1; dietro un mattone che si sfila. La trappola della
         stanza lo protegge.
```

- tra parentesi, il **valore** in monete d'oro di monete, gemme e gioielli (senza gli oggetti magici); se è meno di 1 mo, non c'è;
- poi le **monete**, dalla meno preziosa alla più preziosa, le **gemme**, i **gioielli** e gli **oggetti magici**;
- dopo il punto e virgola, il **nascondiglio**.

Durante la generazione il programma scrive quanti tesori ha messo: `Tesori: 5, per 9.300 mo in monete, gemme e gioielli; oggetti magici: 1`.

Nelle mappe i tesori non compaiono: stanno solo nella chiave.

---

## 9. Un esempio completo

Seme `2-14-2-1-C-02SFP3`: un castello di due livelli con il sottolivello 1a, con mostri, trappole e tesori. I tesori:

| Stanza | Contenuto | Probabilità | Tabella | Tesoro |
|---|---|---|---|---|
| 1-02 | vuota | 1 su 6 | livello 1 | 600 ma (60 mo), dentro una statua cava |
| 1-03 | gli abitanti di oggi, nella loro tana | 3 su 6 | tipo D | 5.000 mr, 6.000 mo, 5 gemme (6.450 mo), sotto il giaciglio |
| 1a-01 | un couatl fuori posto | 3 su 6 | tipo B | 6.000 mr, 1.000 me, 2.000 mo (2.560 mo), tra i rifiuti e le ossa |
| 1a-02 | trappola funzionante (e un indizio) | 2 su 6 | livello 2 (il sottolivello conta come il livello sotto) | 1.100 ma e un Pugnale +1 (110 mo), dietro un mattone; la trappola lo protegge |
| 2-03 | vuota, con un indizio | 1 su 6 | livello 2 | 1.200 ma (120 mo), in una cassetta appesa in una crepa del soffitto |

Si vede che:

- le tane hanno i tesori più ricchi: è lì che i mostri accumulano;
- le stanze vuote hanno poche monete d'argento, come dice la tabella dei primi livelli;
- la stanza 1-03 ha una trappola, ma è la lezione (rotta): il tesoro c'è perché ci sono i mostri, e la trappola non lo protegge;
- l'unico oggetto magico è un'arma semplice della colonna B, perché il dungeon è poco profondo.

---

## 10. Cambiare le tabelle

Tutto sta in `data/treasure.json`. Fai una copia del file prima di modificarlo.

| Voce | Cosa contiene |
|---|---|
| `room_chance` | le probabilità su 6 per stanza `empty`, `monster`, `special`, `trap` |
| `dwellers_type` | il tipo di tesoro degli abitanti di oggi (`"D"`) |
| `unguarded` | il tesoro incustodito: per ogni gruppo di livelli (`levels`: primo e ultimo) le sue righe |
| `types` | i tipi dalla A alla V: per ognuno il valore medio (`average`) e le righe |
| `coins`, `coin_value` | le sigle delle monete nelle due lingue e il loro valore in oro |
| `gems`, `jewellery` | il valore delle gemme (d20) e dei gioielli (dadi × moltiplicatore) |
| `magic_types`, `magic` | la tabella dei tipi (colonne `b` e `x`) e le tabelle degli oggetti, con il dado della colonna B (`basic_die`) |
| `armour_kinds` | il tipo delle armature magiche (d8) |
| `hiding` | i nascondigli: `lair` nelle tane, `loose` nelle altre stanze |

Una riga di un tipo di tesoro è così:

```json
{"chance": 25, "dice": "1d6", "times": 1000, "what": "cp"}
```

cioè: 25% di probabilità, 1d6 × 1.000 monete di rame. `what` può essere una moneta (`cp`, `sp`, `ep`, `gp`, `pp`), `gems`, `jewellery` oppure `magic`, che ha un elenco di oggetti:

```json
{"chance": 15, "what": "magic", "items": [{"count": 2, "kind": "any"}, {"count": 1, "kind": "potion"}]}
```

`kind` può essere `any`, `potion`, `scroll`, `weapon_armour` o `not_weapon`; al posto di `count` si può scrivere `dice` (per esempio `"2d4"`).

Per cambiare il tesoro di un mostro, cambia la lettera del suo campo `treasure` in `data/monsters.json` (vedi [add_monsters_to_bestiary.md](add_monsters_to_bestiary.md)).

Se `data/treasure.json` manca o ha un errore, il programma lo dice e genera il dungeon senza tesori.
