"""Zugriff auf Absätze und Runs einer .docx, unabhängig von Suche und Ersetzung."""
from __future__ import annotations

import re
from collections.abc import Iterator

from docx.document import Document as DocumentTyp
from docx.opc.constants import RELATIONSHIP_TYPE as RT
from docx.oxml.ns import qn
from docx.text.run import Run

# [Name] mit 1 bis 80 Zeichen, ohne Klammern, Zeilenumbruch oder Tab. Gruppe 1 = Name.
# Darin muss mindestens ein Wort stehen, also zwei Buchstaben am Stück; das hält
# Quellenverweise wie [1], [1, 2] oder [S. 12] heraus, lässt aber [AHV-Nummer],
# [PLZ/Ort] und [Betrag 2026] durch.
_INHALT = r"[^\[\]\r\n\t]"
_WORT = r"[A-Za-zÄÖÜäöüß]{2}"
MUSTER = re.compile(rf"\[(?={_INHALT}*{_WORT})({_INHALT}{{1,80}})\]")


def alle_absaetze(doc: DocumentTyp) -> Iterator:
    """Alle w:p im Textkörper (auch Tabellen, Textfelder) und in Kopf- und Fusszeilen."""
    yield from doc.element.body.iter(qn("w:p"))
    for rel in doc.part.rels.values():
        if rel.reltype in (RT.HEADER, RT.FOOTER):
            yield from rel.target_part.element.iter(qn("w:p"))


def runs(p) -> list[Run]:
    """Direkte Runs des Absatzes und Runs in Hyperlinks, in Dokumentreihenfolge.

    Bewusst nicht p.iter(): Textfelder liegen als eigene Absätze in einem Run und
    würden sonst doppelt erfasst.
    """
    return [Run(r, None) for r in p.xpath("./w:r | ./w:hyperlink/w:r")]


def absatz_text(p) -> str:
    return "".join(r.text for r in runs(p))
