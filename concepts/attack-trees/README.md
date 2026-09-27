# Attack Trees aus Kapitel 4 – vier Themen, drei Looks

> **Aktuelle Überarbeitung:** [B auf hellem Grund mit sechs vertieften Bäumen](revision-b-light/index.html) · [PowerPoint](revision-b-light/VITA-FL_Attack_Trees_B_Light.pptx) · [Inhalt und Quellen](revision-b-light/README.md). Die folgenden zwölf Folien sind die ursprünglichen Designvarianten.

Zwölf editierbare Folienvorschläge: vier aus dem Bedrohungskatalog abgeleitete Attack Trees, jeweils in drei visuellen Varianten. Die englische Sprache, das TU-Berlin-Template und die DFL-/Agent-Kennzeichnung entsprechen der Präsentation. **Kapitel 4 und die Hauptpräsentation wurden nicht verändert.**

[Interaktive Galerie: Thema und Look wählen](index.html) · [Looks vergleichen](looks-overview.png) · [Vier Themen vergleichen](trees-overview.png) · [Alle zwölf Folien als PowerPoint](VITA-FL_Attack_Tree_Alternatives.pptx) · [PDF-Vorschau](VITA-FL_Attack_Tree_Alternatives.pdf)

## Die drei Looks

| Look | Gestaltung | Einsatz | PowerPoint |
| --- | --- | --- | --- |
| **A – Klassischer Baum** | Rotes Angreiferziel oben, neutrale Teilziele, klare OR-/AND-Knoten. | **Empfehlung für die formale, gut nachvollziehbare Darstellung der Bäume.** | [Vier Bäume in Look A](VITA-FL_Attack_Trees_A_classic.pptx) |
| **B – Horizontal** | Ziel links, Verzweigungen nach rechts, dunkler Hintergrund mit hellen Knoten. | Visuell deutlich andere Alternative; gut zum schrittweisen Erklären. | [Vier Bäume in Look B](VITA-FL_Attack_Trees_B_horizontal.pptx) |
| **C – Mit Einordnung** | Drei Pfadbereiche mit getrennten Hinweisen auf Anforderungen und Grenzen. | **Empfehlung, wenn im Vortrag auch Kontrollen und Restrisiken besprochen werden.** | [Vier Bäume in Look C](VITA-FL_Attack_Trees_C_annotated.pptx) |

Die Inhalte und logischen Verknüpfungen bleiben über die Looks hinweg gleich. Die Look-Übersicht verwendet denselben Verfügbarkeitsbaum, damit sich die Darstellung direkt vergleichen lässt.

## Vier Angriffsziele

| Baum | Angreiferziel und Zerlegung | Threats aus Kapitel 4 | Vorschauen |
| --- | --- | --- | --- |
| **1 – Training und Modellintegrität** | Autorität missbrauchen, Trainingsdaten verfälschen oder die Veröffentlichung verändern. | T1, T2, T3, T4, T6, T7, T14 | [A](a-training.png) · [B](b-training.png) · [C](c-training.png) |
| **2 – Inferenz und Agent** | Ein falsch gebundenes oder ungeprüftes Ergebnis akzeptieren lassen: Objekte substituieren, frühere Kontexte wiederverwenden oder den Agenten manipulieren. | T2, T8, T9 | [A](a-inference.png) · [B](b-inference.png) · [C](c-inference.png) |
| **3 – Verfügbarkeit und Auditspur** | Fortschritt stoppen, Ergebnisse/Belege unterdrücken oder eine unberechtigte Recovery erzwingen. | T6, T10, T11, T12, T14 | [A](a-availability.png) · [B](b-availability.png) · [C](c-availability.png) |
| **4 – Modelle, Schlüssel und Vertrauenswurzeln** | Vertrauliche Daten erhalten, Schlüssel kompromittieren oder kryptografische, Plattform- und Governance-Annahmen brechen. | T5, T13, T14 | [A](a-confidentiality.png) · [B](b-confidentiality.png) · [C](c-confidentiality.png) |

