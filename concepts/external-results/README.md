# Externe Testergebnisse – drei Folienvorschläge

Drei vollständig überarbeitete, editierbare Alternativen zu den **letzten vier externen Prüfbereichen von Folie 34**: Collection/Timeout, Recovery, Zugriffsschutz und Receipt-Audit. Jede Kategorie zeigt jetzt den konkreten Testeingriff beziehungsweise die geladene Evidenz und die überprüfte Eigenschaft. Die Folien sind Englisch, passend zur Hauptpräsentation. **Variante B wurde ausgewählt und als Folie 35 in die Hauptpräsentation eingebaut.**

**Aktueller Nachweisstand:** Die kontrollierte Collection-Suite ist mit **3/3 Szenarien bestanden: Early, Partial und Zero** vollständig archiviert. Zusammen mit Recovery, Security **16/16** und Receipt-Audit **17/17** liegen für alle vier dargestellten Bereiche erfolgreiche Ausführungsnachweise vor. Die Aussage bleibt auf die ausgewählten Szenarien begrenzt.

[Hauptpräsentation](../../VITA-FL_Thesis_Presentation_TU_Berlin.pptx) · [Eingebaute Folie 35](../../preview/slide-35.png) · [Galerie](index.html) · [Übersicht](overview.png) · [Alle Varianten als PowerPoint](VITA-FL_External_Results_Alternatives.pptx) · [PDF-Vorschau](VITA-FL_External_Results_Alternatives.pdf)

| Variante | Gestaltung | Dateien |
| --- | --- | --- |
| **A – Vier Testfragen** | Vier gleichberechtigte Fragen mit konkreten Eingriffen und Antworten. Die Zähler bleiben nachgeordnet. | [PNG](a-result-cards.png) · [PPTX](a-result-cards.pptx) |
| **B – Konkreter Testkatalog** | Einzelne Eingriffe und die zugehörigen Assertions direkt nebeneinander. Die vier Contract-Guards sind einzeln benannt. **Empfehlung für die genaue Testabdeckung.** | [PNG](b-evidence-matrix.png) · [PPTX](b-evidence-matrix.pptx) |
| **C – Vier Prüfpfade** | Pro Kategorie ein eigener Weg: Eingriff oder Evidenz → ausgeführte Systemfunktion beziehungsweise Verifikation → Prüfergebnis. | [PNG](c-recovery-story.png) · [PPTX](c-recovery-story.pptx) |

Die bestehenden Dateinamen bleiben erhalten, damit bereits geteilte Links auf die überarbeiteten Entwürfe führen. Die Gestaltung liegt in `revised_layouts.py`; `build_designs.py` validiert weiterhin die kanonischen Ergebnisarchive vor dem Rendern.

**Auf der Folie ausdrücklich sichtbar:**

- Collection: 5, 2 oder 0 zugelassene Uploads bei Client-Limit 5 und 45 s Frist; früher Abschluss, Timeout-Abschluss oder keine leere Veröffentlichung.
- Recovery: Aggregator-CVM stoppen; bei Meldung 1/2 Zustand erhalten, bei 3/5 Abbruch und Neuwahl; fünf erfolgreiche Trainingsrunden danach.
- Zugriffsschutz: fehlende/falsche Zugangsdaten gegen UI, Control und Modell-/Job-/Inferenz-APIs; vier ungültige Contract-Aufrufe; unveränderte Konfiguration und erfolgreicher autorisierter Kontrolllauf.
- Receipt-Audit: veröffentlichte Evidenz aus dem Log erneut prüfen; SCITT-Signaturen und Inclusion, AIR-Modell-/Anfrage-/Ausgabe-Hashes, TDX-Quote/RTMR3/Image-Policy, Sello-Autorisierung und Tool-I/O sowie attestierte Empfänger-/Sitzungsbindungen.

RTMR3-Replay bezeichnet den Vergleich Event-Log ↔ jeweilige Quote. Es ist **kein** Vergleich mit dem Registrierungs-RTMR3 und **kein** Modelllade-Event in RTMR3. Der Modellbezug läuft über Manifest, REPORTDATA und AIR. Der Audit verwendet authentische veröffentlichte Nachweise; es wurde kein Receipt-Manipulationsszenario ergänzt. Die Konfigurationsprobe sendet die vorhandene Konfiguration ohne gültige Autorisierung und prüft Ablehnung sowie unveränderten Zustand.


## Ergebnisse und Aussagegrenzen

