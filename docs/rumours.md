# Come nascono le dicerie

*[English version](rumours.en.md)*

Questo documento spiega come WyrmDelve prepara la tabella delle dicerie: le voci, vere e false, che gli avventurieri sentono sul dungeon prima di entrarci, con esempi veri fatti dal programma.

> Le dicerie compaiono solo se all'inizio, a «Cosa vuoi generare?», segni anche le **dicerie** (o `--contenuto dicerie`, anche insieme ad altro: `--contenuto tesori,png,dicerie`; vanno bene anche `voci` e `rumour`). Di cosa parlano dipende da cos'altro hai scelto: vedi il capitolo 3.

## Indice

1. [L'idea: una tabella per l'arbitro](#1-lidea-una-tabella-per-larbitro)
2. [Quante sono, quante vere](#2-quante-sono-quante-vere)
3. [Di cosa parlano](#3-di-cosa-parlano)
4. [Come il programma sa se una diceria è vera](#4-come-il-programma-sa-se-una-diceria-è-vera)
5. [Chi le racconta](#5-chi-le-racconta)
6. [Quante dicerie diverse](#6-quante-dicerie-diverse)
7. [Nella chiave](#7-nella-chiave)
8. [Un esempio completo](#8-un-esempio-completo)
9. [Cambiare le tabelle](#9-cambiare-le-tabelle)

---

## 1. L'idea: una tabella per l'arbitro

Prima di scendere, gli avventurieri chiedono in giro: all'osteria, al villaggio, a chi li ingaggia. L'arbitro tira sulla tabella delle dicerie e racconta quello che esce. Alcune voci sono vere e aiutano davvero (un tesoro in una certa sala, il segreto di un PNG); altre sono false e possono costare care. Nella chiave ogni diceria è segnata **vera** o **falsa**: lo sa solo l'arbitro.

Le dicerie vengono **dopo** tutto il resto e usano dadi propri (fatti dal seme con l'etichetta `rumours`): la mappa, la storia, i mostri, le trappole, i tesori, le fazioni e i PNG di un seme non cambiano se scegli le dicerie o no.

---

## 2. Quante sono, quante vere

La tabella è da **d8**, con due dicerie in più (d10) se il dungeon ha almeno 14 stanze e altre due (d12) se ha almeno 3 livelli principali.

Circa **un terzo** delle dicerie è falso: un terzo della tabella, arrotondato per difetto, più una una volta su due. Una tabella da d12 ha 4 o 5 dicerie false, una da d8 ne ha 2 o 3. Le vere e le false sono mescolate a caso.

---

## 3. Di cosa parlano

| Argomento | Quando | Esempio |
|---|---|---|
| la **storia** | sempre | «Il medico del villaggio, ripulendo i ferri, osserva: prima di tutto vennero i minatori di Beard; poi la scomparsa del dio protettore spazzò via la loro epoca.» |
| quanti **livelli** | sempre, al massimo una diceria | «Chi è sceso fino in fondo ha contato cinque livelli.» |
| quanti **ingressi** | sempre, al massimo una diceria | «Anyone who wants to get in has two entrances to choose from.» |
| un **tesoro** | se hai scelto i tesori | «Nella sala 1-04 nessuno pensa di guardare bene, eppure c'è un tesoro sparso tra i rifiuti e le ossa.» |
| dove sta un **PNG** | se hai scelto i PNG | «La via per arrivare a Dethanezad finisce nella sala 1-06, e non è una via comoda.» |
| il **segreto** di un PNG | se hai scelto i PNG | «Non lasciatevi ingannare dai modi di Kaelpraah: ha rubato nome e vestiti a un compagno morto: nessuno conosce il suo vero volto.» |
| dove sta una **fazione** | se hai scelto le fazioni | «Se cercate il Silenzio di Esnar, guardate nella sala 3-01.» |
| il **segreto** di una fazione | se hai scelto le fazioni | «C'è un motivo se il Giuramento di Thalkorglo non si fida di nessuno: il nome che porta è rubato: apparteneva ai nemici giurati dei fondatori.» |

Gli argomenti sono pescati da un mazzo in cui la storia conta tre volte, i tesori due, i segreti di PNG e fazioni due: così una tabella mescola un po' di tutto. Lo stesso tesoro, PNG o fazione non torna in due dicerie dello stesso tipo.

---

## 4. Come il programma sa se una diceria è vera

Le frasi sulla **storia** sono scritte già vere o già false: le vere dicono solo cose che valgono in ogni dungeon (chi lo costruì, cosa chiuse ogni epoca, chi ci vive oggi, la leggenda della reliquia e dell'eroe scomparso); le false scambiano le epoche, negano i fatti o inventano certezze («l'eroe è tornato ricco e vive in città»).

Tutte le altre frasi sono **neutre**: diventano vere o false secondo i fatti con cui il programma le riempie.

| Argomento | Vera | Falsa |
|---|---|---|
| tesoro | una sala che ha davvero un tesoro, con il suo nascondiglio e il suo valore (arrotondato, come fanno le voci) | una sala senza tesoro, con un nascondiglio e un valore inventati |
| dove sta un PNG o una fazione | la sua vera stanza | un'altra stanza |
| segreto di un PNG o di una fazione | il suo vero segreto (lo stesso della sua sezione nella chiave) | un segreto della tabella che non ha |
| livelli, ingressi | il numero vero | un numero vicino ma sbagliato |

Una diceria vera su un segreto è possibile solo per chi ha un segreto; una sul valore di un tesoro solo se il tesoro vale almeno 10 monete d'oro (altrimenti la frase sceglie il nascondiglio).

---

## 5. Chi le racconta

Una diceria su due comincia con **chi la racconta**: «Un vecchio minatore giura:», «L'oste, asciugando un boccale che resta sempre sporco, sostiene:», «Un erborista dalle dita verdi assicura:». Le altre sono la voce da sola. La fonte non dice nulla sulla verità: anche il bambino scalzo può avere ragione.

---

## 6. Quante dicerie diverse

**Contenuto.** Le affermazioni sono 209 (42 vere e 42 false sulla storia, 30 sui tesori, 18 + 17 sui PNG, 17 + 17 sulle fazioni, 13 sui livelli, 13 sugli ingressi), e ognuna può essere detta da una delle 78 fonti o da nessuna: 209 × 79 = **16.511** dicerie diverse, senza contare i fatti con cui sono riempite (stanze, nomi, segreti, nascondigli, valori, le parole della storia). Una tabella da d8 ne mette insieme 8: più di 10²⁹ tabelle diverse.

**Forma.** Ogni diceria ha 2 forme (con o senza fonte), e le false possono stare in qualunque posizione: una tabella da d8 ha 2⁸ × (28 + 56) = **21.504** forme, una da d10 **337.920**, una da d12 **5.271.552**.

---

## 7. Nella chiave

Le dicerie hanno una sezione loro, **DICERIE**, dopo i PNG e prima degli ingressi; nel PDF è un capitolo con il numero in grassetto e «vera» o «falsa» in corsivo:

```
DICERIE
  Tira 1d12 per ogni diceria che gli avventurieri sentono prima di entrare (in taverna, al
  villaggio, da chi li ingaggia). Solo l'arbitro sa quali sono vere.
    1. [falsa] Chi è sceso fino in fondo ha contato cinque livelli.
    …
```

Mentre genera, il programma dice com'è fatta la tabella: `Dicerie: d12, 7 vere e 5 false`.

---

## 8. Un esempio completo

Seme `4-30-4-3-K-ZZT0P1`, con tutto: 4 livelli, 30 stanze, quindi una tabella da d12. È lo stesso dungeon degli esempi di [factions.md](factions.md) e [npcs.md](npcs.md).

| d12 | | Diceria | Perché |
|---|---|---|---|
| 1 | falsa | Chi è sceso fino in fondo ha contato cinque livelli. | i livelli sono 4 |
| 2 | falsa | L'oste, asciugando un boccale che resta sempre sporco, sostiene: prima degli attuali abitanti, gli uomini fungo di Balabad, laggiù non c'era mai stato nessuno. | storia falsa: prima c'erano i minatori di Beard e gli hobgoblin |
| 3 | vera | Nella sala 1-04 nessuno pensa di guardare bene, eppure c'è un tesoro sparso tra i rifiuti e le ossa. | la sala 1-04 ha un tesoro da 4.600 mo, proprio lì |
| 4 | vera | Se cercate il Silenzio di Esnar, guardate nella sala 3-01. | è la sua base |
| 5 | falsa | Non lasciatevi ingannare dai modi di Kaelpraah: ha rubato nome e vestiti a un compagno morto: nessuno conosce il suo vero volto. | non è il segreto di Kaelpraah |
| 6 | vera | Il medico del villaggio, ripulendo i ferri, osserva: prima di tutto vennero i minatori di Beard; poi la scomparsa del dio protettore spazzò via la loro epoca. | storia vera |
| 7 | falsa | Tuville risuola scarpe in città da vent'anni, e di quella discesa non vuole sentir parlare. | l'eroe scomparso non è mai tornato |
| 8 | vera | La via per arrivare a Dethanezad finisce nella sala 1-06, e non è una via comoda. | Dethanezad sta nella 1-06 |
| 9 | vera | Un disertore con una cicatrice sul collo confessa: prima di fidarvi di Ithvexnar, sappiate questo: fu una sua lettera a indicare ai padroni attuali, gli uomini fungo di Balabad, la strada per questo luogo. | è il segreto di Ithvexnar |
| 10 | vera | C'è un motivo se il Giuramento di Thalkorglo non si fida di nessuno: il nome che porta è rubato: apparteneva ai nemici giurati dei fondatori. | è il segreto del Giuramento |
| 11 | vera | Un erborista dalle dita verdi assicura: per chi ha a che fare con il Silenzio di Esnar, una sola cosa conta: ha già trovato un'arpa che suona da sola, ma ne ha paura, e finge di cercare ancora. | è il segreto del Silenzio |
| 12 | falsa | Nella sala 2-01 c'è un tesoro in un'urna sigillata con la cera: 2.700 monete d'oro, a sentire chi l'ha visto. | la sala 2-01 non ha tesori |

Si vede che una tabella così dà agli avventurieri due piste vere verso un tesoro e i PNG, svela tre segreti (utili per trattare con il Silenzio, il Giuramento e Ithvexnar) e tende due trappole: la sala 2-01 e la falsa colpa di Kaelpraah.

---

## 9. Cambiare le tabelle

Tutto è in `data/rumours.json`. Fai una copia del file prima di modificarlo.

| Voce | Cosa contiene | Segnaposti |
|---|---|---|
| `sources` | chi racconta la diceria, senza punteggiatura finale (il programma aggiunge «:») | quelli della storia |
| `history_true`, `history_false` | affermazioni vere e false sulla storia | quelli della storia |
| `treasure` | un tesoro in una sala | `{room}` e `{where}` (il nascondiglio) o `{value}` («2.700 monete d'oro») |
| `npc_room`, `faction_room` | dove sta un PNG, una fazione | `{npc}` o `{faction}`, e `{room}` |
| `npc_secret`, `faction_secret` | il segreto di un PNG, di una fazione | `{npc}` o `{faction}`, e alla fine `: {secret}` |
| `levels`, `entrances` | quanti livelli, quanti ingressi | `{levels}` («quattro livelli», «un solo livello»), `{entrances}` («due ingressi», «un solo ingresso») |

I segnaposti della storia sono quelli delle fazioni (vedi [factions.md](factions.md#4-le-frasi-di-una-fazione)). Una frase:

```json
{"it": "Se cercate {faction}, guardate nella sala {room}.", "en": "If you are looking for {faction}, look in room {room}."}
```

Le regole per l'italiano sono quelle delle fazioni (vedi [factions.md](factions.md#9-cambiare-le-tabelle)); in più, nessuna parola si accorda con `{npc}`, `{levels}` o `{entrances}`, e le frasi di `history_true` devono essere vere in **qualunque** dungeon: niente su dove sta la reliquia o se l'eroe è morto.

Se `data/rumours.json` manca o ha un errore, il programma lo dice e fa il dungeon senza dicerie.
