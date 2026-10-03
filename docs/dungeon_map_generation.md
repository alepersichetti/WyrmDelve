# Come nasce la mappa del dungeon

Questo documento spiega, passo per passo e con esempi veri, come WyrmDelve costruisce la mappa ASCII di un dungeon: dalle stanze ai corridoi, dalle scale agli ingressi, fino al foglio stampato. Non serve saper programmare: dove compare un nome tecnico, viene spiegato con parole semplici.

Tutte le mappe di questo documento sono state generate dal programma, non disegnate a mano. Puoi rigenerarle con i semi indicati.

> La storia del dungeon (chi lo costruì, chi lo abita, cosa c'è nelle stanze) ha un documento a parte: [story_generation_algorithm.md](story_generation_algorithm.md).

## Indice

1. [Il percorso in breve](#1-il-percorso-in-breve)
2. [Il seme: la ricetta del dungeon](#2-il-seme-la-ricetta-del-dungeon)
3. [I tipi di dungeon e come si impilano](#3-i-tipi-di-dungeon-e-come-si-impilano)
4. [Quante stanze per livello](#4-quante-stanze-per-livello)
5. [La griglia di slot](#5-la-griglia-di-slot)
6. [La pianta di ogni tipo](#6-la-pianta-di-ogni-tipo)
7. [Le epoche: gli strati del dungeon](#7-le-epoche-gli-strati-del-dungeon)
8. [La forma delle stanze](#8-la-forma-delle-stanze)
9. [I corridoi e gli anelli](#9-i-corridoi-e-gli-anelli)
10. [Scale, pozzi, portali e sottolivelli](#10-scale-pozzi-portali-e-sottolivelli)
11. [Gli ingressi](#11-gli-ingressi)
12. [Niente vicoli ciechi](#12-niente-vicoli-ciechi)
13. [Segreti e percorsi insoliti](#13-segreti-e-percorsi-insoliti)
14. [La verifica dei principi di Jaquays](#14-la-verifica-dei-principi-di-jaquays)
15. [Dalla griglia al disegno](#15-dalla-griglia-al-disegno)
16. [Dal disegno al foglio](#16-dal-disegno-al-foglio)
17. [Un esempio completo su più livelli](#17-un-esempio-completo-su-più-livelli)
18. [Cosa puoi cambiare nel file JSON](#18-cosa-puoi-cambiare-nel-file-json)

---

## 1. Il percorso in breve

Quando avvii il programma vedi una barra con 10 passaggi. Ognuno corrisponde a una fase di questo documento:

| Passaggio | Cosa succede | Capitolo |
|---|---|---|
| 1. Impostazioni | si legge (o si crea) il seme | 2 |
| 2. Storia a strati | si scelgono fondatori, epoche e abitanti | documento sulla storia |
| 3. Stanze e strati | si decide quante stanze, dove stanno, di che epoca sono e che forma hanno | 3–8 |
| 4. Corridoi e anelli | si collegano le stanze di ogni livello, con anelli | 9 |
| 5. Collegamenti tra livelli e ingressi | scale, pozzi, portali, ingressi; poi si eliminano i vicoli ciechi | 10–12 |
| 6. Passaggi segreti e insoliti | porte segrete, passaggi nascosti, acqua, crolli, gradini | 13 |
| 7. Verifica dei principi di Jaquays | si controlla che il dungeon rispetti le regole | 14 |
| 8. Formato di stampa | si sceglie la carta e la grandezza delle lettere | 16 |
| 9. Mappa del master | si disegna e si salva la mappa completa | 15 |
| 10. Mappa dei giocatori e chiave | si disegna la mappa senza segreti e si scrive la chiave | 15 |

Un'idea guida attraversa tutto il programma: il dungeon deve essere **"xanderizzato"**, cioè rispettare i principi che Justin Alexander ha raccolto nella serie *Xandering the Dungeon* studiando i dungeon di Jennell Jaquays. In parole semplici: **più strade per arrivare ovunque**, anelli invece di vicoli ciechi, più ingressi, più collegamenti tra i livelli, segreti e scorciatoie. Così i giocatori hanno sempre delle scelte da fare.

---

## 2. Il seme: la ricetta del dungeon

Ogni dungeon ha un **seme**, una specie di ricetta scritta in una riga. Con lo stesso seme il programma rifà sempre lo stesso identico dungeon, su qualunque computer.

Esempio: `3-21-2-4-CDK-000F62`

| Parte | Valore | Significato |
|---|---|---|
| `3` | livelli | 3 livelli principali |
| `21` | stanze | 21 stanze in tutto |
| `2` | ingressi | 2 ingressi dall'esterno |
| `4` | segreti | 4 tra porte segrete e passaggi segreti |
| `CDK` | tipi | livello 1 = **C** Torre, livello 2 = **D** Castello, livello 3 = **K** Underdark (una sola lettera = tutti i livelli dello stesso tipo) |
| `000F62` | codice | 6 simboli che fanno da "numero fortunato": decidono tutti i tiri di dado |

Il codice usa cifre e lettere, ma non `I`, `L`, `O` e `U`, che si confondono facilmente con `1`, `0` e `V`.

### Dadi separati

Dentro il programma i "tiri di dado" non vengono da un unico sacchetto: ce ne sono diversi, ognuno ricavato dal seme con un'etichetta diversa:

- uno per i **parametri** casuali (quanti livelli, stanze, ingressi, segreti);
- uno per i **tipi** di dungeon, quando non li scegli tu;
- uno per la **storia** e uno per il **racconto**;
- uno per la **mappa**.

Così, se cambi una frase della storia nel file JSON, la mappa dello stesso seme resta identica.

### Parametri casuali

Se scegli "dungeon tutto casuale", il programma tira i dadi così:

- **livelli**: da 1 a 6, con 2 e 3 più probabili (pesi 2, 4, 4, 3, 1, 1);
- **stanze**: da 5 a 10 per livello, più 0–3 in più;
- **ingressi**: da 1 a 4, con 2 il più probabile;
- **segreti**: da 1 a un quinto delle stanze.

I limiti sono: da 1 a 10 livelli, da 5 a 200 stanze (almeno 5 per livello), da 1 a 9 ingressi, da 0 a 60 segreti.

---

## 3. I tipi di dungeon e come si impilano

Ci sono 11 tipi di dungeon. Ognuno ha una lettera (quella del seme), una **pianta** tipica (capitolo 6) e una lista di tipi che possono stargli **sotto**.

| Lettera | Tipo | Sopra il suolo? | Cosa ci può stare sotto |
|---|---|---|---|
| A | Palazzo | sì | palazzo, prigione, tomba, tempio, laboratorio arcano, città, Underdark |
| B | Prigione | no | prigione, laboratorio arcano, tomba, Underdark |
| C | Torre | sì | qualunque tipo |
| D | Castello | sì | castello, prigione, tomba, tempio, laboratorio arcano, città, Underdark |
| E | Tempio | no | tempio, tomba, prigione, laboratorio arcano, città, Underdark |
| F | Città | no | città, tomba, prigione, tempio, laboratorio arcano, Underdark |
| G | Laboratorio arcano | no | laboratorio arcano, prigione, tomba, Underdark |
| H | Accademia | sì | accademia, tempio, laboratorio arcano, tomba, prigione, città, Underdark |
| I | Fortezza di confine | sì | fortezza, prigione, tomba, tempio, Underdark |
| J | Tomba | no | tomba, Underdark |
| K | Underdark | no | solo Underdark |

Esempi:

- `CDK` va bene: una torre sopra un castello, sotto il castello le grotte dell'Underdark.
- `JD` non va bene: sotto una tomba non può esserci un castello. Il programma lo dice con un messaggio d'errore.
- `K` con 4 livelli diventa `KKKK`: quattro livelli di Underdark.

### Quando i tipi li sceglie il programma

- 4 volte su 10 (e sempre con un solo livello) tutti i livelli sono dello **stesso tipo**.
- Altrimenti si parte da un tipo a caso e si scende: ogni livello, 4 volte su 10, è dello stesso tipo di quello sopra, altrimenti è uno dei tipi ammessi sotto.

### Il livello del suolo

Il **livello del suolo** è quello dove si trova l'ingresso principale. È il più basso tra i livelli costruiti sopra il suolo (palazzo, torre, castello, accademia, fortezza). Se non ce n'è nessuno, è il primo livello.

Esempio `CDK`: la torre (livello 1) e il castello (livello 2) sono sopra il suolo. Il più basso è il castello: l'ingresso principale **A** è al livello 2, e la torre è in alto, sopra il castello.

---

## 4. Quante stanze per livello

Le stanze si dividono tra i livelli in parti quasi uguali, poi con qualche piccolo scambio casuale, senza mai scendere sotto 5 stanze per livello.

### Il sottolivello

Se le stanze bastano (almeno 5 per livello più 3), 3 stanze vanno in un **sottolivello**: un piccolo nascondiglio a metà tra due livelli, chiamato per esempio `2a` (tra il 2 e il 3). Con un solo livello, il sottolivello sta sotto quel livello.

Esempio `3-21-…`: 3 livelli × 5 = 15, più 3 fa 18, e 21 è più di 18. Quindi 3 stanze vanno nel sottolivello `2a` e le altre 18 si dividono tra i 3 livelli: 6, 6 e 6, poi gli scambi casuali danno 5, 5 e 8.

### Il livello diviso

Alcuni livelli vengono **divisi in due metà** che non si toccano: per andare da una metà all'altra bisogna passare da un altro livello. È un'idea di Jaquays che costringe i giocatori a esplorare in verticale.

- Si può dividere solo un livello con almeno 6 stanze, e ogni metà deve averne almeno 3 (servono per fare un anello).
- Al massimo un livello ogni tre, e mai due livelli divisi uno sopra l'altro.

Sulla mappa, il titolo del livello lo dice: `LIVELLO 3 · UNDERDARK · diviso`.

---

## 5. La griglia di slot

Ogni livello è una **griglia di slot**, come una scacchiera. Ogni slot è un rettangolo di **24 × 11 lettere** e può ospitare al massimo una stanza.

Perché 24 × 11? Perché le lettere sono circa **due volte più alte che larghe**: 24 lettere in larghezza e 11 in altezza danno, sulla carta, un riquadro quasi quadrato.

```
  slot (0,0)              slot (1,0)              slot (2,0)
 ┌────────────────────────┬────────────────────────┬────────────────────────┐
 │  ┌──────────────────┐  │                        │                        │
 │  │ al massimo 20 × 7│  │      slot vuoto:       │                        │
 │  │ lettere di       │  │      ci passano        │                        │
 │  │ pavimento        │  │      i corridoi        │                        │
 │  └──────────────────┘  │                        │                        │
 └────────────────────────┴────────────────────────┴────────────────────────┘
```

- Dentro uno slot, la stanza lascia 2 lettere di margine su ogni lato: lo spazio per i muri e per far passare i corridoi. Il pavimento di una stanza in un solo slot è al massimo **20 × 7** lettere.
- Le stanze grandi (un cortile, una navata, una piazza) occupano **più slot**.
- Ci sono sempre degli **slot vuoti**: circa un terzo in più del numero di stanze, più uno. Lì passano i corridoi, e la mappa respira.

Esempio: 9 stanze → 9 + 4 + 1 = 14 slot → una griglia di 4 colonne × 4 righe (16 slot, 7 vuoti).

---

## 6. La pianta di ogni tipo

Ogni tipo di dungeon dispone le stanze sulla griglia a modo suo. Ecco come il programma sistema **9 stanze** per ogni tipo. Legenda degli schemi:

- `·` = slot vuoto;
- in MAIUSCOLO le stanze principali, che appartengono sempre ai fondatori (epoca I);
- `*` = stanza **gemella**: è l'immagine allo specchio di quella sull'altro lato dell'asse;
- le altre parole indicano la forma (`stanza` rettangolare, `rotonda`, `ottagono`, `piccola`, `ala`).

#### A Palazzo (palace) — 5 × 4 slot
```
    ·     |  stanza  |    ·     | stanza*  |    ·
    ·     | ottagono |  SALONE  |ottagono* |    ·
    ·     |  stanza  |  SALONE  | stanza*  |    ·
    ·     |  stanza  |    ·     | stanza*  |    ·
```
#### B Prigione (prison) — 6 × 2 slot
```
 guardie  |  cella   |  cella   |  cella   |  cella   |  cella
  cella   |  cella   |  cella   |    ·     |    ·     |    ·
```
#### C Torre (tower) — 4 × 3 slot
```
    ·     | rotonda  | rotonda  |    ·
 rotonda  | rotonda  |  NUCLEO  | rotonda
    ·     | rotonda  | rotonda  | rotonda
```
#### D Castello (castle) — 4 × 4 slot
```
 torretta |  stanza  |    ·     | torretta
    ·     | CORTILE  | CORTILE  |  stanza
  stanza  | CORTILE  | CORTILE  |    ·
 torretta |  MASTIO  |    ·     | torretta
```
#### E Tempio (temple) — 5 × 4 slot
```
    ·     | cappella |  abside  |cappella* |    ·
    ·     |    ·     |  NAVATA  |    ·     |    ·
    ·     |  stanza  |  NAVATA  | stanza*  |    ·
    ·     | cappella |  stanza  |cappella* |    ·
```
#### F Città (city) — 4 × 3 slot
```
  stanza  |  stanza  |  stanza  |  stanza
    ·     |  PIAZZA  |  PIAZZA  |    ·
  stanza  |  SALONE  |  stanza  |  stanza
```
#### G Laboratorio arcano (wizard) — 4 × 4 slot
```
    ·     |    ·     | ottagono |    ·
  stanza  | rotonda  |  stanza  |    ·
 rotonda  | CERCHIO  |   LAB.   |    ·
    ·     | ottagono |  stanza  |    ·
```
#### H Accademia (academy) — 4 × 4 slot
```
   ala    |   ala    |    ·     |   ala
 BIBLIOT. | CHIOSTRO | CHIOSTRO |   ala
    ·     | CHIOSTRO | CHIOSTRO |    ·
   ala    |    ·     |  SALONE  |   ala
```
#### I Fortezza di confine (fortress) — 7 × 2 slot
```
 bastione |  stanza  |    ·     |  MASTIO  |    ·     |  stanza  |  stanza
    ·     |  porta   |    ·     |  MASTIO  |  stanza  |  stanza  | bastione
```
#### J Tomba (tomb) — 3 × 5 slot
```
 nicchia  | anticam. | nicchia*
 nicchia  |  stanza  | nicchia*
    ·     |  stanza  |    ·
    ·     |  stanza  |    ·
    ·     | SEPOLCRO |    ·
```
#### K Underdark (underdark) — 4 × 4 slot
```
  stanza  |  stanza  |  GROTTA  |  GROTTA
  stanza  |    ·     |    ·     |  stanza
    ·     |  stanza  |    ·     |  stanza
  stanza  |    ·     |  stanza  |    ·
```

Cosa fa ogni pianta:

| Tipo | Pianta | Come funziona |
|---|---|---|
| Palazzo | simmetrica | Un asse nord-sud; il **salone** del trono al centro; le altre stanze in coppie gemelle a destra e a sinistra (a volte ottagonali); una stanza sull'asse può diventare un **cortile**. |
| Prigione | a blocchi | File di **celle** piccole, tutte uguali e allineate; le **guardie** alle estremità; con 12 stanze o più, una **fossa** rotonda al centro. |
| Torre | radiale | Un **nucleo** rotondo al centro e tutte le altre stanze rotonde, strette intorno. |
| Castello | ad anello | Un **cortile** grande al centro (anche su più slot), gli edifici tutt'intorno; **torrette** rotonde agli angoli e un **mastio** sul lato. |
| Tempio | simmetrica | La **navata** lunga sull'asse, l'**abside** rotonda in cima, le **cappelle** laterali in coppie gemelle. |
| Città | a isolati | Una **piazza** al centro (fino a 2 × 2 slot), un **salone** vicino, case sparse con le strade in mezzo. |
| Laboratorio arcano | radiale | Un **cerchio** di evocazione al centro, il **laboratorio** ottagonale accanto, stanze di forme diverse. |
| Accademia | ad anello | Un **chiostro** al centro, la **biblioteca** e il **salone** sul giro esterno, ali tutte uguali. |
| Fortezza di confine | in linea | Una lunga fila: **bastioni** rotondi alle estremità, il **mastio** al centro (alto quanto la fortezza), una **porta** in basso. |
| Tomba | processionale | Un asse: **anticamera** in cima, sale lungo il percorso, **sepolcro** in fondo; **nicchie** piccole in coppie gemelle ai lati. |
| Underdark | sparsa | Grotte sparse ovunque; con 8 stanze o più, una **grande caverna** su due slot. |

Se una pianta non riesce a stare nella griglia (per esempio con pochissime stanze), il programma ripiega sulla pianta sparsa, che va sempre bene.

---

## 7. Le epoche: gli strati del dungeon

Un buon dungeon ha una storia, e la storia si vede nei muri. Ogni stanza appartiene a una di quattro **epoche**:

| Epoca | Sigla | Chi | Muri sulla mappa |
|---|---|---|---|
| Naturale | **N** | grotte più antiche di ogni costruzione | `#` |
| Prima epoca | **I** | i fondatori | doppi `═ ║ ╔ ╗` |
| Seconda epoca | **II** | chi venne dopo e riadattò le sale | singoli `─ │ ┌ ┐` |
| Terza epoca | **III** | gli abitanti di oggi, che scavano alla buona | `#` |

### Quanto pesa ogni epoca

Ogni tipo ha i suoi pesi. Alcuni esempi:

| Tipo | N | I | II | III |
|---|---|---|---|---|
| Torre | 0% | 75% | 25% | 0% |
| Castello | 0% | 60% | 30% | 10% |
| Tomba | 5% | 70% | 15% | 10% |
| Underdark | 75% | 10% | 10% | 5% |

### Le epoche vanno a macchie

Le epoche non vengono tirate stanza per stanza, altrimenti la mappa sembrerebbe un vestito d'arlecchino. Il programma fa così:

1. sparge sulla griglia alcuni punti (circa uno ogni tre stanze), ognuno con un'epoca tirata con i pesi del tipo;
2. ogni stanza prende l'epoca del **punto più vicino**.

Così le stanze della stessa epoca stanno vicine, come le ali aggiunte a un edificio in tempi diversi.

### Le eccezioni

- Le stanze principali (il salone del trono, la navata, il cortile, il sepolcro…) sono **sempre dei fondatori**.
- Una stanza gemella ha sempre la stessa epoca della sua gemella.
- In ogni dungeon c'è almeno una stanza dei fondatori e ci sono **almeno due epoche diverse**.
- Le stanze di un sottolivello sono tutte della seconda epoca, oppure grotte naturali se il tipo ne ha.
- Un corridoio prende l'epoca della più **recente** delle due stanze che collega: chi venne dopo si collegò alle opere più antiche.

---

## 8. La forma delle stanze

Dentro il suo slot, ogni stanza prende una forma. Ecco le forme, disegnate dal programma:

**Rettangolare dei fondatori (I), con colonne**

```
╔════════════════╗
║................║
║...■..■..■..■...║
║................║
║......1-01......║
║................║
║...■..■..■..■...║
║................║
╚════════════════╝
```

**Rotonda (I)**

```
   ╔════════╗
 ╔═╝........╚═╗
╔╝............╚╗
║..............║
║.....1-01.....║
║..............║
╚╗............╔╝
 ╚═╗........╔═╝
   ╚════════╝
```

**Ottagonale (I)**

```
 ╔════════╗
╔╝........╚╗
║...1-01...║
║..........║
╚╗........╔╝
 ╚════════╝
```

**Rettangolare della seconda epoca (II)**

```
┌─────────┐
│.........│
│.........│
│...1-01..│
│.........│
└─────────┘
```

**Piccola, come una cella (II)**

```
┌─────┐
│.....│
│1-01.│
└─────┘
```

**Grotta naturale (N)**

```
   ########
 ###...##.####
##...........##
#....1-01.....#
#.............#
###..........##
  ###......###
    ########
```

**Grezza, della terza epoca (III)**

```
  #######
###.....##
#........#
#..1-01..#
##.......#
 ####...##
    #####
```

Come si decide la forma e la grandezza:

- Le **grotte naturali** (N) sono sempre ellissi dal bordo irregolare, ottenute sommando tre "onde" al contorno. Il programma tiene un solo pezzo unito, così non restano isole di pavimento.
- Le stanze della **terza epoca** (III), se dovevano essere rettangolari, diventano **grezze**: angoli smussati a caso e qualche rigonfiamento sui lati.
- Le **stanze principali** grandi (saloni, cortili, navate…) occupano dal 75% al 100% dello spazio disponibile.
- Le stanze dei **fondatori** sono larghe dal 40% al 100% dello slot: costruivano in grande.
- Le altre sono più piccole, fino a circa due terzi dello slot.
- Le stanze **rotonde** sono larghe il doppio di quanto sono alte, così sulla carta sembrano davvero tonde.
- Le celle (`piccola`) sono di 5–7 × 2–3 lettere e stanno tutte centrate, in fila come in un vero blocco di celle.
- Le **gemelle** sono la copia esatta, allo specchio, della loro stanza.

### Colonne e numeri

- I grandi saloni rettangolari dei fondatori, se sono larghi almeno 10 lettere e alti almeno 5, ricevono **due file di colonne** `■`, una ogni tre lettere, centrate in modo simmetrico.
- Ogni stanza riceve un **numero** nella forma `livello-numero` (`1-01`, `2a-03`), scritto al centro, in grassetto, solo sulla mappa del master. Le stanze sono numerate in ordine di lettura: da sinistra a destra, dall'alto in basso.

---

## 9. I corridoi e gli anelli

Seguiamo un esempio piccolo: una tomba di 6 stanze su un livello, seme `1-6-1-2-J-TMB001`. Dopo il passaggio 3 le stanze sono al loro posto, ma ancora isolate:

```
                 ╔══════════════════╗
                 ║..................║
                 ║..................║
                 ║.......1-01.......║
                 ║..................║
                 ╚══════════════════╝




                        ###########
                       ##.........###
########               #............#           ########
#......#               #....1-03...##           #......#
#.1-02.#               ##..........#            #.1-04.#
#......#                ##...#######            #......#
########                 #####                  ########






                   ╔═════════════════╗
                   ║.................║
                   ║..■..■..■..■..■..║
                   ║.......1-05......║
                   ║..■..■..■..■..■..║
                   ║.................║
                   ╚═════════════════╝


                   ╔═════════════════╗
                   ║.................║
                   ║..■..■..■..■..■..║
                   ║.................║
                   ║.......1-06......║
                   ║.................║
                   ║..■..■..■..■..■..║
                   ║.................║
                   ╚═════════════════╝
```

Si vedono già le regole dei capitoli precedenti: l'anticamera `1-01` in cima, il sepolcro `1-06` in fondo, le due nicchie `1-02` e `1-04` gemelle ai lati. La stanza `1-03` (forma grezza) e le due nicchie sono della terza epoca, con i muri `#`; le altre sono dei fondatori, con i muri doppi e le colonne.

### Primo passo: chi è vicino di chi

Il programma deve decidere quali coppie di stanze sono "vicine". Usa una regola geometrica chiamata **grafo di Gabriel**:

> Due stanze sono vicine se, disegnando un cerchio che le ha entrambe sul bordo, una di fronte all'altra, **dentro il cerchio non c'è nessun'altra stanza**.

```
   A . . . . . . . . . B        A e B non sono vicine:
         .  C  .                C sta dentro il cerchio tra loro.
                                A–C e C–B invece sono vicine.
```

Questa regola dà coppie di stanze davvero vicine e corridoi che non tagliano attraverso altre stanze. Le distanze si misurano tenendo conto che le lettere sono alte il doppio di quanto sono larghe.

### Secondo passo: l'albero

Il programma mette in fila le coppie di vicini dalla più corta alla più lunga e le prende una per una, **scartando quelle che collegano stanze già raggiungibili**. Il risultato è un **albero**: tutte le stanze sono collegate, con il minimo di corridoi e senza giri.

Nell'esempio: `1-06–1-05`, `1-01–1-03`, `1-03–1-04`, `1-03–1-05`, `1-03–1-02`. Cinque corridoi per sei stanze.

### Terzo passo: gli anelli

Un albero ha un difetto: c'è una sola strada per andare da una stanza all'altra. Per questo il programma aggiunge degli **anelli**, cioè corridoi che chiudono un giro.

- Il numero di anelli è una percentuale delle stanze, diversa per tipo: 25% per la tomba, 50% per la città, 30–40% per gli altri. Nell'esempio: 6 × 25% = 1,5, arrotondato a **2 anelli**.
- Gli anelli si scelgono a caso tra le coppie di vicine rimaste fuori dall'albero, preferendo le più corte.
- **Ogni parte di ogni livello ha almeno un anello**: anche un sottolivello di 3 stanze, anche ciascuna metà di un livello diviso. Se il corridoio scelto non si riesce a scavare, il programma prova con altre coppie finché ci riesce.

Nell'esempio gli anelli sono `1-05–1-02` e `1-01–1-02`:

```
                 ╔══════════════════╗
                 ║..................║
                 ║..................║
                 ║.......1-01.......║
                 ║..................║
                 ╚═╦+╦══════╦+╦═════╝
                   ║.║      ║.║
                   #.#      #.#
                   #.#    ###.#
                   #.#    #...#
                   #.#  ###.#######
                   #.####.........#####
####################.#................##################
#......................#....1-03...##..................#
#.1-02.##############.###..........##############.1-04.#
#......#            #.# ##...#######            #......#
########            #.#  ###.#                  ########
                    #.#    #.#
                    #.#    #.#
                    #.#    #.#
                    #.#    #.#
                    #.#    #.#
                    ║.║    ║.║
                   ╔╩+╩════╩.╩═══════╗
                   ║.................║
                   ║..■..■..■..■..■..║
                   ║.......1-05......║
                   ║..■..■..■..■..■..║
                   ║.................║
                   ╚═════╦═════+╦════╝
                         ║......║
                         ║.╔════╝
                   ╔═════╩.╩═════════╗
                   ║.................║
                   ║..■..■..■..■..■..║
                   ║.................║
                   ║.......1-06......║
                   ║.................║
                   ║..■..■..■..■..■..║
                   ║.................║
                   ╚═════════════════╝
```

### Le porte

Ogni corridoio parte da una porta e arriva a una porta.

- La porta si mette sul muro rivolto verso l'altra stanza. Se la stanza ha già una porta da quella parte, il programma la riusa.
- Nelle stanze costruite (epoche I e II) le porte stanno **nel mezzo di un muro dritto**, mai in un angolo.
- Due porte della stessa stanza non stanno mai una accanto all'altra.
- Nelle stanze costruite, 3 porte su 4 sono vere porte `+`; le altre, e tutte quelle delle grotte, sono semplici aperture `.`.

### Lo scavo: il percorso più economico

Per scavare il corridoio tra due porte, il programma cerca il percorso più "economico" con un metodo chiamato **A\*** ("A stella"), quello che usano anche i navigatori stradali. Ogni passo ha un costo:

| Passo | Costo | Effetto |
|---|---|---|
| nella roccia | 1 | |
| lungo un corridoio già scavato | 0,6 | i corridoi si uniscono e si riusano, come strade |
| nella roccia ma **accanto** a un corridoio | +1,5 | niente corridoi paralleli appiccicati |
| ogni curva | +0,5 | corridoi dritti, con poche curve |

I corridoi non attraversano mai le stanze né i loro muri, e in un livello diviso restano nella loro metà.

---

## 10. Scale, pozzi, portali e sottolivelli

Dopo i corridoi, il programma collega i livelli tra loro. Le regole vengono dai principi di Jaquays:

### Scale tra livelli vicini

- Tra due livelli uno sopra l'altro ci sono **almeno 2 scale**; se entrambi hanno almeno 8 stanze, 6 volte su 10 sono **3**.
- Ogni scala usa **stanze diverse**: le due scale tra il livello 1 e il 2 non partono dalla stessa stanza e non arrivano nella stessa.
- Il programma sceglie ogni volta la stanza **meno usata**, così i collegamenti si spargono per tutto il livello.
- Se un livello è diviso, ognuna delle due metà ha almeno una scala.
- Sulla mappa: `>` scende, `<` sale.

### Pozzi che saltano i livelli

Con 3 o più livelli c'è un **pozzo** o camino `○` che salta un livello (per esempio dal 1 al 3); 3 volte su 10, se ci sono abbastanza livelli, ne salta due (dal 1 al 4). Con 6 livelli o più i pozzi sono due. I giocatori possono così "saltare" una parte del dungeon, oppure caderci dentro.

### Il sottolivello

Il sottolivello è collegato con una **scala** dal livello sopra alla sua prima stanza, e con un **pozzo** dalla sua ultima stanza al livello sotto. Si può attraversare, come una scorciatoia nascosta.

### Il portale magico

A volte c'è un **portale** `Ω` che unisce due punti lontani: due livelli distanti almeno due piani (con almeno tre livelli), oppure due stanze lontane dello stesso livello (con un livello solo).

- La probabilità dipende dal tipo: 100% nel laboratorio arcano, 70% nella torre, 20–60% negli altri. Vale la più alta tra i tipi dei livelli del dungeon.
- Il portale compare solo con almeno 15 stanze (8 per il laboratorio arcano).

### Mai due volte la stessa coppia

Due stanze collegate da una scala non vengono collegate anche da un pozzo o da un portale: ogni collegamento porta in un posto nuovo.

Esempio dal seme `3-21-2-4-CDK-000F62` (capitolo 17):

```
  1-03   ↔ 2-03   scale
  1-05   ↔ 2-04   scale            ← due scale tra 1 e 2, stanze diverse
  2-05   ↔ 3-03   scale
  2-01   ↔ 3-02   scale            ← due scale tra 2 e 3, una per metà del livello diviso
  1-02   ↔ 3-08   pozzo/camino     ← salta il livello 2
  2-02   ↔ 2a-01  scale            ← si entra nel sottolivello
  2a-03  ↔ 3-01   pozzo/camino     ← si esce dal sottolivello
  1-04   ↔ 3-07   portale magico   ← dalla torre alle grotte
```

---

## 11. Gli ingressi

Gli ingressi sono lettere: **A**, **B**, **C**… (la `I` viene saltata, per non confonderla con l'1).

- **A**, l'ingresso principale, è sempre al **livello del suolo** (capitolo 3).
- **B**, se ci sono almeno due livelli, è un **ingresso a metà dungeon**: su un livello sotterraneo intermedio (o su uno sopra il suolo, se sotto non c'è niente). Così i giocatori possono entrare "dal mezzo", un altro principio di Jaquays.
- Gli altri ingressi vanno 6 volte su 10 al livello del suolo, altrimenti su un livello a caso.

### Come si scava un ingresso

Il programma cerca una stanza vicina al **bordo** della mappa e scava un **corridoio dritto** da una porta della stanza fino al bordo. Sulla mappa, fuori dal bordo, compare l'etichetta `[A]` in bianco su nero.

- Gli ingressi stanno lontani tra loro: almeno 6 lettere (2 se non c'è altro modo).
- Ogni ingresso usa una stanza diversa.
- Il corridoio di un ingresso che parte da una grotta è della terza epoca: l'hanno aperto gli abitanti di oggi.

Se tutti i bordi sono occupati, l'ingresso diventa un **pozzo dalla superficie** che cade dritto in una stanza: il pozzo `○` con accanto la lettera dell'ingresso.

```
            [A]
            ║.║                ← ingresso A: corridoio dritto dal bordo
            ║.║                  fino alla porta della stanza 2-01
      ╔═════╩+╩═╗
     ╔╝....>....╚╗
```

---

## 12. Niente vicoli ciechi

Uno dei principi più importanti: **nessuna stanza deve avere una sola via d'uscita**. Un vicolo cieco costringe i giocatori a tornare indietro e toglie scelte.

Dopo scale e ingressi, il programma conta per ogni stanza da quanti posti ci si arriva: corridoi, scale, pozzi, portali e ingressi contano tutti. Se una stanza ne ha uno solo, il programma scava un corridoio verso la stanza più vicina della stessa parte del livello che non le è già collegata.

Nell'esempio della tomba, la nicchia `1-04` era collegata solo a `1-03`. Il programma ha aggiunto il corridoio da `1-04` a `1-05` (a destra, in basso). Il sepolcro `1-06` invece ora ha due vie: il corridoio verso `1-05` e l'ingresso **A**.

```
                 ╔══════════════════╗
                 ║..................║
                 ║..................║
                 ║.......1-01.......║
                 ║..................║
                 ╚═╦+╦══════╦+╦═════╝
                   ║.║      ║.║
                   #.#      #.#
                   #.#    ###.#
                   #.#    #...#
                   #.#  ###.#######
                   #.####.........#####
####################.#................##################
#......................#....1-03...##..................#
#.1-02.##############.###..........##############.1-04.#
#......#            #.# ##...#######            #......#
########            #.#  ###.#                  ##.#####
                    #.#    #.#                   #.#
                    #.#    #.#                   #.#
                    #.#    #.#                   #.#
                    #.#    #.#                   #.#
                    #.#    #.#    ################.#
                    ║.║    ║.║    ║................#
                   ╔╩+╩════╩.╩════╩.═╦##############
                   ║.................║
                   ║..■..■..■..■..■..║
                   ║.......1-05......║
                   ║..■..■..■..■..■..║
                   ║.................║
                   ╚═════╦═════+╦════╝
                         ║......║
                         ║.╔════╝
                   ╔═════╩.╩═════════╗
                   ║.................║
                   ║..■..■..■..■..■..║
                   ║.................║
                   ║.......1-06......║
                   ║.................║
                   ║..■..■..■..■..■..║
                   ║.................║
                   ╚═══════╦+╦═══════╝
                           ║.║
                           ║.║
                           [A]
```

### Il controllo finale

Alla fine il programma verifica che **ogni stanza sia raggiungibile dall'esterno**. Se il metodo A\* non è riuscito a scavare un corridoio (succede, in un angolo affollato), il programma ripara: collega la stanza isolata alla stanza raggiungibile più vicina, o con una scala a un livello vicino.

Se nemmeno così funziona, il programma ricomincia da capo con dadi nuovi (fino a 8 tentativi). Lo stesso seme fa sempre gli stessi tentativi, quindi il risultato resta sempre uguale.

---

## 13. Segreti e percorsi insoliti

Il quarto numero del seme dice quanti **segreti** vuoi. Il programma li distribuisce così:

1. **Un terzo** diventano **passaggi segreti**: un intero corridoio nascosto, disegnato con `░` sulla mappa del master, con una porta segreta `$` a ciascuna estremità. Si sceglie solo un corridoio che non è condiviso con altri, lungo almeno 3 lettere, con porte usate solo da lui.
2. Gli altri diventano **porte segrete** `$` su corridoi visibili, **prima sugli anelli**: così un segreto è sempre una scorciatoia o una via in più, mai l'unica strada.
3. Se chiedi più segreti dei corridoi disponibili, il programma rende segreta anche l'altra porta di un corridoio, poi **nasconde scale e pozzi** (i portali per ultimi). Se ancora non basta, avvisa con un messaggio.

Poi aggiunge i **percorsi insoliti**, sempre sui corridoi visibili e di preferenza sugli anelli:

| Cosa | Simbolo | Quanti |
|---|---|---|
| corridoio **allagato** | `≈≈≈` | 1 (2 con almeno 40 stanze) |
| **crollo** da scavalcare | `∴` | 1 (2 con almeno 30 stanze) |
| **gradini** nello stesso livello | `≡≡` | 1 per livello (2 con almeno 8 stanze) |
| **pozze d'acqua** nelle grotte | `≈` | in circa 4 grotte su 10 |

I gradini sono un piccolo **dislivello**: il livello non è tutto piatto. Se non c'è un tratto dritto per due gradini, ne basta uno; se non c'è nemmeno quello, diventa una pedana in una stanza.

La tomba, alla fine, sulla mappa del master:

```
                 ╔══════════════════╗
                 ║..................║
                 ║..................║
                 ║.......1-01.......║
                 ║..................║
                 ╚═╦$╦══════╦+╦═════╝
                   ║.║      ║.║
                   #.#      #.#
                   #≈#    ###.#
                   #≈#    #...#
                   #≈#  ###.#######
                   #.####.........#####
####################.#................##################
#......................#....1-03...##..................#
#.1-02.##############.###..........##############.1-04.#
#......#            #.# ##...#######            #......#
########            #.#  ###.#                  ##$#####
                    #.#    #≡#                   #░#
                    #∴#    #≡#                   #░#
                    #.#    #.#                   #░#
                    #.#    #.#                   #░#
                    #.#    #.#    ################░#
                    ║.║    ║.║    ║░░░░░░░░░░░░░░░░#
                   ╔╩+╩════╩.╩════╩$═╦##############
                   ║.................║
                   ║..■..■..■..■..■..║
                   ║.......1-05......║
                   ║..■..■..■..■..■..║
                   ║.................║
                   ╚═════╦═════+╦════╝
                         ║......║
                         ║.╔════╝
                   ╔═════╩.╩═════════╗
                   ║.................║
                   ║..■..■..■..■..■..║
                   ║.................║
                   ║.......1-06......║
                   ║.................║
                   ║..■..■..■..■..■..║
                   ║.................║
                   ╚═══════╦+╦═══════╝
                           ║.║
                           ║.║
                           [A]
```

Si vedono: il passaggio segreto `░` tra `1-04` e `1-05` con le due `$`, la porta segreta `$` sotto `1-01`, l'acqua `≈`, il crollo `∴` e i gradini `≡`.

---

## 14. La verifica dei principi di Jaquays

Prima di disegnare, il programma controlla il dungeon e scrive il risultato nella chiave (e lo mostra mentre lavora). Per la tomba:

```
~ Ingressi multipli: uno solo, come richiesto (gli anelli e i livelli compensano)
✓ Anelli (numero ciclomatico del dungeon): 3; su ogni livello: 1: 3
– Collegamenti multipli tra livelli: non applicabile (un solo livello)
– Collegamenti discontinui: non applicabile (un solo livello)
✓ Percorsi segreti e insoliti: 1 porte segrete, 1 passaggi segreti, 0 scale/pozzi nascosti, 1 allagati, 1 crolli, 0 portali
– Sottolivelli: non applicabile (troppe poche stanze per livello)
– Livelli divisi: non applicabile (un solo livello)
✓ Dislivelli interni (gradini nello stesso livello): 1
– Ingresso a metà dungeon: non applicabile (un solo livello)
✓ Dungeon annidati: opera dei fondatori e ampliamenti successivi collegati in 5 punti
```

`✓` = fatto, `~` = fatto in parte (per una tua scelta), `–` = non applicabile, con il motivo.

**Il numero ciclomatico**, detto semplice, è il numero di anelli indipendenti: quanti collegamenti (corridoi, scale, pozzi, portali, ingressi) ci sono in più rispetto al minimo indispensabile per tenere tutto unito. Nella tomba ci sono 8 corridoi e 1 ingresso, cioè 9 collegamenti, tra 7 punti (6 stanze più "l'esterno"): 9 − 7 + 1 = **3**. Sono i 2 anelli del capitolo 9 più quello aggiunto contro i vicoli ciechi. Più il numero è alto, più strade diverse ci sono.

I **dungeon annidati** sono parti di epoche o tipi diversi che si incontrano: grotte naturali collegate al complesso costruito, oppure livelli di tipo diverso uniti da scale, oppure (come qui) le stanze dei fondatori collegate a quelle scavate dopo.

---

## 15. Dalla griglia al disegno

Fino a qui il dungeon è una griglia di numeri: roccia, pavimento di stanza, corridoio, porta. Ora diventa un disegno.

### I muri si disegnano da soli

Il programma non disegna i muri uno per uno: **ogni casella di roccia che tocca il pavimento** (anche in diagonale) diventa muro. Poi decide che aspetto dargli:

1. guarda le stanze lì accanto: se una è dei fondatori il muro è doppio, se è della seconda epoca è singolo;
2. altrimenti guarda i corridoi lì accanto;
3. se non ci sono muri costruiti (grotte, terza epoca), il muro è `#`.

Per i muri doppi e singoli sceglie il pezzo giusto (`═`, `║`, `╔`, `╩`, `╬`…) guardando con quali muri vicini si collega a nord, est, sud e ovest, come in un gioco di tessere.

```
╔═════════╗    ┌─────────┐    ##########
║.........║    │.........│    #........##
║..1-01...║    │..1-02...│    #..1-03...#
║.........║    │.........│    ##.......##
╚═════════╝    └─────────┘     #########
fondatori (I)  seconda (II)   grotta o terza epoca (N, III)
```

### I simboli

| Simbolo | Significato | Simbolo | Significato |
|---|---|---|---|
| `.` | pavimento, apertura | `+` | porta |
| `$` | porta segreta (solo master) | `░` | passaggio segreto (solo master) |
| `<` `>` | scale su / giù | `≡` | gradini |
| `○` | pozzo o camino | `Ω` | portale magico |
| `≈` | acqua | `∴` | crollo |
| `■` | colonna | `[A]` | ingresso |

Con l'opzione `--solo-ascii` (o se il font non ha un simbolo) si usano solo caratteri della tastiera: `#` per tutti i muri, `o` pozzo, `&` portale, `~` acqua, `%` crollo, `=` gradini, `O` colonna, `:` passaggio segreto.

### Mappa del master e mappa dei giocatori

Il programma disegna ogni livello due volte:

| | Master | Giocatori |
|---|---|---|
| numeri delle stanze | sì, in grassetto | no |
| porte segrete `$` | sì | diventano muro |
| passaggi segreti `░` | sì | diventano roccia |
| scale e pozzi nascosti | sì | non si vedono |
| tutto il resto | sì | sì |

La mappa dei giocatori della tomba: la porta segreta sotto `1-01` è un muro, il passaggio segreto è sparito, ma l'acqua, il crollo e i gradini si vedono.

```
                 ╔══════════════════╗
                 ║..................║
                 ║..................║
                 ║..................║
                 ║..................║
                 ╚═╦═╦══════╦+╦═════╝
                   #.#      ║.║
                   #.#      #.#
                   #≈#    ###.#
                   #≈#    #...#
                   #≈#  ###.#######
                   #.####.........#####
####################.#................##################
#......................#...........##..................#
#......##############.###..........##############......#
#......#            #.# ##...#######            #......#
########            #.#  ###.#                  ########
                    #.#    #≡#
                    #∴#    #≡#
                    #.#    #.#
                    #.#    #.#
                    #.#    #.#
                    ║.║    ║.║
                   ╔╩+╩════╩.╩═══════╗
                   ║.................║
                   ║..■..■..■..■..■..║
                   ║.................║
                   ║..■..■..■..■..■..║
                   ║.................║
                   ╚═════╦═════+╦════╝
                         ║......║
                         ║.╔════╝
                   ╔═════╩.╩═════════╗
                   ║.................║
                   ║..■..■..■..■..■..║
                   ║.................║
                   ║.................║
                   ║.................║
                   ║..■..■..■..■..■..║
                   ║.................║
                   ╚═══════╦+╦═══════╝
                           ║.║
                           ║.║
                           [A]
```

Le due mappe vengono ritagliate allo stesso modo, così si sovrappongono perfettamente.

---

## 16. Dal disegno al foglio

### La pagina

La pagina ha: il nome del dungeon (se lo vuoi), una riga con seme e numeri, i livelli disposti in una griglia e la **legenda**. La legenda elenca solo i simboli che compaiono davvero, più la **scala** (1 casella = 5 ft oppure 1,5 m, come hai scelto).

Il programma prova tutte le disposizioni possibili dei livelli (1 colonna, 2 colonne, 3…) e, per ogni formato di carta (A4, A3, A2, A1), sceglie quella con le **lettere più grandi**; a parità, quella che riempie meglio il foglio. Prova il foglio sia in verticale sia in orizzontale.

### La grandezza delle lettere

| Lettere | Giudizio |
|---|---|
| almeno 1,3 mm | leggibili |
| tra 1,1 e 1,3 mm | piccole |
| sotto 1,1 mm | troppo piccole |

Il programma suggerisce il foglio più piccolo con lettere leggibili e mostra tutte le alternative; le lettere non superano 3,2 mm su un A4 (di più sui fogli più grandi). Con "un livello per foglio", tutti i fogli usano la stessa grandezza di lettere, così le mappe combaciano.

### I file

- **PNG** a 600 dpi o **PDF** (una pagina per foglio), in tre colori a scelta.
- Un **.txt** con gli stessi caratteri della mappa, da aprire con qualunque editor.
- La mappa dei giocatori ha la stessa disposizione e la stessa grandezza di lettere di quella del master.

---

## 17. Un esempio completo su più livelli

Seme `3-21-2-4-CDK-000F62`: *La Cittadella di Sullenis*. Torre, castello e Underdark; 21 stanze; 2 ingressi; 4 segreti.

### Livello 1 · Torre

Sopra il suolo, sopra il castello. Tutte le stanze sono rotonde (pianta radiale), tutte dei fondatori (muri doppi). Il portale `Ω` in `1-04` porta alle grotte del livello 3; il pozzo `○` in `1-02` scende fino al livello 3 saltando il castello. Sul corridoio tra `1-01` e `1-04` c'è una porta segreta `$` e un tratto allagato `≈`.

```
                             ╔════════╗
                            ╔╝........╚╗
                           ╔╝..........╚╗
                           ║....1-01....║
                           ║............║
                           ╚╗..........╔╝
                            ╚╗........╔╝
                             ╚╦+══╦╦$═╩═══╗
                              ║..≡║║....≈≈║
                              ╚═╗≡║╚════╗≈║
  ╔═══════╗                 ╔═══╩+╩═══╗ ║.║
╔═╝○......╚═╦═════════════╗╔╝.........╚╗║.║           ╔══════╗
║...........+.............╠╝...........╚╣.║         ╔═╝....Ω.╚═╗
║....1-02...╠═══════════╗.║....1-03.......║         ║..........║
║...........║           ║.+..>..........║.╚═════════╣...1-04...║
║...........║           ╚═╩╗...........╔╣...........+..........║
╚═╗.......╔═╝              ╚╗.........╔╝╚═══════════╩═╗......╔═╝
  ╚════╦+═╩═══════════════╗ ╠+╦═══════╝               ╚══════╝
       ║..................║ ║.║
       ╚════════════════╗.║ ║.║
                        ║.║ ║.╚═╗
                        ║.║ ║...║
                        ╠+╩═╩══+╩═╗
                       ╔╝..>......╚╗
                      ╔╝...........╚╗
                      ║....1-05.....║
                      ║.............║
                      ╚╗...........╔╝
                       ╚╗.........╔╝
                        ╚═════════╝
```

### Livello 2 · Castello

È il livello del suolo: qui c'è l'ingresso **A**. Con sole 5 stanze, il castello è fatto di quattro torri rotonde agli angoli e di un cortile grande al centro (`2-03`). Tra le due torrette in alto corre un **passaggio segreto** `░`. La scala `>` in `2-02` scende nel sottolivello `2a`.

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
          ║.........║             ╔═══════════╩══+╦═════╝
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

La stessa mappa per i giocatori: niente numeri, e il passaggio segreto tra `2-01` e `2-02` è scomparso.

```
        [A]
        ║.║
        ║.║
  ╔═════╩+╩═╗
 ╔╝....>....╚╗                                ╔═════════╗
╔╝...........╚╗                              ╔╝....>....╚╗
║.............║                             ╔╝...........╚╗
║.............║                             ║.............║
╚╗...........╔╝                             ║.............║
 ╚╗.........╔╝                              ╚╗...........╔╝
  ╚═══════╦.╩═══════╗                        ╚╗.........╔╝
          ║.........║             ╔═══════════╩══+╦═════╝
          ╚═══════╗.║             ║...............║
                  ║.║             ║.╔══════════╗≡╔╝
                  ║.║             ║.║          ║≡║
                 ╔╩+╩═════════════╩+╩╗         ║.║
                 ║...................║         ║.║
                 ║...................║         ║.║
                 ║...................║         ║.║
                 ║...................║         ║.║
                 ║.................<.║         ║.║
                 ║...................║         ║.║
                 ╚╦+╦══════════════╦+╣         ║.║
                  ║.║              ║.╚═════════╝.║
          ╔═══════╝.║              ║.............║
          ║.........║              ╚═══════════╦+╩══════╗
    ╔═════╩+╦═══════╝                        ╔═╝........╚═╗
  ╔═╝.......╚═╗                             ╔╝...>........╚╗
  ║...........║                             ║..............║
  ║...........║                             ║..............║
  ║...........║                             ║..............║
  ║.......<...║                             ╚╗............╔╝
  ╚═╗.......╔═╝                              ╚═╗........╔═╝
    ╚═══════╝                                  ╚════════╝
```

### Sottolivello 2a · Castello

Tre stanze della seconda epoca (muri singoli), a metà tra il castello e le grotte. Si entra con la scala da `2-02`, si esce con il pozzo `○` di `2a-03`, che scende al livello 3. Ha il suo anello, con una porta segreta.

```
                                                     ┌──────────┐
                                                     │..........│
 ┌───────┐                                           │..........│
 │.<.....│                                           │..2a-02...│
 │.......├───────────────────────────────────────────┤..........│
 │.2a-01.+...........................................+..........│
 │.......├─────┐.┌───────────────────────────────────┴──────────┘
 │.......│     │.│
 └─┬─+┬──┘     │.│
   │..│        │.│
   │.┌┘        │.│
   │.│         │.│
┌──┴+┴─────────┤.│
│..............$.│
│.....2a-03.○..├─┘
│..............│
└──────────────┘
```

### Livello 3 · Underdark (diviso)

Il livello è **diviso**: la parte ovest (`3-01`, `3-03`, `3-06`) e la parte est (le altre) non si toccano. Per passare dall'una all'altra bisogna risalire. Quasi tutte le stanze sono grotte naturali (`#`), ma alcune (`3-01`, `3-02`) sono dei fondatori: i conti che costruirono la torre scavarono anche quaggiù. L'ingresso **B** a destra è l'**ingresso a metà dungeon**.

```
                                           ╔═══════════════╗
╔═══════════╗                              ║...............║
║....○......║                              ║..■..■..■..■...║
║...........║                              ║......3-02.....║
║...3-01....║                              ║..■<.■..■..■...║
║...........║                              ║...............║
╚═════════╦+╣                              ╚═════╦═══.╦════╝
          ║.║                                    ║....║
          ║.╚════════════════╗                   ║.╔══╝
          #...............∴..║                   ║≡║
         ##.#####══════════╗.║                   #≡#
     #####......###########║.║                 ###.######                ##########
     #..............≈≈≈≈≈.#║.║              ####........#######      #####........###
     #..<...........≈.≈≈≈.##.║              #.................########..............######
     #........3-03.........#.║              #.......3-04..........≡≡......3-05............ [B]
     ####.................##.║              ##...............#########..............######
        ###.........###.###╝.║               ###...........###       #####.......####
          ########### #......║                 ######.######             #######.#
                      #.╔════╝                      #.#                        #.#
                      #.#                           #.#                        #.#
                      #.#                           #.#                    #####.#
                      #.# ##########          #######.####                 #.....#
                      #$###........####    ####..........###             ###.#####
                     ##...............#    #...............#####        ##......###
                     #......3-06......#    #........3-07.......##########○........#
                     ##...............#    #............................#.≈.3-08..#
                      ###...........###    #....Ω.............#########...≈≈≈≈≈.###
                        #############      #########......#####       ####.....##
                                                   ########              #######
```

Il risultato della verifica:

```
✓ Ingressi multipli: 2
✓ Anelli (numero ciclomatico del dungeon): 12; su ogni livello: 1: 2, 2: 2, 2a: 1, 3: 2
✓ Collegamenti multipli tra livelli: 1↔2: 2, 2↔3: 2
✓ Collegamenti discontinui (saltano livelli): 2
✓ Percorsi segreti e insoliti: 3 porte segrete, 1 passaggi segreti, 0 scale/pozzi nascosti, 1 allagati, 1 crolli, 1 portali
✓ Sottolivelli: 2a
✓ Livelli divisi: 3
✓ Dislivelli interni (gradini nello stesso livello): 4
✓ Ingresso a metà dungeon: 1
✓ Dungeon annidati: grotte naturali e complesso costruito collegati in 6 punti
```

Prova a rigenerarlo:

```
python wyrmdelve.py --seme 3-21-2-4-CDK-000F62 --per-livello
```

---

## 18. Cosa puoi cambiare nel file JSON

Il file `wyrmdelve_tables.json` contiene soprattutto parole, ma per ogni tipo di dungeon ci sono anche alcuni numeri che cambiano la mappa:

| Campo | Cosa cambia | Esempio |
|---|---|---|
| `pattern` | la pianta (capitolo 6): `palace`, `prison`, `tower`, `castle`, `temple`, `city`, `wizard`, `academy`, `fortress`, `tomb`, `underdark` | un "tempio" con `"pattern": "tomb"` avrà la pianta di una tomba |
| `eras` | i pesi delle quattro epoche N, I, II, III | `[0.75, 0.1, 0.1, 0.05]` = soprattutto grotte |
| `loops` | la percentuale di anelli | `0.5` = un anello ogni due stanze |
| `portal` | la probabilità del portale | `1.0` = sempre |
| `below` | i tipi che possono stare sotto | `["tomb", "underdark"]` |
| `surface` | se il tipo sta sopra il suolo | `true` / `false` |

Attenzione: cambiando questi numeri, **lo stesso seme darà una mappa diversa** da prima. Le parole invece (nomi delle stanze, storia, ingressi…) cambiano solo i testi.
