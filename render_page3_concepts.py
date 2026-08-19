#!/usr/bin/env python3
"""Render alternative Page 3 concepts without changing the production deck."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw

from render_dfl_concepts import BORDER, DARK, LIGHT, TU_RED, WHITE, font, rounded


ROOT = Path(__file__).resolve().parent
PRESENTATION = ROOT
CONCEPTS = PRESENTATION / "concepts"
BASE = CONCEPTS / "page-03-physician-ai-question.png"
PHOTO = PRESENTATION / "assets" / "physician-editorial-photo.png"
PHOTO_TABLET = PRESENTATION / "assets" / "physician-editorial-photo-tablet.png"
ILLUSTRATION = PRESENTATION / "assets" / "physician-editorial-illustration.png"
ILLUSTRATION_TABLET = PRESENTATION / "assets" / "physician-editorial-illustration-tablet.png"

RIGHT = (502, 186, 1484, 733)


def cover(source: Image.Image, size: tuple[int, int], focus_x: float = 0.5) -> Image.Image:
    target_w, target_h = size
    ratio = max(target_w / source.width, target_h / source.height)
    resized = source.resize(
        (round(source.width * ratio), round(source.height * ratio)),
        Image.Resampling.LANCZOS,
    )
    left = round((resized.width - target_w) * focus_x)
    left = max(0, min(left, resized.width - target_w))
    top = max(0, (resized.height - target_h) // 2)
    return resized.crop((left, top, left + target_w, top + target_h))


def base_canvas() -> Image.Image:
    image = Image.open(BASE).convert("RGB")
    draw = ImageDraw.Draw(image)
    draw.rectangle(RIGHT, fill=WHITE)
    return image


def rounded_paste(canvas: Image.Image, asset: Image.Image, box, radius=28):
    left, top, right, bottom = box
    fitted = cover(asset, (right - left, bottom - top))
    mask = Image.new("L", fitted.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, fitted.width, fitted.height), radius=radius, fill=255)
    canvas.paste(fitted, (left, top), mask)


def translucent_box(image: Image.Image, box, fill, outline, radius=26, width=3):
    overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)
    return Image.alpha_composite(image.convert("RGBA"), overlay).convert("RGB")


def variant_a_photo_panel() -> Image.Image:
    image = base_canvas()
    photo = Image.open(PHOTO_TABLET).convert("RGB")
    panel = cover(photo, (RIGHT[2] - RIGHT[0], RIGHT[3] - RIGHT[1]), focus_x=0.5)
    image.paste(panel, RIGHT[:2])

    image = translucent_box(
        image,
        (532, 236, 1000, 493),
        (255, 255, 255, 235),
        (196, 13, 30, 255),
        radius=28,
        width=3,
    )
    draw = ImageDraw.Draw(image)
    draw.text((570, 270), "THE PHYSICIAN ASKS", font=font(17, True), fill=TU_RED)
    draw.multiline_text(
        (570, 330),
        "“Can’t I just\nask an AI?”",
        font=font(39, True),
        fill=DARK,
        spacing=8,
    )
    draw.rounded_rectangle((532, 550, 1000, 630), radius=18, fill=TU_RED)
    draw.multiline_text(
        (766, 590),
        "A fluent answer is still a claim—\nnot evidence.",
        font=font(18, True),
        fill=WHITE,
        anchor="mm",
        align="center",
        spacing=2,
    )
    return image


def variant_b_editorial_illustration() -> Image.Image:
    image = base_canvas()
    illustration = Image.open(ILLUSTRATION_TABLET).convert("RGB")
    panel = cover(illustration, (RIGHT[2] - RIGHT[0], RIGHT[3] - RIGHT[1]), focus_x=0.5)
    image.paste(panel, RIGHT[:2])
    draw = ImageDraw.Draw(image)

    draw.rounded_rectangle((536, 226, 958, 527), radius=28, fill=(255, 255, 255), outline=TU_RED, width=3)
    draw.rectangle((536, 226, 548, 527), fill=TU_RED)
    draw.text((584, 266), "THE TEMPTING SHORTCUT", font=font(16, True), fill=TU_RED)
    draw.multiline_text(
        (584, 332),
        "“Can’t I just\nask an AI?”",
        font=font(40, True),
        fill=DARK,
        spacing=8,
    )
    draw.text(
        (584, 472),
        "The answer is immediate.\nIts provenance is not.",
        font=font(17, True),
        fill="#686868",
        spacing=5,
    )
    return image


def variant_c_minimal_portrait() -> Image.Image:
    image = base_canvas()
    draw = ImageDraw.Draw(image)
    rounded(draw, RIGHT, fill=LIGHT, outline=BORDER, width=2, radius=34)

    photo = Image.open(PHOTO).convert("RGB")
    rounded_paste(image, photo, (976, 214, 1438, 638), radius=34)
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((536, 224, 925, 555), radius=28, fill=WHITE, outline=TU_RED, width=3)
    draw.text((572, 264), "A NATURAL QUESTION", font=font(16, True), fill=TU_RED)
    draw.multiline_text(
        (572, 328),
        "“Can’t I just\nask an AI?”",
        font=font(38, True),
        fill=DARK,
        spacing=9,
    )
    draw.line((925, 390, 974, 390), fill=TU_RED, width=5)
    draw.polygon([(974, 390), (957, 380), (957, 400)], fill=TU_RED)
    draw.rounded_rectangle((536, 586, 925, 666), radius=18, fill="#FBEAEC", outline=TU_RED, width=2)
    draw.text(
        (730, 626),
        "The workflow must make\nthe answer inspectable.",
        font=font(17, True),
        fill=DARK,
        anchor="mm",
        align="center",
        spacing=4,
    )
    return image


def contact_sheet(images: list[tuple[str, Image.Image]]) -> Image.Image:
    thumb_w = 720
    thumb_h = round(thumb_w * 900 / 1600)
    gutter = 28
    sheet = Image.new("RGB", (thumb_w * 2 + gutter * 3, thumb_h * 2 + gutter * 3), (221, 229, 234))
    positions = [(gutter, gutter), (gutter * 2 + thumb_w, gutter), (gutter, gutter * 2 + thumb_h)]
    for (label, image), (x, y) in zip(images, positions):
        thumb = image.resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
        sheet.paste(thumb, (x, y))
        draw = ImageDraw.Draw(sheet)
        draw.rounded_rectangle((x + 18, y + 17, x + 72, y + 54), radius=9, fill=TU_RED)
        draw.text((x + 45, y + 35), label, font=font(17, True), fill=WHITE, anchor="mm")
    return sheet


def main():
    CONCEPTS.mkdir(parents=True, exist_ok=True)
    variants = [
        ("A", variant_a_photo_panel()),
        ("B", variant_b_editorial_illustration()),
        ("C", variant_c_minimal_portrait()),
    ]
    filenames = {
        "A": "page-03-concept-a-editorial-photo.png",
        "B": "page-03-concept-b-editorial-illustration.png",
        "C": "page-03-concept-c-minimal-portrait.png",
    }
    for label, image in variants:
        path = CONCEPTS / filenames[label]
        image.save(path, quality=95)
        print(path)
    sheet = CONCEPTS / "page-03-doctor-concepts-contact-sheet.png"
    contact_sheet(variants).save(sheet, quality=95)
    print(sheet)


if __name__ == "__main__":
    main()
