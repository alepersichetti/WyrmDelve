# Come nascono le fazioni

*[English version](factions.en.md)*

Questo documento spiega come WyrmDelve inventa i gruppi che si contendono il dungeon: quanti sono, da dove vengono, dove stanno, cosa vogliono e cosa pensano l'uno dell'altro, con esempi veri fatti dal programma.

> Le fazioni compaiono solo se all'inizio, a «Cosa vuoi generare?», segni anche le **fazioni** (o `--contenuto fazioni`, anche insieme ad altro: `--contenuto storia,fazioni`). La storia del luogo, da cui nascono, è spiegata in [story_generation_algorithm.md](story_generation_algorithm.md).

## Indice

1. [L'idea: ogni fazione nasce dalla storia](#1-lidea-ogni-fazione-nasce-dalla-storia)
2. [Quante sono e da dove vengono](#2-quante-sono-e-da-dove-vengono)
3. [Il nome e la base](#3-il-nome-e-la-base)
4. [Le frasi di una fazione](#4-le-frasi-di-una-fazione)
5. [I rapporti tra le fazioni](#5-i-rapporti-tra-le-fazioni)
6. [Quante fazioni diverse](#6-quante-fazioni-diverse)
7. [Nella chiave](#7-nella-chiave)
8. [Un esempio completo](#8-un-esempio-completo)
9. [Cambiare le tabelle](#9-cambiare-le-tabelle)

---

## 1. L'idea: ogni fazione nasce dalla storia

Ogni dungeon di WyrmDelve ha una storia a strati: i **fondatori** che lo costruirono, chi arrivò nella **seconda epoca**, gli **abitanti di oggi**, gli eventi che chiusero ogni epoca, una **reliquia** della leggenda e un **eroe** scomparso. Le fazioni sono i gruppi che oggi si muovono tra quelle rovine, e ognuna è legata a un pezzo di quella storia: le sue frasi usano gli stessi nomi della storia, così il giocatore che ha letto della «scomparsa dei bambini» o del «seme di un albero estinto» li ritrova nelle mire delle fazioni.

Le fazioni vengono **dopo** tutto il resto e usano dadi propri (fatti dal seme con l'etichetta `factions`): la mappa, la storia, i mostri, le trappole e i tesori di un seme non cambiano se scegli le fazioni o no.

---

## 2. Quante sono e da dove vengono

Le fazioni sono **da 2 a 4**: 2 di base, una in più se il dungeon ha almeno 14 stanze, un'altra se ha almeno 3 livelli principali.

Ogni fazione ha un'**origine**, cioè il pezzo di storia da cui nasce:

| Origine | Chi sono | Esempio |
|---|---|---|
| `present` | gruppi che vivono con gli **abitanti di oggi**: li servono, li pagano, li spiano o vogliono cacciarli | «Serve i ghoul del branco di Thalmorn come corte e come scudo, in cambio delle briciole del bottino.» |
| `heirs` | gli **eredi dei fondatori**, che ne custodiscono i riti o vogliono riprendersi il luogo | «Tiene in vita, in segreto, i riti e la lingua che i custodi delle stelle di Belir portarono quaggiù.» |
| `second` | gli ultimi della **seconda epoca**, o chi ne imita i costumi | «Venera come santi i vecchi padroni del luogo, i legionari hobgoblin di Wyria, e ne conserva le ossa nella sala 1-05.» |
| `relic` | chi cerca la **reliquia** della leggenda | «Nacque attorno a una profezia: chi possiederà un seme di un albero estinto regnerà su tutto il sottosuolo.» |
| `outsiders` | **estranei** venuti da fuori: paesani, studiosi, cacciatori di tesori | «I suoi membri vengono dal villaggio più vicino, stanchi di pagare tributi e di contare i dispersi.» |

C'è **sempre** una fazione `present`, perché gli abitanti di oggi sono il centro del dungeon; le altre origini sono pescate a caso, senza ripetersi.

---

## 3. Il nome e la base

**Il nome.** È una parola che dice che tipo di gruppo è, più un nome inventato con le stesse sillabe dei luoghi e delle persone: *il Covo di Peldi*, *la Chiesa di Bekthalra*, *l'Accademia di Junippos*. Ogni nome è adatto solo ad alcune origini: un «Covo» può essere `present` o `second`, un'«Accademia» solo `outsiders` o `relic`, e così via.

**La base.** Ogni fazione ha una stanza sua, scelta tra quelle della sua epoca:

| Origine | Dove sta |
|---|---|
| `present` | una stanza degli abitanti di oggi (strato III) |
| `heirs` | una stanza dei fondatori (strato I) |
| `second` | una stanza della seconda epoca (strato II) |
| `relic` | una stanza qualsiasi |
| `outsiders` | una delle tre stanze più vicine a un ingresso, oppure (una volta su due) **fuori dal dungeon** |

Due fazioni non hanno mai la stessa base. Se mancano stanze della sua epoca, la fazione ne prende un'altra libera. Alcune frasi nominano la base («ne conserva le ossa nella sala 1-05») o hanno senso solo per chi vive nel dungeon («Pattuglia i corridoi a coppie…», «…lontani dalle sue sale»): una fazione che sta fuori dal dungeon non pesca mai quelle frasi, e un rapporto di questo tipo («si contendono un corridoio») lega solo due fazioni che stanno entrambe dentro.

---

## 4. Le frasi di una fazione

Ogni fazione è un paragrafo di frasi, pescate da `data/factions.json`:

1. **da dove viene** (`origins`): sempre per prima;
2. **cosa vuole** (`goals`), **come lo ottiene** (`methods`) e, 7 volte su 10, **chi la guida** (`leaders`): queste tre in ordine casuale;
3. 6 volte su 10, **un segreto** (`secrets`): una verità che i giocatori possono scoprire; nella chiave comincia con «Segreto:», perché l'arbitro lo riconosca subito;
4. **come tratta gli avventurieri** (`attitudes`);
5. **cosa pensa di un'altra fazione** (`relations`), se ce n'è un'altra (vedi il capitolo 5).

Le frasi hanno dei segnaposti tra graffe, riempiti con le parole del dungeon:

| Segnaposto | Cosa diventa | Esempio |
|---|---|---|
| `{f}`, `{s}`, `{p}` | i fondatori, quelli della seconda epoca, gli abitanti di oggi | *i ghoul del branco di Thalmorn* |
| `{e1}`, `{e2}` | gli eventi che chiusero le due epoche | *la scomparsa dei bambini* |
| `{built}`, `{area}`, `{title}` | cosa fu costruito, dove, il nome del luogo | *una torre di guardia* |
| `{relic}`, `{hero}`, `{goal}`, `{visitors}` | la reliquia, l'eroe scomparso, lo scopo dei fondatori, chi passò di lì | *un seme di un albero estinto*, *Dubiiya* |
| `{faction}`, `{other}` | il nome della fazione e quello dell'altra fazione | *il Covo di Peldi* |
| `{leader}` | il nome del capo, inventato | *Duncalme* |
| `{room}` | la stanza della base | *1-05* |

Alcune origini `present` dicono che la fazione **serve** gli abitanti di oggi («Serve … come corte e come scudo»): queste hanno `"leader": false` e la fazione non ha un capo suo, perché il suo capo è quello degli abitanti di oggi.

Il mazzo di ogni tabella si mescola una volta per dungeon: due fazioni dello stesso dungeon non hanno mai lo stesso scopo, metodo, capo, segreto o atteggiamento.

---

## 5. I rapporti tra le fazioni

Le fazioni sono legate in **cerchio**: la prima ha un'opinione sulla seconda, la seconda sulla terza, e l'ultima sulla prima. Con due fazioni c'è un solo rapporto, dalla prima alla seconda. Un rapporto può essere un'alleanza, una tregua, un debito, un tradimento in arrivo:

> Pur di avere un seme di un albero estinto, il Patto di Dratuchal tradirebbe la Chiesa di Bekthalra senza pensarci due volte.

Così ogni fazione ha almeno un legame con un'altra, e l'arbitro ha sempre una leva per mettere i gruppi l'uno contro l'altro.

---

## 6. Quante fazioni diverse

**Contenuto.** Moltiplicando le scelte possibili per una fazione:

| Parte | Scelte |
|---|---|
| nome | 44 |
| origine, con o senza uno dei 24 capi | 65 origini × 25 + 2 origini senza capo = 1.627 |
| scopo | 37 |
| metodo | 32 |
| segreto, o nessuno | 29 + 1 = 30 |
| atteggiamento | 19 |

44 × 1.627 × 37 × 32 × 30 × 19 = **48.313.309.440** fazioni diverse, senza contare i nomi inventati, i rapporti (20) e le parole della storia che cambiano in ogni dungeon.

**Forma.** Scopo, metodo e capo in ordine casuale danno 6 ordini con il capo e 2 senza; con o senza segreto: (6 + 2) × 2 = **16 forme** del paragrafo.

---

## 7. Nella chiave

Le fazioni hanno una sezione loro, **FAZIONI**, dopo la storia e gli strati e prima degli ingressi; nel PDF è un capitolo con il nome di ogni fazione in grassetto:

```
FAZIONI
  Il Covo di Peldi (base: 1a-02)
    Serve i ghoul del branco di Thalmorn come corte e come scudo, in cambio delle briciole del
    bottino. Ha giurato di vendicare Dubiiya, e ha già deciso chi incolpare. …
```

Mentre genera, il programma dice quante fazioni ha creato: `Fazioni: 3 (Il Covo di Peldi, Il Patto di Dratuchal e La Chiesa di Bekthalra)`.

Le fazioni non compaiono sulle mappe: sono solo nella chiave.

---

## 8. Un esempio completo

Seme `2-14-2-1-C-02SFP3`: una torre di guardia a due livelli con il sottolivello 1a. La sua storia: gli eremiti di Lumjorthor la costruirono ai piedi di un vulcano; il risveglio del vulcano la svuotò; i legionari hobgoblin di Wyria se ne impadronirono finché la scomparsa dei bambini non chiuse la loro epoca; oggi ci vivono i ghoul del branco di Thalmorn. Le 14 stanze danno 3 fazioni:

> **Il Covo di Peldi (base: 1a-02)**
> Serve i ghoul del branco di Thalmorn come corte e come scudo, in cambio delle briciole del bottino. Ha giurato di vendicare Dubiiya, e ha già deciso chi incolpare. Pattuglia i corridoi a coppie, con lanterne schermate e un fischietto d'osso. Segreto: il suo oro è falso: piombo dorato, coniato in un'officina nascosta nella sala 1a-02. Mette una taglia su ogni avventuriero che non si presenta prima al suo capo. Per anni il Covo di Peldi ha creduto che il Patto di Dratuchal fosse dalla sua parte; il tradimento è vicino, e nessuno se lo aspetta.
>
> **Il Patto di Dratuchal (base: 1-05)**
> Venera come santi i vecchi padroni del luogo, i legionari hobgoblin di Wyria, e ne conserva le ossa nella sala 1-05. Avvelena i pozzi e le cisterne che non usa, e lascia sul bordo un teschio dipinto di blu. Cerca Dubiiya, o ciò che ne resta, e soprattutto la mappa che Dubiiya portava con sé. Ne regge le sorti Duncalme, che porta sempre con sé il diario di Dubiiya e lo cita come un libro sacro. Chiede un pedaggio di dieci monete d'argento a testa, poi lascia passare senza domande. Pur di avere un seme di un albero estinto, il Patto di Dratuchal tradirebbe la Chiesa di Bekthalra senza pensarci due volte.
>
> **La Chiesa di Bekthalra (base: 2-01)**
> Possiede l'unico disegno fedele che ritrae un seme di un albero estinto, e lo mostra solo a chi ha giurato. Chi comanda oggi è Bahal, che uccise il capo precedente durante un banchetto e lo ricorda a tutti a ogni pasto. Mira a fare del luogo un mercato sotterraneo, con i ghoul del branco di Thalmorn a fare la guardia dietro compenso. Fa la guerra con il fuoco: barili di pece, torce e fumo per stanare chi si nasconde. Segreto: quasi tutti i suoi membri sono fantocci di paglia vestiti e armati: in carne e ossa sono in quattro. Teme gli avventurieri e fugge, ma ne annota i nomi e le armi. Ogni volta che il Covo di Peldi perde un membro, la Chiesa di Bekthalra ne guadagna uno: i disertori cambiano sempre parte nello stesso verso.

Si vede che:

- **il Covo** è la fazione `present`: serve i ghoul, quindi non ha un capo suo, e il suo segreto è nascosto proprio nella sua base;
- **il Patto** è `second`: venera gli hobgoblin della seconda epoca e tiene la base in una loro sala; cerca l'eroe scomparso della storia;
- **la Chiesa** è `relic`: tutto ruota attorno al seme di un albero estinto, la reliquia della leggenda;
- i rapporti formano un cerchio: il Covo si fida del Patto, che lo tradirà; il Patto tradirebbe la Chiesa; la Chiesa ruba membri al Covo.

---

## 9. Cambiare le tabelle

Tutto è in `data/factions.json`. Fai una copia del file prima di modificarlo.

| Voce | Cosa contiene |
|---|---|
| `names` | i nomi: `it` e `en` con `{n}` al posto del nome inventato, e `origins`, le origini a cui il nome si adatta |
| `origins` | da dove viene una fazione, per ogni origine: `present` (usa `{p}`), `heirs` (`{f}`), `second` (`{s}`), `relic` (`{relic}`), `outsiders`; `"leader": false` per chi serve gli abitanti di oggi |
| `goals`, `methods` | cosa vuole e come lo ottiene |
| `leaders` | chi la guida (usa `{leader}`) |
| `secrets` | i segreti |
| `attitudes` | come tratta gli avventurieri |
| `relations` | cosa pensa di un'altra fazione (usa `{faction}` e `{other}`) |

Ogni frase può avere, accanto a `it` e `en`, delle condizioni:

| Condizione | Cosa vuol dire |
|---|---|
| `"inside": true` | solo per una fazione con la base nel dungeon (per un rapporto: tutte e due le fazioni) |
| `"not": ["outsiders"]` | non per queste origini (qui: non per gli estranei, che per esempio non conoscono la lingua dei fondatori) |
| `"leader": false` | solo nelle origini: la fazione non ha un capo suo |

Un nome e una frase:

```json
{"it": "l'Ordine di {n}", "en": "the Order of {n}", "origins": ["heirs", "relic", "outsiders"]}
{"it": "Vuole recuperare {relic} prima di chiunque altro.", "en": "It wants to recover {relic} before anyone else does."}
{"it": "Pattuglia i corridoi a coppie, …", "en": "It patrols the corridors in pairs, …", "inside": true}
```

Qualche regola per l'italiano, perché le frasi stiano in piedi con qualunque parola:

- i nomi delle fazioni cominciano con l'articolo minuscolo (`il`, `la`, `l'`…): il programma mette la maiuscola quando serve;
- niente `di`, `a`, `da`, `in`, `su` davanti a un segnaposto che ha già l'articolo (`{faction}`, `{p}`, `{relic}`…): «i nemici di {faction}» diventerebbe «i nemici di il Covo di Peldi»; meglio «i nemici: {faction}…» o girare la frase;
- niente aggettivi o participi che si accordano con un segnaposto: la fazione può essere maschile o femminile, singolare o plurale;
- una frase non comincia con `{faction}` o `{other}`.

In inglese, niente *he* o *she*: i capi possono essere chiunque.

Se `data/factions.json` manca o ha un errore, il programma lo dice e fa il dungeon senza fazioni.
