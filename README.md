# VITA-FL — Master's Thesis Presentation

This repository contains the English presentation for the VITA-FL master's
thesis. It comprises twenty-seven talk pages, three compact backup and overview
pages (one worker-role overview and two threat overviews), and fourteen
full-size use/misuse-case backup pages, for a total of forty-four pages. The complete
timed talk is approximately twenty-two minutes. The deck is built directly from
the official TU Berlin PowerPoint template, and its title page preserves the
official TU Berlin branding.

## Files

- `TU_Berlin_Praesentation_Master_einfarbig_Rot.pptx`: unchanged TU Berlin source template
- `VITA-FL_Thesis_Presentation_TU_Berlin.pptx`: editable 16:9 presentation
- `preview/contact-sheet.png`: preview of all forty-four pages
- `build_presentation.py`: reproducible deck generator
- `attestation_slides.py`: on-chain verification diagram for Page 14 and the earlier key-derivation layout retained for concepts
- `render_preview.py`: lightweight local QA renderer
- `assets/threat-diagrams/T1.png` … `T14.png`: use/misuse-case source diagrams
- `assets/xray_concept.png`: realistic, anonymized chest-radiograph motif used on Page 3
- `assets/physician-editorial-illustration-tablet.png`: illustrated physician used on Page 3
- `assets/computer-scientist-editorial-illustration.png`: illustrated computer scientist used on Page 4
- `assets/lifecycle-f3.pptx`: approved editable lifecycle diagram used on Page 9
- `assets/ci-cd-image-policy.pptx`: approved editable image-policy pipeline used on Page 13
- `assets/dstack-key-usage-d.pptx`: approved editable key-use actor map used on Page 15
- `assets/aggregation-round-a.pptx`: approved editable aggregation flow used on Page 18
- `assets/sello-air-a.pptx`: approved editable Sello/AIR evidence comparison used on Page 20
- `assets/worker-inference-a.pptx`: approved combined-image and internal-key diagram used on Page 28
- `data/evaluation/authoritative_phala_6w_24r*.{csv,json}`: the sole six-worker, 24-round Phala run of the current deterministic equal-weight FedAvg path, including simulated Anvil gas accounting, used by every evaluation slide; the generator records the run-specific Tier-1 allocation of six worker and two infrastructure TEE slots
- `requirements.txt`: pinned Python dependencies

Every page contains English speaker notes. The PNG renderer is intended only
for layout inspection; PowerPoint remains authoritative for exact font metrics
and line wrapping. Preview rendering expects the DejaVu Sans fonts at their
standard Linux paths.

Pages 1–6 have no domain legend. Pages 7–44 show compact **DFL** and **Agent**
chips at the top right, directly left of the TU Berlin logo. Active domains
retain green (`#207548`) and blue (`#1764A1`); inactive domains are gray.
Page 20 explicitly activates only **Agent**; its **DFL** chip is gray.

Page 6 introduces the hospital-consortium scenario from Chapter 1: complementary
local datasets, a jointly trained chest X-ray model, and its later use through
an AI assistant. The diagram uses editable PowerPoint shapes. Shared control
and the need for evidence connect the preceding motivation and research questions
to the system background.

Page 7 compares representative literature (Lee/Heiss, Ebrahimi et al., Voltran, Hartmann, ZKML,
ZkAudit, Balan, AIR, VET, and Sello) with VITA-FL using editable coverage blocks
and mechanism markers. AIR is labelled as a draft with a demonstration
implementation. Technical background references remain in the speaker notes.
The coverage columns are **DFL**, **Inference**, **Agent**, and **Transparency Log**.
Under verification mechanisms, **Remote attestation** groups **Quote verification**
and **RTMR3 replay**. Voltran's quote cell says **SGX RA**, since the paper evaluates
RA without specifying its individual quote-verifier checks.
Filled and outlined marks distinguish implementations from discussed/framework
options; dashes mean not described in the checked work. Paper names link to
primary sources where a public URL is available. Hartmann's attestation scope
was checked against the original code preserved in the prototype's Git history;
its zkVM verifies certificates rather than ML computations. Speaker notes explain
the scope of the comparison, including
RTMR3 image binding and admission versus per-inference attestation checks.
The **ZKP** column includes proofs beyond ML arithmetic; Hartmann's implemented
certificate proof and VET's TLSNotary proofs are therefore marked. Balan's ZKP
mark, coverage blocks, and TEE mark are outlined to indicate discussion/framework
coverage.
Ebrahimi et al. (IEEE Blockchain 2024) is included with implemented **DFL** and
**ZKP** markers: its companion implementation supplies separate training and
aggregation proofs with on-chain verification. The source link and qualifications
are in the slide notes; the other comparison markers retain their existing meaning.
Page 5 states the attestation-based integration focus without claiming that
earlier lifecycle compositions do not exist.

Page 8 compares centrally coordinated FL with the participant-assigned aggregation
role used in VITA-FL. Three example rounds highlight the same participants taking
the aggregator role in turn. Two role panels introduce worker and aggregator tasks;
speaker notes explain local/global models, role assignment, and recovery limits.

Page 9 uses the approved [lifecycle F3](concepts/lifecycle/integrated/f3-publication-arc.png).
Workers send local updates directly to the aggregator. The global-model section
integrates IPFS model files and blockchain references into the publish/load cycle.
A model-use branch leads to attested inference, invoked by an agent through MCP,
with a tool receipt recorded in the transparency log. All diagram elements remain
editable PowerPoint shapes; notes explain the abstraction and prototype flow.

