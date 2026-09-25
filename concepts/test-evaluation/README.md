# Evaluation slide alternatives

## Selected A: counts by test type

The chosen matrix is refined into a strict test-type overview and inserted as
Page 25. `assets/test-evaluation-a.pptx` is the native editable source asset;
`a-test-categories.png` and `.pdf` preview the selected version.

The audited static inventory contains **808 definitions: 731 unit/component and
77 local integration tests**. It includes current RA-TLS, legacy mTLS, ZK and
deployment-helper tests. These are current-code implementation counts, not
passed executions or the exact code version of the historical Phala run.
No automated complete training-to-inference suite or dedicated production-test
suite was identified. The one recorded Phala run and two CI service smoke
checks are shown separately. Production denotes an execution context rather
than a formal additional test level.

- `test-inventory.csv`: each definition, source location, category and CI job.
- `test-inventory.json`: the complete inventory, source hashes and scope metadata.
- `test-inventory.md`: classification rules, boundary decisions and CI mapping.
- `inventory_tests.py`: reproduce the source count without importing/running tests.
- `build_selected.py`: rebuild the selected editable slide and previews.
- `selected-validation.json`: layout and count checks for the selected slide.

From the presentation repository, run:

```bash
.venv/bin/python concepts/test-evaluation/inventory_tests.py
.venv/bin/python concepts/test-evaluation/build_selected.py
.venv/bin/python update_slide25_test_evaluation.py
```

The original four alternatives below remain available for comparison. Their
legacy-profile example selection differs from the full current-code inventory.

## Original proposals

Four deliberately different, editable one-slide proposals for the existing
English VITA-FL presentation. These describe implemented tests and their scope;
they do not report a new test execution or introduce new pass counts.

| Variant | Visual approach | Presentation purpose |
|---|---|---|
| A — Test matrix | Five rows map system boundary, assertion, source file and test type | Most explicit answer to which tests are implemented where |
| B — Architecture map | Test probes attach to four components along the model-use path | Explain the coverage while referring back to the architecture |
| C — Fault scenarios | Three horizontal fault → check → expected-response sequences | Explain the meaning of a negative test with concrete examples |
| D — Evaluation levels | A staircase separates component, service and deployed-system evidence | Explain why the different kinds of evidence complement each other |

The proposals use native PowerPoint text, shapes and connectors. The official
TU Berlin template, English language, DFL/Agent navigation and established
domain colors are retained. Exact paths, test function names, test doubles and
claim limitations are documented in every slide's speaker notes.

## Files

- `VITA-FL_Test_Evaluation_Alternatives.pptx`: four editable alternatives.
- `VITA-FL_Test_Evaluation_Alternatives.pdf`: convenient preview export.
- `a-test-matrix.pptx` through `d-evaluation-levels.pptx`: individual editable slides.
- `overview.png`: comparison sheet; individual PNG files provide full-size previews.
- `validation.json`: layout/source checks and proof the main deck was preserved.
- `build_designs.py`, `common.py`, `design_*.py`: reproducible native-slide sources.

Suggested placement after selection: after current Page 24, before the learning
curves. The main deck is deliberately not rebuilt: its existing manual edits
must be retained when inserting the chosen native slide.

## Scope

The selected cases cover training-data signatures, local contract/abort rules,
encrypted model exchange, inference-request and receipt bindings, and receiver
error handling. Component tests use real application code with controlled
dependencies. ASGI service integration is local; hardware, registry and log
fixtures do not establish the corresponding cloud behavior.

The separate Phala record contains six workers, 24 training rounds and one final
inference. It did not trigger aggregator recovery. Local quorum and abort tests
must not be presented as a complete measured cloud failover. These examples
remain aligned with the legacy mTLS/AIR-v1 presentation profile; newer RA-TLS
tests are not folded into the old run's evidence.

## Regenerate

From the presentation repository:

```bash
.venv/bin/python concepts/test-evaluation/build_designs.py
```

The PNG/PDF exports use the repository's approximate renderer. Native text and
diagrams remain editable in PPTX; final font wrapping should be checked in the
PowerPoint installation used for presenting.
