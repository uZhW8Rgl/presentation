# Attack Trees – Look B auf hellem Grund

Sechs editierbare Folienvorschläge. **Alle sechs wurden gegen die Implementierung und die tatsächlich erforderlichen Angreiferrechte geprüft.** Die Prüfung ließ Kapitel 4, Hauptpräsentation und Anwendungscode unverändert. Anschließend wurden die sechs freigegebenen Folien auf **Seiten 24–29 der [Hauptpräsentation](../../../VITA-FL_Thesis_Presentation_TU_Berlin.pptx)** integriert; Kapitel 4 und Anwendungscode bleiben unverändert.

[Galerie](index.html) · [PowerPoint](VITA-FL_Attack_Trees_B_Light.pptx) · [PDF](VITA-FL_Attack_Trees_B_Light.pdf) · [Übersicht](overview.png) · [Prüfergebnis mit Codebelegen](implementation-review.md)

Die rechten Blätter bleiben kurze Stichworte. Vollständige Bedingungen, Akteur, erforderliche Schlüssel und Codebelege stehen in `trees.json`, Sprechernotizen und Galeriedetails. Ein Betreiber, ein logisch registrierter Teilnehmer und der tatsächlich signierende TEE-Prozess werden ausdrücklich unterschieden.

## Ergebnis je Folie

| Folie | Geprüfte Angriffspfade | Bewertung des dargestellten Root-Ziels |
| --- | --- | --- |
| [1 – Zulassung](01-admission.png) | Unzulässiges Image, fremde Quote anders binden, aufgezeichnete Registrierung/Rundenaktion wiederholen. Kein stillschweigend angenommener Zugriff auf alte Schlüssel. | **Grün:** die gezeigten externen Versuche scheitern an Roster, Enrollment, Quote, Image/Policy, Nonce und Kontext. |
| [2 – Modellintegrität](02-model.png) | Externe Sample-/Artefaktmanipulation getrennt von absichtlich falscher Aggregation und frei gewählten schädlichen Updates. Letztere verlangen Kontrolle des zugelassenen Prozesses beziehungsweise aller erforderlichen Signierbefugnisse. | **Gelb:** die gezeigten erfolgreichen Manipulationen im bestehenden Run setzen eine Verletzung der geschützten Ausführung/Schlüsselverwahrung voraus. Keine Aussage über statistische Modellrobustheit. |
| [3 – Runden und Recovery](03-recovery.png) | Unautorisierte Reports grün; kompromittierte aktuelle Quorum-Signer gelb; tatsächliche Netzstörung mit ehrlichen Timeoutreports und blockierte Recovery rot. | **Rot:** Verfügbarkeit kann ohne TEE-Schlüssel gestört werden. Korrekte Abwahl eines isolierten Aggregators ist keine gefälschte Meldung. |
| [4 – Inferenz](04-inference.png) | Alte Modellobjekte, fremde Outputs/Receipts und Promptversuche gegen den technischen Verifikationsstatus. | **Grün:** die gezeigten Versuche erzeugen keinen gültigen technischen Erfolgsstatus. Kein Versprechen über beliebigen LLM-Text oder das bei jedem Aufruf allerneueste Modell. |
| [5 – Audit und Interaktion](05-audit.png) | Fehlende Evidence als technischen Erfolg ausgeben grün; signierte Split Views durch kontrollierten Logdienst gelb; Requests/Antworten unterdrücken rot. | **Rot:** Interaktionsunterdrückung braucht keinen Signaturschlüssel. Gültige widersprüchliche Logstatements brauchen dagegen Log-Signierautorität. |
| [6 – Modelloffenlegung](06-disclosure.png) | Entschlüsselung ohne Empfängerschlüssel grün; tatsächliche TEE-Schlüsselextraktion, privilegierter Gastzugriff oder unerlaubte Freigabe alter Geheimnisse an veränderten Code gelb. | **Gelb:** die TEE ist Empfänger, ihr menschlicher Betreiber erhält dadurch keinen Klartextzugriff. |

## Farben und Logik

Dieselbe Legende steht auf jeder Folie und gilt auf allen Ebenen. Blau ist entfernt; Navigation und AND/OR-Verknüpfungen bleiben neutral.

| Farbe | Bedeutung |
| --- | --- |
| **Rot – Possible in threat model** | Der genannte externe Akteur kann den dargestellten Verfügbarkeitsverlust mit der ausdrücklich genannten Fähigkeit verursachen. Kein stillschweigend vorausgesetzter TEE-Schlüsselzugriff und kein experimentell bestätigter Angriff. |
| **Gelb – Assumption boundary** | Eine konkret benannte Grenze der geschützten Ausführung, Schlüsselverwahrung oder vertrauenswürdigen Dienste ist betroffen. Ein lediglich unbekannter Sachverhalt oder eine zukünftige Funktion genügt dafür nicht. |
| **Grün – Blocked under assumptions** | Der gezeigte Angriff wird durch die intakte geprüfte Implementierung unter den genannten Annahmen blockiert. Keine pauschale Sicherheitsgarantie. |
| **Weiß – Action / condition** | Handlung, Angreiferfähigkeit oder notwendige Bedingung. Weiß bedeutet nicht, dass jeder externe Angreifer diese Fähigkeit besitzt. |

**OR:** Ein roter Weg macht das Elternziel rot; sonst ein gelber Weg gelb; nur ausschließlich blockierte Wege ergeben grün. **AND:** Eine blockierte notwendige Bedingung macht den Pfad grün; sonst eine notwendige Annahmegrenze gelb; sonst ein roter Effekt rot. Reine Voraussetzungskombinationen bleiben weiß. Die Kanten sind Zielzerlegung, keine zeitliche Reihenfolge. Ein grüner Knoten benennt weiterhin das hypothetische Angreiferziel, dessen Erfolg blockiert ist.

Die Bäume umfassen ausgewählte Pfade, keine vollständige Aufzählung aller Bedrohungen. Insbesondere macht die gelbe Modellfolie das Modell nicht statistisch sicher: semantisch falsche, korrekt autorisierte Daten und erlaubte Trainingskonfiguration bleiben eigene Analysegegenstände.

## Dateien und Prüfung

`trees.json` enthält Kapitel-Verweise, konkrete Codequellen mit Hashes, jede Angreiferfähigkeit und erforderliche Autorität. `build.py` prüft Quellen, Farbverknüpfung, Metadaten, Layout und PPTX-Roundtrip. Kapitel 4 und Hauptdeck werden vor/nach dem Build gehasht. Die Codeprüfung war statisch; es wurden keine Angriffe, Cloud-Läufe oder neuen Sicherheitstests ausgeführt.

Rebuild aus `presentation`:

```bash
.venv/bin/python concepts/attack-trees/revision-b-light/build.py
```

Native PowerPoint-Knoten, Texte und Verbindungen; PNG/PDF mit dem vorhandenen Pillow-Renderer. PowerPoint kann Schriften geringfügig anders umbrechen. Details der Prüfungen stehen in [validation.json](validation.json).
