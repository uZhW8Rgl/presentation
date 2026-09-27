# CI-Tests und externe Tests – Variante A ausgewählt

**Variante A – Zwei Prüfkataloge** ist für **Seite 26** der Hauptpräsentation ausgewählt und ersetzt die bisherige Kategorienfolie. **CI-Tests** fassen Unit-, Component- und Integrationstests zusammen; **externe Tests** steuern und prüfen das deployte VITA-FL. Beide Bereiche sind nach ihrem Prüfgegenstand unterteilt. Das freigegebene native Asset ist `../../../assets/test-evaluation-a.pptx`; `../a-test-categories.png` zeigt die ausgewählte Fassung. Die Hauptpräsentation bleibt bei **46 Folien**.

[Galerie](index.html) · [Gesamtübersicht](overview.png) · [Alle Varianten als PowerPoint](VITA-FL_CI_External_Test_Alternatives.pptx) · [PDF-Vorschau](VITA-FL_CI_External_Test_Alternatives.pdf)

| Entwurf | Darstellung | Stärke | Dateien |
| --- | --- | --- | --- |
| **A – Zwei Prüfkataloge** | Links sieben CI-Bereiche mit Anzahl und Beispielen; rechts externe Szenariogruppen mit Assertions. | **Ausgewählt für Seite 26 der Hauptpräsentation.** | [PNG](a-two-catalogs.png) · [PPTX](a-two-catalogs.pptx) |
| **B – Gemeinsame Vergleichsmatrix** | Je Prüfgegenstand stehen CI-Checks und verwandte externe Prüfungen nebeneinander. | Erklärt, welche Grenzen die beiden Ansätze prüfen und wo kein externes Szenario existiert. | [PNG](b-boundary-matrix.png) · [PPTX](b-boundary-matrix.pptx) |
| **C – Konkrete Testbedingungen** | CI-Zusammenfassung links; alle acht externen Modi mit Bedingung und erwartetem Verhalten rechts. | Besonders geeignet, um den konkreten Testplan zu erklären. | [PNG](c-scenario-configuration.png) · [PPTX](c-scenario-configuration.pptx) |

Alle Folien sind auf Englisch und bestehen aus editierbaren PowerPoint-Objekten. Die vollständigen Erklärungen und Quellen stehen in den Sprechernotizen.

## Aktualisierte CI-Zählung

**878 eindeutige Testdefinitionen** aus den vom aktuellen `vita-fl/.github/workflows/ci.yml` ausgewählten Quellen, Stand 27. September 2026. Die früheren **808 = 731 Unit/Component + 77 Integration** beschreiben ausschließlich die historischen `../test-inventory.csv`, `.json` und `.md` sowie deren früheren Quellstand. Hier wird keine neue Aufteilung in Unit und Integration behauptet, sondern der vom Nutzer gewünschte gemeinsame CI-Bereich verwendet.

| Prüfgegenstand | Definitionen | Beispiele |
| --- | ---: | --- |
| Lernen und Modellintegrität | 78 | Datenteilung, Aggregationsmathematik, Modellpakete und Modellbindungen |
| Rundensteuerung und Recovery | 117 | Lokaler Timer, Eingabeschluss, Quorum, Veröffentlichung und Rundenfortschritt |
| Identität und sicherer Transport | 240 | Zulassung, Quotes, Schlüssel, RA-TLS/mTLS und Zugriffsschutz |
| Inferenz und Agentenablauf | 49 | MCP-Oberfläche, Jobzuordnung, TEE-/ZK-Inferenzablauf |
| Receipts und Herkunftsnachweise | 64 | AIR, Sello, Log-Bindungen und signierte Trainingsdaten |
| Laufzeitsteuerung und Telemetrie | 107 | Konfiguration, Upload-Gates, Workersteuerung und Ereignismetriken |
| Deployment und Paketierung | 223 | Image-Auswahl, Versionsreihenfolge, Docker-Kontexte und Offline-Terraform |
| **Summe** | **878** | Jede Definition genau einmal zugeordnet |

Die fachliche Zuordnung folgt der Hauptverantwortung jeder Testdatei. Eine Datei kann mehrere Aspekte prüfen, wird für diese Übersicht aber genau einem Bereich zugerechnet. Anzahlen sind keine Aussage über gleiche Testkomplexität oder prozentuale Abdeckung.

Ausführung laut Workflow: GitHub Actions, `ubuntu-latest`, Push/PR auf `main` und `phala_app_key` sowie manueller Start. Parameterkombinationen, Subtests und erneute Ausführungen werden nicht vervielfacht. Bedingt übersprungene Definitionen bleiben enthalten. Lint, Builds und die beiden Anvil/IPFS-Bereitschaftsprüfungen sind zusätzliche Pipeline-Prüfungen außerhalb der 878.

