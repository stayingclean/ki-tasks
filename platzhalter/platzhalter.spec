# -*- mode: python ; coding: utf-8 -*-
# Aufruf aus platzhalter/:  uv run pyinstaller platzhalter.spec --noconfirm
# Windows: dist/platzhalter.exe, eine einzelne Datei.
# macOS:   dist/Platzhalter.app; ein .app ist ohnehin ein Ordner, darum onedir.
import sys

from PyInstaller.utils.hooks import collect_data_files

MAC = sys.platform == "darwin"

a = Analysis(
    ["src/platzhalter/__main__.py"],
    pathex=["src"],
    datas=[
        ("src/platzhalter/ui/index.html", "platzhalter/ui"),
        ("src/platzhalter/ui/logo.txt", "platzhalter/ui"),
    ] + collect_data_files("webview"),
    hiddenimports=(
        ["webview.platforms.cocoa"]
        if MAC
        else ["webview.platforms.winforms", "webview.platforms.edgechromium", "clr_loader"]
    ),
    excludes=["tkinter", "unittest", "pytest"],
    noarchive=False,
)
pyz = PYZ(a.pure)

if MAC:
    exe = EXE(
        pyz, a.scripts, [],
        exclude_binaries=True,
        name="platzhalter",
        console=False,
        upx=False,
        strip=False,
    )
    coll = COLLECT(exe, a.binaries, a.datas, name="platzhalter", upx=False, strip=False)
    app = BUNDLE(
        coll,
        name="Platzhalter.app",
        bundle_identifier="ch.stayingclean.platzhalter",
        info_plist={"NSHighResolutionCapable": True},
    )
else:
    exe = EXE(
        pyz, a.scripts, a.binaries, a.datas,
        name="platzhalter",
        icon="logo.ico",
        console=False,
        upx=False,
        strip=False,
    )
