"""Static, reviewed inventory of CI-selected test definitions (Python 3.9+).

No test module is imported and no test is executed. Run from any directory:
    presentation/.venv/bin/python presentation/concepts/test-evaluation/inventory_tests.py
"""

from __future__ import annotations

import ast
import csv
import hashlib
import json
import re
import subprocess
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2] / "vita-fl"
CI = ".github/workflows/ci.yml"
U, I, S = "unit_component", "local_integration", "system_e2e"
PYTHON_ROOTS = [
    ("agent/tests", "python-quality"),
    ("tee_inference/tests", "python-quality"),
    ("dfl/neural_network/tests", "python-quality"),
    ("dfl/tests", "python-quality"),
    ("zk_inference/tests", "python-quality"),
    ("control_api/tests", "python-quality"),
    ("phala", "python-quality"),
    ("transparency_log", "python-quality"),
    ("transport_security/tests", "transport-pki"),
    ("pki/tests", "transport-pki"),
    ("scripts/tests/test_docker_build_contexts.py", "docker-builds"),
]

# Exact per-definition integration whitelist, reviewed by the tested assertion.
# Helpers/fixtures that happen to compose objects do not change a guard test's type.
INTEGRATION = {}


def integration(path, names, reason):
    for name in names.split():
        key = (path, name)
        assert key not in INTEGRATION, key
        INTEGRATION[key] = reason


integration("tee_inference/tests/test_authorization.py", """
test_every_operation_requires_token_and_mtls_before_work
test_wrong_token_binding_scope_and_expiry_rejected_before_model_load
test_owner_bound_job_flow_emits_verifiable_encrypted_receipt
test_another_authenticated_agent_cannot_read_or_run_job
test_receipt_download_is_authenticated_without_recursive_receipt
test_publication_failure_cannot_return_success_without_receipt
test_revoked_client_certificate_cannot_use_its_unexpired_token
test_health_is_minimal_and_legacy_routes_are_absent
""", "Real ASGI requests exercise production routing, authorization, job ownership and receipt handling; model and log dependencies are controlled.")
integration("tee_inference/tests/test_ratls_authorization.py", """
test_protected_routes_reject_unsigned_calls_and_spoofed_proxy_headers_before_work
test_forged_subject_and_wrong_pop_key_do_not_authorize_model_load
test_mutated_body_session_and_tls_header_are_rejected_before_work
test_same_proof_cannot_execute_twice
test_registry_revocation_rejects_unexpired_token
test_allowed_operations_emit_sello_receipts_bound_to_session_and_tls_key
test_distinct_registered_agent_cannot_access_another_subjects_job
test_log_failure_withholds_response_without_claiming_operation_rollback
""", "Production API exercised through ASGI with real PoP/token/receipt crypto; session, model and publication dependencies are controlled, with no TLS handshake.")
integration("tee_inference/tests/test_inference_service.py", """
test_job_api_keeps_dataset_and_evidence_inside_service_storage
test_health_does_not_load_model_and_prepare_refreshes_it
test_failed_prepare_is_retried_by_next_tool_call
test_legacy_http_inference_route_is_removed
""", "Actual ASGI requests exercise production API routing, model-loading lifecycle or persistent job storage; model dependencies are controlled where applicable.")
integration("tee_inference/tests/test_private_transport.py", """
test_receiver_serves_only_a_private_unix_socket
""", "Production receiver entrypoint runs uvicorn and serves an actual Unix-socket HTTP request with an injected minimal app.")
integration("tee_inference/tests/test_ratls.py", """
test_air_v2_requires_session_challenge_quote_verification_and_existing_policy
""", "Positive compatibility assertion composes production session/evidence handling, service AIR emitter and agent verifier; Dstack and Phala API are mocked.")
integration("dfl/neural_network/tests/test_aggregate_participant_key.py", """
test_aggregate_http_request_forwards_participant_key
test_train_http_request_forwards_participant_key
""", "Loopback HTTP requests exercise the production service.Handler boundary; training or aggregation implementation is mocked.")
integration("dfl/neural_network/tests/test_runtime_trust_root.py", """
test_accepts_matching_manifest_addresses_and_rpc_chain
test_rejects_substituted_runtime_manifest_before_node_start
test_rejects_rpc_chain_substitution_before_node_start
""", "Production resolver extracted from the startup script makes real HTTP calls to a local fake RPC/IPFS server.")
integration("dfl/tests/test_ratls_startup.py", """
test_node_registration_and_receiver_inherit_the_same_resolved_origin
test_origin_resolution_failure_stops_before_node_or_receiver_start
test_legacy_mtls_does_not_resolve_a_dstack_origin
""", "Production shell supervisor is executed and coordinates child-process startup/environment propagation; service executables are stubs.")