Page 10 uses the approved [architecture layout A](concepts/architecture-ledger/draft-a.png):
ledger and IPFS share the purple domain and each connects directly to the
Receiver TEE. Two overlapping dashed frames include the shared infrastructure
in both responsibility groups. The green and blue captions sit below their
colored panels, inside the dashed frames.

Page 13 shows the approved worker-image pipeline: GitHub push, worker tests,
GHCR publication, Terraform, and `EXPECTED_WORKER_IMAGE` in the contracts
container. An owner transaction writes the extracted digest to
`DeviceRegistry.expectedWorkerImageDigest` using
`setExpectedWorkerImageDigest(bytes32)`. This establishes the expected image
policy before the attestation explanation on Page 14. The diagram remains
editable and its source asset is independent of the removed concept folder.

Page 14 shows the worker submitting exact `app_compose`, an ordered event log
and a TDX quote to on-chain verification. It separates the image-Digest policy
comparison, compose-hash binding, RTMR3 replay, and authenticated quote /
REPORTDATA checks. All checks must pass for the worker to be admitted.

Page 15 uses the approved [key-use actor map D](concepts/dstack-key-usage/d-actor-map.png).
The worker TEE holds separate identities for blockchain actions, model exchange,
Sello tool receipts and AIR inference evidence. Arrows connect each identity
to its concrete use and communication partner. The derived AES-GCM key seals
the random RSA private key; RSA signs model packages and unwraps symmetric
model keys. Notes distinguish KMS authorization from on-chain admission and
describe the public-key bindings. The independent editable asset preserves the
approved diagram for future builds.

Page 18 uses the approved [aggregation flow A](concepts/aggregation-round/a-actors-and-messages.png).
Arrows show the sequence without numbered stages. The diagram distinguishes
worker transfer, TEE checks and FedAvg, IPFS storage, and blockchain admission,
input closure and finalization. The transaction binds the signed statement
and model references while advancing the round; notes explain the exact
checks and the separate IPFS publication.

Page 20 uses the approved [Sello/AIR comparison A](concepts/sello-air/guarantees/a-two-evidence-layers.png),
**Sello and AIR: two layers of evidence**. Sello covers authorization, signed
tool-call records and receipt encryption; AIR covers data binding, quote/key
binding and deployment-policy checks. The AIR caption reads **Attested Inference
Receipt**, and the service and shared-log labels use **Inference TEE** and
**Transparency Log**. Technical limitations remain in the speaker notes; the
visible scope sentence is omitted. The approved native asset is reused by the
generator, and the main deck retains forty-four pages.

Page 28 uses the approved [combined worker/inference diagram A](concepts/worker-inference/a-shared-image.png).
One image and container contain the DFL and inference processes, with keys
used internally. The agent receives results and signed evidence through its
tool call, without a private-key transfer. Notes retain the distinction between
on-chain admission and KMS key release and the associated update-policy assumption.

Pages 28–44 are backup material and are not included in the timing below.

## Suggested timing

| Page | Topic | Time |
|---:|---|---:|
| 1 | Title and guiding idea | 0:25 |
| 2 | Personal background and project experience | 0:30 |
| 3 | Physician's starting point | 0:45 |
| 4 | Computer scientist's engineering response | 0:35 |
| 5 | Research gap and questions | 0:45 |
| 6 | Hospital consortium: shared model, local data, verifiable use | 0:35 |
| 7 | Prior work: system coverage and verification | 0:55 |
| 8 | Central FL vs. DFL and worker/aggregator responsibilities | 0:45 |
| 9 | Lifecycle: training, model publication, inference, and logging | 0:40 |
| 10 | Overall architecture | 0:45 |
| 11 | Decentralized training across hospitals | 0:35 |
| 12 | Worker-training and DCAP-admission ZK scope | 0:50 |
| 13 | Worker image: CI/CD, contracts environment, and on-chain policy | 0:45 |
| 14 | On-chain image policy, event-log binding, RTMR3 replay, and quote verification | 0:55 |
| 15 | Key use at blockchain, model-exchange, log and agent interfaces | 0:45 |
| 16 | Weighted aggregator selection | 0:40 |
| 17 | Quorum recovery and aggregator replacement | 0:45 |
| 18 | Aggregation across workers, TEE, IPFS and blockchain | 0:50 |
| 19 | Model handoff | 0:40 |
| 20 | Sello and AIR: two layers of evidence | 0:45 |
| 21 | Agent-mediated attested inference | 0:55 |
| 22 | Independent audit | 0:50 |
| 23 | Cryptographic chain of custody | 0:55 |
| 24 | Sole-run protocol, Tier-1 capacity allocation, and workload summary | 0:45 |
| 25 | BCE, macro-AUROC, macro-F1, accuracy, and exact match across all 24 rounds | 0:50 |
| 26 | Dataset imbalance and metric interpretation | 0:45 |
| 27 | Conclusion and outlook | 0:40 |

Total: approximately twenty-two minutes, including brief transitions between the
timed pages. For a shorter slot, Pages 13–17 and 23
can be treated as technical detail pages without breaking the main narrative.

## Regeneration

The delivered PPTX preserves existing slide edits. The approved lifecycle and
image-policy slides were inserted directly into that file, and the Sello/AIR
comparison replaces Page 20. The generator includes these diagrams from their
independent assets. The former combined
attestation/key slide was replaced with two native diagrams; all other slide
edits were retained. A full regeneration recreates the
source version of earlier slides; it does not retain edits made only in PowerPoint.

Run from the repository root:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python build_presentation.py
.venv/bin/python render_preview.py
```

After substantive edits, open the deck once in Microsoft PowerPoint or
LibreOffice Impress to confirm the exact Arial line wrapping on the target
machine.

The bundled TU Berlin template and its marks remain subject to the applicable
TU Berlin branding and usage rules.