Recovery stammt vom **25.09.2026**, Security und der angezeigte Audit vom **29.09.2026**. Die neuen Collection-Szenarien sind separate Läufe vom **29.09.2026**. Sie verwenden dieselben sieben Container-Image-Pins; die spätere Provisionierungsänderung und neue SCITT-Logidentität sind unten dokumentiert. Die Läufe werden weder zu einem einzigen Durchlauf noch mit dem früheren 24-Runden-Modellversuch zusammengefasst.

| Prüfbereich | Beobachtetes Ergebnis | Aussagegrenze |
| --- | --- | --- |
| Collection / Timeout | **3/3 Szenarien bestanden:** Early mit 5/5 Beiträgen nach **16 s**; Partial mit 2/5 nach **45 s**; Zero ohne Veröffentlichung und mit **3/5-Quorum-Recovery**. | Je ein erfolgreicher Lauf der drei ausgewählten Szenarien, keine Wiederholungsstatistik. Zeiten aus archivierten PolicyOpened-/InputsClosed-Ereignissen, keine direkte Instrumentierung des lokalen Aggregator-Timers. |
| Aggregator-Recovery | Bei Meldung **1 und 2** blieb der Zustand erhalten; Meldung **3 von 5 Berechtigten** löste Abort und Neuwahl aus. Neuwahl nach **112,38 s**, erste Veröffentlichung nach **169,41 s**, jeweils ab bestätigtem VM-Stopp. **5 erfolgreiche Trainingsrunden**, Beteiligung aller **6 Worker über den Lauf**. | Ein erfolgreicher Recovery-Lauf, keine Wiederholungsstatistik. Bootstrap und abgebrochener Versuch zählen nicht zu den fünf erfolgreichen Trainingsrunden. |
| Zugriffsschutz / Vertragsprüfungen | **16/16 bestanden:** 10 unautorisierte Anfragen mit HTTP 401 abgewiesen; 4 erwartete Vertrags-Reverts; Konfiguration unverändert; autorisierter Inferenzablauf erfolgreich. | Ausgewählte Zugriffskontrollen in einem Lauf; Vertragsprüfungen ausschließlich als `eth_call`, keine gesendeten Angriffs-Transaktionen. Keine vollständige Threat-Abdeckung. |
| Veröffentlichte Nachweise | **17/17 bestanden**, Auditdauer **13,34 s**: 10 SCITT-, 1 AIR/TDX-, 3 Session- und 3 Sello-Prüfungen. | Angezeigt wird der Security-Audit. Erneute Ausführung vorhandener Verifier-Primitiven mit frischer Phala-Prüfung. Kein unabhängig implementierter Kryptografie-Verifier; kein Beweis globaler Logvollständigkeit. |

Die Farben kennzeichnen den Nachweisstatus: **Grün = beobachtet/bestanden**. Weiß/Grau gliedern Eingriffe, Systeme und Kategorien ohne weitere Sicherheitsbedeutung. Jede Variante enthält eine Legende. Grün bedeutet nur Erfolg innerhalb der ausgewiesenen Prüfgrenzen. Die DFL-/Agent-Marken oben behalten ihre fachliche Bedeutung.

## Kontrollierte Collection-Suite

Jeder Szenariolauf verwendet **6 Worker, 5 erfolgreiche Trainingsrunden, Client-Limit 5 und 45.000 ms Deadline**. Das Gate beeinflusst gezielt den ersten Trainingsversuch; danach wird es freigegeben. Beteiligung aller sechs Worker gilt über den jeweiligen Lauf, nicht zwingend in jedem kontrollierten Versuch. Bootstrap und abgebrochene Versuche zählen nicht als erfolgreiche Trainingsrunden.

| Szenario | Prüfziel | Archiviertes Ergebnis |
| --- | --- | --- |
| Early | Genau 5 erlaubte Beiträge; Abschluss vor der 45-s-Frist; exakt diese Worker als tatsächliche Contributors. | **143/143 Assertions PASS**; erste Runde 5/5 nach **16 s**; Beitragszahlen der fünf Runden **5, 5, 5, 5, 5**. |
| Partial | Genau 2 erlaubte Beiträge; drei übrige Clients nachweislich am Receiver blockiert; Abschluss nicht vor Fristende; exakt die erlaubten Contributors. | **144/144 Assertions PASS**; erste Runde 2/5 nach **45 s**; Beitragszahlen **2, 5, 5, 5, 5**. |
| Zero | Alle 5 Clients nachweislich blockiert; keine Inputs, kein Abschluss und keine Veröffentlichung bis mindestens 10 s nach Fristende; bei 1/2 Meldungen unveränderter Zustand, bei 3/5 Abort/Neuwahl; anschließende Fortsetzung. | **172/172 Assertions PASS**; Versuch 1 abgebrochen, fünf erfolgreiche Folgeversuche **2–6**, jeweils **5 Beiträge**. |

