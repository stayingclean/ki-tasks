# Platzhalter-Tool Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ein Windows-Programm (EXE), das in einem Ordner rekursiv alle `.docx` nach `[Platzhalter]` durchsucht, sie in einer Oberfläche zum Ausfüllen anzeigt und die ausgefüllten Werte in allen Dateien ersetzt.

**Architecture:** Eigenes uv-Projekt `platzhalter/` mit drei UI-freien Modulen (`dokument.py` iteriert Absätze, `suche.py` sammelt Platzhalter, `docx_ersetzen.py` ersetzt run-übergreifend) und einer pywebview-Oberfläche (`app.py` + `ui/index.html`). PyInstaller packt alles zu `platzhalter.exe`; ein Windows-Job im Pages-Workflow baut die EXE und legt sie in `dist/`.

**Tech Stack:** Python 3.12 (uv), python-docx, pywebview (Edge WebView2), pytest, PyInstaller, GitHub Actions.

**Spec:** `docs/superpowers/specs/2026-09-17-platzhalter-tool-design.md`

## Global Constraints

- Sprache: Deutsch (Schweiz), ss statt ß, Du-Form, keine Ausrufezeichen. Gilt für UI-Texte, README, Kommentare.
- Ordner- und Dateinamen ohne Umlaute. Funktionsnamen Deutsch wie in `build.py` (`kopiere_baum`, `lese_info`).
- `build.py` bleibt unverändert und ohne Abhängigkeiten.
- Platzhalter-Muster: `[Text]` ohne `[`, `]`, Zeilenumbruch oder Tab, 1 bis 80 Zeichen; Schlüssel ist der Text ohne Klammern; Gross-/Kleinschreibung wird unterschieden.
- Eingegebene Werte werden nirgends gespeichert.
- Vor dem Schreiben `<name>.docx.bak` anlegen; Original erst nach vollständigem Schreiben einer temporären Datei ersetzen.
- Alle Befehle aus `platzhalter/` mit `uv run …` ausführen.

---

### Task 1: Projekt-Gerüst mit uv

**Files:**
- Create: `platzhalter/pyproject.toml`
- Create: `platzhalter/.python-version`
- Create: `platzhalter/src/platzhalter/__init__.py`
- Create: `platzhalter/tests/test_paket.py`
- Modify: `.gitignore`

**Interfaces:**
- Produces: importierbares Paket `platzhalter` (src-Layout), `uv run pytest` läuft.

- [ ] **Step 1: pyproject.toml schreiben**

```toml
[project]
name = "platzhalter"
version = "0.1.0"
description = "Platzhalter in Word-Dateien finden und ersetzen"
requires-python = ">=3.12"
dependencies = [
    "pywebview>=5.0",
    "python-docx>=1.1",
]

[dependency-groups]
dev = [
    "pytest>=8",
    "pyinstaller>=6",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/platzhalter"]

[tool.pytest.ini_options]
testpaths = ["tests"]
```

- [ ] **Step 2: .python-version und Paket anlegen**

`platzhalter/.python-version`:
```
3.12
```

`platzhalter/src/platzhalter/__init__.py`:
```python
"""Platzhalter in Word-Dateien finden und ersetzen."""
```

- [ ] **Step 3: .gitignore ergänzen** (Root, an bestehende Zeilen anhängen)

```
build/
.venv/
*.egg-info/
.pytest_cache/
```

- [ ] **Step 4: Smoke-Test schreiben**

`platzhalter/tests/test_paket.py`:
```python
import platzhalter


def test_paket_importierbar():
    assert platzhalter.__doc__
```

- [ ] **Step 5: uv sync und Test ausführen**

Run: `cd platzhalter && uv sync && uv run pytest -v`
Expected: 1 passed. `uv.lock` und `.venv/` entstehen.

- [ ] **Step 6: Commit**

```bash
git add .gitignore platzhalter/pyproject.toml platzhalter/.python-version platzhalter/uv.lock platzhalter/src/platzhalter/__init__.py platzhalter/tests/test_paket.py
git commit -m "Platzhalter-Tool: uv-Projektgeruest"
```

---

### Task 2: Absätze iterieren und Platzhalter suchen

**Files:**
- Create: `platzhalter/src/platzhalter/dokument.py`
- Create: `platzhalter/src/platzhalter/suche.py`
- Test: `platzhalter/tests/test_suche.py`

**Interfaces:**
- Produces:
  - `dokument.MUSTER: re.Pattern` (Gruppe 1 = Name ohne Klammern)
  - `dokument.alle_absaetze(doc: docx.document.Document) -> Iterator[CT_P]` (Body inkl. Tabellen/Textfelder, alle Kopf- und Fusszeilen)
  - `dokument.runs(p: CT_P) -> list[docx.text.run.Run]` (direkte Runs und Runs in Hyperlinks)
  - `dokument.absatz_text(p: CT_P) -> str`
  - `suche.finde_docx(ordner: Path) -> list[Path]`
  - `suche.durchsuche(ordner: Path) -> Suchergebnis` mit `Suchergebnis(ordner: str, dateien: list[str], platzhalter: list[Fund], fehler: list[str])`, `Fund(name: str, anzahl: int, dateien: list[str])`; Pfade relativ zum Ordner, POSIX-Schreibweise.

- [ ] **Step 1: Failing tests schreiben**

