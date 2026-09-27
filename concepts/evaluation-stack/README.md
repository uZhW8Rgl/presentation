# Zusammenspiel der Evaluationswerkzeuge – vier Folienvorschläge

Vier alternative, **editierbare** Einzelfolien im Stil der englischen TU-Berlin-Präsentation. Sie erklären die Architektur von SMEW, SMA, vita-fl-td und VITA-FL auf Metaebene. Variante **C** wurde ausgewählt und als **Seite 24** in die Hauptpräsentation übernommen. Die Entwürfe bleiben separat erhalten. Stand der Implementierung: 27. September 2026.

[Galerie mit Vergrößerung](index.html) · [Gesamtübersicht](overview.png) · [Alle Varianten als PowerPoint](VITA-FL_Evaluation_Stack_Alternatives.pptx) · [PDF-Vorschau](VITA-FL_Evaluation_Stack_Alternatives.pdf)

| Variante | Fokus | Geeignet für | Dateien |
| --- | --- | --- | --- |
| **A – Ablaufkette** | SMEW startet SMA, SMA startet TD, TD steuert VITA-FL. Ergebnisse fließen zurück; Messdaten ergänzen den Bericht. | Eine kurze Einführung in den Gesamtablauf. | [PowerPoint](a-workflow.pptx) · [Vorschau](a-workflow.png) |
| **B – Verschachtelte Ebenen** | Kampagne → Messlauf → Testszenario. Das deployte VITA-FL steht außerhalb dieser Ausführungsebenen. | Die Abgrenzung von Verantwortlichkeiten. | [PowerPoint](b-execution-layers.pptx) · [Vorschau](b-execution-layers.png) |
| **C – Testrechner und Phala** | Lokale Werkzeuge und deploytes System mit Steuerungs-, Ergebnis- und Metrikflüssen. | Die konkrete Erklärung des Versuchsaufbaus. **Empfehlung.** | [PowerPoint](c-deployment-boundary.pptx) · [Vorschau](c-deployment-boundary.png) |
| **D – Vier Rollen** | Jedes Werkzeug beantwortet eine Frage und liefert einen Teil der Auswertung. | Eine besonders ruhige, kompakte Rollenübersicht. | [PowerPoint](d-responsibilities.pptx) · [Vorschau](d-responsibilities.png) |

## Kernaussage für den Vortrag

„SMEW organisiert die Experimente und Wiederholungen. SMA startet den Testtreiber und führt Prozessinformationen, Messdaten und Ergebnisdateien zu einem Bericht zusammen. vita-fl-td steuert die Szenarien und prüft, ob sich das deployte VITA-FL wie erwartet verhält. VITA-FL führt Training, Aggregation und Inferenz aus und veröffentlicht die dazugehörigen Belege. Die gespeicherten Ergebnisse können anschließend im Marimo-Notebook verglichen werden.“

Eine der Alternativen eignet sich als Einstieg in den Evaluationsabschnitt, vor den einzelnen Szenarien und deren Ergebnissen.

## Genauigkeit der Darstellung

- Die Host-/Phala-Aufteilung beschreibt den aktuellen Evaluationsaufbau. Der SMEW-Orchestrator kann getrennt vom Daemon betrieben werden; andere Docker-Profile sind ebenfalls möglich.
- Die Verschachtelung in B beschreibt logische Verantwortungen. VITA-FL wird nicht als lokaler Subprozess des Testtreibers dargestellt.
- Prometheus erfasst die exportierten Metriken. SMA ruft die Zeitreihen **nach dem Lauf für das aufgezeichnete Messfenster** ab.
- SMA ist kein Energiesensor. Die Darstellung behauptet keine Messung elektrischer Energie.
- vita-fl-td prüft die fachlichen Assertions und, bei aktiviertem Audit, veröffentlichte Receipts erneut. Dabei werden Verifier-Primitiven wiederverwendet und aktuelle Phala-Quote-Prüfungen eingeholt.
- SMEW prüft zusätzlich den Ergebnisvertrag und den Status des Messlaufs. Ein erfolgreicher Prozessstart oder Exit allein ist kein bestandener Systemtest.
- Marimo liest gespeicherte Berichte und visualisiert Ergebnisse. Es startet keine Kampagne und wiederholt nicht selbst die kryptografische Verifikation.
- Die Folien nennen keine Erfolgsquoten und machen keine neuen Aussagen über abgeschlossene Experimente. Quellen und ausführlichere Grenzen stehen in den Sprechernotizen jeder Folie.

## Reproduzieren und prüfen

Aus dem Verzeichnis `presentation`:

```bash
.venv/bin/python concepts/evaluation-stack/build_designs.py
```

Der Generator erzeugt eine Datei mit vier Folien, vier Einzelfolien-Dateien, PNG-Vorschauen, PDF, Übersicht und HTML-Galerie. Diagramme und Beschriftungen bestehen aus nativen PowerPoint-Objekten. Nur das Vorlagenlogo ist ein Bild.

Die Prüfung kontrolliert Objektgrenzen, Textumbruch anhand der Vorschau-Schriftmetriken, das erneute Öffnen der PowerPoint-Dateien, Komponentennamen und Sprechernotizen. Ein SHA-256-Vergleich stellt sicher, dass die Hauptpräsentation unverändert bleibt; `validation.json` enthält das Ergebnis und die Fingerabdrücke der verwendeten Quellen. Die Vorschauen wurden außerdem visuell geprüft.

PNG und PDF entstehen mit dem vorhandenen lokalen Pillow-Renderer. PowerPoint kann Arial geringfügig anders umbrechen; die PowerPoint-Dateien bleiben die editierbaren Originale. Es wurden keine Cloud-Läufe gestartet und keine Implementierungen verändert.
