# Stelle suchen: Dauerbetrieb mit RAV, Projekt und Status-Ordnern

Stand 24.09.2026. Baut die Aufgabe `stelle` von einem einzelnen Durchgang zu
einer Stellensuche über Wochen und Monate aus, auf Wunsch mit RAV-Monatsabschluss.

## Warum

`stelle` sucht einmal, schreibt Motivationsschreiben und führt eine einfache
`arbeitsbemuehungen.md`. Wer arbeitslos ist, braucht mehr:

- **Wiederholte Suchen**, die sich merken, was schon vorgeschlagen und
  abgelehnt wurde — sonst schlägt Claude täglich dieselbe Stelle vor.
- **Den Stand jeder Bewerbung**, sichtbar ohne eine Datei zu öffnen: was läuft,
  wo kam eine Absage, wo ein Gespräch.
- **Den Monatsabschluss fürs RAV** aus denselben Daten: Nachweis der
  Arbeitsbemühungen bis zum 5., Angaben der versicherten Person (AvP) zum
  Monatsende, Dateien für Job-Room.
- **Eine automatische Suche**, wo Cowork das kann.

Eine zweite Aufgabe neben `stelle` wurde verworfen: Rund 70 % wären gleich und
würden auseinanderlaufen. Das RAV ist darum ein Schalter innerhalb von `stelle`.

## Entscheide

### Ein Schalter in `stand.md`, per Satz umschaltbar

- **`RAV: ja | nein`** — Claude fragt beim ersten Gespräch mit Beruf und Ort:
  «Bist du beim RAV angemeldet oder meldest du dich bald an?» Bei `ja` dazu
  Kanton und Anmeldedatum. Bei `nein` keine Monatsaufgaben; die Bewerbungen
  werden trotzdem so geführt, dass ein Nachweis jederzeit erstellt werden kann.

Die Person füllt keine Datei aus. «Ich bin jetzt beim RAV angemeldet» genügt;
Claude schreibt es um.

### Dateien, die Claude führt

```
9_Claude/
  wissen.md             mitgeliefert, Fachwissen (diese Aufgabe)
  stand.md              Auftrag, Schalter, gespeicherte Angaben, offene Punkte
  suche-stellen.md      Suchprofil, Portale, Rhythmus, Schwellen, letzte Suche
2_Arbeitsstand/
  stellen.md            jede gefundene Stelle mit Entscheid (Gedächtnis)
  bewerbungen/
    1_in-Vorbereitung/
    2_Beworben/
    3_Im-Gespraech/
    4_Absage/
    5_Zusage/
  rav/JJJJ-MM/          nur bei RAV: ja
  verlauf/
3_Zum-Versenden/        Postausgang: nur, was jetzt raus muss
```

Alle Dateien und Ordner legt Claude zur Laufzeit an. Die Aufgabe im Repo bleibt
bei `INFO.md` und `9_Claude/wissen.md`.

**`suche-stellen.md`** enthält:

- Suchprofil, aus Lebenslauf und Dossier abgeleitet und einmal im Chat
  bestätigt: Berufsbezeichnungen mit Varianten, Region und Umkreis, Pensum,
  Ausschlüsse, Muss-Stichworte.
- Portale. Standard, abrufbar ohne Login: jobs.ch, jobup.ch, jobscout24.ch,
  job-room.ch, jobwinner.ch. Nur als Link (blockieren den Abruf): indeed.ch,
  LinkedIn — Claude gibt dafür die fertige Suchadresse zum Selberöffnen.
- Rhythmus (täglich, werktags, wöchentlich) und Datum der letzten Suche.
- Schwellen, per Satz änderbar: Wiedervorlage nach **7 Tagen** ohne neue
  Stelle, abgelehnte Stellen frühestens nach **14 Tagen**, höchstens **3** auf
  einmal; Nachfassen nach **3 Wochen** ohne Antwort.
- Voreinstellung Dossierform, sobald bekannt: z. B. «Portal → getrennte PDF,
  E-Mail → ein PDF».

