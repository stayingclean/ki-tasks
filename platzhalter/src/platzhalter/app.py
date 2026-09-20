"""pywebview-Fenster und die Python-Seite der Oberfläche."""
from __future__ import annotations

from dataclasses import asdict
from importlib.resources import files
from pathlib import Path

from platzhalter.docx_ersetzen import ersetze_in_datei
from platzhalter.suche import durchsuche

TITEL = "Platzhalter einsetzen"


class Api:
    """Wird von JavaScript über window.pywebview.api aufgerufen.

    Die eingegebenen Werte werden nur für den Lauf gehalten und nirgends gespeichert.
    """

    def __init__(self, ordner: Path | None) -> None:
        self._ordner = ordner
        self._dateien: list[str] = []
        # Unterstrich ist Absicht: pywebview liest die öffentlichen Attribute der Api-Klasse
        # aus, um sie JavaScript anzubieten. Das Fenster-Objekt darf dabei nicht dabei sein.
        self._fenster = None  # wird von starte() gesetzt

    def hole_ordner(self) -> str | None:
        return str(self._ordner) if self._ordner else None

    def waehle_ordner(self) -> str | None:
        import webview

        auswahl = self._fenster.create_file_dialog(webview.FOLDER_DIALOG)
        if not auswahl:
            return None
        self._ordner = Path(auswahl[0])
        return str(self._ordner)

    def suche(self) -> dict:
        ergebnis = durchsuche(self._ordner)
        self._dateien = ergebnis.dateien
        return asdict(ergebnis)

    def ersetze(self, werte: dict[str, str]) -> list[dict]:
        resultate = []
        for rel in self._dateien:
            try:
                n = ersetze_in_datei(self._ordner / rel, werte)
                resultate.append({"datei": rel, "ersetzt": n, "fehler": None})
            except Exception as e:  # gesperrt, beschädigt, kein Schreibrecht
                resultate.append({"datei": rel, "ersetzt": 0, "fehler": str(e)})
        return resultate

    def beende(self) -> None:
        if self._fenster:
            self._fenster.destroy()


def lade_html() -> str:
    """Oberfläche mit eingebettetem Logo.

    Die Seite wird als Zeichenkette an pywebview übergeben, darum lösen relative
    Bildpfade nicht auf. Das Logo steckt als Base64 in ui/logo.txt und ersetzt
    die Marke {{LOGO}} in der Seite. Erzeugt von werkzeuge/logo_aufbereiten.py.
    """
    ui = files("platzhalter") / "ui"
    html = (ui / "index.html").read_text(encoding="utf-8")
    logo = (ui / "logo.txt").read_text(encoding="ascii").strip()
    return html.replace("{{LOGO}}", logo)


def starte(ordner: Path | None) -> None:
    import webview

    api = Api(ordner)
    api._fenster = webview.create_window(
        TITEL, html=lade_html(), js_api=api, width=900, height=700, min_size=(640, 480)
    )
    webview.start()
