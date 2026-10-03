# Come aggiungere mostri al bestiario

Questa guida spiega, passo per passo, come aggiungere i tuoi mostri a WyrmDelve. Non serve saper programmare: basta un editor di testo e un po' di attenzione alle virgolette.

> Come il programma usa i mostri (tabelle dei mostri erranti, stanze, indizi, mostri fuori posto) è spiegato nel capitolo 15 di [story_generation_algorithm.md](story_generation_algorithm.md).

## Indice

1. [Dove sono i mostri](#1-dove-sono-i-mostri)
2. [Com'è fatto un mostro](#2-comè-fatto-un-mostro)
3. [I campi uno per uno](#3-i-campi-uno-per-uno)
4. [Aggiungere un mostro, passo per passo](#4-aggiungere-un-mostro-passo-per-passo)
5. [Esempi pronti da copiare](#5-esempi-pronti-da-copiare)
6. [Aggiungere indizi](#6-aggiungere-indizi)
7. [Aggiungere motivi per i mostri fuori posto](#7-aggiungere-motivi-per-i-mostri-fuori-posto)
8. [Provare il risultato](#8-provare-il-risultato)
9. [Errori comuni](#9-errori-comuni)
10. [Licenze: cosa si può copiare](#10-licenze-cosa-si-può-copiare)

---

## 1. Dove sono i mostri

Tutti i mostri stanno nel file **`wyrmdelve_tables.json`**, nella stessa cartella di `wyrmdelve.py`, sotto la voce `"monsters"`. Ogni mostro è **una riga**.

Prima di cominciare:

1. **Fai una copia** del file (per esempio `wyrmdelve_tables_copia.json`): se qualcosa va storto, la rimetti al suo posto.
2. Apri il file con un editor di testo semplice: Blocco note su Windows, TextEdit su Mac (in modalità "testo semplice"), oppure un editor come Visual Studio Code, che colora il testo e segnala gli errori.
3. Cerca `"monsters"` (Ctrl+F su Windows, Cmd+F su Mac).

---

## 2. Com'è fatto un mostro

Ecco un mostro vero, preso dal file:

```json
{"name": {"it": "ghoul", "en": "ghouls"}, "text": {"it": "morti affamati di carne; i loro artigli paralizzano", "en": "dead hungry for flesh; their claws paralyse"}, "where": ["tomb", "temple", "prison"], "danger": 1, "kind": "undead", "number": "2d6"},
```

Letto in italiano: *i ghoul sono morti affamati di carne, si trovano in tombe, templi e prigioni, sono poco pericolosi (1), sono non morti, e se ne incontrano 2d6.*

Nella chiave del dungeon diventa:

```
  Mostri erranti (d6)
    3. Ghoul: morti affamati di carne; i loro artigli paralizzano.

  1-04 Mostri: Ghoul (2d6).
  1-05 Vuota. Indizio: ossa rosicchiate da denti umani (da 1-04).
```

---

## 3. I campi uno per uno

| Campo | Cosa contiene | Obbligatorio | Esempio |
|---|---|---|---|
| `name` | il nome, in italiano (`it`) e in inglese (`en`) | sì | `{"it": "ghoul", "en": "ghouls"}` |
| `text` | una riga di descrizione, in tutte e due le lingue | sì | `{"it": "morti affamati di carne…", "en": "dead hungry for flesh…"}` |
| `where` | in quali **tipi di dungeon** può comparire | no (senza: ovunque) | `["tomb", "temple"]` oppure `["*"]` |
| `danger` | quanto è **pericoloso**, da 1 a 4 | no (senza: 2) | `1` |
| `kind` | che **creatura** è: decide gli indizi e i motivi per essere fuori posto | no (senza: niente indizio) | `"undead"` |
| `number` | **quanti** se ne incontrano | no (senza: nessun numero) | `"2d6"` |

### `where`: i tipi di dungeon

Scrivi uno o più di questi nomi, tra virgolette e separati da virgole:

| Nome | Tipo | Nome | Tipo |
|---|---|---|---|
| `palace` | Palazzo | `wizard` | Laboratorio arcano |
| `prison` | Prigione | `academy` | Accademia |
| `tower` | Torre | `fortress` | Fortezza di confine |
| `castle` | Castello | `tomb` | Tomba |
| `temple` | Tempio | `underdark` | Underdark |
| `city` | Città | `*` | **ovunque** |

Un mostro compare nelle tabelle di un livello solo se quel livello è di un tipo elencato. Più tipi metti, più spesso uscirà.

### `danger`: il pericolo

| Valore | Pericolo | Dove esce di solito | Esempi |
|---|---|---|---|
| `1` | basso | primo livello | ratti giganti, goblin, scheletri |
| `2` | medio | secondo livello | ghast, ogre, cubo gelatinoso |
| `3` | alto | terzo livello | troll, mummia, basilisco |
| `4` | mortale | livelli più profondi | draghi, lich, golem di ferro |

Il programma mette in ogni livello mostri del pericolo giusto per quella profondità: al primo livello il pericolo 1, poi un punto in più per ogni livello, fino a 4.

### `kind`: che creatura è

| `kind` | Creature | Indizio tipico |
|---|---|---|
| `vermin` | insetti, ragni, ratti, pipistrelli | gusci vuoti, ragnatele |
| `beast` | animali, rettili | ciuffi di pelo, graffi |
| `aquatic` | creature d'acqua | pozze e scie viscide |
| `ooze` | melme e gelatine | pareti stranamente pulite |
| `fungus` | funghi, muffe, piante | spore luminose |
| `magical` | bestie magiche (basilisco, mimic…) | statue con espressione di terrore |
| `dragon` | draghi | scaglie grandi come scudi |
| `giant` | giganti, ogre, troll | orme enormi |
| `humanoid` | persone e umanoidi | i resti di un fuoco |
| `undead` | non morti con un corpo | bende sporche, odore di tomba |
| `spirit` | spiriti e fantasmi | candele che si spengono da sole |
| `construct` | golem, statue, automi | un piedistallo vuoto |
| `elemental` | elementali e geni | un cerchio di evocazione spezzato |
| `demon` | demoni e diavoli | simboli bruciati, zolfo |

Puoi inventare un `kind` nuovo: in quel caso aggiungi anche i suoi indizi (capitolo 6), altrimenti il mostro non lascerà indizi.

### `number`: quanti

Un'espressione di dadi come `"1"`, `"1d3"`, `"1d6"`, `"2d6"`, `"3d6"`. Lascia `""` per gli sciami e le cose che non si contano (una nuvola di pipistrelli, uno sciame d'insetti). Il programma la scrive accanto al nome: `Ghoul (2d6)`.

Una regola semplice: pericolo 1 → `"2d6"`, pericolo 2 → `"1d6"`, pericolo 3 → `"1d3"`, pericolo 4 → `"1"`.

---

## 4. Aggiungere un mostro, passo per passo

Aggiungiamo la **sanguisuga delle cripte**, un mostro inventato.

**1. Trova l'ultimo mostro dell'elenco.** È la riga subito prima di `  ],` e di `"clues"`:

```json
    {"name": {"it": "megera marina", "en": "sea hag"}, …, "number": "1d6"}
  ],
  "clues": {
```

**2. Aggiungi una virgola alla fine dell'ultima riga**, perché dopo ne arriva un'altra:

```json
    {"name": {"it": "megera marina", "en": "sea hag"}, …, "number": "1d6"},
```

**3. Scrivi il tuo mostro sotto**, senza virgola alla fine (ora è lui l'ultimo):

```json
    {"name": {"it": "sanguisuga delle cripte", "en": "crypt leech"}, "text": {"it": "si nasconde nei sarcofagi e succhia il calore dei vivi", "en": "hides in sarcophagi and drains the warmth of the living"}, "where": ["tomb"], "danger": 2, "kind": "undead", "number": "1d6"}
  ],
  "clues": {
```

**4. Salva il file** e prova il programma (capitolo 8).

Puoi anche inserire il mostro **in mezzo** all'elenco: in quel caso la tua riga deve finire con una virgola, come tutte le altre.

---

## 5. Esempi pronti da copiare

Un mostro per ogni situazione tipica. Copia la riga, cambia le parole, salva.

**Uno sciame che si trova ovunque** (senza numero):

```json
{"name": {"it": "sciame di falene", "en": "moth swarm"}, "text": {"it": "falene grigie che spengono le torce e lasciano polvere negli occhi", "en": "grey moths that put out torches and leave dust in the eyes"}, "where": ["*"], "danger": 1, "kind": "vermin", "number": ""},
```

**Un gruppo di persone in città**:

```json
{"name": {"it": "contrabbandieri", "en": "smugglers"}, "text": {"it": "spostano merci proibite attraverso le fogne", "en": "move forbidden goods through the sewers"}, "where": ["city", "prison"], "danger": 1, "kind": "humanoid", "number": "2d6"},
```

**Una creatura d'acqua** (può comparire anche "fuori posto", risalita dalle grotte allagate):

```json
{"name": {"it": "anguilla delle cisterne", "en": "cistern eel"}, "text": {"it": "un'anguilla pallida e cieca che morde le caviglie", "en": "a pale, blind eel that bites at ankles"}, "where": ["underdark", "city"], "danger": 1, "kind": "aquatic", "number": "1d6"},
```

**Un guardiano costruito dai fondatori** (può comparire "fuori posto" nelle sale dei fondatori):

```json
{"name": {"it": "cavaliere di bronzo", "en": "bronze knight"}, "text": {"it": "una statua equestre che carica chi non conosce la parola d'ordine", "en": "an equestrian statue that charges anyone without the password"}, "where": ["castle", "palace", "fortress"], "danger": 3, "kind": "construct", "number": "1"},
```

**Un mostro unico e mortale delle profondità**:

```json
{"name": {"it": "verme della memoria", "en": "memory worm"}, "text": {"it": "un verme lungo un corridoio che divora i ricordi di chi tocca", "en": "a worm as long as a corridor that devours the memories of whoever it touches"}, "where": ["underdark"], "danger": 4, "kind": "magical", "number": "1"},
```

---

## 6. Aggiungere indizi

Gli indizi stanno sotto `"clues"`, raggruppati per `kind`. Ogni volta che un mostro abita una stanza, il programma sceglie un indizio del suo `kind` e lo mette in una stanza vuota vicina.

```json
  "clues": {
    "undead": [
      {"it": "un freddo innaturale e impronte di piedi scalzi nella polvere", "en": "an unnatural cold and bare footprints in the dust"},
      {"it": "bende sporche e un odore di tomba", "en": "dirty bandages and a smell of the grave"},
      {"it": "ossa rosicchiate da denti umani", "en": "bones gnawed by human teeth"}
    ],
```

Per aggiungere un indizio, aggiungi una riga nell'elenco giusto (con la virgola tra una riga e l'altra). Scrivi una cosa che si **vede, sente o annusa**, senza nominare il mostro: deve far venire un sospetto, non svelare tutto. Nella chiave diventa:

```
  1-05 Vuota. Indizio: ossa rosicchiate da denti umani (da 1-04).
```

Per un `kind` nuovo, aggiungi un elenco nuovo:

```json
    "insect_queen": [
      {"it": "celle di cera vuote e un ronzio profondo", "en": "empty wax cells and a deep humming"}
    ],
```

---

## 7. Aggiungere motivi per i mostri fuori posto

Ogni tanto (circa un livello su tre) un mostro **non adatto** al tipo del livello ci vive lo stesso, per un motivo. I motivi stanno sotto `"quirks"`:

```json
{"when": "water", "kinds": ["aquatic"], "text": {"it": "le grotte allagate{from} arrivano fin sotto questa stanza, attraverso una vasca", "en": "the flooded caves{from} reach up under this room, through a pool"}},
```

| Campo | Cosa contiene |
|---|---|
| `when` | **quando** il motivo è possibile (vedi sotto) |
| `kinds` | quali `kind` di mostro può riguardare (`[]` = tutti) |
| `text` | il motivo, in tutte e due le lingue |

I valori di `when`:

| `when` | Il motivo vale solo se… | Segnaposto |
|---|---|---|
| `water` | un altro livello ha grotte naturali e acqua | `{from}` = « del livello 3» |
| `portal` | il dungeon ha un portale magico | `{room}` = la stanza del portale |
| `below` | il livello sotto è di un altro tipo; il mostro viene scelto tra quelli di quel tipo | `{level}` = il numero del livello |
| `founders` | il livello ha stanze dei fondatori | |
| `any` | sempre | |

Nella chiave:

```
  2-03 Mostri: Aboleth (1). Fuori posto: le grotte allagate del livello 3 arrivano fin sotto questa stanza, attraverso una vasca.
```

**Una regola importante:** scrivi il motivo parlando del **luogo**, non del mostro. Il mostro può essere uno solo o un gruppo (*un aboleth*, *dei lupi*): una frase come «è arrivato dal portale» non funzionerebbe con *lupi*. Scrivi invece «il portale di {room} ogni tanto lascia passare qualcosa».

---

## 8. Provare il risultato

Dopo aver salvato, genera un dungeon del tipo giusto con i mostri. Esempio per una tomba di 3 livelli:

```
python wyrmdelve.py --tipo 10 --livelli 3 --contenuto mostri
```

(`--tipo 10` è la tomba: il numero è la posizione nel menu dei tipi, da 1 a 11.)

Poi apri il file `_key.txt` nella cartella del dungeon e cerca il tuo mostro. Se non c'è, rigenera più volte senza `--seme`: i mostri si pescano a caso tra quelli adatti, e con 245 mostri non escono tutti ogni volta.

---

## 9. Errori comuni

Se il file JSON ha un errore, il programma si ferma subito e dice in quale riga guardare:

```
C'è un errore nel file wyrmdelve_tables.json / There is a mistake in wyrmdelve_tables.json:
  Expecting ',' delimiter: line 3912 column 5
```

| Errore | Causa tipica | Come sistemare |
|---|---|---|
| `Expecting ',' delimiter` | manca la virgola alla fine della riga **prima** | aggiungi la virgola |
| `Expecting property name` | c'è una virgola di troppo dopo l'**ultima** riga di un elenco | togli la virgola prima di `]` |
| `Expecting value` | virgolette mancanti, oppure `'` al posto di `"` | usa sempre le virgolette doppie `"` |
| `Invalid control character` | un a capo dentro un testo | scrivi il testo tutto su una riga |
| il mostro non esce mai | `where` sbagliato (per esempio `"tombs"` invece di `"tomb"`) | controlla la tabella del capitolo 3 |
| niente indizio vicino al mostro | il suo `kind` non ha indizi | aggiungili sotto `clues` |

Dentro un testo puoi usare l'apostrofo (`l'ingresso`) senza problemi. Se ti serve una virgoletta doppia, scrivila così: `\"`.

---

## 10. Licenze: cosa si può copiare

WyrmDelve è distribuito con licenza GPL 3.0, e chiunque può copiarlo. Per questo, nel file JSON:

- **puoi** scrivere mostri tuoi, con parole tue;
- **puoi** usare materiale con licenza **Creative Commons BY** (per esempio l'SRD 5.1 o Ironsworn), ricordandoti di **citare la fonte** nei `credits` del file JSON e nella sezione Fonti del README;
- **non copiare** descrizioni da libri o PDF che non hanno una licenza aperta: puoi però prendere l'**idea** di un mostro e il suo nome, se è generico (un ghoul, un ragno gigante), e descriverlo con parole tue. È quello che è stato fatto con i due bestiari citati nel README;
- **evita** i nomi registrati da altri: per esempio *beholder*, *mind flayer*, *displacer beast*, *umber hulk*, *carrion crawler*, *githyanki*, *yuan-ti*.
