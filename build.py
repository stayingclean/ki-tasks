"""Baut aus grundgeruest/ und aufgaben/<name>/ fertige Zips nach dist/.

Aufruf:  python build.py   → dist/grundgeruest.zip, dist/<aufgabe>.zip je Aufgabe,
                             dist/index.html, dist/aufgaben.json

Zusammensetzen: Das Grundgerüst wird kopiert, dann die Aufgaben-Schicht darüber.
Eine Aufgabe besteht aus INFO.md (Titel, Gruppe, Kurzbeschrieb für die
Download-Seite) und 9_Claude/wissen.md (Fachwissen für Claude). INFO.md bleibt
im Repo, wissen.md überschreibt die Fassung aus dem Grundgerüst.

START-HIER.txt bekommt den Titel der Aufgabe eingesetzt und wird mit UTF-8-BOM
und CRLF geschrieben: Der Build läuft auf Linux, die Datei landet auf Windows
in Notepad. Keine Bibliotheken nötig.
"""
from __future__ import annotations

import json
import shutil
import sys
import zipfile
from pathlib import Path

HERE = Path(__file__).parent
BASE = HERE / "grundgeruest"
TASKS = HERE / "aufgaben"
ANLEITUNG = HERE / "anleitung"
DIST = HERE / "dist"

START = "START-HIER.txt"
TITEL_OHNE_AUFGABE = "Papierkram"

# Die Seiten aus anleitung/ veröffentlicht der Toolbox-Deploy, nicht dieses Repo.
# Darum verlinkt die Download-Seite absolut dorthin.
ANLEITUNG_URL = "https://stayingclean.github.io/toolbox/claude-anleitung/"


def lese_info(task: Path) -> dict[str, str]:
    info: dict[str, str] = {"name": task.name}
    for zeile in (task / "INFO.md").read_text(encoding="utf-8").splitlines():
        if ":" in zeile:
            k, v = zeile.split(":", 1)
            info[k.strip()] = v.strip()
    # Die Beschreibung heisst wie die Aufgabe: aufgaben/<name>/ ↔ anleitung/<name>.html
    if (ANLEITUNG / f"{task.name}.html").exists():
        info["seite"] = f"{ANLEITUNG_URL}{task.name}.html"
    return info


def alle_aufgaben() -> list[Path]:
    return sorted(p for p in TASKS.iterdir() if p.is_dir() and (p / "INFO.md").exists())


def kopiere_baum(quelle: Path, ziel: Path) -> None:
    for datei in quelle.rglob("*"):
        if datei.is_dir():
            continue
        rel = datei.relative_to(quelle)
        if rel.name == "INFO.md":
            continue
        z = ziel / rel
        z.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(datei, z)


def schreibe_start(ziel: Path, titel: str) -> None:
    """Titel einsetzen, dann mit BOM und CRLF schreiben (Notepad unter Windows)."""
    pfad = ziel / START
    text = pfad.read_text(encoding="utf-8").replace("{{TITEL}}", titel)
    pfad.write_text(text, encoding="utf-8-sig", newline="\r\n")


def baue_ordner(task: Path | None, ziel: Path) -> None:
    if ziel.exists():
        shutil.rmtree(ziel)
    kopiere_baum(BASE, ziel)
    if task is not None:
        kopiere_baum(task, ziel)
    schreibe_start(ziel, lese_info(task)["titel"] if task else TITEL_OHNE_AUFGABE)
    # .gitkeep sind nur für Git; im Zip sollen die Ordner trotzdem existieren
    for keep in ziel.rglob(".gitkeep"):
        keep.unlink()


def zippe(ordner: Path, zipdatei: Path) -> None:
    with zipfile.ZipFile(zipdatei, "w", zipfile.ZIP_DEFLATED) as zf:
        for pfad in sorted(ordner.rglob("*")):
            arc = pfad.relative_to(ordner)
            if pfad.is_dir():
                zf.writestr(str(arc) + "/", "")
            else:
                zf.write(pfad, arc)


def baue_zip(task: Path | None, name: str) -> Path:
    tmp = DIST / "_tmp" / name
    baue_ordner(task, tmp)
    ziel = DIST / f"{name}.zip"
    zippe(tmp, ziel)
    shutil.rmtree(tmp)
    return ziel


def schreibe_index(infos: list[dict[str, str]]) -> None:
    gruppen: dict[str, list[dict[str, str]]] = {}
    for i in infos:
        gruppen.setdefault(i["gruppe"], []).append(i)
    karten = []
    for g, items in gruppen.items():
        karten.append(f"<h2>{g}</h2><div class='grid'>")
        for i in items:
            # Die Karte führt zur Beschreibung, dort steht der Download ebenfalls.
            # Fehlt die Seite noch, bleibt es beim Zip.
            ziel = i.get("seite", f"{i['name']}.zip")
            mehr = "<span class='mehr'>Ablauf und Beschreibung →</span>" if "seite" in i else ""
            karten.append(
                f"<div class='card'><a class='haupt' href='{ziel}'><span class='name'>{i['titel']}</span>"
                f"<span class='meta'>{i['kurz']}</span>{mehr}</a>"
                f"<a class='dl' href='{i['name']}.zip'>↓ {i['name']}.zip</a></div>"
            )
        karten.append("</div>")
    html = INDEX_HTML.replace("{{KARTEN}}", "\n".join(karten))
    (DIST / "index.html").write_text(html, encoding="utf-8")
    (DIST / "aufgaben.json").write_text(json.dumps(infos, ensure_ascii=False, indent=2), encoding="utf-8")