**`stellen.md`** — eine Zeile je gefundener Stelle: Nr., gefunden am, Firma,
Stelle, Ort, Pensum, Portal mit Referenznummer, Link, Passung 1–5, Hauptgrund
dagegen, Entscheid (`offen`, `beworben → <Ordner>`, `abgelehnt <Datum>: <Grund>`,
`abgelaufen`), Zuweisung RAV ja/nein, via Vermittler. Dieselbe Stelle auf
mehreren Portalen erkennt Claude an Firma und Titel und führt sie einmal.

### Status-Ordner statt Status-Spalte

Eine Bewerbung ist **ein Ordner, der mit ihrem Stand wandert**. Die Nummern
folgen dem Ablauf; der Stand ist im Explorer sichtbar.

- Name: `JJJJ-MM-TT_<Firma>_<Stelle>`, Datum = Bewerbungsdatum (bis zum
  Versand das Datum des Entwurfs). So sortiert der Explorer in der Reihenfolge
  des RAV-Formulars.
- Über einen Vermittler: `JJJJ-MM-TT_<Vermittler>_fuer-<Firma>_<Stelle>`
  (Firma weglassen, wenn unbekannt). Kein eigener Vermittler-Ordner — ein
  Vermittler ist eine Art der Bewerbung, kein Stand.
- Abgelehnte Stellen bekommen keinen Ordner, nur die Zeile in `stellen.md`.
- Kein Ordner für «keine Antwort»: Nach der Nachfass-Schwelle fragt Claude
  «Nachfassen oder als Absage ablegen?»; abgelegt wird nach `4_Absage/` mit
  Grund «keine Antwort».
- `3_Zum-Versenden/` ist der Postausgang. Leer heisst: nichts zu senden. Auf die
  Rückmeldung «gesendet» verschiebt Claude die PDF in den Bewerbungsordner und
  den Ordner nach `2_Beworben/`.

### Vorschläge und Wiedervorlage

- Vorgeschlagen wird nur, was nicht in `stellen.md` steht. «Keine neuen
  Stellen» ist eine gültige Antwort.
- Wiedervorlage: Nach 7 Tagen ohne neue Stelle prüft Claude abgelehnte Stellen,
  die mindestens 14 Tage zurückliegen, auf «noch online». Höchstens 3 auf
  einmal, jede nur einmal. Zweites Nein ist endgültig.
- **Zuweisung RAV**: Bewerbung ist Pflicht, Ablehnen kann zu Einstelltagen
  führen. Claude nimmt sie mit Vermerk auf und lässt kein Ablehnen zu, sagt
  warum.
- **Zumutbarkeit** (nur bei RAV: ja): Lehnt die Person mit einem Grund ab, der
  vor dem RAV nicht hält (z. B. Arbeitsweg unter 2 Stunden pro Weg), sagt
  Claude es einmal. Die Person entscheidet.

### Keine Platzhalter in dieser Aufgabe

Der Lebenslauf mit Adresse, Telefon und E-Mail liegt ohnehin im Ordner. Die
Absenderangaben übernimmt Claude aus Lebenslauf oder Vorlage. Fehlt eine Angabe
(Eintrittsdatum, Verfügbarkeit, Lohnvorstellung, Arbeitspensum), sucht Claude
in `1_Meine-Unterlagen`, fragt sonst einmal und speichert sie in `stand.md`.
`platzhalter.exe` kommt in dieser Aufgabe nicht vor. AHV-Nummer und IBAN haben
in keiner Bewerbung etwas verloren; im RAV-Nachweis bleibt die AHV-Nummer leer.

Das weicht bewusst von der Regel «Jede Lücke bekommt einen Platzhalter» in
`grundgeruest/CLAUDE.md` ab. `wissen.md` sagt das ausdrücklich, damit Claude
den Widerspruch nicht selbst auflösen muss. Bei 10–12 Bewerbungen im Monat wäre
jedes Mal `platzhalter.exe` ein Umweg ohne Schutzwirkung.

### Ablauf pro Stelle

1. **Entwurf** in `1_in-Vorbereitung/<Ordner>/`: `inserat.pdf` (Druckansicht),
   `inserat.md` (Firma, Stelle, Ort, Pensum, Anforderungen, Frist, Kontakt,
   Bewerbungsweg, Link), `motivationsschreiben.docx`. Liegt in
   `1_Meine-Unterlagen` eine Vorlage, übernimmt Claude Aufbau und Ton und
   schreibt den Inhalt auf das Inserat um; sonst schlichtes Standardformat,
   höchstens eine Seite. Text zuerst im Chat.
