# WyrmDelve

<div align="center">

**Italiano** · [English](README.md)

</div>

<table align="center"><tr><td><pre>
      *         :       :       :       :       :          *
  . (     . . . . .           . . . . . . . . . . . .  . (    .
   ) )  *   :       :  (__)         :   `   :    /  :   ) )  *
  ( ( )  .. . . .   _--) _(__   . . . . . . . . . . .  ( ( )  .
 ` )`(      ;    /¯¯  ( {φ}) \  :       :       :     ` )`(
  \~~~/   . .   /(  )  \ ~/  ))   . . . . . . . . . .  \~~~/  .
   |≡|   ´  :  / |`´).  ¯¯. / )    /:       :       :   |≡|   ´
. .\_/. .\. .  | | /       /\ |   . . . . . . . . . . . \_/ . .
:   |   :      | ||       |  ||  .      :       :       :|
. .[=]. . . .  ├ππ\\ππ¢ππππ┤ ||  |\   . . . . . . . . . [=] . .
    |       :  |   \\---.  | ||  | \        :       :    |  :
. . . . . .   =====(_(≡=====(((≡=XXXX&gt;  . . . . . . . . . . . .
:       :      ||         ||    ´/    \      `  :       :
=============  ||         ||     `----´  =======================
    /      /   /\          \\   |      \      \   | σ       \
  /         /  ¯¯            ¯¯           \       ´√))θ       \
      /            /            |            \     / \    \
</pre></td></tr></table>

<div align="center">

<img src="img_examples/OSR%20LOGO.png" alt="Logo OSR" width="25%"><br>
Compatibile con qualunque gioco di ruolo analogico "OSR". Fratello di [WyrmHex](https://github.com/alepersichetti/WyrmHex).

</div>

### WyrmDelve v0.0.1

**WyrmDelve** disegna a caso dungeon e labirinti per campagne old school (OSR), fatti solo di lettere e simboli come nei roguelike NetHack, Angband, ADOM, Brogue, Caves of Qud e Dwarf Fortress.

Ogni dungeon ha una **storia a strati**, e si vede dai muri:

| Muri | Strato |
|---|---|
| `#` (grotte irregolari) | **N** — grotte naturali, più antiche di ogni costruzione |
| `═║╔╗` | **I** — i fondatori (re, cavalieri, sacerdoti, maghi, legioni, nani…) |
| `─│┌┐` | **II** — chi venne dopo (cultisti, contrabbandieri, un negromante, goblin, monaci) |
| `#` (stanze sbozzate) | **III** — gli abitanti di oggi (un orco, orchetti, non morti, ragni, trogloditi) |

Le stanze sono numerate **livello-stanza**: `1-01`, `2-07`, e `1a-01` per un sottolivello. La chiave del dungeon racconta per ogni stanza a cosa serviva in ogni epoca (es. *Sala del trono; II: bisca; III: tana dell'orco*).

Ogni livello è di uno di **11 tipi di dungeon**, ognuno con la sua pianta, le sue stanze, i suoi costruttori e i suoi ingressi:

| N. | Tipo | Pianta |
|---|---|---|
| 1 | Antico palazzo | simmetrica rispetto a un asse, la sala del trono al centro, le ali in coppie speculari |
| 2 | Sotterraneo o prigione di creature intelligenti o arcane | file di piccole celle, corpi di guardia alle estremità, una fossa al centro |
| 3 | Torre | stanze rotonde strette attorno a una scala centrale |
| 4 | Castello | edifici attorno a un cortile, torri rotonde agli angoli, il mastio |
| 5 | Tempio | una lunga navata sull'asse con l'abside in testa, cappelle laterali a coppie |
| 6 | Città | edifici fitti, strade tra l'uno e l'altro, una piazza al centro |
| 7 | Dungeon alchemico o arcano di un mago | stanze rotonde e ottagonali attorno a un cerchio di evocazione |
| 8 | Accademia magica o religiosa | aule tutte uguali attorno a un chiostro, una biblioteca e un'aula magna |
| 9 | Fortezza di confine | una lunga linea fortificata, bastioni alle estremità, il mastio al centro, la porta |
| 10 | Tomba o cripta | un asse processionale dall'anticamera alla camera funeraria, nicchie a coppie |
| 11 | Underdark o grotte sotterranee | caverne naturali sparse, una grande caverna |

I livelli sono **impilati in modo coerente**: una torre può stare sopra un castello ma mai sotto una grotta, una cripta sta sotto un tempio e mai sopra un castello, e l'Underdark è sempre in fondo. L'ingresso principale è al piano terra (l'edificio più basso sopra il suolo, oppure il livello più in alto se è tutto sotterraneo).

La pianta segue **sempre** i principi di Jennell Jaquays, come li descrive Justin Alexander in *Xandering the Dungeon*: ingressi multipli, anelli, collegamenti multipli e discontinui tra i livelli, percorsi segreti e insoliti (porte e passaggi segreti, scale nascoste, passaggi allagati, crolli, portali), sottolivelli, livelli divisi, dislivelli interni, ingressi a metà dungeon, dungeon annidati. A fine generazione il programma verifica che ogni stanza sia raggiungibile e stampa quali principi ha applicato.

---

## 1. Cosa ti serve

Metti questi file nella **stessa cartella**, per esempio una cartella `dungeon` sul Desktop:

- `wyrmdelve.py` (il programma)
- `wyrmdelve_tables.json` (le parole di cui sono fatti i dungeon: nomi, stanze, storia; vedi il capitolo 7)
- la cartella `fonts` (i font delle mappe e del PDF della storia: il programma usa solo questi, così non dipende dal tuo sistema)
- `requirements.txt` (l'elenco di quello che serve al programma)
- `README.md` (la stessa guida in inglese) e `README.it.md` (questa guida)

Non devi creare nient'altro: la cartella `dungeons_generated`, dove vengono salvati i dungeon, la crea il programma la prima volta che lo usi.

Ti serve anche **Python**, il programma che fa funzionare i file `.py`: versione **3.8 o più recente** (meglio l'ultima).

---

## 2. Installazione

La fai **una volta sola**. Ci vogliono circa cinque minuti.

### Passo 1 — Installa Python

- **Windows e macOS:** vai su <https://www.python.org/downloads/>, scarica l'ultima versione e installala come un qualsiasi programma.
  - Su Windows, se l'installazione mostra una casella **"Add python.exe to PATH"**, mettici la spunta.
- **Linux:** di solito Python è già installato.

### Passo 2 — Apri il terminale nella cartella con i file

Il terminale è una finestra in cui si scrivono comandi. Niente paura: dovrai solo copiare e incollare i comandi di questa guida. Dopo aver incollato un comando, premi **Invio** per eseguirlo.

- **Windows 11:** apri la cartella `dungeon`, fai clic destro in uno spazio vuoto e scegli **"Apri nel terminale"**.
- **Windows 10:** apri la cartella `dungeon`, fai clic sulla barra dell'indirizzo in alto, scrivi `cmd` e premi Invio.
- **macOS:** apri l'app **Terminale** (in Applicazioni → Utility). Scrivi `cd` seguito da uno spazio, trascina la cartella `dungeon` nella finestra e premi Invio.
- **Linux:** apri la cartella, fai clic destro in uno spazio vuoto e scegli **"Apri nel terminale"**.

### Passo 3 — Crea l'ambiente virtuale (consigliato)

Il programma riceve uno spazio tutto suo dentro la cartella, chiamato *ambiente virtuale*: una sottocartella nascosta di nome `.venv`, da lasciare com'è. Così le librerie che gli servono non si mescolano con il resto del computer, e se qualcosa va storto basta cancellare `.venv` e ricominciare. Scrivi:

**Windows**
```
py -m venv .venv
```

**macOS e Linux**
```
python3 -m venv .venv
```

Sullo schermo non compare nulla: è normale. Lo fai una volta sola.

### Passo 4 — Attiva l'ambiente virtuale

Attivarlo dice al terminale di usare il Python che sta dentro `.venv`. Scrivi:

**Windows**
```
.venv\Scripts\activate
```

**macOS e Linux**
```
source .venv/bin/activate
```

Da questo momento la riga in cui scrivi comincia con `(.venv)`: è così che capisci che è attivo. Devi riattivarlo ogni volta che apri un nuovo terminale (vedi il capitolo 3).

### Passo 5 — Installa le librerie

Con l'ambiente virtuale attivo, scarica **Pillow**, la libreria che crea le immagini, e **fpdf2**, quella che scrive il PDF della storia. Il comando è uguale su tutti i sistemi:

```
pip install -r requirements.txt
```

Se alla fine vedi una riga che comincia con `Successfully installed`, è tutto a posto. Lo fai una volta sola.

---

## 3. Creare un dungeon

Apri il terminale nella cartella, come nel passo 2. Prima attiva l'ambiente virtuale (come nel passo 4), poi avvia il programma:

**Windows**
```
.venv\Scripts\activate
python wyrmdelve.py
```

**macOS e Linux**
```
source .venv/bin/activate
python wyrmdelve.py
```

Basta attivarlo una volta ogni volta che apri un terminale: finché la riga comincia con `(.venv)` è attivo, e puoi creare tutti i dungeon che vuoi con `python wyrmdelve.py`. Quando hai finito, scrivi `deactivate` o chiudi semplicemente il terminale. Se hai appena finito l'installazione nella stessa finestra, l'ambiente è già attivo.

Il programma ti fa alcune domande. **Ogni domanda ha una risposta già pronta tra parentesi quadre: se ti va bene, premi solo Invio.**

1. **Lingua:** scrivi `1` per l'italiano o `2` per l'inglese (con Invio resta l'italiano). Da qui in poi domande, messaggi e testi sulla mappa sono nella lingua scelta.
2. **Compare l'orco nel suo dungeon.** Premi **Invio** per un dungeon tutto casuale, scrivi **P** per scegliere tu i parametri, oppure **R** per rifare un dungeon che hai già creato (vedi il capitolo 4).
3. Con **P** scegli: numero di livelli, numero di stanze (almeno 5 per livello), numero di ingressi/uscite dall'area, numero di porte e passaggi segreti. Poi il **tipo di dungeon** (vedi la tabella in alto; `0` = a caso). Con più di un livello, il programma prima ti chiede se **i livelli sono tutti dello stesso tipo** o se **ogni livello ha il suo tipo**: in questo caso li scegli uno per uno dall'alto, e per ogni livello l'elenco mostra solo i tipi che possono stare sotto quello di sopra.

   Con **Invio** (dungeon tutto casuale) i tipi li sceglie il programma, sempre in un ordine coerente.
4. **Colori:**
   1. simboli neri su sfondo bianco (la risposta già pronta, la migliore per stampare)
   2. simboli bianchi su sfondo celeste
   3. simboli bianchi su sfondo nero
5. **Vuoi un nome per la mappa?** Se no, la mappa esce senza titolo. Se sì, scegli se **generarlo a caso** (es. *Tomba di Zordur*, la risposta già pronta) o **scriverlo tu**.
6. **Vuoi anche la storia del dungeon?** `1` = mappe e storia (la risposta già pronta: la chiave in `.txt` e in PDF), `2` = solo le mappe. Il programma lo chiede ogni volta, anche per un dungeon tutto casuale.
7. **Unità di misura della griglia:** `1` = imperiale, **1 casella = 5 ft** (piedi); `2` = metrica, **1 casella = 1,5 m** (la risposta già pronta in italiano). La scala viene scritta nella legenda delle mappe, nella chiave e nel PDF della storia; il dungeon è lo stesso con entrambe le scelte.

A questo punto il programma costruisce il dungeon. Mostra ogni passaggio con una barra che si riempie:

```
[████░░░░░░]  4/10  Corridoi e anelli
```

Poi fa le ultime tre domande:

7. **Come impaginare i livelli:**
   1. tutti i livelli in **un solo foglio** (la risposta già pronta)
   2. **un livello per foglio**, su file separati

   Con un solo livello questa domanda non compare.
8. **Che file vuoi:** un'immagine **PNG** (una per foglio) oppure un **PDF** (con un livello per foglio, un solo PDF con tutti i fogli: comodo per stampare tutto in una volta).
9. **Formato di stampa:** il programma mostra una tabella con **A4, A3, A2 e A1**: per ognuno, quanto saranno grandi i caratteri e se si leggono bene. La risposta già pronta tra parentesi è il **formato consigliato**, il foglio più piccolo su cui la mappa si legge bene. Premi Invio per accettarlo o scrivi un altro formato, per esempio `A3`. Ad esempio:

   ```
   · A4  orizzontale  livelli 2x2   caratteri da 1.29 mm   piccolo
   · A3  orizzontale  livelli 2x2   caratteri da 1.88 mm   leggibile   <- consigliato
   · A2  orizzontale  livelli 2x2   caratteri da 2.71 mm   leggibile
   · A1  orizzontale  livelli 2x2   caratteri da 3.89 mm   leggibile
   ```

   L'immagine esce sempre a **600 dpi** e il foglio si gira da solo in verticale o in orizzontale.

Alla fine il programma ti dice dove ha salvato i file e `Completato in ... s`.

---

## 4. Rifare un dungeon già creato

Ogni dungeon ha un **seme**, un codice come `3-24-2-5-CDK-K7Q2MB` (livelli-stanze-ingressi-segreti-tipi-codice). I tipi sono una lettera per livello dall'alto, da `A` a `K` nell'ordine della tabella in alto (`CDK` = torre, castello, Underdark); una lettera sola vuol dire che tutti i livelli sono di quel tipo. I semi delle versioni precedenti, senza i tipi, funzionano ancora. È stampato sotto il titolo della mappa ed è anche il nome della cartella del dungeon dentro `dungeons_generated`. **Lo stesso seme dà sempre lo stesso dungeon.**

Per rifarlo (per esempio su un altro formato o con altri colori), avvia il programma, scrivi **R** nella schermata dell'orco e scrivi il seme. Maiuscole e minuscole non contano, e O e 0, oppure I, L e 1, valgono come lo stesso carattere.

---

## 5. I file che ottieni

Tutto va in `dungeons_generated/<seme>/`, una cartella per ogni dungeon:

| File | Cosa contiene |
|---|---|
| `<seme>_gm.png` | la **mappa del master**: numeri delle stanze, porte segrete `$` e passaggi segreti `░` |
| `<seme>_players.png` | la **mappa dei giocatori**: la stessa mappa senza numeri e senza segreti |
| `<seme>_key.txt` | la **chiave del dungeon**: storia, strati, ingressi, collegamenti tra livelli, cosa c'è in ogni stanza, verifica dei principi di Jaquays |
| `<seme>_story.pdf` | la **storia**: la stessa chiave come un libro su pagine A4, con i titoli in Sebaldus-Gotisch e il testo in Crimson Text, pronta da stampare o da leggere sul tablet |
| `.txt` accanto a ogni mappa | la stessa mappa come testo semplice, da aprire con qualsiasi editor di testo |

Se scegli **solo le mappe**, la chiave e il PDF della storia non vengono creati.

I titoli della storia usano **Sebaldus-Gotisch** e il testo **Crimson Text**, entrambi nella cartella `fonts` (vedi `fonts/README.md`).

Con **un livello per foglio** i nomi dei PNG contengono il livello: `<seme>_gm_L1.png`, `<seme>_gm_L2a.png`… Tutti i fogli usano caratteri della stessa grandezza, così i livelli restano in scala. Con il **PDF** ottieni invece `<seme>_gm.pdf` e `<seme>_players.pdf` (una pagina per foglio, 600 dpi, senza perdita di qualità), ognuno con il suo `.txt`.

### Simboli

| Simbolo | Significato | Simbolo | Significato |
|---|---|---|---|
| `.` | pavimento | `+` | porta |
| `$` | porta segreta (solo master) | `░` | passaggio segreto (solo master) |
| `<` `>` | scale su / giù | `≡` | gradini, stesso livello |
| `○` | pozzo o camino tra livelli (può saltarne qualcuno) | `Ω` | portale magico |
| `≈` | acqua | `∴` | crollo |
| `■` | colonna | `[A]` | ingresso (riquadro pieno sulla mappa) |

**Scala.** Ogni lettera della mappa è una casella della griglia: **1 casella = 5 ft** (imperiale) oppure **1,5 m** (metrica), come scritto in fondo alla legenda. Le lettere sono più alte che larghe, quindi sulla carta le caselle sono rettangoli: per misurare conta le caselle, non i millimetri.

---

## 6. Stampare

Le immagini hanno già la misura esatta del foglio scelto, a 600 dpi: si stampano nitide anche sui fogli grandi.

- Stampa sul **formato che hai scelto**, con il foglio girato come l'immagine (verticale o orizzontale).
- Nelle opzioni di stampa scegli **"Dimensioni effettive"** o **"100%"**. Evita "Adatta alla pagina", che rimpicciolisce la mappa.
- Bianco su nero consuma molto inchiostro: è pensato per gli schermi (tablet, tavoli virtuali) più che per la carta.
- Se la tua stampante arriva solo all'A4, una copisteria può stampare A3, A2 e A1: porta il file PNG o PDF così com'è.

---

## 7. Cambiare le parole dei dungeon

La logica del programma sta in `wyrmdelve.py`; le **parole** che pesca a caso stanno in `wyrmdelve_tables.json`, **nella stessa cartella di `wyrmdelve.py`**: un file di testo che puoi aprire e modificare con qualsiasi editor (Blocco note, TextEdit…). Contiene circa 3.400 voci (stanze, costruttori, occupanti, grotte, eventi, luoghi, ingressi, sillabe per i nomi), che si combinano in miliardi di storie diverse:

| Sezione | Cosa contiene |
|---|---|
| `credits` | da dove vengono le voci (lascialo com'è) |
| `name_syllables` | `syllables`: le sillabe con cui si formano i nomi; `endings`: le desinenze dei nomi per lingua (arabo, danese, francese antico, persiano, greco, latino, tedesco, russo, stile Tolkien). Un nome è fatto di 2–3 sillabe, oppure di 1–2 sillabe più la desinenza di una lingua (*Drakberg*, *Rosslav*, *Phelias*, *Kaelhil*…). Puoi aggiungere una lingua: un nome nuovo con il suo elenco di desinenze |
| `dungeon_types` | gli 11 tipi (strato I): i loro nomi, come si impilano, la pianta, chi li costruì, il nome della mappa, le stanze e gli ingressi (vedi sotto) |
| `second_age` | chi venne dopo (strato II) e le sue stanze |
| `present_day` | gli abitanti di oggi (strato III) e le loro stanze |
| `natural_rooms` | le grotte naturali (strato N) |
| `events` | cosa chiuse ogni epoca |
| `areas` | dove si trova il dungeon: `surface` per gli edifici sopra il suolo, `underground` per gli altri |
| `surface_shaft` | l'ingresso usato quando nessuna parete del livello può ospitarne uno |
| `history` | le frasi della storia in cima alla chiave: per ogni parte (`founded` la fondazione, `caves` le grotte, `second` la seconda epoca, `fall` la sua fine, `present` gli abitanti di oggi, `crude` i cunicoli recenti) un elenco di frasi tra cui il programma ne sceglie una; `opening` (aprire con gli abitanti di oggi), `golden` (l'epoca d'oro dei fondatori) e `legend` (una leggenda finale) a volte ci sono e a volte no |

Ogni tipo in `dungeon_types` ha:

| Campo | Cosa vuol dire |
|---|---|
| `id`, `code` | il nome interno e la lettera usata nel seme |
| `menu`, `name` | il nome nella domanda sul tipo e il nome breve sulla mappa |
| `surface` | `true` se sta sopra il suolo (torre, castello…) |
| `below` | **i tipi che possono stargli direttamente sotto**: è questo che tiene coerenti i livelli |
| `eras` | quanto è probabile ogni strato nelle sue stanze: grotte naturali, fondatori, seconda epoca, oggi |
| `pattern` | la sua pianta (una delle 11 piante della tabella in alto) |
| `loops`, `portal` | quanti corridoi chiudono un anello, quanto è probabile un portale magico |
| `builders`, `built`, `titles` | chi lo costruì, cosa costruirono, il nome della mappa |
| `rooms` | le sue stanze |
| `special` | i nomi delle sue stanze chiave (la sala del trono, l'abside, il chiostro…) |
| `entrances`, `side_entrances` | gli ingressi principali, e quelli sugli altri livelli |
| `shaft_entrance` | (facoltativo) il suo ingresso per quando nessuna parete può ospitarne uno |

Ogni testo è scritto nelle due lingue, così:

```
{"it": "sala del trono", "en": "throne hall"},
```

Puoi cambiare le parole o aggiungere righe nuove copiandone una esistente. I costruttori vanno scritti al plurale (*i conti di {n}*, *il barone {n} e i suoi vassalli*), perché la storia dice "{f} costruirono…". `{n}` è il punto in cui il programma mette un nome casuale; in `history`, `{f}`, `{built}`, `{area}`, `{e1}`, `{s}`, `{e2}` e `{p}` sono i fondatori, cosa costruirono, il luogo, il primo evento, la seconda epoca, il secondo evento e gli abitanti di oggi. Gli abitanti di oggi possono essere singolari o plurali (*una setta*, *i coboldi*): nelle frasi nuove non accordarci un verbo, scrivi per esempio «chi vi scende incontra {p}». Se modifichi le frasi della storia, lo stesso seme dà ancora le stesse mappe e le stesse stanze: cambia solo il racconto.

Fai una **copia** del file prima di modificarlo. Lascia le virgolette `"`, le virgole tra le righe e le parentesi esattamente come sono: se qualcosa è fuori posto, il programma ti dice quale riga controllare (vedi il capitolo 9). Cambiare il file cambia i dungeon: lo stesso seme può dare una storia diversa da prima.

---

## 8. Per chi ha fretta: le opzioni

Invece di rispondere alle domande, puoi scrivere tutto su una riga. Quello che non indichi è scelto a caso (o chiesto, per il formato di stampa). Esempi, con l'ambiente virtuale attivo (vedi il capitolo 3):

```
python wyrmdelve.py --livelli 3 --stanze 24 --ingressi 2 --segreti 5
python wyrmdelve.py --seme 3-24-2-5-CDK-K7Q2MB --formato A3 --pdf
python wyrmdelve.py --tipo 3,4,11 --stanze 24
python wyrmdelve.py --per-livello --pdf --titolo "La Tana dell'Orco"
```

Ogni opzione ha anche un nome inglese (dopo la barra `/`), e puoi mescolarli come vuoi.

| Opzione | Cosa fa | Esempio |
|---|---|---|
| `--lingua` / `--language` | Lingua: `it` o `en` | `--lingua en` |
| `--livelli` / `--levels` | Numero di livelli, da 1 a 10 | `--livelli 3` |
| `--stanze` / `--rooms` | Numero di stanze, da 5 a 200 (almeno 5 per livello) | `--stanze 24` |
| `--ingressi` / `--entrances` | Ingressi/uscite dall'area, da 1 a 9 | `--ingressi 2` |
| `--segreti` / `--secrets` | Porte e passaggi segreti, da 0 a 60 | `--segreti 5` |
| `--tipo` / `--type` | Tipo di dungeon, da 1 a 11 come nella tabella in alto: un numero per tutti i livelli, oppure uno per livello dall'alto, separati da virgole (i livelli devono stare in un ordine coerente) | `--tipo 4` o `--tipo 3,4,11` |
| `--seme` / `--seed` | Rifà il dungeon di quel seme | `--seme 3-24-2-5-CDK-K7Q2MB` |
| `--colori` / `--colors` | 1 nero su bianco, 2 bianco su celeste, 3 bianco su nero | `--colori 2` |
| `--formato` / `--format` | Foglio: `A4`, `A3`, `A2` o `A1`; senza, il programma lo chiede | `--formato A2` |
| `--per-livello` / `--per-level` | Un livello per foglio | `--per-livello` |
| `--un-foglio` / `--one-sheet` | Tutti i livelli in un solo foglio | `--un-foglio` |
| `--pdf` / `--png` | Salva in PDF o in PNG | `--pdf` |
| `--titolo` / `--title` | Nome sulla mappa (default: uno casuale) | `--titolo "La Tana dell'Orco"` |
| `--senza-titolo` / `--no-title` | Mappa senza nome | `--senza-titolo` |
| `--senza-storia` / `--no-story` | Solo le mappe: niente chiave né PDF della storia | `--senza-storia` |
| `--unita` / `--units` | Scala della griglia: `imperiale` (1 casella = 5 ft) o `metrica` (1 casella = 1,5 m); di base metrica in italiano, imperiale in inglese | `--unita imperiale` |
| `--solo-ascii` / `--ascii-only` | Solo i caratteri della tastiera (`# ~ = o`) | `--solo-ascii` |
| `--font` | Un file di font a tua scelta (tutte le lettere devono avere la stessa larghezza) | `--font consola.ttf` |
| `--uscita` / `--output` | Cartella in cui salvare al posto di `dungeons_generated` | `--uscita mie_mappe` |

Per vedere l'elenco completo, scrivi `python wyrmdelve.py --help`.

### Limiti

Livelli 1–10, stanze 5–200 (almeno 5 per livello), ingressi 1–9, segreti 0–60. Se chiedi più segreti di quanti corridoi e collegamenti ci siano, il programma te lo dice e mette quelli che può. Alcune tecniche di Jaquays hanno bisogno di spazio: con un solo livello non ci sono collegamenti tra livelli, un sottolivello (3 stanze) richiede almeno 3 stanze in più delle 5 per livello, i livelli divisi servono livelli da almeno 6 stanze (3 per metà).

Ogni dungeon viene controllato secondo lo Xandering: ogni livello (e ogni metà di un livello diviso, e ogni sottolivello) ha almeno un anello, nessuna stanza è un vicolo cieco (ognuna si raggiunge da almeno due punti), i collegamenti tra due livelli partono da stanze diverse e due stanze non sono mai collegate due volte. La sezione di Jaquays della chiave elenca gli anelli livello per livello.

---

## 9. Problemi comuni

**"py" / "python3" non è riconosciuto come comando.**
Python non è installato, oppure su Windows non è stato aggiunto al PATH. Reinstallalo con la spunta su "Add python.exe to PATH", poi chiudi e riapri il terminale.

**"Manca la libreria Pillow".**
L'ambiente virtuale non è attivo: la riga in cui scrivi non comincia con `(.venv)`. Attivalo (passo 4 dell'installazione) e riavvia il programma. Se succede ancora, le librerie non sono ancora installate: fai il passo 5.

**"No such file or directory" / "can't open file 'wyrmdelve.py'".**
Il terminale non è aperto nella cartella con i file. Chiudilo e riaprilo come nel passo 2.

**Windows: l'attivazione dà un errore che dice che "l'esecuzione di script è disabilitata nel sistema".**
Il terminale PowerShell di Windows blocca gli script finché non li permetti. Scrivi la riga qui sotto, rispondi `S` (o `Y`), poi riattiva. Basta farlo una volta.

```
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

**macOS: `python wyrmdelve.py` dice "command not found: python".**
L'ambiente virtuale non è attivo. Su macOS il comando `python` esiste solo dentro l'ambiente virtuale (fuori c'è solo `python3`). Attivalo (passo 4) e riprova.

**macOS e Linux: `source .venv/bin/activate` dà errore, oppure la riga non comincia con `(.venv)`.**
Il tuo terminale potrebbe usare una shell meno comune, che vuole un comando di attivazione suo. Con **fish** scrivi `source .venv/bin/activate.fish`; con **csh** o **tcsh** scrivi `source .venv/bin/activate.csh`. I terminali normali di macOS (zsh) e Linux (bash) usano `source .venv/bin/activate`, come nel passo 4.

**Linux: `python3 -m venv .venv` dà un errore che parla di `ensurepip` o `venv`.**
Manca un pezzo di Python. Su Ubuntu e Debian installalo con la riga qui sotto, poi ripeti il passo 3.

```
sudo apt install python3-venv
```

**Durante l'installazione qualcosa è andato storto.**
Cancella la cartella `.venv` (è nascosta: su Windows attiva "Elementi nascosti" nel menu Visualizza, su macOS premi Cmd+Maiusc+. nel Finder) e ricomincia dal passo 3. I tuoi dungeon in `dungeons_generated` non vengono toccati.

**"Manca il file wyrmdelve_tables.json".**
Il file con le parole dei dungeon non è nella cartella. Mettilo accanto a `wyrmdelve.py`.

**"C'è un errore nel file wyrmdelve_tables.json".**
Dopo che hai modificato il file, qualcosa è fuori posto: il messaggio dice a che riga e colonna (`line 12 column 5`). Di solito è una virgola mancante tra due righe, una virgola in più dopo l'ultima riga di un elenco, o delle virgolette `"` mancanti. Correggi, oppure rimetti la copia che avevi fatto prima di modificarlo.

**"Questo seme non è valido".**
Uno dei caratteri del seme è sbagliato o manca. Confrontalo con il nome della cartella del dungeon o con la riga sotto il titolo della mappa. Deve avere sei parti separate da trattini, come `3-24-2-5-CDK-K7Q2MB` (cinque per i semi delle versioni precedenti). Se il messaggio aggiunge un motivo, come «Con 5 livelli servono almeno 25 stanze», il seme viene da una versione precedente che permetteva meno stanze per livello, quindi non si può rifare. Creane uno nuovo con gli stessi livelli e almeno 5 stanze per livello.

**"Il livello 1 (Castello) non può stare sopra il livello 2 (Torre)".**
I tipi che hai indicato con `--tipo` non si impilano in modo coerente. Cambia l'ordine o scegli altri tipi: quelli più alti vanno per primi (una torre sopra un castello, un castello sopra una cripta, l'Underdark per ultimo).

**Il programma dice "Caratteri molto piccoli".**
Il dungeon è troppo grande per il formato scelto: la mappa si stampa, ma si legge a fatica. Scegli un formato più grande (quello consigliato), oppure metti un livello per foglio.

**Alcuni simboli sono diventati lettere semplici.**
Il font installato sul tuo computer non ha quei simboli. Il programma li sostituisce da solo e te lo dice. Puoi scegliere un altro font con `--font`, per esempio `--font DejaVuSansMono.ttf`, se è installato.

**"Nessun font monospazio trovato".**
La cartella `fonts` non è accanto a `wyrmdelve.py`. Rimettila al suo posto (viene con il programma): le mappe usano il DejaVu Sans Mono che c'è dentro. In alternativa puoi indicare un altro font con tutte le lettere larghe uguali con `--font`, per esempio `--font consola.ttf`.

**Non c'è il PDF della storia.**
Il programma dice perché, in una riga che comincia con `ERRORE`, subito dopo le impostazioni e di nuovo alla fine. Controlla di aver risposto `1` (mappe e storia) a «Vuoi anche la storia del dungeon?», poi:
- **«manca la libreria fpdf2»**: con l'ambiente virtuale attivo, scrivi `pip install -r requirements.txt` (passo 5);
- **«è installata la vecchia libreria «fpdf» … al posto di «fpdf2»»**: le due librerie si pestano i piedi. Scrivi `pip uninstall -y fpdf fpdf2`, poi `pip install -r requirements.txt`;
- **«manca il font …»**: rimetti la cartella `fonts` accanto a `wyrmdelve.py`.

Le mappe e la chiave `.txt` vengono create comunque.

**La mappa stampata è più piccola del foglio, o non è centrata.**
Nelle opzioni di stampa scegli "Dimensioni effettive" o "100%", non "Adatta alla pagina".

**Il disegno dell'orco sembra tagliato a destra.**
La finestra del terminale è troppo stretta. Allargala e riavvia il programma.

**Voglio fermare il programma a metà.**
Premi **Ctrl+C**. Non si rompe niente: basta riavviarlo.

---

## Fonti

- Justin Alexander, [Xandering the Dungeon](https://thealexandrian.net/wordpress/13085/roleplaying-games/xandering-the-dungeon) (parti 1–5) e [Xandering on the Small Scale](https://thealexandrian.net/wordpress/34950/roleplaying-games/thought-of-the-day-xandering-on-the-small-scale)
- Alcune voci di `wyrmdelve_tables.json` (caratteristiche delle stanze, grotte, luoghi, nomi dei siti, minacce, guai degli insediamenti) sono tradotte e adattate da *Ironsworn* e *Ironsworn: Delve* di Shawn Tomkin ([ironswornrpg.com](https://ironswornrpg.com)), con licenza [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/); i dati sono stati letti da [Datasworn](https://github.com/rsek/datasworn). Dalla stessa fonte vengono le sillabe dei nomi di Ironsworn.
- Le sillabe e le desinenze in stile Tolkien sono statistiche di frequenza ricavate dalla lista di nomi di [Angband](https://github.com/angband/angband) (`lib/gamedata/names.txt`); la lista non è copiata.

## Licenza

WyrmDelve è software libero con licenza [GNU General Public License v3.0](LICENSE). Le parti di `wyrmdelve_tables.json` adattate da Ironsworn mantengono la loro attribuzione CC BY 4.0 (vedi Fonti qui sopra). > **I font non ricadono nella licenza GPL 3.0.** In particolare **Sebaldus-Gotisch** (© Typographer Mediengestaltung 2002, digitalizzato da Dieter Steffmann, «All rights reserved») e **Crimson Text** (SIL Open Font License 1.1) mantengono le loro condizioni; lo stesso vale per DejaVu (licenza DejaVu / Bitstream Vera). La GPL 3.0 vale per il programma e per le tabelle, non per i file della cartella `fonts/`: vedi `fonts/README.md`.
