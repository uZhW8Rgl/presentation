# Sello and AIR — slide proposals

Six editable English slides: three alternatives for Sello and three for AIR.
The two selections can be mixed. Source links appear on the slides; detailed
implementation notes and qualifications are in each slide's speaker notes.

## Visual choices

| Variant | Emphasis | Sello | AIR |
|---|---|---|---|
| A — Flow | Explain actors and evidence movement | [Preview](a-sello-flow.png) | [Preview](a-air-flow.png) |
| B — Comparison | Map the cited contribution to VITA-FL | [Preview](b-sello-comparison.png) | [Preview](b-air-comparison.png) |
| C — Contents | Distinguish the receipt from its surrounding evidence | [Preview](c-sello-receipt.png) | [Preview](c-air-bundle.png) |

**B** gives the clearest comparison for a research presentation. **A** emphasizes
the operational sequence; **C** gives more room to receipt and bundle contents.

- [All six previews](overview.png)
- [Browser gallery](index.html)
- [Editable PowerPoint](VITA-FL_Sello_AIR_Alternatives.pptx)
- [Preview PDF](VITA-FL_Sello_AIR_Alternatives.pdf)

## Sources

- Juan Figuera, **Notarized Agents: Receiver-Attested Confidential Receipts for
  AI Agent Actions**, 2026, [arXiv:2606.04193v1](https://arxiv.org/html/2606.04193v1).
  The paper motivates a receiver-produced, owner-encrypted audit trail. Sections
  3–4 describe the protocol and identity/log roles. This is the thesis's
  `figuera2026notarized` reference.
- B. Tsyrulnikov, **Attested Inference Receipt (AIR)**,
  [Internet-Draft 02](https://www.ietf.org/archive/id/draft-tsyrulnikov-rats-attested-inference-receipt-02.html),
  July 2026. Sections 4, 7.3, 8, 9.3 and 11.4 cover format, assurance, receipt
  validation, transparency integration and replay. Labelled as a draft throughout.

## Implementation snapshot and deviations

Checked against local VITA-FL code on **23 September 2026**, including the new
mandatory Sello and mTLS changes. This describes implemented code, not a claim
that a new version has been deployed or quantitatively evaluated.

### Sello

The receiver hashes canonical tool input and its raw response, encrypts the
receipt body for the configured owner, signs it, publishes it to SCITT and
returns it with an inclusion reference. The agent verifies and decrypts it.
The fixed calls are model fetch, image selection and inference. The last call's
input is a `job_id` object; the medical image pixels belong to the separate AIR
evidence bundle. A failed log publication returns an error even if computation
has already occurred; the prototype does not roll back that computation.

VITA-FL binds the receiver signing key and endpoint to Worker 0's on-chain
admission. It derives that key through a dedicated dstack context. Additional
access checks require mTLS and a short-lived token bound to audience, scopes,
subject and client-certificate Digest. A random token identifier is not consumed
as a one-use credential and does not bind a unique request body.

The prototype does not reproduce the source's complete trust boundary:

- One SCITT/CCF Virtual Mode node; no independent log witnesses or gossip.
- Publication bundles are retrieved by response reference; no independent
  owner discovery indexed by token reference.
- Owner decryption key and token issuer seed reside in the agent service.
  Compromise of that runtime therefore also exposes the owner capability.
- Log verification material is fetched from the configured endpoint rather
  than an independently pinned trust anchor. Historical receiver-key auditing
  requires preserving the relevant registry state.

Code: [`sello_v1.py`](../../../vita-fl/agent_receipts/sello_v1.py),
[`environment.py`](../../../vita-fl/agent_receipts/environment.py),
[`receiver_log.py`](../../../vita-fl/agent_receipts/receiver_log.py),
[`sello_client.py`](../../../vita-fl/agent/sello_client.py),
[`app.py`](../../../vita-fl/tee_inference/service/app.py),
[`peer.py`](../../../vita-fl/transport_security/peer.py).

### AIR-style evidence

The receiver signs deterministic CBOR commitments to the DFL manifest, exact
numeric request, prediction response and per-call quote. The manifest binds a
separately available model artifact; the receipt does not contain model weights.
A dedicated dstack-derived Ed25519 key is distinct from Sello and TLS keys.
Two portions of TDX REPORTDATA bind the signing key/manifest and request.

The returned VITA-FL bundle adds original numeric bytes, the manifest, quote,
receipt/key, REPORTDATA, exact Compose and ordered event log. The agent checks
receipt bindings, RTMR3 replay, Image Digest and deployment policy, then publishes
the full bundle to SCITT. That bundle includes unencrypted input pixels. It is
evidence about numeric DFL-model inference, not the agent's LLM reasoning.

The slides deliberately use **AIR-style**:

- `dcap_collateral_verified=False`: the agent does not authenticate each
  individual quote's Intel signature, certification chain or collateral.
  Hardware attribution relies on separately admitted Worker 0 and its
  registry-bound Sello identity.
- The receiver supplies the nonce. The 300-second recentness check, with
  30-second skew, is not verifier-challenge or seen-`cti` replay protection.
- The verifier does not reconcile every signed measurement-map field with
  quote registers. RTMR3 replay is a separate explicit comparison.
- The REPORTDATA construction is prototype-specific, not the draft's exact
  illustrated construction. DFL provenance and full-bundle SCITT publication
  are integration choices, not additions claimed to be invented by VITA-FL.

Code: [`attestation.py`](../../../vita-fl/tee_inference/service/attestation.py),
[`AIR profile`](../../../vita-fl/tee_inference/air/v1.py),
[`numeric protocol`](../../../vita-fl/tee_inference/protocol/v1.py),
[`verification and publication`](../../../vita-fl/agent/tee_inference_client.py).

## Rebuild and validation

From `presentation/`:

```sh
.venv/bin/python concepts/sello-air/build_designs.py
```

The builder checks text bounds, slide count, shape identifiers, citation links,
speaker notes and the main presentation's unchanged SHA-256. PNGs/PDF are local
layout previews; PowerPoint is authoritative for exact typography. All diagrams
use native editable shapes. `validation.json` records these checks.
