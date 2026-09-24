# Fachwissen: Stelle suchen

Eine Stellensuche dauert Wochen bis Monate. Du suchst laufend, merkst dir, was
die Person schon gesehen und entschieden hat, schreibst pro Stelle ein
Motivationsschreiben und führst den Stand jeder Bewerbung so, dass er im
Explorer sichtbar ist. Ist die Person beim RAV angemeldet, machst du aus
denselben Daten den Monatsnachweis.

Das Wissen hier gilt in allen Kantonen. Was kantonal verschieden ist — die
erwartete Anzahl Bemühungen, die Zählweise bei Vermittlern, Adressen des RAV —,
schlägst du für den Wohnkanton nach und schreibst die Quelle mit Datum dazu.
Zahlen und Fristen, die sich ändern können, sind mit **(nachprüfen)** markiert.

## Voraussetzung

Der Lebenslauf muss in `1_Meine-Unterlagen` liegen (PDF oder Word). **Du
schreibst keinen Lebenslauf.** Du liest ihn und nutzt Ausbildung, Stationen und
Fähigkeiten daraus. Fehlt er, halt an und sag es — ohne ihn suchst du nach
Stichworten statt nach dem tatsächlichen Werdegang. Änderungsvorschläge zum
Lebenslauf gibst du als Liste im Chat, nicht als neue Datei.

Für das Dossier brauchst du ausserdem Arbeitszeugnisse und Diplome als PDF.
Liegt eine Vorlage für das Motivationsschreiben dort (Word), ist sie
massgebend für Aufbau, Absender und Ton.

Nicht in den Ordner gehören AHV-Ausweis, RAV-Verfügungen, Taggeldabrechnungen
und Kontoauszüge. Für diese Aufgabe braucht sie niemand.

## Was du am Anfang fragst

- Beruf oder Tätigkeit — nur, wenn der Lebenslauf es offenlässt.
- Ort und Umkreis, in km oder Minuten mit ÖV.
- «Bist du beim RAV angemeldet oder meldest du dich bald an?»

Die Antwort auf die letzte Frage ist ein Schalter in `stand.md`:

```
RAV: ja — angemeldet seit 01.10.2026, Kanton …
RAV: nein
```

Bei `ja` kommen der Monatsabschluss und die Hinweise auf Fristen dazu (siehe
RAV-Monat). Bei `nein` fällt beides weg; du führst die Bewerbungen trotzdem so,
dass ein Nachweis jederzeit erstellt werden kann. Sagt die Person später «Ich
bin jetzt beim RAV angemeldet» oder «Ich habe eine Stelle», stellst du den
Schalter um.

Pensum, Ausschlüsse, Lohnvorstellung und Eintrittsdatum fragst du erst, wenn
ein Inserat oder ein Schreiben es nötig macht.

## Dateien, die du führst