`platzhalter/tests/test_suche.py`:
```python
from pathlib import Path

from docx import Document

from platzhalter.dokument import MUSTER, absatz_text, alle_absaetze
from platzhalter.suche import durchsuche, finde_docx


def speichere(pfad: Path, *absaetze: str) -> Path:
    doc = Document()
    for a in absaetze:
        doc.add_paragraph(a)
    pfad.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(pfad))
    return pfad


def test_muster_findet_platzhalter():
    assert MUSTER.findall("Hallo [ADRESSE], [Ort] und [AHV]") == ["ADRESSE", "Ort", "AHV"]


def test_muster_ignoriert_leere_verschachtelte_und_umbrueche():
    assert MUSTER.findall("[] [[x]] [a\nb] [a\tb]") == ["x"]


def test_muster_begrenzt_laenge():
    assert MUSTER.findall("[" + "x" * 80 + "]") == ["x" * 80]
    assert MUSTER.findall("[" + "x" * 81 + "]") == []


def test_finde_docx_rekursiv_und_ueberspringt_sperr_und_sicherungsdateien(tmp_path):
    speichere(tmp_path / "a.docx", "x")
    speichere(tmp_path / "unter" / "tief" / "b.docx", "x")
    speichere(tmp_path / "~$a.docx", "x")
    (tmp_path / "a.docx.bak").write_bytes(b"egal")
    (tmp_path / "notiz.txt").write_text("egal")
    gefunden = finde_docx(tmp_path)
    assert [p.relative_to(tmp_path).as_posix() for p in gefunden] == ["a.docx", "unter/tief/b.docx"]


def test_alle_absaetze_umfasst_tabelle_und_kopfzeile(tmp_path):
    doc = Document()
    doc.add_paragraph("Body [A]")
    doc.add_table(rows=1, cols=1).cell(0, 0).text = "Zelle [B]"
    doc.sections[0].header.paragraphs[0].text = "Kopf [C]"
    doc.sections[0].footer.paragraphs[0].text = "Fuss [D]"
    texte = [absatz_text(p) for p in alle_absaetze(doc)]
    assert "Body [A]" in texte
    assert "Zelle [B]" in texte
    assert "Kopf [C]" in texte
    assert "Fuss [D]" in texte


def test_durchsuche_zaehlt_und_sortiert(tmp_path):
    speichere(tmp_path / "eins.docx", "[ADRESSE] und [ADRESSE]", "[Ort]")
    speichere(tmp_path / "sub" / "zwei.docx", "[ADRESSE]", "[AHV]")
    e = durchsuche(tmp_path)
    assert e.ordner == str(tmp_path)
    assert e.dateien == ["eins.docx", "sub/zwei.docx"]
    assert e.fehler == []
    assert [(f.name, f.anzahl, f.dateien) for f in e.platzhalter] == [
        ("ADRESSE", 3, ["eins.docx", "sub/zwei.docx"]),
        ("AHV", 1, ["sub/zwei.docx"]),
        ("Ort", 1, ["eins.docx"]),
    ]


def test_durchsuche_meldet_kaputte_datei(tmp_path):
    (tmp_path / "kaputt.docx").write_bytes(b"kein zip")
    speichere(tmp_path / "ok.docx", "[X]")
    e = durchsuche(tmp_path)
    assert e.dateien == ["ok.docx"]
    assert len(e.fehler) == 1 and e.fehler[0].startswith("kaputt.docx: ")
    assert [f.name for f in e.platzhalter] == ["X"]
```

- [ ] **Step 2: Tests ausführen, Fehlschlag prüfen**

Run: `cd platzhalter && uv run pytest tests/test_suche.py -v`
Expected: FAIL mit `ModuleNotFoundError: No module named 'platzhalter.dokument'`

- [ ] **Step 3: dokument.py schreiben**

```python
"""Zugriff auf Absätze und Runs einer .docx, unabhängig von Suche und Ersetzung."""
from __future__ import annotations

import re
from collections.abc import Iterator

from docx.document import Document as DocumentTyp
from docx.opc.constants import RELATIONSHIP_TYPE as RT
from docx.oxml.ns import qn
from docx.text.run import Run

# [Name] ohne Klammern, Zeilenumbruch oder Tab, 1 bis 80 Zeichen. Gruppe 1 = Name.
MUSTER = re.compile(r"\[([^\[\]\r\n\t]{1,80})\]")


def alle_absaetze(doc: DocumentTyp) -> Iterator:
    """Alle w:p im Textkörper (auch Tabellen, Textfelder) und in Kopf- und Fusszeilen."""
    yield from doc.element.body.iter(qn("w:p"))
    for rel in doc.part.rels.values():
        if rel.reltype in (RT.HEADER, RT.FOOTER):
            yield from rel.target_part.element.iter(qn("w:p"))


def runs(p) -> list[Run]:
    """Direkte Runs des Absatzes und Runs in Hyperlinks, in Dokumentreihenfolge.
    Bewusst nicht p.iter(): Textfelder liegen als eigene Absätze in einem Run."""
    return [Run(r, None) for r in p.xpath("./w:r | ./w:hyperlink/w:r")]


def absatz_text(p) -> str:
    return "".join(r.text for r in runs(p))
```

- [ ] **Step 4: suche.py schreiben**

```python
"""Alle .docx eines Ordners finden und die Platzhalter darin zählen."""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

from docx import Document

from platzhalter.dokument import MUSTER, absatz_text, alle_absaetze


@dataclass
class Fund:
    name: str
    anzahl: int
    dateien: list[str]


@dataclass
class Suchergebnis:
    ordner: str
    dateien: list[str] = field(default_factory=list)
    platzhalter: list[Fund] = field(default_factory=list)
    fehler: list[str] = field(default_factory=list)


def finde_docx(ordner: Path) -> list[Path]:
    """Rekursiv alle .docx, ohne Word-Sperrdateien (~$…). .bak fällt weg, weil die Endung nicht passt."""
    return sorted(
        p for p in ordner.rglob("*.docx")
        if p.is_file() and not p.name.startswith("~$")
    )


def durchsuche(ordner: Path) -> Suchergebnis:
    ergebnis = Suchergebnis(ordner=str(ordner))
    zaehler: dict[str, Counter[str]] = {}
    for pfad in finde_docx(ordner):
        rel = pfad.relative_to(ordner).as_posix()
        try:
            doc = Document(str(pfad))
        except Exception as e:  # beschädigt, kein Zip, kein Word-Paket
            ergebnis.fehler.append(f"{rel}: {e}")
            continue
        ergebnis.dateien.append(rel)
        for p in alle_absaetze(doc):
            for name in MUSTER.findall(absatz_text(p)):
                zaehler.setdefault(name, Counter())[rel] += 1
    ergebnis.platzhalter = sorted(
        (Fund(name, sum(c.values()), sorted(c)) for name, c in zaehler.items()),
        key=lambda f: (-f.anzahl, f.name.lower(), f.name),
    )
    return ergebnis
```

