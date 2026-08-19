#!/usr/bin/env python3
"""Render three editable-slide design concepts as PNG previews."""

from __future__ import annotations

import math
from io import BytesIO
from pathlib import Path
from zipfile import ZipFile

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
PRESENTATION = ROOT
TEMPLATE = PRESENTATION / "TU_Berlin_Praesentation_Master_einfarbig_Rot.pptx"
OUTPUT = PRESENTATION / "concepts"

WIDTH = 1600
HEIGHT = 900
FOOTER_Y = 755

TU_RED = "#C40D1E"
DARK = "#434343"
WHITE = "#FFFFFF"
LIGHT = "#F3F3F3"
MID = "#B2B2B2"
BORDER = "#D5D5D5"
BLUE = "#1F90CC"
BLUE_TINT = "#EAF5FA"
GREEN = "#2F8F46"
GREEN_TINT = "#EAF6ED"
ORANGE = "#FF6C00"
ORANGE_TINT = "#FFF1E7"
RED_TINT = "#FBEAEC"

FONT_REGULAR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(size: int, bold: bool = False):
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REGULAR, size)


def centered(draw, xy, text, face, fill=DARK, anchor="mm"):
    draw.text(xy, text, font=face, fill=fill, anchor=anchor, align="center", spacing=3)


def base_slide(title: str, kicker: str):
    image = Image.new("RGB", (WIDTH, HEIGHT), WHITE)
    draw = ImageDraw.Draw(image)
    draw.text((77, 35), title, font=font(40), fill=DARK)
    draw.text((77, 119), kicker.upper(), font=font(17, True), fill=TU_RED)
    draw.line((73, 157, 1510, 157), fill="#315463", width=3)
    draw.rectangle((0, FOOTER_Y, WIDTH, HEIGHT), fill=TU_RED)
    draw.text((73, 826), "CONCEPT PREVIEW", font=font(16), fill=WHITE)
    draw.text(
        (245, 826),
        "Ramon Mehrpoya  |  Master's Thesis  |  Verifiable Decentralized Federated Machine Learning and Inference for AI Agent Systems  |  VITA-FL",
        font=font(13),
        fill=WHITE,
    )
    date_text = "19 August 2026"
    date_font = font(13)
    draw.text((1515 - draw.textlength(date_text, font=date_font), 826), date_text, font=date_font, fill=WHITE)

    with ZipFile(TEMPLATE) as archive:
        logo = Image.open(BytesIO(archive.read("ppt/media/image2.png"))).convert("RGBA")
    logo.thumbnail((118, 92), Image.Resampling.LANCZOS)
    image.paste(logo, (1393, 45), logo)
    return image, draw


def rounded(draw, box, fill=WHITE, outline=BORDER, width=2, radius=18):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def hospital_icon_classic(draw, cx, cy, color=BLUE, scale=1.0):
    w = int(55 * scale)
    h = int(54 * scale)
    left = int(cx - w / 2)
    top = int(cy - h / 2)
    draw.rounded_rectangle((left, top + 7, left + w, top + h), radius=5, fill=WHITE, outline=color, width=3)
    draw.polygon(
        [(left - 3, top + 12), (cx, top - 3), (left + w + 3, top + 12)],
        fill=color,
    )
    draw.rectangle((cx - 7 * scale, top + 20 * scale, cx + 7 * scale, top + 43 * scale), fill=color)
    draw.rectangle((cx - 16 * scale, top + 28 * scale, cx + 16 * scale, top + 35 * scale), fill=color)
    for dx in (-19, 18):
        draw.rectangle(
            (cx + dx * scale - 4, top + 39 * scale, cx + dx * scale + 4, top + 48 * scale),
            fill=color,
        )


def hospital_icon_tower(draw, cx, cy, color=BLUE, scale=1.0):
    w = 49 * scale
    h = 58 * scale
    draw.rounded_rectangle((cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), radius=4, fill=WHITE, outline=color, width=3)
    draw.rounded_rectangle((cx - 18 * scale, cy - 20 * scale, cx + 18 * scale, cy - 3 * scale), radius=3, fill=color)
    centered(draw, (cx, cy - 11 * scale), "H", font(max(10, int(14 * scale)), True), WHITE)
    for row in (-1, 1):
        for col in (-1, 1):
            x = cx + col * 12 * scale
            y = cy + row * 10 * scale + 10 * scale
            draw.rectangle((x - 4 * scale, y - 3 * scale, x + 4 * scale, y + 3 * scale), fill=color)
    draw.rectangle((cx - 7 * scale, cy + 18 * scale, cx + 7 * scale, cy + h / 2), fill=color)