INDEX_HTML = """<!DOCTYPE html>
<html lang="de"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ki-tasks – Aufgaben-Ordner zum Herunterladen</title>
<style>
:root{--bg:#FAF8F5;--card:#fff;--border:#E8E4DF;--text:#1C1C1C;--muted:#7A7268;--accent:#008080;--accent-dark:#006666;--tint:#E6F2F2}
*{box-sizing:border-box}body{margin:0;font-family:Inter,-apple-system,"Segoe UI",Roboto,sans-serif;background:var(--bg);color:var(--text);line-height:1.5}
.wrap{max-width:820px;margin:0 auto;padding:44px 20px 64px}h1{font-family:Georgia,serif;color:var(--accent-dark);font-size:2rem;margin:0 0 8px}
.sub{color:var(--muted);margin:0 0 24px}h2{font-size:.8rem;text-transform:uppercase;letter-spacing:.08em;color:var(--muted);margin:28px 0 10px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:14px}
.card{display:flex;flex-direction:column;gap:6px;padding:16px 18px;background:var(--card);border:1px solid var(--border);border-radius:14px;transition:transform .15s,border-color .15s}
.card:hover{border-color:var(--accent);transform:translateY(-2px)}.haupt{display:flex;flex-direction:column;gap:4px;text-decoration:none;color:var(--text);flex:1}
.name{font-weight:600;color:var(--accent-dark)}.meta{color:var(--muted);font-size:.88rem}.mehr{font-size:.85rem;font-weight:600;color:var(--accent);margin-top:4px}.dl{font-size:.8rem;color:var(--muted);text-decoration:none}.dl:hover{color:var(--accent)}
.box{background:var(--tint);border-left:4px solid var(--accent);padding:12px 16px;border-radius:0 12px 12px 0;margin:0 0 18px}
a.big{display:block;padding:18px 20px;background:var(--accent);color:#fff;border-radius:14px;text-decoration:none;font-weight:600;margin:0 0 10px}
code{background:var(--card);border:1px solid var(--border);padding:1px 6px;border-radius:6px;font-size:.88em}
footer{margin-top:44px;padding-top:18px;border-top:1px solid var(--border);color:var(--muted);font-size:.82rem}
.footer-links{display:flex;flex-wrap:wrap;align-items:center;gap:8px 14px;margin-top:12px}.footer-credit,.footer-coffee{display:inline-flex;align-items:center;gap:8px;color:var(--muted);text-decoration:none}
.footer-credit:hover,.footer-coffee:hover{color:var(--accent)}.footer-avatar{width:28px;height:28px;border-radius:50%;border:1px solid var(--border)}
</style></head><body><div class="wrap">
<h1>Aufgaben-Ordner zum Herunterladen</h1>
<p class="sub">Fertige Startordner für Papierkram mit KI-Unterstützung. Entpacken, in Claude Cowork verbinden, «Was steht an?» schreiben.
Wie es weitergeht, steht in der <a href="https://stayingclean.github.io/toolbox/claude-anleitung/">Anleitung «Mit Claude arbeiten»</a>.</p>
<div class="box">Zip in einen neuen Ordner entpacken (Windows: Rechtsklick → «Alle extrahieren»). Darin liegt <code>START-HIER.txt</code> — mehr musst du nicht lesen.
Claude stellt die Fragen und legt die Dateien selber an; du legst nur deine Unterlagen in <code>1_Meine-Unterlagen</code>.
Zwei Aufgaben: zwei Zips herunterladen, in zwei Ordner entpacken.</div>
{{KARTEN}}
<a class="big" href="grundgeruest.zip" style="background:var(--card);color:var(--accent-dark);border:1px solid var(--border);margin-top:22px">↓ Leerer Ordner für eine eigene Aufgabe (grundgeruest.zip)</a>
<a class="big" href="platzhalter.exe" style="background:var(--card);color:var(--accent-dark);border:1px solid var(--border)">↓ platzhalter.exe — Adresse, Telefon und IBAN am Schluss einsetzen</a>
<footer>
<div>Quelle und Mitarbeit: <a href="https://github.com/stayingclean/ki-tasks">github.com/stayingclean/ki-tasks</a> · Teil der <a href="https://stayingclean.github.io/toolbox/">Toolbox</a></div>
<div class="footer-links"><a class="footer-credit" href="https://github.com/stayingclean" target="_blank" rel="noopener"><img class="footer-avatar" src="https://github.com/stayingclean.png?size=80" alt="stayingclean" loading="lazy" width="28" height="28"><span>Erstellt von stayingclean</span></a>
<span aria-hidden="true">·</span><a class="footer-coffee" href="https://buymeacoffee.com/stayingclean" target="_blank" rel="noopener"><span aria-hidden="true">☕</span><span>Kaffee spendieren</span></a></div>
</footer></div></body></html>
"""


def main() -> None:
    DIST.mkdir(exist_ok=True)
    for alt in DIST.glob("*.zip"):
        alt.unlink()
    tasks = alle_aufgaben()
    baue_zip(None, "grundgeruest")
    for t in tasks:
        baue_zip(t, t.name)
    schreibe_index([lese_info(t) for t in tasks])
    print(f"{len(tasks)} Aufgaben, Zips in {DIST}")


if __name__ == "__main__":
    sys.exit(main())