integration("transport_security/tests/test_transport.py", """
test_real_mtls_and_thumbprint
test_rejects_plaintext_redirect_and_revoked_server
test_call_keeps_certificate_binding_across_renewals_and_receipt_download
""", "Actual local TLS client/server or certificate-bound receipt-download wiring is exercised with generated certificates and controlled external dependencies.")
integration("transport_security/tests/test_ratls_transport.py", """
test_actual_tls_connection_is_attested_before_credentials_and_body
test_failed_attestation_never_sends_protected_http
test_error_response_retains_attested_session_and_owns_socket
test_slow_evidence_has_absolute_deadline_and_sends_no_credentials
""", "Actual local TLS connection tests attestation-before-credentials, socket/error handling or deadlines; quote and deployment verification are mocked.")
integration("transport_security/tests/test_ratls_transport.py", """
test_generated_nginx_configuration_is_accepted
""", "Generated production proxy configuration is parsed by the real nginx -t process; no live proxy traffic is asserted by this definition.")
integration("pki/tests/test_step_ca_integration.py", """
test_real_ca_one_use_renewal_and_active_revocation
""", "Disposable real local step-ca/step processes exercise enrollment, renewal and active revocation; requires their binaries.")
integration("pki/tests/test_nginx_integration.py", """
test_nginx_private_socket_overwrites_headers_and_enforces_revocation
""", "Real local nginx, TLS and Unix-socket receiver exercise trusted header forwarding and certificate revocation; requires nginx.")

integration("phala/test_agent_zk_configuration.py", """
test_disabled_zk_does_not_inherit_a_previous_deployments_endpoint
""", "Real offline Terraform evaluates production deployment configuration; no cloud resources are created.")
integration("phala/test_image_manifest.py", """
test_selected_images_and_revisions_survive_destroy_and_failed_recreation
""", "Real offline Terraform with its built-in provider exercises retained deployment state; no live Phala deployment.")
integration("phala/test_runtime_bootstrap.py", """
test_static_and_dynamic_worker_security_topology_render_identically
test_runtime_compose_accepts_missing_and_explicit_endpoints
""", "Real offline Terraform renders production runtime/worker templates; no cloud resources are created.")
integration("phala/test_github_state.py", """
test_real_gpg_roundtrip_and_wrong_key_fail_without_secret_output
""", "Production state encryption invokes real GPG for a round trip and wrong-key rejection; GitHub is not contacted.")
integration("phala/test_github_state.py", """
test_real_terraform_apply_restore_and_destroy_offline
""", "Real offline Terraform and production encrypted-state handling are composed; GitHub API is fake.")
integration("phala/test_ci_deploy.py", """
test_newer_build_and_same_commit_retry_are_allowed
test_slow_older_build_is_skipped
test_missing_history_fails_instead_of_allowing_rollback
test_force_push_divergence_requires_reconciliation
test_image_revision_must_belong_to_current_deployment_branch
""", "Production deployment-revision logic invokes real Git against an actual temporary repository and history.")
integration("phala/test_ci_deploy.py", """
test_sigterm_reaches_main_cancellation_handler
""", "A real OS SIGTERM exercises installation/restoration of the production main cancellation handler.")
integration("phala/test_ci_deploy.py", """
test_signalled_child_retains_remote_deployment_lock
""", "Real checked-command cancellation propagates through production GitHubState.session; remote network, synchronization and unlock are mocked.")
integration("scripts/tests/test_docker_build_contexts.py", """
test_real_tracked_context_contains_every_local_copy_source
""", "Production context staging invokes real Git ls-files and stages actual tracked files for Docker COPY inputs.")
integration("scripts/tests/test_docker_build_contexts.py", """
test_all_image_copy_inputs_survive_their_effective_ignore_policy
test_real_staged_tee_copy_inputs_survive_effective_ignore_policy
test_tee_package_inclusions_do_not_include_private_keys_or_caches
""", "Actual local Docker builds exercise ignore/COPY rules and, where applicable, saved-image contents; requires a Docker daemon.")

