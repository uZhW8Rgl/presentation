#!/usr/bin/env python3
"""Insert/update the six approved attack trees after Page 23, preserving existing edits."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import tempfile
from zipfile import ZipFile

from pptx import Presentation

import build_presentation as b
from update_slide25_test_evaluation import footer, snapshot, visible

ROOT = Path(__file__).resolve().parent
DECK = ROOT / 'VITA-FL_Thesis_Presentation_TU_Berlin.pptx'
ASSET = b.ATTACK_TREE_ASSET
RECORD = ROOT / 'assets/attack-trees-integration.json'
CHAPTER = ROOT.parent / 'overleaf/chapters/chapter4.tex'
TARGET = 23
COUNT = len(b.ATTACK_TREE_SLUGS)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_structure(prs):
    assert len(prs.slides) == 52, 'Expected 35 talk pages and 17 backup pages'
    assert len(prs.slide_masters) == 2
    names = [b.ATTACK_TREE_SLIDE_PREFIX + slug for slug in b.ATTACK_TREE_SLUGS]
    assert [prs.slides[i].name for i in range(TARGET, TARGET + COUNT)] == names
    assert sum(s.name.startswith(b.ATTACK_TREE_SLIDE_PREFIX) for s in prs.slides) == COUNT
    for i, text in ((22, 'Cryptographic chain of custody'), (30, 'One end-to-end Phala FedAvg run'),
                    (34, 'Conclusion and outlook'), (35, 'Training and inference share one verified image')):
        assert text in visible(prs.slides[i]), (i, text)
    assert prs.slides[29].name == b.EVALUATION_STACK_SLIDE_NAME
    assert prs.slides[31].name == b.TEST_EVALUATION_SLIDE_NAME
    for page, slide in enumerate(prs.slides, 1):
        assert slide.notes_slide.notes_text_frame.text.strip(), f'Empty notes on Page {page}'
        if page > 1:
            assert footer(slide).text == f'Page {page}'
        ids = [node.get('id') for node in slide.element.xpath('.//p:cNvPr')]
        assert len(ids) == len(set(ids)), f'Duplicate shape IDs on Page {page}'
        if TARGET < page <= TARGET + COUNT:
            assert 'TREE-SPECIFIC MODEL' in slide.notes_slide.notes_text_frame.text
            assert 'B light ·' not in visible(slide)
            assert sum(s.name.startswith('Attack legend swatch: ') for s in slide.shapes) == 4
            assert sum(s.name.startswith('Attack legend label: ') for s in slide.shapes) == 4
            assert not slide.element.xpath('.//a:blip'), 'Attack trees must remain native and editable'
            for s in slide.shapes:
                assert s.left >= 0 and s.top >= 0
                assert s.left + s.width <= prs.slide_width + 12700
                assert s.top + s.height <= prs.slide_height + 12700
    return prs


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--render', action='store_true', help='Refresh all deck previews')
    args = parser.parse_args()
    assert ASSET.is_file()
    prs = Presentation(DECK)
    old_count = len(prs.slides)
    assert old_count in (46, 52), 'Unexpected deck size; refusing to overwrite'
    inserting = old_count == 46
    if inserting:
        assert 'Cryptographic chain of custody' in visible(prs.slides[22])
        assert prs.slides[23].name == b.EVALUATION_STACK_SLIDE_NAME
        assert not any(s.name.startswith(b.ATTACK_TREE_SLIDE_PREFIX) for s in prs.slides)
    else:
        check_structure(prs)
    source = Presentation(ASSET)
    assert len(source.slides) == COUNT
    before = [snapshot(s) for s in prs.slides]
    before_hash = digest(DECK)
    chapter_hash = digest(CHAPTER)
    backup = Path(tempfile.mkdtemp(prefix='vita-fl-before-attack-trees-')) / DECK.name
    shutil.copy2(DECK, backup)
    if inserting:
        b.insert_attack_tree_slides(prs, TARGET)
    else:
        for i, (asset_slide, slug) in enumerate(zip(source.slides, b.ATTACK_TREE_SLUGS)):
            b.apply_attack_tree_asset(prs.slides[TARGET + i], asset_slide, TARGET + i + 1, slug)
    check_structure(prs)

    handle, filename = tempfile.mkstemp(prefix='.attack-trees-', suffix='.pptx', dir=ROOT)
    os.close(handle)
    candidate = Path(filename)
    try:
        prs.save(candidate)
        checked = check_structure(Presentation(candidate))
        preserved = 0
        for index, old in enumerate(before):
            if not inserting and TARGET <= index < TARGET + COUNT:
                continue
            new_index = index + (COUNT if inserting and index >= TARGET else 0)
            assert snapshot(checked.slides[new_index]) == old, \
                f'Existing Page {index + 1} changed beyond its footer'
            preserved += 1
        for i, asset_slide in enumerate(source.slides):
            integrated = checked.slides[TARGET + i]
            assert integrated.notes_slide.notes_text_frame.text == asset_slide.notes_slide.notes_text_frame.text
            assert len(integrated.shapes) == len(asset_slide.shapes)
            for approved, actual in zip(asset_slide.shapes, integrated.shapes):
                if approved.has_text_frame and approved.text.startswith('B light · '):
                    continue
                assert approved.element.xml == actual.element.xml, (i, approved.name)
        with ZipFile(backup) as old_zip, ZipFile(candidate) as new_zip:
            assert new_zip.testzip() is None
            for name in old_zip.namelist():
                if name.startswith(('ppt/media/', 'ppt/slideMasters/', 'ppt/slideLayouts/', 'ppt/notesMasters/')):
                    assert old_zip.read(name) == new_zip.read(name), name
        # Exercise the same generator hook without regenerating the user's existing slides.
        generated = b.prepare_template()
        for _ in range(TARGET):
            generated.slides.add_slide(generated.slide_masters[1].slide_layouts[0])
        b.insert_attack_tree_slides(generated, TARGET)
        for i in range(COUNT):
            assert visible(generated.slides[TARGET + i]) == visible(checked.slides[TARGET + i])
            assert generated.slides[TARGET + i].notes_slide.notes_text_frame.text == source.slides[i].notes_slide.notes_text_frame.text
        assert digest(CHAPTER) == chapter_hash
        os.replace(candidate, DECK)
    finally:
        candidate.unlink(missing_ok=True)

    RECORD.write_text(json.dumps({
        'pages': list(range(24, 30)), 'slides_before': old_count, 'slides_after': 52,
        'talk_pages': 35, 'backup_pages': 17, 'mode': 'insert' if inserting else 'replace',
        'preserved_other_slides_and_notes': preserved,
        'allowed_existing_change': 'page-number footers only on insertion; none outside trees on update',
        'main_deck_sha256_before': before_hash, 'main_deck_sha256_after': digest(DECK),
        'asset_sha256': digest(ASSET), 'chapter4_sha256': chapter_hash, 'chapter4_unchanged': True,
        'backup': str(backup), 'structure_check': 'passed', 'generator_hook': 'passed',
        'approved_shape_xml_preserved_except_footer': True, 'source_notes_preserved': True,
        'media_masters_layouts_unchanged': True, 'native_editable_shapes': True,
        'visual_review': 'pending',
    }, indent=2) + '\n')
    if args.render:
        import render_preview
        render_preview.main()
    print(f'{"Inserted" if inserting else "Updated"} attack trees on Pages 24–29; 52 pages (35 talk, 17 backup).')
    print(f'Preserved {preserved} existing slides and notes; backup: {backup}')
    print(f'Checks: {RECORD}')


if __name__ == '__main__':
    main()
