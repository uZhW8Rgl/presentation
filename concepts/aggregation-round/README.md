# Vorschläge für Folie 18: Aggregation verständlicher darstellen

- [Übersicht](overview.png)
- [Editierbare PowerPoint](VITA-FL_Aggregation_Round_Alternatives.pptx)
- [PDF](VITA-FL_Aggregation_Round_Alternatives.pdf)

## Entwürfe

| Variante | PNG | Idee |
|---|---|---|
| A | [Zuständigkeiten und Nachrichten](a-actors-and-messages.png) | Worker, Aggregator-TEE, IPFS und Blockchain zeigen den tatsächlichen Ablauf. |
| B | [Modellfluss](b-model-flow.png) | Drei beispielhafte, geprüfte Modelle müssen vollständig in den Mittelwert eingehen; danach folgen Speicherung und Finalisierung. |
| C | [Signierte Aggregationsaussage](c-signed-statement.png) | Macht sichtbar, wie Eingabemenge, Regel, Ergebnis und IPFS-Verweise zusammengebunden werden. |

Variante A wurde ohne die Nummerierung 1–4 als Folie 18 in die Hauptpräsentation
übernommen. Die Pfeile zeigen den Ablauf. Die editierbare Quelle liegt unabhängig
von diesem Ordner unter `assets/aggregation-round-a.pptx`. B und C bleiben als
Alternativen erhalten. Die Entwürfe zeigen reguläre Trainingsrunden; der
Bootstrap-Sonderfall steht in den Notizen.

## Wesentliche Codebefunde

1. Lokale Modelle gehen direkt per authentisiertem HTTPS an den Aggregator.
   Der Empfänger prüft Signaturen und Hashes; signierte Worker-Commitments
   werden in `GMStorage` erfasst.
2. `closeModelSubmissions` setzt eine ausreichende Zahl akzeptierter Eingaben
   voraus und schließt die Menge ab. `inputRoot` ist ein fortlaufender Keccak-Hash
   in Annahmereihenfolge, kein Merkle-Root. Die Folien nennen ihn verständlicher
   „input fingerprint“.
3. Der Aggregator prüft, dass Dateien und Hashes zu den On-chain-Einträgen
   passen und die lokale Anzahl exakt mit der festgeschriebenen Anzahl
   übereinstimmt. FedAvg mittelt jeden Modellparameter mit gleichem Gewicht.
4. Das verschlüsselte globale Modell, seine Signatur und das Empfänger-
   Schlüsselpaket werden zuerst auf IPFS veröffentlicht. Danach liegen die
   drei CIDs für die signierte Aggregationsaussage vor.
5. Der registrierte Action-Key signiert die EIP-712-Aussage über Runde,
   Aggregator, Eingabefingerabdruck/-anzahl, Regel/Policy, Ausgabehashes,
   Veröffentlichung und Nonce. RSA-Modellsignatur und Action-Signatur
   erfüllen unterschiedliche Aufgaben.
6. `GMStorage.finalizeRoundWithAggregation` prüft Autorisierung und Signatur,
   bindet sie an den festgeschriebenen Kontext und veröffentlicht die neuen
   Modellreferenzen zusammen mit dem Rundenwechsel in einer Transaktion.
   Die Blockchain berechnet FedAvg nicht erneut. IPFS-Upload und spätere
   Aggregatorauswahl sind außerhalb dieser atomaren Transaktion.

Quellen:

- `vita-fl/dfl/node_server/src/server.ts:625–702,1310–1365,1930–2004,2229–2330,2786–2828`
- `vita-fl/dfl/neural_network/cli.py:1248–1320`
- `vita-fl/dfl/node_server/src/ipfs.ts:300–367`
- `vita-fl/dfl/node_server/src/bc_client.ts:542–650`
- `vita-fl/smart_contracts/src/core/GMStorage.sol:180–248,294–373`
- `vita-fl/smart_contracts/src/core/AggregationPolicy.sol:16,203–215,260–305`
- `vita-fl/smart_contracts/src/core/AggregatorSelection.sol:169–195`

## Erzeugen

Aus `presentation/`:

```bash
.venv/bin/python concepts/aggregation-round/build_designs.py
```

Alle Diagrammelemente sind native PowerPoint-Formen. Geprüft werden Foliengrenzen,
Textumbruch und der unveränderte Hash der Hauptpräsentation. PNG/PDF dienen als
Layoutvorschau; die endgültige Textdarstellung hängt von PowerPoint ab.