integration("smart_contracts/test/AggregatorSelectionAccess.t.sol", """
testCurrentAggregatorCanSelectAfterCompletedRound
testSelectionCannotRunBeforeGMStorageRoundAdvanced
testAuthorizedNonAggregatorCanRecoverSelectionGapAfterCompletedRound
testTimeoutReportCannotAbortAnActiveSubmissionWindow
testCompletedRoundAggregatorCannotMutateNextRoundBeforeSelection
testStaleRoundExpectationRevertsWithoutCounting
testTimeoutCannotTargetSuccessfulAggregatorBeforeNextRoundSelection
testBootstrapTimeoutQuorumCannotSelectReplacement
""", "Assertion crosses actual selection and GMStorage/policy round or rollback coordination; registry and other dependencies may be stubs.")
integration("smart_contracts/test/GMStorageAbort.t.sol", """
testAbortAfterRejectedPublicationKeepsLastCompletedArtifacts
""", "Real GMStorage-to-AggregationPolicy publication rejection preserves previously finalized artifacts.")
integration("smart_contracts/test/GMStorageAggregatorReward.t.sol", """
testAtomicFinalizationPublishesAdvancesAndRewardsExactlyOnce
testAtomicFinalizationPromotesPublisherKeyAndFinalizedBundle
testPublisherKeyIsSnapshottedInsideAtomicFinalization
testNonBootstrapRoundRequiresConfiguredMinimum
testAggregationPolicyPointerRejectsAccountsAndWrongLedgerBinding
testNextRoundRequiresFreshSelectionAndFreshPolicySnapshot
testWrongAggregationStatementCannotPublishOrReward
""", "Assertion exercises real GMStorage-policy publication, threshold or ledger-binding transitions; registry/selection dependencies may be stubs.")
integration("smart_contracts/test/GMStorageContribution.t.sol", """
testAggregatorConfirmationAwardsWorkerExactlyOnePoint
testParentHashCommitsToModelSignatureAndKeyBundle
testSubmissionWindowClosureRejectsNewModelsButAllowsIdenticalRetry
testWorkerCanReceiveOneNewPointInNextRound
""", "Assertion exercises actual GMStorage-to-policy contribution, closure or publication collaboration.")


def default_reason(path):
    if path.endswith(".sol"):
        return "Local contract/library rule or guard; fixture-only cross-contract setup and mocks do not establish integration of the asserted property."
    if path.endswith((".js", ".mjs")):
        return "Isolated Node component, crypto, source/configuration assertion or shell fragment with controlled dependencies; no live application service boundary."
    if path.startswith("control_api/"):
        return "Direct service/helper invocation or source assertion; cloud, RPC and subprocess collaborators are controlled rather than exercised through a real API boundary."
    if path.startswith("zk_inference/"):
        return "Isolated runtime/configuration or manually constructed handler with injected dependencies; no actual proof pipeline or HTTP server boundary."
    if path.startswith("agent/"):
        return "Client, orchestration, policy or receipt component assertion with controlled dependencies; fixture crypto alone does not establish a live service boundary."
    if path == "dfl/tests/test_container_scripts.py":
        return "Source/Bash-syntax assertion or isolated healthcheck with fake curl; no actual service call."
    if path.startswith("phala/"):
        return "Isolated deployment/configuration/state component with controlled cloud or process dependencies; no live cloud lifecycle."
    return "Isolated production component, protocol/crypto/model/configuration assertion or guard; fixtures and mocked dependencies do not change the tested scope."


def python_definitions(source):
    """Return declarations, preserving owning class and explicit skip metadata."""
    tree = ast.parse(source)
    found = []

    def walk(node, owners=(), inherited=()):
        decorators = getattr(node, "decorator_list", ())
        own = tuple(ast.unparse(value) for value in decorators)
        context = inherited + own
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name.startswith("test_"):
            runtime_skip = any(
                isinstance(child, ast.Call)
                and isinstance(child.func, ast.Attribute)
                and child.func.attr in ("skip", "skipTest", "importorskip")
                for child in ast.walk(node)
            )
            skips = [value for value in context if "skip" in value]
            found.append({
                "line": node.lineno,
                "name": node.name,
                "qualified_name": ".".join(owners + (node.name,)),
                "parametrized": any("parametrize" in value for value in context),
                "conditional_skip": bool(skips) or runtime_skip,
                "skip_note": "; ".join(skips + (["Runtime skip call present"] if runtime_skip else [])),
            })
        next_owners = owners + (node.name,) if isinstance(node, ast.ClassDef) else owners
        for child in ast.iter_child_nodes(node):
            walk(child, next_owners, context)

    walk(tree)
    return found


