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
    warnung: str | None = None


VERLAUF = "verlauf"

VERLAUF_GEWAEHLT = (
    "Dieser Ordner ist ein Verlauf. Frühere Fassungen sollen bleiben, "
    "was du damals verschickt hast. Wähle den Ordner darüber."
)


def ist_verlauf(ordner: Path) -> bool:
    """Liegt der gewählte Ordner selbst in einem «verlauf», auf beliebiger Ebene?"""
    return any(teil.lower() == VERLAUF for teil in ordner.resolve().parts)


def finde_docx(ordner: Path) -> list[Path]:
    """Rekursiv alle .docx, ohne Word-Sperrdateien (~$…).

    Sicherungen (.docx.bak) fallen weg, weil die Endung nicht passt.

    Ordner namens «verlauf» bleiben aussen vor, auf jeder Ebene. Dort liegen
    frühere Fassungen, und die sollen bleiben, was damals verschickt wurde.
    """
    return sorted(
        p for p in ordner.rglob("*.docx")
        if p.is_file()
        and not p.name.startswith("~$")
        and not any(teil.lower() == VERLAUF for teil in p.relative_to(ordner).parts[:-1])
    )


def durchsuche(ordner: Path) -> Suchergebnis:
    ergebnis = Suchergebnis(ordner=str(ordner))
    if ist_verlauf(ordner):
        ergebnis.warnung = VERLAUF_GEWAEHLT
        return ergebnis
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
