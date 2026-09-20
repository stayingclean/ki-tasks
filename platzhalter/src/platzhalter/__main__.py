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
