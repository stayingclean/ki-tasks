# ki-tasks vereinfachen: Claude führt die Dateien, der Mensch spricht

Stand 20.09.2026. Ersetzt den Aufbau mit Grundgerüst, acht Schritten und fünf
nummerierten Ordnern.

## Warum

Das Projekt ist aus einer Idee und ein paar Prompts entstanden. Der Aufbau hat
zwei Probleme, die im Alltag durchschlagen:

1. **Dateien sind gleichzeitig Formular und Gedächtnis.** `profil.md` und
   `00_Auftraege/<name>.md` sind Eingabeformulare für den Menschen, `aufgaben.md`
   und `log.md` sind Gedächtnis für Claude. Beide liegen als `.md` nebeneinander.
   Wer nicht weiss, was er anfassen muss, fasst nichts an. Für «Stelle suchen»
   waren vor dem ersten Ergebnis fünf Hürden zu nehmen: zwei Dateien ausfüllen,
   eine lesen, PDF ablegen, eine Excel mit Häkchen bearbeiten, und einen exakten
   Satz abtippen.

2. **Die Regeln waren die falschen.** `regeln.md` bestand zu zwei Dritteln aus
   Mechanik (Pfade, `_v2`-Namen, Dateiformate). Was tatsächlich Fehler
   verhindert, stand nicht darin: widersprechen, dem Beleg mehr glauben als der
   mündlichen Angabe, keinen Beleg verändern, vor dem Versand nachprüfen, was
   veralten kann, und im Zweifel fragen statt raten.

Grundsatz des Umbaus: **Der Mensch spricht, Claude schreibt die Dateien.** Von
Hand angefasst wird nur noch, was sich nicht sprechen lässt — ein PDF in einen
Ordner legen und einen Word-Entwurf kommentieren.

## Zielbild

Die Zielplattform ist Claude Desktop → Cowork. Keine Slash-Befehle, keine Skills,
kein `.claude/`. Der einzige automatische Haken ist `CLAUDE.md` im verbundenen
Ordner. Alles muss aus **einem Satz** entstehen, den sich ein Mensch merkt:
`Was steht an?` — im leeren Ordner genauso wie drei Wochen später.

Entpackter Ordner beim Benutzer:

```
START-HIER.txt          das Einzige, was ein Mensch liest
CLAUDE.md               Leitplanken, muss im Wurzelverzeichnis liegen
1_Meine-Unterlagen/     PDF und Scans der Person. Claude liest, schreibt nie
2_Arbeitsstand/         Funde, Tabellen, Entwürfe als .docx
  verlauf/              frühere Fassungen, datiert
3_Zum-Versenden/        fertige PDF, nur auf Freigabe
9_Claude/               wissen.md (mitgeliefert) und stand.md (Claude legt an)
```

Vier sprechende Namen statt fünf Nummern. Die Ziffern 1-2-3 geben die Reihenfolge,
ohne dass jemand acht Schritte kennen muss. Das einzige `.md` im Blickfeld ist
`CLAUDE.md`, und die ist erkennbar nicht für Menschen.

## Entscheide

### Die acht Schritte fallen weg

Sie existierten, damit man `Führe den Auftrag … aus, Schritte 1 und 2` tippen
kann — genau die Reibung, die entfernt wird. Was pro Aufgabe wirklich anders
läuft, steht in `wissen.md`. Das Mermaid-Diagramm wandert in die Anleitung im
Repo `stayingclean/toolbox`; wer wissen will, wie es funktioniert, liest sie,
wer arbeiten will, braucht sie nicht.

### Auftrag und Fachwissen werden getrennt

`gesuch-krankheitskosten.md` war 100 Zeilen: rund 8 davon «was diese Person will»,
rund 92 Fachwissen, das für alle gleich ist. Getrennt liest der Benutzer gar
nichts mehr:

- **`9_Claude/wissen.md`** — Fachwissen zur Aufgabe, wird mitgeliefert, ändert
  sich pro Person nicht. Claudes Nachschlagewerk.
- **`9_Claude/stand.md`** — der konkrete Auftrag, die offenen Punkte, was
  erledigt ist. Entsteht im Gespräch, wird von Claude geführt.

### `[OFFEN]` wird ersatzlos gestrichen

Mehrere `[OFFEN]` in einem Dokument meinen verschiedene Dinge, `platzhalter.exe`
würde sie alle mit demselben Wert füllen. Stattdessen bekommt jede Lücke einen
Platzhalter, der benennt, was dort hingehört: `[Einzugsdatum]`,
`[Monatsmiete]` — dieselbe Form wie `[ADRESSE]`. Ein Konzept statt
zwei, und `platzhalter.exe` zeigt jeden Platzhalter mit Namen, Anzahl und
Fundstellen. Das Tool **ist** die Liste; eine zweite in einer Markdown-Datei
wäre eine zweite Wahrheit, die veraltet.

Regel: Platzhalternamen sind über den ganzen Ordner eindeutig. Zwei verschiedene
Beträge heissen nie beide `[Betrag]`.

Davon getrennt: Lücken, an denen Claude **nicht weiterarbeiten kann**, gehören
nicht ins Dokument, sondern als offener Punkt in `stand.md`.

### Ein Dateiname, Verlauf nach Datum

Ersetzt `_v2, _v3`. Die aktuelle Fassung behält immer denselben Namen; die
bisherige wandert vor jeder Änderung nach
`2_Arbeitsstand/verlauf/JJJJ-MM-TT_<name>.docx`. Zweimal am selben Tag: `_2`.