2. **Kontrolle** durch die Person, im Chat oder mit Word-Kommentaren.
3. **Versandweg** aus dem Inserat:
   - E-Mail → ein PDF `Bewerbung_<Name>_<Firma>.pdf` (Motivationsschreiben,
     Lebenslauf, Zeugnisse, Diplome) und `mailtext.md`. Ist Gmail o. ä.
     verbunden: Entwurf anlegen. **Nie senden**, auch nicht auf Bitte in einer
     geplanten Aufgabe.
   - Firmenportal → getrennte PDF je Dokumentart, einheitlich benannt. Claude
     legt keine Konten an und schaut nicht hinter ein Login; nennt das Übliche
     und fragt bei Besonderheiten.
   - Unklar → fragen.
   Die erste Antwort wird Voreinstellung in `suche-stellen.md`; danach fragt
   Claude nur bei Abweichung.
4. **Fertig** in `3_Zum-Versenden/<Ordner>/`. Vorher prüfen: Ansprechperson,
   Frist, Inserat noch online. Dateien über 5 MB benennen.
5. **Rückmeldung**: Claude erinnert am Ende jeder fertigen Bewerbung daran und
   bei jedem Sessionstart, solange der Postausgang nicht leer ist. Notiert
   werden Datum und Art (brieflich/elektronisch, persönlich, telefonisch) —
   die Kategorien des RAV-Formulars.

Weitere Rückmeldungen per Satz: «Einladung zum Gespräch» → `3_Im-Gespraech/`,
«Absage, Grund …» → `4_Absage/` mit Grund, «Zusage» → `5_Zusage/`.

### RAV-Monat (nur bei RAV: ja)

Fakten, in `wissen.md` mit Quelle:

- Nachweis der persönlichen Arbeitsbemühungen, Formular 716.007, landesweit.
  Frist 5. Tag des Folgemonats, fällt er aufs Wochenende der nächste Werktag
  (Art. 26 AVIV). Später eingereicht zählt ohne entschuldbaren Grund nicht.
- Felder: Datum, Firma/Adresse/Kontaktperson/Telefon, Stelle, Pensum
  (Vollzeit / Teilzeit %), Zuweisung RAV, Art (brieflich/elektronisch,
  persönlich, telefonisch), Ergebnis (offen, Vorstellungsgespräch, Anstellung,
  Absage mit Grund).
- In Job-Room online erfassbar; Übermittlung ans RAV in der Nacht vom 5. auf
  den 6. PDF-Uploads getrennt nach Dokumenttyp, im Bereich RAV höchstens 5 MB.
- AvP an die Arbeitslosenkasse, zum Monatsende, in Job-Room ab dem 22.; geht
  **nicht** automatisch weg.
- Anzahl: keine Bundeszahl, massgebend ist die Abmachung mit der RAV-Beratung;
  üblich 10–12 pro Monat (z. B. ZH, SH). Qualität zählt; schriftliche,
  zugeschnittene Bewerbungen wiegen mehr als Telefonate.
- **Vermittler**: Die Annahme «alle Bewerbungen über einen Vermittler zählen als
  eine» ist amtlich nicht belegt. Belegt (Merkblatt RAV Schaffhausen): Die
  Anmeldung bei einem Vermittler zählt einmalig als eine Bemühung; danach zählt
  jede Bewerbung auf eine konkret ausgeschriebene Stelle, mit Referenznummer.
  Nur über Vermittler zu suchen genügt nicht (AVIG-Praxis ALE B315). Die
  Zählweise ist kantonale Praxis — Claude bittet, sie beim ersten RAV-Gespräch
  zu bestätigen, und hält die Antwort in `stand.md` fest.
- Belege mindestens 6 Monate aufbewahren; Claude löscht keine
  Bewerbungsordner.

Was Claude liefert, in `2_Arbeitsstand/rav/JJJJ-MM/`:

- `nachweis.md` — die Bemühungen des Monats in der Reihenfolge und mit den
  Feldern von Job-Room bzw. 716.007.
