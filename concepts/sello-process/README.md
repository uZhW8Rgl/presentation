# Sello + AIR: Ablauf und Verifikation

Die ausgewählte Variante B ist mit einer vereinfachten Kopie in die [Hauptpräsentation](../../VITA-FL_Thesis_Presentation_TU_Berlin.pptx) integriert: **Detailansicht auf Seite 24**, **generalisierte Ansicht auf Seite 25**. Beide zeigen den dritten MCP-Aufruf `run_and_verify_tee_inference`. Kapitel 4 bleibt unberührt. Die ursprünglichen drei Entwürfe bleiben als Vergleich verfügbar. Alle Diagramme bestehen aus editierbaren PowerPoint-Elementen im hellen TU-Berlin-Stil; ihre Texte sind passend zum Hauptdeck auf Englisch.

[Übersicht](overview.png) · [Galerie](index.html) · [PowerPoint mit allen Varianten](VITA-FL_Sello_Process_Alternatives.pptx) · [PDF-Vorschau](VITA-FL_Sello_Process_Alternatives.pdf)

**Integriertes Folienpaar:** [Editierbares Asset](../../assets/sello-process-b.pptx) · [PDF-Vorschau](b-presentation-pair.pdf) · [Generalisierte Vorschau](b-generalized.png) · [Generalisierte Einzelfolie](b-generalized.pptx).

| Entwurf | Darstellung |
| --- | --- |
| [A – Vertikales Sequenzdiagramm](a-sequence.png) · [PPTX](a-sequence.pptx) | Drei Akteursspalten, Zeit von oben nach unten, nummerierte Nachrichten und lokale Schritte. |
| [B – Horizontale Rollenbahnen](b-swimlanes.png) · [PPTX](b-swimlanes.pptx) | Vier horizontale Bereiche von oben nach unten: Agent Runtime, Inference TEE, Transparency Log und Phala API; der Prozess wandert von links nach rechts zwischen den Rollen. |
| [C – Zwei Belege im Zusammenspiel](c-receipt-journey.png) · [PPTX](c-receipt-journey.pptx) | Drei große Verantwortungsbereiche; getrennte AIR- und Sello-Belege mit ihren Publikationswegen. |
| [B – Generalisierte Kopie](b-generalized.png) · [PPTX](b-generalized.pptx) | Seite 25: gleiche vier Rollen und gleicher Protokollpfad, mit zusammengefassten Prüfgruppen und ohne sichtbaren A10-Schritt. |

Variante B zeigt die feste Implementierung innerhalb des ausgewählten Tools `run_and_verify_tee_inference`. Das LLM kann aus den bereitgestellten Tools wählen; die Agent Runtime führt die zum Tool gehörenden Prüfungen verbindlich aus. Der Hinweis auf der Folie lautet: **“LLM selects the tool · Runtime enforces verification.”** Die Rollenbahn „Agent Runtime“ bezeichnet daher den ausführenden und prüfenden Code, nicht frei gewählte Einzelschritte des Sprachmodells.

Die Detailansicht von Variante B auf Seite 24 zeigt auf **einer Folie** den vollständigen AIR-Ablauf A1–A10 mit höherer Agent-Runtime-Bahn und Phala API ganz unten. POST der Quote mit JSON-Antwort und anschließender GET der Originalquote mit Byte-Antwort sind getrennt dargestellt. A und C behalten ihre drei Rollenbereiche und fassen dieselben globalen Schritte zusammen: **A1** Erstellung, **A2–A8** Verifikation, **A9–A10** Publikation und Inclusion-Prüfung.

## Generalisierte Kopie auf Seite 25

Die Kopie verwendet dieselben Farben, Rollen und ursprünglichen Schrittnummern wie die Detailansicht. Sie bündelt:

