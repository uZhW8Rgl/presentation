# Sello and AIR — tasks and guarantees on one slide

Four alternative **combined single slides**, each covering Sello and AIR together.
The slide text is English, matching the thesis presentation. All diagrams and
labels are native, editable PowerPoint objects. Detailed technical explanations,
source references and implementation limits are in the speaker notes.

| Variant | Visual approach | Useful for | Preview | Editable single slide |
|---|---|---|---|---|
| A | Direct comparison: three guarantees per evidence layer | The clearest first explanation of responsibilities | [PNG](a-two-evidence-layers.png) | [PPTX](a-two-evidence-layers.pptx) |
| B | Four-stage workflow | Showing authorization, evidence creation, sealing and verification in context | [PNG](b-verification-workflow.png) | [PPTX](b-verification-workflow.pptx) |
| C | Spatial map of the checking scopes | Explaining how numeric-inference evidence fits inside a tool interaction | [PNG](c-checking-scopes.png) | [PPTX](c-checking-scopes.pptx) |
| D | Scenario / check / enforced outcome matrix | Explaining exactly what kinds of substitution or policy mismatch are detected | [PNG](d-detected-changes.png) | [PPTX](d-detected-changes.pptx) |

[All four slides — PowerPoint](VITA-FL_Sello_AIR_Guarantees.pptx) ·
[PDF preview](VITA-FL_Sello_AIR_Guarantees.pdf) ·
[Overview](overview.png) · [Browser gallery](index.html)

**Approved variant A** is integrated as Page 20 of the
[main presentation](../../../VITA-FL_Thesis_Presentation_TU_Berlin.pptx), replacing
the earlier Sello-only slide. The independent
[editable asset](../../../assets/sello-air-a.pptx) makes this choice reproducible.
Its AIR caption is **Attested Inference Receipt**; visible labels use **Inference
TEE** and **Transparency Log**. A omits the visible scope sentence and preserves
the technical qualifications in its notes. On the main slide, **Agent** is active
and **DFL** is gray. The main deck remains at forty-four pages.

## Content covered

- **AIR data integrity:** Ed25519 signature and hashes of the model manifest,
  exact numeric input, inference result and quote.
- **AIR quote binding:** REPORTDATA binds the AIR signing key, manifest and
  request. The AIR signature binds the result.
- **AIR configuration:** ordered RTMR3 replay, measured Compose, image digest,
  and the configured chain, contracts and RPC trust inputs.
- **Sello authorization:** mTLS and token identity/audience/scope/certificate/
  expiry checks, with jobs bound to the authenticated agent.
- **Sello response evidence:** receiver signature over action, input/output
  commitments, token reference and result status; checked against the call.
- **Sello privacy:** HPKE encryption of the receipt body for the owner.
- **Publication:** receiver publishes Sello before returning success; the agent
  verifies publication, checks AIR and separately registers its evidence bundle.

Colour assignment follows the existing deck's domains: blue for tool interaction,
green for numeric DFL-model inference, purple for logging. The nested regions in
C describe checking scopes; the AIR bundle is not inside Sello's encrypted body.

## Assurance boundary

These slides describe the implementation reviewed in the conversation, before
the proposed RA-TLS and Phala verification API additions. The speaker notes
record that per-inference Intel quote verification is absent and that TEE trust
relies on prior worker admission. Variants B–D also display this scope on the
slide. They do not claim independent mathematical proof of inference correctness.

The notes preserve further qualifications: receiver-generated AIR nonce, no
exactly-once protection, incomplete measurement-map reconciliation, owner keys
inside the agent runtime, unencrypted input/output in the separately logged AIR
bundle, and the SCITT prototype's single virtual node, development TLS, unpinned
log keys, ephemeral Phala storage and missing independent witnesses. A log failure
withholds a successful verified response but does not roll back computation.

## Source and implementation references

- Figuera, **Notarized Agents: Receiver-Attested Confidential Receipts for AI
  Agent Actions** (2026), [arXiv:2606.04193](https://arxiv.org/abs/2606.04193).
- Tsyrulnikov, **Attested Inference Receipt (AIR)**,
  [Internet-Draft 02](https://www.ietf.org/archive/id/draft-tsyrulnikov-rats-attested-inference-receipt-02.html).
- [Prior source/implementation comparison](../README.md).
- [AIR emission](../../../../vita-fl/tee_inference/service/attestation.py),
  [AIR checks and publication](../../../../vita-fl/agent/tee_inference_client.py).
- [Sello receipt](../../../../vita-fl/agent_receipts/sello_v1.py),
  [owner checks](../../../../vita-fl/agent/sello_client.py),
  [authorization and publication-before-response](../../../../vita-fl/tee_inference/service/app.py).

## Rebuild and validation

From `presentation/`:

```sh
.venv/bin/python concepts/sello-air/guarantees/build.py
```

The builder checks text bounds, duplicate shape IDs, source links, speaker-note
coverage, round-trip PPTX loading and the main deck's unchanged SHA-256. It exports
four individual PPTX/PNG files, a combined PPTX, a PDF preview, a contact sheet and
a local HTML gallery. The generated PNGs were visually reviewed.

PNG/PDF previews use the existing Pillow layout renderer. PowerPoint remains
authoritative for exact Arial metrics and rendering; no Office renderer is
available in this workspace. The alternatives deck remains separate; approved
variant A is also included in the main presentation as described above.
