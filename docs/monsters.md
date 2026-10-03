# Come nascono i mostri

*[English version](monsters.en.md)*

Questo documento spiega come WyrmDelve popola un dungeon: le tabelle dei mostri erranti, i mostri nelle stanze, gli indizi nelle stanze vuote e i mostri fuori posto. Gli esempi sono generati dal programma.

> I mostri compaiono solo se all'inizio, a «Cosa vuoi generare?», scegli una risposta con i **mostri** (oppure `--contenuto mostri`, anche insieme ad altro). Per **aggiungere** mostri, indizi e motivi al file JSON c'è una guida a parte: [add_monsters_to_bestiary.md](add_monsters_to_bestiary.md).

## Indice

1. [In breve](#1-in-breve)
2. [Il pericolo cresce con la profondità](#2-il-pericolo-cresce-con-la-profondità)
3. [La tabella dei mostri erranti](#3-la-tabella-dei-mostri-erranti)
4. [Le stanze: mostri, indizi, stanze vuote](#4-le-stanze-mostri-indizi-stanze-vuote)
5. [I mostri fuori posto](#5-i-mostri-fuori-posto)
6. [Un esempio completo](#6-un-esempio-completo)
7. [Da dove vengono i mostri](#7-da-dove-vengono-i-mostri)

---

## 1. In breve

Con i mostri, la chiave del dungeon (`.txt` e PDF) ha:

- per ogni livello, sotto il titolo, una **tabella d6 di mostri erranti**;
- per ogni stanza, **cosa c'è dentro**: dei mostri, un indizio, oppure niente.

Tutto si decide **dopo** che il dungeon è stato costruito, con dadi propri (ricavati dal seme con l'etichetta `monsters`): la mappa e la storia di un seme non cambiano se scegli o no i mostri, e lo stesso seme dà sempre gli stessi mostri.

I mostri stanno nella tabella `monsters` di `wyrmdelve_tables.json` (245 mostri): ognuno dice dove può comparire (`where`), quanto è pericoloso (`danger`, da 1 a 4), che creatura è (`kind`) e quanti se ne incontrano (`number`).

---

## 2. Il pericolo cresce con la profondità

Ogni livello ha un **pericolo** da 1 a 4: il primo livello ha pericolo 1, e ogni livello più in basso aggiunge un punto, fino a 4. Con più di 4 livelli il pericolo cresce più piano, in modo da arrivare a 4 solo all'ultimo livello.

| Livelli del dungeon | Pericolo livello per livello |
|---|---|
| 1 | 1 |
| 3 | 1, 2, 3 |
| 4 | 1, 2, 3, 4 |
| 6 | 1, 2, 2, 3, 3, 4 |

Un sottolivello prende il pericolo della sua profondità, a metà tra i due livelli, arrotondato.

Per scegliere i mostri di un livello il programma cerca, in quest'ordine:

1. mostri adatti al **tipo** del livello con **lo stesso pericolo**;
2. se non bastano, quelli con un punto in più o in meno;
3. poi qualunque mostro adatto al tipo;
4. e solo alla fine qualunque mostro.

---

## 3. La tabella dei mostri erranti

Si tira un d6 quando i personaggi fanno rumore o perdono tempo.

- **1** sono sempre **gli abitanti di oggi** (lo strato III della storia), in giro per le sale: il dungeon è casa loro.
- **2–6** sono cinque mostri scelti come nel capitolo 2: ragni e melme nelle grotte, non morti nelle tombe, demoni e golem nel laboratorio arcano, ronde e tagliagole in città.
- **Niente doppioni**: finché ce ne sono di nuovi, un mostro già uscito su un livello non torna su un altro.
- Se il livello ha un **mostro fuori posto** (capitolo 5), prende il posto del 6, con un rimando alla sua stanza.

---

## 4. Le stanze: mostri, indizi, stanze vuote

Un buon dungeon non è pieno di mostri: le stanze vuote danno respiro, fanno salire la tensione e lasciano spazio all'esplorazione. Livello per livello:

1. **Circa un terzo delle stanze** ha dei mostri (il 35%, arrotondato, almeno una), e **almeno un terzo resta sempre vuoto**.
2. **Gli abitanti di oggi** vivono nelle stanze che hanno uno strato della terza epoca (`III:` nella descrizione): sono le loro tane, fino a metà delle stanze occupate.
3. Se c'è un **mostro fuori posto**, prende una stanza costruita (dei fondatori o della seconda epoca), se ce n'è una libera.
4. **Gli altri mostri** della tabella dei mostri erranti occupano le stanze rimaste: la tabella dice chi gira, le stanze dicono dove dorme.
5. Per **ogni stanza con mostri**, la stanza vuota più vicina (prima quelle collegate da un corridoio, poi quelle della stessa parte del livello, poi le più vicine) riceve un **indizio** del tipo giusto per quella creatura (`kind`): ossa rosicchiate per i non morti, scie viscide per le creature d'acqua, odore di zolfo per i demoni, segni di passaggio per gli abitanti di oggi. L'indizio dice da quale stanza viene.
6. Le altre stanze sono semplicemente **vuote**.

Accanto a ogni mostro c'è **quanti** se ne incontrano: di solito 2d6 per i mostri deboli, poi 1d6, 1d3 e infine 1 per i più pericolosi; niente numero per gli sciami.

Nella chiave:

| Testo | Significato |
|---|---|
| `Mostri: Orso (1d6).` | la tana di un mostro |
| `Mostri: i bugbear di … (2d6): è la loro tana.` | la tana degli abitanti di oggi |
| `Mostri: Aboleth (1). Fuori posto: …` | un mostro fuori posto, con il motivo |
| `Vuota. Indizio: orme fresche di zampe nella polvere (da 2-02).` | una stanza vuota con un indizio |
| `Vuota.` | una stanza vuota |

---

## 5. I mostri fuori posto

Un dungeon troppo ordinato è prevedibile. Per questo, **circa un livello su tre** (3 volte su 10) ospita un mostro che **non c'entra** con il tipo del livello, e la chiave dice perché è lì. Il motivo nasce da ciò che il dungeon ha davvero: un motivo vale solo se la sua condizione (`when` nella tabella `quirks`) è vera.

| `when` | Condizione | Motivo (esempio) | Mostro |
|---|---|---|---|
| `water` | un altro livello ha grotte naturali e acqua (di preferenza più in basso) | le grotte allagate del livello 3 arrivano fin sotto questa stanza, attraverso una vasca | una creatura d'acqua |
| `portal` | il dungeon ha un portale magico | il portale di 1-04 ogni tanto lascia passare qualcosa | qualunque |
| `below` | il livello sotto è di un altro tipo | dal livello 3 sale spesso qualcosa a caccia | uno adatto al livello sotto |
| `founders` | il livello ha stanze dei fondatori | i fondatori lasciarono qui un guardiano, e nessuno ha mai revocato l'ordine | un costrutto |
| `any` | sempre | un incantesimo andato storto ha aperto un varco; gli abitanti di oggi tengono qui in catene ciò che catturano; una battaglia recente; un tesoro nascosto; corridoi in cui è facile perdersi | secondo il motivo |

Il mostro fuori posto può essere un po' più pericoloso del livello (fino a due punti in più): è una sorpresa, e il master può decidere come usarla. È così che può comparire, per esempio, un **aboleth nella vasca di un castello**, risalito dalle grotte allagate del livello sotto.

Esempio (seme `4-42-4-2-F-003ADB`, una città di 4 livelli, livello 3):

```
  1a-01 Mostri: Serpente velenoso gigante (1d6). Fuori posto: in questi corridoi è facile perdersi,
  e non tutti trovano l'uscita.
```

---

## 6. Un esempio completo

Il livello 2 del seme `3-21-2-4-CDK-000F62` (un castello), con storia e mostri:

```
LIVELLO 2 — CASTELLO
  Mostri erranti (d6)
    1. I bugbear di Inchalville: gli abitanti di oggi, in giro per le sale.
    2. Orso: un orso affamato entrato dalle rovine.
    3. Pantera: un felino nero, a volte tenuto come animale da guardia.
    4. Mimic: sembra un forziere o una porta, finché non morde.
    5. Mutaforma: prende l'aspetto di chi ha davanti e si infiltra nel gruppo.
    6. Lupo mannaro: di giorno una persona come tante, di notte un lupo.
  2-01 [I] Torre della prigione; III: tana dei bugbear.
         Mostri: i bugbear di Inchalville (2d6): è la loro tana.
         uscite: → 2-03 (apertura); → 2-02 (passaggio segreto); > scale giù → 3-02; ingresso A
  2-02 [I] Torre d'angolo; II: sala dei ricordi.
         Mostri: Orso (1d6).
         uscite: → 2-03 (porta); → 2-01 (passaggio segreto); → 2-05 (porta, gradini); > scale giù →
         2a-01
  2-03 [I] Cortile delle scuderie.
         Vuota. Indizio: un mucchio di ossa e di oggetti rubati, il bottino di qualcuno (da 2-01).
         uscite: → 2-04 (porta); → 2-01 (porta); → 2-05 (porta); → 2-02 (porta); < scale su → 1-03
  2-04 [I] Torre del vessillo.
         Vuota.
         uscite: → 2-03 (porta); < scale su → 1-05
  2-05 [I] Torrione; II: cucina comune.
         Vuota. Indizio: orme fresche di zampe nella polvere (da 2-02).
         uscite: → 2-03 (porta); → 2-02 (porta, gradini); > scale giù → 3-03
```

- La tabella ha gli abitanti di oggi all'1 e cinque mostri da castello di pericolo 2 (o vicino).
- `2-01` è una stanza della terza epoca (*tana dei bugbear*): ci vivono gli abitanti di oggi.
- `2-02` è la tana dell'orso, il primo mostro della tabella.
- `2-03` e `2-05` sono vuote, ma con un indizio: ciascuna è collegata da un corridoio a una delle due tane.
- `2-04` è vuota e basta.

---

## 7. Da dove vengono i mostri

L'elenco è stato ricavato confrontando due bestiari, *OSR Bestiary* (bucolian) e il *Monstrous Bestiary* di *Aketon* (Reese Surles), ed eliminando i doppioni: per esempio il *Ruster* di Aketon è il mostro della ruggine, il *Gel Cube* è il cubo gelatinoso, il *Landshark* è la bulette. I due bestiari non hanno una licenza aperta, quindi da loro vengono solo i nomi delle creature e i Dadi Vita (usati per il pericolo): **tutte le descrizioni sono scritte per WyrmDelve**. L'aboleth viene dall'SRD 5.1 (CC BY 4.0). Sono stati tolti i mostri con nomi registrati da altri, i signori dei demoni con un nome proprio e gli animali che in un dungeon non hanno senso (balene, cavalli, dinosauri…). Le fonti complete sono nel README.