| Gruppe | Bedeutung |
| --- | --- |
| **A2 / A4** | Agent-Prüfungen vor und nach den API-Aufrufen: Kontext-/Quote-Policy sowie JSON-Verifikationsergebnis. |
| **A3 / A5** | Phala-Quote-Verifikation und Abruf der Originalquote. Der Hin-/Rückweg fasst zwei HTTP-Transaktionen mit dazwischenliegender JSON-Prüfung im Agenten zusammen. |
| **A6–A8** | Lokaler Bytevergleich, AIR-Signatur und Bindungen, RTMR3-Replay sowie Deployment-/Ausgabepolicy. |
| **A9** | Separate AIR-Bundle-Publikation; die unveränderte Implementierung verlangt weiterhin die erfolgreiche Inclusion-Prüfung. |

**A10 entfällt nur als sichtbarer Kasten.** Die Inclusion-Verifikation wurde weder aus dem Code noch aus den Erfolgsvoraussetzungen entfernt. Die Gruppe A2/A4 ist kein zusammenhängender Block: Vorprüfung → Quote-POST → JSON-Prüfung → Rawquote-GET bleiben die tatsächliche Reihenfolge. Erst nach abgeschlossenem API-Pfad geht der durchgezogene Ablauf weiter zu A6–A8. Die gestrichelten Datenpfeile **A1 → 7 → A2/A4** und der verbindliche Ablauf **9 → A2/A4** bleiben erhalten.

## Farben

Eine Legende steht auf jeder Folie. Die Farben kennzeichnen Protokollbereiche, keine Sicherheitsbewertung:

- **Dunkelorange (`#A84B13`, Tönung `#FFF3E8`):** Sello-Aufrufbeleg, seine Veröffentlichung und Prüfung sowie der ausdrücklich bezeichnete RA-TLS-Auditexport dieses Pfads.
- **Dunkelblau (`#245AA5`, Tönung `#EDF3FD`):** Inferenz und AIR-Erstellung, AIR-Prüfung und separate Veröffentlichung des AIR-Evidence-Bundles.
- **Grau (`#686868`):** Gemeinsame Autorisierung, Sessionaufbau und Transport der Antwort, die beide Belege enthält.

Akteursbereiche bleiben neutral. Die RA-TLS-Sessionprüfung gehört zum gemeinsamen Aufbau und wird nicht als AIR-Schritt eingefärbt.

In beiden B-Ansichten unterscheiden die Linienstile **durchgezogen = Ausführungsreihenfolge** und **gestrichelt = AIR-Datenbezug**. Zwei dunkelblaue gestrichelte Pfeile zeigen **A1 → 7** (das erzeugte AIR-Bundle wird in der Antwort transportiert) und **7 → A2** (dieses empfangene Bundle wird später geprüft). Sie zeigen Datenherkunft und -verwendung, keine zusätzlichen Requests oder parallele Ausführung. Das tatsächliche Bundle kommt mit Antwort 7; die bestehende Reihenfolge **Sello-Abschluss 9 → A2** bleibt verbindlich.

## Reihenfolge

Die drei Entwürfe zeigen denselben Ablauf im aktuellen RA-TLS-Pfad der Phala-Konfiguration. Modell und Inferenzjob sind bereits vorbereitet. Die ursprünglichen Nummern 1–9 bleiben für Sello und gemeinsamen Aufbau erhalten; A1–A10 kennzeichnen durchgehend die AIR-Schritte.

1. **Gemeinsam, 1–3:** Der Agent erstellt das Autorisierungstoken, prüft die attestierte TLS-Session und sendet den geschützten Request mit Token und PoP. Die TEE prüft die Autorisierung.
2. **AIR, A1:** Die TEE führt die Inferenz aus, erzeugt eine eigene Inferenz-Quote, signiert das AIR-Receipt und erstellt das vollständige Evidence-Bundle.
3. **Sello, 4:** Die TEE bindet den logischen Toolinput (`job_id`) und die vollständigen AIR-Ausgabebytes über Hashes. Sie verschlüsselt den Receipt-Body per HPKE für den Owner und signiert anschließend den verschlüsselten Umschlag per COSE.
4. **Sello, 5–6:** Die TEE publiziert das Receipt über ein SCITT-Statement. Das Log liefert Inclusion-Evidence; die TEE prüft sie vor einer erfolgreichen Antwort.
5. **Gemeinsam, 7:** Die Antwort enthält das AIR-Bundle im Body, das Sello-Receipt in Headern sowie die Sello-Publication-Bundle-Referenz.
6. **Sello, 8:** Der Agent prüft Receipt-Signatur, Entschlüsselung, Aufruf-/Sessionbindung und Inclusion. Das Publication-Bundle wird bei der TEE abgerufen, öffentliche Logkeys beim Log.
7. **Sello-Pfad, 9:** Der bestehende RA-TLS-Auditexport publiziert die ursprüngliche Session-Evidence und den owner-verschlüsselten Token-/Input-/Output-Kontext. Beide Publikationen mit Inclusion-Prüfung müssen gelingen.
8. **AIR, A2–A8:** Lokale Vorprüfungen, delegierte Quote-Verifikation bei Phala mit getrennten JSON-/Rawquote-Abrufen, anschließender Bytevergleich sowie lokale AIR-, RTMR3- und Deployment-Policyprüfungen.
9. **AIR, A9–A10:** Der Agent publiziert das vollständige geprüfte AIR-Evidence-Bundle separat und prüft dessen Inclusion. Erst danach meldet der Aufruf `verified-and-transparency-logged`.

