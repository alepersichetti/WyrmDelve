# Come nascono le trappole

*[English version](trap.en.md)*

Questo documento spiega come WyrmDelve sceglie, piazza e descrive le trappole di un dungeon, con esempi veri generati dal programma.

> Le trappole compaiono solo se all'inizio, a «Cosa vuoi generare?», segni anche le **trappole** (oppure `--contenuto trappole`, anche insieme ad altro: `--contenuto storia,trappole`). Come nasce la mappa su cui vengono messe è spiegato in [dungeon_map_generation.md](dungeon_map_generation.md).

## Indice

1. [L'idea: una trappola è un problema, non un tiro di dado](#1-lidea-una-trappola-è-un-problema-non-un-tiro-di-dado)
2. [Le famiglie e i tre gradi](#2-le-famiglie-e-i-tre-gradi)
3. [Il percorso, passo per passo](#3-il-percorso-passo-per-passo)
4. [Quante trappole e dove](#4-quante-trappole-e-dove)
5. [Chi le ha costruite](#5-chi-le-ha-costruite)
6. [Prima si impara, poi si rischia](#6-prima-si-impara-poi-si-rischia)
7. [Più si scende, più sono crudeli](#7-più-si-scende-più-sono-crudeli)
8. [Trappole già pronte e trappole montate](#8-trappole-già-pronte-e-trappole-montate)
9. [Sulla mappa e nella chiave](#9-sulla-mappa-e-nella-chiave)
10. [Un esempio completo](#10-un-esempio-completo)
11. [Aggiungere trappole](#11-aggiungere-trappole)

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

Tutte le trappole stanno in `data/traps.json`. Del post sono usati i principi, non il testo. Le trappole proprie di WyrmDelve, gli inneschi, i meccanismi e le varianti sono scritti per WyrmDelve; 34 trappole già pronte (segnate `"source": "srd35"`) sono adattate dalle trappole di esempio del *System Reference Document 3.5*, Open Game Content con licenza OGL 1.0a (vedi `LICENSE-OGL.txt`), le stesse su cui si basa il generatore di [donjon](https://donjon.bin.sh): stessi meccanismi (raffica di dardi, falce dal muro, colonna che crolla, stanza che schiaccia…), testo riscritto per il gioco old school, senza prove di abilità né numeri a parte i dadi.

---

## 2. Le famiglie e i tre gradi

Una **famiglia** è un meccanismo. Ogni famiglia ha fino a tre **gradi**:

| Grado | Cosa è |
|---|---|
| **0 — rotta o scoperta** | non fa danni: mostra come funziona il meccanismo |
| **1 — funzionante** | il meccanismo nascosto |
| **2 — crudele** | una variante che punisce chi crede di aver capito |

Le famiglie, con le trappole già pronte per grado e i meccanismi da cui se ne montano di nuove (capitolo 8):

| Famiglia | Già pronte (gradi 0 / 1 / 2) | Meccanismi (con versione rotta) | Esempi | Note |
|---|---|---|---|---|
| `pit` fosse | 1 / 3 / 3 | 3 (0) | fossa nascosta, fossa irta di punte, buca coperta di rami | |
| `block` blocchi | 1 / 3 / 4 | 2 (0) | lastra che cade, mattoni dal soffitto, masso che rotola | |
| `darts` dardi | 1 / 4 / 4 | 2 (2) | dardi avvelenati, ago avvelenato nella serratura, raffica di dardi | |
| `blade` lame | 1 / 2 / 3 | 3 (1) | lama a pendolo, falce dal muro, statua del boia, tronco chiodato | |
| `spear` lance | — | 1 (1) | lance dal muro | |
| `crush` muri e soffitti | — / 1 / 1 | 1 (1) | muro che schiaccia, stanza che schiaccia | |
| `net` reti | — / 2 / — | 1 (1) | rete dal soffitto, catena che fa inciampare | |
| `cage` gabbie | — | 1 (1) | gabbia che scende | |
| `gate` saracinesche | — / 1 / — | — | saracinesca che divide il gruppo | |
| `wire` fili | — / 1 / — | — | filo affilato nel corridoio | |
| `lever` leve | 1 / 1 / 1 | — | leva sotto la botola, tre leve | |
| `slide` scivoli | 1 / 1 / 1 | 1 (0) | pavimento che si inclina | solo se c'è un livello sotto in cui cadere |
| `gas` gas | 1 / 1 / 1 | 2 (0) | gas soporifero, gas velenoso, nebbia innocua | |
| `fire` fuoco | — / 1 / — | 2 (1) | getto di fuoco, vampata d'olio | |
| `acid` acido | — | 1 (1) | spruzzo d'acido | |
| `poison` veleni | — / 2 / 1 | — | maniglia avvelenata, scrigno con la muffa, punte avvelenate nei muri | |
| `rune` rune | 1 / 3 / 4 | 2 (1) | runa di fuoco, glifo che esplode, sigillo nel libro, specchio che imprigiona | solo in laboratorio arcano, accademia, tempio, torre, tomba |
| `flood` allagamenti | 1 / 1 / 1 | 1 (0) | stanza che si allaga | solo in Underdark, tomba, tempio, città, prigione, castello |
| `alarm` allarmi | — | 1 (0) | gong d'allarme | |
| `swarm` sciami | — | 1 (0) | vaso di insetti | rozza |
| `crude` rozze | — / 5 / — | — | campanelli d'allarme, tagliola, sacco sopra la porta, laccio, pavimento di cocci | le trappole degli abitanti di oggi |

In tutto: 21 famiglie, 65 trappole già pronte (31 di WyrmDelve, 34 dal System Reference Document 3.5), 25 meccanismi, 18 inneschi e 11 varianti, per **2.648 trappole diverse**.

---

## 3. Il percorso, passo per passo

Le trappole arrivano **dopo** che il dungeon è stato costruito, e usano dadi propri (ricavati dal seme con l'etichetta `traps`): la mappa, la storia e i mostri di un seme non cambiano se scegli o no le trappole.

1. **Distanze.** Il programma conta, per ogni stanza, quanti passi servono per arrivarci dall'esterno, attraverso corridoi, scale, pozzi, portali e ingressi. Un corridoio vale mezzo passo in più della più vicina delle sue due stanze.
2. **Posti possibili.** Su ogni livello: tutte le stanze, e i corridoi lunghi almeno 5 caselle che non hanno già qualcosa di speciale (acqua, crollo, gradini, passaggio segreto).
3. **Scelta dei posti.** Per ogni livello, il programma estrae alcuni posti, preferendo quelli importanti (capitolo 4).
4. **Scelta della trappola.** Per ogni posto, una trappola adatta: al costruttore (capitolo 5), al tipo del livello, al posto (stanza o corridoio) e al grado per quella profondità (capitolo 7). Due volte su cinque è una trappola già pronta, le altre volte una montata dai suoi pezzi (capitolo 8).
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
| I fondatori | `═║` | **accurato** (`built`) | meccanismi: fosse, blocchi, dardi, lame, lance, reti, gabbie, leve, scivoli, gas, fuoco, acido, rune, allagamenti, inneschi come lastre a pressione, porte, serrature e statuette |
| II seconda epoca | `─│` | **accurato** (`built`) | come sopra: chi venne dopo nascose i suoi passaggi |
| N grotte naturali, III oggi | `#` | **rozzo** (`crude`) | campanelli, tagliole, lacci, sacchi di sassi, cocci di vetro, buche coperte di rami, tronchi chiodati, vasi di insetti, olio e scintilla, inneschi come fili tesi, pietre smosse, esche e assi marce |

Così le trappole raccontano la storia del posto: nelle sale antiche ci sono meccanismi pensati da architetti, nelle tane degli abitanti di oggi ci sono trappole fatte con quello che c'era.

---

## 6. Prima si impara, poi si rischia

È il cuore dell'algoritmo. Per ogni famiglia di trappole funzionanti (gradi 1 e 2):

1. il programma trova la trappola funzionante **più vicina all'esterno**;
2. se c'è già una trappola di grado 0 della stessa famiglia **più vicina** ancora, va bene così;
3. altrimenti ne aggiunge una in un posto libero **prima**, cioè con meno passi dall'esterno, scegliendo il posto subito prima, per far vedere il meccanismo poco prima che serva;
4. se prima non c'è posto, prova alla stessa distanza;
5. se non c'è posto nemmeno lì (per esempio, la trappola è nella stanza dell'ingresso), quella trappola diventa essa stessa la versione rotta.

La versione rotta viene dalle trappole già pronte di grado 0 o dalla versione rotta (`broken`) di un meccanismo della stessa famiglia. Le famiglie senza nessuna versione rotta (per esempio le rozze, gli sciami, le saracinesche) non hanno lezione: sono semplici, e i loro segnali (fili tesi, vasi che ronzano, scanalature nei muri) si spiegano da soli.

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

Una trappola montata di grado 2 è un meccanismo con una **variante** crudele (capitolo 8). Se per quel posto non c'è una trappola di grado 2 adatta, si usa il grado 1.

---

## 8. Trappole già pronte e trappole montate

Le trappole già pronte sono poche e scritte a mano. Per averne migliaia, il programma ne **monta** di nuove da tre pezzi:

| Pezzo | Cosa dice | Quanti | Esempi |
|---|---|---|---|
| **innesco** (`triggers`) | cosa la fa scattare, e come lo si nota | 18 | lastra a pressione, filo teso, porta, coperchio di un forziere, statuetta sul piedistallo, gradino falso, luce, rumore, serratura, esca, asse marcia |
| **meccanismo** (`mechanisms`) | cosa succede, con il suo segnale e la sua versione rotta | 25 | dardi dalle pareti, botola, gabbia che scende, gas velenoso, spruzzo d'acido, glifo di gelo, gong d'allarme, tronco chiodato |
| **variante** (`twists`) | cosa la rende crudele (solo grado 2) | 11 | con veleno, che si riarma, con una gemella più avanti, che sigilla la stanza, con un'esca, dal segnale nascosto, con un mostro sul fondo |

I pezzi si combinano solo se stanno bene insieme: l'innesco e il meccanismo devono andare bene per lo stesso posto (stanza o corridoio) e lo stesso costruttore, il meccanismo deve essere adatto al tipo del livello (le rune solo nei luoghi magici, l'acqua solo dove ce n'è), e la variante deve andare bene per quel meccanismo (il veleno solo su dardi, lame, lance, fosse e fili; il mostro sul fondo solo su fosse e scivoli). Alcuni inneschi escludono qualche meccanismo: il coperchio di un forziere non apre uno scivolo.

Le parti della trappola nella chiave si compongono così:

| Parte | Come si compone | Esempio |
|---|---|---|
| **nome** | meccanismo + variante + (innesco) | Lance dal muro con un ago per chi la disinnesca (filo teso) |
| **segnale** | segnale del meccanismo; dell'innesco; della variante | buchi grandi come un pugno, in fila, con il bordo scheggiato; un filo sottile all'altezza della caviglia, che luccica alla luce |
| **effetto** | effetto del meccanismo, effetto della variante | lance scattano fuori dai buchi e trafiggono chi passa, e chi prova a disinnescarla a mano si punge su un ago avvelenato |
| **contromisure** | dell'innesco; del meccanismo; della variante | scavalcare il filo; tagliarlo tenendolo teso con una mano; passare chinati sotto la fila; incastrare le lance con dei cunei; disinnescarla con attrezzi lunghi, mai con le dita |

La **lezione** (grado 0) di una famiglia montata è la versione rotta del meccanismo: *lance spezzate*, *balestra arrugginita*, *gabbia arrugginita*. Il suo effetto e le sue contromisure sono uguali per tutte: il meccanismo è rotto, ma mostra com'è fatto.

Quante trappole diverse ci sono: 65 già pronte, 10 versioni rotte dei meccanismi e 2.573 combinazioni di innesco, meccanismo e variante (o nessuna variante) che stanno bene insieme. In tutto **2.648**.

---

## 9. Sulla mappa e nella chiave

- **Mappa dell'arbitro**: il simbolo `^` in grassetto sulla casella della trappola, e una voce `^ trappola (solo arbitro)` nella legenda.
- **Mappa dei giocatori**: niente, nemmeno nella legenda.
- **Chiave** (`.txt` e PDF): le trappole delle stanze sono scritte sotto la stanza; quelle dei corridoi sono elencate sotto il titolo del livello, in ordine di distanza dall'ingresso, così la lezione viene prima.
- **Durante la generazione** il programma scrive quante trappole ha messo: `7 trappole (^ solo sulla mappa dell'arbitro)`.

---

## 10. Un esempio completo

Seme `3-21-2-4-CDK-000F62`: torre (livello 1), castello (livello 2, con l'ingresso principale **A**), sottolivello 2a, Underdark (livello 3). Le trappole, in ordine di distanza dall'esterno:

| Passi | Dove | Epoca | Trappola | Grado |
|---|---|---|---|---|
| 1 | stanza 2-01 | I | lance spezzate | 0, la lezione |
| 1,5 | corridoio 2-01 – 2-03 | I | lance dal muro con un ago per chi la disinnesca (filo teso) | 2, montata |
| 3 | stanza 1-03 | I | balestra arrugginita | 0, la lezione |
| 3,5 | corridoio 1-03 – 1-05 | I | filo affilato nel corridoio | 1, SRD 3.5 |
| 3,5 | corridoio 2a-01 – 2a-02 | II | giavellotto dalla parete | 1, SRD 3.5 |
| 4 | stanza 3-03 | N | vaso di insetti (detriti) | rozza, montata |
| 4,5 | corridoio 3-03 – 3-06 | N | laccio | rozza |

Si vede tutto il percorso:

- le **lance spezzate** sono nella prima stanza dopo l'ingresso **A**: chi entra vede come sono fatti i buchi delle lance, e subito dopo, nel corridoio verso 2-03, trova le lance vere, già crudeli (il livello 2 ha il 30% di gradi 2);
- la **balestra arrugginita** sulla torre insegna la famiglia dei dardi: il **giavellotto dalla parete** del sottolivello, che è più lontano;
- il **filo affilato** non ha una lezione: la sua famiglia non ha versioni rotte, e il filo si nota da sé se la luce lo prende;
- nelle grotte, dove vivono gli abitanti di oggi, ci sono trappole rozze: un **vaso di insetti** nascosto tra i detriti e un **laccio**.

La mappa dell'arbitro del livello 2: un `^` nella stanza 2-01 e uno nel corridoio verso 2-03.

```
        [A]
        ║.║
        ║.║
  ╔═════╩+╩═╗
 ╔╝....>....╚╗                                ╔═════════╗
╔╝...........╚╗                              ╔╝....>....╚╗
║.............╠═════════════════════════════╦╝...........╚╗
║....2-01.^...$░░░░░░░░░░░░░░░░░░░░░░░░░░░░░$....2-02.....║
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
          ╔═══════╝.║              ║.............║
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

Nella chiave, sotto il titolo del livello, le trappole dei corridoi sono in ordine di distanza dall'ingresso; quelle delle stanze sono scritte sotto la stanza:

```
LIVELLO 2 — CASTELLO
  Trappole nei corridoi
    ^ tra 2-01 e 2-03: Lance dal muro con un ago per chi la disinnesca (filo teso). Segnale:
      buchi grandi come un pugno, in fila, con il bordo scheggiato; un filo sottile
      all'altezza della caviglia, che luccica alla luce. Effetto: lance scattano fuori dai
      buchi e trafiggono chi passa, e chi prova a disinnescarla a mano si punge su un ago
      avvelenato. Contromisure: scavalcare il filo; tagliarlo tenendolo teso con una mano;
      passare chinati sotto la fila; incastrare le lance con dei cunei; disinnescarla con
      attrezzi lunghi, mai con le dita.
  2-01 Trappola (^): Lance spezzate. Segnale: aste spezzate che spuntano dai buchi di un muro, con
  resti di stoffa. Effetto: nessuno: il meccanismo è rotto o scoperto, ma mostra com'è fatto.
  Contromisure: studiare il meccanismo: le trappole funzionanti dello stesso tipo danno lo stesso
  segnale.
```

---

## 11. Aggiungere trappole

Tutto sta in `data/traps.json`, un elemento per riga. Fai una copia del file prima di modificarlo.

### Una trappola già pronta (`traps`)

```json
{"family": "pit", "stage": 1, "places": ["room", "corridor"], "builders": "built", "where": ["*"], "name": {"it": "fossa nascosta", "en": "hidden pit"}, "tell": {"it": "le lastre del pavimento hanno fessure dritte e suonano vuote", "en": "the floor slabs have straight seams and sound hollow"}, "effect": {"it": "il pavimento si apre: una caduta profonda su un fondo di pietra", "en": "the floor opens: a deep fall onto a stone bottom"}, "counter": {"it": "sondare il pavimento con un'asta; saltarla; bloccare il coperchio con dei chiodi", "en": "probe the floor with a pole; jump it; nail the lid shut"}, "source": "wyrmdelve"},
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
| `source` | (facoltativo) da dove viene | `"wyrmdelve"`, `"srd35"` |

### Un innesco (`triggers`)

```json
{"builders": ["built"], "places": ["room", "corridor"], "name": {"it": "lastra a pressione", "en": "pressure plate"}, "tell": {"it": "una lastra appena più alta delle altre, con il bordo pulito", "en": "a slab a little higher than the rest, with a clean edge"}, "counter": {"it": "non calpestare la lastra; bloccarla con un cuneo", "en": "don't step on the slab; jam it with a chock"}},
```

`builders` e `places` sono elenchi; `avoid` (facoltativo) elenca le famiglie con cui l'innesco non ha senso, per esempio `["slide"]`. Nelle contromisure **nomina l'oggetto** («non calpestare la lastra»), non usare un pronome: dopo vengono le contromisure del meccanismo, e «non calpestarla» non si capirebbe più.

### Un meccanismo (`mechanisms`)

```json
{"family": "cage", "builders": ["built"], "places": ["room"], "where": ["*"], "name": {"it": "gabbia che scende", "en": "dropping cage"}, "tell": {"it": "quattro scanalature negli angoli…", "en": "four grooves in the corners…"}, "effect": {"it": "una gabbia di ferro cade…", "en": "an iron cage drops…"}, "counter": {"it": "restare vicino ai muri…", "en": "keep near the walls…"}, "broken": {"name": {"it": "gabbia arrugginita", "en": "rusted cage"}, "tell": {"it": "una gabbia caduta di traverso, bloccata a metà dalla ruggine", "en": "a cage fallen askew, stuck halfway by rust"}}},
```

I campi sono quelli delle trappole già pronte (senza `stage`: lo decide il programma), con `builders` come elenco. `broken` (facoltativo) è la sua versione rotta, la lezione: nome e segnale. Senza `broken`, la famiglia può avere una lezione solo da una trappola già pronta di grado 0.

### Una variante (`twists`)

```json
{"families": ["darts", "blade", "spear", "pit", "wire"], "places": ["room", "corridor"], "name": {"it": "con veleno", "en": "with poison"}, "effect": {"it": "e le ferite sono avvelenate (tiro salvezza contro veleno)", "en": "and the wounds are poisoned (save versus poison)"}, "counter": {"it": "non toccare le punte a mani nude", "en": "don't touch the points bare-handed"}, "tell": {"it": "un odore amaro, di mandorle", "en": "a bitter smell, of almonds"}},
```

`families` sono le famiglie a cui si può aggiungere (`["*"]` = tutte). `effect` e `tell` sono facoltativi; l'effetto si aggiunge dopo quello del meccanismo, quindi comincia con «e…», «poi…» o «ma…». Il **nome** si aggiunge dopo quello del meccanismo, che può essere maschile o femminile, singolare o plurale: scrivilo in modo che vada bene con tutti («con veleno», «che si riarma», non «avvelenata»).

### Consigli

- **Una famiglia nuova** funziona meglio con tutti e tre i gradi, o con un meccanismo con la sua versione rotta. Senza grado 0, la regola «prima si impara» non può essere rispettata per quella famiglia.
- **Il segnale** deve descrivere il **meccanismo** (cosa si vede), non il pericolo (cosa succede).
- **Le contromisure** devono essere cose che i giocatori possono fare con l'equipaggiamento di tutti i giorni: aste, corde, chiodi, cera, stracci, sassi da lanciare.
- **Il grado 0** deve far capire il grado 1: stesso meccanismo, ma scoperto, rotto o già scattato.
- Per le regole su virgole e virgolette nel file JSON, vedi il capitolo 9 di [add_monsters_to_bestiary.md](add_monsters_to_bestiary.md): valgono anche qui.