NODE_DECLARATION = re.compile(r'''(?m)^[ \t]*test(?:\.(?:only|skip|todo))?\s*\(\s*(['"])((?:\\.|(?!\1)[^\\])*)\1''')
SOLIDITY_DECLARATION = re.compile(r"\bfunction\s+(test\w*)\s*\(")


def other_definitions(source, language):
    pattern = NODE_DECLARATION if language == "Node" else SOLIDITY_DECLARATION
    matches = list(pattern.finditer(source))
    for index, match in enumerate(matches):
        name = match.group(2) if language == "Node" else match.group(1)
        skip_note = ""
        if language == "Node":
            # Inspect this declaration's options, never a neighboring test's.
            # The checked-in Node suites use arrow callbacks; skip options are
            # before that callback, including the two local-artifact guards.
            end = matches[index + 1].start() if index + 1 < len(matches) else len(source)
            options = source[match.end():end].split("=>", 1)[0]
            skip = re.search(r"\bskip\s*:\s*([^,}]+)", options)
            if skip and skip.group(1).strip() != "false":
                skip_note = "Node test option: skip: " + " ".join(skip.group(1).split())
            elif re.match(r"\s*test\.skip\s*\(", match.group(0)):
                skip_note = "Explicit test.skip declaration"
        yield {
            "line": source.count("\n", 0, match.start()) + 1,
            "name": name,
            "qualified_name": name,
            "parametrized": False,
            "conditional_skip": bool(skip_note),
            "skip_note": skip_note,
        }


def git(*arguments):
    return subprocess.check_output(["git", "-C", str(REPO), *arguments], text=True).strip()