Sello-Schritt 8 fasst Verifikation und zugehörige Abrufe zusammen; Sello-Schritt 9 fasst zwei zusätzliche Publikationen zusammen. Rückwege für Inclusion-Prüfungen sind teilweise zusammengefasst. Es handelt sich also nicht um nur zwei HTTP-Logzugriffe. Der Agent übernimmt in diesem Prototyp auch die Owner-/Token-Issuer-Funktion; dafür gibt es keinen eigenen Akteursbereich. Die unterste, vierte Bahn in B stellt ausschließlich die Phala API dar.

## AIR-Schritte der Detailansicht B

**Reihenfolge: gemeinsamer Aufbau 1–3 → A1 → Sello 4–9 → A2–A10.** Die lokalen Schritte liegen in der Agent Runtime, nicht beim LLM oder bei Phala.

| Schritt | Akteur | Aktion |
| --- | --- | --- |
| **A1** | Inference TEE | Inferenz ausführen, Inferenzquote und signiertes AIR-Bundle erzeugen. |
| **A2** | Agent Runtime | Session, Request-/Manifestbindung, AIR-Key/Nonce, REPORTDATA und Plattform-Allowlist vorprüfen. |
| **A3** | Agent Runtime ⇄ Phala API | Quote per POST als `{"hex": …}` senden; JSON-Verifikationsergebnis empfangen. |
| **A4** | Agent Runtime | `success`, `quote.verified`, zurückgelieferte Quote-Felder und Lookup-`checksum` prüfen. |
| **A5** | Agent Runtime ⇄ Phala API | Originalquote per GET `/raw/{checksum}` abrufen; vollständige Quotebytes empfangen. |
| **A6** | Agent Runtime | Vollständige Quote vergleichen; AIR-Signatur, Modell-/Input-/Output-/Nonce-Bindungen, Quote-Hash und signierte Messwerte prüfen. |
| **A7** | Agent Runtime | **Verify RTMR3:** Eventlog lokal replayen und mit RTMR3 der authentifizierten Quote vergleichen. |
| **A8** | Agent Runtime | Gemessenen Compose-Hash, Image-Digest und Contract-/Chain-/RPC-Policy prüfen; anschließende Plausibilitätsprüfungen der Ausgabe sind in den Notizen erläutert. |
| **A9** | Agent Runtime ⇄ Transparency Log | Vollständiges AIR-Domainbundle registrieren, Publication-Evidence erhalten und öffentliche SCITT-Keys abrufen. |
| **A10** | Agent Runtime | Inclusion der exakten Statement-/Bundle-Bytes prüfen und erst danach verifizierten Erfolg zurückgeben. |

A3 und A5 zeigen jeweils Request und direkte Antwort; Phala sendet keinen zusätzlichen Callback und keine Antwort an die Inference TEE. A9 ist ein gruppierter SCITT-Ablauf mit Submit/Wait und Keyabruf, kein Versprechen eines einzigen HTTP-Requestpaars. Die Ausgabeprüfungen nach der Deployment-Policy kontrollieren endliche Werte, Wahrscheinlichkeiten in `[0,1]` und den Entscheidungsschwellenwert; sie belegen keine medizinische Korrektheit.