- [ ] **Step 5: Tests ausführen**

Run: `cd platzhalter && uv run pytest tests/test_suche.py -v`
Expected: 7 passed

- [ ] **Step 6: Commit**

```bash
git add platzhalter/src/platzhalter/dokument.py platzhalter/src/platzhalter/suche.py platzhalter/tests/test_suche.py
git commit -m "Platzhalter-Tool: Absaetze iterieren und Platzhalter suchen"
```

---

### Task 3: Platzhalter in einer Datei ersetzen

**Files:**
- Create: `platzhalter/src/platzhalter/docx_ersetzen.py`
- Test: `platzhalter/tests/test_docx_ersetzen.py`

**Interfaces:**
- Consumes: `dokument.MUSTER`, `dokument.alle_absaetze`, `dokument.runs`
- Produces:
  - `docx_ersetzen.ersetze_im_absatz(p, werte: dict[str, str]) -> int`
  - `docx_ersetzen.ersetze_in_datei(pfad: Path, werte: dict[str, str]) -> int` (Anzahl Ersetzungen; 0 = Datei unangetastet, keine .bak; wirft OSError/PermissionError bei gesperrter Datei)

- [ ] **Step 1: Failing tests schreiben**

`platzhalter/tests/test_docx_ersetzen.py`:
```python
from pathlib import Path

from docx import Document

from platzhalter.dokument import absatz_text, alle_absaetze
from platzhalter.docx_ersetzen import ersetze_im_absatz, ersetze_in_datei


def absatz_mit_runs(*teile: str):
    doc = Document()
    p = doc.add_paragraph()
    for t in teile:
        p.add_run(t)
    return p


def test_platzhalter_in_einem_run():
    p = absatz_mit_runs("Wohnhaft an [ADRESSE].")
    assert ersetze_im_absatz(p._p, {"ADRESSE": "Musterweg 1"}) == 1
    assert p.text == "Wohnhaft an Musterweg 1."


def test_platzhalter_ueber_drei_runs_verteilt():
    p = absatz_mit_runs("Hallo [AD", "RES", "SE], danke")
    assert ersetze_im_absatz(p._p, {"ADRESSE": "Musterweg 1"}) == 1
    assert p.text == "Hallo Musterweg 1, danke"
    assert [r.text for r in p.runs] == ["Hallo Musterweg 1", "", ", danke"]


def test_zwei_vorkommen_im_selben_absatz():
    p = absatz_mit_runs("[A] und [A] und [B]")
    assert ersetze_im_absatz(p._p, {"A": "eins", "B": "zwei"}) == 3
    assert p.text == "eins und eins und zwei"


def test_leerer_oder_fehlender_wert_bleibt_stehen():
    p = absatz_mit_runs("[A] [B] [C]")
    assert ersetze_im_absatz(p._p, {"A": "", "B": "x"}) == 1
    assert p.text == "[A] x [C]"


def test_formatierung_des_ersten_runs_bleibt():
    p = absatz_mit_runs("Name: ", "[NA", "ME]")
    p.runs[1].bold = True
    ersetze_im_absatz(p._p, {"NAME": "Muster"})
    assert p.runs[0].text == "Name: " and p.runs[0].bold is None
    assert p.runs[1].text == "Muster" and p.runs[1].bold is True


def test_tab_im_run_bleibt_erhalten():
    p = absatz_mit_runs("Name:\t[NAME]")
    ersetze_im_absatz(p._p, {"NAME": "Muster"})
    assert p.text == "Name:\tMuster"


def test_ersetze_in_datei_tabelle_kopfzeile_und_sicherung(tmp_path: Path):
    pfad = tmp_path / "brief.docx"
    doc = Document()
    doc.add_paragraph("Sehr geehrte [ANREDE]")
    doc.add_table(rows=1, cols=1).cell(0, 0).text = "IBAN: [IBAN]"
    doc.sections[0].header.paragraphs[0].text = "[NAME], [ADRESSE]"
    doc.save(str(pfad))

    n = ersetze_in_datei(pfad, {"ANREDE": "Frau Muster", "IBAN": "CH00", "NAME": "M", "ADRESSE": ""})

    assert n == 3
    texte = [absatz_text(p) for p in alle_absaetze(Document(str(pfad)))]
    assert "Sehr geehrte Frau Muster" in texte
    assert "IBAN: CH00" in texte
    assert "M, [ADRESSE]" in texte
    assert (tmp_path / "brief.docx.bak").exists()
    assert not (tmp_path / "brief.docx.tmp").exists()
    assert "[ANREDE]" in [absatz_text(p) for p in alle_absaetze(Document(str(tmp_path / "brief.docx.bak")))][0]


def test_ersetze_in_datei_ohne_treffer_laesst_datei_unveraendert(tmp_path: Path):
    pfad = tmp_path / "x.docx"
    doc = Document()
    doc.add_paragraph("[A]")
    doc.save(str(pfad))
    vorher = pfad.read_bytes()

    assert ersetze_in_datei(pfad, {"B": "x", "A": ""}) == 0
    assert pfad.read_bytes() == vorher
    assert not (tmp_path / "x.docx.bak").exists()
```

- [ ] **Step 2: Tests ausführen, Fehlschlag prüfen**

Run: `cd platzhalter && uv run pytest tests/test_docx_ersetzen.py -v`
Expected: FAIL mit `ModuleNotFoundError: No module named 'platzhalter.docx_ersetzen'`

- [ ] **Step 3: docx_ersetzen.py schreiben**

