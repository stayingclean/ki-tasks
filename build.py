"""Baut aus grundgeruest/ und aufgaben/<name>/ fertige Zips nach dist/.

Aufruf:  python build.py   → dist/grundgeruest.zip, dist/<aufgabe>.zip je Aufgabe,
                             dist/index.html, dist/aufgaben.json

Zusammensetzen: Das Grundgerüst wird kopiert, dann die Aufgaben-Schicht darüber.
Eine Aufgabe besteht aus INFO.md (Titel, Gruppe, Kurzbeschrieb für die
Download-Seite) und 9_Claude/wissen.md (Fachwissen für Claude). INFO.md bleibt
im Repo, wissen.md überschreibt die Fassung aus dem Grundgerüst.

Was gerade fällig ist, zeigt die Download-Seite in einer rechten Spalte: eine
Aufgabe mit `faellig: MM-TT bis MM-TT` in INFO.md während dieses Fensters, dazu
die Kantonsfristen aus fristen/<aufgabe>.json. Entschieden wird im Browser nach
dem heutigen Datum, nicht beim Build — die Seite wird nur bei einem Push neu
gebaut. Ist nichts fällig, bleibt die Spalte weg.

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
FRISTEN = HERE / "fristen"
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
    """Nach `reihenfolge:` aus INFO.md, dann nach Name. Dieselbe Folge gilt in der
    Navigation der Anleitung; der Toolbox-Deploy liest das Feld ebenfalls."""
    tasks = [p for p in TASKS.iterdir() if p.is_dir() and (p / "INFO.md").exists()]
    return sorted(tasks, key=lambda p: (int(lese_info(p).get("reihenfolge", 1000)), p.name))


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


def lese_fristen() -> dict[str, dict]:
    """fristen/<aufgabe>.json → {aufgabe: daten}. Landet als JSON in der Seite."""
    if not FRISTEN.exists():
        return {}
    return {f.stem: json.loads(f.read_text(encoding="utf-8")) for f in sorted(FRISTEN.glob("*.json"))}


def schreibe_faellig(infos: list[dict[str, str]]) -> None:
    """faellig.json (Daten) und faellig.js (Daten + Darstellung) nach dist/.

    faellig.js ist die einzige Stelle, die rechnet, was fällig ist. Die
    Download-Seite bindet es ein; in der Anleitung lädt es anleitung.js auf
    jeder Seite (gleiche Origin stayingclean.github.io).
    """
    daten = {
        "aufgaben": [
            {k: i[k] for k in ("name", "titel", "navtitel", "faellig", "faellig-text", "seite") if k in i}
            for i in infos
        ],
        "fristen": lese_fristen(),
    }
    roh = json.dumps(daten, ensure_ascii=False)
    (DIST / "faellig.json").write_text(roh, encoding="utf-8")
    (DIST / "faellig.js").write_text(FAELLIG_JS.replace("{{DATEN}}", roh), encoding="utf-8")


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
                f"<div class='card' data-aufgabe='{i['name']}'><a class='haupt' href='{ziel}'><span class='name'>{i['titel']}</span>"
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
:root{--bg:#FAF8F5;--card:#fff;--border:#E8E4DF;--text:#1C1C1C;--muted:#7A7268;--accent:#008080;--accent-dark:#006666;--tint:#E6F2F2;--warn:#B45309;--warn-border:#F2D3B0;--warn-tint:#FDF1E3}
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
.wrap.mit-spalte{max-width:1180px;display:grid;grid-template-columns:minmax(0,1fr) 300px;gap:36px;align-items:start}
.spalte{position:sticky;top:24px;margin-top:8px;padding:16px 18px;background:var(--card);border:1px solid var(--warn-border);border-top:4px solid var(--warn);border-radius:14px}
.spalte h2{margin:0 0 4px;color:var(--warn)}.spalte h3{font-size:.95rem;margin:16px 0 4px}.spalte h3 a{color:var(--accent-dark);text-decoration:none}.spalte h3 a:hover{text-decoration:underline}
.spalte p{margin:0 0 6px;font-size:.88rem}.spalte ul{list-style:none;margin:6px 0;padding:0;font-size:.86rem}.spalte li{display:flex;justify-content:space-between;gap:8px;padding:4px 0;border-top:1px solid var(--border)}
.spalte li a{color:var(--text);text-decoration:none}.spalte li a:hover{color:var(--accent)}.rest{color:var(--muted);white-space:nowrap}.knapp{color:var(--warn);font-weight:600}
.spalte .klein{color:var(--muted);font-size:.78rem;margin-top:8px}
.badge{align-self:flex-start;font-size:.72rem;font-weight:600;text-transform:uppercase;letter-spacing:.05em;color:var(--warn);background:var(--warn-tint);border-radius:999px;padding:2px 9px}
.card.ist-faellig{border-color:var(--warn-border);box-shadow:inset 0 3px 0 var(--warn)}
@media (max-width:900px){.wrap.mit-spalte{display:flex;flex-direction:column;gap:0}.spalte{order:-1;position:static;margin:0 0 24px}}
</style></head><body><div class="wrap"><div class="inhalt">
<h1>Aufgaben-Ordner zum Herunterladen</h1>
<p class="sub">Fertige Startordner für Papierkram mit KI-Unterstützung. Entpacken, in Claude Cowork verbinden, «Was steht an?» schreiben.
Wie es weitergeht, steht in der <a href="https://stayingclean.github.io/toolbox/claude-anleitung/">Anleitung «Mit Claude arbeiten»</a>.</p>
<div class="box">Zip in einen neuen Ordner entpacken (Windows: Rechtsklick → «Alle extrahieren»; Mac: Doppelklick). Darin liegt <code>START-HIER.txt</code> — mehr musst du nicht lesen.
Claude stellt die Fragen und legt die Dateien selber an; du legst nur deine Unterlagen in <code>1_Meine-Unterlagen</code>.
Zwei Aufgaben: zwei Zips herunterladen, in zwei Ordner entpacken.</div>
{{KARTEN}}
<a class="big" href="grundgeruest.zip" style="background:var(--card);color:var(--accent-dark);border:1px solid var(--border);margin-top:22px">↓ Leerer Ordner für eine eigene Aufgabe (grundgeruest.zip)</a>
<a class="big" href="platzhalter.exe" style="background:var(--card);color:var(--accent-dark);border:1px solid var(--border)">↓ platzhalter.exe — Adresse, Telefon und IBAN am Schluss einsetzen</a>
<a class="big" href="platzhalter-mac.zip" style="background:var(--card);color:var(--accent-dark);border:1px solid var(--border)">↓ platzhalter-mac.zip — dasselbe für den Mac</a>
<footer>
<div>Quelle und Mitarbeit: <a href="https://github.com/stayingclean/ki-tasks">github.com/stayingclean/ki-tasks</a> · Teil der <a href="https://stayingclean.github.io/toolbox/">Toolbox</a></div>
<div class="footer-links"><a class="footer-credit" href="https://github.com/stayingclean" target="_blank" rel="noopener"><img class="footer-avatar" src="https://github.com/stayingclean.png?size=80" alt="stayingclean" loading="lazy" width="28" height="28"><span>Erstellt von stayingclean</span></a>
<span aria-hidden="true">·</span><a class="footer-coffee" href="https://buymeacoffee.com/stayingclean" target="_blank" rel="noopener"><span aria-hidden="true">☕</span><span>Kaffee spendieren</span></a></div>
</footer></div>
<aside class="spalte" id="faellig" data-rahmen=".wrap" hidden aria-labelledby="faellig-titel"><h2 id="faellig-titel">Jetzt fällig</h2></aside>
</div>
<script src="faellig.js"></script>
</body></html>
"""