## Wichtige Abgrenzungen

- Die ersten beiden MCP-Funktionen verwenden ebenfalls Sello. Die hier gezeigten AIR-Schritte A1–A10 gehören zum dritten Aufruf `run_and_verify_tee_inference`.
- Die Quote des RA-TLS-Sessionaufbaus und die Inferenz-Quote im AIR-Bundle sind unterschiedliche Belege.
- Variante B zeigt die Phala-Prüfung der **Inferenz-Quote**. Die separate Quote-Verifikation beim Sessionaufbau bleibt in 1–3 zusammengefasst. Die JSON-Antwort auf den Quote-POST (A3) und die Byte-Antwort auf den Rawquote-GET (A5) haben getrennte Rückwege zum Agenten.
- Phala übernimmt die kryptografische Quote-Verifikation; der Agent prüft die Intel-DCAP-Vertrauenskette nicht unabhängig selbst. Er kontrolliert Erfolg, Quote-Felder und exakte Quotebytes und prüft AIR-Signatur, Bindungen, RTMR3 und Policy lokal. Die API-Antwort wird nicht als signiertes EAT dargestellt.
- AIR-Signierschlüssel, Sello-Receiver-Key und Signierschlüssel des äußeren SCITT-Statements sind getrennt.
- Sello verschlüsselt zunächst Receipt-Hashes und Metadaten, nicht das gesamte AIR-Ergebnis. Der zusätzliche Auditkontext enthält Token/Input/Output owner-verschlüsselt.
- Das Publication-Bundle ist kein zweites Sello-Receipt. Der Agent lädt es über den von der TEE angegebenen Endpunkt.
- Fehlgeschlagene Publikation verhindert verifizierten Erfolg; bereits ausgeführte Berechnung wird nicht zurückgerollt.
- Log-Inclusion belegt die Aufnahme der geprüften Bytes. Sie belegt allein weder Inferenzkorrektheit noch globale Logkonsistenz oder dauerhafte Verfügbarkeit.

## Codebelege und Prüfung

Geprüfte Quellen im Repository `vita-fl`: `agent/run_agent.py`, `agent/sello_client.py`, `agent/tee_inference_client.py`, `transport_security/ratls_client.py`, `transport_security/attestation.py`, `tee_inference/service/app.py`, `tee_inference/service/attestation.py`, `agent_receipts/sello_v1.py`, `agent_receipts/receiver_log.py`, `agent_receipts/scitt.py`, `agent_receipts/environment.py` und die Phala-Templates. Exakte Zeilen, Quellhashes und Erläuterungen stehen in den Sprechernotizen.

Assets und Vorschauen aus `presentation` neu bauen:

```bash
.venv/bin/python concepts/sello-process/build.py
```

Dieser Builder erzeugt auch [das Folienpaar](../../assets/sello-process-b.pptx), aktualisiert die Hauptpräsentation aber nicht selbst. Die Integration beziehungsweise Aktualisierung der beiden Hauptfolien übernimmt [update_sello_process.py](../../update_sello_process.py):

```bash
.venv/bin/python update_sello_process.py --render
```

Der Asset-Build prüft Layout, PPTX-Roundtrip, Sello-/gemeinsame Schritte 1–9, AIR-Schritte A1–A10 in der Detailansicht beziehungsweise A1–A9 in der generalisierten Darstellung, drei Akteursbereiche in A/C und vier in beiden B-Ansichten, Farblegenden und native Formen. Er prüft außerdem, dass er selbst Hauptpräsentation und Kapitel 4 nicht verändert. A/C verwenden die Gruppen A1, A2–A8 und A9–A10. Die Integration aktualisiert anschließend gezielt die beiden Hauptfolien; ihr Prüfprotokoll steht in [sello-process-integration.json](../../assets/sello-process-integration.json). Der Asset-Prüfbericht steht in [validation.json](validation.json). PNG und PDF sind lokale Layoutvorschauen; Umbrüche in PowerPoint können aufgrund anderer Schriften leicht abweichen.
