# Static test inventory

**808 implemented test definitions: 731 unit/component, 77 local integration, 0 complete automated system E2E.**

This is a source inventory, not an execution report. No pass rate, successful CI run or new test result is claimed. Production is an execution context, not a fourth test level.

| Test type | Definitions | Boundary |
|---|---:|---|
| Unit/component | 731 | Isolated functions, modules, contracts, crypto, guards, source and configuration checks; dependencies controlled |
| Local integration | 77 | Actual API/socket/process boundaries or asserted collaboration of production components; selected dependencies can remain mocked |
| Complete system E2E | 0 | No automated full application lifecycle established in the selected CI test definitions |

Languages: **569 Python, 138 Solidity, 101 Node**; **96 test files**.

## Counting and classification rules

- U: isolated production function/module/contract/library, fixtures/mocks, pure/source/configuration checks.
- I: asserted behavior crosses a real production API/service/process boundary or actively composes production components; external dependencies may remain mocked.
- Classification is assertion-specific: fixture construction, filenames and end_to_end in a name do not determine the category.
- The exact reviewed integration whitelist is encoded in inventory_tests.py; all other inventoried definitions are U.
- System E2E means an automated complete application lifecycle; none is defined in this inventory.
- Production is an execution context, not an additional test level; no automated production execution is established by this static inventory.
- Count declarations, not executions. Parametrization, subtests, loops and duplicate runs in publisher workflows are not expanded.
- Conditional skips remain included: local model fixtures, Terraform, nginx, Smallstep binaries and Docker availability can affect executed counts.
- Python uses static AST traversal; Solidity and Node use static declaration matching for this checkout's source style. Tests are never imported or collected.
- A model-inference function or Hybrid-R test named end_to_end remains a component test. Direct control-API calls with mocked dependencies remain component tests; ASGI/HTTP requests exercise integration boundaries.
- Only the positive AIR-v2 service-emitter/agent-verifier compatibility test is classified as integration in test_ratls.py; isolated rejection guards stay component tests despite a composed fixture.
- Solidity integration requires the assertion to traverse actual production contracts. Cross-contract setup alone and a mocked TDX verifier do not establish that scope.
- This checkout includes newer RA-TLS definitions. Their inventory must not be attributed to the historical mTLS/AIR-v1 cloud run.

## CI execution configuration

Primary source: [ci.yml](../../../vita-fl/.github/workflows/ci.yml). CI is configured for push/PR on main and phala_app_key, and manual dispatch. The table describes configured execution, not an observed outcome.

| CI job | Unit/component | Local integration | Command scope |
|---|---:|---:|---|
| python-quality | 461 | 43 | pytest agent/tests and tee_inference/tests; unittest discovery for DFL neural/container, ZK, control API, Phala and transparency-log tests |
| transport-pki | 50 | 10 | pytest transport_security/tests pki/tests; CI installs/checks nginx, step and step-ca |
| node-server | 89 | 0 | npm test → node --test in dfl/node_server |
| smart-contracts | 130 | 20 | forge test -vvv plus node --test test/*.test.mjs |
| docker-builds | 1 | 4 | unittest test_docker_build_contexts.py, only matrix.name == tee-inference |

Publisher workflows can rerun subsets; those invocations do not create additional definitions.

## Separate evidence, excluded from 808

- **2 configured service-readiness checks** in runtime-smoke-test: Anvil eth_chainId and IPFS /api/v0/version. They do not execute the full training/inference lifecycle.
- **1 existing manual Phala workflow record**: data/evaluation/authoritative-phala-6w-24r-20260901/README.md (six workers, 24 training rounds and final inference). No new cloud run, full recovery experiment or production qualification is claimed.

## Representative assertions

| Category | Test | Scope |
|---|---|---|
| unit_component | `dfl/neural_network/tests/test_dicom_provenance.py:49::test_modified_label_is_rejected` | Isolated production component, protocol/crypto/model/configuration assertion or guard; fixtures and mocked dependencies do not change the tested scope. |
| unit_component | `agent/tests/test_tee_inference_client.py:430::test_request_substitution_is_rejected` | Client, orchestration, policy or receipt component assertion with controlled dependencies; fixture crypto alone does not establish a live service boundary. |
| local_integration | `tee_inference/tests/test_authorization.py:145::test_publication_failure_cannot_return_success_without_receipt` | Real ASGI requests exercise production routing, authorization, job ownership and receipt handling; model and log dependencies are controlled. |
| local_integration | `smart_contracts/test/GMStorageAggregatorReward.t.sol:187::testAtomicFinalizationPublishesAdvancesAndRewardsExactlyOnce` | Assertion exercises real GMStorage-policy publication, threshold or ledger-binding transitions; registry/selection dependencies may be stubs. |
| local_integration | `pki/tests/test_step_ca_integration.py:22::test_real_ca_one_use_renewal_and_active_revocation` | Disposable real local step-ca/step processes exercise enrollment, renewal and active revocation; requires their binaries. |

## Reproduce and audit

From the workspace root:

```bash
presentation/.venv/bin/python presentation/concepts/test-evaluation/inventory_tests.py
```

The script asserts 808 = 569 + 138 + 101 and the reviewed 731/77 split, rejecting stale whitelist entries or duplicate identifiers. It writes test-inventory.json, test-inventory.csv and this overview. Each test row includes path, line, name, category, rationale, CI job, source SHA-256 and commit.

- Commit: `29b78acafcfe1362257e1cebb3f0f91a0026be80`
- Tracked working-tree changes present: `False`
- Combined source SHA-256: `e66bc970c69daa0148d2317e1b168c8dcfeeb137e17c42c8cd1b89844ea8a28c`
- Inventory script SHA-256: `a12579ac9d6a3387c8170a2f8b16f6004b972434e86e837c1067a4d10b18fa87`
- Generated UTC: `2026-09-24T14:09:44.920080+00:00`

The commit identifies the base revision; per-file content hashes identify the actual inspected working tree. The combined hash covers every inventoried test file, ci.yml and the Node package.json. It does not hash every production implementation dependency.

Machine-readable outputs contain the complete per-definition classification and source-hash manifest. Static classification is a documented operational convention for this evaluation, not a universal taxonomy.
