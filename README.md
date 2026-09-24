# ki-tasks – Aufgaben-Ordner für Papierkram mit KI-Unterstützung

Fertige Startordner für Aufgaben wie Wohnungssuche, Stellensuche oder Gesuche,
gebaut nach der Anleitung [«Mit Claude arbeiten»](https://stayingclean.github.io/toolbox/claude-anleitung/).

**Herunterladen:** https://stayingclean.github.io/ki-tasks/ (ein Zip pro Aufgabe)
oder das ganze Repo als [main.zip](https://github.com/stayingclean/ki-tasks/archive/refs/heads/main.zip).

## Idee

Der Mensch spricht, Claude schreibt die Dateien. Von Hand angefasst wird nur, was
sich nicht sprechen lässt: ein PDF in einen Ordner legen und einen Word-Entwurf
kommentieren. Alles andere — Auftrag, offene Punkte, Trefferlisten — entsteht im
Gespräch und wird von Claude geführt.

Zielplattform ist Claude Desktop → Cowork. Dort gibt es keine Slash-Befehle und
keine Skills; der einzige automatische Haken ist `CLAUDE.md` im verbundenen
Ordner. Darum muss alles aus **einem Satz** entstehen, den sich ein Mensch merkt:
`Was steht an?`

So sieht der entpackte Ordner beim Benutzer aus:

```
START-HIER.txt          das Einzige, was ein Mensch liest
CLAUDE.md               Leitplanken für Claude
1_Meine-Unterlagen/     PDF und Scans der Person. Claude liest, schreibt nie
2_Arbeitsstand/         Funde, Tabellen, Entwürfe als .docx
  verlauf/              frühere Fassungen, datiert
3_Zum-Versenden/        fertige PDF, nur auf Freigabe
9_Claude/               wissen.md (mitgeliefert) und stand.md (Claude legt an)
```

Und so ist das Repo aufgebaut:

```
grundgeruest/                 EINMAL: START-HIER.txt, CLAUDE.md und die vier Ordner
aufgaben/
  wohnung/                    nur das Aufgabenspezifische:
    INFO.md                     Titel, Gruppe, Kurzbeschrieb (für die Download-Seite)
    9_Claude/wissen.md          Fachwissen zu dieser Aufgabe
  stelle/
  gesuch-krankheitskosten/
build.py                      Grundgerüst + Aufgabe → dist/<aufgabe>.zip, dazu index.html
platzhalter/                  Windows-Programm: [Platzhalter] in Word-Dateien einsetzen (uv, EXE)
anleitung/                    Ordner, Platzhalter, je Aufgabe eine Seite (holt der Toolbox-Deploy)
```

`build.py` legt das Grundgerüst hin und die Aufgaben-Schicht darüber — eine reine
Überlagerung, `wissen.md` der Aufgabe ersetzt die Fassung aus dem Grundgerüst.

## Zwei Dateien, die den Unterschied machen

**`grundgeruest/CLAUDE.md`** enthält die Leitplanken: widersprechen, wenn ein
Kriterium unrealistisch ist; dem Beleg mehr glauben als der mündlichen Angabe;
nie einen Beleg verändern; vor dem Versand nachprüfen, was veralten kann
(Adressen, Ansprechpersonen, Fristen); im Zweifel fragen statt raten.

**`aufgaben/<name>/9_Claude/wissen.md`** ist das Fachwissen zur Aufgabe. Es ist
bewusst getrennt vom konkreten Auftrag: Das Wissen ist für alle gleich und wird
mitgeliefert, der Auftrag entsteht im Gespräch und landet in `stand.md`. Wer eine
Aufgabe herunterlädt, muss deshalb nichts ausfüllen.

## Lokal bauen

```
python build.py
```

Keine Abhängigkeiten ausser Python 3.10+. Das Ergebnis liegt in `dist/`
(gitignored): ein Zip pro Aufgabe, `grundgeruest.zip` für eine eigene Aufgabe,
dazu `index.html` und `aufgaben.json`.

## Platzhalter-Tool

`platzhalter/` enthält ein kleines Windows-Programm für den letzten Schritt: Es
sucht in einem Ordner rekursiv alle Word-Dateien nach Platzhaltern in eckigen
Klammern, zeigt sie zum Ausfüllen an und setzt die Werte in allen Dateien ein.
Download: https://stayingclean.github.io/ki-tasks/platzhalter.exe

Claude lässt darum jede Lücke als benannten Platzhalter stehen — `[ADRESSE]`,
`[IBAN]`, aber auch `[Einzugsdatum]` oder `[Monatsmiete]`. Adresse,
Telefonnummer und IBAN kommen so nie in eine Datei, die Claude liest.

Eigenes uv-Projekt, unabhängig von `build.py`. Details in `platzhalter/README.md`.
Die EXE baut der Workflow auf einem Windows-Runner und legt sie neben die Zips.

## Anleitung

`anleitung/` enthält zwei Seiten zur Arbeitsweise, eine Übersicht und eine
Seite je Aufgabe:

```
der-ordner.html      was drinliegt und was Claude darin tut
platzhalter.html     Adresse und IBAN am Schluss einsetzen
aufgaben.html        welches Zip wofür, was allen gemeinsam ist
<name>.html          je Aufgabe: Ablauf, was Claude fragt, wo er sucht, was du
                     besorgen musst, was entsteht, wo er widerspricht, Download
```

Der Deploy des Repos
[stayingclean/toolbox](https://github.com/stayingclean/toolbox) holt den Ordner
beim Bauen und kopiert ihn nach `docs/claude-anleitung/`. Die Seiten erscheinen
darum unter [der Toolbox-URL](https://stayingclean.github.io/toolbox/claude-anleitung/)
und nicht auf der Download-Seite dieses Repos.

Sie liegen hier, weil sie sich mit dem Ordner zusammen ändern müssen: Wer
`grundgeruest/` umbaut, eine Leitplanke in `grundgeruest/CLAUDE.md` ändert, am
Platzhalter-Tool etwas dreht oder ein `wissen.md` anpasst, zieht diese Seiten
mit nach. Genau dieser Gleichschritt war gebrochen, solange die Anleitung
vollständig im anderen Repo lag.

Die Aufgabenseiten sind die Leseform von `aufgaben/<name>/9_Claude/wissen.md`
— dieselbe Sache, einmal für Claude und einmal für einen Menschen. Ändert sich
das `wissen.md`, ändert sich die Seite mit. Neue Regeln gehören aber weiterhin
ins `wissen.md`, nicht hierher.

Aussehen und Navigation kommen von drüben (`stil.css`, `anleitung.js`): kein
eigener CSS-Block ausser für wirklich Seitenspezifisches, Links relativ.
Einzeln im Browser geöffnet sehen die Seiten darum unfertig aus; zum Prüfen
neben eine Kopie von `stil.css` und `anleitung.js` legen. `build.py` kopiert den Ordner nicht, schaut
aber nach, ob `anleitung/<name>.html` existiert: Dann führt die Karte auf der
Download-Seite zu dieser Beschreibung unter der Toolbox-URL, der Zip-Link steht
darunter. Fehlt die Seite, zeigt die Karte direkt aufs Zip.

### Namenskonvention: Aufgabe und Seite

Eine Aufgabenseite erscheint von selbst in der Navigation und auf der
Übersicht, wenn sie gleich heisst wie der Aufgabenordner:

```
aufgaben/<name>/INFO.md     reihenfolge: 30      → Platz in Navigation und Karten
anleitung/<name>.html       <h1>…</h1>           → Titel in Navigation und Karte
                            <p class="lead">…</p> → Text der Karte auf aufgaben.html
```

Der Lead wird wörtlich zum Kartentext. Er muss darum ohne die Seite verständlich
sein: die Aufgabe beschreiben, nicht die Seite («Was Claude dabei fragt …» taugt
als Karte nicht).

Beim Toolbox-Deploy setzt `tools/anleitung_aufgaben.py` drüben daraus den Block
«Aufgaben» in `SEITEN` und die Karten zwischen `<!-- AUFGABEN-KARTEN -->` auf
`aufgaben.html` ein. Die Karten, die hier im Repo stehen, sind nur für die
lokale Ansicht. Eine Seite in `anleitung/` ohne passende Aufgabe (und nicht von
Hand in `SEITEN`) lässt den Deploy abbrechen, weil sie sonst unerreichbar wäre.
Eine Aufgabe ohne Seite wird nur gemeldet; ihre Karte auf der Download-Seite
zeigt dann direkt aufs Zip.

Nur Seiten, die keine Aufgabe beschreiben (wie `der-ordner.html`), müssen
drüben noch von Hand in `SEITEN` eingetragen werden.

### Deploy der Toolbox anstossen

Nach jedem Deploy hier stösst der Job `toolbox` in
`.github/workflows/pages.yml` den Deploy drüben an (`repository_dispatch`).
Das Token stellt eine GitHub App aus. Einmalig einrichten:

1. GitHub → Settings → Developer settings → GitHub Apps → New GitHub App.
   Webhook ausschalten, Repository permissions → Contents: Read and write.
2. Die App **nur** auf `stayingclean/toolbox` installieren.
3. Einen Private Key erzeugen (.pem).
4. Hier in ki-tasks → Settings → Secrets and variables → Actions:
   Variable `TOOLBOX_APP_ID` (App-ID), Secret `TOOLBOX_APP_KEY` (ganzer Inhalt der .pem).

Ohne die Variable wird der Job übersprungen; drüben zieht dann der tägliche
Cron nach.

## Neue Aufgabe anlegen

1. Ordner `aufgaben/<name>/` (kleingeschrieben, ohne Umlaute; der Name wird
   Dateiname des Zips).
2. `INFO.md` mit `titel:`, `gruppe:`, `kurz:` und `reihenfolge:` (Zahl; bestimmt
   die Folge auf der Download-Seite und in der Navigation der Anleitung).
3. `9_Claude/wissen.md` nach dem Aufbau von `aufgaben/wohnung/9_Claude/wissen.md`:
   was Claude am Anfang fragt · wo gesucht wird · wie Treffer abgelegt und im Chat
   ausgewählt werden · welche Unterlagen nötig sind · welche Dokumente entstehen ·
   was nach `3_Zum-Versenden/` geht.
4. `python build.py` ausführen und das Zip einmal selbst entpacken und anschauen.
5. `anleitung/<name>.html` nach dem Vorbild von `anleitung/wohnung.html`, mit
   `<h1>` und `<p class="lead">`. Navigation und Karte entstehen beim Deploy
   drüben von selbst (siehe «Namenskonvention»).

Was NICHT in eine Aufgabe gehört: Regeln zum Verhalten (die stehen in
`grundgeruest/CLAUDE.md`), Formulare zum Ausfüllen, Beispieldaten echter Personen.

`wissen.md` beschreibt, was Claude wissen muss — nicht, was der Benutzer tun soll.
Steht darin ein Satz, der eine Handlung vom Benutzer verlangt, gehört er ins
Gespräch, nicht in die Datei.

## Veröffentlichen

Push auf `main` baut die Zips per GitHub Actions und veröffentlicht `dist/` auf
GitHub Pages. Einmalig in den Repo-Einstellungen: Pages → Source «GitHub Actions».

## Sprache und Ton

Deutsch (Schweiz): ss statt ß. Du-Form gegenüber dem Benutzer. Kurz, keine
Ausrufezeichen.
