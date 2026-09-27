#!/usr/bin/env python3
"""Build approved A: CI coverage and external scenarios, for current Page 26."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys

from pptx import Presentation

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PROPOSALS = HERE / 'ci-external'
SOURCE = PROPOSALS / 'a-two-catalogs.pptx'
sys.path.insert(0, str(ROOT))
import build_presentation as b
import render_preview as renderer
sys.path.insert(0, str(ROOT / 'concepts/color-navigation'))
from build_concepts import check_layout


def verify_inventory():
    inventory = json.loads((PROPOSALS / 'ci-inventory.json').read_text())
    data = json.loads((PROPOSALS / 'slide-data.json').read_text())
    assert len(inventory['tests']) == 878
    assert len({t['id'] for t in inventory['tests']}) == 878
    counts = Counter(t['functional_group'] for t in inventory['tests'])
    assert counts == {g['id']: g['count'] for g in data['ci_groups']}
    assert sum(counts.values()) == 878 and len(counts) == 7
    for name, expected in inventory['source_files'].items():
        actual = hashlib.sha256((ROOT.parent / 'vita-fl' / name).read_bytes()).hexdigest()
        assert actual == expected, 'Refresh the CI inventory before rebuilding: ' + name
    external = json.loads((PROPOSALS / 'external-scope.json').read_text())
    assert external['considered_scenarios_total'] == 8
    assert sum(g['count'] or 0 for g in external['groups']) == 8
    return inventory


def build(prs, page_number=26):
    source = Presentation(SOURCE)
    assert len(source.slides) == 1
    slide = prs.slides.add_slide(prs.slide_masters[1].slide_layouts[0])
    b._apply_native_evaluation_asset(
        slide, page_number, str(SOURCE), b.TEST_EVALUATION_SLIDE_NAME,
    )
    original_notes = source.slides[0].notes_slide.notes_text_frame.text
    _, details = original_notes.split('\nCI BOUNDARY AND COUNTING\n', 1)
    details = details.replace(
        'A cross-boundary mapping in variant B connects related questions, not equivalent\n'
        'coverage or one-to-one test cases. Some code properties have no live fault probe.\n',
        'Some code properties have no live fault probe.\n',
    )
    notes = '''SELECTED VARIANT A — CI CHECKS AND EXTERNAL SYSTEM TESTS

PURPOSE
Approved replacement for Page 26. The left catalog combines unit/component and
local integration tests under CI, grouped by the subject under test. The right
catalog explains external scenario types and their expected responses. Counts
refer to implementations, not passed executions or independent samples.
The source/configuration snapshot is dated 27 September 2026. No test or cloud
campaign was executed to build this slide. The adjacent historical 24-round
Phala experiment remains separate evidence; it is not attributed to the current
SMEW/SMA/test-driver profile.

CI BOUNDARY AND COUNTING
''' + details
    notes += '\nInventory paths are relative to presentation/concepts/test-evaluation/ci-external/.\n'
    b.add_note(slide, notes)
    return slide


def main():
    inventory = verify_inventory()
    prs = b.prepare_template()
    prs.core_properties.title = 'VITA-FL — CI checks and external system tests'
    build(prs)
    check_layout(prs)
    output = ROOT / 'assets/test-evaluation-a.pptx'
    prs.save(output)
    reopened = Presentation(output)
    check_layout(reopened)
    visible = '\n'.join(s.text for s in reopened.slides[0].shapes if s.has_text_frame)
    assert '878' in visible and '8 modes + audit' in visible
    assert 'Page 26' in visible and 'Variant A' not in visible
    preview = renderer.render_slide(reopened, reopened.slides[0])
    preview.save(HERE / 'a-test-categories.png')
    preview.save(HERE / 'a-test-categories.pdf', resolution=120)
    (HERE / 'selected-validation.json').write_text(json.dumps({
        'page': 26, 'selected_variant': 'ci-external/a-two-catalogs',
        'layout': 'passed', 'bounds': 'passed', 'native_editable_slide': True,
        'ci_definitions': 878, 'ci_subject_groups': 7,
        'external_scenario_modes': 8, 'security_scenario_checks': 16,
        'cross_scenario_receipt_audit_checks': 17,
        'test_execution': 'not performed; implementation counts, not pass counts',
        'inventory_commit': inventory['commit'],
        'inventory_source_sha256': inventory['source_sha256'],
        'source_asset_sha256': hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        'asset': str(output.relative_to(ROOT)),
    }, indent=2) + '\n')
    print('Built approved A for Page 26: 878 CI definitions, 8 external modes + receipt audit.')


if __name__ == '__main__':
    main()
