# ki-tasks

Repo mit Startordnern für Papierkram mit KI-Unterstützung. Aufbau und Regeln: README.md.

Leitidee: Der Mensch spricht, Claude schreibt die Dateien. Zielplattform ist
Claude Desktop → Cowork — keine Slash-Befehle, keine Skills, der einzige
automatische Haken ist `CLAUDE.md` im verbundenen Ordner.

Beim Arbeiten an diesem Repo:
- `grundgeruest/` ist die einzige Quelle für das Verhalten. Änderungen an den
  Regeln nur in `grundgeruest/CLAUDE.md`, nie in einer Aufgabe duplizieren.
- Eine Aufgabe in `aufgaben/<name>/` enthält nur: `INFO.md` und
  `9_Claude/wissen.md`. Nichts anderes.
- `wissen.md` beschreibt, was Claude wissen muss — nicht, was der Benutzer tun
  soll. Verlangt ein Satz eine Handlung vom Benutzer, gehört er ins Gespräch.
- Keine Datei, die der Benutzer ausfüllen muss. Was Claude braucht, erfragt es
  und schreibt es selbst nach `9_Claude/stand.md`.
- Ordnernamen im Grundgerüst: Deutsch, ohne Umlaute (ae/oe/ue), mit einstelliger
  Nummer in der Reihenfolge der Benutzung (1_Meine-Unterlagen … 3_Zum-Versenden);
  `9_Claude` ist Claudes Bereich und steht darum am Schluss.
- `build.py` hat keine Abhängigkeiten; das soll so bleiben (läuft in der Action
  mit blankem Python). `START-HIER.txt` muss mit BOM und CRLF ins Zip — der
  Build läuft auf Linux, die Datei landet in Notepad.
- `platzhalter/` ist ein eigenes uv-Projekt (Windows-Tool, EXE per PyInstaller).
  Befehle dort mit `uv run …`; nach Änderungen `uv run pytest`. Es hat nichts mit
  `build.py` zu tun. Der Ordner `verlauf` wird von der Suche ausgenommen, damit
  Archivfassungen nicht mitgefüllt werden.
- Nach jeder Änderung `python build.py` laufen lassen; `dist/` ist gitignored.
- Inhalte: Deutsch (Schweiz), Du-Form, keine echten Personendaten, keine
  Beispiele mit Klarnamen.
- `anleitung/` enthält `der-ordner.html` und `platzhalter.html` (beschreiben den
  Ordner), `aufgaben.html` und eine Seite je Aufgabe, benannt wie der
  Aufgabenordner: `aufgaben/<name>/` ↔ `anleitung/<name>.html`. Der Deploy von `stayingclean/toolbox` holt den Ordner beim Bauen und
  kopiert ihn nach `docs/claude-anleitung/`; die Seiten erscheinen darum unter
  der Toolbox-URL und nicht auf der Seite dieses Repos. Sie liegen hier, weil sie
  sich mit dem Ordner zusammen ändern müssen: Wer `grundgeruest/` umbaut, am
  Platzhalter-Tool etwas dreht oder ein `wissen.md` anpasst, zieht sie mit nach.
  Eine Aufgabenseite ist die Leseform des zugehörigen `wissen.md` — dieselbe
  Sache für einen Menschen; neue Regeln gehören trotzdem ins `wissen.md`, nicht
  auf die Seite. Aussehen und Navigation (`stil.css`, `anleitung.js`) kommen von
  drüben — hier kein eigener CSS-Block ausser für wirklich Seitenspezifisches,
  Links relativ. Navigation und Karten auf `aufgaben.html` setzt der Deploy drüben
  aus der Namenskonvention ein (`<h1>`, `<p class="lead">`, `reihenfolge:` in
  `INFO.md`; Details in der README). Der Lead wird wörtlich zum Kartentext und
  beschreibt darum die Aufgabe, nicht die Seite. Die Karten zwischen den Markern nicht von
  Hand pflegen. Nur eine Seite, die keine Aufgabe ist, muss drüben von Hand in
  `SEITEN`. Nach jedem Deploy hier stösst der Job `toolbox` den Deploy drüben an. `build.py` schaut in `anleitung/` nur nach, ob `<name>.html` existiert, und
  verlinkt die Karte der Download-Seite dann dorthin (Toolbox-URL); die Seiten gehören in
  keinen Zip.
- Die übrige Anleitung (Einstieg, Abos, Datenschutz, Prompts) bleibt im Repo
  `stayingclean/toolbox` unter `docs/claude-anleitung/`.
