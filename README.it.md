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
| `═║╔╗` | **I** — i fondatori (nani, sacerdoti, un mago, una legione, una tomba imperiale) |
| `─│┌┐` | **II** — chi venne dopo (cultisti, contrabbandieri, un negromante, goblin, monaci) |
| `#` (stanze sbozzate) | **III** — gli abitanti di oggi (un orco, orchetti, non morti, ragni, trogloditi) |

Le stanze sono numerate **livello-stanza**: `1-01`, `2-07`, e `1a-01` per un sottolivello. La chiave del dungeon racconta per ogni stanza a cosa serviva in ogni epoca (es. *Sala del trono; II: bisca; III: tana dell'orco*).

La pianta segue **sempre** i principi di Jennell Jaquays, come li descrive Justin Alexander in *Xandering the Dungeon*: ingressi multipli, anelli, collegamenti multipli e discontinui tra i livelli, percorsi segreti e insoliti (porte e passaggi segreti, scale nascoste, passaggi allagati, crolli, portali), sottolivelli, livelli divisi, dislivelli interni, ingressi a metà dungeon, dungeon annidati. A fine generazione il programma verifica che ogni stanza sia raggiungibile e stampa quali principi ha applicato.

---

## 1. Cosa ti serve

Metti nella **stessa cartella**:

- `wyrmdelve.py` (il programma)
- `requirements.txt`
- `README.it.md` e `README.md`

La cartella `dungeons_generated` la crea il programma.

Serve Python 3.8 o successivo e la libreria Pillow:

```
pip install -r requirements.txt
```

## 2. Come si usa

```
python wyrmdelve.py
```

1. Scegli la lingua (italiano o inglese).
2. Compare l'orco nel suo dungeon. Premi **INVIO** per un dungeon tutto casuale, oppure scrivi **P** per scegliere tu i parametri, o **R** per rifare un dungeon dal suo seme.
3. Con **P** scegli: numero di livelli, numero di stanze (almeno 2 per livello), numero di ingressi/uscite dall'area, numero di porte e passaggi segreti.
4. In ogni caso scegli i colori:
   1. simboli neri su sfondo bianco (default)
   2. simboli bianchi su sfondo celeste
   3. simboli bianchi su sfondo nero
5. Vuoi un **nome** per la mappa? Se no, la mappa esce senza titolo. Se sì, scegli se **generarlo a caso** (es. *Tomba di Zordur*, default) o **scriverlo tu**.
6. Il programma costruisce il dungeon e ti chiede come impaginare i livelli:
   1. tutti i livelli in **un solo foglio** (default)
   2. **un livello per foglio**, su file separati

   (con un solo livello la domanda non compare).
7. Poi ti chiede che file vuoi: un'immagine **PNG** (una per foglio) oppure un **PDF** (con un livello per foglio, un solo PDF con tutti i fogli).
8. Infine ti mostra una tabella con **A4, A3, A2 e A1**: per ogni formato la grandezza dei caratteri e se sono leggibili. Ti consiglia il foglio più piccolo su cui la mappa si legge bene; premi Invio per accettarlo o scrivi un altro formato. L'immagine esce sempre a **600 dpi** e il foglio si gira da solo in verticale o in orizzontale.

## 3. Cosa ottieni

In `dungeons_generated/<seme>/`:

| File | Contenuto |
|---|---|
| `<seme>_gm.png` / `.txt` | mappa del master: numeri delle stanze, porte `S` e passaggi `░` segreti |
| `<seme>_players.png` / `.txt` | la stessa mappa senza numeri e senza segreti |
| `<seme>_key.txt` | storia, strati, ingressi, collegamenti tra livelli, chiave stanza per stanza, verifica dei principi di Jaquays |

Con **un livello per foglio** i nomi dei PNG contengono il livello: `<seme>_gm_L1.png`, `<seme>_gm_L2a.png`… Tutti i fogli usano caratteri della stessa grandezza, così i livelli restano in scala. Con il **PDF** ottieni invece `<seme>_gm.pdf` e `<seme>_players.pdf` (una pagina per foglio, senza perdita di qualità, 600 dpi), ognuno con il suo `.txt`.

Il **seme** (es. `3-24-2-5-K7Q2MB` = livelli-stanze-ingressi-segreti-codice) contiene tutto il dungeon: lo stesso seme dà sempre lo stesso dungeon.

## 4. Simboli

| Simbolo | Significato | Simbolo | Significato |
|---|---|---|---|
| `.` | pavimento | `+` | porta |
| `S` | porta segreta (solo master) | `░` | passaggio segreto (solo master) |
| `<` `>` | scale su / giù | `≡` | gradini, stesso livello |
| `○` | pozzo o camino tra livelli (può saltarne qualcuno) | `Ω` | portale magico |
| `≈` | acqua | `∴` | crollo |
| `■` | colonna | `[A]` | ingresso (riquadro pieno sulla mappa) |

## 5. Opzioni da riga di comando

Ogni opzione ha un nome italiano e uno inglese. Quello che non indichi è scelto a caso.

```
python wyrmdelve.py --livelli 3 --stanze 24 --ingressi 2 --segreti 5
python wyrmdelve.py --colori 2                   (1 nero/bianco, 2 bianco/celeste, 3 bianco/nero)
python wyrmdelve.py --seme 3-24-2-5-K7Q2MB       rifà un dungeon
python wyrmdelve.py --formato A2                 salta la domanda sul formato
python wyrmdelve.py --per-livello                un livello per foglio (--un-foglio: tutti in uno)
python wyrmdelve.py --pdf                        salva in PDF (--png: in PNG)
python wyrmdelve.py --titolo "La Tana dell'Orco"
python wyrmdelve.py --senza-titolo               mappa senza nome
python wyrmdelve.py --solo-ascii                 solo caratteri della tastiera (# ~ = o)
python wyrmdelve.py --font MioFont.ttf
python wyrmdelve.py --lingua en
python wyrmdelve.py --help
```

## 6. Limiti

Livelli 1–10, stanze 3–200 (almeno 2 per livello), ingressi 1–9, segreti 0–60. Se chiedi più segreti di quanti corridoi e collegamenti ci siano, il programma lo dice e mette quelli possibili. Alcuni principi di Jaquays hanno bisogno di spazio: con un solo livello non ci sono collegamenti tra livelli, i sottolivelli compaiono da 8 stanze in su, i livelli divisi su livelli da almeno 6 stanze.

## Fonti

- Justin Alexander, [Xandering the Dungeon](https://thealexandrian.net/wordpress/13085/roleplaying-games/xandering-the-dungeon) (parti 1–5) e [Xandering on the Small Scale](https://thealexandrian.net/wordpress/34950/roleplaying-games/thought-of-the-day-xandering-on-the-small-scale)