**Abhängigkeit:** `platzhalter.exe` sucht mit `rglob("*.docx")` rekursiv und
würde die Archivfassungen mitfüllen — die echte IBAN landete in zehn Dateien
statt in einer. Der Ordner `verlauf` muss in `finde_docx` übersprungen werden.
Eigener Umbau im Projekt `platzhalter/`, ohne ihn ist der Verlauf nicht sicher.

### Datenschutz: ehrlich statt beruhigend

Dass Claude die Belege sieht, ist bei Gesuchen der Kern des Nutzens: Nur so
lassen sich genannte Beträge gegen die Abrechnung prüfen, statt sie zu
übernehmen. Ein Ordner, in den Claude nicht hineinsieht, nimmt genau das weg.
Darum:

- Eine Ablage, keine Zone mit «Claude öffnet das nie». Eine solche Regel erzeugt
  Vertrauen, das sie nicht einlösen kann — die Dateien liegen trotzdem im
  verbundenen Ordner.
- `START-HIER.txt` beruhigt nicht, sondern trifft zu: *Alles in diesem Ordner
  geht an Anthropic. Was dort damit geschieht, steht in deinen
  Kontoeinstellungen.* Die alte Formulierung («Nicht ablegen: AHV-Ausweis,
  Bankkarten, Passwörter») liess den Schluss zu, der Rest sei unbedenklich — und
  die Aufgabe verlangte dann Kontoauszüge und Steuerrechnungen.
- Claude macht die Triage im Gespräch statt der Benutzer im Kopf: *braucht
  Claude es zum Rechnen* → in den Ordner; *braucht nur der Empfänger* → bleibt
  draussen, kommt beim Versand dazu; *braucht niemand* → gar nicht. Liegt etwas
  der zweiten oder dritten Art im Ordner, sagt Claude es ungefragt.

### Gesundheitsangaben: die Person entscheidet

Kein Verbot mehr. Claude schreibt sie nicht ungefragt in ein Dokument, darf
begründet abraten, hält sich danach an den Entscheid der Person.

### Auswahl aus Treffern läuft im Chat

Bisher: Excel öffnen, Kontrollkästchen setzen, speichern — mit einer Fussnote,
wie man in Excel 365 Kontrollkästchen einfügt. Neu: Claude legt die Trefferliste
als Tabelle in `2_Arbeitsstand/` ab (als Gedächtnis) und fragt im Chat, welche
Nummern weiterverfolgt werden.

### Drei Aufgaben statt vier

`wohnung-bei-stelle` war «Wohnung» mit Kriterien aus der Stellensuche. Wird zu
einer Nachfrage am Ende der Stellensuche und zu rund zehn Zeilen in
`stelle/9_Claude/wissen.md`. Bleiben: **wohnung**, **stelle**,
**gesuch-krankheitskosten**.

### Auslieferung bleibt ein Zip pro Aufgabe

Die Katalogseite («Was willst du erledigen?») ist die laientauglichste
Auswahloberfläche, die es im Projekt gibt, und die Toolbox-Anleitung verlinkt
sie. Gestrichen werden `alle-aufgaben.zip` und die Mehrfach-Zips
(`python build.py wohnung stelle`): wer zwei Aufgaben hat, lädt zwei Zips.

## Folgen für build.py

- `MERGE` und `fuege_zusammen()` entfallen vollständig — es gibt keine
  zusammengeführten Dateien mehr. Eine Aufgabe ist eine reine Überlagerung.
- `baue_zip()` nimmt eine Aufgabe statt einer Liste; das argv-Handling für
  Mehrfach-Zips entfällt.
- Neu: `START-HIER.txt` bekommt den Aufgabentitel aus `INFO.md` eingesetzt und
  wird **mit UTF-8-BOM und CRLF** geschrieben. Der `build`-Job läuft auf
  `ubuntu-latest`; ohne das käme die Datei mit LF im Zip an und ältere
  Notepad-Versionen zerlegen sie.
- `index.html`: Knopf für `alle-aufgaben.zip` weg, Beschreibungstext auf den
  neuen Aufbau.
- Keine Abhängigkeiten, wie bisher.

## Eine Aufgabe besteht künftig aus zwei Dateien

```
aufgaben/<name>/
  INFO.md                  titel, gruppe, kurz  (für Katalogseite und START-HIER.txt)
  9_Claude/wissen.md       Fachwissen zu dieser Aufgabe
```

Vorher waren es vier (`INFO.md`, `00_Auftraege/<name>.md`,
`02_Unterlagen/LIESMICH.md`, `aufgaben.md`), die sich überschnitten und
auseinanderliefen.

## Was gelöscht wird

`grundgeruest/regeln.md`, `profil.md`, `log.md`, `aufgaben.md`, `README.md`,
die Ordner `00_Auftraege` bis `04_Final`, und pro Aufgabe `00_Auftraege/`,
`02_Unterlagen/` und `aufgaben.md`.

## Offen, bewusst nicht gelöst

- Die Anleitung in `stayingclean/toolbox` unter `docs/claude-anleitung/` muss
  nachgezogen werden (Seiten arbeitsablauf, ordner-dateien, auftraege). Eigener
  Durchgang in jenem Repo.
- Ob Cowork `CLAUDE.md` in jedem Fall von selbst liest, ist nur durch den einen
  Testlauf belegt. Bleibt zu beobachten.
