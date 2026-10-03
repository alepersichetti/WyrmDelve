# Come nascono le trappole

Questo documento spiega come WyrmDelve sceglie, piazza e descrive le trappole di un dungeon, con esempi veri generati dal programma.

> Le trappole compaiono solo se all'inizio, a «Cosa vuoi generare?», scegli una risposta con le **trappole** (oppure `--contenuto trappole`, anche insieme ad altro: `--contenuto storia,trappole`). Come nasce la mappa su cui vengono messe è spiegato in [dungeon_map_generation.md](dungeon_map_generation.md).

## Indice

1. [L'idea: una trappola è un problema, non un tiro di dado](#1-lidea-una-trappola-è-un-problema-non-un-tiro-di-dado)
2. [Le famiglie e i tre gradi](#2-le-famiglie-e-i-tre-gradi)
3. [Il percorso, passo per passo](#3-il-percorso-passo-per-passo)
4. [Quante trappole e dove](#4-quante-trappole-e-dove)
5. [Chi le ha costruite](#5-chi-le-ha-costruite)
6. [Prima si impara, poi si rischia](#6-prima-si-impara-poi-si-rischia)
7. [Più si scende, più sono crudeli](#7-più-si-scende-più-sono-crudeli)
8. [Sulla mappa e nella chiave](#8-sulla-mappa-e-nella-chiave)
9. [Un esempio completo](#9-un-esempio-completo)
10. [Aggiungere trappole](#10-aggiungere-trappole)

---

## 1. L'idea: una trappola è un problema, non un tiro di dado

La logica segue i principi del post [*Some Traps*](https://goblinpunch.blogspot.com/2018/08/some-traps.html) di Goblin Punch (Arnold K.):

- **prima si impara**: prima di una trappola nascosta, i giocatori devono aver visto lo stesso meccanismo scoperto o rotto;
- **si annuncia il meccanismo, non il pericolo**: c'è sempre qualcosa da notare (fessure, fori, una leva troppo oliata), anche se non si sa cosa succederà;
- **si risolve ragionando**: con quello che vedono, i giocatori possono evitarla, disinnescarla o usarla a loro vantaggio, senza affidarsi a un tiro di dado.

Per questo ogni trappola, nella chiave, ha quattro parti:

| Parte | Cosa dice | Esempio (fossa nascosta) |
|---|---|---|
| **nome** | che cos'è | fossa nascosta |
| **segnale** | cosa si nota, se si guarda | le lastre del pavimento hanno fessure dritte e suonano vuote |
| **effetto** | cosa succede se scatta | il pavimento si apre: una caduta profonda su un fondo di pietra |
| **contromisure** | come la si batte ragionando | sondare il pavimento con un'asta; saltarla; bloccare il coperchio con dei chiodi |

Le trappole del file `wyrmdelve_tables.json` sono scritte per WyrmDelve: del post sono usati i principi, non il testo.

---

## 2. Le famiglie e i tre gradi

Una **famiglia** è un meccanismo. Ogni famiglia ha fino a tre **gradi**:

| Grado | Cosa è |
|---|---|
| **0 — rotta o scoperta** | non fa danni: mostra come funziona il meccanismo |
| **1 — funzionante** | il meccanismo nascosto |
| **2 — crudele** | una variante che punisce chi crede di aver capito |

Le famiglie del file:

| Famiglia | Grado 0 | Grado 1 | Grado 2 | Dove | Note |
|---|---|---|---|---|---|
| `pit` fosse | fossa scoperta | fossa nascosta | doppia fossa | stanze e corridoi | |
| `block` blocchi | blocco caduto | lastra che cade | soffitto che scende | stanze e corridoi (il soffitto solo nelle stanze) | |
| `darts` dardi | feritoie arrugginite | dardi avvelenati | corridoio dei dardi | stanze e corridoi | |
| `blade` lame | lama bloccata | lama a pendolo | corridoio delle falci | stanze e corridoi | |
| `lever` leve | leva spezzata | leva sotto la botola | tre leve | stanze | |
| `slide` scivoli | scivolo aperto | pavimento che si inclina | scivolo nel corridoio | stanze e corridoi | solo se c'è un livello sotto in cui cadere |
| `gas` gas | ugello rotto | gas soporifero | stanza sigillata | stanze | |
| `rune` rune | runa spenta | runa di fuoco | cerchio di glifi | stanze e corridoi | solo in laboratorio arcano, accademia, tempio, torre, tomba |
| `flood` allagamenti | stanza allagata a metà | stanza che si allaga | — | stanze | solo in Underdark, tomba, tempio, città, prigione, castello |
| `crude` rozze | — | campanelli d'allarme, tagliola, sacco sopra la porta, laccio, pavimento di cocci | — | stanze e corridoi | le trappole degli abitanti di oggi |

In tutto: 10 famiglie, 31 trappole.

---

## 3. Il percorso, passo per passo

Le trappole arrivano **dopo** che il dungeon è stato costruito, e usano dadi propri (ricavati dal seme con l'etichetta `traps`): la mappa, la storia e i mostri di un seme non cambiano se scegli o no le trappole.

1. **Distanze.** Il programma conta, per ogni stanza, quanti passi servono per arrivarci dall'esterno, attraverso corridoi, scale, pozzi, portali e ingressi. Un corridoio vale mezzo passo in più della più vicina delle sue due stanze.
2. **Posti possibili.** Su ogni livello: tutte le stanze, e i corridoi lunghi almeno 5 caselle che non hanno già qualcosa di speciale (acqua, crollo, gradini, passaggio segreto).
3. **Scelta dei posti.** Per ogni livello, il programma estrae alcuni posti, preferendo quelli importanti (capitolo 4).
4. **Scelta della trappola.** Per ogni posto, una trappola adatta: al costruttore (capitolo 5), al tipo del livello, al posto (stanza o corridoio) e al grado per quella profondità (capitolo 7).
5. **La lezione.** Per ogni famiglia usata, il programma controlla che i giocatori incontrino prima la versione rotta (capitolo 6), e se serve la aggiunge.
6. **La casella.** Ogni trappola riceve una casella precisa sulla mappa: in una stanza, una casella libera lontana dalle porte, dal numero della stanza e dagli altri simboli; in un corridoio, la casella centrale.

Ogni stanza e ogni corridoio ospita al massimo una trappola.

---

## 4. Quante trappole e dove

- **Quante**: circa una ogni 5 stanze per livello, e almeno una per livello (sottolivelli compresi), più le trappole rotte che insegnano.
- **Dove**: si protegge ciò che vale. Il programma estrae i posti con questi pesi:

| Posto | Peso |
|---|---|
| stanza **importante** (sala del trono, sepolcro, laboratorio, abside, mastio…) | 3 |
| corridoio che porta a una stanza importante | 2 |
| ogni altra stanza o corridoio | 1 |

Un posto con peso 3 ha tre volte più probabilità di essere scelto di uno con peso 1.

---

## 5. Chi le ha costruite

Il costruttore dipende dall'**epoca** del posto, la stessa che si vede dai muri:

| Epoca del posto | Muri | Costruttore | Trappole |
|---|---|---|---|
| I fondatori | `═║` | **accurato** (`built`) | meccanismi: fosse, blocchi, dardi, lame, leve, scivoli, gas, rune, allagamenti |
| II seconda epoca | `─│` | **accurato** (`built`) | come sopra: chi venne dopo nascose i suoi passaggi |
| N grotte naturali, III oggi | `#` | **rozzo** (`crude`) | campanelli, tagliole, lacci, sacchi di sassi, cocci di vetro |

Così le trappole raccontano la storia del posto: nelle sale antiche ci sono meccanismi pensati da architetti, nelle tane degli abitanti di oggi ci sono trappole fatte con quello che c'era.

---

## 6. Prima si impara, poi si rischia

È il cuore dell'algoritmo. Per ogni famiglia di trappole funzionanti (gradi 1 e 2):

1. il programma trova la trappola funzionante **più vicina all'esterno**;
2. se c'è già una trappola di grado 0 della stessa famiglia **più vicina** ancora, va bene così;
3. altrimenti ne aggiunge una in un posto libero **prima**, cioè con meno passi dall'esterno, scegliendo il posto subito prima, per far vedere il meccanismo poco prima che serva;
4. se prima non c'è posto, prova alla stessa distanza;
5. se non c'è posto nemmeno lì (per esempio, la trappola è nella stanza dell'ingresso), quella trappola diventa essa stessa la versione rotta.

Le trappole rozze non hanno grado 0: sono semplici, e i loro segnali (fili tesi, mucchi di stracci) si spiegano da soli.

Le distanze contano i passi lungo **tutto** il dungeon, non il livello: se l'ingresso principale è al livello 2, la lezione può stare al livello 2 e la trappola funzionante al livello 1, che si raggiunge salendo le scale.

---

## 7. Più si scende, più sono crudeli

Le trappole rozze sono sempre di grado 1. Per le altre, la probabilità del grado 2 cresce con la profondità del livello:

| Livello | Probabilità del grado 2 |
|---|---|
| 1 | 0% |
| 2 | 30% |
| sottolivello 2a | 45% |
| 3 | 60% |
| 4 e oltre | 80% |

Se per quel posto non c'è una trappola di grado 2 adatta (per esempio, gli allagamenti non hanno grado 2), si usa il grado 1.

---

## 8. Sulla mappa e nella chiave

- **Mappa del master**: il simbolo `^` in grassetto sulla casella della trappola, e una voce `^ trappola (solo master)` nella legenda.
- **Mappa dei giocatori**: niente, nemmeno nella legenda.
- **Chiave** (`.txt` e PDF): le trappole delle stanze sono scritte sotto la stanza; quelle dei corridoi sono elencate sotto il titolo del livello, in ordine di distanza dall'ingresso, così la lezione viene prima.
- **Durante la generazione** il programma scrive quante trappole ha messo: `7 trappole (^ solo sulla mappa del master)`.

---

## 9. Un esempio completo

Seme `3-21-2-4-CDK-000F62`: torre (livello 1), castello (livello 2, con l'ingresso principale **A**), sottolivello 2a, Underdark (livello 3). Le trappole, in ordine di distanza dall'esterno:

| Passi | Dove | Epoca | Trappola | Grado |
|---|---|---|---|---|
| 1,5 | corridoio 2-01 – 2-03 | I | fossa scoperta | 0, la lezione |
| 2 | stanza 3-02 | I | fossa nascosta | 1 |
| 2,5 | corridoio 2-03 – 2-05 | I | fossa nascosta | 1 |
| 2,5 | corridoio 3-07 – 3-08 | N | pavimento di cocci | rozza |
| 3,5 | corridoio 1-03 – 1-05 | I | fossa nascosta | 1 |
| 3,5 | corridoio 1-03 – 1-04 | I | lama bloccata | 0, la lezione |
| 4 | stanza 2a-02 | II | lama a pendolo | 1 |

Si vede tutto il percorso:

- la **fossa scoperta** è nel primo corridoio dopo l'ingresso **A**: chi entra impara subito che le fosse esistono e come si riconoscono;
- le **fosse nascoste** vengono dopo, su tre livelli diversi;
- la **lama bloccata** sulla torre insegna la lama a pendolo del sottolivello, che è più lontano;
- il **pavimento di cocci** è nelle grotte, dove vivono gli abitanti di oggi: una trappola rozza.

La mappa del master del livello 2: i due `^` sono nei corridoi.

```
        [A]
        ║.║
        ║.║
  ╔═════╩+╩═╗
 ╔╝....>....╚╗                                ╔═════════╗
╔╝...........╚╗                              ╔╝....>....╚╗
║.............╠═════════════════════════════╦╝...........╚╗
║....2-01.....$░░░░░░░░░░░░░░░░░░░░░░░░░░░░░$....2-02.....║
╚╗...........╔╩═════════════════════════════╣.............║
 ╚╗.........╔╝                              ╚╗...........╔╝
  ╚═══════╦.╩═══════╗                        ╚╗.........╔╝
          ║.....^...║             ╔═══════════╩══+╦═════╝
          ╚═══════╗.║             ║...............║
                  ║.║             ║.╔══════════╗≡╔╝
                  ║.║             ║.║          ║≡║
                 ╔╩+╩═════════════╩+╩╗         ║.║
                 ║...................║         ║.║
                 ║...................║         ║.║
                 ║...................║         ║.║
                 ║.......2-03........║         ║.║
                 ║.................<.║         ║.║
                 ║...................║         ║.║
                 ╚╦+╦══════════════╦+╣         ║.║
                  ║.║              ║.╚═════════╝.║
          ╔═══════╝.║              ║......^......║
          ║.........║              ╚═══════════╦+╩══════╗
    ╔═════╩+╦═══════╝                        ╔═╝........╚═╗
  ╔═╝.......╚═╗                             ╔╝...>........╚╗
  ║...........║                             ║..............║
  ║....2-04...║                             ║.....2-05.....║
  ║...........║                             ║..............║
  ║.......<...║                             ╚╗............╔╝
  ╚═╗.......╔═╝                              ╚═╗........╔═╝
    ╚═══════╝                                  ╚════════╝
```

Nella chiave, sotto il titolo del livello, le trappole dei corridoi sono in ordine di distanza dall'ingresso. La fossa scoperta, vicino all'ingresso **A**, insegna a riconoscere la fossa nascosta più avanti:

```
Trappole nei corridoi
  ^ tra 2-01 e 2-03: Fossa scoperta. Segnale: il coperchio di una fossa è crollato: si vede
    il fondo, pieno di ossa. Effetto: nessuno, se la si guarda: insegna che qui ci sono
    fosse nascoste. Contromisure: girarle intorno lungo il bordo.
  ^ tra 2-03 e 2-05: Fossa nascosta. Segnale: le lastre del pavimento hanno fessure dritte
    e suonano vuote. Effetto: il pavimento si apre: una caduta profonda su un fondo di
    pietra. Contromisure: sondare il pavimento con un'asta; saltarla; bloccare il coperchio
    con dei chiodi.
```

Le trappole nelle stanze sono scritte sotto la stanza:

```
3-02 Trappola (^): Fossa nascosta. Segnale: le lastre del pavimento hanno fessure dritte e
suonano vuote. Effetto: il pavimento si apre: una caduta profonda su un fondo di pietra.
Contromisure: sondare il pavimento con un'asta; saltarla; bloccare il coperchio con dei chiodi.
```

---

## 10. Aggiungere trappole

Le trappole stanno nella tabella `traps` di `wyrmdelve_tables.json`, una per riga. Per esempio:

```json
{"family": "pit", "stage": 1, "places": ["room", "corridor"], "builders": "built", "where": ["*"], "name": {"it": "fossa nascosta", "en": "hidden pit"}, "tell": {"it": "le lastre del pavimento hanno fessure dritte e suonano vuote", "en": "the floor slabs have straight seams and sound hollow"}, "effect": {"it": "il pavimento si apre: una caduta profonda su un fondo di pietra", "en": "the floor opens: a deep fall onto a stone bottom"}, "counter": {"it": "sondare il pavimento con un'asta; saltarla; bloccare il coperchio con dei chiodi", "en": "probe the floor with a pole; jump it; nail the lid shut"}},
```

| Campo | Cosa contiene | Valori |
|---|---|---|
| `family` | la famiglia | un nome qualunque: le trappole con lo stesso nome si insegnano a vicenda |
| `stage` | il grado | `0` rotta (insegna), `1` funzionante, `2` crudele |
| `places` | dove può stare | `["room"]`, `["corridor"]` o tutti e due |
| `builders` | chi la costruisce | `"built"` (fondatori e seconda epoca) o `"crude"` (abitanti di oggi) |
| `where` | in quali tipi di dungeon | `["*"]` ovunque, oppure per esempio `["tomb", "temple"]` |
| `needs` | (facoltativo) una condizione | `"below"`: solo se c'è un livello sotto |
| `name`, `tell`, `effect`, `counter` | nome, segnale, effetto, contromisure | in italiano (`it`) e in inglese (`en`) |

Consigli:

- **Una famiglia nuova** funziona meglio con tutti e tre i gradi. Senza grado 0, la regola «prima si impara» non può essere rispettata per quella famiglia.
- **Il segnale** deve descrivere il **meccanismo** (cosa si vede), non il pericolo (cosa succede).
- **Le contromisure** devono essere cose che i giocatori possono fare con l'equipaggiamento di tutti i giorni: aste, corde, chiodi, cera, stracci, sassi da lanciare.
- **Il grado 0** deve far capire il grado 1: stesso meccanismo, ma scoperto, rotto o già scattato.
- Per le regole su virgole e virgolette nel file JSON, vedi il capitolo 9 di [add_monsters_to_bestiary.md](add_monsters_to_bestiary.md): valgono anche qui.
