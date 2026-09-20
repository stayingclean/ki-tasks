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
- `anleitung/` enthält die zwei Seiten, die den Ordner beschreiben
  (`der-ordner.html`, `platzhalter.html`). Der Deploy von `stayingclean/toolbox`
  holt den Ordner beim Bauen und kopiert ihn nach `docs/claude-anleitung/`; die
  Seiten erscheinen darum unter der Toolbox-URL und nicht auf der Seite dieses
  Repos. Sie liegen hier, weil sie sich mit dem Ordner zusammen ändern müssen:
  Wer `grundgeruest/` umbaut oder am Platzhalter-Tool etwas dreht, zieht sie mit
  nach. Aussehen und Navigation (`stil.css`, `anleitung.js`) kommen von drüben —
  hier kein eigener CSS-Block ausser für wirklich Seitenspezifisches, Links
  relativ. Eine neue Seite muss drüben in `anleitung.js` in die Liste `SEITEN`,
  sonst taucht sie in keiner Navigation auf. `build.py` fasst `anleitung/` nicht
  an; die Seiten gehören in keinen Zip.
- Die übrige Anleitung (Einstieg, Abos, Datenschutz, Prompts) bleibt im Repo
  `stayingclean/toolbox` unter `docs/claude-anleitung/`.