- `nachweis.pdf` — das amtliche Formular ausgefüllt, ohne AHV-Nummer und
  Unterschrift, nur wenn die Person auf Papier/PDF einreicht. Formular von der
  Formularseite auf arbeit.swiss, damit es die aktuelle Fassung ist.
- `hochladen.md` — welche Dateien aus welchen Bewerbungsordnern nach Job-Room
  gehören.
- `avp.md` — die Fragen des AvP mit den Antworten, soweit bekannt; den Rest
  fragt Claude.

Einreichweg (Job-Room oder Papier) fragt Claude beim ersten Abschluss und
speichert ihn. Hinweise beim Sessionstart: ab dem 22. AvP, ab dem 1. Frist des
Nachweises, ab dem 3. mit Nachdruck. Liegt die Zahl der Bemühungen unter der
vereinbarten, sagt Claude es laufend, nicht erst am Monatsende. Claude loggt
sich nie in Job-Room ein.

### Keine Wohnungssuche mehr in dieser Aufgabe

Die Nachfrage «Wohnungen in der Nähe?» am Ende der Stellensuche fällt weg,
samt Portalen und Ablage. Die Aufgabe bleibt bei Stellen und RAV. Fragt die
Person nach einer Wohnung, verweist Claude auf die eigene Aufgabe `wohnung`
(ein eigener Ordner) und sucht nicht in diesem.

### Cowork-Projekt: optional, empfohlen bei RAV oder längerer Suche

Ein Projekt kann nicht im Zip mitkommen; es existiert nur lokal in der App. Die
Anweisungen, die man dort eintragen würde, stehen schon in `CLAUDE.md`. Ein
Projekt bringt: gruppierte Chats, eine geplante Suche, die den Ordner sieht,
eigenes Gedächtnis.

Claude empfiehlt es ausdrücklich bei `RAV: ja` oder wenn die Suche länger
dauert, und erwähnt es sonst nur. Die Vorlage steht in `wissen.md` als
Abschnitt «Projekt einrichten» — als Wissen für Claude, nicht als Formular.
Sagt die Person ja, schreibt Claude die Felder **fertig ausgefüllt** aus
`stand.md` in den Chat:

- Name, Beschreibung (ein Satz), Ordner.
- Anweisungen, nur was ausserhalb des Ordners gilt: zu Beginn jeder Session
  `stand.md` lesen, egal was die erste Nachricht ist; E-Mails nur als Entwurf,
  nie senden; geplante Läufe schreiben ihr Ergebnis nach `stand.md` und
  `stellen.md` und legen keine Bewerbung ohne die Person an.
- Links: Job-Room-Login, die Portale mit Suchadresse, die Seite des
  kantonalen RAV.
- Geplante Aufgabe: Rhythmus und Text; die Person bestätigt.
- Connectors: ist Gmail verbunden, nennt Claude die Grenze (nur Entwürfe).

Was nur die Person weiss (Name der RAV-Beratung, vereinbarte Anzahl), fragt
Claude einzeln und setzt es ein. Es bleibt keine Lücke.

**Grenze der geplanten Suche**: Sie braucht den lokalen Ordner, läuft darum nur
lokal — Computer wach, Claude Desktop offen. Ob verpasste Läufe nachgeholt
werden, ist nicht dokumentiert. Darum ist sie Zusatz, nicht Grundlage: Beim
Sessionstart schaut Claude auf die letzte Suche in `suche-stellen.md` und sucht
nach, wenn sie länger als der Rhythmus zurückliegt.

Ein geplanter Lauf sucht, schreibt neue Treffer in `stellen.md` mit Entscheid
`offen`, legt keine Bewerbungsordner an und schreibt eine Zeile in `stand.md`
(«3 neue Stellen, warten auf Entscheid»).

## Änderungen im Grundgerüst

Gelten für alle Aufgaben.

- **`grundgeruest/CLAUDE.md`, Abschnitt Sitzungsbeginn:** Egal mit welchem Satz
  die Session beginnt, zuerst `stand.md` lesen. Ist etwas fällig oder
  überfällig, in einem Satz nennen, dann erledigen, worum die Person bittet.