```python
"""Platzhalter in einer .docx ersetzen, auch wenn Word sie auf mehrere Runs verteilt hat."""
from __future__ import annotations

import os
import shutil
from pathlib import Path

from docx import Document

from platzhalter.dokument import MUSTER, alle_absaetze, runs


def ersetze_im_absatz(p, werte: dict[str, str]) -> int:
    """Ersetzt alle Platzhalter mit nicht leerem Wert. Gibt die Anzahl Ersetzungen zurück.

    Der Absatztext wird aus den Runs zusammengesetzt. Jede Fundstelle wird von hinten nach
    vorn bearbeitet, damit die einmal berechneten Offsets gültig bleiben: Der Wert kommt
    in den ersten betroffenen Run, die weiteren betroffenen Runs werden gekürzt oder geleert.
    """
    alle = runs(p)
    texte = [r.text for r in alle]
    ganz = "".join(texte)
    funde = [m for m in MUSTER.finditer(ganz) if werte.get(m.group(1))]
    if not funde:
        return 0

    offsets = [0]
    for t in texte:
        offsets.append(offsets[-1] + len(t))

    def run_index(pos: int, ende: bool) -> int:
        # ende=False: Run, der das Zeichen an pos enthält. ende=True: Run, der das Zeichen vor pos enthält.
        for i in range(len(texte)):
            if ende and offsets[i] < pos <= offsets[i + 1]:
                return i
            if not ende and offsets[i] <= pos < offsets[i + 1]:
                return i
        raise ValueError("Position ausserhalb des Absatzes")

    neu = list(texte)
    for m in reversed(funde):
        start, ende = m.span()
        wert = werte[m.group(1)]
        i, j = run_index(start, False), run_index(ende, True)
        if i == j:
            neu[i] = neu[i][: start - offsets[i]] + wert + neu[i][ende - offsets[i] :]
        else:
            neu[i] = neu[i][: start - offsets[i]] + wert
            for k in range(i + 1, j):
                neu[k] = ""
            neu[j] = neu[j][ende - offsets[j] :]

    for r, alt, frisch in zip(alle, texte, neu):
        if alt != frisch:
            r.text = frisch
    return len(funde)


def ersetze_in_datei(pfad: Path, werte: dict[str, str]) -> int:
    """Ersetzt in einer Datei. Ohne Treffer bleibt sie unangetastet. Sonst: .bak anlegen,
    in .tmp schreiben, dann das Original ersetzen. Fehler lassen das Original unverändert."""
    werte = {k: v for k, v in werte.items() if v}
    if not werte:
        return 0
    doc = Document(str(pfad))
    anzahl = sum(ersetze_im_absatz(p, werte) for p in alle_absaetze(doc))
    if anzahl == 0:
        return 0
    shutil.copy2(pfad, pfad.with_name(pfad.name + ".bak"))
    tmp = pfad.with_name(pfad.name + ".tmp")
    try:
        doc.save(str(tmp))
        os.replace(tmp, pfad)
    finally:
        if tmp.exists():
            tmp.unlink()
    return anzahl
```

- [ ] **Step 4: Tests ausführen**

Run: `cd platzhalter && uv run pytest -v`
Expected: alle Tests passed (1 + 7 + 8 = 16)

- [ ] **Step 5: Commit**

```bash
git add platzhalter/src/platzhalter/docx_ersetzen.py platzhalter/tests/test_docx_ersetzen.py
git commit -m "Platzhalter-Tool: Ersetzung ueber Run-Grenzen, .bak und atomares Schreiben"
```

---

### Task 4: Oberfläche mit pywebview

**Files:**
- Create: `platzhalter/src/platzhalter/app.py`
- Create: `platzhalter/src/platzhalter/__main__.py`
- Create: `platzhalter/src/platzhalter/ui/index.html`
- Test: `platzhalter/tests/test_app.py` (nur die Api-Klasse, ohne Fenster)

**Interfaces:**
- Consumes: `suche.durchsuche`, `docx_ersetzen.ersetze_in_datei`
- Produces:
  - `app.Api(ordner: Path | None)` mit Methoden `hole_ordner() -> str | None`, `waehle_ordner() -> str | None`, `suche() -> dict` (asdict von Suchergebnis), `ersetze(werte: dict[str, str]) -> list[dict]` (`{datei, ersetzt, fehler}` je durchsuchter Datei), `beende() -> None`
  - `app.starte(ordner: Path | None) -> None`
  - `python -m platzhalter [ordner]`

- [ ] **Step 1: Failing test für die Api schreiben**

`platzhalter/tests/test_app.py`:
```python
from pathlib import Path

from docx import Document

from platzhalter.app import Api


def speichere(pfad: Path, text: str) -> None:
    doc = Document()
    doc.add_paragraph(text)
    doc.save(str(pfad))


def test_api_suche_und_ersetze(tmp_path: Path):
    speichere(tmp_path / "a.docx", "[A] [B]")
    speichere(tmp_path / "b.docx", "[B]")
    api = Api(tmp_path)

    assert api.hole_ordner() == str(tmp_path)
    ergebnis = api.suche()
    assert ergebnis["dateien"] == ["a.docx", "b.docx"]
    assert [p["name"] for p in ergebnis["platzhalter"]] == ["B", "A"]

    resultate = api.ersetze({"A": "eins", "B": ""})
    assert resultate == [
        {"datei": "a.docx", "ersetzt": 1, "fehler": None},
        {"datei": "b.docx", "ersetzt": 0, "fehler": None},
    ]


def test_api_ersetze_meldet_fehler_pro_datei(tmp_path: Path):
    speichere(tmp_path / "a.docx", "[A]")
    api = Api(tmp_path)
    api.suche()
    (tmp_path / "a.docx").write_bytes(b"jetzt kaputt")
    resultate = api.ersetze({"A": "x"})
    assert resultate[0]["datei"] == "a.docx"
    assert resultate[0]["ersetzt"] == 0
    assert resultate[0]["fehler"]
```

- [ ] **Step 2: Test ausführen, Fehlschlag prüfen**

Run: `cd platzhalter && uv run pytest tests/test_app.py -v`
Expected: FAIL mit `ModuleNotFoundError: No module named 'platzhalter.app'`

- [ ] **Step 3: app.py schreiben**