Mit `--collection-reports` akzeptiert der Generator genau drei kanonische SMEW-Berichte, jeweils einen für `early`, `partial` und `zero`, in beliebiger Reihenfolge. Alle drei sind abgeschlossen und ersetzen den früheren Collection-Stand „Partial evidence“ durch **grün: 3/3 Szenarien bestanden**. Der Generator prüft die Nachweise vor jeder Erzeugung erneut. Die überarbeiteten Entwürfe verlangen alle drei Collection-Archive sowie das Security-Archiv; ein fehlender Nachweis wird nicht durch einen angenommenen Erfolg ersetzt.

Für jeden Lauf müssen SMEW `succeeded`/Exit 0, SMA `ok`/Subprozess-Exit 0 und TD `PASS` mit leeren Fehlerlisten vorliegen. Der Generator prüft Gate-Inventar, Receiver-Blockierungen, tatsächliche Contributors, Fristverhalten, Zero-Nonpublication, Quorum, Rundenzahl und Beteiligung sowie die Image-Pins. Exportierte und gezippte Ergebnisse müssen übereinstimmen. Quellpfade und SHA-256-Werte werden in `evidence.json` ergänzt.

Zeiten stammen aus `PolicyOpened` und dem Blockzeitstempel von `InputsClosed`. Fehlt der Zeitstempel im Archiv, wird nur die bestandene Relation zur Frist angezeigt. **3/3** bezeichnet drei verschiedene kontrollierte Szenarien mit jeweils einem erfolgreichen Lauf, weder drei Assertions noch eine statistische Zuverlässigkeitsaussage. Frühere fehlgeschlagene oder abgebrochene Versuche bleiben dokumentiert.

## Was die 16 Security-Checks prüfen

| Umfang | Prüfung | Ergebnis |
| --- | --- | --- |
| 2 UI + 2 Control | Anfragen ohne bzw. mit falschen Zugangsdaten | HTTP 401 und passende Challenge bzw. Fehlerbegründung |
| 6 Inferenzzugriffe | Modellabruf, Jobabruf und Jobausführung ohne bzw. mit gefälschter Autorisierung | HTTP 401 mit passender Fehlerbegründung; TLS-Peer-Key an den verifizierten Positivlauf gebunden |
| 4 Contract-Guards | Veraltete Runde, falscher Aggregator, unregistrierter Action-Key, unberechtigte Policy-Änderung | Jeweils erwarteter Revert-Grund in `eth_call` |
| 1 Konfigurationsinvariante | Workerzahl, Client-Limit, Runden, Epoche und Frist nach den unautorisierten Control-Anfragen | Unverändert |
| 1 Positivkontrolle | Regulärer Ablauf der drei Agent-Werkzeuge mit attestierter Inferenz und veröffentlichten Nachweisen | Erfolgreich; keine Aussage über die Vorhersagegenauigkeit des Modells |

**10 + 4 + 1 + 1 = 16.** Die Konfigurationsinvariante ist keine weitere HTTP-Ablehnung. Die 17 Audit-Assertions sind keine 17 unabhängigen Experimente. Der frühere Recovery-Audit bestand separat 17 Checks in 13,58 s; beide Audits werden nicht zu 34 Checks zusammengezählt.

## Startfehler und Änderungen zwischen den Läufen

Bei den neuen Collection-Starts trat **Phala HTTP 429** während der Worker-Provisionierung auf; die Control-API meldete dafür HTTP 500. Ein Early-Start scheiterte mit HTTP 409. Diese Versuche sind als `ERROR` archiviert und gelten nicht als bestandene Collection-Prüfungen:

- Partial: `SMEW/reports/vita-fl-partial-5r-20260929-a2fb2bbf/2026_09_29_14_26_19_6fba5816/`.
- Early: `SMEW/reports/vita-fl-early-5r-20260929-a2fb2bbf/2026_09_29_14_33_19_245ab035/` und `2026_09_29_14_40_08_624be60f/`.

Danach wurde ausschließlich die Terraform-Provisionierungsparallelität der Control-API durch **`TF_CLI_ARGS_apply=-parallelism=2`** geändert. Das vorhandene Runtime-App-Deployment wurde in-place aktualisiert; App-ID, sieben Image-Pins, OS und verschlüsselte Umgebung blieben erhalten. **Gleiche Images bedeuten hier keine vollständig identische Laufzeitkonfiguration:** Der Security-Lauf war vor dieser Änderung. Der geprüfte und angewandte Plan liegt in `vita-fl-td/generated/collection-check-20260929/parallelism-plan.json`. Alter/neuer Compose-Hash, Änderung und Plan-Hash werden in `evidence.json` und den Sprechernotizen erhalten.

