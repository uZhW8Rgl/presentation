# Current vita-fl CI inventory

Commit: `61b96e514c0803d071f6f955d353e9d46a1e2244`; tracked working tree clean: `True`.

878 unique static definitions = 617 Python + 145 Solidity + 116 Node. No execution or PASS claim.

| Functional area | Definitions | CI jobs |
|---|---:|---|
| Learning & model integrity | 78 | node-server, python-quality |
| Round control & recovery | 117 | node-server, smart-contracts |
| Identity & secure transport | 240 | node-server, python-quality, smart-contracts, transport-pki |
| Inference & agent workflow | 49 | python-quality |
| Receipts & provenance | 64 | python-quality, smart-contracts |
| Runtime control & telemetry | 107 | node-server, python-quality |
| Deployment & packaging | 223 | docker-builds, python-quality, smart-contracts |

78 + 117 + 240 + 49 + 64 + 107 + 223 = 878

## Learning & model integrity

- Training shards form the exact reproducible, disjoint seed-42 partition. `dfl/neural_network/tests/test_chestmnist_training_shards.py:26::test_signed_shards_are_exact_disjoint_seed_42_partition`
- Even-size coordinate median averages the two middle values. `dfl/neural_network/tests/test_hybrid_r.py:61::test_even_coordinate_median_averages_middle_two`
- Aggregator rejects unauthenticated active parent-model evidence. `dfl/node_server/test/aggregator_parent_model.test.js:19::aggregator authenticates the active parent model fail-closed`

## Round control & recovery

- Local collection deadline releases a partial set without advancing the latest block. `dfl/node_server/test/aggregation_window.test.js:39::local timer releases a partial set while the latest block never advances`
- Registry contraction cannot reduce the snapshotted recovery quorum. `smart_contracts/test/AggregatorSelectionAccess.t.sol:346::testTimeoutQuorumDoesNotShrinkAfterRegistryContraction`
- Actual local Anvil transaction succeeds with pending-block gas estimation after timeout. `dfl/node_server/test/timeout_pending.test.js:26::timeout report estimates the pending block when Anvil latest predates its deadline`

## Identity & secure transport

- Malformed quote signature boundaries are rejected. `transport_security/tests/test_attestation.py:72::test_quote_parser_rejects_invalid_signature_boundaries`
- Actual local TLS connection is attested before credentials/body are sent; quote verification is controlled. `transport_security/tests/test_ratls_transport.py:148::test_actual_tls_connection_is_attested_before_credentials_and_body`
- Real local step-ca/step enrollment, renewal and active revocation. `pki/tests/test_step_ca_integration.py:22::test_real_ca_one_use_renewal_and_active_revocation`

## Inference & agent workflow

- Public MCP surface exposes only the six intended job tools. `agent/tests/test_mcp_surface.py:18::test_only_the_six_job_tools_are_public`
- Production ASGI job API keeps dataset and evidence in service storage. `tee_inference/tests/test_inference_service.py:41::test_job_api_keeps_dataset_and_evidence_inside_service_storage`
- ZK model/sample/proof artifacts belong to the job; proof-producing dependencies are injected. `zk_inference/tests/test_job_runtime.py:13::test_model_sample_and_verified_proof_are_job_owned`

## Receipts & provenance

- AIR receipt verification accepts the official TDX golden vector under its expected policy. `tee_inference/tests/test_air_v1.py:54::test_verifies_official_tdx_golden_vector`
- Sello receipt verification rejects a changed output hash. `agent/tests/test_sello_v1.py:140::test_tampered_output_is_rejected`
- Signed medical-data provenance rejects a modified label. `dfl/neural_network/tests/test_dicom_provenance.py:49::test_modified_label_is_rejected`

## Runtime control & telemetry

- Invalid submission deadlines are rejected before persistence or run start. `control_api/tests/test_training_submission_deadline.py:66::test_invalid_deadlines_are_rejected_before_persistence_or_start`
- Evaluation upload gate preserves run/roster selection and supports release and restart. `control_api/tests/test_evaluation_gate.py:23::test_generation_roster_selection_release_and_restart`
- Signed worker events update evaluation metrics with the correct values and scales. `control_api/tests/test_telemetry.py:47::test_signed_event_updates_evaluation_metrics`

## Deployment & packaging

- Older slow build cannot replace a newer deployment revision; uses local Git history. `phala/test_ci_deploy.py:113::test_slow_older_build_is_skipped`
- Offline Terraform retains selected image revisions through destroy and failed recreation; conditional on Terraform availability. `phala/test_image_manifest.py:23::test_selected_images_and_revisions_survive_destroy_and_failed_recreation`
- Staged tracked Docker context contains every COPY source and excludes secrets/caches. `scripts/tests/test_docker_build_contexts.py:64::test_real_tracked_context_contains_every_local_copy_source`

## Scope and limitations

- Counts are unique declared tests selected by the checked-in CI commands, not executed test cases or PASS counts. No test modules were imported, collected or executed.
- One Python test_* function/method, Solidity test* function or explicit Node test(...) declaration is one unit. Parameters, fuzz cases, loops, subtests and CI reruns are not expanded.
- 33 definitions have explicit Python parameterization; 20 definitions contain potential skip conditions/calls. These are metadata indicators, not actual runtime skip counts. Terraform checks may skip if the binary is unavailable; CI does not explicitly install Terraform in python-quality.
- Functional grouping is disjoint by each test file's dominant responsibility. Cross-cutting assertions within a file remain assigned once; counts do not measure coverage, security strength or equal test complexity.
- Unit/component/local integration tests share the CI umbrella. Real local ASGI/TLS/step-ca/nginx/Git/GPG/Terraform/Anvil boundaries may be exercised; cloud APIs, quote appraisal, model/proof execution or other collaborators are often controlled/mocked.
- CI node-server installs Foundry v1.3.1 and sets REQUIRE_ANVIL_TESTS=1, so timeout_pending.test.js is not silently skipped for a missing Anvil binary in CI.
- Actual Phala system scenarios and fresh log-based receipt audits belong to the separate SMEW/SMA/vita-fl-td campaign workflow, not these 878 vita-fl CI definitions.
- Historical 808-definition inventory and its 731/77 taxonomy were not overwritten or reused as current counts.
