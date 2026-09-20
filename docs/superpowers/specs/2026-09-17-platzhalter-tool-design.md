# Platzhalter-Tool: Design

Datum: 2026-09-17

## Zweck

Kleines Windows-Programm für Schritt 8 des Ablaufs («Fertig»): Der Benutzer setzt die
Platzhalter wie `[ADRESSE]`, `[TELEFON]`, `[AHV]`, `[IBAN]` in den Word-Entwürfen selbst ein.
Bisher von Hand, künftig mit diesem Programm. Es wird von der Homepage als EXE
heruntergeladen (`https://stayingclean.github.io/ki-tasks/platzhalter.exe`).

## Ablauf im Programm

1. Start: Windows-Ordnerdialog. Alternativ Ordner als erstes Kommandozeilen-Argument.
2. Suche rekursiv alle `.docx` im Ordner. Übersprungen werden Word-Sperrdateien (`~$…`)
   und Sicherungen (`.bak`).
3. Platzhalter sammeln: jedes `[Text]` mit 1 bis 80 Zeichen ohne Klammern, Zeilenumbruch
   oder Tab, das ein Wort enthält, also zwei Buchstaben am Stück (`A-Za-zÄÖÜäöüß`).
   Gross-/Kleinschreibung wird unterschieden. Der Wortzwang hält Quellenverweise heraus:
   `[1]`, `[1, 2]`, `[12]`, `[S. 12]` und `[3a]` gelten nicht als Platzhalter, wohl aber
   `[AHV-Nummer]`, `[PLZ/Ort]` und `[Betrag 2026]`. Bekannte Grenze: `[vgl. 3]` wird
   erkannt, weil «vgl» als Wort zählt.
4. Oberfläche: pro Platzhalter ein Eingabefeld, daneben Anzahl Vorkommen; Dateien aufklappbar.
   Sortierung nach Häufigkeit, dann alphabetisch.
5. Knopf «Ersetzen»: Bestätigung mit Zusammenfassung (n Platzhalter in m Dateien, leere
   Felder werden übersprungen). Ohne ausgefüllten Wert ist der Knopf deaktiviert.
6. Ersetzen in allen zuvor durchsuchten Dateien, die mindestens einen ausgefüllten
   Platzhalter enthalten. Vor dem Schreiben wird `<name>.docx.bak` angelegt (bestehende
   `.bak` wird überschrieben). Danach Ergebnisliste je Datei: Anzahl Ersetzungen oder Fehler.
7. Eingegebene Werte werden nirgends gespeichert (kein Log, keine Konfigurationsdatei).

## Ersetzung in der Datei

- Bibliothek: python-docx. Es werden alle `w:p`-Elemente durchlaufen in: Textkörper
  (inklusive Tabellen und Textfelder, da über XML iteriert wird), allen Kopf- und Fusszeilen.
- Word teilt Text oft auf mehrere Runs (`w:r`/`w:t`). Vorgehen pro Absatz: Text aller Runs
  zusammensetzen; enthält er keinen ausgefüllten Platzhalter, Absatz unverändert lassen.
  Sonst: für jedes Vorkommen den Bereich der betroffenen Runs bestimmen, den ersetzten Text
  in den ersten betroffenen Run schreiben, die restlichen betroffenen Runs leeren.
  Formatierung des ersten Runs bleibt. Runs ohne `w:t` (Bilder, reine Tabs oder Umbrüche)
  zählen mit Textlänge 0 und werden nie angetastet.
- Nicht unterstützt: Platzhalter in Kommentaren, Fussnoten, Feldern (`w:fldSimple`) oder
  über Absatzgrenzen hinweg.

## Fehler

- Datei gesperrt (Word offen) oder beschädigt: Meldung in der Ergebnisliste, übrige Dateien
  werden verarbeitet. Beim Suchen werden unlesbare Dateien mit Fehler aufgeführt.
- Keine `.docx` oder keine Platzhalter gefunden: Hinweis mit Knopf «Anderer Ordner».
- Fehler beim Ersetzen einer Datei: Originaldatei bleibt unverändert, weil zuerst in eine
  temporäre Datei geschrieben und diese dann an die Stelle des Originals verschoben wird.