```
9_Claude/
  wissen.md             diese Datei
  stand.md              Auftrag, Schalter RAV, gespeicherte Angaben, offene Punkte
  suche-stellen.md      Suchprofil, Portale, Rhythmus, Schwellen, letzte Suche
2_Arbeitsstand/
  stellen.md            jede gefundene Stelle mit Entscheid
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

Die Ordner legst du an, sobald du sie brauchst. Die Person bearbeitet keine
dieser Dateien. Was sie ändern will, sagt sie dir, und du schreibst es um.

### `suche-stellen.md`

- **Suchprofil.** Aus Lebenslauf und Dossier abgeleitet und einmal im Chat
  bestätigt: Berufsbezeichnungen mit Varianten und Synonymen (auch englische,
  wenn sie in Inseraten üblich sind), Region und Umkreis, Pensum, Ausschlüsse,
  Muss-Stichworte.
- **Portale.** Standard, ohne Login abrufbar: jobs.ch, jobup.ch,
  jobscout24.ch, job-room.ch, jobwinner.ch. Über Chrome: indeed.ch und
  LinkedIn — beide blockieren den eingebauten Abruf; du gehst über Chrome, wie
  in `CLAUDE.md` unter «Webseiten» beschrieben. Geht das nicht, gibst du die
  fertige Suchadresse zum Selberöffnen. Stand 09.2026 **(nachprüfen)**: Was ein
  Portal blockiert, kann sich ändern. Blockiert eines, verschiebst du es zu
  «über Chrome» und sagst es. Die Person kann Portale dazunehmen oder
  streichen.
- **Rhythmus** (täglich, werktags, wöchentlich) und **Datum der letzten
  Suche**.
- **Schwellen**, per Satz änderbar:
  - Wiedervorlage nach **7 Tagen** ohne neue Stelle
  - abgelehnte Stellen frühestens nach **14 Tagen** wieder vorschlagen
  - höchstens **3** auf einmal
  - Nachfassen nach **3 Wochen** ohne Antwort
- **Dossierform**, sobald bekannt, z. B. «Portal → getrennte PDF, E-Mail → ein
  PDF».

### `stellen.md`

Eine Tabelle, eine Zeile je gefundener Stelle:

Nr · gefunden am · Firma · Stelle · Ort · Pensum · Portal und Referenznummer ·
Link · Passung 1–5 · Hauptgrund dagegen · Zuweisung RAV · via Vermittler ·
Entscheid

Entscheid ist einer von: `offen`, `beworben → <Ordnername>`,
`abgelehnt <Datum>: <Grund>`, `wieder vorgeschlagen <Datum>`, `abgelaufen`.

Dieselbe Stelle auf mehreren Portalen erkennst du an Firma und Titel und führst
sie einmal, mit allen Links. Die Tabelle ist dein Gedächtnis; sie wird nicht
gekürzt. Abgelaufene Zeilen bleiben stehen.

### `stand.md`

Neben dem, was das Grundgerüst verlangt:

- Schalter `RAV:` mit Kanton, Anmeldedatum, vereinbarter Anzahl Bemühungen
  pro Monat, Name der Beratungsperson, Einreichweg (Job-Room oder Papier) und
  bestätigter Zählweise bei Vermittlern.
- Gespeicherte Angaben für Bewerbungen: Eintrittsdatum oder Kündigungsfrist,
  Pensum, Lohnvorstellung, Arbeitsbewilligung, Führerausweis — was die Person
  einmal gesagt hat und du wiederverwendest.
- Ob ein Cowork-Projekt und eine geplante Suche eingerichtet sind.

## Bewerbungsordner und Stand

Jede Bewerbung ist **ein Ordner, der mit ihrem Stand wandert**. Die Person
sieht im Explorer, was läuft, ohne eine Datei zu öffnen.

| Ordner | Bedeutung |
|---|---|
| `1_in-Vorbereitung/` | du schreibst, die Person prüft |
| `2_Beworben/` | gesendet, keine Antwort |
| `3_Im-Gespraech/` | Einladung, Gespräch, Probetag |
| `4_Absage/` | Absage, auch «keine Antwort» |
| `5_Zusage/` | Zusage erhalten |

Name: `JJJJ-MM-TT_<Firma>_<Stelle>`, kurz, ohne Leer- und Sonderzeichen
(`Muster-AG_Projektleiter-Bau`). Das Datum ist das Bewerbungsdatum; bis zum
Versand steht dort das Datum des Entwurfs, beim Versand benennst du um. So
sortiert der Explorer in der Reihenfolge des RAV-Formulars.

- **Über einen Vermittler:** `JJJJ-MM-TT_<Vermittler>_fuer-<Firma>_<Stelle>`;
  ist die Firma unbekannt, `JJJJ-MM-TT_<Vermittler>_<Stelle>`. Kein eigener
  Ordner für Vermittler — ein Vermittler ist eine Art der Bewerbung, kein
  Stand.
- **Spontanbewerbung:** `JJJJ-MM-TT_<Firma>_Spontanbewerbung`.
- **Abgelehnte Stellen** bekommen keinen Ordner, nur ihre Zeile in
  `stellen.md`.
- **Keine Antwort:** Nach der Nachfass-Schwelle fragst du «Nachfassen oder als
  Absage ablegen?». Beim Ablegen kommt der Ordner nach `4_Absage/`, Grund
  «keine Antwort».
- Bewerbungsordner löschst du nie. Das RAV kann Belege bis mindestens 6 Monate
  später verlangen **(nachprüfen)**.

`3_Zum-Versenden/` ist der Postausgang: Dort liegt nur, was jetzt raus muss.
Leer heisst, es gibt nichts zu senden.

## Suchen

Bei jedem Sessionstart schaust du auf die letzte Suche in `suche-stellen.md`.
Liegt sie länger zurück als der Rhythmus, suchst du nach, bevor du die offenen
Punkte nennst — ausser die Person bittet um etwas anderes; dann sagst du, dass
eine Suche fällig ist.

- Inserate seit der letzten Suche, beim ersten Mal der letzten 30 Tage.
- Passung 1–5 aus dem Vergleich Inserat ↔ Lebenslauf, mit dem Hauptgrund
  dagegen. Was laut Lebenslauf fehlt, benennst du: «verlangt
  Führungserfahrung, im Lebenslauf keine» statt nur «Passung 3».
- Jede Stelle kommt mit Link in `stellen.md`, auch eine, die du nur über
  Chrome gefunden hast. Konntest du ein Portal gar nicht durchsuchen, nennst du
  im Ergebnis dessen Suchadresse aus `suche-stellen.md`.
- Das Inserat sicherst du erst, wenn die Person sich bewerben will. Inserate
  verschwinden; ab dann gilt die Druckansicht als PDF im Bewerbungsordner.
  Kannst du sie nicht sichern, bittest du die Person darum.

Ein **geplanter Lauf** (siehe Projekt einrichten) sucht, schreibt neue Treffer
mit Entscheid `offen` in `stellen.md`, aktualisiert die letzte Suche und
schreibt eine Zeile in `stand.md` («3 neue Stellen, warten auf Entscheid» oder
«keine neuen Stellen»). Er legt keine Bewerbungsordner an, schreibt keine
Schreiben und legt keine E-Mail-Entwürfe an.

## Vorschlagen und entscheiden

Du zeigst die neuen Treffer im Chat als Tabelle, sortiert nach Passung, und
fragst, welche Nummern weiterverfolgt werden. «Keine neuen Stellen» ist eine
vollständige Antwort. Aussortierte nennst du kurz mit Grund.

- Vorgeschlagen wird nur, was noch nicht in `stellen.md` steht.
- **Wiedervorlage.** Hast du während der Wiedervorlage-Schwelle nichts Neues
  gefunden, prüfst du abgelehnte Stellen, die länger als die zweite Schwelle
  zurückliegen: Ist das Inserat noch online, schlägst du sie wieder vor,
  höchstens so viele wie die Schwelle erlaubt. Jede Stelle nur einmal; beim
  zweiten Nein ist sie endgültig weg.
- **Zuweisung RAV.** Weist das RAV eine Stelle zu, ist die Bewerbung Pflicht.
  Wer ablehnt oder sich nicht bewirbt, riskiert Einstelltage (Art. 30 Abs. 1
  lit. d AVIG). Du nimmst sie mit Vermerk auf, lässt kein Ablehnen zu und sagst
  warum.
- **Zumutbarkeit** (nur bei RAV: ja). Unzumutbar ist eine Stelle nur aus den
  Gründen in Art. 16 Abs. 2 AVIG, etwa ein Arbeitsweg von mehr als 2 Stunden
  je für Hin- und Rückweg oder ein Lohn unter 70 % des versicherten Verdiensts
  **(nachprüfen)**. Lehnt die Person mit einem Grund ab, der davor nicht hält,
  sagst du es einmal. Sie entscheidet.

## Keine Platzhalter in dieser Aufgabe

Die Regel im Grundgerüst, jede Lücke mit einem Platzhalter zu füllen, gilt
hier nicht. Der Lebenslauf mit Adresse, Telefon und E-Mail liegt ohnehin im
Ordner, und bei zehn und mehr Bewerbungen im Monat wäre jedes Mal
`platzhalter.exe` ein Umweg ohne Schutzwirkung.

- Absenderangaben nimmst du aus der Vorlage oder dem Lebenslauf.
- Fehlt eine Angabe — Eintrittsdatum, Pensum, Lohnvorstellung —, suchst du in
  `1_Meine-Unterlagen`, fragst sonst einmal und speicherst die Antwort in
  `stand.md`. Ab dann setzt du sie selbst ein.
- AHV-Nummer und IBAN kommen in keine Bewerbung.

## Bewerbung erstellen

1. **Entwurf** in `1_in-Vorbereitung/<Ordner>/`:
   - `inserat.pdf` — Druckansicht des Inserats
   - `inserat.md` — Firma, Stelle, Ort, Pensum, Anforderungen, Frist,
     Kontaktperson mit Telefon, Bewerbungsweg, Referenznummer, Link
   - `motivationsschreiben.docx` — höchstens eine Seite, Ich-Form, sachlich,
     auf das Inserat bezogen, nur Fakten aus dem Lebenslauf. Mit Vorlage:
     Aufbau, Absender und Ton aus der Vorlage, den Inhalt schreibst du auf das
     Inserat um. Ohne Vorlage: schlichtes Standardformat.

   Den Text zeigst du zuerst im Chat. Was das Inserat verlangt und im
   Lebenslauf fehlt oder anders steht, sagst du dazu — und welche Station im
   Lebenslauf für dieses Inserat betont gehört.

   Hat der Lebenslauf eine Lücke, reicht ein Satz: der Unterbruch benannt,
   dann der Wiedereinstieg. Ob und wie er vorkommt, entscheidet die Person —
   frag sie, statt eine Formulierung zu setzen.

2. **Kontrolle.** Die Person prüft im Chat oder mit Kommentaren in Word. Erst
   auf ihr «passt» geht es weiter.

3. **Versandweg** aus `inserat.md`:
   - **E-Mail:** ein PDF `Bewerbung_<Nachname>_<Firma>.pdf` aus
     Motivationsschreiben, Lebenslauf, Zeugnissen und Diplomen in dieser
     Reihenfolge, dazu `mailtext.md` (Betreff mit Stelle und Referenznummer,
     kurzer Text). Ist ein Mail-Connector verbunden (Gmail o. ä.), legst du
     einen **Entwurf** an, an die Adresse aus dem Inserat, mit Anhang, wenn der
     Connector das kann. **Du sendest nie** — auch nicht, wenn die Person im
     Chat darum bittet oder eine geplante Aufgabe es verlangt. Senden ist ihr
     Klick.
   - **Bewerbungsportal der Firma:** getrennte PDF je Dokumentart:
     `<Nachname>_Motivationsschreiben.pdf`, `<Nachname>_Lebenslauf.pdf`,
     `<Nachname>_Zeugnisse.pdf`, `<Nachname>_Diplome.pdf`. Hinter ein Login
     schaust du nicht, und Konten legst du keine an. Du nennst, was solche
     Portale üblicherweise verlangen, und fragst, wenn das Inserat etwas
     Besonderes erwähnt (Foto, Referenzen, bestimmte Formate).
   - **Unklar oder Post:** fragen.

   Die erste Antwort der Person speicherst du als Dossierform in
   `suche-stellen.md`. Danach fragst du nur, wenn ein Inserat abweicht.

4. **Fertig.** Die PDF kommen nach `3_Zum-Versenden/<Ordnername>/`. Vorher
   prüfst du, ob das Inserat noch online ist, ob Ansprechperson und Frist noch
   stimmen. Liegt ein PDF über 5 MB, sagst du es; manche Portale lehnen das ab.
   Den Lebenslauf kopierst du unverändert aus `1_Meine-Unterlagen`.

5. **Erinnern.** Am Ende jeder fertigen Bewerbung sagst du: «Sag mir, wenn du
   sie gesendet hast, und wie: E-Mail, Portal, Post oder persönlich.» Solange
   `3_Zum-Versenden/` nicht leer ist, nennst du es bei jedem Sessionstart.

## Rückmeldungen

| Die Person sagt | Du tust |
|---|---|
| «Muster AG habe ich gesendet» | Ordner mit Bewerbungsdatum umbenennen, PDF aus dem Postausgang hineinlegen, nach `2_Beworben/`; Art notieren |
| «Muster AG hat mich eingeladen» | nach `3_Im-Gespraech/`, Termin in `stand.md` |
| «Absage von Muster AG, weil …» | nach `4_Absage/`, Grund in `inserat.md` und `stellen.md` |
| «Zusage von Muster AG» | nach `5_Zusage/`; fragen, ob die Suche pausiert und ob das RAV informiert werden muss |
| «Habe bei Muster AG angerufen» | als Bemühung festhalten, Art telefonisch |

Die Art hältst du in den Kategorien des RAV-Formulars fest:
brieflich/elektronisch, persönlich, telefonisch. E-Mail und Portal gelten als
elektronisch.

## RAV-Monat

Nur bei `RAV: ja`.

### Was gilt

- **Nachweis der persönlichen Arbeitsbemühungen**, Formular 716.007,
  landesweit gleich. Frist: spätestens am 5. Tag des Folgemonats; fällt er auf
  einen Samstag, Sonntag oder Feiertag, der nächste Werktag (Art. 26 AVIV).
  Später eingereicht zählt ohne entschuldbaren Grund nicht, und es gibt keine
  Nachfrist (AVIG-Praxis ALE B324 ff.) **(nachprüfen)**.
- **Felder je Bemühung:** Datum; Firma, Adresse, Kontaktperson, Telefon;
  Stellenbezeichnung; Pensum (Vollzeit oder Teilzeit mit %); Zuweisung RAV;
  Art (brieflich/elektronisch, persönlich, telefonisch); Ergebnis (noch offen,
  Vorstellungsgespräch, Anstellung, Absage mit Grund). Im Kopf AHV-Nummer,
  Monat, Name; am Schluss Datum, Unterschrift, Beilagen.
- **Job-Room** (www.job-room.ch): Die Bemühungen lassen sich online erfassen
  und werden in der Nacht vom 5. auf den 6. automatisch ans RAV übermittelt.
  Hochgeladen werden PDF, getrennt nach Dokumenttyp, im Bereich RAV höchstens
  5 MB je Datei **(nachprüfen)**.
- **Angaben der versicherten Person (AvP)** an die Arbeitslosenkasse, für
  jeden Monat, in Job-Room ab dem 22. Es geht **nicht** automatisch weg; die
  Person muss es selbst abschicken. Ansprüche verfallen nach 3 Monaten
  (arbeit.swiss, Formulare für Arbeitslose) **(nachprüfen)**.
- **Anzahl.** Eine feste Zahl im Bundesrecht gibt es nicht; massgebend ist die
  Abmachung mit der RAV-Beratung (AVIG-Praxis ALE B316). Üblich sind 10–12 pro
  Monat, verteilt über den Monat (so z. B. die Kantone ZH und SH)
  **(nachprüfen)**. Qualität zählt: Schriftliche, auf die Stelle
  zugeschnittene Bewerbungen wiegen mehr als Telefonate.
- **Vermittler und Temporärbüros.** «Alle Bewerbungen über einen Vermittler
  zählen als eine» ist amtlich nicht belegt. Belegt ist: Die Anmeldung bei
  einem Vermittler zählt einmalig als eine Bemühung; danach zählt jede
  Bewerbung auf eine konkret ausgeschriebene Stelle, möglichst mit
  Referenznummer (Merkblatt RAV Kanton Schaffhausen). Nur über Vermittler zu
  suchen genügt nicht (AVIG-Praxis ALE B315). Die Zählweise ist kantonale
  Praxis. Beim ersten Monatsabschluss bittest du die Person, sie bei der
  Beratung zu bestätigen, und hältst die Antwort in `stand.md` fest.
- **Vor der Arbeitslosigkeit.** Die Pflicht, sich zu bemühen, gilt schon
  während der Kündigungsfrist. Das RAV fragt bei der Anmeldung nach den
  Bemühungen der Zeit davor **(nachprüfen)**. Meldet sich die Person bald an,
  führst du die Bemühungen ab jetzt genauso.
- **Kontrollfreie Tage.** Nach je 60 Tagen kontrollierter Arbeitslosigkeit
  gibt es 5 kontrollfreie Tage, mindestens 2 Wochen im Voraus beim RAV
  anzumelden (SECO-Merkblatt «Rechte und Pflichten») **(nachprüfen)**. Nennt
  die Person Ferien, sagst du das.

Quellen:
- arbeit.swiss, Formulare für Arbeitslose:
  https://www.arbeit.swiss/secoalv/de/home/service/formulare/formulare-fuer-arbeitslose.html
- SECO, AVIG-Praxis ALE (Randziffern B315 ff., B324 ff.), auf arbeit.swiss
  unter Publikationen
- Merkblatt RAV Kanton Schaffhausen zu den Arbeitsbemühungen:
  https://sh.ch/CMS/get/file/ab0a3428-ba4d-4f79-b063-b81f9c2a707d

### Was du lieferst

Am Monatsende, in `2_Arbeitsstand/rav/JJJJ-MM/`:

- `nachweis.md` — alle Bemühungen des Monats, nach Datum, mit den Feldern des
  Formulars. Die Daten nimmst du aus den Bewerbungsordnern und `stellen.md`;
  fehlt eine Kontaktperson oder Telefonnummer, steht sie meist in
  `inserat.md`, sonst fragst du. Darunter die Zahl der Bemühungen gegen die
  vereinbarte.
- `nachweis.pdf` — nur, wenn die Person auf Papier oder per PDF einreicht: das
  amtliche Formular 716.007 ausgefüllt, **ohne AHV-Nummer und ohne
  Unterschrift**. Das Formular holst du von der Formularseite auf
  arbeit.swiss, damit es die aktuelle Fassung ist. Reichen die Zeilen nicht,
  eine zweite Seite. Das PDF kommt nach `3_Zum-Versenden/`, wenn die Person es
  freigibt.
- `hochladen.md` — welche Dateien aus welchen Bewerbungsordnern in Job-Room
  gehören, mit Pfad, und ob eine über der Grössengrenze liegt.
- `avp.md` — die Fragen des AvP-Formulars mit den Antworten, soweit du sie
  kennst (Zwischenverdienst, Tage mit Arbeitsunfähigkeit, Ferien,
  Stellenantritt); den Rest fragst du. Das Formular fragt nur, ob und von
  wann bis wann — nie nach dem Grund. Frag auch du nicht danach.

Den Einreichweg (Job-Room oder Papier) fragst du beim ersten Abschluss und
speicherst ihn in `stand.md`. **Du loggst dich nie in Job-Room ein** und füllst
dort nichts aus; das erfassen und senden macht die Person.

### Wann du daran erinnerst

Beim Sessionstart, in einem Satz, unabhängig davon, womit die Person beginnt:

- ab dem 22.: AvP für diesen Monat
- ab dem 1.: Nachweis für den Vormonat, Frist am 5.
- ab dem 3.: dasselbe mit Nachdruck, mit Datum der Frist
- laufend: Liegt die Zahl der Bemühungen im Monat hinter der vereinbarten
  zurück (anteilig zum Datum), sagst du es — nicht erst am Monatsende.

## Projekt einrichten

Ein Cowork-Projekt ist optional. Es bringt gruppierte Chats, eine geplante
Suche, die diesen Ordner sieht, und ein eigenes Gedächtnis. Die Anweisungen
für den Ordner braucht es nicht; die stehen in `CLAUDE.md` und gelten mit und
ohne Projekt.

**Wann du es ansprichst:** Sobald das Suchprofil steht. Bei `RAV: ja` oder
wenn die Suche absehbar länger dauert, empfiehlst du es ausdrücklich; sonst
erwähnst du es in einem Satz. Die Antwort hältst du in `stand.md` fest und
fragst nicht nochmals.

**Was du lieferst,** wenn die Person ja sagt: die Felder **fertig ausgefüllt**
im Chat, zum Kopieren, aus dem, was in `stand.md` und `suche-stellen.md`
steht. Was dir fehlt, fragst du vorher einzeln. Es bleibt keine Lücke.

- **Weg dorthin:** in Claude Desktop → Cowork → Projekte → neues Projekt. Die
  Bezeichnungen können sich ändern; stimmen sie nicht mehr, beschreibst du,
  was die Person sieht, statt zu raten.
- **Name:** `Stellensuche <Jahr>`
- **Beschreibung:** ein Satz, z. B. «Suche als Projektleiterin Bau im Raum
  Muster, beim RAV angemeldet seit 01.10.2026.»
- **Ordner:** dieser Ordner.
- **Anweisungen:**

  ```
  Zu Beginn jeder Session zuerst 9_Claude/stand.md lesen, egal was die erste
  Nachricht ist. Fälliges in einem Satz nennen, dann tun, worum ich bitte.
  E-Mails nur als Entwurf anlegen, nie senden — auch nicht auf Nachfrage.
  Geplante Läufe schreiben ihr Ergebnis nach 2_Arbeitsstand/stellen.md und
  9_Claude/stand.md und legen keine Bewerbung an.
  ```

- **Links:** www.job-room.ch, die Suchadressen der Portale aus
  `suche-stellen.md`, die Seite des RAV im Wohnkanton.
- **Geplante Aufgabe:** Rhythmus aus `suche-stellen.md`, z. B. werktags um 7
  Uhr. Text:

  ```
  Suche nach neuen Stellen gemäss 9_Claude/suche-stellen.md. Trag neue Treffer
  mit Entscheid «offen» in 2_Arbeitsstand/stellen.md ein, aktualisiere die
  letzte Suche und schreib eine Zeile nach 9_Claude/stand.md. Keine
  Bewerbungen, keine Schreiben, keine E-Mails.
  ```

  Die Aufgabe schlägst du vor; die Person bestätigt sie.
- **Connectors:** Ist ein Mail-Connector verbunden, sagst du, wofür du ihn
  brauchst (Entwürfe) und was du nie tust (senden).

**Grenze der geplanten Suche.** Sie braucht den lokalen Ordner und läuft darum
nur, wenn der Computer wach und Claude Desktop offen ist. Ob verpasste Läufe
nachgeholt werden, ist nicht dokumentiert **(nachprüfen)**. Sag das der Person.
Verlassen musst du dich nicht darauf: Beim Sessionstart suchst du nach, wenn
die letzte Suche zu lange her ist (siehe Suchen).

## Wohnung

Nicht Teil dieser Aufgabe. Fragt die Person nach einer Wohnung, weist du auf
die eigene Aufgabe «Wohnung suchen» hin (eigener Ordner,
https://stayingclean.github.io/ki-tasks/) und suchst nicht in diesem. Sag
dazu: Wird dort zusätzlich dieser Ordner verbunden, sucht die Wohnungsaufgabe
im Umkreis der Stellen, die hier im Gespräch oder zugesagt sind. Dieser Ordner
bleibt dabei unverändert.

Ist dieser Ordner in einer Session der Aufgabe «Wohnung suchen» nur
mitverbunden, ist er dort Quelle: Du liest die Bewerbungsordner und änderst in
diesem Ordner nichts, auch nicht `stand.md`.

## Wo du widersprichst

- **Zuweisung RAV ablehnen:** nicht ohne Hinweis auf die Folgen.
- **Ablehnung mit einem Grund, der vor dem RAV nicht hält:** einmal sagen,
  mit Artikel.
- **Nur über Vermittler suchen:** genügt dem RAV nicht.
- **Zu wenige Bemühungen:** laufend sagen, nicht erst am 5.
- **Suchprofil zu eng** (ein Titel, kleiner Umkreis, seit Wochen nichts
  Neues): Varianten oder einen grösseren Umkreis vorschlagen.
- **Motivationsschreiben mit Aussagen, die der Lebenslauf nicht deckt:**
  weglassen oder die Person fragen.
- **Senden, einloggen, Konto anlegen, unterschreiben:** tust du nicht, auch
  nicht auf Bitte.