def inventory():
    sources = {}
    definitions = []
    for root, job in PYTHON_ROOTS:
        target = REPO / root
        files = [target] if target.is_file() else sorted(target.rglob("test_*.py"))
        definitions.extend((path, "Python", job) for path in files)
    definitions.extend((path, "Solidity", "smart-contracts") for path in sorted((REPO / "smart_contracts/test").glob("*.t.sol")))
    definitions.extend((path, "Node", "node-server") for path in sorted((REPO / "dfl/node_server/test").glob("*.test.js")))
    definitions.extend((path, "Node", "smart-contracts") for path in sorted((REPO / "smart_contracts/test").glob("*.test.mjs")))
    rows = []
    matched_integration = set()
    for file, language, job in definitions:
        path = file.relative_to(REPO).as_posix()
        raw = file.read_bytes()
        source = raw.decode("utf-8")
        digest = hashlib.sha256(raw).hexdigest()
        sources[path] = digest
        tests = python_definitions(source) if language == "Python" else other_definitions(source, language)
        for test in tests:
            key = (path, test["name"])
            if key in INTEGRATION:
                matched_integration.add(key)
            rows.append({
                "path": path,
                **test,
                "category": I if key in INTEGRATION else U,
                "reason": INTEGRATION.get(key, default_reason(path)),
                "language": language,
                "ci_job": job,
                "ci_workflow": CI,
                "ci_condition": "matrix.name == 'tee-inference'" if job == "docker-builds" else "",
                "source_sha256": digest,
            })
    assert matched_integration == set(INTEGRATION), "Stale integration whitelist: " + repr(set(INTEGRATION) - matched_integration)
    rows.sort(key=lambda row: (row["path"], row["line"], row["name"]))
    assert len({(row["path"], row["qualified_name"]) for row in rows}) == len(rows), "Duplicate test identifiers"
    counts = Counter(row["language"] for row in rows)
    assert counts == {"Python": 569, "Solidity": 138, "Node": 101}, counts
    categories = Counter(row["category"] for row in rows)
    assert len(rows) == 808 and categories == {U: 731, I: 77}, categories
    test_file_count = len(sources)
    for support in (CI, "dfl/node_server/package.json"):
        sources[support] = hashlib.sha256((REPO / support).read_bytes()).hexdigest()
    source_hash = hashlib.sha256(json.dumps(sources, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    commit = git("rev-parse", "HEAD")
    for row in rows:
        row["commit"] = commit
    return {
        "schema": "vita-fl-static-test-inventory-v1",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "repository": str(REPO),
        "commit": commit,
        "working_tree_dirty": bool(git("status", "--porcelain", "--untracked-files=no")),
        "source_sha256": source_hash,
        "source_sha256_definition": "SHA-256 of compact sorted JSON mapping every inventoried test file plus ci.yml and node package.json to its content SHA-256.",
        "inventory_script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "execution": "Static inspection only; no tests imported, collected or executed. No pass/fail result is asserted.",
        "counting_unit": "One declared Python test_* function/method, Solidity test* function, or explicit Node test(...) declaration; parameters, loops, subtests and CI reruns are not expanded; conditional skips included.",
        "classification_rules": [
            "U: isolated production function/module/contract/library, fixtures/mocks, pure/source/configuration checks.",
            "I: asserted behavior crosses a real production API/service/process boundary or actively composes production components; external dependencies may remain mocked.",
            "Classification is assertion-specific: fixture construction, filenames and end_to_end in a name do not determine the category.",
            "The exact reviewed integration whitelist is encoded in inventory_tests.py; all other inventoried definitions are U.",
            "System E2E means an automated complete application lifecycle; none is defined in this inventory.",
            "Production is an execution context, not an additional test level; no automated production execution is established by this static inventory.",
        ],
        "counts": {
            "definitions": len(rows), "test_files": test_file_count,
            "by_language": dict(sorted(counts.items())),
            "by_category": {U: categories[U], I: categories[I], S: 0},
            "automated_production_context_definitions_identified": 0,
        },
        "sources": dict(sorted(sources.items())),
        "separate_evidence": [
            {"kind": "ci_service_readiness_check", "name": "Anvil JSON-RPC readiness", "path": CI, "ci_job": "runtime-smoke-test", "check": "eth_chainId", "count": 1, "status": "Configured; not executed by this inventory"},
            {"kind": "ci_service_readiness_check", "name": "IPFS API readiness", "path": CI, "ci_job": "runtime-smoke-test", "check": "/api/v0/version", "count": 1, "status": "Configured; not executed by this inventory"},
            {"kind": "manual_deployed_run_record", "name": "Recorded Phala workflow", "path": "data/evaluation/authoritative-phala-6w-24r-20260901/README.md", "count": 1, "scope": "Existing record: six workers, 24 training rounds and final inference. Separate from automated definitions; no new execution or production qualification asserted."},
        ],
        "tests": rows,
    }


def markdown(data):
    rows = data["tests"]
    grouped = defaultdict(Counter)
    for row in rows:
        grouped[row["ci_job"]][row["category"]] += 1
    out = [
        "# Static test inventory", "",
        "**808 implemented test definitions: 731 unit/component, 77 local integration, 0 complete automated system E2E.**", "",
        "This is a source inventory, not an execution report. No pass rate, successful CI run or new test result is claimed. Production is an execution context, not a fourth test level.", "",
        "| Test type | Definitions | Boundary |", "|---|---:|---|",
        "| Unit/component | 731 | Isolated functions, modules, contracts, crypto, guards, source and configuration checks; dependencies controlled |",
        "| Local integration | 77 | Actual API/socket/process boundaries or asserted collaboration of production components; selected dependencies can remain mocked |",
        "| Complete system E2E | 0 | No automated full application lifecycle established in the selected CI test definitions |", "",
        "Languages: **569 Python, 138 Solidity, 101 Node**; **96 test files**.", "",
        "## Counting and classification rules", "",
    ]
    out.extend("- " + rule for rule in data["classification_rules"])
    out.extend([
        "- Count declarations, not executions. Parametrization, subtests, loops and duplicate runs in publisher workflows are not expanded.",
        "- Conditional skips remain included: local model fixtures, Terraform, nginx, Smallstep binaries and Docker availability can affect executed counts.",
        "- Python uses static AST traversal; Solidity and Node use static declaration matching for this checkout's source style. Tests are never imported or collected.",
        "- A model-inference function or Hybrid-R test named end_to_end remains a component test. Direct control-API calls with mocked dependencies remain component tests; ASGI/HTTP requests exercise integration boundaries.",
        "- Only the positive AIR-v2 service-emitter/agent-verifier compatibility test is classified as integration in test_ratls.py; isolated rejection guards stay component tests despite a composed fixture.",
        "- Solidity integration requires the assertion to traverse actual production contracts. Cross-contract setup alone and a mocked TDX verifier do not establish that scope.",
        "- This checkout includes newer RA-TLS definitions. Their inventory must not be attributed to the historical mTLS/AIR-v1 cloud run.", "",
        "## CI execution configuration", "",
        "Primary source: [ci.yml](../../../vita-fl/.github/workflows/ci.yml). CI is configured for push/PR on main and phala_app_key, and manual dispatch. The table describes configured execution, not an observed outcome.", "",
        "| CI job | Unit/component | Local integration | Command scope |", "|---|---:|---:|---|",
    ])
    scopes = {
        "python-quality": "pytest agent/tests and tee_inference/tests; unittest discovery for DFL neural/container, ZK, control API, Phala and transparency-log tests",
        "transport-pki": "pytest transport_security/tests pki/tests; CI installs/checks nginx, step and step-ca",
        "node-server": "npm test → node --test in dfl/node_server",
        "smart-contracts": "forge test -vvv plus node --test test/*.test.mjs",
        "docker-builds": "unittest test_docker_build_contexts.py, only matrix.name == tee-inference",
    }
    for job in scopes:
        out.append("| {} | {} | {} | {} |".format(job, grouped[job][U], grouped[job][I], scopes[job]))
    out.extend([
        "", "Publisher workflows can rerun subsets; those invocations do not create additional definitions.", "",
        "## Separate evidence, excluded from 808", "",
        "- **2 configured service-readiness checks** in runtime-smoke-test: Anvil eth_chainId and IPFS /api/v0/version. They do not execute the full training/inference lifecycle.",
        "- **1 existing manual Phala workflow record**: data/evaluation/authoritative-phala-6w-24r-20260901/README.md (six workers, 24 training rounds and final inference). No new cloud run, full recovery experiment or production qualification is claimed.", "",
        "## Representative assertions", "",
        "| Category | Test | Scope |", "|---|---|---|",
    ])
    examples = [
        ("dfl/neural_network/tests/test_dicom_provenance.py", "test_modified_label_is_rejected"),
        ("agent/tests/test_tee_inference_client.py", "test_request_substitution_is_rejected"),
        ("tee_inference/tests/test_authorization.py", "test_publication_failure_cannot_return_success_without_receipt"),
        ("smart_contracts/test/GMStorageAggregatorReward.t.sol", "testAtomicFinalizationPublishesAdvancesAndRewardsExactlyOnce"),
        ("pki/tests/test_step_ca_integration.py", "test_real_ca_one_use_renewal_and_active_revocation"),
    ]
    lookup = {(row["path"], row["name"]): row for row in rows}
    for example in examples:
        row = lookup[example]
        out.append("| {} | `{}:{}::{}` | {} |".format(row["category"], row["path"], row["line"], row["name"], row["reason"]))
    out.extend([
        "", "## Reproduce and audit", "",
        "From the workspace root:", "", "```bash",
        "presentation/.venv/bin/python presentation/concepts/test-evaluation/inventory_tests.py", "```", "",
        "The script asserts 808 = 569 + 138 + 101 and the reviewed 731/77 split, rejecting stale whitelist entries or duplicate identifiers. It writes test-inventory.json, test-inventory.csv and this overview. Each test row includes path, line, name, category, rationale, CI job, source SHA-256 and commit.", "",
        "- Commit: `{}`".format(data["commit"]),
        "- Tracked working-tree changes present: `{}`".format(data["working_tree_dirty"]),
        "- Combined source SHA-256: `{}`".format(data["source_sha256"]),
        "- Inventory script SHA-256: `{}`".format(data["inventory_script_sha256"]),
        "- Generated UTC: `{}`".format(data["generated_at_utc"]), "",
        "The commit identifies the base revision; per-file content hashes identify the actual inspected working tree. The combined hash covers every inventoried test file, ci.yml and the Node package.json. It does not hash every production implementation dependency.", "",
        "Machine-readable outputs contain the complete per-definition classification and source-hash manifest. Static classification is a documented operational convention for this evaluation, not a universal taxonomy.", "",
    ])
    return "\n".join(out)


def main():
    data = inventory()
    (HERE / "test-inventory.json").write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    with (HERE / "test-inventory.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(data["tests"][0]))
        writer.writeheader()
        writer.writerows(data["tests"])
    (HERE / "test-inventory.md").write_text(markdown(data), encoding="utf-8")
    print(json.dumps({"counts": data["counts"], "commit": data["commit"], "source_sha256": data["source_sha256"]}, indent=2))


if __name__ == "__main__":
    main()