Gemeinsam verweisen die Bäume auf alle **T1–T14**. Einzelne Threats erscheinen mehrfach, weil sie verschiedene Phasen betreffen. T6 hat beispielsweise sowohl einen Integritätsaspekt (akzeptiertes Update auslassen) als auch einen Verfügbarkeitsaspekt (nicht veröffentlichen). Die kompakte Darstellung ist keine vollständige Aufzählung sämtlicher Ausprägungen jedes Threats.

## Logik und Aussagegrenzen

- **OR:** Ein Kind genügt für das dargestellte Elternziel.
- **AND:** Alle Kindbedingungen müssen gemeinsam erfüllt sein. Beim Kollusionspfad müssen dieselben zulässigen Reports die Meldeschwelle erreichen und fälschlich den Ausfall des gesunden Aggregators behaupten. Eine erreichte Schwelle kann allein auch berechtigte Recovery bedeuten; falsche Meldungen allein können unterhalb der Schwelle bleiben.
- Die Kanten zeigen eine **Zielzerlegung**, keine zeitliche Reihenfolge und keinen Nachrichtenfluss.
- Die Blätter formulieren hypothetisch erreichte Teilziele. Ein Replay-Versuch allein wird beispielsweise nicht mit erfolgreicher Annahme gleichgesetzt: Das Blatt lautet „Get stale authority or updates accepted“.
- Bei der falschen Abwahl müssen die Reports dieselbe aktuelle Runde und denselben Aggregator betreffen und die sonstigen Vertragsbedingungen einschließlich Berechtigung und Zeitbedingungen erfüllen. Diese Voraussetzungen stehen in den Sprechernotizen.
- **F/NF-Kennungen** nennen Anforderungen aus Kapitel 4. Sie sind keine Aussage über nachgewiesene Implementierung, getestete Abwehr oder formale Sicherheit. In Look C stehen diese Hinweise außerhalb der Baumkanten.
- **Amber** markiert einen expliziten Restrisiko- oder Annahmebereich; die Farbe ist kein berechneter Risikowert. Gültig signierte vergiftete Daten, fehlende unabhängige Log-Witnesses, anhaltende Infrastruktur-Ausfälle und Vertrauenswurzel-Kompromisse bleiben abgegrenzt.
- Kapitel 4 enthält Use-/Misuse-Diagramme und einen Bedrohungskatalog. Die hier gezeigten Attack Trees sind eine **abgeleitete Präsentationsdarstellung**, keine unveränderten Abbildungen aus dem Kapitel.
- Der Kapitelstand beschreibt seine eigenen Attestations- und Replay-Grenzen. Neuere Implementierungsänderungen und externe Receipt-Audits werden diesem Stand nicht rückwirkend zugeschrieben.

Die vollständigen Modellierungsbegründungen, Assets, Anforderungen und Annahmen stehen pro Baum in den Sprechernotizen und in [trees.json](trees.json). Der genaue Quellstand und die Zeilenanfänge der T-Einträge stehen in [source-map.json](source-map.json).

## Dateien erzeugen und prüfen

Aus dem Verzeichnis `presentation`:

```bash
.venv/bin/python concepts/attack-trees/build_designs.py
```

Der Generator erstellt zwölf native PowerPoint-Folien, drei Decks mit je vier Bäumen, zwölf Einzelvorschauen, zwei Übersichten, PDF und eine lokale HTML-Galerie. Knoten, Beschriftungen und Verbindungen bleiben in PowerPoint editierbar.

Geprüft werden Threat-/Requirement-/Assumption-Referenzen, die Baumstruktur, vollständige T1–T14-Zuordnung, Objektgrenzen, Textumbruch und das erneute Öffnen der PowerPoint-Dateien. SHA-256-Vergleiche kontrollieren, dass Hauptpräsentation und Kapitel 4 unverändert bleiben. Die Vorschauen wurden visuell geprüft. `validation.json` enthält das Ergebnis.

Die Vorschauen entstehen mit dem vorhandenen Pillow-Renderer. PowerPoint kann Arial geringfügig anders umbrechen; die PPTX-Dateien bleiben die editierbaren Originale. Es wurden keine Tests, Angriffe oder Cloud-Läufe ausgeführt.
