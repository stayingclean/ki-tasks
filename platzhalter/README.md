# Platzhalter einsetzen

Kleines Programm für Windows und Mac, für den letzten Schritt des Ablaufs: Es durchsucht einen Ordner
(mit Unterordnern) nach Word-Dateien und ausfüllbaren PDF-Formularen, zeigt alle Platzhalter in eckigen Klammern wie
`[ADRESSE]` oder `[IBAN]` an und setzt die von dir eingegebenen Werte in allen Dateien ein.

Download: https://stayingclean.github.io/ki-tasks/platzhalter.exe (Windows),
https://stayingclean.github.io/ki-tasks/platzhalter-mac.zip (Mac mit Apple-Chip).

Linux, ohne fertiges Programm, mit [uv](https://docs.astral.sh/uv/):

```
uvx --from "git+https://github.com/stayingclean/ki-tasks#subdirectory=platzhalter" --with "pywebview[qt]" platzhalter
```

## Benutzen

1. `platzhalter.exe` bzw. `Platzhalter` starten und den Ordner wählen, zum Beispiel `2_Arbeitsstand`.
2. Für jeden Platzhalter den Wert eintragen. Was du leer lässt, bleibt stehen.
3. «Ersetzen» und bestätigen. Von jeder geänderten Datei liegt danach eine Sicherung
   `<name>.docx.bak` oder `<name>.pdf.bak` daneben. Die eingegebenen Werte werden nirgends gespeichert.

Ordner namens `verlauf` lässt das Programm bewusst aus, auf jeder Ebene: dort liegen frühere
Fassungen, und die sollen bleiben, was du damals verschickt hast. So landen deine echten
Angaben nur im aktuellen Entwurf und nicht in jeder alten Fassung daneben. Wählst du einen
`verlauf` direkt als Ordner aus, sagt dir das Programm das und ersetzt gar nichts — wähle
dann den Ordner darüber.

Beim ersten Start warnt das System, weil das Programm nicht signiert ist. Windows
SmartScreen: «Weitere Informationen» und dann «Trotzdem ausführen». Mac: «Fertig», dann
Systemeinstellungen → Datenschutz & Sicherheit → «Dennoch öffnen». Dateien, die gerade in Word offen
sind, können nicht geändert werden; sie erscheinen im Ergebnis mit Fehler.

Als Platzhalter gilt alles in eckigen Klammern, das ein Wort enthält, also zwei Buchstaben
am Stück: `[ADRESSE]`, `[Ort]`, `[Grösse]`, `[AHV-Nummer]`, `[PLZ/Ort]`, `[Betrag 2026]`.
Quellenverweise wie `[1]`, `[1, 2]` oder `[S. 12]` enthalten kein Wort und bleiben darum
unangetastet. Eine Ausnahme bleibt: `[vgl. 3]` gilt als Platzhalter, weil «vgl» ein Wort ist.

Ersetzt wird in Textkörper, Tabellen, Textfeldern sowie Kopf- und Fusszeilen, auch wenn Word
einen Platzhalter intern auf mehrere Textstücke verteilt hat. Nicht unterstützt: Platzhalter
in Kommentaren, Fussnoten oder über Absatzgrenzen hinweg. Nur `.docx`, kein altes `.doc`.

In PDF gilt nur, was in einem Textfeld eines Formulars (AcroForm) steht. Der gedruckte Text
der Seite bleibt, wie er ist: Dort stehen die Zeichen an festen Stellen, ein längerer Wert
würde überlaufen, und der eingebetteten Schrift fehlen oft die nötigen Buchstaben. Ein PDF
ohne Formularfelder oder mit Passwort zum Öffnen erscheint gar nicht erst in der Liste.
Formulare, die nur gegen Bearbeiten geschützt sind, gehen; gespeichert werden sie danach
ohne diesen Schutz. Hat ein Formular zusätzlich einen XFA-Teil, fällt der beim Speichern
weg, sonst zeigte Acrobat die alten Werte an. Reine XFA-Formulare ohne AcroForm-Felder
werden nicht unterstützt.

## Entwickeln

Voraussetzung: [uv](https://docs.astral.sh/uv/). Alle Befehle in diesem Ordner.

```
uv sync                                   # Python 3.12 und Abhängigkeiten
uv run pytest                             # Tests
uv run python -m platzhalter <ordner>     # Programm starten
uv run pyinstaller platzhalter.spec       # dist/platzhalter.exe bzw. dist/Platzhalter.app
```

Aufbau: `dokument.py` (Absätze, Runs und das Muster), `suche.py` (Dateien finden, Platzhalter
zählen), `docx_ersetzen.py` (Ersetzen über Run-Grenzen), `pdf_formular.py` (Textfelder
eines PDF-Formulars lesen und ersetzen, mit pypdf), `datei.py` (Sicherung und atomares
Schreiben), `app.py` und `ui/index.html` (Oberfläche mit pywebview). Alle Module ausser
`app.py` kennen keine Oberfläche und sind einzeln getestet. Die Test-Formulare baut
`tests/formular.py` selbst.

Das Logo liegt als `logo.png` bei. Daraus erzeugt
`uv run --with pillow python werkzeuge/logo_aufbereiten.py` zwei Fassungen, die beide
eingecheckt sind, damit der Build ohne Pillow auskommt: `logo.ico` als Symbol der EXE und
`src/platzhalter/ui/logo.txt` als Base64 für den Kopf der Oberfläche. Nach einem Austausch
von `logo.png` das Skript einmal laufen lassen.

EXE und Mac-App baut der GitHub-Actions-Workflow des Repos auf je einem Windows- und
macOS-Runner und veröffentlicht sie zusammen mit den Zips auf GitHub Pages. Die Mac-App
hat kein eigenes Symbol (dafür bräuchte es eine `.icns`-Datei).
