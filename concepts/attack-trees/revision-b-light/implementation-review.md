# Implementierungsprüfung der sechs Attack Trees

Geprüft wurden die dargestellten Pfade gegen den aktuellen lokalen Code, mit getrennten Akteur- und Schlüsselvoraussetzungen. Die Prüfung bestätigt keine praktisch ausgeführten Angriffe und ersetzt keinen vollständigen Sicherheitsaudit. Kapitel 4 wurde nicht geändert. Exakte Quellen und SHA-256-Hashes stehen pro Folie in `trees.json`.

## Zentrale Korrektur

**Ein Teilnehmerkonto oder ein betriebenes Phala-CVM gewährt keine beliebige Signatur mit den Schlüsseln des zugelassenen Workloads.** Die Rollen sind verschieden:

| Autorität | Verwendung | Was ein Angreifer dafür tatsächlich braucht |
| --- | --- | --- |
| Logische Teilnehmeridentität | Enrollment eines Teilnehmers | Autorisierung dieses Kontos und gültige Admission; ersetzt keine spätere Action-Signatur. |
| TEE-Action-Key | Transaktionen, Commitments, Timeoutreports | Aktueller dstack-abgeleiteter Action-Key oder Kontrolle der ihn verwendenden Ausführung. |
| TEE-RSA-Key | Modell-/Uploadsignaturen und Entschlüsselung | Der entsprechende private RSA-Key oder Kontrolle des signierenden/entschlüsselnden Prozesses. |
| Medizinische Signer | Herkunft und Annotationen | Autorisierter Geräte-/Radiologensigner; korrekt signiert bedeutet nicht medizinisch wahr. |
| AIR-/Sello-Autorität | Inferenz- und Aufrufbelege | Passende Empfänger-/Evidence-Signierautorität und sämtliche Kontextbindungen. |
| Log-Autorität | Gültige Transparenzstatements | Kontrolle des autorisierten Logdienstes und seiner Signierbefugnis; TEE-Schlüssel helfen dabei nicht automatisch. |

Codebasis: `vita-fl/dfl/node_server/src/action_key.ts:65,198`, `participant_key.ts:247,332`, `vita-fl/smart_contracts/src/core/DeviceRegistry.sol:248,293`.

## 1 – Zulassung: grün für die gezeigten externen Versuche

Eine echte Quote zu einem beliebigen Image reicht nicht: Der Teilnehmer muss zum owner-committed Roster gehören; Enrollment-Signatur, Action-Sender, Quote-REPORTDATA und Nonce müssen zusammenpassen. Image und Rollen-Policy müssen zugelassen sein. Nach vollständiger Registrierung wird der Run-Roster eingefroren.

Der alte Text „mit abgelöstem Schlüssel signieren“ setzte nicht belegten Schlüsselzugriff und eine normale In-Run-Rotation voraus. Er wurde durch **Wiederholen bereits signierter Aktionen** ersetzt. Das Wiederholen verlangt keinen privaten Schlüssel; die Annahme im falschen aktuellen Kontext bleibt blockiert.

Belege: `DeviceRegistry.sol:119–134,248–255,293–338,477–530`, `AutomataDcapTdxV4Attestation.sol:149–171,310–333`.

## 2 – Modell: keine frei verfügbaren bösartigen Worker-Updates

Ein externer Angreifer kann Bytes verändern oder alte signierte Objekte wiederholen. Er erzeugt damit keine neuen gültigen Herkunfts-, Upload- und Commitment-Signaturen. Die entsprechenden Pfade bleiben grün.

**Absichtlich falsche Aggregation** verlangt nun ausdrücklich Kontrolle des zugelassenen Aggregators oder seiner beiden erforderlichen Signierbefugnisse: aktueller Action-Key **und** RSA-Artefaktsigner. Der intakte Code prüft Mitgliedschaft, Hashes und Anzahl im geschlossenen Accepted Set und mittelt genau die bereitgestellten Dateien. Die Blockchain prüft signierte Bindungen; sie berechnet den Mittelwert nicht selbst. Nach kompromittierter Ausführung kann eine mathematisch falsche Ausgabe trotzdem korrekt signiert sein. Dieser Pfad ist gelb (AS5).

