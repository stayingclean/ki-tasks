# -*- mode: python ; coding: utf-8 -*-
# Aufruf aus platzhalter/:  uv run pyinstaller platzhalter.spec --noconfirm
from PyInstaller.utils.hooks import collect_data_files

a = Analysis(
    ["src/platzhalter/__main__.py"],
    pathex=["src"],
    datas=[
        ("src/platzhalter/ui/index.html", "platzhalter/ui"),
        ("src/platzhalter/ui/logo.txt", "platzhalter/ui"),
    ] + collect_data_files("webview"),
    hiddenimports=[
        "webview.platforms.winforms",
        "webview.platforms.edgechromium",
        "clr_loader",
    ],
    excludes=["tkinter", "unittest", "pytest"],
    noarchive=False,
)
pyz = PYZ(a.pure)
exe = EXE(
    pyz, a.scripts, a.binaries, a.datas,
    name="platzhalter",
    icon="logo.ico",
    console=False,
    upx=False,
    strip=False,
)
