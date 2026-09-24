"""Platzhalter in den Textfeldern eines PDF-Formulars (AcroForm) finden und ersetzen.

Nur die ausfüllbaren Felder, nie der gedruckte Text der Seite: Ein Feld hat seine
eigene Schrift und Grösse, der eingesetzte Wert passt sich an. Im Seitentext stehen
die Zeichen an festen Stellen, und ein längerer Wert würde überlaufen.
"""
from __future__ import annotations

import re
from pathlib import Path

from pypdf import PasswordType, PdfReader, PdfWriter
from pypdf.generic import NameObject

from platzhalter.datei import schreibe_mit_sicherung
from platzhalter.dokument import MUSTER


def oeffne(pfad: Path) -> PdfReader | None:
    """Das Formular zum Lesen, oder None, wenn es keins ist.

    None heisst: keine Formularfelder, oder ein Passwort zum Öffnen. Beides kann Claude
    nicht mit Platzhaltern gefüllt haben. Formulare, die nur gegen Bearbeiten geschützt
    sind, öffnen sich mit leerem Passwort. Eine kaputte Datei wirft.
    """
    reader = PdfReader(str(pfad))
    if reader.is_encrypted and reader.decrypt("") == PasswordType.NOT_DECRYPTED:
        return None
    if not reader.get_fields():
        return None
    return reader


def _textfelder(reader: PdfReader) -> dict[str, str]:
    """Voller Feldname → Wert, nur Textfelder mit Text."""
    return {
        name: str(feld["/V"])
        for name, feld in reader.get_fields().items()
        if feld.get("/FT") == "/Tx" and isinstance(feld.get("/V"), str)
    }


def platzhalter_texte(reader: PdfReader) -> list[str]:
    return list(_textfelder(reader).values())


def ersetze_in_pdf(pfad: Path, werte: dict[str, str]) -> int:
    """Ersetzt in den Textfeldern und gibt die Anzahl Ersetzungen zurück.

    Ohne Treffer bleibt die Datei unangetastet, sonst wie bei Word mit .bak daneben.
    """
    werte = {k: v for k, v in werte.items() if v}
    if not werte:
        return 0
    reader = oeffne(pfad)
    if reader is None:
        return 0

    anzahl = 0

    def einsetzen(m: re.Match) -> str:
        nonlocal anzahl
        if m.group(1) not in werte:
            return m.group(0)
        anzahl += 1
        return werte[m.group(1)]

    neu = {}
    for name, wert in _textfelder(reader).items():
        frisch = MUSTER.sub(einsetzen, wert)
        if frisch != wert:
            neu[name] = frisch
    if anzahl == 0:
        return 0

    writer = PdfWriter(clone_from=reader)
    # Ein Formular mit XFA-Teil zeigt in Acrobat die XFA-Daten und nicht die Felder,
    # der eingesetzte Wert bliebe dort unsichtbar. Ohne XFA gelten die Felder.
    writer._root_object["/AcroForm"].pop(NameObject("/XFA"), None)
    # auto_regenerate setzt NeedAppearances: Der Viewer zeichnet die Felder mit ihrer
    # eigenen Schrift neu, statt der einfachen Darstellung von pypdf zu vertrauen.
    writer.update_page_form_field_values(None, neu, auto_regenerate=True)
    schreibe_mit_sicherung(pfad, lambda tmp: writer.write(str(tmp)))
    return anzahl
