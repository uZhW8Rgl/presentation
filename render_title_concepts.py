#!/usr/bin/env python3
"""Render alternative middle/right designs for the unchanged title slide."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw

from render_dfl_concepts import (
    BLUE,
    DARK,
    GREEN,
    ORANGE,
    TU_RED,
    WHITE,
    font,
)


ROOT = Path(__file__).resolve().parent
PRESENTATION = ROOT
BASE = PRESENTATION / "preview" / "slide-01.png"
OUTPUT = PRESENTATION / "concepts"

TU_RED_DARK = "#A20B19"
TU_RED_LIGHT = "#D74655"
RIGHT = (850, 220, 1600, 755)


def canvas() -> Image.Image:
    image = Image.open(BASE).convert("RGB")
    ImageDraw.Draw(image).rectangle(RIGHT, fill=TU_RED)
    return image


def line_arrow(draw: ImageDraw.ImageDraw, start, end, fill=WHITE, width=4) -> None:
    draw.line((*start, *end), fill=fill, width=width)
    x, y = end
    draw.polygon(((x, y), (x - 13, y - 8), (x - 13, y + 8)), fill=fill)


def concept_a_evidence_lens() -> Image.Image:
    image = canvas()
    draw = ImageDraw.Draw(image)
    draw.text((1233, 235), "WHAT MAKES A RESULT INSPECTABLE?", font=font(16, True), fill=WHITE, anchor="mm")

    center = (1233, 462)
    outer_nodes = [
        ((969, 423), "MODEL\nORIGIN", GREEN),
        ((1233, 300), "MEASURED\nEXECUTION", BLUE),
        ((1491, 423), "LOG\nINCLUSION", ORANGE),
    ]
    for (cx, cy), label, accent in outer_nodes:
        draw.line((cx, cy, *center), fill="#F2A8B0", width=4)
        draw.ellipse((cx - 58, cy - 58, cx + 58, cy + 58), fill=TU_RED_DARK, outline=WHITE, width=3)
        draw.ellipse((cx - 9, cy - 30, cx + 9, cy - 12), fill=accent)
        draw.multiline_text((cx, cy + 9), label, font=font(12, True), fill=WHITE, anchor="ma", align="center", spacing=1)

    draw.ellipse((center[0] - 108, center[1] - 108, center[0] + 108, center[1] + 108), fill=TU_RED_DARK, outline=WHITE, width=4)
    draw.text(center, "RESULT", font=font(29, True), fill=WHITE, anchor="mm")
    draw.text((center[0], center[1] + 42), "one concrete inference", font=font(13), fill=WHITE, anchor="mm")
    draw.text((1233, 665), "Evidence converges on one concrete result.", font=font(18, True), fill=WHITE, anchor="mm")
    return image


def concept_b_three_questions() -> Image.Image:
    image = canvas()
    draw = ImageDraw.Draw(image)
    draw.rectangle((70, 530, 825, 615), fill=TU_RED)
    draw.text(
        (925, 285),
        "ARCHITECTURE DESIGN FOR VERIFIABLE AI WORKFLOWS",
        font=font(16, True),
        fill="#F7BBC1",
    )
    questions = ["Which model?", "Which input?", "Which workload?"]
    for index, question in enumerate(questions):
        y = 352 + index * 94
        draw.text((925, y - 8), question, font=font(34, True), fill=WHITE)
        draw.line((925, y + 52, 1508, y + 52), fill="#E66B77", width=2)
    return image


def concept_c_two_domain_bridge() -> Image.Image:
    image = canvas()
    draw = ImageDraw.Draw(image)
    draw.text((917, 281), "THE CONTRIBUTION IN ONE VIEW", font=font(16, True), fill="#F7BBC1")

    left_center = (1005, 445)
    right_center = (1442, 445)
    for center, accent, heading, body in [
        (left_center, GREEN, "MODEL", "Decentralized\nproduction"),
        (right_center, BLUE, "RESULT", "AI-assisted\ndiagnosis"),
    ]:
        cx, cy = center
        draw.ellipse((cx - 112, cy - 112, cx + 112, cy + 112), fill=TU_RED_DARK, outline=WHITE, width=4)
        draw.ellipse((cx - 18, cy - 18, cx + 18, cy + 18), fill=accent)
        draw.text((cx, cy - 52), heading, font=font(22, True), fill=WHITE, anchor="mm")
        draw.multiline_text((cx, cy + 50), body, font=font(16, True), fill=WHITE, anchor="mm", align="center", spacing=3)

    draw.line((1117, 445, 1330, 445), fill=WHITE, width=5)
    draw.polygon(((1330, 445), (1311, 433), (1311, 457)), fill=WHITE)
    draw.rounded_rectangle((1115, 360, 1332, 420), radius=18, fill=WHITE)
    draw.multiline_text((1224, 389), "ATTESTED, TRACEABLE\nHANDOFF", font=font(13, True), fill=TU_RED_DARK, anchor="mm", align="center", spacing=1)
    draw.text((1224, 640), "From collaborative training to accountable use.", font=font(18, True), fill=WHITE, anchor="mm")
    return image


def concept_d_minimal_typography() -> Image.Image:
    image = canvas()
    draw = ImageDraw.Draw(image)
    draw.text((916, 267), "VITA-FL", font=font(91, True), fill=TU_RED_LIGHT)
    draw.line((921, 382, 1513, 382), fill=WHITE, width=3)

    verbs = [("TRAIN", GREEN), ("ATTEST", BLUE), ("VERIFY", ORANGE)]
    for index, (verb, accent) in enumerate(verbs):
        y = 423 + index * 76
        draw.rectangle((921, y + 10, 935, y + 53), fill=accent)
        draw.text((963, y), verb, font=font(37, True), fill=WHITE)
    draw.text((921, 680), "One path. One accountable result.", font=font(19, True), fill=WHITE)
    return image


def contact_sheet(variants: list[tuple[str, Image.Image]]) -> Image.Image:
    thumb_w = 720
    thumb_h = 405
    gutter = 28
    sheet = Image.new("RGB", (thumb_w * 2 + gutter * 3, thumb_h * 2 + gutter * 3), (221, 229, 234))
    positions = [(gutter, gutter), (gutter * 2 + thumb_w, gutter), (gutter, gutter * 2 + thumb_h), (gutter * 2 + thumb_w, gutter * 2 + thumb_h)]
    for (label, image), position in zip(variants, positions):
        thumb = image.resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
        sheet.paste(thumb, position)
        x, y = position
        draw = ImageDraw.Draw(sheet)
        draw.rounded_rectangle(
            (x + thumb_w - 72, y + thumb_h - 54, x + thumb_w - 18, y + thumb_h - 17),
            radius=9,
            fill=TU_RED_DARK,
            outline=WHITE,
            width=1,
        )
        draw.text(
            (x + thumb_w - 45, y + thumb_h - 35),
            label,
            font=font(17, True),
            fill=WHITE,
            anchor="mm",
        )
    return sheet


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    variants = [
        ("A", concept_a_evidence_lens()),
        ("B", concept_b_three_questions()),
        ("C", concept_c_two_domain_bridge()),
        ("D", concept_d_minimal_typography()),
    ]
    names = {
        "A": "title-concept-a-evidence-lens.png",
        "B": "title-concept-b-three-questions.png",
        "C": "title-concept-c-two-domain-bridge.png",
        "D": "title-concept-d-minimal-typography.png",
    }
    for label, image in variants:
        destination = OUTPUT / names[label]
        image.save(destination, quality=95)
        print(destination)
    sheet = OUTPUT / "title-concepts-contact-sheet.png"
    contact_sheet(variants).save(sheet, quality=95)
    print(sheet)


if __name__ == "__main__":
    main()
