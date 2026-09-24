# VITA-FL: Folienideen und Farbcodierung

Stand: 6. September 2026. Grundlage sind die vorhandene Präsentation mit 39 Folien
(22 Vortragsfolien, ungefähr 17 Minuten) und der lokale Vita-FL-Code. Die bestehende
Präsentation und ihr Generator wurden nicht verändert. Diese Konzepte sind ein
separates, editierbares Vorschlagsdeck; Folientexte bleiben passend zum Vortrag auf Englisch.

## Vorschauen

- [Galerie mit vergrößerbaren Vorschauen](index.html)
- [Editierbare PowerPoint: acht Konzepte](VITA-FL_Color_Navigation_Concepts.pptx)
- [PDF mit allen Vorschauen](VITA-FL_Color_Navigation_Concepts.pdf)
- [Übersichtsbild der sieben konkreten Folien](overview.png)
- [Farbsystem und drei Navigationsvarianten](01-color-system.png)
- [Neue Motivationsfolie: Krankenhäuser und Datenkontrolle](08-hospital-data-control.png)

Meine Empfehlung: **Navigation A + Systemkarte 02 + Modellübergabe 03** übernehmen.
Die Fehlerfälle und Worker-Matrix bringen als neue Inhalte besonders viel: Sie
zeigen greifbares Verhalten und echte Messdaten. Dafür lassen sich Details ins
Backup verschieben, statt den Vortrag zu verlängern.

## Feste Farbbedeutung

| Bereich | Farbe | Helle Fläche | Zugeordnete Elemente |
|---|---|---|---|
| DFL | Grün `#207548` | `#EDF6F0` | Medizinische Trainingsinputs, Worker, Training, Aggregation, DFL-Messwerte |
| Agent / MCP / Inference / Log | Blau `#1764A1` | `#EDF4FA` | Agent, MCP-Tools, Receiver, AIR, Tool-Receipts, Transparency Log |
| Blockchain / IPFS | Violett `#7446A6` | `#F3EEF8` | Smart Contracts, autoritative Modellreferenzen, IPFS-Artefakte |
| TU Berlin | Rot `#C40D1E` | vorhandene Vorlage | Logo und Footer; bei Fehlern zusätzlich ein explizites ×/STOP-Label |

Die heutigen Farben wechseln ihre Bedeutung: Auf Folie 6 ist der Receiver blau,
auf 14 und 16 grün. Der Ledger ist auf 6 grün und auf 14 rot. Log und IPFS sind
beide violett. Mit der festen Zuordnung kann das Publikum denselben Bereich
über mehrere Folien wiedererkennen.

Anwendungsregeln:

1. **Die drei Beschriftungen bleiben an derselben Stelle unter dem Titel.**
   Aktive Bereiche sind gefüllt, inaktive grau. Auf einer Schnittstellenfolie
   dürfen mehrere Bereiche aktiv sein, etwa Blau und Violett beim Handoff.
2. **Bereichsfarben bezeichnen Funktionen, keine Vertrauensstufen.**
   Vertrauensgrenzen zusätzlich beschriften und gegebenenfalls dunkelgrau
   gestrichelt darstellen. Ein grünes Objekt bedeutet nicht „sicher“.
3. **Komponenten erben ihre Bereichsfarbe.** Der Receiver bleibt auch beim
   Prüfen grün gefärbter DFL-Artefakte blau. Alle drei TEE-Toolschritte sind blau;
   Nummern und Namen unterscheiden die Operationen.
4. **Blockchain und IPFS gehören optisch zusammen, bleiben funktional getrennt.**
   Blockchain bezeichnet den finalisierten Zustand; IPFS liefert Artefakte.
   Der Transparency Log bleibt blau und bekommt eine eigene, eindeutige Box.
5. **Farbe durch Beschriftung, Form und Füllung ergänzen.** Bei der Worker-Matrix
   stehen A/T und kräftige/helle Füllung für Aggregation/Training. Keine sechs
   zusätzlichen Workerfarben einführen. Bei Metriken Namen und Linienmuster
   verwenden; die Bereichsfarbe nicht für eine zweite Bedeutung umwidmen.
6. **Helle Flächen, dunkle Schrift, farbige Titel und Konturen.** Die dunkleren
   Hauptfarben sind für weiße Schrift in Navigation und Markierungen gewählt.
   TU-Rot bleibt erhalten, wird aber aus normalen Datenfluss-Pfeilen herausgenommen.

Die [erste Vorschau](01-color-system.png) vergleicht drei Navigationsformen:

- **A – persistente Felder:** die klarste Zuordnung, Empfehlung für dieses Deck.
- **B – unterstrichene Bereiche:** zurückhaltender, auf der Inferenzsequenz gezeigt.
- **C – kleine Systemkarte:** stärkerer Architekturbezug, besonders auf Übergangsfolien.

Für das fertige Deck eine Navigationsform auswählen und durchgehend verwenden.
Die unterschiedlichen Formen im Vorschlagsdeck dienen dem Vergleich.