Beim Runtime-Neustart änderte sich außerdem der **SCITT-Schlüsselsatz des Transparency Logs**. Für Collection wurde `vita-fl-td/generated/collection-check-20260929/audit-policy-p2.json` über die authentifizierte Deployment-UI neu gebunden. `restart-verification.json` dokumentiert alten/neuen Keyset-Hash und Policy-Hash. Die ursprüngliche Security-Policy bleibt erhalten; Plattform-Allowlist und Sello-Identität wurden nicht geändert. Der Generator prüft diese Bindungen sowie – bei mitgeliefertem Security-Archiv – die beiden Policies gegeneinander. Die neue Log-Identität wird nicht rückwirkend in den früheren Audit eingesetzt.

Auch der frühere Recovery-Versuch und der separate Partial-Lauf vom 25.09. endeten nach Abbruch mit `ERROR`. Erfolgreiche spätere Szenarioläufe rechtfertigen deshalb **keine kampagnenweite 100-%-Erfolgsquote**. Der Generator erhält frühere kanonische `ERROR`-Versuche aus den ausgewählten Collection-Kampagnen mit Quellen-Hashes.

## Quellen und Reproduzierbarkeit

Die generierten Zahlen, Ereigniszeiten, Quellpfade, Deployment-/Testtreiber-Unterschiede und SHA-256-Fingerabdrücke stehen in [evidence.json](evidence.json). Der vollständige Suite-Build ergänzt die drei Collection-Archive einschließlich früherer `ERROR`-Versuche und geänderter Provisionierungs-/Logidentität. Quellen und Grenzen stehen ebenfalls in den Sprechernotizen.

- Recovery: `SMEW/reports/vita-fl-recovery-5r-61b96e51/2026_09_25_17_22_19_749db20e/`.
- Security und angezeigter Audit: `SMEW/reports/vita-fl-security-5r-20260929-a2fb2bbf/2026_09_29_13_35_26_f18d168d/`.
- Early: `SMEW/reports/vita-fl-early-5r-20260929-a2fb2bbf/2026_09_29_15_02_42_ca2cea1a/`.
- Partial: `SMEW/reports/vita-fl-partial-5r-20260929-a2fb2bbf/2026_09_29_15_16_23_dbffef0e/`.
- Zero: `SMEW/reports/vita-fl-zero-5r-20260929-a2fb2bbf/2026_09_29_15_30_36_da447d90/`.
- Rohdaten: jeweils `subprocess_output/result.json` und `subprocess_output/run-artifacts.zip`, insbesondere `chain-events.json`, `observations.jsonl`, `security.json` bzw. `transparency-audit.json`.
- Früherer Partial-Abbruch: `SMEW/reports/vita-fl-partial-5r-61b96e51/2026_09_25_17_35_46_15585dd8/subprocess_output/result.json`.
- Früherer Recovery-Abbruch: `SMEW/reports/vita-fl-recovery-5r-98664d28/2026_09_25_16_34_03_e48f9a7c/subprocess_output/result.json`.
- Security-Inventar: `vita-fl-td/src/vita_fl_td/security_bridge.py`.
- [Ausführlicher Security-Ergebnisbericht](../../../vita-fl-td/generated/security-check-20260929/results/README.md).

Den aktuellen vollständigen Stand aus den drei kanonischen Archiven erzeugen. Jeder Bericht enthält `smew.json`, `run.json` und `subprocess_output/`; Scratch-Verzeichnisse werden abgelehnt:

```bash
.venv/bin/python concepts/external-results/build_designs.py \
  --security-report ../SMEW/reports/vita-fl-security-5r-20260929-a2fb2bbf/2026_09_29_13_35_26_f18d168d \
  --collection-reports \
    ../SMEW/reports/vita-fl-early-5r-20260929-a2fb2bbf/2026_09_29_15_02_42_ca2cea1a \
    ../SMEW/reports/vita-fl-partial-5r-20260929-a2fb2bbf/2026_09_29_15_16_23_dbffef0e \
    ../SMEW/reports/vita-fl-zero-5r-20260929-a2fb2bbf/2026_09_29_15_30_36_da447d90
```

Der Generator startet keinen Cloud-Lauf. Der aktuelle Generator verlangt `--security-report` und genau drei `--collection-reports`. Layout, Objektgrenzen und erneutes Öffnen aller PowerPoint-Dateien werden geprüft. PowerPoint-Elemente bleiben editierbar. PNG/PDF verwenden den bestehenden Pillow-Renderer; Schriftumbrüche in PowerPoint können leicht abweichen. Hash-Prüfungen sichern Hauptpräsentation und Chapter 4.