# Wird als dist/faellig.js veröffentlicht, {{DATEN}} durch faellig.json ersetzt.
# Bewusst ES5 und ohne fetch: läuft so auch per file:// und in alten Browsern.
FAELLIG_JS = """/* «Jetzt fällig» — gebaut von stayingclean/ki-tasks (build.py), nicht von Hand ändern.

   Gerechnet wird mit dem heutigen Datum im Browser, weil die Seiten nur bei einem
   Push neu gebaut werden. Zum Ausprobieren: ?heute=2026-11-20

   Was das Skript auf einer Seite tut, hängt davon ab, was es vorfindet:
   - <aside id="faellig" data-rahmen="…"> (Download-Seite): füllt die Spalte und
     gibt dem Rahmen die Klasse mit-spalte.
   - Seite der Anleitung (.layout, geladen von anleitung.js): legt dieselbe Spalte
     selbst an, auf jeder Unterseite gleich.
   - Karten (.card[data-aufgabe] oder .card mit Link auf <name>.html): Abzeichen.
   - Seitenleiste der Anleitung (.nav a[href="<name>.html"]): Klasse ist-faellig.
   Ist nichts fällig, tut es nichts. */
(function () {
  if (window.faelligGeladen) { return; }
  window.faelligGeladen = true;

  var d = {{DATEN}};
  var DOWNLOAD = 'https://stayingclean.github.io/ki-tasks/';
  var q = /[?&]heute=(\\d{4})-(\\d{2})-(\\d{2})/.exec(location.search);
  var jetzt = new Date();
  var heute = q ? new Date(+q[1], q[2] - 1, +q[3]) : new Date(jetzt.getFullYear(), jetzt.getMonth(), jetzt.getDate());
  var MONATE = ['Januar','Februar','März','April','Mai','Juni','Juli','August','September','Oktober','November','Dezember'];
  // In der Anleitung liegen die Aufgabenseiten nebenan; auf der Download-Seite nicht
  var inAnleitung = !!document.querySelector('.layout');

  function esc(t) { return String(t).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;'); }
  // "MM-TT" → nächstes Vorkommen ab heute (heute zählt noch)
  function naechstes(mmtt) {
    var t = mmtt.split('-'), x = new Date(heute.getFullYear(), t[0] - 1, +t[1]);
    if (x < heute) { x = new Date(heute.getFullYear() + 1, t[0] - 1, +t[1]); }
    return x;
  }
  function tage(x) { return Math.round((x - heute) / 864e5); }
  function datum(x) { return x.getDate() + '. ' + MONATE[x.getMonth()]; }
  function rest(n) {
    var t = n === 0 ? 'heute' : n === 1 ? 'morgen' : 'noch ' + n + ' Tage';
    return '<span class="rest' + (n <= 14 ? ' knapp' : '') + '">' + t + '</span>';
  }
  var aufgaben = {};
  d.aufgaben.forEach(function (a) { aufgaben[a.name] = a; });
  function kopf(name) {
    var a = aufgaben[name] || { name: name, titel: name };
    var ziel = a.seite ? (inAnleitung ? name + '.html' : a.seite) : DOWNLOAD + name + '.zip';
    return '<h3><a href="' + esc(ziel) + '">' + esc(a.navtitel || a.titel) + '</a></h3>';
  }

  var faellig = [];  // [{name, inhalt}] in der Reihenfolge der Spalte

  // Aufgaben mit Saisonfenster aus INFO.md: "faellig: 10-01 bis 11-30"
  d.aufgaben.forEach(function (a) {
    if (!a.faellig) { return; }
    var f = a.faellig.split(/\\s*bis\\s*/), bis = naechstes(f[1]), von = naechstes(f[0]);
    // Im Fenster, wenn das nächste Ende vor dem nächsten Anfang kommt (oder heute beginnt)
    if (bis < von || tage(von) === 0) {
      faellig.push({ name: a.name, inhalt:
        '<ul><li><span>bis ' + datum(bis) + '</span>' + rest(tage(bis)) + '</li></ul>' +
        (a['faellig-text'] ? '<p>' + esc(a['faellig-text']) + '</p>' : '') });
    }
  });

  // Fristen je Kanton aus fristen/<aufgabe>.json: nur feste Daten innerhalb des Vorlaufs
  Object.keys(d.fristen).forEach(function (name) {
    var f = d.fristen[name], vorlauf = f.vorlauf_tage || 60, zeilen = [];
    (f.kantone || []).forEach(function (k) {
      if (k.art !== 'datum' || !k.frist) { return; }
      var x = naechstes(k.frist), n = tage(x);
      if (n > vorlauf) { return; }
      var fuer = x.getFullYear() + ({ vorjahr: 1, anspruchsjahr: 0, folgejahr: -1 }[k.jahr] || 0);
      zeilen.push({ n: n, html: '<li><a href="' + esc(k.quelle) + '" title="' + esc(k.notiz || '') + '">' +
        esc(k.name) + ' · ' + datum(x) + ' <small>(für ' + fuer + ')</small></a>' + rest(n) + '</li>' });
    });
    if (!zeilen.length) { return; }
    zeilen.sort(function (a, b) { return a.n - b.n; });
    faellig.push({ name: name, inhalt: (f.titel ? '<p>' + esc(f.titel) + '</p>' : '') +
      '<ul>' + zeilen.map(function (z) { return z.html; }).join('') + '</ul>' +
      '<p class="klein">' + esc(f.hinweis || '') + (f.stand ? ' Stand ' + esc(f.stand) + '.' : '') + '</p>' });
  });

  if (!faellig.length) { return; }

  var spalte = document.getElementById('faellig');
  var layout = document.querySelector('.layout');
  if (!spalte && layout) {
    // Anleitung: rechts neben main, als drittes Kind von .layout (Stile in stil.css)
    layout.insertAdjacentHTML('beforeend', '<aside class="spalte" id="faellig" data-rahmen=".layout" hidden ' +
      'aria-labelledby="faellig-titel"><h2 id="faellig-titel">Jetzt fällig</h2></aside>');
    spalte = document.getElementById('faellig');
  }
  if (spalte) {
    spalte.insertAdjacentHTML('beforeend', faellig.map(function (e) { return kopf(e.name) + e.inhalt; }).join(''));
    spalte.hidden = false;
    var rahmen = document.querySelector(spalte.getAttribute('data-rahmen') || '.wrap');
    if (rahmen) { rahmen.classList.add('mit-spalte'); }
  }

  faellig.forEach(function (e) {
    var karte = document.querySelector('.card[data-aufgabe="' + e.name + '"]');
    if (!karte) {
      var link = document.querySelector('.card a[href="' + e.name + '.html"]');
      karte = link && link.closest('.card');
    }
    if (karte && !karte.classList.contains('ist-faellig')) {
      karte.classList.add('ist-faellig');
      karte.insertAdjacentHTML('afterbegin', '<span class="badge">Jetzt fällig</span>');
    }
    var nav = document.querySelector('.nav a[href="' + e.name + '.html"]');
    if (nav) { nav.classList.add('ist-faellig'); }
  });
})();
"""


def main() -> None:
    DIST.mkdir(exist_ok=True)
    for alt in DIST.glob("*.zip"):
        alt.unlink()
    tasks = alle_aufgaben()
    baue_zip(None, "grundgeruest")
    for t in tasks:
        baue_zip(t, t.name)
    infos = [lese_info(t) for t in tasks]
    schreibe_index(infos)
    schreibe_faellig(infos)
    print(f"{len(tasks)} Aufgaben, Zips in {DIST}")


if __name__ == "__main__":
    sys.exit(main())
