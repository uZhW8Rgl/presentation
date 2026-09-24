# Alternativen für Folie 15: dstack-Schlüssel und ihre Verwendung

Vier unterschiedliche, editierbare Entwürfe. Die Hauptpräsentation bleibt bis
zur Auswahl unverändert.

- [Gesamtübersicht](overview.png)
- [PowerPoint mit vier Entwürfen](VITA-FL_Dstack_Key_Usage_Alternatives.pptx)
- [PDF](VITA-FL_Dstack_Key_Usage_Alternatives.pdf)

## Varianten

| Variante | Vorschau | Schwerpunkt |
|---|---|---|
| A | [Schlüssel → Verwendung](a-key-use-lanes.png) | Drei horizontale Wege; Herkunft, Schlüssel und Aufgaben direkt verbunden. |
| B | [Schlüssel im Ablauf](b-lifecycle-uses.png) | DFL koordinieren, Modelle austauschen, Modellnutzung nachweisen; Schlüssel stehen bei ihren Aufgaben. |
| C | [RSA-Schutz und Modellzugriff](c-model-key-custody.png) | Unterscheidet den abgeleiteten Versiegelungsschlüssel, den zufälligen RSA-Schlüssel und die Modellschlüssel. |
| D | [Akteure und Nachrichten](d-actor-map.png) | Worker-TEE, Blockchain, Modellempfänger, Transparenzlog und Agent; Schlüssel bei den Nachrichten. |

## Inhaltliche Präzisierungen

- **secp256k1:** signiert Update-Commitments, Aggregationsaussagen und
  Protokolltransaktionen.
- **Abgeleiteter AES-256-GCM-Schlüssel:** versiegelt den privaten RSA-Schlüssel
  für die Speicherung und stellt ihn aus erhaltenem Zustand wieder her.
- **Zufälliger RSA-3072-Schlüssel:** signiert Modellpakete und entschlüsselt
  deren symmetrische Transportschlüssel. Die Modellbytes werden mit frischen
  symmetrischen Schlüsseln verschlüsselt.
- **Separate Ed25519-Schlüssel:** Sello signiert Tool-Receipts, die im
  Transparenzlog aufgezeichnet werden; AIR signiert Inferenznachweise, die
  der Agent gegen Modell, Anfrage und Ergebnis prüft.
- Registrierung bindet öffentliche Action-, RSA- und Sello-Identitäten.
  AIR besitzt eine eigene Bindung im Inferenz-Quote. Das Transparenzlog
  bestätigt Aufzeichnung, nicht eigenständig die Berechnung.

Quellen im lokalen Prototyp:

- `vita-fl/dfl/node_server/src/action_key.ts:65–121`
- `vita-fl/dfl/node_server/src/bc_client.ts:219–249,542–650,676–749`
- `vita-fl/dfl/node_server/src/participant_key.ts:81–96,178–200,253–286`
- `vita-fl/dfl/node_server/src/server.ts:493–511`
- `vita-fl/dfl/node_server/src/gm_crypto.ts:178–213,278–303`
- `vita-fl/dfl/neural_network/cli.py:1117–1165`
- `vita-fl/agent_receipts/sello_v1.py:189–217`
- `vita-fl/tee_inference/service/app.py:128–142`
- `vita-fl/tee_inference/service/attestation.py:56–104`
- `vita-fl/agent/sello_client.py:60–68,119–149`
- `vita-fl/agent/tee_inference_client.py:530–609`
- `vita-fl/smart_contracts/src/core/DeviceRegistry.sol:437–465`

## Erzeugen

Aus `presentation/`:

```bash
.venv/bin/python concepts/dstack-key-usage/build_designs.py
```

Die Diagramme bestehen aus editierbaren PowerPoint-Formen. Der Generator prüft
Textumbrüche und Foliengrenzen und bestätigt, dass die Hauptpräsentation
unverändert bleibt. PNG und PDF sind lokale Layoutvorschauen.
