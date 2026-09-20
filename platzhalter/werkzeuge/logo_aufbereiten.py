"""Erzeugt aus logo.png die beiden Fassungen, die das Programm braucht.

Einmalig auszuführen, wenn sich logo.png ändert:

    uv run --with pillow python werkzeuge/logo_aufbereiten.py

Ergebnis (beide werden eingecheckt, damit der Build ohne Pillow auskommt):
- logo.ico                      Symbol der EXE, Grössen 16 bis 256
- src/platzhalter/ui/logo.txt   96 Pixel als Base64, von index.html eingebettet
"""
from __future__ import annotations

import base64
import io
from pathlib import Path

from PIL import Image

HIER = Path(__file__).parent.parent
QUELLE = HIER / "logo.png"
ICO = HIER / "logo.ico"
BASE64 = HIER / "src" / "platzhalter" / "ui" / "logo.txt"

GROESSEN = [16, 24, 32, 48, 64, 128, 256]
KOPFHOEHE = 96  # dargestellt wird das Logo mit 40 Pixeln, doppelt für scharfe Bildschirme


def main() -> None:
    bild = Image.open(QUELLE).convert("RGBA")
    bild.save(ICO, format="ICO", sizes=[(g, g) for g in GROESSEN])

    klein = bild.resize((KOPFHOEHE, KOPFHOEHE), Image.LANCZOS)
    puffer = io.BytesIO()
    klein.save(puffer, format="PNG", optimize=True)
    BASE64.write_text(base64.b64encode(puffer.getvalue()).decode("ascii"), encoding="ascii")

    print(f"{ICO.name}: {ICO.stat().st_size // 1024} KB")
    print(f"{BASE64.name}: {BASE64.stat().st_size // 1024} KB Base64")


if __name__ == "__main__":
    main()
