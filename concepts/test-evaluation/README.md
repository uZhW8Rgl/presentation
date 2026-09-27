# Evaluation slide alternatives

## Selected A: CI checks and external system tests

**Variant A — Two catalogs** from the [CI/external proposals](ci-external/README.md)
is selected for Page 26 of the main presentation, replacing the earlier
matrix by test type. `assets/test-evaluation-a.pptx` is the approved native,
editable source asset; `a-test-categories.png` and `.pdf` preview the selected
version. The main deck remains at **46 pages**.

The left catalog combines unit, component and integration tests into one CI
block: **878 unique definitions in seven subject groups**. The right catalog
covers **eight external scenario modes**, plus a cross-scenario receipt audit
with **17 checks**. The `security` mode has **16 checks including a positive
inference control**. Definitions, modes and checks are separate counting units;
none denotes a passed execution. Manipulation and adversarial tool-order tests
remain outside the selected external scope.

The current Phala training profile has six workers, five successful
non-bootstrap rounds, client limit five and a 45-second collection deadline.
`configuration` checks setup only; the current profile also trains before
`inference`. These settings do not describe every historical run.

- `ci-external/ci-inventory.json` and `.md`: current CI inventory, grouping and source metadata.
- `ci-external/external-scope.json`: external modes, assertions, configuration and evidence boundaries.
- `ci-external/slide-data.json`: presentation labels and subject mapping.
- `build_selected.py`: rebuild the selected editable slide and previews.
- `selected-validation.json`: checks recorded by the selected-slide builder.

From the presentation repository, run:

```bash
.venv/bin/python concepts/test-evaluation/build_selected.py
.venv/bin/python update_slide25_test_evaluation.py --render
```

The updater replaces the test slide on Page 26 while retaining the other slides
and existing PowerPoint edits. The historical `inventory_tests.py` is not a
prerequisite for the current selected builder.

## Historical inventory and previous selected matrix

The previous matrix used **808 definitions: 731 unit/component and 77 local
integration tests**. These figures belong only to the historical
`test-inventory.csv`, `test-inventory.json` and `test-inventory.md` files and
their earlier source snapshot. `inventory_tests.py` is the corresponding
historical inventory tool; it is not the current 878-definition inventory.

That inventory included RA-TLS, legacy mTLS, ZK and deployment-helper tests.
Its absence of an automated complete training-to-inference suite or dedicated
production-test suite describes the historical CI inventory, not the current
external scenario implementation. The one recorded Phala run and two CI
service smoke checks were separate from its definition count. Production
identified an execution context rather than an additional formal test level.

The original four alternatives below remain available for comparison. Their
legacy-profile example selection differs from the current CI/external catalog.

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

These original alternatives are historical proposals. The current selected
CI/external variant A occupies Page 26, after the cloud-run overview on Page 25
and before the learning curves on Page 27. Its updater retains existing manual
edits elsewhere in the main deck.

## Historical proposal scope

The original cases cover training-data signatures, local contract/abort rules,
encrypted model exchange, inference-request and receipt bindings, and receiver
error handling. Component tests use real application code with controlled
dependencies. ASGI service integration is local; hardware, registry and log
fixtures do not establish the corresponding cloud behavior.

The separate Phala record contains six workers, 24 training rounds and one final
inference. It did not trigger aggregator recovery. Local quorum and abort tests
must not be presented as a complete measured cloud failover. These examples
remain aligned with the legacy mTLS/AIR-v1 presentation profile; newer RA-TLS
tests are not folded into the old run's evidence.

## Regenerate the original proposals

To recreate the historical four-proposal comparison, from the presentation repository:

```bash
.venv/bin/python concepts/test-evaluation/build_designs.py
```

The PNG/PDF exports use the repository's approximate renderer. Native text and
diagrams remain editable in PPTX; final font wrapping should be checked in the
PowerPoint installation used for presenting.
