# Stelle suchen mit RAV — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Die Aufgabe `stelle` für eine Stellensuche über Monate mit optionalem RAV-Monatsabschluss, Status-Ordnern und Cowork-Projekt ausbauen; Wohnungssuche entfernen.

**Architecture:** Reine Inhaltsänderung. Verhalten steht in `aufgaben/stelle/9_Claude/wissen.md`, zwei allgemeine Regeln im Grundgerüst, die Leseform in `anleitung/stelle.html`. `build.py` überlagert wie bisher, bleibt unverändert.

**Tech Stack:** Markdown, HTML/CSS (Stil aus `stil.css` der Toolbox), Python 3.10+ für `build.py`.

**Spec:** `docs/superpowers/specs/2026-09-24-stelle-rav-design.md`

## Global Constraints

- Deutsch (Schweiz), ss statt ß, Du-Form, keine Ausrufezeichen, keine Klarnamen; Beispielfirma «Muster AG».
- Aufgabe enthält nur `INFO.md` und `9_Claude/wissen.md`.
- `wissen.md` beschreibt, was Claude weiss und tut — kein Satz, der vom Benutzer eine Handlung verlangt (die sagt Claude im Gespräch).
- Keine Platzhalter in dieser Aufgabe; `platzhalter.exe` kommt nicht vor.
- Kein Bezug auf einen bestimmten Kanton ausser als Quellenbeleg.
- Nur `anleitung/stelle.html` wird bei der Anleitung angefasst; kein CSS ausser seitenspezifisch; Links relativ (ausser externe).
- `build.py` bleibt ohne Abhängigkeiten und unverändert.

---

### Task 1: Grundgerüst — robuster Sitzungsbeginn

**Files:**
- Modify: `grundgeruest/CLAUDE.md` (Abschnitt «Sitzungsbeginn»)
- Modify: `grundgeruest/START-HIER.txt` (Schritt 4)

- [ ] **Step 1:** In `grundgeruest/CLAUDE.md` den ersten Absatz unter `## Sitzungsbeginn` ersetzen durch:

```markdown
Lies zuerst `9_Claude/stand.md`, egal mit welchem Satz die Session beginnt.
Ist etwas fällig oder überfällig, nenn es in einem Satz; dann erledige, worum
die Person bittet. Beginnt sie mit «Was steht an?», nenn alle offenen Punkte.
```

- [ ] **Step 2:** In `START-HIER.txt` nach `  4. Schreiben:   Was steht an?` die Zeile `     Oder einfach, was du willst. Claude weiss, wo du stehst.` einfügen (ASCII-Umschrift wie im Rest der Datei: keine Umlaute nötig in dieser Zeile).
- [ ] **Step 3:** `python build.py`; prüfen, dass `START-HIER.txt` im Zip mit BOM und CRLF beginnt:

```bash
python -c "import zipfile;d=zipfile.ZipFile('dist/stelle.zip').read('START-HIER.txt');print(d[:3]==b'\xef\xbb\xbf', b'\r\n' in d)"
```
Expected: `True True`

- [ ] **Step 4:** Commit `Grundgerüst: jeder Startsatz liest zuerst stand.md`.

### Task 2: `wissen.md` und `INFO.md` für `stelle`

**Files:**
- Modify (neu schreiben): `aufgaben/stelle/9_Claude/wissen.md`
- Modify: `aufgaben/stelle/INFO.md`

Gliederung von `wissen.md` (Inhalt je Abschnitt aus der Spezifikation, Abschnitt in Klammern):

