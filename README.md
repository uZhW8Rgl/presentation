# VITA-FL — Master's Thesis Presentation

This repository contains the English presentation for the VITA-FL master's
thesis. It comprises twenty-nine talk pages, three compact backup and overview
pages (one worker-role overview and two threat overviews), and fourteen
full-size use/misuse-case backup pages, for a total of forty-six pages. The complete
timed talk is approximately twenty-four minutes. The deck is built directly from
the official TU Berlin PowerPoint template, and its title page preserves the
official TU Berlin branding.

## Files

- `TU_Berlin_Praesentation_Master_einfarbig_Rot.pptx`: unchanged TU Berlin source template
- `VITA-FL_Thesis_Presentation_TU_Berlin.pptx`: editable 16:9 presentation
- `preview/contact-sheet.png`: preview of all forty-six pages
- `build_presentation.py`: reproducible deck generator
- `update_evaluation_stack.py`: idempotent insertion/update of the approved evaluation-stack diagram on Page 24 with structural preservation checks
- `update_slide25_test_evaluation.py`: idempotent insertion/update of the selected CI/external-test slide on Page 26 with structural preservation checks
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
- `assets/evaluation-stack-c.pptx`: approved native evaluation-stack diagram used on Page 24
- `assets/test-evaluation-a.pptx`: approved native CI/external-test variant A used on Page 26
- `assets/test-evaluation-integration.json`: insertion/update audit and backup location
- `assets/worker-inference-a.pptx`: approved combined-image and internal-key diagram used on Page 30
- `data/evaluation/authoritative_phala_6w_24r*.{csv,json}`: the sole six-worker, 24-round Phala run of the current deterministic equal-weight FedAvg path, including simulated Anvil gas accounting, used by the cloud-run and learning-metric slides; the generator records the run-specific Tier-1 allocation of six worker and two infrastructure TEE slots
- `requirements.txt`: pinned Python dependencies

Every page contains English speaker notes. The PNG renderer is intended only
for layout inspection; PowerPoint remains authoritative for exact font metrics
and line wrapping. Preview rendering expects the DejaVu Sans fonts at their
standard Linux paths.

Pages 1–6 have no domain legend. Pages 7–46 show compact **DFL** and **Agent**
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

Page 9 uses the approved [lifecycle diagram](preview/slide-09.png).
Workers send local updates directly to the aggregator. The global-model section
integrates IPFS model files and blockchain references into the publish/load cycle.
A model-use branch leads to inference, invoked by an agent through MCP,
with a tool receipt recorded in the transparency log. A separate Phala remote
attestation check appears beneath Inference, linked by an evidence-verification connector. All diagram elements remain
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
generator.

Page 24 uses the approved **Local evaluation, deployed system** diagram
from `assets/evaluation-stack-c.pptx`. SMEW coordinates the campaign, SMA runs
the test driver and retrieves Prometheus time series for the measurement window,
and vita-fl-td checks the deployed VITA-FL system through its APIs and RPC.
The diagram separates the local experiment host from the VITA-FL services and
Prometheus in Phala; saved results feed the reports and Marimo analysis.
SMA retrieves the time series after the scenario ends. The slide explains the
evaluation workflow without claiming that system metrics constitute a general
energy measurement or changing the scope of the historical run on Page 25.

Page 26 uses the selected **CI checks and external system tests** variant A
from [the CI/external proposals](concepts/test-evaluation/ci-external/README.md).
Its left catalog groups **878 CI-selected definitions** into seven subjects:
learning/model integrity, round control/recovery, identity/transport,
inference/agent workflow, receipts/provenance, runtime/telemetry and
deployment/packaging. Unit, component and integration tests share one CI block;
each definition counts once before parameter expansion or repeated executions.
The right catalog covers **eight external modes**: configuration, normal,
inference, early, partial, zero, recovery and security. A separate,
cross-scenario receipt audit has **17 checks**; the security mode has **16 checks,
including a positive inference control**. These are distinct counting units,
not passed runs or an exhaustive coverage measure. Manipulation and adversarial
tool-order tests remain outside the selected external scope.

