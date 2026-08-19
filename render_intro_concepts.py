#!/usr/bin/env python3
"""Render three self-introduction slide concepts for visual selection."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw

from render_dfl_concepts import (
    BLUE,
    BLUE_TINT,
    BORDER,
    DARK,
    GREEN,
    GREEN_TINT,
    LIGHT,
    ORANGE,
    ORANGE_TINT,
    RED_TINT,
    TU_RED,
    WHITE,
    base_slide,
    centered,
    font,
    rounded,
)


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "concepts"


def portrait_placeholder(draw: ImageDraw.ImageDraw, box, accent=TU_RED, dark=False, label=True):
    left, top, right, bottom = box
    fill = "#343434" if dark else LIGHT
    line = "#686868" if dark else BORDER
    rounded(draw, box, fill=fill, outline=line, width=3, radius=28)
    cx = (left + right) / 2
    cy = top + (bottom - top) * 0.42
    radius = min(right - left, bottom - top) * 0.14
    draw.ellipse((cx - radius, cy - radius, cx + radius, cy + radius), fill=accent)
    shoulder_top = cy + radius * 1.15
    draw.rounded_rectangle(
        (cx - radius * 2.0, shoulder_top, cx + radius * 2.0, shoulder_top + radius * 1.55),
        radius=int(radius * 0.65),
        fill=accent,
    )
    if label:
        centered(draw, (cx, bottom - 38), "PORTRAIT", font(13, True), WHITE if dark else DARK)


def pill(draw, box, label, fill, outline):
    rounded(draw, box, fill=fill, outline=outline, width=2, radius=18)
    centered(draw, ((box[0] + box[2]) / 2, (box[1] + box[3]) / 2), label, font(15, True), outline)


def concept_a():
    image, draw = base_slide("About me", "Concept A · Personal profile")
    portrait_placeholder(draw, (80, 188, 570, 707), accent=TU_RED, dark=True)

    draw.text((650, 196), "Ramon Mehrpoya", font=font(42, True), fill=DARK)
    draw.text((652, 259), "Master's thesis candidate · Computer Science · TU Berlin", font=font(21), fill=TU_RED)
    draw.line((652, 306, 1435, 306), fill=BORDER, width=2)

    draw.text((652, 334), "ACADEMIC BACKGROUND", font=font(14, True), fill=TU_RED)
    draw.text((652, 365), "Bachelor's degree in Business Informatics · TU Berlin", font=font(21, True), fill=DARK)

    draw.text((652, 410), "PROJECT EXPERIENCE AT ISE, TU BERLIN", font=font(14, True), fill=TU_RED)
    projects = [
        (650, "GAIA-X 4 PLC-AAD", "Blockchain &\nencryption", GREEN_TINT, GREEN),
        (915, "ZOKRATES PLUS", "ZK · TEE · remote\nattestation · DFL", BLUE_TINT, BLUE),
        (1180, "ZODIAC", "AI agents &\nMCP tools", ORANGE_TINT, ORANGE),
    ]
    for x, project, focus, fill, accent in projects:
        rounded(draw, (x, 438, x + 255, 545), fill=fill, outline=accent, width=3, radius=17)
        centered(draw, (x + 127.5, 464), project, font(13, True), accent)
        centered(draw, (x + 127.5, 511), focus, font(14, True), DARK)

        draw.line((x + 127.5, 546, x + 127.5, 581), fill=TU_RED, width=4)
        draw.polygon(
            [(x + 127.5, 590), (x + 117.5, 573), (x + 137.5, 573)],
            fill=TU_RED,
        )

    rounded(draw, (650, 590, 1435, 705), fill=RED_TINT, outline=TU_RED, width=3, radius=18)
    draw.text((682, 611), "TODAY'S THESIS", font=font(13, True), fill=TU_RED)
    draw.text((682, 641), "VITA-FL", font=font(27, True), fill=DARK)
    draw.text(
        (855, 640),
        "Verifiable Inference and Trust Architecture\nfor Federated Learning",
        font=font(16, True),
        fill=DARK,
        spacing=4,
    )
    return image


def concept_b():
    image, draw = base_slide("Presenter and thesis", "Concept B · Academic profile")
    rounded(draw, (75, 185, 1525, 370), fill=RED_TINT, outline=TU_RED, width=3, radius=26)
    portrait_placeholder(draw, (108, 208, 278, 348), accent=TU_RED, dark=False, label=False)
    draw.text((325, 218), "Ramon Mehrpoya", font=font(38, True), fill=DARK)
    draw.text((327, 275), "Master's thesis candidate · TU Berlin", font=font(20), fill=TU_RED)
    draw.text(
        (327, 316),
        "Bachelor's degree in Business Informatics · TU Berlin",
        font=font(16),
        fill=DARK,
    )

    cards = [
        (
            "01",
            "GAIA-X 4 PLC-AAD",
            "Blockchain & encryption",
            "Ledger coordination and\nprotected model exchange",
            GREEN_TINT,
            GREEN,
        ),
        (
            "02",
            "ZOKRATES PLUS",
            "ZK · TEE · remote attestation · DFL",
            "Measured admission and\nverifiable execution",
            BLUE_TINT,
            BLUE,
        ),
        (
            "03",
            "ZODIAC",
            "AI agents & MCP tools",
            "Agent-driven retrieval and\nauditable tool execution",
            ORANGE_TINT,
            ORANGE,
        ),
    ]
    for index, (number, heading, focus, contribution, fill, accent) in enumerate(cards):
        x = 76 + index * 487
        rounded(draw, (x, 410, x + 450, 646), fill=fill, outline=accent, width=3, radius=22)
        draw.text((x + 28, 435), number, font=font(17, True), fill=accent)
        draw.text((x + 88, 435), heading, font=font(16, True), fill=accent)
        draw.text((x + 28, 493), focus, font=font(16, True), fill=DARK)
        draw.line((x + 28, 531, x + 422, 531), fill=accent, width=2)
        draw.text((x + 28, 550), contribution, font=font(17, True), fill=DARK, spacing=5)

    rounded(draw, (76, 674, 1500, 728), fill=RED_TINT, outline=TU_RED, width=3, radius=16)
    centered(
        draw,
        (788, 701),
        "VITA-FL brings these foundations together: decentralized training · attested inference · transparent tool use",
        font(17, True),
        DARK,
    )
    return image


def concept_c():
    image, draw = base_slide("How previous projects shaped VITA-FL", "Concept C · Experience-to-thesis map")
    portrait_placeholder(draw, (75, 206, 345, 585), accent=TU_RED, dark=True)
    centered(draw, (210, 620), "Ramon Mehrpoya", font(21, True), DARK)
    centered(draw, (210, 651), "TU Berlin", font(15, True), TU_RED)
    centered(draw, (210, 686), "Business Informatics", font(15, True), DARK)

    columns = [
        (
            400,
            "GAIA-X 4 PLC-AAD",
            "Blockchain & encryption",
            "Ledger coordination &\nprotected model exchange",
            GREEN_TINT,
            GREEN,
        ),
        (
            770,
            "ZOKRATES PLUS",
            "ZK · TEE · remote\nattestation · DFL",
            "Measured admission &\nverifiable execution",
            BLUE_TINT,
            BLUE,
        ),
        (
            1140,
            "ZODIAC",
            "AI agents & MCP tools",
            "Agent-driven retrieval &\nauditable tool use",
            ORANGE_TINT,
            ORANGE,
        ),
    ]
    for x, project, focus, contribution, fill, accent in columns:
        rounded(draw, (x, 220, x + 330, 365), fill=fill, outline=accent, width=3, radius=20)
        centered(draw, (x + 165, 267), project, font(16, True), accent)
        centered(draw, (x + 165, 322), focus, font(16, True), DARK)

        draw.line((x + 165, 366, x + 165, 410), fill=accent, width=4)
        draw.polygon([(x + 165, 418), (x + 155, 401), (x + 175, 401)], fill=accent)

        rounded(draw, (x, 420, x + 330, 548), fill=WHITE, outline=accent, width=3, radius=18)
        centered(draw, (x + 165, 484), contribution, font(17, True), DARK)

        draw.line((x + 165, 549, x + 165, 588), fill=TU_RED, width=4)
        draw.polygon([(x + 165, 596), (x + 155, 579), (x + 175, 579)], fill=TU_RED)

    rounded(draw, (400, 598, 1470, 701), fill=RED_TINT, outline=TU_RED, width=3, radius=20)
    draw.text((430, 620), "VITA-FL", font=font(25, True), fill=TU_RED)
    draw.text(
        (430, 660),
        "Decentralized training  ·  Attested inference  ·  Transparent AI-agent tool use",
        font=font(17, True),
        fill=DARK,
    )
    return image


def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    concepts = {
        "intro-concept-a-personal-profile.png": concept_a(),
        "intro-concept-b-academic-profile.png": concept_b(),
        "intro-concept-c-topic-led.png": concept_c(),
    }
    for filename, image in concepts.items():
        path = OUTPUT / filename
        image.save(path, quality=95)
        print(path)


if __name__ == "__main__":
    main()