Die eigenen Tests von SMEW, SMA und vita-fl-td sind nicht automatisch Bestandteil dieser vita-fl-CI-Zahl. Detaillierte Definitionen, Dateizuordnung, CI-Jobs, Commit und Quellen-Fingerabdrücke: [ci-inventory.json](ci-inventory.json). Lesbarer Kurzbericht mit konkreten Testfunktionen: [ci-inventory.md](ci-inventory.md).

## Externer Testumfang

**Acht berücksichtigte Szenariotypen** aus neun vorhandenen CLI-Modi. Die zuvor abgewählte Manipulationsprüfung ist ausgenommen. Der Receipt-Audit ergänzt passende Inferenzläufe und wird nicht als weiterer Szenariotyp gezählt.

| Gruppe | Szenarien | Prüfung |
| --- | --- | --- |
| Einstellungen | `configuration` | Speichern/Lesen; ungültige Frist abweisen und Zustand erhalten |
| Ablauf und Inferenz | `normal`, `inference` | Erfolgreiche Trainingsrunden und Beteiligung; Inferenz mit dem finalisierten Modell |
| Sammelfrist | `early`, `partial`, `zero` | 5/5 Inputs vor Frist; 2/5 nach Frist; 0/5 ohne Veröffentlichung und anschließende Quorum-Recovery |
| Aggregatorausfall | `recovery` | Echten CVM-Stopp bestätigen; 1/3 → 2/3 → 3/3 Stimmen, Neuwahl und Fortsetzung |
| Zugriff und Vertragsbedingungen | `security` | 16 Checks einschließlich regulärer Inferenz als Positivkontrolle |
| Zusätzlicher Receipt-Audit | szenarioübergreifend | 17 Checks: 10 SCITT, 1 AIR/TDX, 3 Attestation-Sessions, 3 Sello |

Das aktuelle **Trainingsprofil** verwendet sechs Worker, fünf erfolgreiche Nicht-Bootstrap-Runden, Clientlimit fünf und 45 Sekunden Sammelfrist. `configuration` ist eine reine Setup-Prüfung. Im aktuellen Profil läuft auch vor `inference` das Training. Andere Kampagnen können diese Einstellungen variieren. Die acht Szenariotypen, 16 Security-Checks und 17 Audit-Checks sind verschiedene Zähleinheiten und werden nicht addiert.

Ausführung: SMEW organisiert die Kampagne, SMA führt den lokalen Testtreiber aus und sammelt Messdaten; vita-fl-td steuert das Phala-Deployment und prüft die Assertions. Timeout-Szenarien verwenden das ausdrücklich aktivierte Upload-Gate, Recovery einen echten Aggregator-CVM-Stopp. Der Audit verifiziert veröffentlichte Belege erneut mit den aufgezeichneten Produktions-Verifiern und neuer Phala-Quote-Appraisal.

Die Folien beschreiben Implementierung und Konfiguration, **keine acht bestandenen Live-Szenarien**. Für ihre Erstellung wurden keine Tests oder Cloud-Kampagnen ausgeführt. Historische Normal-Läufe mit anderen Rundenzahlen werden nicht dem aktuellen Fünf-Runden-Profil zugeschrieben. Details: [external-scope.json](external-scope.json).

## Ausgewählte Folie aktualisieren

Aus dem Verzeichnis `presentation`:

```bash
.venv/bin/python concepts/test-evaluation/build_selected.py
.venv/bin/python update_slide25_test_evaluation.py --render
```

Der erste Befehl erzeugt das freigegebene Asset und die Vorschauen von Variante A; der zweite aktualisiert Seite 26 unter Erhalt der anderen Folien und ihrer PowerPoint-Änderungen. Das historische `inventory_tests.py` ist kein Vorbereitungsschritt für diese Fassung.

## Alle drei Entwürfe erzeugen

Aus dem Verzeichnis `presentation`:

```bash
.venv/bin/python concepts/test-evaluation/ci-external/build_designs.py
```

Der Generator kontrolliert die 878 eindeutigen Definitionen, die disjunkte Gruppensumme, die Quellen-Fingerabdrücke, die Szenariozählung, die Objektgrenzen und den Textumbruch. Er prüft die gespeicherten PPTX-Dateien durch erneutes Öffnen und bestätigt per SHA-256, dass Hauptpräsentation und ausgewählte Testfolie beim Erzeugen der Vergleichsentwürfe unverändert bleiben. Ändern sich die inventarisierten CI-Quellen, verlangt er eine Aktualisierung des Inventars.

PNG und PDF sind Vorschauen aus dem vorhandenen Pillow-Renderer; PowerPoint kann Arial leicht anders umbrechen. Die editierbaren Originale sind die PPTX-Dateien. `validation.json` dokumentiert die Kontrollen des Entwurfsgenerators; `../selected-validation.json` und `../../../assets/test-evaluation-integration.json` gehören zur ausgewählten Fassung und ihrer Integration.