The current Phala training profile uses six workers, five successful training
rounds excluding bootstrap, client limit five and a 45-second collection deadline.
Configuration is a setup-only check. The current profile also trains before the
inference mode; historical runs can use different settings. SMEW/SMA/vita-fl-td
exercise the deployed services; collection scenarios use a documented upload
gate, while recovery stops the selected aggregator CVM. Speaker notes distinguish
implemented checks, configured execution and observed results. Both DFL and
Agent navigation chips are active.

The earlier **808 = 731 unit/component + 77 integration** inventory remains only
in the historical `concepts/test-evaluation/test-inventory.{csv,json,md}` files.
Its absence of an automated complete cloud training/inference or fault-injection
evaluation describes that historical inventory. It is not the current Page 26
scope and does not change the legacy-profile Phala results on Page 25.

Page 30 uses the approved [combined worker/inference diagram A](concepts/worker-inference/a-shared-image.png).
One image and container contain the DFL and inference processes, with keys
used internally. The agent receives results and signed evidence through its
tool call, without a private-key transfer. Notes retain the distinction between
on-chain admission and KMS key release and the associated update-policy assumption.

Pages 30–46 are backup material and are not included in the timing below.

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
| 24 | Evaluation workflow: SMEW, SMA, vita-fl-td, and VITA-FL in Phala | 0:45 |
| 25 | Sole-run protocol, Tier-1 capacity allocation, and workload summary | 0:45 |
| 26 | CI checks by subject and configured external system tests | 0:55 |
| 27 | BCE, macro-AUROC, macro-F1, accuracy, and exact match across all 24 rounds | 0:50 |
| 28 | Dataset imbalance and metric interpretation | 0:45 |
| 29 | Conclusion and outlook | 0:40 |

Total: approximately twenty-four minutes, including brief transitions between the
timed pages. For a shorter slot, Pages 13–17 and 23
can be treated as technical detail pages without breaking the main narrative.

## Regeneration

The delivered PPTX preserves existing slide edits. The approved lifecycle and
image-policy slides were inserted directly into that file, and the Sello/AIR
comparison replaces Page 20. The approved evaluation-stack diagram is inserted
as Page 24 before the historical cloud-run overview, now on Page 25. The
selected CI/external-test variant A replaces the previous test matrix on Page 26.
The update retains the other slides and their notes; the deck remains at 46 pages. The generator
includes these diagrams from their
independent assets. The former combined
attestation/key slide was replaced with two native diagrams; all other slide
edits were retained. A full regeneration recreates the
source version of earlier slides; it does not retain edits made only in PowerPoint.

To insert or update the approved evaluation-stack slide while preserving
existing PowerPoint edits, run from the presentation directory:

```bash
.venv/bin/python update_evaluation_stack.py --render
```

The updater integrates the editable diagram from `assets/evaluation-stack-c.pptx`
and advances the subsequent page numbers. It updates the existing diagram on
repeat runs; `--render` refreshes the previews.

To rebuild the selected CI/external-test asset and update Page 26 while
preserving existing PowerPoint edits, run from the presentation directory:

```bash
.venv/bin/python concepts/test-evaluation/build_selected.py
.venv/bin/python update_slide25_test_evaluation.py --render
```

The selected builder uses CI/external variant A and the current inventory in
`concepts/test-evaluation/ci-external/`. The earlier `inventory_tests.py` belongs
to the historical 808-definition inventory and is not a prerequisite for this build.

The updater creates a backup in a new `vita-fl-before-test-evaluation-*`
directory under the system temporary directory and validates the candidate before replacing the deck. It verifies
the other slides' XML (apart from page numbers), speaker notes and slide
relationships, unchanged media/masters/layouts, sequential Page 2–46 footers, the
29-page talk/17-page backup boundary, native shapes and the generator hook.
A second run updates the test slide on Page 26 instead of adding another page. It records the
asset and deck hashes in `assets/test-evaluation-integration.json`.

For a complete regeneration, run from the presentation directory:

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
