# «Jetzt fällig» in der Anleitung (stayingclean/toolbox)

Was in `stayingclean/toolbox` zu ändern ist, damit fällige Aufgaben in der
Anleitung unter `/toolbox/claude-anleitung/` auffallen. Die Hauptseite der
Toolbox bleibt, wie sie ist.

## Wie es zusammenhängt

`build.py` in ki-tasks veröffentlicht neben der Download-Seite:

- `https://stayingclean.github.io/ki-tasks/faellig.json`: Daten (`faellig:` aus
  `INFO.md`, `fristen/*.json`)
- `https://stayingclean.github.io/ki-tasks/faellig.js`: dieselben Daten plus
  Darstellung. Das ist die einzige Stelle, die ausrechnet, was fällig ist.

Weil Toolbox und ki-tasks auf derselben Origin liegen (`stayingclean.github.io`),
kann jede Anleitungsseite das Skript laden. Je nachdem, was es auf der Seite
findet, tut es Folgendes:

| findet | tut |
|---|---|
| `<aside id="faellig" data-rahmen=".layout">` (nur `aufgaben.html`, kommt aus ki-tasks) | füllt die Spalte, gibt `.layout` die Klasse `mit-spalte` |
| `.card` mit Link auf `<name>.html` | Abzeichen «Jetzt fällig», Klasse `ist-faellig` |
| `.nav a[href="<name>.html"]` | Klasse `ist-faellig` (Punkt in der Seitenleiste) |
| Seite `<name>.html` mit `header.page` | Band `.faellig-band` unter dem Kopf |

Ist nichts fällig, tut das Skript nichts: Die Spalte bleibt `hidden`, das Layout
bleibt zweispaltig.

## 1. `docs/claude-anleitung/stil.css`

Als Ganzes vor dem Block `@media print` anhängen (also nach dem bestehenden
`@media (max-width: 860px)`), und in `@media print` `.spalte` zu den
ausgeblendeten Elementen nehmen.

```css
/* «Jetzt fällig»: faellig.js aus stayingclean/ki-tasks. Ohne fälligen Eintrag
   bleibt die Spalte hidden und .layout zweispaltig. */
.layout.mit-spalte { grid-template-columns: var(--sidebar) minmax(0, 1fr) 300px; }
.spalte { position: sticky; top: 24px; align-self: start; margin: 44px 24px 0 0; padding: 16px 18px;
  background: var(--card); border: 1px solid #F2D3B0; border-top: 4px solid var(--warn); border-radius: 14px; font-size: .88rem; }
.spalte h2 { font-family: var(--font-body); font-size: .78rem; text-transform: uppercase; letter-spacing: .08em; color: var(--warn); margin: 0 0 4px; }
.spalte h3 { font-size: .95rem; margin: 16px 0 4px; }
.spalte h3 a { text-decoration: none; }
.spalte h3 a:hover { text-decoration: underline; }
.spalte p, .faellig-band p { margin: 0 0 6px; }
.spalte ul, .faellig-band ul { list-style: none; margin: 6px 0; padding: 0; }
.spalte li, .faellig-band li { display: flex; justify-content: space-between; gap: 8px; padding: 4px 0; margin: 0; border-top: 1px solid var(--border); }
.spalte li a { color: var(--text); text-decoration: none; }
.spalte li a:hover { color: var(--accent); }
.rest { color: var(--muted); white-space: nowrap; }
.rest.knapp { color: var(--warn); font-weight: 600; }
.spalte .klein { color: var(--muted); font-size: .78rem; margin-top: 8px; }
.badge { display: inline-block; font-size: .72rem; font-weight: 600; text-transform: uppercase; letter-spacing: .05em;
  color: var(--warn); background: var(--warn-tint); border-radius: 999px; padding: 2px 9px; margin-bottom: 6px; }
.card.ist-faellig { border-color: #F2D3B0; box-shadow: inset 0 3px 0 var(--warn); }
.nav a.ist-faellig::after { content: ''; display: inline-block; width: 7px; height: 7px; margin-left: 7px;
  border-radius: 50%; background: var(--warn); vertical-align: middle; }
.faellig-band { border-left: 4px solid var(--warn); background: var(--warn-tint); padding: 12px 16px; border-radius: 0 12px 12px 0; margin: 0 0 24px; font-size: .95rem; }
.faellig-band .kicker { color: var(--warn); }
/* Zu schmal für drei Spalten: Spalte über den Inhalt, Seitenleiste über beide Zeilen */
@media (max-width: 1180px) {
  .layout.mit-spalte { grid-template-columns: var(--sidebar) minmax(0, 1fr); }
  .layout.mit-spalte .sidebar { grid-row: 1 / span 2; }
  .layout.mit-spalte .spalte { grid-column: 2; grid-row: 1; position: static; margin: 28px 48px 0; max-width: 764px; }
  .layout.mit-spalte main { grid-column: 2; grid-row: 2; padding-top: 28px; }
}
/* Handy: Spalte unter der Seitenleiste, über dem Inhalt. Muss nach dem
   1180er-Block stehen, sonst gewinnt dessen grid-row (gleiche Spezifität). */
@media (max-width: 860px) {
  .layout.mit-spalte { grid-template-columns: 1fr; }
  .layout.mit-spalte .sidebar, .layout.mit-spalte .spalte, .layout.mit-spalte main { grid-column: 1; grid-row: auto; }
  .layout.mit-spalte .spalte { order: 1; margin: 20px 18px 0; max-width: none; }
  .layout.mit-spalte main { order: 2; padding-top: 20px; }
}
```