def hospital_icon_facade(draw, cx, cy, color=BLUE, scale=1.0):
    w = 67 * scale
    h = 45 * scale
    draw.rounded_rectangle((cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), radius=4, fill=WHITE, outline=color, width=3)
    draw.rectangle((cx - w / 2, cy - h / 2, cx + w / 2, cy - h / 2 + 10 * scale), fill=color)
    centered(draw, (cx, cy - 12 * scale), "H", font(max(10, int(13 * scale)), True), WHITE)
    for col in (-22, -8, 8, 22):
        draw.rectangle((cx + col * scale - 3, cy - 2 * scale, cx + col * scale + 3, cy + 5 * scale), fill=color)
    draw.rectangle((cx - 8 * scale, cy + 8 * scale, cx + 8 * scale, cy + h / 2), fill=color)


def hospital_icon_campus(draw, cx, cy, color=BLUE, scale=1.0):
    draw.rectangle((cx - 30 * scale, cy - 2 * scale, cx + 30 * scale, cy + 24 * scale), fill=WHITE, outline=color, width=3)
    draw.rectangle((cx - 17 * scale, cy - 29 * scale, cx + 17 * scale, cy + 24 * scale), fill=WHITE, outline=color, width=3)
    draw.rounded_rectangle((cx - 13 * scale, cy - 23 * scale, cx + 13 * scale, cy - 7 * scale), radius=3, fill=color)
    centered(draw, (cx, cy - 15 * scale), "H", font(max(10, int(13 * scale)), True), WHITE)
    for x in (-23, 23):
        draw.rectangle((cx + x * scale - 4, cy + 7 * scale, cx + x * scale + 4, cy + 14 * scale), fill=color)
    draw.rectangle((cx - 7 * scale, cy + 7 * scale, cx + 7 * scale, cy + 24 * scale), fill=color)


def hospital_icon_pin(draw, cx, cy, color=BLUE, scale=1.0):
    radius = 26 * scale
    draw.ellipse((cx - radius, cy - radius - 8 * scale, cx + radius, cy + radius - 8 * scale), fill=WHITE, outline=color, width=3)
    draw.polygon([(cx - 15 * scale, cy + 10 * scale), (cx + 15 * scale, cy + 10 * scale), (cx, cy + 36 * scale)], fill=color)
    draw.ellipse((cx - 16 * scale, cy - 24 * scale, cx + 16 * scale, cy + 8 * scale), fill=color)
    centered(draw, (cx, cy - 8 * scale), "H", font(max(12, int(17 * scale)), True), WHITE)


def hospital_icon_radiology(draw, cx, cy, color=BLUE, scale=1.0):
    hospital_icon_tower(draw, cx - 12 * scale, cy, color, scale * 0.86)
    draw.rounded_rectangle((cx + 10 * scale, cy - 19 * scale, cx + 39 * scale, cy + 23 * scale), radius=3, fill=DARK, outline=color, width=3)
    draw.ellipse((cx + 17 * scale, cy - 11 * scale, cx + 32 * scale, cy + 14 * scale), outline=WHITE, width=2)
    draw.line((cx + 24.5 * scale, cy - 9 * scale, cx + 24.5 * scale, cy + 12 * scale), fill=WHITE, width=2)


def hospital_symbol(draw, cx, cy, color=BLUE, scale=1.0, style="classic"):
    functions = {
        "classic": hospital_icon_classic,
        "tower": hospital_icon_tower,
        "facade": hospital_icon_facade,
        "campus": hospital_icon_campus,
        "pin": hospital_icon_pin,
        "radiology": hospital_icon_radiology,
    }
    functions[style](draw, cx, cy, color, scale)


