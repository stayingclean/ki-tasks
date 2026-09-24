"""Kleine PDF-Formulare für die Tests, ohne weitere Abhängigkeit gebaut."""
from __future__ import annotations

from pathlib import Path

from pypdf import PdfWriter
from pypdf.generic import (
    ArrayObject,
    DictionaryObject,
    NameObject,
    RectangleObject,
    TextStringObject,
)


def formular(
    pfad: Path,
    felder: dict[str, str],
    *,
    ankreuzfeld: bool = False,
    xfa: bool = False,
    passwort: str | None = None,
) -> Path:
    """Eine Seite mit je einem Textfeld pro Eintrag. «person.name» wird zum Feld «name»
    unter dem Elternfeld «person», so wie Formulare ihre Felder oft gruppieren."""
    w = PdfWriter()
    seite = w.add_blank_page(595, 842)
    schrift = w._add_object(DictionaryObject({
        NameObject("/Type"): NameObject("/Font"),
        NameObject("/Subtype"): NameObject("/Type1"),
        NameObject("/BaseFont"): NameObject("/Helvetica"),
    }))
    widgets, oben, eltern = ArrayObject(), ArrayObject(), {}

    for i, (name, wert) in enumerate(felder.items()):
        *pfadteile, kurz = name.split(".")
        feld = DictionaryObject({
            NameObject("/Type"): NameObject("/Annot"),
            NameObject("/Subtype"): NameObject("/Widget"),
            NameObject("/FT"): NameObject("/Tx"),
            NameObject("/T"): TextStringObject(kurz),
            NameObject("/V"): TextStringObject(wert),
            NameObject("/DA"): TextStringObject("/Helv 10 Tf 0 g"),
            NameObject("/Rect"): RectangleObject([50, 780 - 30 * i, 400, 800 - 30 * i]),
        })
        ref = w._add_object(feld)
        widgets.append(ref)
        if pfadteile:
            gruppe = ".".join(pfadteile)
            if gruppe not in eltern:
                eltern[gruppe] = w._add_object(DictionaryObject({
                    NameObject("/T"): TextStringObject(gruppe),
                    NameObject("/Kids"): ArrayObject(),
                }))
                oben.append(eltern[gruppe])
            eltern[gruppe].get_object()["/Kids"].append(ref)
            feld[NameObject("/Parent")] = eltern[gruppe]
        else:
            oben.append(ref)

    if ankreuzfeld:
        ref = w._add_object(DictionaryObject({
            NameObject("/Type"): NameObject("/Annot"),
            NameObject("/Subtype"): NameObject("/Widget"),
            NameObject("/FT"): NameObject("/Btn"),
            NameObject("/T"): TextStringObject("Ja"),
            NameObject("/V"): NameObject("/Off"),
            NameObject("/Rect"): RectangleObject([50, 50, 60, 60]),
        }))
        widgets.append(ref)
        oben.append(ref)

    seite[NameObject("/Annots")] = widgets
    acro = DictionaryObject({
        NameObject("/Fields"): oben,
        NameObject("/DA"): TextStringObject("/Helv 10 Tf 0 g"),
        NameObject("/DR"): DictionaryObject({
            NameObject("/Font"): DictionaryObject({NameObject("/Helv"): schrift}),
        }),
    })
    if xfa:
        acro[NameObject("/XFA")] = ArrayObject()
    w._root_object[NameObject("/AcroForm")] = acro
    if passwort is not None:
        w.encrypt(user_password=passwort, owner_password="besitzer", algorithm="AES-256")
    pfad.parent.mkdir(parents=True, exist_ok=True)
    with open(pfad, "wb") as f:
        w.write(f)
    return pfad


def ohne_formular(pfad: Path) -> Path:
    w = PdfWriter()
    w.add_blank_page(595, 842)
    pfad.parent.mkdir(parents=True, exist_ok=True)
    with open(pfad, "wb") as f:
        w.write(f)
    return pfad