`--warn` und `--warn-tint` gibt es schon. `#F2D3B0` ist der Rand, den auch die
Download-Seite benutzt (dort `--warn-border`). Wer will, nimmt ihn als Variable
in `:root` auf.

## 2. `docs/claude-anleitung/anleitung.js`

Am Ende der IIFE, nach der Seitenleiste (das Skript markiert Links darin, die
Leiste muss also schon stehen):

```js
  /* «Jetzt fällig» kommt aus stayingclean/ki-tasks (build.py → faellig.js):
     Punkt in der Seitenleiste, Band auf der Aufgabenseite, Spalte auf
     aufgaben.html. Gleiche Origin, darum kein CORS. aufgaben.html bindet das
     Skript zusätzlich selbst ein; es läuft trotzdem nur einmal
     (window.faelligGeladen). Ohne Netz fehlt nur die Markierung. */
  var faellig = document.createElement('script');
  faellig.src = 'https://stayingclean.github.io/ki-tasks/faellig.js';
  faellig.async = true;
  document.body.appendChild(faellig);
```

## 3. `tools/anleitung_aufgaben.py` und Deploy

Hier ist nichts zu tun. Das Skript liest aus `INFO.md` nur `navtitel:` und
`reihenfolge:`; `faellig:` und `faellig-text:` stören nicht. Freiwillig: In
`tests/test_anleitung_aufgaben.py` eine `INFO.md` mit diesen Feldern
mittesten, damit das so bleibt.

Ein Neubau der Toolbox ist für neue Fristen nicht nötig: `faellig.js` wird
bei jedem Laden der Seite frisch von ki-tasks geholt.

## Reihenfolge beim Ausrollen

1. Toolbox: `stil.css` und `anleitung.js` auf `master`. Ohne `faellig.js`
   drüben lädt das Skript ins Leere (404), sonst ändert sich nichts.
2. ki-tasks: Branch `download-faellig` mergen. Der Deploy veröffentlicht
   `faellig.js` und stösst den Toolbox-Deploy an, der das neue
   `aufgaben.html` mit der Spalte übernimmt.

Umgekehrt stünde die Spalte auf `aufgaben.html` kurz ohne Stil unter dem Inhalt.

## Prüfen

`aufgaben.html?heute=2026-11-15`: Spalte mit Krankenkasse und fünf Kantonen
(31. Dezember), Karten markiert, Punkt bei Krankenkasse und Prämienverbilligung.
`krankenkasse.html?heute=2026-11-15`: Band unter dem Kopf.
`aufgaben.html?heute=2026-06-05`: keine Spalte, zweispaltig wie bisher.
Breiten 1400, 1000 und 375 px.