def hospital_card(
    draw,
    center,
    name,
    subtitle="Local X-rays + TEE",
    highlight=False,
    width=210,
    height=98,
    icon_style="classic",
):
    cx, cy = center
    border = TU_RED if highlight else BLUE
    fill = RED_TINT if highlight else BLUE_TINT
    box = (cx - width // 2, cy - height // 2, cx + width // 2, cy + height // 2)
    rounded(draw, box, fill=fill, outline=border, width=4 if highlight else 2, radius=16)
    hospital_symbol(draw, cx - width // 2 + 47, cy, border, 0.78, icon_style)
    draw.text((cx - width // 2 + 84, cy - 27), name, font=font(17, True), fill=DARK)
    draw.text((cx - width // 2 + 84, cy + 1), subtitle, font=font(12), fill=DARK)
    if highlight:
        draw.text((cx - width // 2 + 84, cy + 24), "Temporary aggregator", font=font(11, True), fill=TU_RED)
    return box


def arc_arrow(draw, center, radii, start_deg, end_deg, color=DARK, width=5):
    cx, cy = center
    rx, ry = radii
    if end_deg <= start_deg:
        end_deg += 360
    points = []
    for step in range(41):
        theta = math.radians(start_deg + (end_deg - start_deg) * step / 40)
        points.append((cx + rx * math.cos(theta), cy + ry * math.sin(theta)))
    draw.line(points, fill=color, width=width, joint="curve")
    end = points[-1]
    previous = points[-4]
    angle = math.atan2(end[1] - previous[1], end[0] - previous[0])
    length = 17
    spread = 8
    back = (end[0] - length * math.cos(angle), end[1] - length * math.sin(angle))
    left = (back[0] + spread * math.cos(angle + math.pi / 2), back[1] + spread * math.sin(angle + math.pi / 2))
    right = (back[0] + spread * math.cos(angle - math.pi / 2), back[1] + spread * math.sin(angle - math.pi / 2))
    draw.polygon([end, left, right], fill=color)


def bezier_arrow(draw, start, control, end, color=BLUE, width=4, dashed=True):
    points = []
    for step in range(61):
        t = step / 60
        x = (1 - t) ** 2 * start[0] + 2 * (1 - t) * t * control[0] + t**2 * end[0]
        y = (1 - t) ** 2 * start[1] + 2 * (1 - t) * t * control[1] + t**2 * end[1]
        points.append((x, y))
    if dashed:
        for index in range(0, len(points) - 1, 6):
            segment = points[index : min(index + 4, len(points))]
            if len(segment) > 1:
                draw.line(segment, fill=color, width=width, joint="curve")
    else:
        draw.line(points, fill=color, width=width, joint="curve")
    tip = points[-1]
    previous = points[-4]
    angle = math.atan2(tip[1] - previous[1], tip[0] - previous[0])
    length = 16
    spread = 8
    back = (tip[0] - length * math.cos(angle), tip[1] - length * math.sin(angle))
    draw.polygon(
        [
            tip,
            (back[0] + spread * math.cos(angle + math.pi / 2), back[1] + spread * math.sin(angle + math.pi / 2)),
            (back[0] + spread * math.cos(angle - math.pi / 2), back[1] + spread * math.sin(angle - math.pi / 2)),
        ],
        fill=color,
    )


def lock_icon(draw, cx, cy, color=TU_RED, scale=1.0):
    draw.arc(
        (cx - 14 * scale, cy - 22 * scale, cx + 14 * scale, cy + 5 * scale),
        180,
        360,
        fill=color,
        width=max(2, int(4 * scale)),
    )
    draw.rounded_rectangle(
        (cx - 18 * scale, cy - 3 * scale, cx + 18 * scale, cy + 27 * scale),
        radius=5,
        fill=color,
    )
    draw.ellipse((cx - 3 * scale, cy + 6 * scale, cx + 3 * scale, cy + 12 * scale), fill=WHITE)
    draw.rectangle((cx - 2 * scale, cy + 10 * scale, cx + 2 * scale, cy + 18 * scale), fill=WHITE)


def footer_statement(draw, text):
    rounded(draw, (470, 686, 1450, 733), fill=RED_TINT, outline=TU_RED, width=2, radius=10)
    centered(draw, (960, 710), text, font(16, True), TU_RED)


def concept_a():
    image, draw = base_slide(
        "Decentralized training across hospitals",
        "Concept A · Circular training round",
    )
    center = (820, 455)
    radii = (420, 215)
    angles = [-90, -18, 54, 126, 198]
    node_centers = [
        (center[0] + radii[0] * math.cos(math.radians(a)), center[1] + radii[1] * math.sin(math.radians(a)))
        for a in angles
    ]
    for index, angle in enumerate(angles):
        next_angle = angles[(index + 1) % len(angles)]
        if index == len(angles) - 1:
            next_angle += 360
        arc_arrow(draw, center, radii, angle + 15, next_angle - 15, BLUE, 5)
    rounded(draw, (675, 330, 965, 580), fill=WHITE, outline=TU_RED, width=5, radius=125)
    centered(draw, (820, 405), "SHARED VERIFIABLE", font(15, True), TU_RED)
    centered(draw, (820, 455), "MODEL STATE", font(27, True), DARK)
    centered(draw, (820, 505), "Ledger-coordinated rounds", font(15), DARK)
    lock_icon(draw, 820, 546, TU_RED, 0.65)
    for i, location in enumerate(node_centers):
        hospital_card(draw, location, f"Hospital {chr(65 + i)}", highlight=i == 1)
    rounded(draw, (55, 252, 285, 452), fill=LIGHT, outline=BORDER, width=2)
    centered(draw, (170, 286), "ROUND CYCLE", font(15, True), TU_RED)
    phases = ["1  Train locally", "2  Sign update", "3  Aggregate", "4  Publish model"]
    for row, phase in enumerate(phases):
        draw.text((80, 324 + 34 * row), phase, font=font(14, row == 0), fill=DARK)
    footer_statement(draw, "Raw X-rays stay local; only authenticated model artifacts enter the shared round.")
    return image


def concept_b():
    image, draw = base_slide(
        "Decentralized training across hospitals",
        "Concept B · Hospitals around the global model",
    )
    hospitals = {
        "A": (445, 235),
        "B": (1155, 235),
        "C": (1280, 485),
        "D": (800, 625),
        "E": (320, 485),
    }

    # A clockwise outer ring indicates that the temporary aggregator role can
    # move to another admitted hospital in the following round.
    bezier_arrow(draw, (548, 205), (800, 164), (1052, 205), ORANGE, 4, dashed=False)
    bezier_arrow(draw, (1258, 260), (1435, 325), (1378, 445), ORANGE, 4, dashed=False)
    bezier_arrow(draw, (1260, 528), (1170, 700), (900, 660), ORANGE, 4, dashed=False)
    bezier_arrow(draw, (700, 660), (430, 700), (340, 528), ORANGE, 4, dashed=False)
    bezier_arrow(draw, (222, 445), (285, 330), (342, 260), ORANGE, 4, dashed=False)

    # The current encrypted model is distributed to each admitted worker.
    bezier_arrow(draw, (690, 294), (620, 205), (545, 240), TU_RED, 4, dashed=False)
    bezier_arrow(draw, (910, 294), (980, 205), (1055, 240), TU_RED, 4, dashed=False)
    bezier_arrow(draw, (610, 400), (470, 405), (422, 470), TU_RED, 4, dashed=False)
    bezier_arrow(draw, (990, 400), (1130, 405), (1178, 470), TU_RED, 4, dashed=False)

    # Signed local updates converge on the temporary aggregator.
    bezier_arrow(draw, (445, 283), (455, 560), (700, 612), BLUE, 4, dashed=True)
    bezier_arrow(draw, (1155, 283), (1145, 560), (900, 612), BLUE, 4, dashed=True)
    bezier_arrow(draw, (1180, 515), (1095, 660), (900, 635), BLUE, 4, dashed=True)
    bezier_arrow(draw, (420, 515), (505, 660), (700, 635), BLUE, 4, dashed=True)

    # The selected aggregator publishes the next model artifact.
    bezier_arrow(draw, (800, 578), (800, 540), (800, 506), BLUE, 6, dashed=False)
    draw.text((816, 536), "Aggregated publication", font=font(12, True), fill=BLUE)

    for name, location in hospitals.items():
        hospital_card(
            draw,
            location,
            f"Hospital {name}",
            "Local training",
            highlight=name == "D",
            width=205,
            height=90,
            icon_style="campus",
        )

    rounded(draw, (610, 292, 990, 506), fill=RED_TINT, outline=TU_RED, width=4, radius=28)
    centered(draw, (800, 332), "CURRENT ENCRYPTED", font(15, True), TU_RED)
    centered(draw, (800, 382), "GLOBAL MODEL", font(29, True), DARK)
    lock_icon(draw, 800, 435, TU_RED, 0.82)
    rounded(draw, (672, 468, 928, 496), fill=WHITE, outline=BORDER, width=1, radius=10)
    centered(draw, (800, 482), "Resolved from the ledger", font(12), DARK)

    rounded(draw, (62, 214, 295, 420), fill=LIGHT, outline=BORDER, width=2)
    centered(draw, (178, 246), "DATA FLOW", font(15, True), TU_RED)
    draw.line((92, 289, 156, 289), fill=TU_RED, width=5)
    draw.polygon([(156, 289), (140, 280), (140, 298)], fill=TU_RED)
    draw.text((171, 278), "Encrypted model", font=font(12), fill=DARK)
    for x in range(92, 151, 14):
        draw.line((x, 331, min(x + 8, 156), 331), fill=BLUE, width=4)
    draw.polygon([(156, 331), (140, 322), (140, 340)], fill=BLUE)
    draw.text((171, 320), "Signed update", font=font(12), fill=DARK)
    draw.line((92, 371, 156, 371), fill=BLUE, width=5)
    draw.polygon([(156, 371), (140, 362), (140, 380)], fill=BLUE)
    draw.text((171, 360), "Publication", font=font(12), fill=DARK)
    draw.line((92, 407, 156, 407), fill=ORANGE, width=5)
    draw.polygon([(156, 407), (140, 398), (140, 416)], fill=ORANGE)
    draw.text((171, 396), "Aggregator rotation", font=font(11), fill=DARK)
    return image


def hospital_symbol_options():
    image, draw = base_slide(
        "Hospital symbol options",
        "Choose the visual language for the DFL training slide",
    )
    options = [
        ("A", "Modern tower", "tower", False),
        ("B", "Clinic facade", "facade", False),
        ("C", "Hospital campus", "campus", True),
        ("D", "Location marker", "pin", False),
        ("E", "Hospital + X-ray", "radiology", False),
    ]
    positions = [(350, 320), (800, 320), (1250, 320), (575, 575), (1025, 575)]
    for (code, label, style, recommended), (cx, cy) in zip(options, positions):
        border = TU_RED if recommended else BORDER
        fill = RED_TINT if recommended else LIGHT
        rounded(draw, (cx - 175, cy - 105, cx + 175, cy + 105), fill=fill, outline=border, width=4 if recommended else 2, radius=22)
        hospital_symbol(draw, cx, cy - 18, TU_RED if recommended else BLUE, 1.5, style)
        centered(draw, (cx, cy + 60), f"{code} · {label}", font(17, True), DARK)
        if recommended:
            centered(draw, (cx, cy + 88), "RECOMMENDED", font(11, True), TU_RED)
    rounded(draw, (390, 698, 1210, 735), fill=BLUE_TINT, outline=BLUE, width=2, radius=10)
    centered(draw, (800, 716), "All variants use a neutral H rather than a branded medical emblem.", font(14, True), BLUE)
    return image


def concept_c():
    image, draw = base_slide(
        "Decentralized training across hospitals",
        "Concept C · Two-layer trust circle",
    )
    center = (820, 445)
    outer = (465, 240)
    angles = [-90, -18, 54, 126, 198]
    locations = [
        (center[0] + outer[0] * math.cos(math.radians(a)), center[1] + outer[1] * math.sin(math.radians(a)))
        for a in angles
    ]
    for i, location in enumerate(locations):
        hospital_card(draw, location, f"Hospital {chr(65 + i)}", "Local data + worker", highlight=i == 2, width=190, height=88)
    for a, b in zip(angles, angles[1:] + [angles[0] + 360]):
        arc_arrow(draw, center, outer, a + 16, b - 16, BLUE, 4)

    controls = [
        ("ATTESTATION", -90, BLUE_TINT, BLUE),
        ("SIGNATURES", 0, GREEN_TINT, GREEN),
        ("LEDGER", 90, RED_TINT, TU_RED),
        ("ENCRYPTION", 180, ORANGE_TINT, ORANGE),
    ]
    for label, angle, fill, border in controls:
        theta = math.radians(angle)
        cx = center[0] + 250 * math.cos(theta)
        cy = center[1] + 130 * math.sin(theta)
        rounded(draw, (cx - 100, cy - 31, cx + 100, cy + 31), fill=fill, outline=border, width=3, radius=18)
        centered(draw, (cx, cy), label, font(14, True), border)

    rounded(draw, (690, 350, 950, 540), fill=DARK, outline=TU_RED, width=5, radius=95)
    centered(draw, (820, 407), "VITA-FL", font(18, True), WHITE)
    centered(draw, (820, 452), "TRAINING", font(27, True), WHITE)
    centered(draw, (820, 490), "ROUND", font(27, True), WHITE)
    rounded(draw, (55, 270, 270, 438), fill=LIGHT, outline=BORDER, width=2)
    centered(draw, (162, 302), "TWO LAYERS", font(15, True), TU_RED)
    draw.ellipse((82, 334, 113, 365), fill=BLUE)
    draw.text((128, 338), "Hospitals and data", font=font(12), fill=DARK)
    draw.ellipse((82, 382, 113, 413), fill=TU_RED)
    draw.text((128, 386), "Trust controls", font=font(12), fill=DARK)
    footer_statement(draw, "Local training is surrounded by explicit admission, provenance, coordination, and confidentiality controls.")
    return image


def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    concepts = {
        "dfl-concept-a-circular-round.png": concept_a(),
        "dfl-concept-b-global-model.png": concept_b(),
        "dfl-concept-c-trust-circle.png": concept_c(),
        "hospital-symbol-options.png": hospital_symbol_options(),
    }
    for name, image in concepts.items():
        path = OUTPUT / name
        image.save(path, quality=95)
        print(path)


if __name__ == "__main__":
    main()