```python
"""pywebview-Fenster und die Python-Seite der Oberfläche."""
from __future__ import annotations

from dataclasses import asdict
from importlib.resources import files
from pathlib import Path

from platzhalter.docx_ersetzen import ersetze_in_datei
from platzhalter.suche import durchsuche

TITEL = "Platzhalter einsetzen"


class Api:
    """Wird von JavaScript über window.pywebview.api aufgerufen. Werte werden nie gespeichert."""

    def __init__(self, ordner: Path | None) -> None:
        self.ordner = ordner
        self.dateien: list[str] = []
        self.fenster = None  # wird von starte() gesetzt

    def hole_ordner(self) -> str | None:
        return str(self.ordner) if self.ordner else None

    def waehle_ordner(self) -> str | None:
        import webview

        auswahl = self.fenster.create_file_dialog(webview.FOLDER_DIALOG)
        if not auswahl:
            return None
        self.ordner = Path(auswahl[0])
        return str(self.ordner)

    def suche(self) -> dict:
        ergebnis = durchsuche(self.ordner)
        self.dateien = ergebnis.dateien
        return asdict(ergebnis)

    def ersetze(self, werte: dict[str, str]) -> list[dict]:
        resultate = []
        for rel in self.dateien:
            try:
                n = ersetze_in_datei(self.ordner / rel, werte)
                resultate.append({"datei": rel, "ersetzt": n, "fehler": None})
            except Exception as e:  # gesperrt, beschädigt, kein Schreibrecht
                resultate.append({"datei": rel, "ersetzt": 0, "fehler": str(e)})
        return resultate

    def beende(self) -> None:
        if self.fenster:
            self.fenster.destroy()


def lade_html() -> str:
    return (files("platzhalter") / "ui" / "index.html").read_text(encoding="utf-8")


def starte(ordner: Path | None) -> None:
    import webview

    api = Api(ordner)
    api.fenster = webview.create_window(
        TITEL, html=lade_html(), js_api=api, width=900, height=700, min_size=(640, 480)
    )
    webview.start()
```

- [ ] **Step 4: __main__.py schreiben**

```python
"""Aufruf: python -m platzhalter [ordner]"""
from __future__ import annotations

import sys
from pathlib import Path

from platzhalter.app import starte


def main(argv: list[str] | None = None) -> None:
    args = sys.argv[1:] if argv is None else argv
    ordner = Path(args[0]).resolve() if args else None
    if ordner is not None and not ordner.is_dir():
        sys.exit(f"Kein Ordner: {ordner}")
    starte(ordner)


if __name__ == "__main__":
    main()
```

- [ ] **Step 5: Test ausführen**

Run: `cd platzhalter && uv run pytest tests/test_app.py -v`
Expected: 2 passed

- [ ] **Step 6: ui/index.html schreiben**

Vier Ansichten (`start`, `laden`, `liste`, `ergebnis`), ein Bestätigungs-Dialog. Farben wie `dist/index.html` (Teal). Volle Datei:

```html
<!DOCTYPE html>
<html lang="de"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Platzhalter einsetzen</title>
<style>
:root{--bg:#FAF8F5;--card:#fff;--border:#E8E4DF;--text:#1C1C1C;--muted:#7A7268;--accent:#008080;--accent-dark:#006666;--tint:#E6F2F2;--rot:#B3261E;--rot-tint:#FBEAE8}
*{box-sizing:border-box}html,body{height:100%}body{margin:0;font-family:Inter,-apple-system,"Segoe UI",Roboto,sans-serif;background:var(--bg);color:var(--text);line-height:1.5;display:flex;flex-direction:column}
header{padding:20px 28px 12px;border-bottom:1px solid var(--border);background:var(--card)}
h1{font-family:Georgia,serif;color:var(--accent-dark);font-size:1.5rem;margin:0}
.pfad{color:var(--muted);font-size:.85rem;margin-top:4px;display:flex;gap:10px;align-items:center;flex-wrap:wrap}
.pfad code{background:var(--bg);border:1px solid var(--border);padding:1px 6px;border-radius:6px;font-size:.85em;word-break:break-all}
main{flex:1;overflow:auto;padding:20px 28px}
.view{display:none}.view.aktiv{display:block}
.box{background:var(--tint);border-left:4px solid var(--accent);padding:12px 16px;border-radius:0 12px 12px 0;margin:0 0 18px}
.box.rot{background:var(--rot-tint);border-color:var(--rot)}
button{font:inherit;border-radius:12px;padding:10px 18px;border:1px solid var(--border);background:var(--card);color:var(--accent-dark);cursor:pointer;font-weight:600}
button:hover{border-color:var(--accent)}button.primaer{background:var(--accent);color:#fff;border-color:var(--accent)}
button.primaer:hover{background:var(--accent-dark)}button:disabled{opacity:.45;cursor:default}
a.link{color:var(--accent);cursor:pointer;text-decoration:underline;background:none;border:0;padding:0;font-weight:500}
.zentriert{text-align:center;padding:60px 20px;color:var(--muted)}
.karte{background:var(--card);border:1px solid var(--border);border-radius:14px;padding:14px 18px;margin-bottom:10px}
.zeile{display:grid;grid-template-columns:minmax(140px,1fr) 2fr;gap:14px;align-items:center}
.name{font-family:Consolas,monospace;font-weight:600;color:var(--accent-dark);word-break:break-all}
.meta{color:var(--muted);font-size:.82rem;margin-top:2px}
input[type=text]{font:inherit;width:100%;padding:9px 12px;border:1px solid var(--border);border-radius:10px;background:var(--bg)}
input[type=text]:focus{outline:2px solid var(--accent);border-color:var(--accent);background:#fff}
.dateien{display:none;margin:8px 0 0;padding:0 0 0 18px;color:var(--muted);font-size:.82rem}
.karte.offen .dateien{display:block}
footer{padding:14px 28px;border-top:1px solid var(--border);background:var(--card);display:flex;justify-content:space-between;align-items:center;gap:12px}
footer .info{color:var(--muted);font-size:.9rem}
table{width:100%;border-collapse:collapse;background:var(--card);border:1px solid var(--border);border-radius:14px;overflow:hidden}
td,th{text-align:left;padding:10px 14px;border-bottom:1px solid var(--border);font-size:.92rem;vertical-align:top}
th{color:var(--muted);font-weight:600;font-size:.8rem;text-transform:uppercase;letter-spacing:.06em}
tr:last-child td{border-bottom:0}.fehler{color:var(--rot)}.ok{color:var(--accent-dark)}
.schleier{position:fixed;inset:0;background:rgba(28,28,28,.4);display:none;align-items:center;justify-content:center;padding:20px}
.schleier.aktiv{display:flex}
.dialog{background:var(--card);border-radius:16px;padding:22px 26px;max-width:480px;width:100%;box-shadow:0 12px 40px rgba(0,0,0,.2)}
.dialog h2{margin:0 0 10px;font-size:1.1rem;color:var(--accent-dark)}.dialog p{margin:0 0 8px}
.dialog .knoepfe{display:flex;justify-content:flex-end;gap:10px;margin-top:18px}
.spinner{width:36px;height:36px;border:4px solid var(--border);border-top-color:var(--accent);border-radius:50%;animation:dreh 1s linear infinite;margin:0 auto 14px}
@keyframes dreh{to{transform:rotate(360deg)}}
</style></head><body>
<header>
  <h1>Platzhalter einsetzen</h1>
  <div class="pfad"><span id="pfad-text">Kein Ordner gewählt</span><button class="link" id="anderer-ordner" type="button">Anderer Ordner</button></div>
</header>
<main>
  <section id="view-start" class="view">
    <div class="zentriert">
      <p>Wähle den Ordner mit den Word-Dateien. Alle Unterordner werden mitdurchsucht.</p>
      <button class="primaer" id="ordner-waehlen" type="button">Ordner wählen</button>
    </div>
  </section>
  <section id="view-laden" class="view">
    <div class="zentriert"><div class="spinner"></div><p id="laden-text">Durchsuche Word-Dateien</p></div>
  </section>
  <section id="view-liste" class="view">
    <div id="hinweise"></div>
    <div id="karten"></div>
  </section>
  <section id="view-ergebnis" class="view">
    <div class="box" id="ergebnis-kopf"></div>
    <table><thead><tr><th>Datei</th><th>Ergebnis</th></tr></thead><tbody id="ergebnis-zeilen"></tbody></table>
  </section>
</main>
<footer>
  <span class="info" id="fuss-info"></span>
  <span>
    <button id="knopf-fertig" type="button" style="display:none">Fertig</button>
    <button class="primaer" id="knopf-ersetzen" type="button" disabled>Ersetzen</button>
  </span>
</footer>
<div class="schleier" id="schleier">
  <div class="dialog">
    <h2>Werte einsetzen</h2>
    <p id="dialog-text"></p>
    <p class="meta">Leere Felder bleiben als Platzhalter stehen. Von jeder geänderten Datei wird vorher eine Sicherung mit Endung .bak angelegt. Die eingegebenen Werte werden nicht gespeichert.</p>
    <div class="knoepfe"><button id="dialog-abbrechen" type="button">Abbrechen</button><button class="primaer" id="dialog-ok" type="button">Ersetzen</button></div>
  </div>
</div>
<script>
const $ = (id) => document.getElementById(id);
const api = () => window.pywebview.api;
let ergebnis = null;

function zeige(name) {
  document.querySelectorAll('.view').forEach(v => v.classList.toggle('aktiv', v.id === 'view-' + name));
  $('knopf-ersetzen').style.display = name === 'liste' ? '' : 'none';
  $('knopf-fertig').style.display = name === 'ergebnis' ? '' : 'none';
  if (name !== 'liste') $('fuss-info').textContent = '';
}

function escapeHtml(s) {
  return String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
}

function plural(n, eins, viele) { return n + ' ' + (n === 1 ? eins : viele); }

async function start() {
  const ordner = await api().hole_ordner();
  if (ordner) return suchen(ordner);
  await ordnerWaehlen();
}

async function ordnerWaehlen() {
  const ordner = await api().waehle_ordner();
  if (ordner) suchen(ordner); else if (!ergebnis) zeige('start');
}

async function suchen(ordner) {
  $('pfad-text').innerHTML = '<code>' + escapeHtml(ordner) + '</code>';
  zeige('laden');
  ergebnis = await api().suche();
  zeigeListe();
}

function zeigeListe() {
  const hinweise = [];
  if (ergebnis.fehler.length) hinweise.push('<div class="box rot">Nicht lesbar: ' + ergebnis.fehler.map(escapeHtml).join('<br>') + '</div>');
  if (!ergebnis.dateien.length) hinweise.push('<div class="box">Keine Word-Dateien (.docx) in diesem Ordner gefunden.</div>');
  else if (!ergebnis.platzhalter.length) hinweise.push('<div class="box">' + plural(ergebnis.dateien.length, 'Datei', 'Dateien') + ' durchsucht, keine Platzhalter in eckigen Klammern gefunden.</div>');
  else hinweise.push('<div class="box">' + plural(ergebnis.platzhalter.length, 'Platzhalter', 'Platzhalter') + ' in ' + plural(ergebnis.dateien.length, 'Datei', 'Dateien') + '. Fülle aus, was du ersetzen willst.</div>');
  $('hinweise').innerHTML = hinweise.join('');
  $('karten').innerHTML = ergebnis.platzhalter.map((p, i) => `
    <div class="karte" data-i="${i}">
      <div class="zeile">
        <div><div class="name">[${escapeHtml(p.name)}]</div>
          <div class="meta">${p.anzahl}× in ${plural(p.dateien.length, 'Datei', 'Dateien')} · <button class="link toggle" type="button">anzeigen</button></div></div>
        <input type="text" data-name="${escapeHtml(p.name)}" autocomplete="off" spellcheck="false" placeholder="Wert für ${escapeHtml(p.name)}">
      </div>
      <ul class="dateien">${p.dateien.map(d => '<li>' + escapeHtml(d) + '</li>').join('')}</ul>
    </div>`).join('');
  document.querySelectorAll('.toggle').forEach(b => b.addEventListener('click', () => {
    const k = b.closest('.karte'); k.classList.toggle('offen'); b.textContent = k.classList.contains('offen') ? 'ausblenden' : 'anzeigen';
  }));
  document.querySelectorAll('input[data-name]').forEach(inp => inp.addEventListener('input', aktualisiereFuss));
  zeige('liste');
  aktualisiereFuss();
  const erster = document.querySelector('input[data-name]'); if (erster) erster.focus();
}

function werte() {
  const w = {};
  document.querySelectorAll('input[data-name]').forEach(inp => { w[inp.dataset.name] = inp.value.trim(); });
  return w;
}

function statistik() {
  const w = werte();
  const namen = Object.keys(w).filter(n => w[n]);
  const dateien = new Set();
  ergebnis.platzhalter.filter(p => namen.includes(p.name)).forEach(p => p.dateien.forEach(d => dateien.add(d)));
  return { namen, dateien: dateien.size };
}

function aktualisiereFuss() {
  const s = statistik();
  $('knopf-ersetzen').disabled = s.namen.length === 0;
  $('fuss-info').textContent = s.namen.length ? plural(s.namen.length, 'Platzhalter', 'Platzhalter') + ' ausgefüllt, betrifft ' + plural(s.dateien, 'Datei', 'Dateien') : 'Noch nichts ausgefüllt';
}

async function ersetzen() {
  $('schleier').classList.remove('aktiv');
  $('laden-text').textContent = 'Setze Werte ein';
  zeige('laden');
  const resultate = await api().ersetze(werte());
  const gesamt = resultate.reduce((a, r) => a + r.ersetzt, 0);
  const fehler = resultate.filter(r => r.fehler).length;
  $('ergebnis-kopf').className = 'box' + (fehler ? ' rot' : '');
  $('ergebnis-kopf').textContent = plural(gesamt, 'Ersetzung', 'Ersetzungen') + ' in ' + plural(resultate.filter(r => r.ersetzt).length, 'Datei', 'Dateien') + (fehler ? ', ' + plural(fehler, 'Datei', 'Dateien') + ' mit Fehler' : '') + '.';
  $('ergebnis-zeilen').innerHTML = resultate.map(r => '<tr><td>' + escapeHtml(r.datei) + '</td><td>' +
    (r.fehler ? '<span class="fehler">Fehler: ' + escapeHtml(r.fehler) + '</span>' : r.ersetzt ? '<span class="ok">' + plural(r.ersetzt, 'Ersetzung', 'Ersetzungen') + '</span>' : '<span class="meta">nichts zu ersetzen</span>') + '</td></tr>').join('');
  $('laden-text').textContent = 'Durchsuche Word-Dateien';
  zeige('ergebnis');
}

$('ordner-waehlen').addEventListener('click', ordnerWaehlen);
$('anderer-ordner').addEventListener('click', ordnerWaehlen);
$('knopf-ersetzen').addEventListener('click', () => {
  const s = statistik();
  $('dialog-text').textContent = plural(s.namen.length, 'Platzhalter', 'Platzhalter') + ' in ' + plural(s.dateien, 'Datei', 'Dateien') + ' ersetzen?';
  $('schleier').classList.add('aktiv');
  $('dialog-ok').focus();
});
$('dialog-abbrechen').addEventListener('click', () => $('schleier').classList.remove('aktiv'));
$('dialog-ok').addEventListener('click', ersetzen);
$('knopf-fertig').addEventListener('click', () => api().beende());
document.addEventListener('keydown', e => { if (e.key === 'Escape') $('schleier').classList.remove('aktiv'); });
window.addEventListener('pywebviewready', start);
</script>
</body></html>
```

