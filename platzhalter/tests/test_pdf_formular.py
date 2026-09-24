from pathlib import Path

import pytest
from pypdf import PdfReader

from formular import formular, ohne_formular
from platzhalter.pdf_formular import ersetze_in_pdf, oeffne, platzhalter_texte


def werte_im_pdf(pfad: Path) -> dict[str, str]:
    reader = PdfReader(str(pfad))
    if reader.is_encrypted:
        reader.decrypt("")
    return {k: f.get("/V") for k, f in reader.get_fields().items() if f.get("/FT") == "/Tx"}


def test_platzhalter_texte_liest_nur_textfelder(tmp_path):
    pfad = formular(tmp_path / "f.pdf", {"Name": "[VORNAME NAME]", "Ort": "Zürich"}, ankreuzfeld=True)
    assert sorted(platzhalter_texte(oeffne(pfad))) == ["Zürich", "[VORNAME NAME]"]


def test_oeffne_gibt_none_ohne_formularfelder(tmp_path):
    assert oeffne(ohne_formular(tmp_path / "inserat.pdf")) is None


def test_oeffne_gibt_none_bei_passwort(tmp_path):
    assert oeffne(formular(tmp_path / "f.pdf", {"A": "[AA]"}, passwort="geheim")) is None


def test_oeffne_liest_formular_mit_leerem_benutzerpasswort(tmp_path):
    # Amtliche Formulare sind oft gegen Bearbeiten geschützt, lassen sich aber ohne Passwort öffnen.
    pfad = formular(tmp_path / "f.pdf", {"A": "[AA]"}, passwort="")
    assert platzhalter_texte(oeffne(pfad)) == ["[AA]"]


def test_oeffne_wirft_bei_kaputter_datei(tmp_path):
    (tmp_path / "kaputt.pdf").write_bytes(b"kein pdf")
    with pytest.raises(Exception):
        oeffne(tmp_path / "kaputt.pdf")


def test_ersetze_in_pdf_setzt_werte_und_laesst_rest_stehen(tmp_path):
    pfad = formular(tmp_path / "f.pdf", {
        "Name": "[VORNAME NAME]",
        "Adresse": "[Strasse], [PLZ/Ort]",
        "Quelle": "Seite [1]",
        "Leer": "",
    })
    n = ersetze_in_pdf(pfad, {"VORNAME NAME": "Vreni Muster", "Strasse": "Weg 1", "PLZ/Ort": ""})
    assert n == 2
    assert werte_im_pdf(pfad) == {
        "Name": "Vreni Muster",
        "Adresse": "Weg 1, [PLZ/Ort]",
        "Quelle": "Seite [1]",
        "Leer": "",
    }
    assert (tmp_path / "f.pdf.bak").exists()
    assert werte_im_pdf(tmp_path / "f.pdf.bak")["Name"] == "[VORNAME NAME]"
    assert not (tmp_path / "f.pdf.tmp").exists()


def test_ersetze_in_pdf_trifft_verschachtelte_felder(tmp_path):
    pfad = formular(tmp_path / "f.pdf", {"person.name": "[Name]", "partner.name": "[Name Partner]"})
    assert ersetze_in_pdf(pfad, {"Name": "A", "Name Partner": "B"}) == 2
    assert werte_im_pdf(pfad) == {"person.name": "A", "partner.name": "B"}


def test_ersetze_in_pdf_ohne_treffer_laesst_datei_unberuehrt(tmp_path):
    pfad = formular(tmp_path / "f.pdf", {"A": "[AA]"})
    vorher = pfad.read_bytes()
    assert ersetze_in_pdf(pfad, {"BB": "x", "AA": ""}) == 0
    assert pfad.read_bytes() == vorher
    assert not (tmp_path / "f.pdf.bak").exists()


def test_ersetze_in_pdf_entfernt_xfa(tmp_path):
    # Bei Formularen mit XFA-Teil zeigt Acrobat sonst die alten XFA-Daten statt der Felder.
    pfad = formular(tmp_path / "f.pdf", {"A": "[AA]"}, xfa=True)
    ersetze_in_pdf(pfad, {"AA": "x"})
    assert "/XFA" not in PdfReader(str(pfad)).trailer["/Root"]["/AcroForm"]


def test_ersetze_in_pdf_verlangt_neuaufbau_der_anzeige(tmp_path):
    pfad = formular(tmp_path / "f.pdf", {"A": "[AA]"})
    ersetze_in_pdf(pfad, {"AA": "x"})
    assert PdfReader(str(pfad)).trailer["/Root"]["/AcroForm"]["/NeedAppearances"] == True  # noqa: E712 (BooleanObject)


def test_ersetze_in_pdf_mit_leerem_benutzerpasswort(tmp_path):
    pfad = formular(tmp_path / "f.pdf", {"A": "[AA]"}, passwort="")
    assert ersetze_in_pdf(pfad, {"AA": "x"}) == 1
    assert werte_im_pdf(pfad) == {"A": "x"}
