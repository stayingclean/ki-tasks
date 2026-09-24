"""Platzhalter in einer .docx ersetzen, auch wenn Word sie auf mehrere Runs verteilt hat."""
from __future__ import annotations

from pathlib import Path

from docx import Document

from platzhalter.datei import schreibe_mit_sicherung
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
        # ende=False: Run, der das Zeichen an pos enthält.
        # ende=True: Run, der das Zeichen vor pos enthält.
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
            neu[i] = neu[i][: start - offsets[i]] + wert + neu[i][ende - offsets[i]:]
        else:
            neu[i] = neu[i][: start - offsets[i]] + wert
            for k in range(i + 1, j):
                neu[k] = ""
            neu[j] = neu[j][ende - offsets[j]:]

    for r, alt, frisch in zip(alle, texte, neu):
        if alt != frisch:
            r.text = frisch
    return len(funde)


def ersetze_in_datei(pfad: Path, werte: dict[str, str]) -> int:
    """Ersetzt in einer Datei und gibt die Anzahl Ersetzungen zurück.

    Ohne Treffer bleibt die Datei unangetastet, sonst siehe schreibe_mit_sicherung().
    """
    werte = {k: v for k, v in werte.items() if v}
    if not werte:
        return 0
    doc = Document(str(pfad))
    anzahl = sum(ersetze_im_absatz(p, werte) for p in alle_absaetze(doc))
    if anzahl == 0:
        return 0
    schreibe_mit_sicherung(pfad, lambda tmp: doc.save(str(tmp)))
    return anzahl