**Frei gewählte schädliche Updates im bestehenden Run** verlangen entsprechend tatsächlich kontrollierte Worker-Ausführung beziehungsweise deren RSA- und Action-Autorität. Aufnahme und schädliche Wirkung bleiben zusätzliche Bedingungen. Auch dieser dargestellte Pfad ist gelb; eine konkrete Poisoning-Wirkung wurde nicht nachgewiesen.

Die normale ChestMNIST-Datenzufuhr ist im Image enthalten und wird beim Start kopiert. Die Folie behauptet deshalb keinen offenen Upload beliebiger vergifteter Trainingsdaten. Dabei sind nicht alle Einstellungen unveränderlich: `TRAIN_DATA_SRC`, `DATASET_NAME` und `EPOCH` sind zulässige variable Policy-Werte. Ein vorab autorisierter Deployment-Akteur kann vorhandene Datenpfade/Epochen wählen. Daraus folgt weder beliebige neue signierte Datenzufuhr noch eine bewiesene Qualitätsattacke.

Eine tatsächlich autorisierte medizinische Person kann auch falsche Semantik signieren, ohne Kryptographie zu brechen. Für einen entsprechend zugelassenen künftigen Dateneingang bleibt das ein eigener Poisoningpfad. **Gelb auf dieser Folie bezeichnet die ausdrücklich dargestellte Prozess-/Schlüsselkompromittierung, nicht allgemein falsche Semantik oder bloß den Umfang eines zukünftigen Runs.** Es folgt keine Garantie statistischer Robustheit.

Belege: `server.ts:470–518,644–732,1341–1399,2276–2317,2820–2860`; `cli.py:985–990,1279–1311`; `dicom_provenance.py:307–374`; `AggregationPolicy.sol:237–278`; `GMStorage.sol:294–342`; `gm_crypto.ts:126–172,209–213`; `dfl/Dockerfile:73–76`; `start_node_neural_network.sh:71–80`; `worker_policy.ts:45–76,478–480`.

## 3 – Recovery: vier getrennte Fälle

1. **Unberechtigte Reports – grün:** Eine öffentliche Contract-Funktion aufzurufen ersetzt die aktuelle Action-Key-Autorisierung nicht. Das logische Teilnehmerkonto reicht nicht.
2. **Erfundene, gültig signierte Quorum-Reports – gelb:** Genügend aktuelle TEE-Action-Signer müssen tatsächlich kompromittiert sein. Runde, Aggregator, Fristen, Eligibility und Quorum gelten weiterhin.
3. **Netzstörung mit ehrlichen Reports – rot:** Werden alle Uploads vor der ersten Annahme blockiert, bleibt das Set leer und es kann nicht veröffentlicht werden. Ausreichend intakte Worker können nach Miss-Zählern und Zeitgrenzen selbst gültige Reports signieren, wenn Policy/RPC lesbar und ihre Transaktionen zustellbar bleiben. Der Angreifer braucht keinen ihrer Schlüssel. Das ist ein Verfügbarkeitsangriff **mit korrekter Recovery-Reaktion**, keine gefälschte oder willkürliche Abwahl.
4. **Recovery verhindern – rot:** Der Aggregator bleibt nicht verfügbar und gleichzeitig erreichen zu wenige Reporter die Blockchain oder laufen überhaupt weiter. Eine einzelne Aggregatorstörung allein erfüllt diesen Pfad nicht.

Das Defaultquorum beträgt `ceil(eligible × 50 / 100)`: bei sechs autorisierten Teilnehmern also **3 von 5 Nicht-Aggregatoren**. Offlinegehen verkleinert den autorisierten/snapshotgebundenen Kreis nicht automatisch. Alle Reports müssen dieselbe aktuelle Runde und denselben Aggregator betreffen; Duplikate zählen nicht. Bootstrap-Runde 0 ist ausgenommen. Es muss noch ein zulässiger Ersatz existieren.

**Nur einige Uploads blockieren reicht nicht als Nachweis für eine Abwahl:** Schon vorhandene Beiträge können nach Deadline eine Veröffentlichung ermöglichen. Der dargestellte Pfad beginnt deshalb ausdrücklich vor der ersten Annahme. Ehrliche Worker berücksichtigen neben der Contract-Zulässigkeit ihr eigenes Fortschrittsbudget und die Aggregationskulanz. Das sind vorhandene Codebedingungen; bei dieser Prüfung wurden keine Timer verändert.

