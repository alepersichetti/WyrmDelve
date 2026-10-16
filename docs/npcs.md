# Come nascono i PNG

*[English version](npcs.en.md)*

Questo documento spiega come WyrmDelve inventa i personaggi non giocanti (PNG) che gli avventurieri possono incontrare nel dungeon: quanti sono, chi sono, come sono legati alla storia del luogo e alle fazioni, dove stanno e cosa vogliono, con esempi veri fatti dal programma.

> I PNG compaiono solo se all'inizio, a «Cosa vuoi generare?», segni anche i **PNG** (o `--contenuto png`, anche insieme ad altro: `--contenuto fazioni,png`). La storia del luogo è spiegata in [story_generation_algorithm.md](story_generation_algorithm.md), le fazioni in [factions.md](factions.md).

## Indice

1. [L'idea: persone con un motivo per essere lì](#1-lidea-persone-con-un-motivo-per-essere-lì)
2. [Quanti sono e chi sono](#2-quanti-sono-e-chi-sono)
3. [Nome, genere, ruolo e stanza](#3-nome-genere-ruolo-e-stanza)
4. [Le frasi di un PNG](#4-le-frasi-di-un-png)
5. [I rapporti tra i PNG](#5-i-rapporti-tra-i-png)
6. [Quanti PNG diversi](#6-quanti-png-diversi)
7. [Nella chiave](#7-nella-chiave)
8. [Un esempio completo](#8-un-esempio-completo)
9. [Cambiare le tabelle](#9-cambiare-le-tabelle)

---

## 1. L'idea: persone con un motivo per essere lì

Un PNG di WyrmDelve non è un incontro a caso: è nel dungeon **per qualcosa che riguarda il luogo**. Discende dai fondatori, serve gli abitanti di oggi, cerca la reliquia della leggenda, è venuto a sapere cosa accadde all'eroe scomparso, oppure fa parte di una delle fazioni. Le sue frasi usano gli stessi nomi della storia e delle fazioni, così l'arbitro ha in mano una rete di persone che si conoscono, si odiano e si devono favori.

I PNG vengono **dopo** tutto il resto e usano dadi propri (fatti dal seme con l'etichetta `npcs`): la mappa, la storia, i mostri, le trappole, i tesori e le fazioni di un seme non cambiano se scegli i PNG o no.

---

## 2. Quanti sono e chi sono

I PNG sono **da 3 a 5**: 3 di base, uno in più se il dungeon ha almeno 14 stanze, un altro se ha almeno 3 livelli principali.

Se hai scelto anche le **fazioni**, alcuni PNG ne fanno parte: al massimo tutti tranne due, almeno uno, e mai più delle fazioni. Ognuno di questi appartiene a una fazione diversa e, una volta su due, ne è il **capo**, se la fazione ne ha uno con un nome: allora ha proprio il nome del capo che compare tra le fazioni.

Gli altri PNG sono **solitari**, ognuno legato a un pezzo diverso della storia:

| Tipo | Chi sono | Esempio |
|---|---|---|
| `present` | legati agli **abitanti di oggi**: li servono, li venerano, ne sono prigionieri | «Venera gli uomini fungo di Balabad come dei viventi, e lascia offerte che nessuno ha mai chiesto.» |
| `heirs` | legati ai **fondatori**: ne discendono, ne custodiscono la memoria | «Restaura da anni, una lettera alla volta, le iscrizioni che i minatori di Beard incisero sui muri.» |
| `second` | legati a quelli della **seconda epoca** | «Sua nonna era tra gli hobgoblin mercanti di schiavi di Leebek e, a sentire i vecchi, fu proprio lei a scatenare una crociata.» |
| `relic` | attirati dalla **reliquia** | «She heard in a tavern that a seed from an extinct tree cures every ailment, and has a sick daughter at home.» |
| `outsiders` | venuti **da fuori**: dal villaggio, dalla città, da una spedizione fallita | «Insegue un debitore che è scappato laggiù con la cassa di una confraternita.» |
| `member` | **membri** di una fazione | «Ha scelto il Silenzio di Esnar perché era l'unica fazione che offrisse un pasto caldo.» |
| `leader` | **capi** di una fazione | «Fu eletta per acclamazione, e ora guida il Branco di Rinu senza sapere bene come si faccia.» |

I tipi dei solitari sono pescati a caso, senza ripetersi.

---

## 3. Nome, genere, ruolo e stanza

**Il nome** è inventato con le stesse sillabe dei luoghi e delle persone, e non è mai quello dell'eroe scomparso, di un capo di fazione (tranne quando il PNG è proprio quel capo) o di un altro PNG.

**Il genere** è tirato a caso per ogni PNG: decide le desinenze in italiano («innamorata», «riconosciuto») e i pronomi in inglese (*he*, *she*).

**Il ruolo** dice che mestiere fa o che cosa è: *vecchia maestra d'armi*, *acchiappatopi*, *negromante alle prime armi*, *servo dei mostri*. Ogni ruolo è adatto solo ad alcuni tipi.

**La stanza:**

| Tipo | Dove sta |
|---|---|
| `member`, `leader` | nella base della sua fazione (fuori dal dungeon, se la fazione sta fuori) |
| `present` | in una stanza degli abitanti di oggi (strato III) |
| `heirs` | in una stanza dei fondatori (strato I) |
| `second` | in una stanza della seconda epoca (strato II) |
| `relic` | in una stanza qualsiasi |
| `outsiders` | in una delle tre stanze più vicine a un ingresso, oppure (una volta su tre) **fuori dal dungeon** |

I solitari non stanno mai nella stessa stanza tra loro, né nella base di una fazione. Un PNG fuori dal dungeon non pesca mai le frasi che nominano la sua stanza o che hanno senso solo per chi vive lì sotto.

---

## 4. Le frasi di un PNG

Ogni PNG è un paragrafo di frasi, pescate da `data/npcs.json`:

1. **il legame con il luogo** (`origins`, per il suo tipo): sempre per primo;
2. **cosa vuole** (`wants`), **come si presenta** (`manners`: aspetto, abitudini, un dettaglio da recitare) e **cosa può offrire** agli avventurieri (`offers`): queste tre in ordine casuale;
3. 6 volte su 10, **cosa teme** (`fears`), dopo la prima di queste tre;
4. una volta su due, **un segreto** (`secrets`): nella chiave comincia con «Segreto:», perché l'arbitro lo riconosca subito;
5. **cosa pensa di un altro PNG** (`relations`, vedi il capitolo 5).

I segnaposti sono quelli delle fazioni (vedi [factions.md](factions.md#4-le-frasi-di-una-fazione)), più:

| Segnaposto | Cosa diventa |
|---|---|
| `{npc}` | il nome del PNG |
| `{faction}` | la sua fazione, con l'articolo minuscolo: *il Branco di Rinu* |
| `{other}` | il nome di un altro PNG |
| `{room}` | la sua stanza |
| `{o}` | in italiano, `o` o `a` secondo il genere: «riconosciut{o}» |
| `{He}`, `{he}`, `{him}`, `{his}`, `{His}` | in inglese, i pronomi secondo il genere |

Il mazzo di ogni tabella si mescola una volta per dungeon: due PNG dello stesso dungeon non hanno mai lo stesso desiderio, modo, offerta, paura o segreto.

---

## 5. I rapporti tra i PNG

Come le fazioni, i PNG sono legati in **cerchio**: il primo ha un sentimento verso il secondo, il secondo verso il terzo, e l'ultimo verso il primo. Un rapporto può essere un debito, un amore segreto, un odio, un ricatto:

> Deve a Ithvexnar un pasto caldo e una ferita ricucita, e i debiti li salda sempre.

I rapporti attraversano le fazioni: un membro del Branco può essere innamorato di un membro del Silenzio, e un solitario può ricattare il capo di una fazione.

---

## 6. Quanti PNG diversi

**Contenuto.** Moltiplicando le scelte possibili per un PNG:

| Parte | Scelte |
|---|---|
| ruolo | 58 |
| legame con il luogo | 96 |
| desiderio | 51 |
| modo | 51 |
| offerta | 35 |
| paura, o nessuna | 35 + 1 = 36 |
| segreto, o nessuno | 41 + 1 = 42 |
| rapporto | 30 |

58 × 96 × 51 × 51 × 35 × 36 × 42 × 30 = **22.992.207.436.800** PNG diversi (quasi 23 mila miliardi), senza contare il genere, i nomi inventati e le parole della storia e delle fazioni, che cambiano in ogni dungeon.

**Forma.** Desiderio, modo e offerta in ordine casuale danno 6 ordini; con o senza paura, con o senza segreto: 6 × 2 × 2 = **24 forme** del paragrafo.

---

## 7. Nella chiave

I PNG hanno una sezione loro, **PERSONAGGI NON GIOCANTI**, dopo le fazioni e prima degli ingressi; nel PDF è un capitolo con il nome di ogni PNG in grassetto. Accanto al nome ci sono il ruolo, la stanza e, per chi ne fa parte, la fazione:

```
PERSONAGGI NON GIOCANTI
  Kaelpraah, vecchia maestra d'armi (sala 3-01; il Silenzio di Esnar)
    Ha scelto il Silenzio di Esnar perché era l'unica fazione che offrisse un pasto caldo. …
```

Mentre genera, il programma dice quanti PNG ha creato: `Personaggi non giocanti: 5 (Kaelpraah, Dolma, Dethanezad, Bibjerg e Ithvexnar)`.

I PNG non compaiono sulle mappe: sono solo nella chiave.

---

## 8. Un esempio completo

Seme `4-30-4-3-K-ZZT0P1`, con le fazioni. La sua storia: i minatori di Beard costruirono un villaggio sotterraneo per sigillare una porta verso altri mondi; la scomparsa del dio protettore li cacciò; gli hobgoblin mercanti di schiavi di Leebek se ne impadronirono finché non venne una crociata; oggi ci vivono gli uomini fungo di Balabad. L'eroe scomparso è Tuville. Le 30 stanze e i 4 livelli danno 5 PNG:

> **Kaelpraah, vecchia maestra d'armi (sala 3-01; il Silenzio di Esnar)**
> Ha scelto il Silenzio di Esnar perché era l'unica fazione che offrisse un pasto caldo. Offre agli avventurieri un ingaggio: il Silenzio di Esnar paga bene chi porta teste, e meglio chi porta mappe. Nella sua lanterna, al posto della fiamma, brilla una lucciola gigante. Vuole aprire una porta rimasta chiusa fin da quando arrivò la scomparsa del dio protettore. Segreto: il tesoro di cui parla tanto l'ha già trovato e speso, anni fa, in una sola notte di gioco. È segretamente innamorata di Dolma, e non trova il coraggio di dirlo.
>
> **Dolma, negromante alle prime armi (sala 1-04; il Branco di Rinu)**
> Fu eletta per acclamazione, e ora guida il Branco di Rinu senza sapere bene come si faccia. Parla solo sussurrando, e si arrabbia con chi alza la voce. Evita specchi e acque ferme, perché vi vede riflesso un volto che non è il suo. Ripara armi e armature con attrezzi rubati, e lavora bene. Da quando suo fratello è prigioniero dei padroni attuali, gli uomini fungo di Balabad, pensa solo a liberarlo. Deride Dethanezad alle spalle, ma al primo grido d'aiuto accorre.
>
> **Dethanezad, acchiappatopi (sala 1-06; il Giuramento di Thalkorglo)**
> Ha cambiato bandiera due volte; ora sta con il Giuramento di Thalkorglo, ma solo finché ci guadagna. Ha le dita tatuate con le lettere di una preghiera dimenticata, e le recita contandole. Teme di scoprire la verità sulla propria nascita, che ha qualcosa a che fare con una crociata. Cerca le armi che gli hobgoblin mercanti di schiavi di Leebek nascosero prima della fine, per armare il proprio villaggio. Scambia informazioni con informazioni, mai con oro. Ha giurato di uccidere Bibjerg prima della prossima luna piena, ma continua a rimandare.
>
> **Bibjerg, servo dei mostri (sala 4-07)**
> Venera gli uomini fungo di Balabad come dei viventi, e lascia offerte che nessuno ha mai chiesto. Saluta ogni sala in cui entra, come se fosse abitata. Essere riconosciuto è la sua paura più grande: c'è una taglia sulla sua testa in tre baronie. Cede a buon prezzo una pagina del diario di Tuville, con l'ultimo tratto della strada disegnato a carboncino. Vuole riprendersi ciò che mercenari senza paga portarono via anni fa: un ritratto di famiglia. Deve a Ithvexnar un pasto caldo e una ferita ricucita, e i debiti li salda sempre.
>
> **Ithvexnar, bibliotecario (sala 4-05)**
> Restaura da anni, una lettera alla volta, le iscrizioni che i minatori di Beard incisero sui muri. Può organizzare un diversivo per tenere occupati i padroni attuali, gli uomini fungo di Balabad, per il tempo di una candela. Veste di un bianco immacolato, e nessuno capisce come ci riesca quaggiù. Spera di trovare la stanza in cui, si dice, i minatori di Beard nascosero la loro ultima ricchezza. Segreto: fu una sua lettera a indicare ai padroni attuali, gli uomini fungo di Balabad, la strada per questo luogo. Ammira Kaelpraah oltre ogni ragione, e ne imita perfino il modo di camminare.

Si vede che:

- **Kaelpraah**, **Dolma** e **Dethanezad** fanno parte di tre fazioni e stanno nelle loro basi; **Dolma** è proprio il capo del Branco di Rinu che compare tra le fazioni;
- **Bibjerg** è un solitario `present`, servo degli uomini fungo, e sta in una delle loro sale; **Ithvexnar** è `heirs`, e studia le iscrizioni dei fondatori;
- i segreti si intrecciano con la storia: Ithvexnar ha portato qui gli uomini fungo, e Bibjerg li venera;
- i rapporti fanno un cerchio che attraversa le fazioni: Kaelpraah (Silenzio) ama Dolma (Branco), Dolma deride Dethanezad (Giuramento) ma lo soccorre, che vuole uccidere Bibjerg, che deve un favore a Ithvexnar, che ammira Kaelpraah.

---

## 9. Cambiare le tabelle

Tutto è in `data/npcs.json`. Fai una copia del file prima di modificarlo.

| Voce | Cosa contiene |
|---|---|
| `roles` | i ruoli: `it` come coppia [maschile, femminile], `en`, e `kinds`, i tipi di PNG a cui il ruolo si adatta |
| `origins` | il legame con il luogo, per ogni tipo: `present` (usa `{p}`), `heirs` (`{f}`), `second` (`{s}`), `relic` (`{relic}`), `outsiders`, `member` e `leader` (`{faction}`) |
| `wants`, `fears`, `secrets` | cosa vuole, cosa teme, cosa nasconde |
| `manners` | come si presenta: aspetto, abitudini, un dettaglio da recitare |
| `offers` | cosa può dare o fare per gli avventurieri, e a che prezzo |
| `relations` | cosa pensa di un altro PNG (usa `{other}`) |

Le condizioni sono quelle delle fazioni, più una:

| Condizione | Cosa vuol dire |
|---|---|
| `"inside": true` | solo per un PNG che sta nel dungeon |
| `"not": ["outsiders", …]` | non per questi tipi |
| `"faction": true` | solo per un PNG che fa parte di una fazione (obbligatoria per le frasi con `{faction}`) |

Un ruolo e una frase:

```json
{"it": ["cartografo rinnegato", "cartografa rinnegata"], "en": "renegade cartographer", "kinds": ["outsiders", "member"]}
{"it": "Desidera soltanto essere dimenticat{o} da tutti, a cominciare dai creditori.", "en": "All {he} wants is to be forgotten by everyone, starting with the creditors."}
```

Le regole per l'italiano sono quelle delle fazioni (vedi [factions.md](factions.md#9-cambiare-le-tabelle)), con una differenza: le parole che si accordano **con il PNG** usano `{o}`; quelle che si accordano con un segnaposto (`{p}`, `{relic}`, `{faction}`, `{other}`…) restano vietate. Le parole che non finiscono in `-o`/`-a` (per esempio *attore*/*attrice*) vanno evitate. In inglese i pronomi del PNG si scrivono come segnaposti (`{he}`, `{his}`…), mai *he* o *she*.

Se `data/npcs.json` manca o ha un errore, il programma lo dice e fa il dungeon senza PNG.
