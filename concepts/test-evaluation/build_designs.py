#!/usr/bin/env python3
"""Build four editable evaluation proposals without changing the approved deck."""
import hashlib
import json
from pathlib import Path
import sys

from PIL import Image, ImageDraw, ImageFont
from pptx import Presentation

import common as c
import design_a
import design_b
import design_c
import design_d

sys.path.insert(0, str(c.ROOT / "concepts" / "color-navigation"))
from build_concepts import check_layout

DESIGNS = [
    ("a-test-matrix", "A · Vergleichsmatrix", design_a),
    ("b-architecture-map", "B · Tests entlang der Architektur", design_b),
    ("c-fault-scenarios", "C · Drei konkrete Fehlerszenarien", design_c),
    ("d-evaluation-levels", "D · Drei Ebenen der Evaluation", design_d),
]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_bounds(prs):
    for page_index, slide in enumerate(prs.slides, 1):
        for shape in slide.shapes:
            # Tiny rounded-end connector overhang is harmless; text is stricter.
            margin = int(c.b.Inches(.035))
            if shape.left < -margin or shape.top < -margin:
                raise AssertionError(f"Slide {page_index}: off-canvas {shape.name}")
            if shape.left + shape.width > prs.slide_width + margin:
                raise AssertionError(f"Slide {page_index}: right overflow {shape.name}")
            if shape.top + shape.height > prs.slide_height + margin:
                raise AssertionError(f"Slide {page_index}: bottom overflow {shape.name}")


def main():
    main_deck = c.ROOT / "VITA-FL_Thesis_Presentation_TU_Berlin.pptx"
    before = digest(main_deck)
    c.verify_sources()
    prs = c.b.prepare_template()
    prs.core_properties.title = "VITA-FL — Existing tests: four evaluation slide alternatives"
    for _, _, module in DESIGNS:
        module.build(prs)
    check_layout(prs)
    check_bounds(prs)
    output = c.HERE / "VITA-FL_Test_Evaluation_Alternatives.pptx"
    prs.save(output)
    reopened = Presentation(output)
    previews = []
    for slide, (slug, _, module) in zip(reopened.slides, DESIGNS):
        assert "SOURCE MAP" in slide.notes_slide.notes_text_frame.text
        preview = c.renderer.render_slide(reopened, slide)
        preview.save(c.HERE / (slug + ".png"))
        previews.append(preview)
        individual = c.b.prepare_template()
        module.build(individual)
        individual.save(c.HERE / (slug + ".pptx"))

    previews[0].save(c.HERE / "VITA-FL_Test_Evaluation_Alternatives.pdf",
                     save_all=True, append_images=previews[1:], resolution=120)
    overview = Image.new("RGB", (1660, 1040), "#E8ECEF")
    draw = ImageDraw.Draw(overview)
    font = ImageFont.truetype(c.renderer.FONT_BOLD, 21)
    for index, (preview, (_, label, _)) in enumerate(zip(previews, DESIGNS)):
        x, y = 20 + (index % 2) * 820, 16 + (index // 2) * 515
        draw.text((x + 4, y), label, font=font, fill="#263440")
        overview.paste(preview.resize((800, 450), Image.Resampling.LANCZOS), (x, y + 37))
    overview.save(c.HERE / "overview.png")
    assert digest(main_deck) == before, "Main presentation was modified"
    source_map = []
    for path, symbols in c.SOURCES:
        content = (c.REPO / path).read_text()
        source_map.append({"path": path, "tests": [
            {"name": symbol, "line": content[:content.index(symbol)].count("\n") + 1}
            for symbol in symbols]})
    (c.HERE / "validation.json").write_text(json.dumps({
        "variant_count": len(prs.slides), "layout": "passed", "bounds": "passed",
        "speaker_notes": "present", "source_symbols": "verified",
        "test_execution": "not performed; slide proposals inventory existing implementations",
        "main_deck_unchanged": True, "main_deck_sha256": before,
        "source_map": source_map,
    }, indent=2) + "\n")
    print("Built 4 editable alternatives, 4 individual PPTX files, PNG previews, PDF and overview.")
    print("Layout, source references and preservation of the main deck checked.")


if __name__ == "__main__":
    main()
