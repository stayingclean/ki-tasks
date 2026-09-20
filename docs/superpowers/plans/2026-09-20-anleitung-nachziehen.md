# Anleitung nachziehen: Toolbox ausmisten, zwei Seiten nach ki-tasks

Folgearbeit zum Umbau vom 20.09.2026
(`../specs/2026-09-20-ki-tasks-vereinfachung-design.md`, PR #3).

Nach dem Merge beschreibt die Anleitung unter
`stayingclean.github.io/toolbox/claude-anleitung/` durchgehend einen Aufbau, den
es nicht mehr gibt. Der Link auf `alle-aufgaben.zip` liefert bereits 404.

## Der Entscheid

Die Anleitung ist nicht eine Sache, sondern zwei:

| Seiten | Worum es geht | Ändert sich, wenn … |
|---|---|---|
| index, voraussetzungen, abos, alternativen, prompts | Claude allgemein | Anthropic etwas ändert |
| datenschutz | was ein KI-Anbieter speichert | Rechtslage oder Einstellungen |
| arbeitsablauf, ordner-dateien, auftraege, auftragsvorlagen, md-dateien, workflow-* | **der ki-tasks-Ordner** | **ki-tasks umgebaut wird** |

Die dritte Gruppe muss sich im Gleichschritt mit dem Ordner ändern. Genau dieser
Gleichschritt ist schon einmal gebrochen — deshalb ziehen diese Seiten nach
`ki-tasks/anleitung/` um. **Was sich zusammen ändern muss, soll zusammen liegen.**

Der Umzug ist klein: Nach dem Umbau bleiben davon zwei Seiten übrig («Der
Ordner» und «Platzhalter einsetzen»), weil es keine Dateien zum Erklären, keine
Aufträge zum Schreiben, keine Markdown-Editoren zum Installieren und keine
Vorlagen zum Kopieren mehr gibt. Der Katalog existiert bereits als
`stayingclean.github.io/ki-tasks/`, gebaut aus `INFO.md`.

## Die URL bleibt

GitHub Pages bedient pro Projekt-Repo genau einen Pfad
(`<user>.github.io/<repo>/`). `/toolbox/…` kann nur der Deploy des
`toolbox`-Repos ausliefern; es gibt keine Pfad-Delegation. Der Toolbox-Deploy
darf die Quelle aber woanders herholen — Checkout von ki-tasks beim Bauen.

Bewusst **kein** `repository_dispatch` mit PAT: Ein Token, das abläuft, ist mehr
Risiko als ein Tag Verzögerung. Stattdessen ein nächtlicher `schedule` plus
`workflow_dispatch`.

Bekannter Nachteil: Jede der 13 Anleitungsseiten trägt ihren eigenen inline
`<style>`-Block (20–25 KB). Bringen die ki-tasks-Seiten eine eigene Kopie mit,
erreicht sie eine spätere Designänderung nicht. Darum zuerst das gemeinsame CSS
nach `docs/claude-anleitung/stil.css` herauslösen — eine Hygiene, die ohnehin
fehlte.

## Reihenfolge

Erst Toolbox (CSS herauslösen, ausmisten, `deploy.yml` verdrahten), danach
ki-tasks (die zwei Seiten gegen das dann existierende `stil.css` schreiben).

---

## Prompt 1 — Toolbox-Repo

```
Repo stayingclean/toolbox. Der Anleitungs-Branch liegt als Worktree unter
C:\workspace\toolbox-anleitung (Branch claude-anleitung).

WICHTIG: C:\workspace\eraschle ist ein anderer Checkout desselben Repos, steht
auf einem anderen Branch und hat uncommittete Änderungen. Dort nichts anfassen.
Arbeite in einem eigenen Worktree.

Lies zuerst im Repo C:\workspace\ki-tasks:
  docs/superpowers/specs/2026-09-20-ki-tasks-vereinfachung-design.md
  grundgeruest/START-HIER.txt
  grundgeruest/CLAUDE.md
  platzhalter/README.md

Kurz: ki-tasks wurde grundlegend vereinfacht. Der Benutzer bearbeitet keine
Markdown-Datei mehr. Er entpackt ein Zip, verbindet den Ordner in Cowork und
schreibt genau einen Satz: "Was steht an?". Claude stellt die Fragen und führt
alle Dateien selbst. Weg sind: die acht Schritte, regeln.md, profil.md, log.md,
aufgaben.md, die Auftrags-Dateien und die Ordner 00 bis 04. Neu: START-HIER.txt,
CLAUDE.md, 1_Meine-Unterlagen, 2_Arbeitsstand (mit verlauf/), 3_Zum-Versenden,
9_Claude (wissen.md + stand.md). alle-aufgaben.zip gibt es nicht mehr.

Entschieden ist: Seiten, die den ki-tasks-Ordner beschreiben, ziehen nach
ki-tasks um, weil sie sich mit ihm zusammen ändern müssen. Die URL
stayingclean.github.io/toolbox/claude-anleitung/ bleibt bestehen. Seiten über
Claude im Allgemeinen bleiben in der Toolbox.

AUFGABE 1 - gemeinsames CSS herauslösen.
Jede Seite in docs/claude-anleitung/ trägt einen eigenen inline <style>-Block.
Zieh den gemeinsamen Teil nach docs/claude-anleitung/stil.css und ersetz ihn in
allen Seiten durch ein <link>. Seitenspezifische Regeln dürfen inline bleiben.
Prüf danach jede Seite im Browser - das muss pixelgleich aussehen.

AUFGABE 2 - ausmisten. Diese Seiten beschreiben Dinge, die es nicht mehr gibt:
  - ordner-dateien.html   (regeln.md, profil.md, log.md, Ordner 00 bis 04)
  - auftraege.html        (Aufträge schreibt niemand mehr von Hand)
  - md-dateien.html       (Markdown-Editoren - der Benutzer bearbeitet nichts mehr)
  - auftragsvorlagen.html (hartcodierte Kacheln, toter alle-aufgaben.zip-Link,
                           eingebettete Volltexte gelöschter Auftragsdateien)
Ersatzlos löschen. Ihr Inhalt geht in zwei neue Seiten, die aus ki-tasks kommen
(siehe Aufgabe 4). Alle Navigations- und Querverweise auf diese vier Seiten
anpassen. Prüf mit grep, dass kein toter Link übrig bleibt.

  - arbeitsablauf.html und workflow-bewerbung.html / workflow-gesuch.html:
    Entscheide begründet, ob sie bleiben, umziehen oder verschwinden. Der
    Arbeitsablauf beschreibt den Ordner, gehört also eher nach ki-tasks.

AUFGABE 3 - was bleibt, korrigieren.
  - datenschutz.html: Der Ton stimmt nicht mehr. Bisher sinngemäss "lege keine
    sensiblen Dinge ab", was den Schluss nahelegt, der Rest sei unbedenklich -
    während die Aufgabe dann Kontoauszüge und Steuerrechnungen verlangt. Neu:
    Alles im Ordner geht an Anthropic, und das ist bei Gesuchen auch nötig,
    damit Claude Beträge gegen Belege prüfen kann. Nie hinein gehören
    AHV-Ausweis, Bankkarten, Passwörter, Unterlagen Dritter. Claude macht die
    Triage im Gespräch. Die abgestimmte Fassung steht in
    ki-tasks/grundgeruest/START-HIER.txt. Von hier auf die neue
    Platzhalter-Seite verlinken.
  - index.html, voraussetzungen.html, abos.html, alternativen.html,
    prompts.html: durchsehen, vermutlich nur kleine Korrekturen. Überall, wo
    der Einstieg beschrieben wird, gilt neu: entpacken, Ordner verbinden,
    "Was steht an?" - und sonst nichts.
  - beispiel-projekt/ und docs/claude-anleitung/beispiel-projekt.zip bilden den
    alten Aufbau ab (auftraege/, profil.md, regeln.md, kriterien.md, log.md).
    Ein Beispielordner, in dem der Benutzer nichts mehr ausfüllt, zeigt wenig.
    Vorschlag machen: löschen oder auf den neuen Aufbau bringen.

AUFGABE 4 - deploy.yml: Anleitungsseiten aus ki-tasks holen.
In .github/workflows/deploy.yml vor "Upload artifact" einfügen:

  - name: Anleitung aus ki-tasks holen
    uses: actions/checkout@v4
    with:
      repository: stayingclean/ki-tasks
      path: _ki-tasks
  - name: Einsetzen
    run: cp -r _ki-tasks/anleitung/. docs/claude-anleitung/

Und den Auslöser ergänzen, damit eine Änderung in ki-tasks nicht liegenbleibt:

  on:
    push: { branches: [master] }
    schedule: [{ cron: "0 5 * * *" }]
    workflow_dispatch:

Bewusst kein repository_dispatch mit PAT - ein Token, das abläuft, ist mehr
Risiko als ein Tag Verzögerung. Der Ordner _ki-tasks darf nicht im Artefakt
landen; prüf das.

Der Ordner ki-tasks/anleitung/ existiert noch nicht - er entsteht in einer
zweiten Sitzung. Bau den Workflow so, dass er nicht scheitert, solange der
Ordner fehlt, und halt an dieser Stelle an, statt die Seiten selbst zu
erfinden.

AUFGABE 5 - den Katalog entdoppeln.
Der Kurzbeschrieb jeder Aufgabe stand hartcodiert in auftragsvorlagen.html und
steht in ki-tasks/aufgaben/<name>/INFO.md. ki-tasks veröffentlicht bereits
https://stayingclean.github.io/ki-tasks/aufgaben.json mit name, titel, gruppe
und kurz. Wo künftig Kacheln stehen sollen, aus dieser Datei rendern (fetch im
Browser) oder schlicht auf stayingclean.github.io/ki-tasks/ verlinken. Keine
zweite Kopie der Beschreibungen.

Vorgehen: Zeig mir zuerst eine Übersicht pro Seite - bleibt / ändert sich /
zieht um / verschwindet, mit je einem Satz Begründung, und dazu deinen
Vorschlag für arbeitsablauf und die beiden workflow-Seiten. Erst nach meiner
Zustimmung anfangen zu schreiben.

Sprache: Deutsch (Schweiz), ss statt ß, Du-Form, kurz, keine Ausrufezeichen.
Bauen und prüfen wie in CLAUDE.md des Repos beschrieben.
```

---

## Prompt 2 — ki-tasks, erst nach Prompt 1

```
Repo C:\workspace\ki-tasks. Arbeite in einem eigenen Worktree.

Lies zuerst:
  docs/superpowers/specs/2026-09-20-ki-tasks-vereinfachung-design.md
  grundgeruest/START-HIER.txt, grundgeruest/CLAUDE.md
  platzhalter/README.md
  README.md

Im Toolbox-Repo (C:\workspace\toolbox-anleitung, Branch claude-anleitung) wurde
die Anleitung ausgemistet und das gemeinsame CSS nach
docs/claude-anleitung/stil.css herausgelöst. Der Deploy dort holt neu den
Ordner anleitung/ aus DIESEM Repo und kopiert ihn nach docs/claude-anleitung/.
Die Seiten erscheinen also unter
stayingclean.github.io/toolbox/claude-anleitung/ - die Links darin sind relativ
und zeigen auf die dort verbliebenen Seiten.

Leg anleitung/ an mit zwei Seiten. Schau dir eine verbliebene Toolbox-Seite als
Vorlage an: gleicher Seitenkopf, gleiche Navigation, <link> auf stil.css, kein
eigener CSS-Block ausser für wirklich Seitenspezifisches.

1. der-ordner.html - "Der Ordner"
   Was nach dem Entpacken drinliegt und was Claude darin tut. Vier Ordner
   (1_Meine-Unterlagen, 2_Arbeitsstand mit verlauf/, 3_Zum-Versenden,
   9_Claude), START-HIER.txt, CLAUDE.md. Dazu das Ablaufdiagramm aus dem
   gelöschten grundgeruest/README.md - hol es aus der Git-History (git log --
   grundgeruest/README.md) und pass es auf den neuen Aufbau an. Als Mermaid
   funktioniert es auf einer statischen Seite nicht ohne Weiteres; entweder als
   SVG einbetten oder in eine schlichte Bildbeschreibung umbauen.
   Tonfall: "so arbeitet Claude darin", nicht "so machst du es". Der Benutzer
   muss hier nichts lernen - die Seite ist zum Nachschauen, nicht zum Befolgen.

2. platzhalter.html - "Adresse und IBAN am Schluss einsetzen"
   Das Tool ist in der Anleitung bisher überhaupt nicht beschrieben.
   - Download: https://stayingclean.github.io/ki-tasks/platzhalter.exe
   - Wozu: Claude lässt jede Lücke als benannten Platzhalter in eckigen
     Klammern stehen - [ADRESSE], [IBAN], aber auch [Einzugsdatum] oder
     [Monatsmiete]. Dadurch kommen Adresse, Telefonnummer und IBAN
     nie in eine Datei, die Claude liest. Am Schluss setzt das Tool sie lokal
     ein, ohne Internet.
   - Bedienung: starten, Ordner 2_Arbeitsstand wählen, Werte eintragen, was
     leer bleibt bleibt stehen, "Ersetzen". Von jeder geänderten Datei liegt
     danach eine Sicherung .docx.bak daneben. Eingegebene Werte werden nirgends
     gespeichert.
   - Ehrlich erwähnen: Windows SmartScreen warnt beim ersten Start, weil die
     Datei nicht signiert ist ("Weitere Informationen" -> "Trotzdem
     ausführen"). In Word geöffnete Dateien lassen sich nicht ändern. Nur
     .docx, kein altes .doc. Der Unterordner verlauf wird ausgelassen, damit
     alte Fassungen nicht nachträglich mit echten Daten gefüllt werden.
   Details stehen in platzhalter/README.md - nicht abschreiben, für Laien
   formulieren.

Ergänze README.md und CLAUDE.md dieses Repos um einen Absatz: anleitung/
enthält die Seiten, die den Ordner beschreiben, wird vom Toolbox-Deploy geholt
und erscheint unter der Toolbox-URL. Wer den Ordneraufbau ändert, ändert diese
Seiten mit - das ist der Grund, warum sie hier liegen.

Prüf zum Schluss, dass python build.py weiterhin läuft und anleitung/ nicht
versehentlich in den Zips landet.

Sprache: Deutsch (Schweiz), ss statt ß, Du-Form, kurz, keine Ausrufezeichen.
```
