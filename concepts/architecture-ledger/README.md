# Folie 6: Ledger und IPFS als gemeinsamer Farbbereich

Zwei Layoutentwürfe zur Architekturfolie. Der freigegebene **Entwurf A** wurde
am 8. September 2026 als Folie 6 in das Hauptdeck und dessen Vorschau übernommen.
Die Galerie bleibt als Vergleich erhalten; ihr Generator schreibt nur die
Entwurfsdateien und verändert das Hauptdeck nicht.

- [Entwurf A: Infrastruktur in der Mitte](draft-a.png)
- [Entwurf B: Infrastrukturband unter den zwei Blöcken](draft-b.png)
- [Beide Entwürfe als editierbare PowerPoint](VITA-FL_Slide06_Architecture_Drafts.pptx)
- [Beide Entwürfe als PDF](VITA-FL_Slide06_Architecture_Drafts.pdf)

**A** zeigt den Weg von links nach rechts. Die DFL-Seite publiziert
Modellreferenz und Modellartefakte; Ledger und IPFS stehen gemeinsam in einer
violetten Spalte. Zwei getrennte violette Pfeile führen zum Receiver TEE.
Zwei überlappende schwarze, gestrichelte Rahmen umfassen DFL + Blockchain/IPFS
und Blockchain/IPFS + Agent/Inference. Die leicht versetzten Ober- und
Unterkanten machen beide Gruppierungen sichtbar; Blockchain/IPFS liegt in
beiden Rahmen. Die bestehenden Komponenten und Pfeile bleiben erhalten.
Die grünen und blauen Abschlusssätze stehen unterhalb der jeweiligen
Farbflächen, aber innerhalb der gestrichelten Rahmen. Dafür sind die grünen
und blauen Farbflächen in der Höhe verkürzt; die violette Fläche bleibt bestehen.

**B** erhält die beiden Verantwortungsblöcke oben und stellt Blockchain/IPFS
als gemeinsame Infrastruktur darunter dar. Die beschrifteten violetten
Verbindungen treffen an getrennten Punkten auf den Receiver TEE.

In beiden Varianten entspricht die Farbzuordnung der gewählten Fußzeile:
DFL grün, Blockchain/IPFS violett, Agent/MCP/Inference/Log blau. Die Fußzeile
behält ihre Reihenfolge und den weißen Rahmen; alle drei Bereiche sind aktiv.

## Bedeutung der Verbindungen

| Verbindung | Bedeutung |
|---|---|
| Ledger → Receiver TEE | Finalisierte Modellreferenz mit CIDs, Runde und Publisher-Key |
| IPFS → Receiver TEE | Signiertes, verschlüsseltes Modellbundle und zugehörige Artefakte |

Der Receiver initiiert die Auflösung und das Laden selbst. Die Pfeilspitzen
zeigen den Informationsfluss zum Receiver. Ein Ledger→IPFS-Datenpfeil entfällt,
weil die Blockchain keine Modelldateien zu IPFS hochlädt.

Lokale Codebelege:
[`tee_inference/service/model_source.py`](../../../vita-fl/tee_inference/service/model_source.py)
ab Zeile 218 sowie
[`agent/blockchain_source.py`](../../../vita-fl/agent/blockchain_source.py)
ab Zeilen 354 und 544. Die Details stehen auch in den PowerPoint-Notizen.

## Erzeugung und Prüfung

```bash
presentation/.venv/bin/python presentation/concepts/architecture-ledger/build_drafts.py
```

Der Generator prüft Textflächen und Foliengrenzen, die violette Ledger-Farbe
sowie beide violetten Receiver-Verbindungen mit Pfeilspitzen. Dateihashes
stellen sicher, dass beim Erzeugen der Entwürfe Hauptdeck und Hauptvorschauen
unverändert bleiben.
PNG und PDF sind lokale Layoutvorschauen; Diagramme und Texte in der PPTX
sind native, editierbare PowerPoint-Elemente.