## Konkrete Folienvorschläge

| Vorschau | Einsatz im bestehenden Deck | Mehrwert / Zeitbedarf |
|---|---|---|
| [02: Architektur](02-architecture.png) | Folie 6 ersetzen | Zwei Verantwortungsketten, darunter gemeinsame Infrastruktur. Kein zusätzlicher Vortragsslot. |
| [03: Modellübergabe](03-model-handoff.png) | Folie 14 ersetzen | Blockchain benennt, IPFS liefert, Receiver prüft. Historischer Publisher-Key-Snapshot wird sichtbar. |
| [04: Inferenzsequenz](04-inference-sequence.png) | Folie 16 ersetzen | Drei blaue Toolschritte; Rückgabe folgt auf Receipt-Publikation und Verifikation. |
| [05: Fehlerpfade](05-failure-paths.png) | Nach Folie 14 oder 16; alternativ Backup | Manipulierte Modellbytes und ausgefallene Log-Publikation machen Ablehnung konkret. Etwa 30–40 Sekunden. |
| [06: Aussagekraft der Nachweise](06-evidence-scope.png) | Folie 18 vereinfachen oder Backup nach 17 | Pro Beleg genau eine Frage und eine Grenze. Gut für Prüfungsgespräche. |
| [07: Worker-Rollen](07-worker-roles.png) | Nach Folie 19 oder Backup zu 10 | Sechs Worker × 24 Runden aus echten Daten; verbindet Auswahllogik und beobachteten Ablauf. Etwa 25–35 Sekunden. |
| [08: Krankenhäuser und Datenkontrolle](08-hospital-data-control.png) | Nach der Arztperspektive auf Folie 3, vor der technischen Antwort | Patientengeheimnisse schützen, Zugriffe kontrollieren und gemeinsam lernen, ohne Rohdaten zentral zu sammeln. Etwa 20–30 Sekunden. |

Die neue Krankenhausfolie zeigt drei Einrichtungen mit geschützten lokalen
Patientendaten. Nur Modellupdates führen zum gemeinsamen Modell. Die Kernaussage
lautet: **Krankenhäuser möchten Datenkontrolle und gemeinsames Lernen verbinden.**
Das ist das angestrebte Anwendungsszenario; der Prototyp wurde mit ChestMNIST auf
Phala untersucht. Die Darstellung behauptet keinen realen Krankenhausbetrieb
und keine formale Datenschutzgarantie allein durch föderiertes Lernen. Das
gemeinsame Modell ist ein Artefakt; die Aggregatorrolle ist temporär.

Codebasis sind das Training auf lokalen Shards und die Verschlüsselung des
exportierten lokalen Modells in [`cli.py`](../../../vita-fl/dfl/neural_network/cli.py),
Zeilen 991–1004 und 1069–1077. „Model updates“ bezeichnet hier vollständige lokale
Modellparameter. Diese Grenzen und ein kurzer Sprechtext stehen in den Foliennotizen.

Die Fehlerpfade sind **illustrierte Codepfade**, keine neu durchgeführten Angriffe.
Die Log-Ausfallregel gilt für den gezeigten Pfad mit aktivierten Sello-Receipts.
Eine bereits ausgeführte Aktion wird bei einem Publikationsfehler nicht zurückgerollt;
es wird kein erfolgreicher Toolabschluss zurückgegeben.

Für eine kompakte Vortragsfassung würde ich Original Hybrid-R (derzeit Folie 13)
und das detaillierte Kryptografie-Inventar (18) ins Backup verschieben. So entsteht
Platz für einen Fehlerfall und die empirische Worker-Matrix. Alternativ bleibt die
Matrix im Backup, und 18 wird durch die kurze Nachweisübersicht ersetzt.

Weitere sinnvolle Verbesserungen ohne neue Folien:

- **Folie 8:** je ZK-Relation nur Input → Zustandsänderung → gebundener Output
  zeigen; die langen kryptografischen Listen ins Backup.
- **Folie 19:** Trainingswerte grün, Inferenzwerte blau, Anvil-Gas violett.
  Die 2,839 ms bezeichnen native Inferenz, nicht den gesamten Agent-/Log-Ablauf.
- **Folie 20:** AUROC und F1 groß zeigen; BCE ergänzend. Accuracy und Exact Match
  mit der Baseline auf Folie 21 erklären.
- **Optionales Gas-Backup:** 76,64 % Registrierung, 9,34 % Initialisierung,
  14,02 % übriger Workerbetrieb. Als Anvil-EVM-Gasbilanz beschriften, nicht als
  öffentliche Chain-Gebühren oder Phala-Betriebskosten.

## Code- und Datenbelege

Die folgenden Zeilen beziehen sich auf den beim Review gelesenen lokalen Stand.
Die PowerPoint-Notizen nennen zusätzlich die relevanten Quellen und Grenzen.

