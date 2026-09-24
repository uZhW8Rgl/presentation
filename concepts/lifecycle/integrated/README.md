# Infrastructure integrated into the DFL workflow

Current proposal deck: `VITA-FL_Lifecycle_Integrated_DFL.pptx`.

- **F1 — Workflow ring:** training → aggregation → IPFS model storage → blockchain finalization → next round.
- **F2 — Functional links:** direct worker updates, global-model store/load loop through IPFS, and explicit blockchain coordination/commit links.
- **F3 — Publication arc:** the global-model section of the circle combines IPFS files and blockchain references; publication and loading close the training cycle.

Prototype check: workers send encrypted local updates directly over authenticated
HTTPS to the current aggregator. **Local updates are not routed via IPFS.**
The aggregator publishes the global-model bundle in IPFS and finalizes its references
on blockchain. Workers load that model for the next round. Relevant implementation:

- `vita-fl/dfl/node_server/src/server.ts`: `uploadLocalModel`, accepted submission commitments, aggregation.
- `vita-fl/dfl/node_server/src/ipfs.ts`: global-model upload/finalization and download.
- `vita-fl/smart_contracts/src/core/GMStorage.sol`: finalization and round advancement.
- `vita-fl/smart_contracts/src/core/AggregatorSelection.sol`: next aggregator selection.

F1 uses workflow arrows: the IPFS-to-blockchain transition means the aggregator
registers CIDs, not that IPFS submits a transaction or sends model weights to the chain.
Its next-round transition includes reference resolution and artifact retrieval.
F2 shows principal information directions. F3 abstracts publication/retrieval as a
paired segment. Additional details and trust boundaries are explained in slide notes.
The inference service receives model information; the agent invokes it through MCP.
The transparency log remains separate from blockchain.

All diagrams are editable PowerPoint shapes. PNGs are approximate layout previews.
**F3 is approved and included as Page 9 in the main presentation**, directly
before the detailed architecture on Page 10. Its editable source asset is
`presentation/assets/lifecycle-f3.pptx`. Original A and earlier proposals remain available.

Regenerate from `presentation`:

```bash
.venv/bin/python concepts/lifecycle/integrated/build_integrated.py
```