- [ ] **Step 7: Manuell prüfen**

Testordner anlegen (z. B. im Scratchpad) mit zwei `.docx`, die `[ADRESSE]` und `[Ort]` enthalten, eine davon mit einem über Runs verteilten Platzhalter. Dann:

Run: `cd platzhalter && uv run python -m platzhalter <testordner>`
Expected: Fenster öffnet, Liste zeigt beide Platzhalter mit Zählern, Ersetzen mit einem leeren Feld ersetzt nur das ausgefüllte, Ergebnisansicht zeigt Anzahl je Datei, `.bak` liegt daneben. Start ohne Argument öffnet den Ordnerdialog; Abbrechen zeigt die Startansicht.

- [ ] **Step 8: Commit**

```bash
git add platzhalter/src/platzhalter/app.py platzhalter/src/platzhalter/__main__.py platzhalter/src/platzhalter/ui/index.html platzhalter/tests/test_app.py
git commit -m "Platzhalter-Tool: pywebview-Oberflaeche"
```

---

### Task 5: EXE mit PyInstaller und README des Tools

**Files:**
- Create: `platzhalter/platzhalter.spec`
- Create: `platzhalter/README.md`

**Interfaces:**
- Produces: `platzhalter/dist/platzhalter.exe` (onefile, ohne Konsole)

- [ ] **Step 1: platzhalter.spec schreiben**

```python
# -*- mode: python ; coding: utf-8 -*-
# Aufruf aus platzhalter/:  uv run pyinstaller platzhalter.spec --noconfirm
from PyInstaller.utils.hooks import collect_data_files

a = Analysis(
    ["src/platzhalter/__main__.py"],
    pathex=["src"],
    datas=[("src/platzhalter/ui/index.html", "platzhalter/ui")] + collect_data_files("webview"),
    hiddenimports=["webview.platforms.winforms", "webview.platforms.edgechromium", "clr_loader", "pythonnet"],
    excludes=["tkinter", "unittest", "pytest"],
    noarchive=False,
)
pyz = PYZ(a.pure)
exe = EXE(
    pyz, a.scripts, a.binaries, a.datas,
    name="platzhalter",
    console=False,
    upx=False,
    strip=False,
)
```

- [ ] **Step 2: Lokal bauen**