1. `# Fachwissen: Stelle suchen` + ein Absatz Zweck (Stellensuche über Wochen/Monate, RAV optional).
2. `## Voraussetzung` — Lebenslauf in `1_Meine-Unterlagen`, Claude schreibt keinen; Zeugnisse, Diplome, optional Vorlage Motivationsschreiben; was nicht hineingehört (AHV-Ausweis, RAV-Verfügungen) — aus bestehender Fassung übernehmen und ergänzen.
3. `## Was du am Anfang fragst` — Beruf, Ort/Umkreis, RAV-Frage; Schalter `RAV:` in `stand.md` (Spec «Ein Schalter»).
4. `## Dateien, die du führst` — Baum und Zweck von `stand.md`, `suche-stellen.md`, `stellen.md` (Spec «Dateien, die Claude führt»).
5. `## Bewerbungsordner und Stand` — Status-Ordner, Namensregeln, Vermittler, Postausgang, Nachfassen (Spec «Status-Ordner»).
6. `## Suchen` — Suchprofil, Portale, Rhythmus, Nachsuchen beim Sessionstart, geplanter Lauf (Spec «Vorschläge», «Grenze der geplanten Suche»).
7. `## Vorschlagen und entscheiden` — nur Neues, Wiedervorlage mit Schwellen, Zuweisung RAV, Zumutbarkeit.
8. `## Keine Platzhalter` — Ausnahme zur Grundgerüst-Regel ausdrücklich; fehlende Angaben fragen und in `stand.md` speichern.
9. `## Bewerbung erstellen` — fünf Schritte, Versandweg, Gmail nur Entwurf, nie senden.
10. `## Rückmeldungen` — Sätze und was Claude verschiebt/notiert.
11. `## RAV-Monat` — Fakten mit Quellen-URL, Lieferungen in `rav/JJJJ-MM/`, Fristhinweise, Vermittlerregel, nie in Job-Room einloggen.
12. `## Projekt einrichten` — wann empfehlen, Vorlage der Felder, geplante Aufgabe mit Text, Grenzen.
13. `## Wohnung` — ein Satz: nicht Teil dieser Aufgabe, Verweis auf Aufgabe `wohnung`.
14. `## Wo du widersprichst` — Zuweisung, Zumutbarkeit, zu wenig Bemühungen, Vermittler-only, unrealistische Kriterien.

- [ ] **Step 1:** `wissen.md` nach dieser Gliederung schreiben.
- [ ] **Step 2:** `INFO.md` `kurz:` auf: `Stellen laufend suchen und nach deinem Lebenslauf bewerten, Bewerbungen nach Stand geordnet, Motivationsschreiben pro Stelle. Wenn du beim RAV bist: der Monatsnachweis dazu.`
- [ ] **Step 3:** Prüfen:

```bash
grep -n -i "wohnung\|platzhalter\|\[[A-Z]" aufgaben/stelle/9_Claude/wissen.md
grep -n -i "appenzell\|herisau\| AR \|Raschle" aufgaben/stelle/9_Claude/wissen.md
```
Expected: nur der Verweis-Satz auf `wohnung` und der Satz «Keine Platzhalter»; zweite Suche leer.
- [ ] **Step 4:** Gegenlesen auf Sätze mit Handlung für den Benutzer; umformulieren zu «Sag der Person …».
- [ ] **Step 5:** `python build.py`; `dist/stelle.zip` enthält `9_Claude/wissen.md` neuer Fassung.
- [ ] **Step 6:** Commit `stelle: Dauerbetrieb mit Status-Ordnern, RAV-Monat und Projekt`.

### Task 3: `anleitung/stelle.html`

**Files:**
- Modify (neu schreiben): `anleitung/stelle.html`

- [ ] **Step 1:** Kopf, Sidebar, Footer und Skript-Einbindung aus der bestehenden Datei übernehmen (Struktur unverändert, damit `anleitung.js` die Navigation einsetzt).
- [ ] **Step 2:** Download-Knopf (`.download`-Regel aus `platzhalter.html` in den Seiten-`<style>` kopieren) auf `https://stayingclean.github.io/ki-tasks/stelle.zip`.
- [ ] **Step 3:** Abschnitte laut Spezifikation: Kurzfassung · Was du brauchst · Der Start · Der Ablauf (Diagramm 1) · Projekt einrichten · Der Ordner (`.tree`) · Suchen · Bewerben · Der RAV-Monat (Diagramm 2) · Per Satz ändern · Was Claude nicht tut, wo er widerspricht · Ein Monat im Durchlauf (`.steps`).
- [ ] **Step 4:** Diagramm 1 als HTML/CSS-Flussdiagramm (Klassen `.fluss`, `.schritt`, `.ast`, `.opt`), Status-Kästen in den Farben der Ordner; RAV/Projekt-Teile gestrichelt (`.opt`). Diagramm 2 als Zeitleiste (`.monat`). Farben nur aus `stil.css`-Variablen.
- [ ] **Step 5:** Prüfen mit `stil.css` und `anleitung.js` von der veröffentlichten Toolbox in einem Scratch-Ordner, Browser-Pane bei Desktop- und 375-px-Breite: kein horizontales Scrollen der Seite, Diagramme lesbar.
- [ ] **Step 6:** Commit `Anleitung stelle: Ablauf, RAV-Monat und Projekt mit Diagrammen`.

### Task 4: Abschluss

- [ ] **Step 1:** `python build.py` sauber; Zip einmal entpacken und Baum ansehen.
- [ ] **Step 2:** `git diff origin/main --stat` — nur die Dateien aus Spec «Was sich an Dateien ändert» plus Spec/Plan.