| Aussage | Quelle |
|---|---|
| Aktiver Aggregationspfad ist gleichgewichtete FedAvg | [`cli.py`](../../../vita-fl/dfl/neural_network/cli.py), Funktion `_equal_weight_federated_average`, Zeile 1276 |
| Runtime erzwingt FedAvg-Policy ohne Hybrid-R-Validierung | [`server.ts`](../../../vita-fl/dfl/node_server/src/server.ts), Zeile 2285 |
| Finalisierung bindet Zustand und Modellreferenzen atomar | [`GMStorage.sol`](../../../vita-fl/smart_contracts/src/core/GMStorage.sol), Zeilen 180–206 |
| Finalisiertes Bundle enthält den Publisher-Key-Snapshot | [`blockchain_source.py`](../../../vita-fl/agent/blockchain_source.py), Zeile 357 |
| Receiver löst Bundle auf und prüft Modellübergabe | [`model_source.py`](../../../vita-fl/tee_inference/service/model_source.py), Zeile 218 |
| Sechs öffentliche MCP-Tools, davon drei für TEE | [`mcp_server.py`](../../../vita-fl/agent/mcp_server.py), Zeilen 45 und 316 |
| Receiver publiziert Receipt vor Rückgabe; Fehler führt zu HTTP 503 | [`app.py`](../../../vita-fl/tee_inference/service/app.py), Zeilen 118–149 |
| AIR-, Hash-, REPORTDATA-, RTMR3- und Image-/Contract-Prüfung | [`tee_inference_client.py`](../../../vita-fl/agent/tee_inference_client.py), Zeile 542 |
| Inferenz-Verifier meldet `dcap_collateral_verified: False` | [`tee_inference_client.py`](../../../vita-fl/agent/tee_inference_client.py), Zeile 636 |
| Vollständiges Inferenz-Evidence-Bundle wird in SCITT registriert | [`tee_inference_client.py`](../../../vita-fl/agent/tee_inference_client.py), Zeile 691 |
| Sello-Aktivierung ist konfigurationsabhängig | [`environment.py`](../../../vita-fl/agent_receipts/environment.py), Zeile 30 |
| CCF-Log läuft als einzelner Knoten in virtual mode | [`Transparency-Log-README`](../../../vita-fl/transparency_log/README.md) |
| Worker-Rollen pro Runde | [`round_metrics.csv`](../../../vita-fl/data/evaluation/authoritative-phala-6w-24r-20260901/round_metrics.csv) |
| Worker-Aktivität / Trainingsbeiträge | [`worker_activity.csv`](../../../vita-fl/data/evaluation/authoritative-phala-6w-24r-20260901/worker_activity.csv) |
| Gasbilanz und Run-Scope | [`run_manifest.json`](../../../vita-fl/data/evaluation/authoritative-phala-6w-24r-20260901/run_manifest.json) und zugehöriges [`README`](../../../vita-fl/data/evaluation/authoritative-phala-6w-24r-20260901/README.md) |

Die Worker-Matrix ist aus `round_metrics.csv` erzeugt: VM0–5 aggregieren
**2 / 3 / 4 / 4 / 9 / 2** Mal. Jede Runde hat fünf akzeptierte Clientmodelle,
insgesamt 120 Beiträge. Föderierte Runden 1–24 entsprechen publizierten
Modellrunden 2–25. Der Einzelrun belegt keine langfristige Auswahlfairness;
bei null abgebrochenen Versuchen wird die Recovery hier nicht empirisch geprüft.

Zwei Formulierungsgrenzen sind besonders wichtig: Die im Inferenz-Tool fehlende
vollständige DCAP-Collateral-Prüfung ist von der separaten On-Chain-Zulassung
der DFL-Worker zu unterscheiden. Außerdem darf aus der Job-ID im Toolinterface
nicht abgeleitet werden, dass Bilddaten die TEE nie verlassen: Das Evidence-Bundle
enthält Request-Bytes mit Pixeln und wird vollständig registriert.

## Reproduktion und Prüfung

Vom Workspace `/home/ramon/master/Master-Thesis` aus:

```bash
presentation/.venv/bin/python presentation/concepts/color-navigation/build_concepts.py
```

Der Generator nutzt die vorhandene TU-Vorlage, `python-pptx` und den lokalen
Vorschaurenderer. Text, Formen, Verbindungen und die Matrix sind in der PPTX
editierbar. Die PDF enthält die gerasterten Layoutvorschauen.

Geprüft werden Foliengrenzen, Textflächen anhand derselben Fontmetriken wie die
PNG-Vorschau sowie Rundenfolge und Beitragszahl der Quelldaten. Die Vorschauen
wurden zusätzlich visuell geprüft. PowerPoint/LibreOffice waren hier nicht
verfügbar; exakte Office-Schriftumbrüche sind daher nicht geprüft. Die bestehende
Präsentation wurde nicht neu erzeugt, und Anwendungstests wurden für diesen
reinen Vorschlags-/Layoutauftrag nicht ausgeführt.