Run: `cd platzhalter && uv run pyinstaller platzhalter.spec --noconfirm`
Expected: `dist/platzhalter.exe` entsteht, keine Fehler in der Ausgabe. Falls `webview.platforms.edgechromium` nicht existiert (Modulname je Version prüfen mit `uv run python -c "import webview.platforms, pkgutil; print([m.name for m in pkgutil.iter_modules(webview.platforms.__path__)])"`), Eintrag in `hiddenimports` anpassen.

- [ ] **Step 3: EXE starten**

Run: `platzhalter\dist\platzhalter.exe <testordner>` (Testordner aus Task 4)
Expected: Fenster öffnet wie bei `python -m platzhalter`. Prüfen: Suche, Ersetzen, Ergebnis.

- [ ] **Step 4: README schreiben**

`platzhalter/README.md`:
```markdown
# Platzhalter einsetzen

Kleines Windows-Programm für den letzten Schritt des Ablaufs: Es durchsucht einen Ordner
(mit Unterordnern) nach Word-Dateien, zeigt alle Platzhalter in eckigen Klammern wie
`[ADRESSE]` oder `[IBAN]` an und setzt die von dir eingegebenen Werte in allen Dateien ein.

Download: https://stayingclean.github.io/ki-tasks/platzhalter.exe

## Benutzen

1. `platzhalter.exe` starten und den Ordner wählen, zum Beispiel `Papierkram/03_Entwuerfe`.
2. Für jeden Platzhalter den Wert eintragen. Was du leer lässt, bleibt stehen.
3. «Ersetzen» und bestätigen. Von jeder geänderten Datei liegt danach eine Sicherung
   `<name>.docx.bak` daneben. Die eingegebenen Werte werden nirgends gespeichert.

Beim ersten Start warnt Windows SmartScreen, weil die Datei nicht signiert ist:
«Weitere Informationen» und dann «Trotzdem ausführen». Word-Dateien, die gerade in Word
offen sind, können nicht geändert werden; sie erscheinen im Ergebnis mit Fehler.

Nicht unterstützt: Platzhalter in Kommentaren, Fussnoten oder über Absatzgrenzen hinweg.

## Entwickeln

Voraussetzung: [uv](https://docs.astral.sh/uv/). Alles in diesem Ordner ausführen.

```
uv sync                                   # Python 3.12 und Abhängigkeiten
uv run pytest                             # Tests
uv run python -m platzhalter <ordner>     # Programm starten
uv run pyinstaller platzhalter.spec       # dist/platzhalter.exe bauen
```

Aufbau: `dokument.py` (Absätze und Runs einer .docx), `suche.py` (Dateien finden, Platzhalter
zählen), `docx_ersetzen.py` (Ersetzen über Run-Grenzen, Sicherung, atomares Schreiben),
`app.py` und `ui/index.html` (Oberfläche mit pywebview). Die EXE wird vom GitHub-Actions-Workflow
des Repos gebaut und mit den Zips auf GitHub Pages veröffentlicht.
```

- [ ] **Step 5: Commit**

```bash
git add platzhalter/platzhalter.spec platzhalter/README.md
git commit -m "Platzhalter-Tool: PyInstaller-Spec und README"
```

---

### Task 6: Workflow und Repo-Doku

**Files:**
- Modify: `.github/workflows/pages.yml`
- Modify: `README.md` (Root)
- Modify: `CLAUDE.md`

- [ ] **Step 1: Workflow erweitern**

Neue Fassung von `.github/workflows/pages.yml` (Job `exe` neu, `build` wartet darauf und legt die EXE in `dist/`):

```yaml
name: Zips bauen und auf GitHub Pages veröffentlichen

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: pages
  cancel-in-progress: true

jobs:
  exe:
    runs-on: windows-latest
    defaults:
      run:
        working-directory: platzhalter
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v6
      - name: Abhängigkeiten
        run: uv sync --locked
      - name: Tests
        run: uv run pytest
      - name: EXE bauen
        run: uv run pyinstaller platzhalter.spec --noconfirm
      - uses: actions/upload-artifact@v4
        with:
          name: platzhalter-exe
          path: platzhalter/dist/platzhalter.exe
          if-no-files-found: error
  build:
    needs: exe
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - name: Zips bauen
        run: python build.py
      - uses: actions/download-artifact@v4
        with:
          name: platzhalter-exe
          path: dist
      - uses: actions/configure-pages@v5
      - uses: actions/upload-pages-artifact@v3
        with:
          path: ./dist
  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - id: deployment
        uses: actions/deploy-pages@v4
```

- [ ] **Step 2: Root-README ergänzen** (nach dem Abschnitt «Lokal bauen» einfügen)

```markdown
## Platzhalter-Tool

`platzhalter/` enthält ein kleines Windows-Programm für den letzten Schritt: Es sucht in einem
Ordner alle Word-Dateien nach `[Platzhalter]` ab und setzt die eingegebenen Werte ein.
Download: https://stayingclean.github.io/ki-tasks/platzhalter.exe. Eigenes uv-Projekt,
Details in `platzhalter/README.md`. Die EXE baut der Workflow auf einem Windows-Runner.
```

Dazu im Baum-Block der README nach der Zeile mit `build.py` ergänzen:
```
platzhalter/                  Windows-Programm: [Platzhalter] in Word-Dateien einsetzen (uv, EXE)
```

- [ ] **Step 3: CLAUDE.md ergänzen** (als weiteren Punkt in der Liste)

```markdown
- `platzhalter/` ist ein eigenes uv-Projekt (Windows-Tool, EXE per PyInstaller). Befehle dort
  mit `uv run …`; nach Änderungen `uv run pytest`. Es hat nichts mit `build.py` zu tun.
```

- [ ] **Step 4: build.py-Lauf prüfen**

Run: `python build.py`
Expected: unverändert «2 Aufgaben, Zips in …dist» (oder aktuelle Anzahl), keine Fehler.

- [ ] **Step 5: Commit**

```bash
git add .github/workflows/pages.yml README.md CLAUDE.md
git commit -m "Platzhalter-Tool: EXE im Pages-Workflow bauen, Doku"
```