## Aufbau

```
platzhalter/
  pyproject.toml            uv; Abhängigkeiten: pywebview, python-docx; dev: pytest, pyinstaller
  uv.lock
  logo.png                  Original des stayingclean-Logos (970x970)
  logo.ico                  daraus erzeugt: Symbol der EXE, Grössen 16 bis 256
  werkzeuge/logo_aufbereiten.py   erzeugt logo.ico und ui/logo.txt (braucht Pillow)
  src/platzhalter/
    __init__.py
    __main__.py             Start: Argument oder Ordnerdialog, dann Fenster
    dokument.py             MUSTER, alle_absaetze(doc), runs(p), absatz_text(p)
    suche.py                finde_docx(ordner), durchsuche(ordner) -> Suchergebnis
    docx_ersetzen.py        ersetze_in_datei(pfad, werte) -> Anzahl; Absatz-Logik
    app.py                  pywebview-Fenster, Api-Klasse (waehle_ordner, suche, ersetze)
    ui/index.html           Oberfläche in einer Datei, Stil wie dist/index.html (Teal)
    ui/logo.txt             Logo mit 96 Pixeln als Base64, ersetzt {{LOGO}} in der Seite
  tests/
    test_suche.py
    test_docx_ersetzen.py   erzeugt .docx mit geteilten Runs, Tabellen, Kopfzeile
    test_app.py             Api-Klasse ohne Fenster, Einbetten des Logos
  platzhalter.spec          PyInstaller onefile, windowed, ui/ als Daten, logo.ico als Symbol
  README.md                 Nutzung, SmartScreen-Hinweis, Entwicklung mit uv
```

Das Logo erscheint an zwei Stellen: als Symbol der EXE (damit auch im Fensterrahmen und in
der Taskleiste) und im Kopf der Oberfläche links neben dem Titel. Weil die Seite als
Zeichenkette an pywebview geht, lösen relative Bildpfade nicht auf; das Logo wird darum als
Base64 eingebettet. Beim Start über Python statt über die EXE zeigt Windows im Rahmen
weiterhin das Python-Symbol.

Datenfluss: `__main__` → `app.starte(ordner)` → JS ruft `api.suche()` → Python liefert
JSON `{ordner, dateien: [..], platzhalter: [{name, anzahl, dateien: [..]}], fehler: [..]}`
→ JS zeigt Liste → JS ruft `api.ersetze({name: wert, ...})` → Python liefert
`[{datei, ersetzt, fehler}]`.

`suche.py` und `docx_ersetzen.py` haben keine UI-Abhängigkeit und sind einzeln testbar.

## Veröffentlichen

`.github/workflows/pages.yml` bekommt einen Job `exe` auf `windows-latest`:
`astral-sh/setup-uv`, `uv sync`, `uv run pyinstaller platzhalter.spec` im Ordner
`platzhalter/`, Artefakt `platzhalter.exe`. Der Job `build` (ubuntu) braucht `exe`, lädt das
Artefakt nach `dist/platzhalter.exe` nach `python build.py` und veröffentlicht `dist/` wie
bisher. `build.py` bleibt unverändert und ohne Abhängigkeiten. Keine Code-Signatur;
SmartScreen warnt beim ersten Start, das steht im README.

## Repo-Pflege

- `CLAUDE.md`: Zeile zu `platzhalter/` (eigenes uv-Projekt, Tests mit `uv run pytest`).
- `README.md`: Abschnitt «Platzhalter-Tool» mit Download-Link und Kurzbeschreibung.
- Der Link auf der Anleitungsseite (Repo toolbox) wird nicht in diesem Schritt gesetzt.

## Tests

- `suche.py`: Muster (gültig/ungültig), Rekursion, Überspringen von `~$` und `.bak`,
  Zählung über mehrere Dateien.
- `docx_ersetzen.py`: Platzhalter in einem Run, über drei Runs verteilt, zwei Vorkommen im
  selben Absatz, in Tabelle, in Kopfzeile, leerer Wert bleibt stehen, Formatierung des
  ersten Runs bleibt, Datei ohne Treffer bleibt unverändert.
- UI: manuell mit `uv run python -m platzhalter <ordner>`.