- **`grundgeruest/START-HIER.txt`, Schritt 4:** «Was steht an?» bleibt, dazu
  der Hinweis, dass jeder andere Satz auch geht.

Kein eigener Startsatz pro Aufgabe (`start:` in `INFO.md` verworfen): Wenn
jeder Satz funktioniert, ist ein Aufgabensatz nur ein Beispiel, und mehrere
Formeln sind schwerer zu merken als eine.

## Anleitung: `anleitung/stelle.html`

Nur diese Seite wird angefasst; `aufgaben.html`, die Toolbox und die anderen
Seiten nicht (eine andere Session arbeitet daran). Ein neues Muster für
Aufgabenseiten aus jener Session wird beim Zusammenführen nachgezogen.

- Download-Knopf zuoberst (`.download` wie auf `platzhalter.html`) auf
  `https://stayingclean.github.io/ki-tasks/stelle.zip`.
- Abschnitte: Kurzfassung · Was du brauchst · Der Start · Projekt einrichten ·
  Der Ordner · Suchen · Bewerben · Der RAV-Monat · Per Satz ändern · Was Claude
  nicht tut und wo er widerspricht · Ein Monat im Durchlauf.
- **Diagramm 1, Ablauf pro Stelle**, als HTML/CSS (kein SVG-Bild, damit die
  Schrift auf dem Handy lesbar bleibt): Suche (geplant / auf Bitte) →
  Vorschläge → Entscheid (nein → `stellen.md` → Wiedervorlage) → Entwurf →
  Kontrolle → Versandweg (E-Mail / Portal / unklar) → `3_Zum-Versenden` →
  Rückmeldung → `2_Beworben` → Gespräch / Absage / Zusage. Die Kästen tragen
  Nummern und Farben der Status-Ordner. RAV- und Projekt-Teile gestrichelt.
- **Diagramm 2, der RAV-Monat**, als Zeitleiste: laufend bewerben und
  zurückmelden · ab 22. AvP · Monatsende Abschluss · bis 5. Nachweis.
- Seitenspezifischer CSS-Block nur für die Diagramme, mit den Farben aus
  `stil.css` (`--accent`, `--ok`, `--warn`, `--muted` usw.). `stil.css` kennt
  nur ein helles Design; die Diagramme brauchen darum keine Dunkel-Variante.
- Keine Klarnamen, Beispielfirma «Muster AG».

## Was sich an Dateien ändert

- `aufgaben/stelle/9_Claude/wissen.md` — neu geschrieben.
- `aufgaben/stelle/INFO.md` — `kurz:` auf den neuen Umfang.
- `grundgeruest/CLAUDE.md` — Sitzungsbeginn.
- `grundgeruest/START-HIER.txt` — Schritt 4.
- `anleitung/stelle.html` — neu geschrieben.
README und die übrigen Anleitungsseiten nennen «Was steht an?» als Satz, der
genügt, nicht als Pflicht. Sie bleiben unverändert.

`build.py` bleibt unverändert.

## Prüfen

- `python build.py` läuft; `dist/stelle.zip` enthält nur Grundgerüst plus
  `INFO.md`-Titel und `9_Claude/wissen.md`; `START-HIER.txt` mit BOM und CRLF.
- `wissen.md` gegenlesen auf Sätze, die eine Handlung vom Benutzer verlangen
  (gehören ins Gespräch), auf Klarnamen und auf Bezüge zu einem bestimmten
  Kanton ausser als Quellenbeleg.
- `stelle.html` neben einer Kopie von `stil.css` und `anleitung.js` im Browser
  prüfen, auch auf Handybreite (375 px).
- Ein Trockenlauf in Cowork ist nicht Teil dieser Umsetzung; er bleibt offen.

## Offen, bewusst nicht gelöst

- Ob geplante Cowork-Aufgaben mit lokalem Ordner verpasste Läufe nachholen.
- Die Zählweise für Vermittler in anderen Kantonen als SH.
- Die Job-Room-Such-API ist nicht dokumentiert; fällt sie weg, bleibt
  job-room.ch als Link.
- `anleitung/aufgaben.html` beschreibt die Karte «Stelle» noch mit «Auf Wunsch
  gleich Wohnungen in der Nähe». Wird in der Doku-Session nachgezogen, nicht
  hier.
