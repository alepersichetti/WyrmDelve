# Come nasce la storia del dungeon

Questo documento spiega, con parole semplici ed esempi veri, come WyrmDelve inventa la storia di un dungeon: chi lo costruì, chi venne dopo, chi lo abita oggi, cosa si racconta di lui e cosa c'è in ogni stanza.

Tutti i testi di questo documento sono stati scritti dal programma, non a mano. Puoi rigenerarli con i semi indicati.

> Come nasce la mappa (stanze, corridoi, scale, segreti) è spiegato in un documento a parte: [dungeon_map_generation.md](dungeon_map_generation.md).

## Indice

1. [L'idea: una storia a strati](#1-lidea-una-storia-a-strati)
2. [Da dove vengono le parole](#2-da-dove-vengono-le-parole)
3. [I dadi della storia](#3-i-dadi-della-storia)
4. [Gli ingredienti](#4-gli-ingredienti)
5. [I nomi inventati](#5-i-nomi-inventati)
6. [Il racconto: le parti e la forma](#6-il-racconto-le-parti-e-la-forma)
7. [Un racconto smontato pezzo per pezzo](#7-un-racconto-smontato-pezzo-per-pezzo)
8. [Altri tre racconti, tre forme diverse](#8-altri-tre-racconti-tre-forme-diverse)
9. [Quante storie diverse?](#9-quante-storie-diverse)
10. [Gli strati](#10-gli-strati)
11. [Cosa c'è in ogni stanza](#11-cosa-cè-in-ogni-stanza)
12. [Ingressi, uscite e collegamenti](#12-ingressi-uscite-e-collegamenti)
13. [Dove finisce la storia: la chiave e il PDF](#13-dove-finisce-la-storia-la-chiave-e-il-pdf)
14. [Scrivere frasi nuove senza errori](#14-scrivere-frasi-nuove-senza-errori)
15. [I mostri](#15-i-mostri)

---

## 1. L'idea: una storia a strati

Un dungeon interessante non nasce tutto insieme. Qualcuno lo costruisce, poi lo abbandona; altri arrivano, lo riadattano, aprono nuovi passaggi; poi una catastrofe, il crollo, e oggi qualcun altro vive tra le rovine.

WyrmDelve racconta ogni dungeon così, in **quattro epoche**:

| Epoca | Sigla | Chi |
|---|---|---|
| Naturale | **N** | le grotte che c'erano già, prima di tutti |
| Prima epoca | **I** | i **fondatori**, che costruirono il dungeon |
| Seconda epoca | **II** | chi arrivò dopo la prima catastrofe |
| Terza epoca | **III** | chi lo abita **oggi**, dopo la seconda catastrofe |

Le epoche non sono solo parole: si vedono sulla mappa (muri doppi per i fondatori, singoli per la seconda epoca, `#` per grotte e terza epoca) e ogni stanza dice a quale epoca appartiene e come è cambiata nel tempo.

---

## 2. Da dove vengono le parole

Tutte le parole stanno nel file **`wyrmdelve_tables.json`**, accanto al programma. Ogni testo è scritto in italiano e in inglese:

```json
{"it": "la caduta di un meteorite", "en": "the fall of a meteorite"}
```

Il file si può modificare (vedi il capitolo 7 del README e il [capitolo 14](#14-scrivere-frasi-nuove-senza-errori) di questo documento). Ecco cosa contiene, in numeri:

| Tabella | Cosa contiene | Quanti |
|---|---|---|
| `dungeon_types` | gli 11 tipi, ognuno con i suoi fondatori, cosa costruirono, titoli, stanze, stanze speciali, ingressi | 12 fondatori, 6 costruzioni, 12–13 titoli, circa 90–107 stanze per tipo |
| `second_age` | i gruppi della seconda epoca, ognuno con le sue stanze | 35 gruppi |
| `present_day` | gli abitanti di oggi, ognuno con le sue stanze | 45 gruppi |
| `natural_rooms` | le grotte naturali | 144 |
| `events` | le catastrofi che chiudono un'epoca | 147 |
| `areas` | dove si trova il dungeon | 66 in superficie, 58 sottoterra |
| `history` | le frasi del racconto e gli elenchi da cui pescano | 97 frasi; 30 scopi, 30 reliquie, 25 visitatori |
| `name_syllables` | sillabe e desinenze per i nomi | 238 sillabe, 9 famiglie di desinenze |
| `monsters`, `clues`, `quirks` | i mostri, gli indizi nelle stanze vuote, i motivi dei mostri fuori posto | 245 mostri, 15 tipi di indizi, 11 motivi |

---

## 3. I dadi della storia

Ogni dungeon ha un **seme** (per esempio `3-21-2-4-CDK-000F62`). Con lo stesso seme esce sempre la stessa storia.

Il programma però non usa un solo sacchetto di dadi. Ricava dal seme sacchetti diversi:

- uno per gli **ingredienti** della storia e i nomi delle stanze;
- uno per la **forma e le frasi del racconto**;
- uno per i **mostri erranti**;
- uno per la **mappa**.

Per questo:

- se aggiungi o cambi frasi nel file JSON, **la mappa dello stesso seme non cambia**: cambiano solo i testi;
- le frasi del racconto non cambiano i nomi delle stanze, e viceversa.

---

## 4. Gli ingredienti

Prima di scrivere una riga, il programma sceglie gli **ingredienti**. Ecco quelli del seme `3-21-2-4-CDK-000F62` (torre, castello, Underdark):

| Ingrediente | Segnaposto | Come si sceglie | Esempio |
|---|---|---|---|
| i **fondatori** | `{f}` | uno dei 12 costruttori del tipo del **livello del suolo** (qui il castello), con un nome inventato | *i conti di Norin* |
| cosa **costruirono** | `{built}` | una costruzione per ogni tipo diverso del dungeon, unite con virgole ed "e" | *una torre, un castello e un avamposto tra le grotte* |
| **dove** | `{area}` | un luogo in superficie se almeno un livello è sopra il suolo, altrimenti un luogo sotterraneo | *tra le paludi delle lucciole* |
| la **prima catastrofe** | `{e1}` | uno dei 147 eventi | *la morte di un dio minore* |
| la **seconda epoca** | `{s}` | uno dei 35 gruppi, con un nome inventato | *i profughi di Eskrin* |
| la **seconda catastrofe** | `{e2}` | un altro evento, mai uguale al primo | *un'inondazione* |
| gli **abitanti di oggi** | `{p}` | uno dei 45 gruppi, con un nome inventato | *i bugbear di Inchalville* |
| il **titolo** | | uno dei titoli del tipo del livello del suolo, con un nome inventato | *La Cittadella di Sullenis* |

Il **livello del suolo** è quello con l'ingresso principale: il più basso tra i livelli costruiti sopra il suolo (palazzo, torre, castello, accademia, fortezza), oppure il primo livello se il dungeon è tutto sotterraneo. È lui a decidere chi sono i fondatori: in questo esempio la torre sta sopra il castello, ma i fondatori sono quelli di un castello.

Per il racconto servono anche quattro **ingredienti extra**, scelti con i dadi del racconto:

| Ingrediente | Segnaposto | Da dove | Esempio |
|---|---|---|---|
| uno **scopo** | `{goal}` | 30 scopi | *seppellire un re con tutti i suoi tesori* |
| una **reliquia** | `{relic}` | 30 reliquie | *una lampada che non si spegne mai* |
| dei **visitatori** | `{visitors}` | 25 gruppi di passaggio | *cercatori di tesori* |
| un **avventuriero scomparso** | `{hero}` | un nome inventato | *Naljormont* |

---

## 5. I nomi inventati

Ogni `{n}` nelle tabelle (per esempio *i conti di {n}*) diventa un nome inventato. Il programma lo costruisce con le sillabe del file JSON:

- 6 volte su 10: una o due sillabe più una **desinenza** di una famiglia di lingue (arabo, danese, francese antico, persiano, greco, latino, tedesco, russo, o nomi alla Tolkien);
- le altre volte: due o tre sillabe.

Il nome deve essere lungo da 3 a 12 lettere, e nello stesso dungeon non si ripete mai.

Alcuni nomi usciti dal programma:

> Vensilen · Meheqar · Zalbryn · Ulnzor · Varirniya · Cistan · Kethov · Borhard · Sabalo · Halburg · Bareul · Eirbert · Quenev

Le desinenze sono ricavate da statistiche sui nomi di quelle lingue e del gioco Angband (non ne è stato copiato il codice).

---

## 6. Il racconto: le parti e la forma

Il racconto è un paragrafo fatto di **parti**. Ogni parte ha diverse frasi possibili, tra cui il programma ne sceglie una. Le parti vanno sempre in quest'ordine:

| # | Parte | Nome nel JSON | Quando c'è | Frasi |
|---|---|---|---|---|
| 1 | **apertura** | `opening`, `opening_legend` o `opening_place` | a volte (vedi sotto) | 4 + 4 + 4 |
| 2 | la fondazione | `founded` | sempre | 7 |
| 3 | lo scopo dei fondatori | `purpose` | a volte | 5 |
| 4 | le grotte | `caves` | solo se il dungeon ha grotte naturali | 4 |
| 5 | l'epoca d'oro | `golden` | a volte | 6 |
| 6 | i presagi | `omen` | a volte | 4 |
| 7 | la seconda epoca | `second` | sempre | 6 |
| 8 | cosa fecero i nuovi arrivati | `second_detail` | a volte | 5 |
| 9 | la fine della seconda epoca | `fall` | sempre | 5 |
| 10 | l'abbandono | `aftermath` | a volte | 4 |
| 11 | la sorte dei fondatori | `fate` | a volte | 4 |
| 12 | chi passò di lì | `interlude` | a volte | 4 |
| 13 | gli abitanti di oggi | `present` | sempre, tranne se l'apertura parla già di loro | 4 |
| 14 | un dettaglio sul presente | `present_detail` | a volte | 4 |
| 15 | i cunicoli recenti | `crude` | solo se il dungeon ha stanze della terza epoca | 3 |
| 16 | **chiusura** | `legend`, `warning` o `hook` | a volte (vedi sotto) | 8 + 4 + 5 |

### L'apertura

Il programma tira un dado con cinque facce:

- 2 facce: **nessuna apertura**, il racconto comincia dalla fondazione;
- **gli abitanti di oggi** (`opening`): *«Chi vi entra oggi trova lo sciame di uomini ratto di Chalcahun, ma per capire queste sale bisogna tornare indietro di secoli.»* In questo caso la parte 13 viene saltata, perché è già stata detta;
- **una diceria** (`opening_legend`): *«L'ultima spedizione a scendere laggiù, guidata da un certo Eskmorrup, non è mai tornata; ma per capire perché bisogna partire dall'inizio.»*;
- **il luogo** (`opening_place`): *«Pochi sanno dove si trovi, e ancora meno sanno cosa nasconda.»*

### Le parti facoltative

Le otto parti "a volte" (scopo, epoca d'oro, presagi, nuovi arrivati, abbandono, sorte dei fondatori, visitatori, dettaglio sul presente) si decidono una per una: ognuna c'è **4 volte su 10**.

### La chiusura

Un dado con quattro facce:

- **nessuna chiusura**;
- **una leggenda** (`legend`): *«Si dice che nelle sale più profonde si trovi ancora un idolo d'oro.»*;
- **un avvertimento** (`warning`): *«Un vecchio detto della regione avverte: ciò che è sepolto laggiù vuole restarci.»*;
- **un aggancio per l'avventura** (`hook`): *«Ora qualcuno offre una ricompensa a chi riporterà una corona spezzata.»*

Se il racconto si apre con una diceria, non si chiude con una leggenda: sarebbero due voci di paese di fila.

### Le parti si richiamano

Gli ingredienti extra si scelgono una volta sola per dungeon, quindi più parti possono parlare della stessa cosa. La reliquia di cui si mormora all'inizio è la stessa per cui qualcuno offre una ricompensa alla fine; l'avventuriero della spedizione scomparsa è lo stesso di cui un erede cerca notizie.

### Le maiuscole

Molte frasi cominciano con un segnaposto (*«{f} vollero {built}…»*). Il programma mette la maiuscola alla prima lettera di ogni frase dopo averla riempita: *«I conti di Norin vollero…»*.

---

## 7. Un racconto smontato pezzo per pezzo

Ecco il racconto del seme `3-21-2-4-CDK-000F62`. La forma estratta è: apertura con gli abitanti di oggi, nessuna parte facoltativa tranne abbandono, sorte dei fondatori e dettaglio sul presente, chiusura con un avvertimento. Il dungeon ha grotte naturali, ma nessuna stanza della terza epoca.

| Parte | Frase scelta (con i segnaposto) | Risultato |
|---|---|---|
| apertura `opening` | I cacciatori di tesori sanno bene chi abita oggi quei corridoi: `{p}`. Pochi però ne conoscono le origini. | I cacciatori di tesori sanno bene chi abita oggi quei corridoi: *i bugbear di Inchalville*. Pochi però ne conoscono le origini. |
| fondazione | Molte generazioni fa, `{area}`, `{f}` costruirono `{built}`. | Molte generazioni fa, *tra le paludi delle lucciole*, *i conti di Norin* costruirono *una torre, un castello e un avamposto tra le grotte*. |
| grotte | Sfruttarono le grotte naturali che già si aprivano nella roccia, allargandole e collegandole alle loro sale. | (uguale) |
| seconda epoca | Con `{e1}`, i fondatori scomparvero. Al loro posto giunsero `{s}`, che aprirono nuovi passaggi e ne nascosero alcuni. | Con *la morte di un dio minore*, i fondatori scomparvero. Al loro posto giunsero *i profughi di Eskrin*, che aprirono nuovi passaggi e ne nascosero alcuni. |
| fine | Anche il loro tempo finì: con `{e2}`, quell'epoca si chiuse, e parte dei passaggi crollò. | Anche il loro tempo finì: con *un'inondazione*, quell'epoca si chiuse, e parte dei passaggi crollò. |
| abbandono | Le rovine restarono a lungo in silenzio. | (uguale) |
| sorte dei fondatori | Le ultime parole dei fondatori sono ancora incise accanto a una porta murata. | (uguale) |
| ~~abitanti di oggi~~ | | saltata: li ha già nominati l'apertura |
| dettaglio sul presente | Chi abita nei dintorni si tiene alla larga. | (uguale) |
| ~~cunicoli recenti~~ | | saltata: nessuna stanza della terza epoca |
| chiusura `warning` | Chi decide di scendere farebbe bene a portare corde, torce e un buon motivo per tornare. | (uguale) |

Il risultato, come appare nella chiave:

> I cacciatori di tesori sanno bene chi abita oggi quei corridoi: i bugbear di Inchalville. Pochi però ne conoscono le origini. Molte generazioni fa, tra le paludi delle lucciole, i conti di Norin costruirono una torre, un castello e un avamposto tra le grotte. Sfruttarono le grotte naturali che già si aprivano nella roccia, allargandole e collegandole alle loro sale. Con la morte di un dio minore, i fondatori scomparvero. Al loro posto giunsero i profughi di Eskrin, che aprirono nuovi passaggi e ne nascosero alcuni. Anche il loro tempo finì: con un'inondazione, quell'epoca si chiuse, e parte dei passaggi crollò. Le rovine restarono a lungo in silenzio. Le ultime parole dei fondatori sono ancora incise accanto a una porta murata. Chi abita nei dintorni si tiene alla larga. Chi decide di scendere farebbe bene a portare corde, torce e un buon motivo per tornare.

---

## 8. Altri tre racconti, tre forme diverse

**La forma più semplice**: nessuna apertura, nessuna parte facoltativa, nessuna chiusura. Seme `2-10-3-1-J-0GC50N` (una tomba):

> Le cronache più antiche ricordano che gli architetti dell'imperatore Pyrka costruirono una cripta sotto una foresta di funghi giganti. Dopo l'avvelenamento del capo le sale rimasero vuote; i minatori nani di Ishaud le trovarono così, le occuparono e vi aprirono passaggi tenuti nascosti. Il loro dominio non durò: dopo la perdita della pietra del cuore il luogo cadde in rovina e alcuni passaggi crollarono. I pochi tornati a raccontarlo dicono che gli abitanti di oggi sono una banda di avventurieri rivali guidata da Rosina.

**Diceria in apertura, aggancio in chiusura**, con scopo ed epoca d'oro. Seme `1-11-2-2-I-04P6X8` (una fortezza di confine):

> L'ultima spedizione a scendere laggiù, guidata da un certo Eskmorrup, non è mai tornata; ma per capire perché bisogna partire dall'inizio. Molte generazioni fa, lungo la vecchia strada imperiale, i nani guardiani di Rosir costruirono una linea fortificata. Lo fecero per custodire un segreto, o almeno così raccontano le cronache. In quegli anni le sue sale risuonavano di voci, canti e passi. Fu una crociata a cacciare i fondatori. Poco dopo arrivarono i cacciatori di streghe di Gloithette: riadattarono le vecchie sale e scavarono nuovi cunicoli, alcuni segreti. Poi un'invasione dal sottosuolo segnò la fine anche di questa epoca, e alcuni passaggi crollarono. Ora quelle sale appartengono a chi le ha prese per ultimo: gli gnoll del branco di Ethjun. Ai nuovi occupanti si devono i cunicoli più rozzi e gli ingressi più recenti. Un mercante della città vicina paga bene ogni mappa delle sue sale.

**Il luogo in apertura, leggenda in chiusura**, con presagi e un dettaglio sul presente; ci sono grotte e stanze della terza epoca, quindi compaiono anche quelle due parti. Seme `4-36-1-1-CCIK-01PANT` (torre, fortezza, Underdark):

> Sulle mappe è solo un nome, e chi vive nei dintorni preferisce non pronunciarlo. Tutto cominciò quando i mercenari di Ormia scelsero di costruire una torre, una fortezza di confine e una rete di gallerie in mezzo a una giungla. Sfruttarono le grotte naturali che già si aprivano nella roccia, allargandole e collegandole alle loro sale. Le prime crepe, nelle mura e tra la gente, comparvero presto. Quando una maledizione sulle acque pose fine al dominio dei fondatori, i goblin della tribù Griminus presero possesso del luogo e lo trasformarono, aprendo passaggi noti solo a loro. Il loro dominio non durò: dopo l'arrivo di un drago il luogo cadde in rovina e alcuni passaggi crollarono. Ora quelle sale appartengono a chi le ha prese per ultimo: i fantasmi dei minatori di Cuvar. Chi abita nei dintorni si tiene alla larga. I cunicoli più grezzi e gli ingressi più recenti risalgono a quest'ultima epoca. Si racconta che i mercenari di Ormia abbiano nascosto qualcosa nelle sale più profonde, e che nessuno l'abbia ancora trovato.

---

## 9. Quante storie diverse?

Contiamo solo la **forma**, cioè quali parti ci sono:

- aperture e chiusure: 4 aperture × 4 chiusure = 16 combinazioni, meno 1 (diceria + leggenda) = **15**;
- parti facoltative: 8 parti, ognuna c'è o non c'è = 2⁸ = **256**;
- in tutto: 15 × 256 = **3.840 forme diverse**.

Poi ogni parte ha da 3 a 8 frasi possibili: moltiplicandole si arriva a **migliaia di miliardi** di combinazioni di frasi. E ancora non abbiamo contato gli ingredienti: 12 fondatori per tipo, 147 eventi, 35 gruppi della seconda epoca, 45 abitanti di oggi, 124 luoghi, i nomi inventati… Due dungeon con la stessa storia, in pratica, non escono mai.

Il programma stesso può contare le forme: la funzione `history_patterns()` restituisce 3.840 con il file JSON attuale. Se aggiungi una parte facoltativa nuova al codice, il numero raddoppia.

---

## 10. Gli strati

Sotto il racconto, la chiave elenca gli **strati**, dal più antico:

```
STRATI (dal più antico)
  N   Grotte naturali, più antiche di ogni costruzione  [#]
  I   i conti di Norin — una torre, un castello e un avamposto tra le grotte  [═║]
  II  i profughi di Eskrin  [─│]
  III oggi: i bugbear di Inchalville  [#]
```

Tra parentesi quadre ci sono i muri con cui ogni epoca appare sulla mappa. Se un'epoca non ha stanze (per esempio niente grotte), accanto compare *(nessuna stanza)*: la storia la ricorda, ma sulla mappa non c'è.

---

## 11. Cosa c'è in ogni stanza

Ogni stanza ha una **descrizione a strati**: cosa era in origine, e cosa ne hanno fatto le epoche successive.

### Lo strato più antico

Dipende dall'epoca della stanza (decisa dalla mappa):

| Epoca della stanza | Da dove viene il nome |
|---|---|
| **N** grotta naturale | le 144 grotte naturali (*Caverna delle fumarole*) |
| **I** fondatori | le stanze del **tipo del suo livello** (*Sala dei libri volanti* in una torre) |
| **II** seconda epoca | le stanze del gruppo della seconda epoca (*Orto sotterraneo*) |
| **III** oggi | le stanze degli abitanti di oggi |

Le **stanze speciali** della pianta prendono il nome da un elenco apposito del loro tipo: la torretta d'angolo di un castello si chiama *Torre d'angolo* o *Torre della prigione*, il sepolcro di una tomba ha un nome da sepolcro, il nucleo di una torre è una *Scala del vento*.

I nomi si pescano come da un **mazzo di carte**: finché il mazzo non è finito, lo stesso nome non esce due volte. Solo quando sono usciti tutti, il mazzo si rimescola.

### Gli strati successivi

Poi il programma tira i dadi per vedere se la stanza è stata riutilizzata:

| Epoca della stanza | Riadattata nella seconda epoca | Riusata oggi |
|---|---|---|
| N grotta | 15% | 25% |
| I fondatori | 40% | 30% |
| II seconda epoca | — | 30% |
| III oggi | — | — |

Ogni strato aggiunto pesca dal mazzo di quell'epoca.

### Come si legge

```
1-04 [I] Sala delle nuvole; II: santuario improvvisato; III: recinto degli schiavi goblin.
```

- `[I]`: la stanza è dei fondatori, che la costruirono come *Sala delle nuvole*;
- `II:` nella seconda epoca diventò un *santuario improvvisato*;
- `III:` oggi è un *recinto degli schiavi goblin*.

Altri esempi dallo stesso dungeon:

```
1-02 [I] Sala dei libri volanti.
2a-01 [II] Orto sotterraneo.
3-03 [N] Grande caverna; III: dormitorio.
3-08 [N] Grotta della pietra cantante; III: sala delle trappole.
```

Il master può leggere una stanza come un piccolo scavo archeologico: cosa resta dei fondatori, cosa hanno aggiunto gli altri, cosa c'è oggi.

---

## 12. Ingressi, uscite e collegamenti

### Gli ingressi

Ogni ingresso ha una descrizione presa dal tipo del suo livello: dagli **ingressi principali** se è al livello del suolo, dagli **ingressi laterali** se è su un altro livello. Se un ingresso è un pozzo dalla superficie, il tipo può avere una descrizione apposita, altrimenti se ne usa una generica.

```
INGRESSI E USCITE
  A  porta del torrione (livello 2) → 2-01
  B  camino naturale (livello 3, ingresso a metà dungeon) → 3-05
```

### Le uscite di ogni stanza

Sotto ogni stanza, la chiave elenca **da dove si esce** e com'è il passaggio:

```
2-01 [I] Torre della prigione; III: tana dei bugbear.
       uscite: → 2-03 (apertura); → 2-02 (passaggio segreto); > scale giù → 3-02; ingresso A
```

| Testo | Significato |
|---|---|
| `→ 2-03 (porta)` | un corridoio con una porta |
| `(apertura)` | un'apertura senza porta |
| `(porta segreta)` | la porta da questa parte è segreta |
| `(passaggio segreto)` | tutto il corridoio è nascosto |
| `(allagato)`, `(crollo)`, `(gradini)` | il corridoio ha acqua, un crollo da scavalcare o dei gradini |
| `> scale giù → 3-02`, `< scale su` | una scala verso un altro livello |
| `○ pozzo → 3-08, salta un livello` | un pozzo che salta uno o più livelli |
| `Ω portale → 3-07` | un portale magico |
| `ingresso A` | da qui si esce all'aperto |

### I collegamenti tra livelli

```
COLLEGAMENTI TRA LIVELLI
  1-03   ↔ 2-03   scale
  1-02   ↔ 3-08   pozzo/camino
  1-04   ↔ 3-07   portale magico
```

Una scala, un pozzo o un portale **nascosto** è indicato come tale: i giocatori non lo vedono sulla loro mappa.

---

## 13. Dove finisce la storia: la chiave e il PDF

Se rispondi "sì" alla domanda sulla storia, il programma scrive due file con lo stesso contenuto:

- **`<seme>_key.txt`**, la chiave in testo semplice, larga 100 lettere: titolo, seme, tipo, scala, storia, strati, ingressi, collegamenti, per ogni livello la tabella dei mostri erranti e tutte le stanze, e infine la verifica dei principi di Jaquays;
- **`<seme>_story.pdf`**, la stessa chiave come un libro su pagine A4: titoli in **Sebaldus-Gotisch**, testo in **Crimson Text**, numeri delle pagine in fondo.

La lingua è quella che hai scelto all'inizio: ogni testo esiste in italiano e in inglese, e il programma prende la versione giusta.

Se rispondi "no, solo le mappe", la storia viene comunque inventata (serve per il titolo e per i nomi), ma non viene scritta.

---

## 14. Scrivere frasi nuove senza errori

Puoi aggiungere frasi a ogni parte di `history`, e voci a ogni elenco, copiando una riga esistente. Il programma pesca anche le tue. Qualche regola, perché le frasi funzionino con **qualunque** ingrediente:

| Segnaposto | Com'è fatto | Regola | Esempio giusto | Esempio sbagliato |
|---|---|---|---|---|
| `{f}` fondatori | plurale, con articolo (*i conti di Norin*, *la regina Ysa e la sua corte*) | verbo al plurale | *{f} costruirono…* | *di {f}* → «di i conti» |
| `{s}` seconda epoca | plurale, con articolo | verbo al plurale | *giunsero {s}* | *a {s}* → «a i profughi» |
| `{p}` abitanti di oggi | **singolare o plurale** (*una setta*, *i coboldi*) | niente verbi accordati con loro | *chi vi scende incontra {p}* | *oggi vi vivono {p}* → «vi vivono una setta» |
| `{e1}`, `{e2}` eventi | singolare, con articolo (*la caduta…*, *un'eclissi*) | verbo al singolare | *{e1} svuotò il luogo* | *di {e1}* → «di la caduta» |
| `{built}` | con articolo indeterminativo, anche più cose (*una torre e una cripta*) | | *costruirono {built}* | |
| `{area}` | comincia con una preposizione (*su una collina*, *nel deserto*) | usalo così com'è | *costruirono {built} {area}* | *in {area}* |
| `{goal}` | un verbo all'infinito (*custodire un segreto*) | dopo «era», «per», «a» | *il loro scopo era {goal}* | |
| `{relic}` | singolare con articolo indeterminativo (*una corona spezzata*) | dopo «a» va bene: «a una» | *attorno a {relic}* | reliquie con *il/la* |
| `{visitors}` | plurale **senza articolo** (*briganti in fuga*) | dopo il verbo | *vi passarono {visitors}* | *{visitors} vi passarono* (in italiano suona male) |
| `{hero}` | un nome proprio | dopo «di» va bene | *l'erede di {hero}* | |

La regola d'oro in italiano: **niente preposizioni davanti a un segnaposto con l'articolo determinativo**, perché il programma non sa trasformare «di i» in «dei» o «a la» in «alla».

Una frase può usare solo i segnaposto che esistono: se ne usa uno sconosciuto (o se manca l'elenco da cui pescarlo), il programma semplicemente non la sceglie. Un file JSON vecchio, con una sola frase per parte e senza le parti nuove, funziona ancora: le parti che mancano vengono saltate.

---

## 15. I mostri

All'inizio il programma chiede **cosa vuoi generare**: solo le mappe, mappe e storia, mappe e mostri, oppure tutto. Con i mostri, la chiave ha per ogni livello una **tabella d6 di mostri erranti**, e ogni stanza dice **cosa c'è dentro**: dei mostri, un indizio, oppure niente. Anche i mostri hanno dadi propri: la mappa e la storia non cambiano.

Ecco il livello 2 del seme `3-21-2-4-CDK-000F62`, con storia e mostri:

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

### La tabella dei mostri erranti

Si tira un d6 quando i personaggi fanno rumore o perdono tempo.

- **1** sono sempre **gli abitanti di oggi** (lo strato III), in giro per le sale: il dungeon è casa loro.
- **2–6** sono cinque mostri della tabella `monsters` adatti al **tipo del livello**: ragni e melme nelle grotte, non morti nelle tombe, demoni e golem nel laboratorio arcano, ronde e tagliagole in città. Ogni mostro dice dove può comparire (`where`).
- **Più si scende, più è pericoloso.** Ogni mostro ha un pericolo (`danger`) da 1 a 4: il primo livello cerca il pericolo 1, poi sale di un punto per livello fino a 4 (più piano se i livelli sono tanti). Se non bastano, il programma prende mostri di un punto sopra o sotto, poi qualunque mostro adatto al tipo.
- **Niente doppioni** tra un livello e l'altro, finché ce ne sono di nuovi.

### Le stanze: mostri, indizi, stanze vuote

Un buon dungeon non è pieno di mostri: le stanze vuote danno respiro, fanno salire la tensione e lasciano spazio all'esplorazione. Il programma fa così, livello per livello:

1. **Circa un terzo delle stanze** ha dei mostri, e **almeno un terzo resta sempre vuoto**.
2. **Gli abitanti di oggi** vivono nelle stanze della terza epoca (quelle con `III:` nella descrizione): sono le loro tane.
3. **Gli altri mostri** della tabella dei mostri erranti abitano le stanze rimaste: la tabella dice chi gira, le stanze dicono dove dorme.
4. Per **ogni stanza con mostri**, una stanza vuota vicina (collegata da un corridoio, se possibile) riceve un **indizio**: qualcosa che si vede, si sente o si annusa e fa capire che cosa c'è più avanti. L'indizio dipende dal tipo di creatura (`kind`): ossa rosicchiate per i non morti, scie viscide per le creature d'acqua, odore di zolfo per i demoni… e dice da quale stanza viene.
5. Le altre stanze sono semplicemente **vuote**.

Accanto a ogni mostro c'è **quanti** se ne incontrano (`number`): di solito 2d6 per i mostri deboli, 1d6, 1d3 e infine 1 per i più pericolosi.

### I mostri fuori posto

Un dungeon troppo ordinato è prevedibile. Per questo, **circa un livello su tre** ospita un mostro che **non c'entra** con il tipo del livello, e la chiave dice perché è lì. Il motivo nasce da ciò che il dungeon ha davvero:

| Motivo | Quando può succedere |
|---|---|
| le grotte allagate di un altro livello arrivano fin sotto la stanza, o una cisterna comunica con i fiumi sotterranei | se un altro livello ha grotte naturali e acqua; il mostro è una creatura d'acqua |
| il portale ogni tanto lascia passare qualcosa | se c'è un portale magico |
| dal livello sotto sale qualcosa a caccia | se il livello sotto è di un altro tipo; il mostro viene da lì |
| i fondatori lasciarono un guardiano | se il livello ha stanze dei fondatori; il mostro è un costrutto |
| un incantesimo andato storto ha aperto un varco | demoni ed elementali |
| gli abitanti di oggi tengono in catene ciò che catturano, o il loro capo tiene qui le sue bestie | bestie e mostri |
| una battaglia recente, un tesoro nascosto, corridoi in cui è facile perdersi | sempre |

Esempio (seme `4-42-4-2-F-003ADB`, una città di 4 livelli, livello 3):

```
  1a-01 Mostri: Serpente velenoso gigante (1d6). Fuori posto: in questi corridoi è facile perdersi,
  e non tutti trovano l'uscita.
```

È così che può comparire, per esempio, un **aboleth nella vasca di un castello**, risalito dalle grotte allagate del livello sotto. Il mostro fuori posto prende anche l'ultimo posto della tabella d6 del suo livello, con un rimando alla sua stanza.

### Da dove vengono i mostri

L'elenco di 245 mostri è stato ricavato confrontando due bestiari, *OSR Bestiary* (bucolian) e il *Monstrous Bestiary* di *Aketon* (Reese Surles), ed eliminando i doppioni: per esempio il *Ruster* di Aketon è il mostro della ruggine, il *Gel Cube* è il cubo gelatinoso, il *Landshark* è la bulette. I due bestiari non hanno una licenza aperta, quindi da loro vengono solo i nomi delle creature e i Dadi Vita (usati per il pericolo): **tutte le descrizioni sono scritte per WyrmDelve**. L'aboleth viene dall'SRD 5.1 (CC BY 4.0). Sono stati tolti i mostri con nomi registrati da altri, i signori dei demoni con un nome proprio e gli animali che in un dungeon non hanno senso (balene, cavalli, dinosauri…).

Per aggiungere mostri, indizi e motivi: [add_monsters_to_bestiary.md](add_monsters_to_bestiary.md).
