"""Eine geänderte Datei sicher zurückschreiben, gleich für Word und PDF."""
from __future__ import annotations

import os
import shutil
from collections.abc import Callable
from pathlib import Path


def schreibe_mit_sicherung(pfad: Path, schreibe: Callable[[Path], None]) -> None:
    """.bak anlegen, über schreibe() in .tmp schreiben, dann das Original ersetzen.

    Ein Fehler beim Schreiben lässt das Original unverändert.
    """
    shutil.copy2(pfad, pfad.with_name(pfad.name + ".bak"))
    tmp = pfad.with_name(pfad.name + ".tmp")
    try:
        schreibe(tmp)
        os.replace(tmp, pfad)
    finally:
        if tmp.exists():
            tmp.unlink()
