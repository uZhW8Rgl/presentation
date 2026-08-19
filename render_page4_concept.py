#!/usr/bin/env python3
"""Render the mirrored computer-scientist concept for a prospective Page 4."""

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
    base_slide,
    font,
)
from render_page3_concepts import cover


ROOT = Path(__file__).resolve().parent
PRESENTATION = ROOT
ASSET = PRESENTATION / "assets" / "computer-scientist-editorial-illustration.png"
DESTINATION = PRESENTATION / "concepts" / "page-04-computer-scientist-architecture.png"

MAIN_PANEL = (116, 186, 1098, 733)
ARCHITECTURE_PANEL = (1149, 186, 1520, 703)
PURPLE = "#7A35B5"


def arrow_down(draw: ImageDraw.ImageDraw, x: int, top: int, bottom: int) -> None:
    draw.line((x, top, x, bottom - 8), fill="#8D969B", width=3)
    draw.polygon(((x - 7, bottom - 11), (x + 7, bottom - 11), (x, bottom)), fill="#8D969B")


def render() -> Image.Image:
    image, draw = base_slide(
        "A trustworthy answer needs verifiable infrastructure",
        "The computer scientist's response",
    )

    # The editorial image mirrors Page 3: subject left, explanation right.
    scientist = Image.open(ASSET).convert("RGB")
    panel = cover(
        scientist,
        (MAIN_PANEL[2] - MAIN_PANEL[0], MAIN_PANEL[3] - MAIN_PANEL[1]),
        focus_x=0.5,
    )
    image.paste(panel, MAIN_PANEL[:2])
    draw = ImageDraw.Draw(image)

    # Mirrored answer card: the accent sits on the right instead of the left.
    draw.rounded_rectangle((642, 226, 1064, 527), radius=28, fill=WHITE, outline=TU_RED, width=3)
    draw.rectangle((1052, 226, 1064, 527), fill=TU_RED)
    draw.text((681, 266), "THE ENGINEERING RESPONSE", font=font(16, True), fill=TU_RED)
    draw.multiline_text(
        (681, 326),
        "“Then we need more\nthan an AI model.”",
        font=font(31, True),
        fill=DARK,
        spacing=8,
    )
    draw.multiline_text(
        (681, 456),
        "Training, execution, and publication\nmust form one inspectable path.",
        font=font(15, True),
        fill="#686868",
        spacing=5,
    )

    # The far-right card mirrors Page 3's X-ray card, but exposes the backend path.
    draw.rounded_rectangle(ARCHITECTURE_PANEL, radius=42, fill=DARK)
    draw.text((1334, 213), "REQUIRED SYSTEM ARCHITECTURE", font=font(13, True), fill=WHITE, anchor="ma")

    stages = [
        ("SIGNED MEDICAL DATA", GREEN),
        ("ATTESTED DFL", BLUE),
        ("VERIFIED MODEL STATE", PURPLE),
        ("AGENT + INFERENCE TEE", ORANGE),
        ("TRANSPARENCY LOG", TU_RED),
    ]
    row_left = 1178
    row_right = 1491
    row_height = 48
    row_tops = [252, 326, 400, 474, 548]
    for index, ((label, accent), top) in enumerate(zip(stages, row_tops), start=1):
        draw.rounded_rectangle(
            (row_left, top, row_right, top + row_height),
            radius=12,
            fill="#505050",
            outline="#717171",
            width=2,
        )
        draw.ellipse((1191, top + 10, 1219, top + 38), fill=accent)
        draw.text((1205, top + 24), str(index), font=font(14, True), fill=WHITE, anchor="mm")
        draw.text((1232, top + 24), label, font=font(13, True), fill=WHITE, anchor="lm")
        if index < len(stages):
            arrow_down(draw, 1334, top + row_height + 3, row_tops[index] - 3)

    draw.text(
        (1334, 668),
        "Evidence follows every result.",
        font=font(13, True),
        fill=WHITE,
        anchor="mm",
    )

    # Replace the generic preview marker with the prospective page number.
    draw.rectangle((0, 755, 245, 900), fill=TU_RED)
    draw.text((73, 826), "Page 4", font=font(16), fill=WHITE)
    return image


def main() -> None:
    DESTINATION.parent.mkdir(parents=True, exist_ok=True)
    render().save(DESTINATION, quality=95)
    print(DESTINATION)


if __name__ == "__main__":
    main()