Belege: `bc_client.ts:877`; `DeviceRegistry.sol:248`; `AggregatorSelection.sol:195–313`; `server.ts:110–174,2037–2044,2208–2240`; `state_timing.ts:88–111,149–155`; `GMStorage.sol:453`.

## 4 – Inferenz: technische Verifikation, keine Garantie für jeden Chattext

Alte Modelle oder fremde Receipts zu wiederholen benötigt keinen privaten Signierschlüssel. Ihre Annahme im falschen Kontext wird jedoch durch Bundle-/Rundenprüfung, AIR-Signatur, Nonce, Request-/Response-/Manifest-Digests, RA-TLS-Session und Sello-Callbindung verhindert. Die Folie bleibt für diese gezeigten Versuche grün.

Die Frischeaussage wurde präzisiert: **bei der Modellvorbereitung ausgewählte Veröffentlichung**, kein Versprechen, dass jeder Inferenzaufruf nochmals das inzwischen allerneueste globale Modell abfragt.

Ein Prompt kann die Orchestrierung beeinflussen. Er kann die lokal registrierten Tools nicht einfach neu definieren oder AIR-/Sello-Signaturen erzeugen. Der technische Erfolgsstatus entsteht erst nach Verifikation und Transparenzpublikation. Das gilt nicht pauschal für den finalen LLM-Text: Der vorhandene Halluzinationsfilter ist heuristisch. Deshalb lautet das Angriffsziel nun ausdrücklich verifizierte Inferenz, nicht jede beliebige falsche Behauptung.

Belege: `model_source.py:218–241`; `app.py:329–360`; `tee_inference_client.py:245–269,521–618,704–755`; `sello_client.py:182–199`; `run_agent.py:329–365,728–737,1058`.

## 5 – Audit: Log-Signer und Netzwerkakteur getrennt

Eine fehlgeschlagene Sello-Publikation lässt den Receiver fehlschlagen; auch das Domain-Bundle muss vor dem technischen Gesamterfolg publiziert sein. Fehlende Belege als technisch verifizierten Erfolg auszugeben bleibt im intakten Pfad blockiert (grün).

**Gültige widersprüchliche Logstatements setzen Log-Signierautorität voraus.** Ein Netzwerkangreifer kann sie nicht allein mit kopierten Receipts erfinden. Erst kontrollierter Logdienst plus fehlender unabhängiger Vergleich ergibt den gelben AS8-Pfad. Er verlangt keine Fälschung der Receiver-/AIR-/Sello-Signatur.

Requests nicht weiterzuleiten oder Antworten zurückzuhalten benötigt dagegen weder Worker- noch Logschlüssel. Dieser Verfügbarkeitsverlust bleibt rot. Eine zurückgehaltene Antwort löscht keine eventuell bereits publizierten Belege.

Belege: `app.py:196–246`; `sello_client.py:182–199`; `agent_receipts/scitt.py:93–115,189–216`; `tee_inference_client.py:704–755`.

## 6 – Modelloffenlegung: TEE ist Empfänger

Der Modellschlüssel wird für zugelassene öffentliche Empfängerschlüssel verpackt; der menschliche Betreiber ist nicht automatisch Klartextempfänger. Ohne passenden privaten Schlüssel bleibt der externe Entschlüsselungsversuch grün.

Die gelben Routen verlangen tatsächliche Schlüssel-/Prozesskompromittierung, privilegierten Zugriff **innerhalb** des Gasts oder tatsächliche Freigabe bisheriger Geheimnisse an veränderten, nicht von der Registry zugelassenen Code. Deployment-Rechte allein reichen nicht. Die offiziellen Launcher deaktivieren SSH; dessen Abwesenheit wird nach der Repository-Dokumentation nicht selbst durch die aktuelle Admission attestiert. Die wirksame KMS-Upgrade-Policy und Live-Gastzugriff wurden nicht überprüft. Es wird keine aktuelle Schlüsseloffenlegung behauptet.

Belege: `gm_crypto.ts:178–195`; `participant_key.ts:247–290,332–350`; `DeviceRegistry.sol:487–490`; `phala/main.tf:395–403`; `phala/README.md:877–885`.
