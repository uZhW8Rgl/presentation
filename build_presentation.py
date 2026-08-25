#!/usr/bin/env python3
"""Build the English VITA-FL presentation from the TU Berlin template."""

from __future__ import annotations

import csv
from io import BytesIO
from pathlib import Path
from typing import Sequence
from zipfile import ZipFile

from PIL import Image
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.dml import MSO_LINE_DASH_STYLE
from pptx.enum.shapes import MSO_AUTO_SHAPE_TYPE, MSO_CONNECTOR
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.xmlchemy import OxmlElement
from pptx.util import Inches, Pt


ROOT = Path(__file__).resolve().parent
OUT = ROOT
ASSETS = OUT / "assets"
THREAT_DIAGRAMS = ASSETS / "threat-diagrams"
EVALUATION_DATA = ROOT / "data" / "evaluation"
TEMPLATE = OUT / "TU_Berlin_Praesentation_Master_einfarbig_Rot.pptx"
DESTINATION = OUT / "VITA-FL_Thesis_Presentation_TU_Berlin.pptx"

TU_RED = "C40D1E"
TU_RED_DARK = "A20B19"
DARK = "434343"
BLACK = "191919"
WHITE = "FFFFFF"
LIGHT = "F3F3F3"
MID = "B2B2B2"
BORDER = "D5D5D5"
RED_TINT = "FBEAEC"
BLUE = "1F90CC"
BLUE_TINT = "EAF5FA"
GREEN = "2F8F46"
GREEN_TINT = "EAF6ED"
ORANGE = "FF6C00"
ORANGE_TINT = "FFF1E7"
PURPLE = "7A35B5"
PURPLE_TINT = "F3EBF9"

FONT = "Arial"
LANGUAGE = "en-US"


def rgb(value: str) -> RGBColor:
    value = value.lstrip("#")
    return RGBColor(int(value[0:2], 16), int(value[2:4], 16), int(value[4:6], 16))


def set_fill(shape, color: str):
    shape.fill.solid()
    shape.fill.fore_color.rgb = rgb(color)


def set_line(shape, color: str, width: float = 1.0):
    shape.line.color.rgb = rgb(color)
    shape.line.width = Pt(width)


def set_run_language(run):
    run._r.get_or_add_rPr().set("lang", LANGUAGE)


def add_box(slide, x, y, w, h, fill=LIGHT, line=BORDER, radius=True, line_width=1.0):
    kind = MSO_AUTO_SHAPE_TYPE.ROUNDED_RECTANGLE if radius else MSO_AUTO_SHAPE_TYPE.RECTANGLE
    shape = slide.shapes.add_shape(kind, Inches(x), Inches(y), Inches(w), Inches(h))
    set_fill(shape, fill)
    set_line(shape, line, line_width)
    return shape


def add_auto_shape(slide, kind, x, y, w, h, fill=LIGHT, line=BORDER, line_width=1.0, rotation=0):
    """Add an editable native PowerPoint shape beyond the standard card vocabulary."""
    shape = slide.shapes.add_shape(kind, Inches(x), Inches(y), Inches(w), Inches(h))
    set_fill(shape, fill)
    set_line(shape, line, line_width)
    shape.rotation = rotation
    return shape


def add_text(
    slide,
    text: str,
    x: float,
    y: float,
    w: float,
    h: float,
    size: float = 18,
    color: str = DARK,
    bold: bool = False,
    align=PP_ALIGN.LEFT,
    valign=MSO_ANCHOR.TOP,
    margin: float = 0.02,
):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    frame = box.text_frame
    frame.clear()
    frame.word_wrap = True
    frame.margin_left = Inches(margin)
    frame.margin_right = Inches(margin)
    frame.margin_top = Inches(margin)
    frame.margin_bottom = Inches(margin)
    frame.vertical_anchor = valign
    paragraph = frame.paragraphs[0]
    paragraph.alignment = align
    run = paragraph.add_run()
    run.text = text
    run.font.name = FONT
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = rgb(color)
    set_run_language(run)
    return box


def add_rich_text(slide, parts, x, y, w, h, size=16, align=PP_ALIGN.LEFT, valign=MSO_ANCHOR.TOP):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    frame = box.text_frame
    frame.clear()
    frame.word_wrap = True
    frame.margin_left = frame.margin_right = Inches(0.02)
    frame.margin_top = frame.margin_bottom = Inches(0.02)
    frame.vertical_anchor = valign
    paragraph = frame.paragraphs[0]
    paragraph.alignment = align
    for text, color, bold, font_size in parts:
        run = paragraph.add_run()
        run.text = text
        run.font.name = FONT
        run.font.size = Pt(font_size or size)
        run.font.bold = bold
        run.font.color.rgb = rgb(color)
        set_run_language(run)
    return box


def add_bullets(slide, bullets: Sequence[str], x, y, w, h, size=17, color=DARK, accent=TU_RED, spacing=8):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    frame = box.text_frame
    frame.clear()
    frame.word_wrap = True
    frame.margin_left = frame.margin_right = Inches(0.03)
    frame.margin_top = frame.margin_bottom = Inches(0.02)
    for index, text in enumerate(bullets):
        paragraph = frame.paragraphs[0] if index == 0 else frame.add_paragraph()
        paragraph.space_after = Pt(spacing)
        paragraph.line_spacing = 1.0
        marker = paragraph.add_run()
        marker.text = "●  "
        marker.font.name = FONT
        marker.font.size = Pt(max(10, size - 2))
        marker.font.color.rgb = rgb(accent)
        set_run_language(marker)
        run = paragraph.add_run()
        run.text = text
        run.font.name = FONT
        run.font.size = Pt(size)
        run.font.color.rgb = rgb(color)
        set_run_language(run)
    return box


def add_arrow(slide, x1, y1, x2, y2, color=TU_RED, width=1.8, dashed=False):
    connector = slide.shapes.add_connector(
        MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1), Inches(x2), Inches(y2)
    )
    connector.line.color.rgb = rgb(color)
    connector.line.width = Pt(width)
    if dashed:
        connector.line.dash_style = MSO_LINE_DASH_STYLE.DASH
    line_properties = connector._element.spPr.get_or_add_ln()
    tail = OxmlElement("a:tailEnd")
    tail.set("type", "triangle")
    tail.set("w", "med")
    tail.set("len", "med")
    line_properties.append(tail)
    return connector


def add_line_segment(slide, x1, y1, x2, y2, color=DARK, width=1.8, arrow=False, dashed=False):
    connector = slide.shapes.add_connector(
        MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1), Inches(x2), Inches(y2)
    )
    connector.line.color.rgb = rgb(color)
    connector.line.width = Pt(width)
    if dashed:
        connector.line.dash_style = MSO_LINE_DASH_STYLE.DASH
    if arrow:
        line_properties = connector._element.spPr.get_or_add_ln()
        tail = OxmlElement("a:tailEnd")
        tail.set("type", "triangle")
        tail.set("w", "med")
        tail.set("len", "med")
        line_properties.append(tail)
    return connector


def load_evaluation_runs():
    runs = {}
    for participants in (10, 50, 100):
        path = EVALUATION_DATA / f"evaluation_run_{participants}.csv"
        with path.open(newline="", encoding="utf-8") as handle:
            rows = []
            for row in csv.DictReader(handle):
                rows.append(
                    {
                        "round": int(row["round"]),
                        "loss": float(row["loss"]),
                        "micro_f1": float(row["micro_f1"]),
                        "macro_f1": float(row["macro_f1"]),
                        "macro_auroc": float(row["macro_auroc"]),
                        "exact_match": float(row["exact_match"]),
                    }
                )
        if len(rows) != 49 or rows[0]["round"] != 2 or rows[-1]["round"] != 50:
            raise ValueError(f"Unexpected evaluation trajectory in {path}")
        runs[participants] = rows
    return runs


def add_metric_chart(
    slide,
    x,
    y,
    w,
    h,
    title,
    runs,
    metric,
    y_min,
    y_max,
    y_ticks,
    reference=None,
    descriptor=None,
):
    add_box(slide, x, y, w, h, fill=WHITE, line=BORDER, line_width=1.0)
    add_text(
        slide,
        title,
        x + 0.12,
        y + 0.10,
        w - 0.24,
        0.28,
        12.5,
        DARK,
        True,
        align=PP_ALIGN.CENTER,
        valign=MSO_ANCHOR.MIDDLE,
    )

    if descriptor:
        add_text(
            slide,
            descriptor,
            x + 0.16,
            y + 0.35,
            w - 0.32,
            0.27,
            7.2,
            "686868",
            True,
            align=PP_ALIGN.CENTER,
            valign=MSO_ANCHOR.MIDDLE,
            margin=0,
        )

    legend = [(10, BLUE), (50, TU_RED), (100, GREEN)]
    legend_width = min(2.92, w - 0.40)
    legend_x = x + (w - legend_width) / 2
    for index, (participants, color) in enumerate(legend):
        item_x = legend_x + index * (legend_width / 3)
        add_line_segment(slide, item_x, y + 0.72, item_x + 0.24, y + 0.72, color, 2.0)
        add_text(
            slide,
            f"N={participants}",
            item_x + 0.29,
            y + 0.65,
            0.60,
            0.15,
            7.5,
            color,
            True,
            valign=MSO_ANCHOR.MIDDLE,
            margin=0,
        )

    plot_x = x + 0.52
    plot_y = y + 0.94
    plot_w = w - 0.72
    plot_h = h - 1.48
    x_ticks = (2, 10, 20, 30, 40, 50)

    for value, label in y_ticks:
        py = plot_y + plot_h - ((value - y_min) / (y_max - y_min)) * plot_h
        add_line_segment(slide, plot_x, py, plot_x + plot_w, py, BORDER, 0.6)
        add_text(
            slide,
            label,
            x + 0.04,
            py - 0.08,
            0.43,
            0.16,
            7.2,
            "686868",
            align=PP_ALIGN.RIGHT,
            valign=MSO_ANCHOR.MIDDLE,
            margin=0,
        )
    add_text(
        slide,
        "Round",
        plot_x,
        plot_y + plot_h + 0.23,
        plot_w,
        0.15,
        7.2,
        "686868",
        align=PP_ALIGN.CENTER,
        valign=MSO_ANCHOR.MIDDLE,
        margin=0,
    )
    for round_number in x_ticks:
        px = plot_x + ((round_number - 2) / 48) * plot_w
        add_line_segment(slide, px, plot_y, px, plot_y + plot_h, "E8E8E8", 0.45)
        add_text(
            slide,
            str(round_number),
            px - 0.18,
            plot_y + plot_h + 0.05,
            0.36,
            0.15,
            7.2,
            "686868",
            align=PP_ALIGN.CENTER,
            valign=MSO_ANCHOR.MIDDLE,
            margin=0,
        )
    add_line_segment(slide, plot_x, plot_y, plot_x, plot_y + plot_h, DARK, 0.9)
    add_line_segment(slide, plot_x, plot_y + plot_h, plot_x + plot_w, plot_y + plot_h, DARK, 0.9)

    if reference is not None:
        py = plot_y + plot_h - ((reference - y_min) / (y_max - y_min)) * plot_h
        add_line_segment(slide, plot_x, py, plot_x + plot_w, py, MID, 1.0, dashed=True)
        add_text(
            slide,
            "chance",
            plot_x + plot_w - 0.54,
            py - 0.18,
            0.50,
            0.14,
            7.0,
            "686868",
            align=PP_ALIGN.RIGHT,
            margin=0,
        )

    for participants, color in legend:
        points = []
        for row in runs[participants]:
            px = plot_x + ((row["round"] - 2) / 48) * plot_w
            value = max(y_min, min(y_max, row[metric]))
            py = plot_y + plot_h - ((value - y_min) / (y_max - y_min)) * plot_h
            points.append((px, py))
        for first, second in zip(points, points[1:]):
            add_line_segment(slide, first[0], first[1], second[0], second[1], color, 1.65)


def add_bezier_arrow(
    slide,
    start,
    control,
    end,
    color=BLUE,
    width=1.8,
    dashed=False,
    segments=24,
    end_arrow=True,
):
    points = []
    for step in range(segments + 1):
        t = step / segments
        x = (1 - t) ** 2 * start[0] + 2 * (1 - t) * t * control[0] + t**2 * end[0]
        y = (1 - t) ** 2 * start[1] + 2 * (1 - t) * t * control[1] + t**2 * end[1]
        points.append((x, y))
    for index, (first, second) in enumerate(zip(points, points[1:])):
        is_last = index == segments - 1
        if dashed and not is_last and index % 5 in {3, 4}:
            continue
        add_line_segment(
            slide,
            first[0],
            first[1],
            second[0],
            second[1],
            color,
            width,
            arrow=is_last and end_arrow,
        )


def add_hospital_campus_icon(slide, cx, cy, color=BLUE, scale=1.0):
    add_box(slide, cx - 0.25 * scale, cy - 0.01 * scale, 0.50 * scale, 0.23 * scale, fill=WHITE, line=color, radius=False, line_width=1.2)
    add_box(slide, cx - 0.14 * scale, cy - 0.27 * scale, 0.28 * scale, 0.49 * scale, fill=WHITE, line=color, radius=False, line_width=1.2)
    add_box(slide, cx - 0.10 * scale, cy - 0.22 * scale, 0.20 * scale, 0.15 * scale, fill=color, line=color, radius=True, line_width=0.5)
    add_text(slide, "H", cx - 0.08 * scale, cy - 0.215 * scale, 0.16 * scale, 0.12 * scale, 8.5 * scale, WHITE, True, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE, margin=0)
    add_box(slide, cx - 0.055 * scale, cy + 0.06 * scale, 0.11 * scale, 0.16 * scale, fill=color, line=color, radius=False, line_width=0.5)
    for offset in (-0.18, 0.18):
        add_box(slide, cx + offset * scale - 0.035 * scale, cy + 0.06 * scale, 0.07 * scale, 0.07 * scale, fill=color, line=color, radius=False, line_width=0.5)


def add_hospital_card(slide, center, name, highlight=False):
    cx, cy = center
    card_width = 1.96 if highlight else 1.72
    x = cx - card_width / 2
    y = cy - 0.38
    accent = TU_RED if highlight else BLUE
    fill = RED_TINT if highlight else BLUE_TINT
    add_box(slide, x, y, card_width, 0.76, fill=fill, line=accent, line_width=2.0 if highlight else 1.1)
    add_hospital_campus_icon(slide, x + 0.39, cy, accent, 0.82)
    text_width = card_width - 0.80
    add_text(slide, name, x + 0.70, y + 0.16, text_width, 0.19, 10.5, DARK, True)
    add_text(slide, "Local training", x + 0.70, y + 0.42, text_width, 0.16, 7.7, DARK)
    if highlight:
        add_text(slide, "Temporary aggregator", x + 0.68, y + 0.61, card_width - 0.72, 0.13, 6.0, TU_RED, True)


def add_oval(slide, x, y, w, h, fill, line=None, line_width=1.0):
    shape = slide.shapes.add_shape(
        MSO_AUTO_SHAPE_TYPE.OVAL,
        Inches(x),
        Inches(y),
        Inches(w),
        Inches(h),
    )
    set_fill(shape, fill)
    if line is None:
        shape.line.fill.background()
    else:
        set_line(shape, line, line_width)
    return shape


def add_physician_with_stethoscope(slide, x, y):
    skin = "E8BE9A"
    hair = "3B2B27"

    # Soft halo and white coat establish a friendly, non-photorealistic figure
    # while keeping every component editable in PowerPoint.
    add_oval(slide, x + 0.02, y, 2.80, 2.80, BLUE_TINT, line=BLUE, line_width=0.8)
    add_box(slide, x + 0.15, y + 1.55, 2.50, 2.18, fill=WHITE, line=BLUE, line_width=1.4)
    add_box(slide, x + 1.03, y + 1.59, 0.75, 1.14, fill=BLUE_TINT, line=BLUE, line_width=0.8)
    add_box(slide, x + 1.15, y + 1.22, 0.48, 0.48, fill=skin, line=skin, radius=False, line_width=0.5)

    # Head, hair, ears, and a minimal face.
    add_oval(slide, x + 0.94, y + 0.04, 1.03, 1.17, hair)
    add_oval(slide, x + 0.84, y + 0.53, 0.22, 0.30, skin)
    add_oval(slide, x + 1.84, y + 0.53, 0.22, 0.30, skin)
    add_oval(slide, x + 0.98, y + 0.17, 0.94, 1.06, skin)
    add_oval(slide, x + 1.22, y + 0.60, 0.07, 0.07, DARK)
    add_oval(slide, x + 1.62, y + 0.60, 0.07, 0.07, DARK)
    add_line_segment(slide, x + 1.34, y + 0.94, x + 1.57, y + 0.94, TU_RED, 1.0)

    # Coat lapels and center seam.
    add_line_segment(slide, x + 0.36, y + 1.77, x + 1.10, y + 2.45, BLUE, 1.1)
    add_line_segment(slide, x + 2.43, y + 1.77, x + 1.82, y + 2.45, BLUE, 1.1)
    add_line_segment(slide, x + 1.40, y + 2.42, x + 1.40, y + 3.61, BORDER, 0.9)

    # Stethoscope: two curved tubes, a stem, and a chest piece.
    add_bezier_arrow(
        slide,
        (x + 0.65, y + 1.78),
        (x + 0.61, y + 2.50),
        (x + 1.20, y + 2.62),
        DARK,
        1.8,
        segments=12,
        end_arrow=False,
    )
    add_bezier_arrow(
        slide,
        (x + 2.18, y + 1.78),
        (x + 2.22, y + 2.50),
        (x + 1.62, y + 2.62),
        DARK,
        1.8,
        segments=12,
        end_arrow=False,
    )
    add_bezier_arrow(
        slide,
        (x + 1.41, y + 2.62),
        (x + 1.42, y + 2.96),
        (x + 1.68, y + 3.12),
        DARK,
        1.8,
        segments=8,
        end_arrow=False,
    )
    add_oval(slide, x + 1.56, y + 3.04, 0.28, 0.28, WHITE, line=DARK, line_width=1.4)

    add_box(slide, x + 1.94, y + 2.50, 0.45, 0.28, fill=RED_TINT, line=TU_RED, line_width=0.8)
    add_text(slide, "MD", x + 2.00, y + 2.57, 0.33, 0.12, 6.5, TU_RED, True, align=PP_ALIGN.CENTER, margin=0)
    add_text(slide, "PHYSICIAN", x + 0.57, y + 3.83, 1.70, 0.18, 9.0, BLUE, True, align=PP_ALIGN.CENTER)


def add_divider(slide, x, y, w, color=BORDER, height=0.015):
    shape = slide.shapes.add_shape(
        MSO_AUTO_SHAPE_TYPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(height)
    )
    set_fill(shape, color)
    shape.line.fill.background()
    return shape


def add_content_title(slide, title: str, kicker: str, slide_number: int):
    title_size = 24 if len(title) < 43 else 21.5
    add_text(slide, title, 0.61, 0.32, 9.65, 0.62, title_size, DARK, False)
    add_text(slide, kicker.upper(), 0.62, 1.02, 9.7, 0.22, 9.5, TU_RED, True)
    add_divider(slide, 0.61, 1.30, 11.95, TU_RED, 0.018)
    add_text(slide, f"Page {slide_number}", 0.60, 6.88, 1.0, 0.22, 9.5, WHITE, False)
    add_text(
        slide,
        "Ramon Mehrpoya  |  Master's Thesis  |  Verifiable Decentralized Federated Machine Learning and Inference for AI Agent Systems  |  VITA-FL",
        1.75,
        6.88,
        9.35,
        0.22,
        8.5,
        WHITE,
        False,
    )
    add_text(
        slide,
        "19 August 2026",
        11.20,
        6.88,
        1.53,
        0.22,
        8.5,
        WHITE,
        False,
        align=PP_ALIGN.RIGHT,
    )


def add_note(slide, text: str):
    notes = slide.notes_slide.notes_text_frame
    notes.text = text
    for paragraph in notes.paragraphs:
        for run in paragraph.runs:
            set_run_language(run)


def image_fit(slide, path: Path, x, y, w, h):
    with Image.open(path) as image:
        ratio = image.width / image.height
    target = w / h
    if ratio > target:
        picture_width = w
        picture_height = w / ratio
    else:
        picture_height = h
        picture_width = h * ratio
    return slide.shapes.add_picture(
        str(path),
        Inches(x + (w - picture_width) / 2),
        Inches(y + (h - picture_height) / 2),
        Inches(picture_width),
        Inches(picture_height),
    )


def image_cover(slide, path: Path, x, y, w, h, focus_x=0.5):
    target_ratio = w / h
    with Image.open(path) as source:
        source = source.convert("RGB")
        source_ratio = source.width / source.height
        if source_ratio > target_ratio:
            crop_width = round(source.height * target_ratio)
            left = round((source.width - crop_width) * focus_x)
            left = max(0, min(left, source.width - crop_width))
            crop_box = (left, 0, left + crop_width, source.height)
        else:
            crop_height = round(source.width / target_ratio)
            top = max(0, (source.height - crop_height) // 2)
            crop_box = (0, top, source.width, top + crop_height)
        cropped = source.crop(crop_box)
        stream = BytesIO()
        cropped.save(stream, format="PNG")
        stream.seek(0)
        return slide.shapes.add_picture(
            stream,
            Inches(x),
            Inches(y),
            Inches(w),
            Inches(h),
        )


def add_template_student_photo(slide):
    """Reuse the credited student photograph and crop from the TU title template."""
    with ZipFile(TEMPLATE) as archive:
        stream = BytesIO(archive.read("ppt/media/image5.jpg"))
    picture = slide.shapes.add_picture(
        stream,
        Inches(-0.0071),
        Inches(1.3786),
        Inches(9.7171),
        Inches(3.5801),
    )
    picture.crop_top = 0.38334
    picture.crop_bottom = 0.06404
    picture.name = "Page 1 TU Berlin students photograph"
    return picture


def build_assets():
    ASSETS.mkdir(parents=True, exist_ok=True)
    required_assets = [
        ASSETS / "xray_concept.png",
        ASSETS / "physician-editorial-illustration-tablet.png",
        ASSETS / "computer-scientist-editorial-illustration.png",
        ASSETS / "ramon-mehrpoya-portrait-cutout.png",
    ]
    for asset in required_assets:
        if not asset.is_file():
            raise FileNotFoundError(f"Missing presentation asset: {asset}")


def remove_shape(shape):
    shape._element.getparent().remove(shape._element)


def delete_slide(prs, index: int):
    slide_id = prs.slides._sldIdLst[index]
    prs.part.drop_rel(slide_id.rId)
    prs.slides._sldIdLst.remove(slide_id)


def remove_slide_placeholders(slide):
    for shape in list(slide.shapes):
        if getattr(shape, "is_placeholder", False):
            remove_shape(shape)


def prepare_template() -> Presentation:
    if not TEMPLATE.exists():
        raise FileNotFoundError(f"TU Berlin template not found: {TEMPLATE}")
    prs = Presentation(TEMPLATE)
    while len(prs.slides):
        delete_slide(prs, 0)

    # Keep the official logo and red footer, but remove unfinished sample fields.
    content_master = prs.slide_masters[1]
    for shape in list(content_master.shapes):
        if shape.name in {"Bildplatzhalter 8", "Textfeld 18", "Textfeld 19"}:
            remove_shape(shape)

    prs.core_properties.title = "VITA-FL — Master's Thesis Presentation"
    prs.core_properties.subject = (
        "Verifiable Decentralized Federated Machine Learning and Inference for AI Agent Systems"
    )
    prs.core_properties.author = "Ramon Mehrpoya"
    prs.core_properties.keywords = "VITA-FL, DFL, TEE, attested inference, transparency log"
    prs.core_properties.language = LANGUAGE
    return prs


def new_title_slide(prs):
    slide = prs.slides.add_slide(prs.slide_masters[0].slide_layouts[0])
    remove_slide_placeholders(slide)
    return slide


def new_content_slide(prs, _declared_number, title, kicker):
    slide = prs.slides.add_slide(prs.slide_masters[1].slide_layouts[0])
    remove_slide_placeholders(slide)
    # Derive the visible page number from the actual deck order so removing or
    # inserting a slide cannot leave stale footer numbers behind.
    add_content_title(slide, title, kicker, len(prs.slides))
    return slide


def slide_title(prs):
    slide = new_title_slide(prs)
    add_template_student_photo(slide)
    add_text(
        slide,
        "© Philipp Arnoldt",
        8.50,
        4.72,
        1.02,
        0.14,
        6.3,
        WHITE,
        False,
        align=PP_ALIGN.RIGHT,
        valign=MSO_ANCHOR.MIDDLE,
        margin=0,
    )
    add_text(
        slide,
        "Verifiable Decentralized Federated Machine Learning\nand Inference for AI Agent Systems",
        0.60,
        5.30,
        9.11,
        1.18,
        24,
        WHITE,
        False,
        valign=MSO_ANCHOR.MIDDLE,
    )
    add_text(slide, "Ramon Mehrpoya", 0.61, 6.55, 3.25, 0.25, 14, WHITE, True)
    add_text(slide, "Master's Thesis", 0.61, 6.86, 3.25, 0.22, 10.5, WHITE)
    add_note(
        slide,
        "This presentation introduces VITA-FL, a prototype that connects verifiable decentralized "
        "federated learning to attested inference in an AI-agent system. It presents how the model, "
        "its production process, and its use during inference can be bound into one verifiable path.",
    )


def slide_about(prs):
    slide = new_content_slide(
        prs,
        2,
        "About me",
        "Academic background · project experience · Master's thesis",
    )

    portrait = image_fit(
        slide,
        ASSETS / "ramon-mehrpoya-portrait-cutout.png",
        0.72,
        1.51,
        3.92,
        4.40,
    )
    portrait.name = "Page 2 Ramon Mehrpoya portrait cutout"
    portrait_frame = slide.shapes.add_shape(
        MSO_AUTO_SHAPE_TYPE.ROUNDED_RECTANGLE,
        Inches(0.67),
        Inches(1.49),
        Inches(4.08),
        Inches(4.44),
    )
    portrait_frame.fill.background()
    set_line(portrait_frame, "9A9A9A", 1.35)
    portrait_frame.name = "Page 2 gray portrait frame"

    add_text(
        slide,
        "Ramon Mehrpoya",
        5.42,
        1.64,
        6.55,
        0.48,
        26,
        DARK,
        True,
        valign=MSO_ANCHOR.MIDDLE,
    )

    add_text(
        slide,
        "ACADEMIC BACKGROUND",
        5.43,
        2.58,
        2.65,
        0.20,
        8.4,
        TU_RED,
        True,
        valign=MSO_ANCHOR.MIDDLE,
    )
    add_text(
        slide,
        "Bachelor's degree in Business Informatics · TU Berlin",
        5.43,
        2.86,
        6.45,
        0.31,
        12.6,
        DARK,
        True,
        valign=MSO_ANCHOR.MIDDLE,
    )
    add_text(
        slide,
        "Master's thesis candidate · Computer Science · TU Berlin",
        5.43,
        3.17,
        6.45,
        0.31,
        12.6,
        DARK,
        True,
        valign=MSO_ANCHOR.MIDDLE,
    )

    add_text(
        slide,
        "PROJECT EXPERIENCE AT ISE, TU BERLIN",
        5.43,
        3.51,
        3.45,
        0.20,
        8.4,
        TU_RED,
        True,
        valign=MSO_ANCHOR.MIDDLE,
    )
    projects = [
        (5.42, "GAIA-X 4 PLC-AAD", "Blockchain &\nencryption", GREEN_TINT, GREEN),
        (7.63, "ZOKRATES PLUS", "ZK · TEE · remote\nattestation · DFL", BLUE_TINT, BLUE),
        (9.83, "ZODIAC", "AI agents &\nMCP tools", ORANGE_TINT, ORANGE),
    ]
    for x, project, focus, fill, accent in projects:
        add_box(slide, x, 3.75, 2.13, 0.89, fill=fill, line=accent, line_width=1.2)
        add_text(
            slide,
            project,
            x + 0.08,
            3.91,
            1.97,
            0.18,
            7.8,
            accent,
            True,
            align=PP_ALIGN.CENTER,
            valign=MSO_ANCHOR.MIDDLE,
        )
        add_text(
            slide,
            focus,
            x + 0.10,
            4.22,
            1.93,
            0.35,
            8.4,
            DARK,
            True,
            align=PP_ALIGN.CENTER,
            valign=MSO_ANCHOR.MIDDLE,
        )
        add_arrow(slide, x + 1.065, 4.65, x + 1.065, 5.00, TU_RED, 1.8)

    add_box(slide, 5.42, 5.02, 6.54, 0.86, fill=RED_TINT, line=TU_RED, line_width=1.4)
    add_text(
        slide,
        "THESIS PROTOTYPE",
        5.68,
        5.16,
        1.72,
        0.18,
        7.8,
        TU_RED,
        True,
        valign=MSO_ANCHOR.MIDDLE,
    )
    add_text(
        slide,
        "VITA-FL",
        5.68,
        5.40,
        1.35,
        0.29,
        16.2,
        DARK,
        True,
        valign=MSO_ANCHOR.MIDDLE,
    )
    add_text(
        slide,
        "Verifiable Inference and Trust Architecture\nfor Federated Learning",
        7.13,
        5.38,
        4.42,
        0.38,
        9.6,
        DARK,
        True,
        valign=MSO_ANCHOR.MIDDLE,
    )

    add_note(
        slide,
        "Before turning to the research problem, I want to briefly introduce my background. I am a "
        "Computer Science master's thesis candidate at TU Berlin and hold a bachelor's degree in "
        "Business Informatics. At ISE, my focus in Gaia-X 4 PLC-AAD was blockchain and encryption. "
        "ZoKrates Plus brought together zero knowledge, trusted execution, remote attestation, and "
        "decentralized federated learning. ZODIAC focused on AI agents and MCP tools. These three "
        "strands led directly to VITA-FL: Verifiable Inference and Trust Architecture for Federated Learning.",
    )


def slide_problem(prs):
    slide = new_content_slide(prs, 3, "A plausible result is not evidence", "Starting point: the physician's request")
    add_box(slide, 0.67, 1.55, 3.08, 4.30, fill=DARK, line=DARK)
    image_fit(slide, ASSETS / "xray_concept.png", 0.94, 1.80, 2.54, 2.54)
    add_text(slide, "“Analyze this\nchest X-ray.”", 0.96, 4.46, 2.48, 0.65, 20, WHITE, True, align=PP_ALIGN.CENTER)
    physician_picture = image_cover(
        slide,
        ASSETS / "physician-editorial-illustration-tablet.png",
        4.18,
        1.55,
        8.18,
        4.56,
    )
    physician_picture.name = "Page 3 physician illustration with tablet"
    add_box(slide, 4.47, 1.88, 3.52, 2.51, fill=WHITE, line=TU_RED, line_width=1.5)
    add_box(slide, 4.47, 1.88, 0.10, 2.51, fill=TU_RED, line=TU_RED, radius=False)
    add_text(slide, "THE TEMPTING SHORTCUT", 4.87, 2.22, 2.72, 0.20, 9.5, TU_RED, True)
    add_text(
        slide,
        "“Can’t I just\nask an AI?”",
        4.87,
        2.76,
        2.84,
        0.91,
        25,
        DARK,
        True,
        valign=MSO_ANCHOR.MIDDLE,
    )
    add_text(
        slide,
        "But is it suitable\nfor clinical use?",
        4.87,
        3.93,
        2.78,
        0.43,
        10.5,
        "686868",
        True,
        valign=MSO_ANCHOR.MIDDLE,
    )
    add_note(
        slide,
        "Imagine a physician with a chest X-ray asking: Can't I just ask an AI? The AI can return a "
        "fluent and plausible result, but the response does not show whether it used the intended "
        "X-ray, the current model publication, or an attested inference path. The question is therefore "
        "not merely whether AI can answer, but whether the answer is backed by inspectable evidence.",
    )


def slide_engineering_response(prs):
    slide = new_content_slide(
        prs,
        4,
        "A trustworthy answer needs verifiable infrastructure",
        "The computer scientist's response",
    )

    scientist_picture = image_cover(
        slide,
        ASSETS / "computer-scientist-editorial-illustration.png",
        0.97,
        1.55,
        8.18,
        4.56,
    )
    scientist_picture.name = "Page 4 computer scientist illustration with tablet"

    add_box(slide, 5.35, 1.88, 3.52, 2.51, fill=WHITE, line=TU_RED, line_width=1.5)
    add_box(slide, 8.77, 1.88, 0.10, 2.51, fill=TU_RED, line=TU_RED, radius=False)
    add_text(slide, "THE ENGINEERING RESPONSE", 5.68, 2.22, 2.78, 0.20, 9.5, TU_RED, True)
    add_text(
        slide,
        "“Then we need more\nthan an AI model.”",
        5.55,
        2.70,
        3.16,
        0.86,
        18.5,
        DARK,
        True,
        valign=MSO_ANCHOR.MIDDLE,
    )
    add_text(
        slide,
        "Training, execution, and publication\nmust form one inspectable path.",
        5.55,
        3.80,
        3.02,
        0.43,
        9.7,
        "686868",
        True,
    )

    add_box(slide, 9.58, 1.55, 3.09, 4.31, fill=DARK, line=DARK)
    add_text(
        slide,
        "REQUIRED SYSTEM ARCHITECTURE",
        9.80,
        1.78,
        2.65,
        0.20,
        8.2,
        WHITE,
        True,
        align=PP_ALIGN.CENTER,
    )
    architecture_stages = [
        ("SIGNED MEDICAL DATA", GREEN),
        ("ATTESTED DFL", BLUE),
        ("VERIFIED MODEL STATE", PURPLE),
        ("AGENT + INFERENCE TEE", ORANGE),
        ("TRANSPARENCY LOG", TU_RED),
    ]
    row_tops = [2.10, 2.72, 3.33, 3.95, 4.57]
    for index, ((label, accent), top) in enumerate(zip(architecture_stages, row_tops), start=1):
        add_box(slide, 9.82, top, 2.61, 0.40, fill="505050", line="717171", line_width=0.8)
        add_oval(slide, 9.93, top + 0.08, 0.24, 0.24, accent)
        add_text(
            slide,
            str(index),
            9.96,
            top + 0.11,
            0.18,
            0.16,
            7.0,
            WHITE,
            True,
            align=PP_ALIGN.CENTER,
            valign=MSO_ANCHOR.MIDDLE,
            margin=0,
        )
        add_text(
            slide,
            label,
            10.27,
            top + 0.12,
            2.02,
            0.17,
            7.5,
            WHITE,
            True,
            valign=MSO_ANCHOR.MIDDLE,
            margin=0,
        )
        if index < len(architecture_stages):
            add_arrow(slide, 11.12, top + 0.42, 11.12, row_tops[index] - 0.03, MID, 1.3)
    add_text(
        slide,
        "Evidence follows every result.",
        9.86,
        5.48,
        2.53,
        0.20,
        7.8,
        WHITE,
        True,
        align=PP_ALIGN.CENTER,
    )
    add_note(
        slide,
        "The computer scientist's response is that a plausible model output is not enough. Trust must "
        "be engineered across the complete path: signed medical data enters an attested decentralized "
        "training process, the current model state is resolved from an authoritative publication, "
        "inference runs in a measured environment, and the resulting tool evidence is recorded in a "
        "transparency log. This requirement motivates the research gap on the next page: the individual "
        "mechanisms exist, but the challenge is to compose them into one user-inspectable system.",
    )


def slide_gap(prs):
    slide = new_content_slide(prs, 5, "Research gap and research questions", "The missing composition")
    areas = [
        ("DFL", "Model production", GREEN_TINT, GREEN),
        ("AGENT", "Tool orchestration", ORANGE_TINT, ORANGE),
        ("INFERENCE", "Attested execution", BLUE_TINT, BLUE),
    ]
    for index, (label, body, fill, accent) in enumerate(areas):
        x = 0.82 + index * 4.12
        add_box(slide, x, 1.53, 3.55, 1.08, fill=fill, line=accent)
        add_text(
            slide,
            label,
            x + 0.15,
            1.72,
            3.25,
            0.32,
            17,
            accent,
            True,
            align=PP_ALIGN.CENTER,
            valign=MSO_ANCHOR.MIDDLE,
        )
        add_text(
            slide,
            body,
            x + 0.15,
            2.14,
            3.25,
            0.27,
            10.5,
            DARK,
            align=PP_ALIGN.CENTER,
            valign=MSO_ANCHOR.MIDDLE,
        )
        if index < 2:
            add_text(
                slide,
                "?",
                x + 3.65,
                1.82,
                0.37,
                0.40,
                22,
                MID,
                True,
                align=PP_ALIGN.CENTER,
                valign=MSO_ANCHOR.MIDDLE,
            )
    add_box(slide, 0.72, 2.88, 11.89, 0.64, fill=TU_RED, line=TU_RED, radius=False)
    add_text(
        slide,
        "Gap: no inspectable path from decentralized training to verified inference.",
        0.95,
        3.02,
        11.43,
        0.36,
        15,
        WHITE,
        True,
        align=PP_ALIGN.CENTER,
        valign=MSO_ANCHOR.MIDDLE,
    )
    questions = [
        (
            "RQ 1:",
            "How can DFL models be integrated into AI agent-based system architectures while ensuring trustworthiness across the entire training and inference pipeline?",
            GREEN_TINT,
            GREEN,
        ),
        (
            "RQ 1.1:",
            "How can verifiable DFL guarantee integrity and availability during model training?",
            BLUE_TINT,
            BLUE,
        ),
        (
            "RQ 1.2:",
            "How can ML inference be made verifiable, such that the integrity of model predictions can be guaranteed, for example through cryptographic proofs of execution?",
            PURPLE_TINT,
            PURPLE,
        ),
    ]
    for index, (label, body, fill, accent) in enumerate(questions):
        x = 0.68 + index * 4.07
        add_box(slide, x, 3.70, 3.83, 2.24, fill=fill, line=accent)
        add_text(
            slide,
            label,
            x + 0.24,
            3.95,
            1.15,
            0.34,
            15,
            accent,
            True,
            valign=MSO_ANCHOR.MIDDLE,
        )
        add_text(
            slide,
            body,
            x + 0.24,
            4.38,
            3.35,
            1.43,
            11.8,
            DARK,
            False,
            valign=MSO_ANCHOR.MIDDLE,
        )
    add_note(
        slide,
        "The main research question asks how DFL models can be integrated into AI agent-based system "
        "architectures while preserving trustworthiness across the complete training and inference "
        "pipeline. The first sub-question focuses on integrity and availability during verifiable DFL "
        "training. The second asks how inference and model predictions can be made verifiable, for "
        "example through cryptographic proofs of execution.",
    )


def slide_architecture(prs):
    slide = new_content_slide(prs, 6, "VITA-FL: two responsibility blocks", "")
    add_box(slide, 0.63, 1.51, 5.98, 4.41, fill=GREEN_TINT, line=GREEN)
    add_box(slide, 6.73, 1.51, 5.97, 4.41, fill=BLUE_TINT, line=BLUE)
    add_text(slide, "DFL BLOCK", 0.88, 1.73, 1.8, 0.3, 14, GREEN, True)
    add_text(slide, "AGENT AND INFERENCE BLOCK", 6.98, 1.73, 3.4, 0.3, 14, BLUE, True)
    left_nodes = [
        (0.92, "DATA", "Signed medical\ninput", GREEN),
        (2.55, "WORKER TEE", "Attested\ntraining", GREEN),
        (4.28, "LEDGER", "Coordination\nand publication", GREEN),
    ]
    right_nodes = [
        (7.28, "RECEIVER TEE", "Independent resolution\nand inference", BLUE),
        (9.48, "MCP", "Three bounded\ntools", BLUE),
        (11.04, "LOG", "Receipts and\nevidence", PURPLE),
    ]
    for x, label, body, accent in left_nodes + right_nodes:
        width = 1.42 if x < 6 else 1.78 if x == 7.28 else 1.28
        add_box(slide, x, 2.32, width, 1.36, fill=WHITE, line=accent)
        add_text(
            slide,
            label,
            x + 0.06,
            2.49,
            width - 0.12,
            0.32,
            11.5,
            accent,
            True,
            align=PP_ALIGN.CENTER,
            valign=MSO_ANCHOR.MIDDLE,
        )
        add_text(
            slide,
            body,
            x + 0.06,
            2.89,
            width - 0.12,
            0.62,
            10,
            DARK,
            True,
            align=PP_ALIGN.CENTER,
            valign=MSO_ANCHOR.MIDDLE,
        )
    add_arrow(slide, 2.34, 3.01, 2.51, 3.01, MID, 1.3)
    add_arrow(slide, 3.97, 3.01, 4.24, 3.01, MID, 1.3)
    add_arrow(slide, 9.06, 3.01, 9.44, 3.01, MID, 1.3)
    add_arrow(slide, 10.76, 3.01, 11.00, 3.01, MID, 1.3)
    add_box(slide, 5.56, 3.94, 2.28, 0.97, fill=PURPLE_TINT, line=PURPLE)
    add_text(slide, "IPFS", 5.70, 4.11, 2.0, 0.26, 14, PURPLE, True, align=PP_ALIGN.CENTER)
    add_text(slide, "Signed, encrypted model", 5.72, 4.49, 1.96, 0.24, 10.5, DARK, True, align=PP_ALIGN.CENTER)
    add_arrow(slide, 5.70, 3.60, 6.16, 3.93, PURPLE, 1.7)
    add_arrow(slide, 7.20, 3.93, 7.70, 3.60, PURPLE, 1.7)
    add_text(
        slide,
        "The DFL block produces the authoritative model state.",
        1.02,
        4.29,
        4.30,
        0.62,
        16.5,
        DARK,
        True,
        align=PP_ALIGN.CENTER,
        valign=MSO_ANCHOR.MIDDLE,
    )
    add_text(
        slide,
        "The agent orchestrates the deterministic components.",
        7.82,
        4.29,
        4.38,
        0.62,
        16.5,
        DARK,
        True,
        align=PP_ALIGN.CENTER,
        valign=MSO_ANCHOR.MIDDLE,
    )
    add_note(
        slide,
        "VITA-FL separates two responsibilities. The DFL block admits measured workers, consumes "
        "attributable medical inputs, coordinates rounds, and publishes an encrypted and signed model. "
        "The agent and inference block independently resolves that publication and performs inference "
        "in a measured receiver workload. The language-model agent can initiate the workflow, but it "
        "cannot choose a local model, override a failed check, or convert missing evidence into a "
        "successful result.",
    )


def slide_dfl_hospitals(prs):
    slide = new_content_slide(
        prs,
        7,
        "Decentralized training across hospitals",
        "Local data · shared model · verifiable coordination",
    )
    hospitals = {
        "A": (3.71, 1.96),
        "B": (9.63, 1.96),
        "C": (10.67, 4.04),
        "D": (6.67, 5.21),
        "E": (2.67, 4.04),
    }

    # Clockwise role rotation between the admitted hospital participants.
    rotation_paths = [
        ((4.57, 1.71), (6.67, 1.37), (8.77, 1.71)),
        ((10.48, 2.17), (11.96, 2.71), (11.48, 3.71)),
        ((10.50, 4.40), (9.75, 5.83), (7.50, 5.50)),
        ((5.83, 5.50), (3.58, 5.83), (2.83, 4.40)),
        ((1.85, 3.71), (2.38, 2.75), (2.85, 2.17)),
    ]
    for start, control, end in rotation_paths:
        add_bezier_arrow(slide, start, control, end, ORANGE, 2.0, segments=18)

    # The encrypted current model is distributed to each worker.
    distribution_paths = [
        ((5.75, 2.45), (5.17, 1.71), (4.54, 2.00)),
        ((7.58, 2.45), (8.17, 1.71), (8.79, 2.00)),
        ((5.08, 3.33), (3.92, 3.38), (3.52, 3.92)),
        ((8.25, 3.33), (9.42, 3.38), (9.82, 3.92)),
    ]
    for start, control, end in distribution_paths:
        add_bezier_arrow(slide, start, control, end, TU_RED, 2.0, segments=16)

    # Round-bound signed worker updates converge on the selected aggregator.
    # End just outside the highlighted card.  The hospital cards are layered
    # above the paths, so endpoints inside Hospital D would hide the arrowheads.
    update_paths = [
        ((3.71, 2.36), (3.79, 4.67), (5.58, 4.73)),
        ((9.63, 2.36), (9.54, 4.67), (7.76, 4.73)),
        ((9.83, 4.29), (9.13, 5.50), (7.78, 5.23)),
        ((3.50, 4.29), (4.21, 5.50), (5.56, 5.23)),
    ]
    for start, control, end in update_paths:
        add_bezier_arrow(slide, start, control, end, BLUE, 2.0, dashed=True, segments=18)

    # The temporary aggregator publishes the next encrypted model artifact.
    add_bezier_arrow(slide, (6.67, 4.82), (6.67, 4.52), (6.67, 4.23), BLUE, 2.7, segments=10)
    add_text(slide, "Aggregated publication", 6.80, 4.48, 1.45, 0.18, 7.8, BLUE, True)

    for name, center in hospitals.items():
        add_hospital_card(slide, center, f"Hospital {name}", highlight=name == "D")

    add_box(slide, 5.08, 2.43, 3.17, 1.78, fill=RED_TINT, line=TU_RED, line_width=2.2)
    add_text(slide, "CURRENT ENCRYPTED", 5.56, 2.67, 2.21, 0.22, 10.5, TU_RED, True, align=PP_ALIGN.CENTER)
    add_text(slide, "GLOBAL MODEL", 5.30, 3.07, 2.73, 0.34, 19.5, DARK, True, align=PP_ALIGN.CENTER)
    # Native, editable padlock symbol.
    add_bezier_arrow(slide, (6.56, 3.57), (6.67, 3.40), (6.78, 3.57), TU_RED, 1.5, segments=8, end_arrow=False)
    add_box(slide, 6.51, 3.55, 0.32, 0.27, fill=TU_RED, line=TU_RED, line_width=0.5)
    add_text(slide, "•", 6.59, 3.59, 0.16, 0.12, 8, WHITE, True, align=PP_ALIGN.CENTER, margin=0)
    add_box(slide, 5.60, 3.90, 2.14, 0.24, fill=WHITE, line=BORDER, line_width=0.6)
    add_text(slide, "Resolved from the ledger", 5.69, 3.955, 1.96, 0.12, 7.7, DARK, align=PP_ALIGN.CENTER, margin=0)

    add_box(slide, 0.52, 1.78, 1.94, 1.72, fill=LIGHT, line=BORDER, line_width=1.0)
    add_text(slide, "DATA FLOW", 0.80, 1.98, 1.39, 0.18, 10.0, TU_RED, True, align=PP_ALIGN.CENTER)
    legend = [
        (2.38, TU_RED, False, "Encrypted model"),
        (2.73, BLUE, True, "Signed update"),
        (3.08, BLUE, False, "Publication"),
        (3.40, ORANGE, False, "Aggregator rotation"),
    ]
    for y, color, dashed, label in legend:
        add_arrow(slide, 0.76, y, 1.29, y, color, 1.9, dashed=dashed)
        add_text(slide, label, 1.42, y - 0.09, 0.91, 0.16, 7.4 if label != "Aggregator rotation" else 6.0, DARK)

    add_note(
        slide,
        "This slide illustrates one decentralized training round across five independent hospitals. "
        "Each hospital keeps its raw X-rays local and runs an admitted training worker. The current "
        "encrypted global model is distributed to the workers, while their signed and round-bound "
        "model updates converge on the temporary aggregator, shown here as Hospital D. That aggregator "
        "publishes the next global model. The orange clockwise arrows denote rotation of the temporary "
        "aggregator role between rounds; they do not represent patient-data transfer between hospitals.",
    )


def slide_dfl(prs):
    slide = new_content_slide(
        prs,
        8,
        "What makes the shared model verifiable?",
        "One evidence chain from signed input to finalized publication",
    )

    add_text(
        slide,
        "Source, execution, and publication stay bound to the same training round.",
        1.10,
        1.48,
        11.13,
        0.36,
        15.0,
        DARK,
        True,
        align=PP_ALIGN.CENTER,
        valign=MSO_ANCHOR.MIDDLE,
    )
    add_divider(slide, 1.50, 1.95, 10.33, TU_RED, 0.018)

    centers = [2.20, 6.67, 11.13]
    stages = [
        (
            "INPUT",
            "SIGNED, DICOM-INSPIRED INPUT",
            "Device signature binds image bytes.\nRadiologist signature binds the label.",
            "PROVENANCE",
            GREEN_TINT,
            GREEN,
        ),
        (
            "TEE",
            "ADMITTED WORKER TEE",
            "TDX/DCAP admits the measured workload.\nIt verifies inputs and runs the fixed round.",
            "MEASURED EXECUTION",
            BLUE_TINT,
            BLUE,
        ),
        (
            "LEDGER",
            "LEDGER-FINALIZED MODEL",
            "Finalization binds the round,\ninput root, and model hash.",
            "AUTHORITATIVE M(r+1)",
            PURPLE_TINT,
            PURPLE,
        ),
    ]

    # One artifact moves through one evidence chain; arrows are behind the three stages.
    add_arrow(slide, 2.84, 2.98, 6.03, 2.98, MID, 2.3)
    add_arrow(slide, 7.31, 2.98, 10.49, 2.98, MID, 2.3)
    add_text(slide, "authenticated sample", 3.35, 2.66, 2.18, 0.18, 8.0, GREEN, True, align=PP_ALIGN.CENTER)
    add_text(slide, "signed update commitment", 7.83, 2.66, 2.15, 0.18, 8.0, BLUE, True, align=PP_ALIGN.CENTER)

    for center, (short, heading, body, outcome, fill, accent) in zip(centers, stages):
        add_oval(slide, center - 0.64, 2.34, 1.28, 1.28, fill, accent, 2.0)
        add_text(
            slide,
            short,
            center - 0.54,
            2.73,
            1.08,
            0.34,
            13.0 if short != "LEDGER" else 10.5,
            accent,
            True,
            align=PP_ALIGN.CENTER,
            valign=MSO_ANCHOR.MIDDLE,
            margin=0,
        )
        add_text(slide, heading, center - 1.70, 3.83, 3.40, 0.28, 11.2, accent, True, align=PP_ALIGN.CENTER)
        add_text(
            slide,
            body,
            center - 1.70,
            4.22,
            3.40,
            0.58,
            10.5,
            DARK,
            False,
            align=PP_ALIGN.CENTER,
            valign=MSO_ANCHOR.MIDDLE,
        )
        add_text(slide, outcome, center - 1.40, 4.93, 2.80, 0.20, 8.2, accent, True, align=PP_ALIGN.CENTER)

    add_box(slide, 0.90, 5.44, 11.53, 0.55, fill=TU_RED, line=TU_RED, radius=False)
    add_text(
        slide,
        "A model becomes authoritative only when all three links verify; a broken link stops finalization.",
        1.18,
        5.58,
        10.97,
        0.24,
        11.3,
        WHITE,
        True,
        align=PP_ALIGN.CENTER,
        valign=MSO_ANCHOR.MIDDLE,
    )
    add_note(
        slide,
        "This slide makes one claim: the shared model is verifiable only when one evidence chain remains "
        "intact. DICOM-inspired source signatures bind the image bytes and their annotation. An admitted "
        "TDX worker verifies those inputs and produces the round-bound update inside the measured workload. "
        "Ledger finalization then binds the round, input root, and model hash into the next authoritative "
        "model state. If any link fails, the child model is not finalized. The next slide explains why "
        "VITA-FL executes the operational worker relation with TEE and remote attestation rather than as "
        "one comprehensive zero-knowledge proof.",
    )


def slide_tee_vs_zk(prs):
    slide = new_content_slide(
        prs,
        9,
        "Why TEE/RA for the operational path?",
        "Two independent ZK relations—not one neural-network circuit",
    )

    add_box(slide, 0.66, 1.47, 12.00, 0.51, fill=LIGHT, line=TU_RED, radius=False)
    add_rich_text(
        slide,
        [
            ("RELATION SCOPE   ", TU_RED, True, 10.5),
            ("The proof would need to cover the surrounding cryptographic workflow as well as the tensors.", DARK, True, 12.0),
        ],
        0.88,
        1.60,
        11.56,
        0.24,
        align=PP_ALIGN.CENTER,
        valign=MSO_ANCHOR.MIDDLE,
    )

    panels = [
        (
            0.62,
            "WORKER TRAINING AS A ZK RELATION",
            "EVERY ROUND",
            "STATEFUL TRAINING TRANSITION",
            [
                "Resolve the exact parent model, round policy, and signed training inputs",
                "Decrypt model material and verify signatures, commitments, hashes, and nonces",
                "Encode forward/backward passes, optimizer state, and tensor updates",
                "Hash, sign, encrypt, wrap, and package the resulting update for the aggregator",
            ],
            PURPLE_TINT,
            PURPLE,
            ORANGE,
        ),
        (
            6.82,
            "DCAP ADMISSION AS A ZK RELATION",
            "PER ADMISSION",
            "QUOTE AND MEASUREMENT APPRAISAL",
            [
                "Parse Quote V4, TD report, certificate chain, QE identity, and TCB information",
                "Verify P-256 signatures, hashes, revocation material, freshness, and appraisal policy",
                "Replay every ordered application event into RTMR3 and match the quoted value",
                "Bind REPORTDATA, Compose, image, registry, caller, role policy, and one-time nonce",
            ],
            BLUE_TINT,
            BLUE,
            GREEN,
        ),
    ]
    for x, heading, status, claim, bullets, fill, accent, status_color in panels:
        add_box(slide, x, 2.17, 5.88, 2.94, fill=fill, line=accent, line_width=1.2)
        add_text(slide, heading, x + 0.25, 2.39, 4.00, 0.35, 12.7, accent, True)
        add_box(slide, x + 4.31, 2.35, 1.25, 0.35, fill=status_color, line=status_color, radius=False)
        add_text(
            slide,
            status,
            x + 4.38,
            2.44,
            1.11,
            0.18,
            8.4,
            WHITE,
            True,
            align=PP_ALIGN.CENTER,
            valign=MSO_ANCHOR.MIDDLE,
        )
        add_text(slide, claim, x + 0.27, 2.86, 5.30, 0.22, 9.5, accent, True)
        add_bullets(
            slide,
            bullets,
            x + 0.26,
            3.14,
            5.34,
            1.72,
            9.9,
            DARK,
            accent,
            3,
        )

    add_box(slide, 0.92, 5.38, 11.50, 0.54, fill=TU_RED, line=TU_RED, radius=False)
    add_rich_text(
        slide,
        [
            ("VITA-FL DECISION   ", WHITE, True, 10.2),
            (
                "TEE/RA keeps both relations native and stateful; ZK remains useful for narrow encoded claims.",
                WHITE,
                True,
                11.0,
            ),
        ],
        1.15,
        5.53,
        11.04,
        0.25,
        align=PP_ALIGN.CENTER,
        valign=MSO_ANCHOR.MIDDLE,
    )
    add_text(
        slide,
        "Scope statement—not a measured TEE-over-ZK speedup. Sources: RFC 9334 · Intel TDX/DCAP · Chen et al., EuroSys ’24.",
        0.77,
        6.02,
        11.78,
        0.16,
        7.1,
        DARK,
        False,
        align=PP_ALIGN.CENTER,
        margin=0,
    )
    add_note(
        slide,
        "Two independent relations explain why VITA-FL does not use a zero-knowledge proof as its "
        "operational worker path. A complete training proof would cover much more than the neural network: "
        "it would need the exact parent and policy, signed-input checks, decryption and signature checks, "
        "the iterative optimizer transition, and the hashing, signing, encryption, key wrapping, and package "
        "formation performed after training. That proof is needed for every worker transition in every round. "
        "Separately, proving DCAP registration would require quote and certificate parsing, cryptographic "
        "signature and hash verification, collateral and TCB appraisal, and a complete ordered RTMR3 replay "
        "with REPORTDATA and enrollment bindings. VITA-FL instead executes these stateful relations natively "
        "inside measured TDX workloads and appraises remote-attestation evidence. This is a relation-scope "
        "argument, not an empirical claim that TEEs are universally faster than ZK. ZK remains suitable for "
        "narrow, precisely encoded claims. References: IETF RFC 9334; Intel TDX/DCAP documentation; and "
        "Chen et al., ZKML, EuroSys 2024, https://doi.org/10.1145/3627703.3650088.",
    )


def slide_phala_attestation_keys(prs):
    slide = new_content_slide(
        prs,
        10,
        "From Intel-backed evidence to app-bound secrets",
        "Live Phala path · independent quote verification · path-separated dstack keys",
    )

    # Left: evidence creation and certificate/collateral verification.
    add_box(slide, 0.48, 1.48, 7.16, 4.36, fill=ORANGE_TINT, line=ORANGE, line_width=1.2)
    add_text(slide, "A · VERIFY THE TDX EVIDENCE", 0.76, 1.68, 2.55, 0.25, 12.5, ORANGE, True)

    add_box(slide, 3.02, 1.62, 4.22, 0.60, fill=WHITE, line=ORANGE, line_width=1.0)
    add_text(
        slide,
        "INTEL PCS / PCCS COLLATERAL",
        3.18,
        1.72,
        3.90,
        0.18,
        9.5,
        ORANGE,
        True,
        align=PP_ALIGN.CENTER,
        valign=MSO_ANCHOR.MIDDLE,
    )
    add_text(
        slide,
        "PCK chain + validity · CRLs · QE identity · TCB info",
        3.18,
        1.95,
        3.90,
        0.15,
        8.0,
        DARK,
        align=PP_ALIGN.CENTER,
        valign=MSO_ANCHOR.MIDDLE,
    )

    add_box(slide, 0.76, 2.48, 1.78, 1.42, fill=BLUE_TINT, line=BLUE, line_width=1.1)
    add_text(slide, "MEASURED CVM", 0.91, 2.69, 1.48, 0.25, 11.5, BLUE, True, align=PP_ALIGN.CENTER)
    add_text(
        slide,
        "MRTD + RTMR0–2\nRTMR3 event log\nREPORTDATA",
        0.91,
        3.04,
        1.48,
        0.66,
        9.6,
        DARK,
        True,
        align=PP_ALIGN.CENTER,
        valign=MSO_ANCHOR.MIDDLE,
    )

    add_box(slide, 2.84, 2.48, 1.66, 1.42, fill=RED_TINT, line=TU_RED, line_width=1.1)
    add_text(slide, "TDX QUOTE V4", 2.98, 2.69, 1.38, 0.25, 11.5, TU_RED, True, align=PP_ALIGN.CENTER)
    add_text(
        slide,
        "Quoting Enclave signature\nPCK certificate",
        2.98,
        3.12,
        1.38,
        0.46,
        9.2,
        DARK,
        True,
        align=PP_ALIGN.CENTER,
        valign=MSO_ANCHOR.MIDDLE,
    )

    add_box(slide, 4.82, 2.36, 2.40, 1.68, fill=WHITE, line=ORANGE, line_width=1.4)
    add_text(slide, "DCAP VERIFIER", 5.04, 2.57, 1.96, 0.25, 12.0, ORANGE, True, align=PP_ALIGN.CENTER)
    add_text(
        slide,
        "Intel-rooted signatures\nRevocation + TCB status\nMeasurements + challenge",
        5.04,
        2.98,
        1.96,
        0.75,
        9.6,
        DARK,
        True,
        align=PP_ALIGN.CENTER,
        valign=MSO_ANCHOR.MIDDLE,
    )

    add_arrow(slide, 2.55, 3.19, 2.79, 3.19, BLUE, 1.6)
    add_arrow(slide, 4.51, 3.19, 4.76, 3.19, TU_RED, 1.6)
    add_arrow(slide, 5.98, 2.23, 5.98, 2.33, ORANGE, 1.4)

    add_box(slide, 4.99, 4.26, 2.06, 0.55, fill=GREEN_TINT, line=GREEN, line_width=1.1)
    add_text(
        slide,
        "VERIFIED APP IDENTITY",
        5.12,
        4.42,
        1.80,
        0.22,
        10.4,
        GREEN,
        True,
        align=PP_ALIGN.CENTER,
        valign=MSO_ANCHOR.MIDDLE,
    )
    add_arrow(slide, 6.02, 4.05, 6.02, 4.23, GREEN, 1.5)

    add_box(slide, 0.78, 4.30, 3.72, 1.10, fill=PURPLE_TINT, line=PURPLE, line_width=1.0)
    add_text(slide, "VITA-FL ON-CHAIN ADMISSION", 1.00, 4.50, 3.28, 0.22, 10.6, PURPLE, True)
    add_text(
        slide,
        "Independently checks the pinned base tuple, replays RTMR3, and binds workload, participant, action key, and nonce.",
        1.00,
        4.82,
        3.28,
        0.43,
        8.7,
        DARK,
        True,
        valign=MSO_ANCHOR.MIDDLE,
    )
    add_arrow(slide, 3.67, 3.92, 3.67, 4.27, PURPLE, 1.4, dashed=True)

    # Right: the attested KMS provisions deterministic material through dstack.sock.
    add_box(slide, 7.82, 1.48, 5.02, 4.36, fill=BLUE_TINT, line=BLUE, line_width=1.2)
    add_text(slide, "B · DERIVE APP-BOUND SECRETS", 8.08, 1.68, 4.42, 0.25, 11.8, BLUE, True)

    add_box(slide, 8.10, 2.08, 4.47, 1.02, fill=GREEN_TINT, line=GREEN, line_width=1.2)
    # Editable key glyph.
    add_oval(slide, 8.35, 2.39, 0.34, 0.34, WHITE, line=GREEN, line_width=1.4)
    add_line_segment(slide, 8.67, 2.56, 9.03, 2.56, GREEN, 2.0)
    add_line_segment(slide, 8.91, 2.56, 8.91, 2.72, GREEN, 2.0)
    add_line_segment(slide, 9.02, 2.56, 9.02, 2.67, GREEN, 2.0)
    add_text(slide, "ATTESTED DSTACK KMS", 9.18, 2.29, 3.08, 0.24, 12.2, GREEN, True, align=PP_ALIGN.CENTER)
    add_text(
        slide,
        "Verifies quote + policy · protects the KMS root secret",
        9.18,
        2.63,
        3.08,
        0.23,
        9.2,
        DARK,
        True,
        align=PP_ALIGN.CENTER,
    )
    add_arrow(slide, 7.08, 4.53, 8.04, 2.72, GREEN, 1.6, dashed=True)

    add_box(slide, 8.58, 3.34, 3.42, 0.47, fill=WHITE, line=BLUE, line_width=1.0)
    add_text(
        slide,
        "GetKey(app ID, path) via dstack.sock",
        8.72,
        3.46,
        3.14,
        0.22,
        10.1,
        BLUE,
        True,
        align=PP_ALIGN.CENTER,
        valign=MSO_ANCHOR.MIDDLE,
    )
    add_arrow(slide, 10.29, 3.11, 10.29, 3.31, GREEN, 1.4)

    key_outputs = [
        (8.06, "ACTION", "HMAC →\nsecp256k1", BLUE_TINT, BLUE),
        (9.62, "RSA CUSTODY", "HKDF →\nAES-GCM wrap", ORANGE_TINT, ORANGE),
        (11.18, "AIR RECEIPT", "Ed25519\nsigning key", PURPLE_TINT, PURPLE),
    ]
    for x, heading, body, fill, accent in key_outputs:
        add_box(slide, x, 4.08, 1.40, 1.08, fill=fill, line=accent, line_width=1.0)
        add_text(slide, heading, x + 0.08, 4.25, 1.24, 0.20, 8.6, accent, True, align=PP_ALIGN.CENTER)
        add_text(
            slide,
            body,
            x + 0.08,
            4.57,
            1.24,
            0.38,
            8.7,
            DARK,
            True,
            align=PP_ALIGN.CENTER,
            valign=MSO_ANCHOR.MIDDLE,
        )
    add_arrow(slide, 10.29, 3.82, 10.29, 4.02, BLUE, 1.4)
    add_text(
        slide,
        "Same app + path ⇒ same key\nDifferent app or path ⇒ different key",
        8.08,
        5.26,
        4.50,
        0.32,
        8.1,
        DARK,
        True,
        align=PP_ALIGN.CENTER,
        valign=MSO_ANCHOR.MIDDLE,
    )
    add_text(
        slide,
        "App-bound ≠ non-exportable: protect returned material.",
        8.08,
        5.62,
        4.50,
        0.14,
        7.4,
        TU_RED,
        True,
        align=PP_ALIGN.CENTER,
        valign=MSO_ANCHOR.MIDDLE,
        margin=0,
    )

    add_box(slide, 0.72, 5.94, 11.91, 0.30, fill=RED_TINT, line=TU_RED, radius=False, line_width=0.8)
    add_text(
        slide,
        "Attestation authenticates measured identity—not bug-free code; Intel TDX and the KMS TEE remain trust anchors.",
        0.92,
        6.01,
        11.51,
        0.16,
        9.6,
        TU_RED,
        True,
        align=PP_ALIGN.CENTER,
        valign=MSO_ANCHOR.MIDDLE,
        margin=0,
    )
    add_note(
        slide,
        "The workload does not validate its own claim. The measured Phala CVM asks the Intel TDX "
        "Quoting Enclave to turn its TD report into Quote V4 evidence. A verifier validates the "
        "Intel-rooted PCK chain, certificate validity and revocation information, Quoting Enclave "
        "identity, platform TCB status, measurements, and REPORTDATA. In dstack, the separately "
        "attested KMS verifies quote and policy before deriving deterministic 32-byte material bound "
        "to the application identity and requested path. The application receives it through "
        "/var/run/dstack.sock. VITA-FL uses separate paths to derive the secp256k1 action authority, "
        "an AES-256-GCM wrapping key for a random RSA-3072 participant key, and the Ed25519 AIR key. "
        "The VITA-FL registry independently verifies the live quote on chain, including the pinned "
        "dstack base tuple, replayed RTMR3 event log, workload policy, REPORTDATA, and enrollment "
        "binding. Official references: https://github.com/Dstack-TEE/dstack, "
        "https://docs.phala.com/phala-cloud/key-management/get-a-key, and "
        "https://cc-enabling.trustedservices.intel.com/intel-tdx-enabling-guide/02/infrastructure_setup/.",
    )


def slide_aggregator_selection(prs):
    slide = new_content_slide(
        prs,
        11,
        "Weighted aggregator selection",
        "Participation raises probability without excluding newcomers",
    )
    add_box(slide, 0.78, 1.49, 11.78, 0.55, fill=LIGHT, line=BORDER, radius=False)
    add_text(
        slide,
        "P(worker i) = (score_i + 1) / Σ(score_j + 1)",
        1.02,
        1.62,
        11.30,
        0.28,
        17,
        DARK,
        True,
        align=PP_ALIGN.CENTER,
        valign=MSO_ANCHOR.MIDDLE,
    )

    examples = [
        ("WORKER A", 0, 1, BLUE_TINT, BLUE),
        ("WORKER B", 1, 2, RED_TINT, TU_RED),
        ("WORKER C", 3, 4, GREEN_TINT, GREEN),
        ("WORKER D", 6, 7, PURPLE_TINT, PURPLE),
    ]
    for index, (name, score, weight, fill, accent) in enumerate(examples):
        x = 0.86 + index * 3.06
        add_box(slide, x, 2.23, 2.70, 0.92, fill=fill, line=accent)
        add_text(slide, name, x + 0.12, 2.38, 2.46, 0.20, 10.5, accent, True, align=PP_ALIGN.CENTER)
        add_text(
            slide,
            f"score {score}  →  weight {weight}",
            x + 0.12,
            2.72,
            2.46,
            0.23,
            12,
            DARK,
            True,
            align=PP_ALIGN.CENTER,
            valign=MSO_ANCHOR.MIDDLE,
        )

    bar_x, bar_y, bar_w, bar_h = 1.00, 3.50, 11.32, 0.70
    weights = [1, 2, 4, 7]
    colors = [BLUE, TU_RED, GREEN, PURPLE]
    percentages = ["7.1%", "14.3%", "28.6%", "50.0%"]
    cursor = bar_x
    for weight, color, percentage in zip(weights, colors, percentages):
        width = bar_w * weight / sum(weights)
        add_box(slide, cursor, bar_y, width, bar_h, fill=color, line=WHITE, radius=False, line_width=0.7)
        add_text(
            slide,
            percentage,
            cursor + 0.02,
            bar_y + 0.20,
            width - 0.04,
            0.26,
            10 if width > 1.0 else 8.2,
            WHITE,
            True,
            align=PP_ALIGN.CENTER,
            valign=MSO_ANCHOR.MIDDLE,
            margin=0,
        )
        cursor += width
    add_box(slide, 0.82, 4.38, 11.70, 0.64, fill=LIGHT, line=TU_RED, radius=False)
    add_rich_text(
        slide,
        [
            ("1 · HASH DRAW CONTEXT   ", TU_RED, True, 10.0),
            (
                "r = uint256(keccak256(prevrandao, timestamp, block number, round, "
                "current aggregator public address))",
                DARK,
                True,
                10.2,
            ),
        ],
        1.02,
        4.57,
        11.30,
        0.22,
        align=PP_ALIGN.CENTER,
        valign=MSO_ANCHOR.MIDDLE,
    )

    add_box(slide, 0.82, 5.16, 5.78, 0.78, fill=BLUE_TINT, line=BLUE)
    add_text(slide, "2 · DRAW ONE TICKET", 1.08, 5.31, 2.18, 0.20, 10.5, BLUE, True)
    add_text(
        slide,
        "ticket = r mod W = r mod 14  ∈  {0, …, 13}",
        1.08,
        5.57,
        5.20,
        0.22,
        12.2,
        DARK,
        True,
        align=PP_ALIGN.CENTER,
        valign=MSO_ANCHOR.MIDDLE,
    )
    add_box(slide, 6.78, 5.16, 5.74, 0.78, fill=GREEN_TINT, line=GREEN)
    add_text(slide, "3 · MAP TO CUMULATIVE INTERVAL", 7.04, 5.31, 3.20, 0.20, 10.5, GREEN, True)
    add_text(
        slide,
        "A: 0   ·   B: 1–2   ·   C: 3–6   ·   D: 7–13   |   Example: 5 → C",
        7.04,
        5.57,
        5.18,
        0.22,
        10.4,
        DARK,
        True,
        align=PP_ALIGN.CENTER,
        valign=MSO_ANCHOR.MIDDLE,
    )
    source = add_rich_text(
        slide,
        [
            ("prevrandao pseudorandom value: ", DARK, False, 7.5),
            ("https://eips.ethereum.org/EIPS/eip-4399", TU_RED, False, 7.5),
        ],
        0.90,
        6.10,
        11.54,
        0.16,
        align=PP_ALIGN.CENTER,
        valign=MSO_ANCHOR.MIDDLE,
    )
    source.text_frame.paragraphs[0].runs[-1].hyperlink.address = "https://eips.ethereum.org/EIPS/eip-4399"
    add_note(
        slide,
        "Each authorized worker receives weight score plus one. In the example the weights sum to 14, "
        "so the displayed probabilities are one, two, four, and seven divided by 14. For the normal "
        "selection, the contract hashes prevrandao, the block timestamp, block number, round, and the "
        "current aggregator public address. The resulting 256-bit value is converted to an integer and "
        "reduced modulo the total weight. This produces one ticket from zero through 13. The ticket is "
        "then mapped into the cumulative intervals in the displayed worker order: A receives zero, B "
        "one through two, C three through six, and D seven through 13. A ticket of five therefore selects "
        "Worker C. The interval widths—not the hash itself—create the probabilities. prevrandao is the "
        "EVM-accessible beacon-chain RANDAO value specified by EIP-4399 and is pseudorandom rather than "
        "an unbiased randomness oracle. Source: https://eips.ethereum.org/EIPS/eip-4399.",
    )


def slide_aggregator_recovery(prs):
    slide = new_content_slide(
        prs,
        12,
        "Quorum recovery when an aggregator stalls",
        "Abort the attempt · preserve the last finalized model · select a successor",
    )
    # Recovery changes protocol state while a separate green rail preserves model state.
    add_arrow(slide, 1.91, 2.74, 2.24, 2.74, TU_RED, 1.7)
    for y in (2.12, 2.57, 3.02):
        add_bezier_arrow(slide, (3.06, y + 0.17), (3.46, y + 0.17), (3.72, 2.74), PURPLE, 1.2, segments=8)
    add_arrow(slide, 5.86, 2.74, 6.48, 2.74, TU_RED, 1.8)
    add_arrow(slide, 7.96, 2.74, 8.56, 2.74, ORANGE, 1.8)
    add_arrow(slide, 10.04, 2.74, 10.72, 2.74, BLUE, 1.8)
    add_arrow(slide, 11.47, 3.48, 11.47, 4.72, BLUE, 1.5)

    add_oval(slide, 0.50, 2.00, 1.46, 1.46, BLUE_TINT, BLUE, 1.8)
    add_text(slide, "ROUND r", 0.72, 2.31, 1.02, 0.25, 12.5, BLUE, True, align=PP_ALIGN.CENTER)
    add_text(slide, "AGGREGATOR\nSTALLED", 0.66, 2.70, 1.14, 0.46, 9.6, DARK, True, align=PP_ALIGN.CENTER)
    add_text(slide, "repeated lack of progress", 0.36, 3.53, 1.76, 0.22, 8.0, DARK, align=PP_ALIGN.CENTER)

    add_text(slide, "SIGNED TIMEOUT REPORTS", 2.03, 1.57, 1.43, 0.36, 8.9, PURPLE, True, align=PP_ALIGN.CENTER)
    for index, y in enumerate((2.12, 2.57, 3.02), 1):
        add_oval(slide, 2.39, y, 0.38, 0.38, PURPLE_TINT, PURPLE, 1.1)
        add_text(slide, f"W{index}", 2.45, y + 0.10, 0.26, 0.16, 7.0, PURPLE, True, align=PP_ALIGN.CENTER, margin=0)
    add_text(slide, "action key binds exact\nround + aggregator\nduplicates reject", 1.93, 3.51, 1.54, 0.62, 7.8, DARK, align=PP_ALIGN.CENTER)

    add_oval(slide, 3.72, 1.66, 2.14, 2.14, PURPLE_TINT, PURPLE, 2.2)
    add_line_segment(slide, 3.95, 2.72, 5.63, 2.72, PURPLE, 2.0)
    add_text(slide, "FIRST REPORT\nFREEZES E", 4.08, 1.99, 1.42, 0.43, 9.0, PURPLE, True, align=PP_ALIGN.CENTER)
    add_text(slide, "q = ceil(E × 50 / 100)", 3.99, 2.51, 1.60, 0.30, 10.0, DARK, True, align=PP_ALIGN.CENTER)
    add_text(slide, "50% quorum\nof eligible reporters", 4.08, 2.98, 1.42, 0.40, 8.1, DARK, align=PP_ALIGN.CENTER)
    add_text(slide, "q reached", 5.90, 2.45, 0.55, 0.20, 7.5, TU_RED, True, align=PP_ALIGN.CENTER)

    add_oval(slide, 6.50, 2.00, 1.46, 1.46, RED_TINT, TU_RED, 2.0)
    add_text(slide, "ABORT r", 6.71, 2.30, 1.04, 0.25, 12.0, TU_RED, True, align=PP_ALIGN.CENTER)
    add_text(slide, "penalize · record\nadvance to r+1", 6.66, 2.69, 1.14, 0.46, 8.6, DARK, True, align=PP_ALIGN.CENTER)
    add_text(slide, "NO M(r)", 6.71, 3.56, 1.04, 0.20, 8.4, TU_RED, True, align=PP_ALIGN.CENTER)

    add_oval(slide, 8.58, 2.00, 1.46, 1.46, ORANGE_TINT, ORANGE, 1.8)
    add_text(slide, "WEIGHTED", 8.77, 2.26, 1.08, 0.22, 9.0, ORANGE, True, align=PP_ALIGN.CENTER)
    add_text(slide, "SUCCESSOR\nDRAW", 8.72, 2.57, 1.18, 0.46, 9.8, DARK, True, align=PP_ALIGN.CENTER)
    add_text(slide, "failed address excluded", 8.44, 3.54, 1.74, 0.22, 7.8, DARK, align=PP_ALIGN.CENTER)

    add_oval(slide, 10.74, 2.00, 1.46, 1.46, BLUE_TINT, BLUE, 1.8)
    add_text(slide, "TRAINING", 10.92, 2.27, 1.10, 0.22, 10.0, BLUE, True, align=PP_ALIGN.CENTER)
    add_text(slide, "ROUND r+1", 10.88, 2.63, 1.18, 0.27, 11.2, DARK, True, align=PP_ALIGN.CENTER)
    add_text(slide, "new aggregator", 10.85, 3.08, 1.24, 0.20, 8.0, DARK, align=PP_ALIGN.CENTER)

    add_text(slide, "PRESERVED MODEL STATE", 2.02, 4.42, 2.62, 0.24, 10.2, GREEN, True)
    add_line_segment(slide, 1.78, 5.03, 11.80, 5.03, GREEN, 4.0, arrow=True)
    add_oval(slide, 0.66, 4.56, 1.14, 1.14, GREEN_TINT, GREEN, 2.0)
    add_text(slide, "M(r−1)", 0.83, 4.88, 0.80, 0.24, 12.0, GREEN, True, align=PP_ALIGN.CENTER)
    add_text(slide, "M(r−1) remains authoritative throughout recovery", 2.02, 4.76, 3.86, 0.25, 9.2, DARK, True)
    add_text(slide, "×  M(r) was never finalized", 6.12, 4.64, 2.12, 0.24, 9.0, TU_RED, True, align=PP_ALIGN.CENTER)
    add_text(slide, "parent of round r+1", 10.38, 5.21, 1.76, 0.22, 8.4, GREEN, True, align=PP_ALIGN.CENTER)

    add_box(slide, 1.36, 5.68, 10.62, 0.43, fill=TU_RED, line=TU_RED, radius=False)
    add_text(
        slide,
        "No blockchain rewind: the failed attempt is abandoned and the previous finalized model is preserved.",
        1.64,
        5.77,
        10.06,
        0.23,
        11.5,
        WHITE,
        True,
        align=PP_ALIGN.CENTER,
        valign=MSO_ANCHOR.MIDDLE,
    )
    add_note(
        slide,
        "Recovery starts only after registered worker TEEs report the exact current round and aggregator. "
        "The first accepted report freezes the eligible non-aggregator reporter set and the required "
        "quorum; the default threshold is the ceiling of fifty percent. At quorum, the contract penalizes "
        "the failed aggregator, marks the attempt aborted, advances the raw round, and selects a replacement "
        "from the current authorized set while excluding the failed address. This is not a blockchain "
        "rollback: the last atomically finalized model remains authoritative. The quorum authenticates "
        "reports but does not objectively prove global unreachability.",
    )


def slide_close_compare_commit(prs):
    slide = new_content_slide(
        prs,
        13,
        "Freeze → Compare → Finalize",
        "One frozen submission set · one policy decision · one finalized round",
    )

    candidate_nodes = [
        (3.28, 1.94, "MEAN", 8.7),
        (3.28, 2.78, "MEDIAN", 8.3),
        (3.28, 3.62, "TRIMMED", 7.8),
        (3.28, 4.46, "MULTI-\nKRUM", 8.2),
    ]

    # Draw the fan-out/fan-in first so all native decision nodes remain in the foreground.
    for _, y, _, _ in candidate_nodes:
        add_bezier_arrow(slide, (2.31, 3.30), (2.70, y + 0.46), (3.16, y + 0.46), BLUE, 1.35, segments=10)
        add_bezier_arrow(slide, (4.28, y + 0.46), (4.74, y + 0.46), (5.13, 3.30), ORANGE, 1.35, segments=10)
    add_arrow(slide, 5.13, 3.30, 7.83, 3.30, TU_RED, 1.8)
    add_bezier_arrow(slide, (9.51, 2.76), (9.72, 2.59), (9.88, 2.59), GREEN, 1.5, segments=10)
    add_bezier_arrow(slide, (9.51, 3.85), (9.72, 4.01), (9.88, 4.01), ORANGE, 1.5, segments=10)
    add_bezier_arrow(slide, (11.26, 2.59), (11.45, 2.59), (11.57, 2.93), GREEN, 1.5, segments=10)
    add_bezier_arrow(slide, (11.26, 4.01), (11.45, 4.01), (11.57, 3.67), ORANGE, 1.5, segments=10)

    add_auto_shape(slide, MSO_AUTO_SHAPE_TYPE.FLOWCHART_DATA, 0.62, 2.55, 1.58, 1.50, BLUE_TINT, BLUE, 1.5)
    add_text(slide, "FREEZE", 0.86, 2.73, 1.10, 0.24, 13.0, BLUE, True, align=PP_ALIGN.CENTER)
    add_text(slide, "WORKER\nSUBMISSIONS", 0.78, 3.08, 1.27, 0.55, 11.5, DARK, True, align=PP_ALIGN.CENTER)
    add_text(slide, "ordered signed commitments\nroot rₙ · count n", 0.67, 4.20, 1.49, 0.45, 8.3, DARK, align=PP_ALIGN.CENTER)

    add_text(slide, "CANDIDATE FAN-OUT", 2.72, 1.72, 2.15, 0.20, 9.4, ORANGE, True, align=PP_ALIGN.CENTER)
    for x, y, label, size in candidate_nodes:
        add_oval(slide, x, y, 0.96, 0.96, ORANGE_TINT, ORANGE, 1.2)
        add_text(
            slide,
            label,
            x + 0.08,
            y + 0.28 if "\n" not in label else y + 0.20,
            0.80,
            0.40,
            size,
            ORANGE,
            True,
            align=PP_ALIGN.CENTER,
            valign=MSO_ANCHOR.MIDDLE,
            margin=0,
        )
    add_text(slide, "eligible variants · Multi-Krum requires ≥ 5 inputs", 2.24, 5.49, 3.02, 0.22, 8.2, DARK, align=PP_ALIGN.CENTER)

    add_text(slide, "COMPARE VALIDATION LOSS", 5.40, 2.82, 2.16, 0.22, 9.4, TU_RED, True, align=PP_ALIGN.CENTER)
    add_text(slide, "same signed · hash-pinned set", 5.40, 3.47, 2.16, 0.20, 8.1, DARK, align=PP_ALIGN.CENTER)

    add_auto_shape(slide, MSO_AUTO_SHAPE_TYPE.FLOWCHART_DECISION, 7.86, 2.39, 1.83, 1.83, ORANGE_TINT, ORANGE, 1.5)
    add_text(slide, "L(best) ≤", 8.18, 2.79, 1.19, 0.21, 10.0, ORANGE, True, align=PP_ALIGN.CENTER)
    add_text(slide, "1.05 × L(parent)?", 8.10, 3.08, 1.35, 0.38, 9.2, DARK, True, align=PP_ALIGN.CENTER)

    add_box(slide, 9.91, 2.25, 1.35, 0.68, fill=GREEN_TINT, line=GREEN, line_width=1.3)
    add_text(slide, "YES", 10.08, 2.34, 1.01, 0.17, 8.4, GREEN, True, align=PP_ALIGN.CENTER, margin=0)
    add_text(slide, "BEST CANDIDATE", 10.01, 2.57, 1.15, 0.18, 7.6, DARK, True, align=PP_ALIGN.CENTER, margin=0)

    add_box(slide, 9.91, 3.67, 1.35, 0.68, fill=ORANGE_TINT, line=ORANGE, line_width=1.3)
    add_text(slide, "NO", 10.08, 3.76, 1.01, 0.17, 8.4, ORANGE, True, align=PP_ALIGN.CENTER, margin=0)
    add_text(slide, "PARENT MODEL", 10.01, 3.99, 1.15, 0.18, 7.6, DARK, True, align=PP_ALIGN.CENTER, margin=0)

    add_box(slide, 11.58, 2.52, 1.20, 1.56, fill=LIGHT, line=TU_RED, line_width=1.5)
    add_text(slide, "FINALIZE", 11.69, 2.80, 0.98, 0.22, 10.0, TU_RED, True, align=PP_ALIGN.CENTER)
    add_text(slide, "ROUND", 11.69, 3.12, 0.98, 0.27, 13.0, DARK, True, align=PP_ALIGN.CENTER)
    add_text(
        slide,
        "record the chosen\nmodel + evidence",
        11.63,
        3.50,
        1.10,
        0.38,
        7.2,
        DARK,
        align=PP_ALIGN.CENTER,
    )

    add_note(
        slide,
        "This slide separates two decisions that are easy to conflate. The weighted draw selects which "
        "authorized worker may act as aggregator. Once the accepted update set is closed, Hybrid-R-style "
        "policy determines which aggregation result may be published. The ledger freezes the worker-submission "
        "set as an ordered root "
        "and explicit count; the measured aggregator must stage that same set. It computes every candidate "
        "eligible for the participant count: arithmetic mean, coordinate median, symmetric trimmed means, "
        "and Multi-Krum from five inputs onward. Candidates are evaluated on one separately signed and "
        "hash-pinned validation artifact. The best finite candidate is retained only when its loss is at "
        "most five percent above the parent loss; otherwise the unchanged parent is emitted. These are "
        "mutually exclusive outcomes: the round records either the selected candidate or the retained parent. "
        "One ledger transaction then binds the closed set, policy, evidence, output, encrypted publication references, "
        "publisher authority, and round transition. The end-to-end Phala run and the local 10, 50, and 100 "
        "participant runs used arithmetic mean. Hybrid-R-style behavior was component-tested and was not "
        "evaluated in a live poisoning campaign.",
    )


def slide_handoff(prs):
    slide = new_content_slide(
        prs,
        14,
        "The agent cannot choose the model",
        "Ledger = authority · IPFS = untrusted bytes · receiver = verification",
    )

    # Draw the three incoming paths before the foreground cards.
    add_arrow(slide, 6.67, 2.03, 6.67, 2.24, GREEN, 1.8)
    add_arrow(slide, 3.18, 3.58, 3.53, 3.58, TU_RED, 1.8)
    add_arrow(slide, 10.14, 3.58, 9.80, 3.58, PURPLE, 1.8)

    add_box(slide, 4.78, 1.44, 3.78, 0.59, fill=LIGHT, line=MID, radius=True, line_width=1.0)
    add_text(slide, "AGENT REQUEST", 5.05, 1.54, 1.31, 0.18, 8.6, DARK, True, align=PP_ALIGN.CENTER)
    add_text(slide, "PREPARE CURRENT MODEL", 6.27, 1.54, 2.02, 0.18, 8.6, DARK, True, align=PP_ALIGN.CENTER)
    add_text(slide, "no path · no CID · no round · no publisher", 5.08, 1.80, 3.18, 0.16, 7.5, TU_RED, True, align=PP_ALIGN.CENTER)

    add_box(slide, 0.62, 2.25, 2.56, 2.80, fill=RED_TINT, line=TU_RED, radius=True, line_width=1.6)
    add_text(slide, "LEDGER", 1.01, 2.52, 1.78, 0.30, 15.0, TU_RED, True, align=PP_ALIGN.CENTER)
    add_text(slide, "FINALIZED STATE", 0.95, 2.94, 1.90, 0.22, 9.0, DARK, True, align=PP_ALIGN.CENTER)
    add_text(
        slide,
        "round + publisher\nkey snapshot\nmodel CID\nsignature CID\nkey-bundle CID",
        0.92,
        3.37,
        1.96,
        1.10,
        9.1,
        DARK,
        align=PP_ALIGN.CENTER,
    )
    add_text(slide, "defines what is current", 0.92, 4.68, 1.96, 0.20, 8.0, TU_RED, True, align=PP_ALIGN.CENTER)

    add_box(slide, 3.54, 2.18, 6.26, 3.05, fill=GREEN_TINT, line=GREEN, radius=True, line_width=1.8)
    add_text(slide, "MEASURED RECEIVER", 4.72, 2.46, 3.90, 0.31, 15.0, GREEN, True, align=PP_ALIGN.CENTER)
    receiver_steps = [
        (3.88, "1  RESOLVE", "latest finalized\nledger tuple"),
        (5.74, "2  RETRIEVE", "named CIDs\nunwrap + decrypt"),
        (7.60, "3  VERIFY", "hashes · round\npublisher · key snapshot"),
    ]
    for x, heading, body in receiver_steps:
        add_box(slide, x, 2.96, 1.66, 1.18, fill=WHITE, line=GREEN, line_width=1.0)
        add_text(slide, heading, x + 0.10, 3.11, 1.46, 0.20, 9.2, GREEN, True, align=PP_ALIGN.CENTER)
        add_text(slide, body, x + 0.10, 3.49, 1.46, 0.40, 8.8, DARK, align=PP_ALIGN.CENTER)
    add_box(slide, 3.88, 4.47, 5.38, 0.47, fill=GREEN, line=GREEN, radius=False)
    add_text(slide, "INSTALL THE EXACT MODEL—OR REJECT", 4.16, 4.59, 4.82, 0.20, 10.7, WHITE, True, align=PP_ALIGN.CENTER)

    add_box(slide, 10.14, 2.25, 2.56, 2.80, fill=PURPLE_TINT, line=PURPLE, radius=True, line_width=1.6)
    add_text(slide, "IPFS", 10.54, 2.52, 1.76, 0.30, 15.0, PURPLE, True, align=PP_ALIGN.CENTER)
    add_text(slide, "UNTRUSTED STORAGE", 10.37, 2.94, 2.10, 0.22, 9.0, DARK, True, align=PP_ALIGN.CENTER)
    add_text(
        slide,
        "encrypted model\npublisher signature\nrecipient key envelope",
        10.44,
        3.44,
        1.96,
        0.72,
        9.2,
        DARK,
        align=PP_ALIGN.CENTER,
    )
    add_text(slide, "may be stale, unavailable, or hostile", 10.36, 4.58, 2.12, 0.38, 7.8, PURPLE, True, align=PP_ALIGN.CENTER)

    add_box(slide, 0.96, 5.53, 11.42, 0.53, fill=TU_RED, line=TU_RED, radius=False)
    add_text(
        slide,
        "Reject local paths, stale CIDs, alternative publishers, and hash mismatches.",
        1.24,
        5.67,
        10.86,
        0.24,
        12.0,
        WHITE,
        True,
        align=PP_ALIGN.CENTER,
        valign=MSO_ANCHOR.MIDDLE,
    )
    add_note(
        slide,
        "The agent triggers preparation but never chooses the model. It sends no local path, CID, round, "
        "or publisher identity. The measured receiver first resolves the latest finalized publication from "
        "the ledger, including the current round, publisher and key snapshot, and the model, signature, and "
        "recipient-key-bundle CIDs. IPFS is only untrusted storage for the referenced bytes; it is not an "
        "authority. The receiver fetches exactly those objects, unwraps Worker 0's recipient key, decrypts "
        "the model, and verifies content hashes, round, publisher signature, and key snapshot. Inference "
        "proceeds only when ledger identity, retrieved bytes, and publisher proof agree. A local path, stale "
        "CID, alternative publisher, or mismatching object is rejected.",
    )


def slide_sello_protocol(prs):
    slide = new_content_slide(
        prs,
        15,
        "Sello: evidence from the receiving service",
        "Figuera proposal (2026) · receiver-created · owner-encrypted · transparency-recorded",
    )

    add_rich_text(
        slide,
        [
            ("CORE IDEA   ", TU_RED, True, 11.0),
            ("The service that performs the action creates the evidence—not the agent.", DARK, True, 13.0),
        ],
        0.78,
        1.61,
        11.78,
        0.30,
        align=PP_ALIGN.CENTER,
        valign=MSO_ANCHOR.MIDDLE,
    )

    stages = [
        (
            0.72,
            "1  AUTHORIZED REQUEST",
            "The agent presents the owner's permission for one action.",
            BLUE_TINT,
            BLUE,
        ),
        (
            4.82,
            "2  RECEIVING SERVICE",
            "The service executes the action and signs an encrypted receipt.",
            GREEN_TINT,
            GREEN,
        ),
        (
            8.92,
            "3  TRANSPARENCY LOG",
            "The log records the receipt and returns inclusion evidence.",
            PURPLE_TINT,
            PURPLE,
        ),
    ]
    for x, heading, body, fill, accent in stages:
        add_box(slide, x, 2.35, 3.15, 1.58, fill=fill, line=accent, line_width=1.4)
        add_text(
            slide,
            heading,
            x + 0.18,
            2.62,
            2.79,
            0.27,
            11.5,
            accent,
            True,
            align=PP_ALIGN.CENTER,
        )
        add_text(
            slide,
            body,
            x + 0.30,
            3.10,
            2.55,
            0.48,
            10.2,
            DARK,
            align=PP_ALIGN.CENTER,
            valign=MSO_ANCHOR.MIDDLE,
        )

    add_arrow(slide, 3.89, 3.14, 4.76, 3.14, BLUE, 1.7)
    add_arrow(slide, 7.99, 3.14, 8.86, 3.14, GREEN, 1.7)

    add_box(slide, 1.18, 4.34, 10.97, 0.76, fill=LIGHT, line=TU_RED, line_width=1.2)
    add_text(slide, "OWNER VERIFIES LATER", 1.48, 4.56, 2.47, 0.24, 11.0, TU_RED, True)
    add_text(
        slide,
        "Check log inclusion + service signature  →  decrypt the receipt",
        4.06,
        4.54,
        7.70,
        0.27,
        11.0,
        DARK,
        True,
        align=PP_ALIGN.CENTER,
        valign=MSO_ANCHOR.MIDDLE,
    )

    add_box(slide, 1.18, 5.35, 10.97, 0.50, fill=TU_RED, line=TU_RED, radius=False)
    add_text(
        slide,
        "VITA-FL adopts the receiver-first pattern: publish the receipt before returning success.",
        1.45,
        5.48,
        10.43,
        0.23,
        11.2,
        WHITE,
        True,
        align=PP_ALIGN.CENTER,
    )
    add_text(slide, "Source: J. Figuera, Notarized Agents, arXiv:2606.04193 (2026).", 0.80, 6.02, 11.72, 0.18, 8.2, DARK, align=PP_ALIGN.CENTER)
    add_note(
        slide,
        "Figuera's Sello proposal starts from a trust-boundary problem: a compromised agent or operator "
        "cannot be the sole source of truth about its own actions. The agent presents a signed JWS "
        "authorization token that binds the owner's HPKE public key and permitted log policy. The called "
        "service verifies that token, performs or denies the action, and hashes the exact input and output. "
        "It encrypts the receipt body to the owner with HPKE, signs the encrypted envelope with its own "
        "Ed25519 key in COSE_Sign1, and submits it to a witness-cosigned Merkle transparency log. The owner "
        "later discovers entries by the token-derived reference, verifies inclusion and the service key, and "
        "decrypts locally. VITA-FL selectively adopts the receiver-first pattern and additionally fails "
        "closed unless the receiver publishes its receipt before returning a successful tool result. It does "
        "not implement Sello's owner-discovery and witness-cosigned-log architecture: the evaluation used "
        "single-node CCF Virtual Mode without an independent witness, gossip, or a durable deployment. Sello "
        "does not prove that a call was never made and does not prevent collusion by a receiving service. "
        "Source: Juan Figuera, "
        "Notarized Agents: Receiver-Attested Confidential Receipts for AI Agent Actions, arXiv:2606.04193, 2026.",
    )


def slide_agent(prs):
    slide = new_content_slide(prs, 16, "Block 2: agent-mediated attested inference", "Three bounded MCP operations, four log records")
    actors = [
        (1.55, "AGENT SERVICE", BLUE),
        (6.25, "INFERENCE TEE", GREEN),
        (10.78, "TRANSPARENCY LOG", PURPLE),
    ]
    for x, label, accent in actors:
        width = 2.15 if x < 10 else 2.25
        add_box(slide, x - width / 2, 1.47, width, 0.55, fill=WHITE, line=accent)
        add_text(slide, label, x - width / 2 + 0.06, 1.64, width - 0.12, 0.22, 11.5, accent, True, align=PP_ALIGN.CENTER)
        lifeline = slide.shapes.add_connector(
            MSO_CONNECTOR.STRAIGHT, Inches(x), Inches(2.04), Inches(x), Inches(5.06)
        )
        lifeline.line.color.rgb = rgb(MID)
        lifeline.line.width = Pt(1.0)
        lifeline.line.dash_style = MSO_LINE_DASH_STYLE.DASH
    operations = [
        (2.35, "1  TEE BUNDLE FETCH", "Resolve and verify the current model bundle", BLUE),
        (3.15, "2  TEE IMAGE PICK", "Create receiver-owned image state", GREEN),
        (3.95, "3  TEE INFERENCE", "Run native inference and emit AIR/TDX evidence", ORANGE),
    ]
    for y, heading, body, accent in operations:
        add_arrow(slide, 1.67, y, 6.12, y, accent, 1.7)
        add_text(slide, heading, 1.78, y - 0.35, 2.25, 0.24, 11.2, accent, True)
        add_text(slide, body, 4.08, y - 0.35, 1.90, 0.28, 9.4, DARK, True, align=PP_ALIGN.RIGHT)
        add_arrow(slide, 6.38, y + 0.25, 10.65, y + 0.25, PURPLE, 1.6)
        add_text(
            slide,
            "Publish receiver receipt before output",
            7.06,
            y + 0.04,
            2.98,
            0.20,
            9.5,
            PURPLE,
            True,
            align=PP_ALIGN.CENTER,
        )
    add_arrow(slide, 1.67, 4.70, 10.65, 4.70, TU_RED, 1.9)
    add_text(
        slide,
        "The agent service validates and publishes the complete inference bundle",
        3.05,
        4.25,
        6.24,
        0.38,
        10.8,
        TU_RED,
        True,
        align=PP_ALIGN.CENTER,
    )
    add_box(slide, 0.87, 5.25, 11.54, 0.60, fill=LIGHT, line=TU_RED, radius=False)
    add_rich_text(
        slide,
        [
            ("3 × receiver-signed tool receipts", PURPLE, True, 15),
            ("   +   ", DARK, False, 16),
            ("1 × complete inference bundle", BLUE, True, 15),
            ("   = 4 log records", GREEN, True, 15),
        ],
        1.08,
        5.43,
        11.12,
        0.27,
        align=PP_ALIGN.CENTER,
        valign=MSO_ANCHOR.MIDDLE,
    )
    add_note(
        slide,
        "The language-model agent can invoke only three bounded TEE operations. For each successful "
        "call, the deterministic inference receiver signs the exact input and output and publishes the "
        "receipt before returning the result. After inference, deterministic code in the agent service "
        "validates the complete AIR and TDX evidence bundle and publishes that bundle separately. The "
        "transparency log records inclusion and order; it does not itself decide whether the inference "
        "or attestation evidence is semantically valid.",
    )


def slide_external_audit(prs):
    slide = new_content_slide(
        prs,
        17,
        "Independent audit: verify the evidence—not the UI",
        "Recorded? → authentic? → acceptable under policy?",
    )

    add_arrow(slide, 0.86, 5.14, 0.86, 1.93, TU_RED, 2.0)
    depth = add_text(slide, "AUDIT DEPTH", 0.23, 2.65, 0.34, 1.78, 9.0, TU_RED, True, align=PP_ALIGN.CENTER)
    depth.rotation = 270

    layers = [
        (
            1.55,
            4.38,
            10.28,
            0.82,
            "LOG PROOF",
            "Was this exact signed statement recorded?",
            "PUBLIC",
            PURPLE_TINT,
            PURPLE,
        ),
        (
            1.55,
            3.18,
            10.28,
            0.82,
            "RECEIPT AUTHENTICITY",
            "Did the receiver sign this request and response?",
            "OWNER DATA",
            BLUE_TINT,
            BLUE,
        ),
        (
            1.55,
            1.96,
            10.28,
            0.82,
            "INFERENCE APPRAISAL",
            "Does the attested workload satisfy trusted policy?",
            "POLICY",
            GREEN_TINT,
            GREEN,
        ),
    ]
    for x, y, w, h, heading, detail, scope, fill, accent in layers:
        add_box(slide, x, y, w, h, fill=fill, line=accent, line_width=1.3)
        add_text(slide, heading, x + 0.30, y + 0.22, 2.70, 0.26, 11.2, accent, True, valign=MSO_ANCHOR.MIDDLE)
        add_text(
            slide,
            detail,
            x + 3.00,
            y + 0.17,
            w - 4.58,
            h - 0.27,
            10.0,
            DARK,
            True,
            align=PP_ALIGN.CENTER,
            valign=MSO_ANCHOR.MIDDLE,
        )
        add_box(slide, x + w - 1.48, y + 0.22, 1.18, 0.34, fill=accent, line=accent, radius=False)
        add_text(
            slide,
            scope,
            x + w - 1.40,
            y + 0.30,
            1.02,
            0.17,
            7.7,
            WHITE,
            True,
            align=PP_ALIGN.CENTER,
            valign=MSO_ANCHOR.MIDDLE,
            margin=0,
        )

    add_box(slide, 1.55, 5.48, 10.28, 0.42, fill=LIGHT, line=BORDER, radius=False)
    add_text(
        slide,
        "AUDITOR NEEDS   exported statements · pinned historical keys · appraisal policy",
        1.79,
        5.59,
        9.80,
        0.20,
        9.3,
        DARK,
        True,
        align=PP_ALIGN.CENTER,
    )
    add_note(
        slide,
        "An independent audit requires exported artifacts rather than only a transaction identifier or "
        "browser view. First, the auditor verifies the CCF receipt and Merkle inclusion path against a "
        "historical SCITT service key archived outside the log, recovering the exact signed statement and "
        "its log position. Second, anyone with the pinned receiver key can verify the signature over the "
        "encrypted Sello-style envelope, but its confidential action, status, and input/output hashes remain "
        "owner-scoped. Full content verification requires the original authorization JWS, issuer key, owner "
        "HPKE private key, and exact request and response. Third, the separate inference-evidence record "
        "contains the request, response, AIR-inspired receipt, quote, event log, measured Compose, model "
        "manifest, and REPORTDATA. The auditor can recheck signatures and hashes, reconstruct REPORTDATA, "
        "and replay RTMR3, but must supply a trusted policy snapshot. A full retrospective DCAP appraisal "
        "also needs the quote-time certificate chain, revocation material, QE identity, TCB information, and "
        "appraisal policy. The evaluated log was a single-node CCF Virtual-Mode service, so durable independent "
        "auditing additionally depends on exporting statements and pinning the contemporaneous service key.",
    )


def slide_cryptographic_chain(prs):
    slide = new_content_slide(
        prs,
        18,
        "Cryptographic chain of custody",
        "Who produced it · who may read it · which exact bytes are bound",
    )
    nodes = [
        (0.55, "01  MEDICAL INPUT", "SIGN", "Device + radiologist\nRSA-2048 / SHA-256", GREEN_TINT, GREEN),
        (3.10, "02  PARTICIPANT TEE", "BIND\n+ SEAL", "secp256k1 action key · RSA-3072 custody\nREPORTDATA + RTMR3", BLUE_TINT, BLUE),
        (5.65, "03  WORKER UPDATE", "ENCRYPT\n+ SIGN", "AES-CBC · RSA-OAEP\npackage signature · EIP-712", ORANGE_TINT, ORANGE),
        (8.20, "04  GLOBAL MODEL", "WRAP\n+ FINALIZE", "AES-GCM · per-recipient OAEP\naggregator signature · IPFS CID", PURPLE_TINT, PURPLE),
        (10.75, "05  INFERENCE + LOG", "VERIFY\n+ RECORD", "AIR/TDX · HPKE receipt\nES256 statement · CCF receipt", RED_TINT, TU_RED),
    ]
    for index in range(4):
        start_x = nodes[index][0] + 1.71
        end_x = nodes[index + 1][0] - 0.08
        add_arrow(slide, start_x, 3.12, end_x, 3.12, MID, 1.7)

    for x, heading, action, detail, fill, accent in nodes:
        add_text(slide, heading, x - 0.20, 1.65, 2.05, 0.34, 10.0, accent, True, align=PP_ALIGN.CENTER)
        add_oval(slide, x, 2.30, 1.65, 1.65, fill, accent, 1.7)
        add_text(
            slide,
            action,
            x + 0.19,
            2.69 if "\n" in action else 2.82,
            1.27,
            0.62,
            13.0 if "\n" not in action else 11.4,
            accent,
            True,
            align=PP_ALIGN.CENTER,
            valign=MSO_ANCHOR.MIDDLE,
            margin=0,
        )
        add_text(slide, detail, x - 0.23, 4.25, 2.11, 0.66, 8.5, DARK, True, align=PP_ALIGN.CENTER)

    add_rich_text(
        slide,
        [
            ("Each transition preserves exact-byte binding; ", TU_RED, True, 9.6),
            ("confidentiality and authorization change with the object and recipient.", DARK, True, 9.6),
        ],
        1.08,
        5.24,
        11.18,
        0.24,
        align=PP_ALIGN.CENTER,
        valign=MSO_ANCHOR.MIDDLE,
    )
    add_box(slide, 0.98, 5.72, 11.38, 0.38, fill=LIGHT, line=BORDER, radius=False)
    add_text(
        slide,
        "TLS protects transport hops; application signatures, recipient encryption, and ledger/log bindings survive intermediary storage.",
        1.18,
        5.82,
        10.98,
        0.19,
        10.2,
        DARK,
        True,
        align=PP_ALIGN.CENTER,
        valign=MSO_ANCHOR.MIDDLE,
    )
    add_note(
        slide,
        "The chain begins with independent device and radiologist RSA signatures. Inside an admitted "
        "participant TEE, an application-bound secp256k1 action key authorizes protocol mutations and a "
        "random RSA-3072 participant key is sealed with dstack-derived material. Worker updates are "
        "encrypted for the current aggregator and signed over their round context. The global model is "
        "signed, encrypted with AES-GCM, and wrapped separately for every authorized recipient before "
        "IPFS publication and atomic ledger finalization. The native inference receiver inside the Worker "
        "0 TEE verifies that tuple and emits AIR and receiver receipts; the agent verifies them before the "
        "full bundle is recorded in the transparency log. CBC confidentiality on worker updates relies on "
        "the surrounding signature and hash bindings for integrity.",
    )


def slide_evaluation(prs):
    slide = new_content_slide(prs, 19, "Evaluation: what was actually tested?", "Three evidence levels—not one blanket success claim")
    column_x = [2.52, 4.46, 6.40, 8.34, 10.28]
    headers = ["ADMISSION", "ROUND PATH", "PARTICIPANTS", "AGGREGATION", "RECEIPTS / RECOVERY"]
    for x, heading in zip(column_x, headers):
        add_text(slide, heading, x, 1.56, 1.78, 0.34, 8.4, DARK, True, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)
    add_divider(slide, 0.58, 1.98, 11.88, TU_RED, 0.020)

    rows = [
        (
            2.14,
            "LIVE",
            "PHALA INTEGRATION",
            ["fresh\nquotes", "5 observed\nrounds", "3 TEE\nworkers", "Arithmetic\nMean", "all 3\nMCP ops"],
            BLUE_TINT,
            BLUE,
        ),
        (
            3.26,
            "SIMULATED",
            "LOCAL DOCKER",
            ["recorded quote\nreplay", "50\nrounds", "10 · 50 · 100\nlogical", "Arithmetic\nMean", "not part of\nscale run"],
            GREEN_TINT,
            GREEN,
        ),
        (
            4.38,
            "AUTOMATED",
            "FAIL-CLOSED TESTS",
            ["reject\nmismatch", "timeout +\nrecovery", "deterministic\nfixtures", "Hybrid-R\ncomponents", "verify +\nrecover"],
            ORANGE_TINT,
            ORANGE,
        ),
    ]
    for y, status, label, values, fill, accent in rows:
        add_box(slide, 0.58, y, 11.88, 0.91, fill=fill, line=BORDER, radius=False, line_width=0.7)
        add_box(slide, 0.58, y, 1.70, 0.91, fill=accent, line=accent, radius=False)
        add_text(slide, status, 0.72, y + 0.16, 1.42, 0.20, 9.3, WHITE, True, align=PP_ALIGN.CENTER)
        add_text(slide, label, 0.70, y + 0.48, 1.46, 0.22, 7.7, WHITE, True, align=PP_ALIGN.CENTER)
        for index, (x, value) in enumerate(zip(column_x, values)):
            if index:
                add_divider(slide, x - 0.15, y + 0.10, 0.012, BORDER, 0.70)
            add_text(
                slide,
                value,
                x,
                y + 0.20,
                1.78,
                0.50,
                10.3,
                accent if value != "not part of\nscale run" else MID,
                True,
                align=PP_ALIGN.CENTER,
                valign=MSO_ANCHOR.MIDDLE,
            )
    add_text(
        slide,
        "Evidence boundary: protocol observation—not fresh per-worker admission at scale, independent failure domains, or Phala/CVM scalability.",
        1.0,
        5.55,
        11.32,
        0.20,
        9.4,
        TU_RED,
        True,
        align=PP_ALIGN.CENTER,
    )
    add_text(
        slide,
        "Data evidence: DICOM-inspired synthetic byte streams with experimental self-signed identities—not native clinical DICOM.",
        1.0,
        5.89,
        11.32,
        0.18,
        8.8,
        DARK,
        True,
        align=PP_ALIGN.CENTER,
    )
    add_note(
        slide,
        "The evaluation distinguishes live integration, local participant-scale simulation, and automated "
        "negative tests. The Phala run used three separately admitted worker confidential VMs with fresh "
        "TDX/DCAP quotes, exercised arithmetic-mean training for five observed rounds, all three MCP "
        "operations, and attested inference. The 10, 50, and 100 participant experiments instead ran on a "
        "single local Docker host and replayed one recorded TEE quote; they reached round 50 but do not "
        "evaluate fresh per-worker admission, independent failure domains, a distributed network, or Phala "
        "confidential-VM scalability. Hybrid-R-style candidates and the five-percent parent gate were "
        "component-tested with limited deterministic fixtures, not in a live poisoning campaign. Signed "
        "input provenance used DICOM-inspired synthetic byte streams and experimental self-signed identities, "
        "not native clinical DICOM objects.",
    )


def slide_learning_trajectories(prs):
    slide = new_content_slide(
        prs,
        20,
        "Observed optimization trajectories overlap across scale",
        "Single-host Docker · recorded quote replay · one run per logical participant count",
    )
    runs = load_evaluation_runs()
    add_metric_chart(
        slide,
        0.55,
        1.50,
        6.05,
        3.85,
        "Binary cross-entropy loss",
        runs,
        "loss",
        0.17,
        0.65,
        [(0.20, "0.20"), (0.30, "0.30"), (0.40, "0.40"), (0.50, "0.50"), (0.60, "0.60")],
        descriptor="Lower is better · ideal 0 · here: imbalance-driven decline",
    )
    add_metric_chart(
        slide,
        6.73,
        1.50,
        6.05,
        3.85,
        "Exact match (%)",
        runs,
        "exact_match",
        0.0,
        56.0,
        [(0, "0"), (10, "10"), (20, "20"), (30, "30"), (40, "40"), (50, "50")],
        descriptor="All 14 labels correct · ideal 100% · 53% ≈ all-negative baseline",
    )
    findings = [
        ("LOSS ↓", "0.62 → 0.19; negative-label fit", BLUE_TINT, BLUE),
        ("EXACT ↑", "53.16% ≈ 53.17% all-negative baseline", GREEN_TINT, GREEN),
        ("JOINT VIEW", "Optimization ≠ useful learning", LIGHT, DARK),
    ]
    for index, (heading, body, fill, accent) in enumerate(findings):
        x = 0.65 + index * 4.15
        add_box(slide, x, 5.55, 3.88, 0.52, fill=fill, line=accent)
        add_text(slide, heading, x + 0.14, 5.66, 1.12, 0.20, 8.8, accent, True)
        add_text(
            slide,
            body,
            x + 1.18,
            5.64,
            2.52,
            0.24,
            9.2,
            DARK,
            True,
            align=PP_ALIGN.CENTER,
            valign=MSO_ANCHOR.MIDDLE,
        )
    add_note(
        slide,
        "The three completed ChestMNIST runs each expose forty-nine learned global models from rounds "
        "two through fifty; round one is the bootstrap state. Binary cross-entropy is the mean "
        "probabilistic error across the fourteen independent labels; lower is better and zero is the "
        "theoretical optimum. Exact match counts a sample only when its complete fourteen-label vector "
        "is correct; higher is better and one hundred percent is the optimum. Loss falls from "
        "approximately 0.62 to 0.188 and exact match rises to approximately fifty-three percent. However, "
        "53.1717 percent of the 22,433 test samples have a completely negative fourteen-label vector, so the "
        "53.11 to 53.16 percent endpoint is effectively the all-negative baseline. The unweighted binary "
        "cross-entropy objective makes this majority-negative shortcut attractive: falling loss confirms "
        "optimization of the recorded objective, not useful positive-finding discrimination. The trajectories for ten, "
        "fifty, and one hundred participants almost overlap. This is an observed single run per scale, "
        "so it validates repeatable local protocol simulation but is not evidence of distributed scale, "
        "confidential-VM scalability, or statistical scale invariance.",
    )


def slide_learning_quality(prs):
    slide = new_content_slide(
        prs,
        21,
        "Optimization does not imply useful discrimination",
        "AUROC remains near chance while both F1 scores collapse",
    )
    runs = load_evaluation_runs()
    add_metric_chart(
        slide,
        0.42,
        1.50,
        4.08,
        3.86,
        "Macro AUROC",
        runs,
        "macro_auroc",
        0.485,
        0.515,
        [(0.49, "0.49"), (0.50, "0.50"), (0.51, "0.51")],
        reference=0.50,
        descriptor="Ranking quality · ideal 1 · ≈0.5 = chance-level discrimination",
    )
    add_metric_chart(
        slide,
        4.63,
        1.50,
        4.08,
        3.86,
        "Micro F1",
        runs,
        "micro_f1",
        0.0,
        0.11,
        [(0.00, "0.00"), (0.05, "0.05"), (0.10, "0.10")],
        descriptor="Overall positive detection · ideal 1 · ≈0 = positives missed",
    )
    add_metric_chart(
        slide,
        8.84,
        1.50,
        4.08,
        3.86,
        "Macro F1",
        runs,
        "macro_f1",
        0.0,
        0.11,
        [(0.00, "0.00"), (0.05, "0.05"), (0.10, "0.10")],
        descriptor="Equal-weight label detection · ideal 1 · ≈0 = broad failure",
    )
    interpretations = [
        (0.50, 3.92, "AUROC ≈ 0.50", "Little ranking signal", BLUE_TINT, BLUE),
        (4.71, 3.92, "MICRO F1 ≈ 0", "Positive findings are missed", ORANGE_TINT, ORANGE),
        (8.92, 3.92, "MACRO F1 ≈ 0", "Failure spans the labels", PURPLE_TINT, PURPLE),
    ]
    for x, width, heading, body, fill, accent in interpretations:
        add_box(slide, x, 5.55, width, 0.56, fill=fill, line=accent)
        add_text(slide, heading, x + 0.12, 5.63, width - 0.24, 0.17, 9.2, accent, True, align=PP_ALIGN.CENTER)
        add_text(slide, body, x + 0.12, 5.84, width - 0.24, 0.16, 8.8, DARK, True, align=PP_ALIGN.CENTER)
    add_note(
        slide,
        "Macro AUROC measures per-label ranking quality and then gives every label equal weight; one is "
        "ideal and 0.5 is chance-level ranking. Micro F1 pools all positive-label decisions, so frequent "
        "labels have more influence. Macro F1 first evaluates each label and then averages them equally, "
        "making rare-label failure more visible. Both F1 scores have an optimum of one at the fixed 0.5 "
        "decision threshold. An F1 value near zero alone could be caused by class imbalance or a poorly "
        "calibrated threshold. Here, however, macro AUROC is also near its threshold-independent chance "
        "level, which supplies additional evidence that the scores contain little useful ranking signal. "
        "Across the recorded runs, the best macro AUROC is 0.508392 for one hundred "
        "participants at round fifty. The largest micro and macro F1 values, 0.104170 and 0.078440, both "
        "occur for one hundred participants at round two before the trajectories collapse. The optimization "
        "curves must not be read as clinical success. At round fifty, macro AUROC is "
        "approximately 0.504, 0.507, and 0.508 for ten, fifty, and one hundred participants. Micro F1 "
        "falls to about 0.0001 and macro F1 to about 0.0005 to 0.001. Loss reduction and rising exact "
        "match are therefore explained by a majority-negative shortcut favored by severe class imbalance "
        "and the unweighted binary cross-entropy objective. The dataset makes this failure mode plausible, "
        "but the result still means that these runs did not learn a useful multilabel classifier. "
        "These local runs validate protocol execution at the simulated logical participant counts, not "
        "distributed-system scalability or diagnostic utility.",
    )


def slide_results(prs):
    slide = new_content_slide(prs, 22, "Results: demonstrated chain and explicit limits", "System integration is not a clinical claim")
    add_text(slide, "DEMONSTRATED PROCESS EVIDENCE", 0.74, 1.51, 5.42, 0.31, 13.5, GREEN, True)
    add_text(slide, "CLINICAL CLAIM BOUNDARY", 7.15, 1.51, 5.43, 0.31, 13.5, ORANGE, True, align=PP_ALIGN.CENTER)
    add_divider(slide, 6.61, 1.48, 0.024, TU_RED, 3.92)
    add_text(slide, "≠", 6.27, 3.04, 0.70, 0.58, 29, TU_RED, True, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)

    add_line_segment(slide, 1.49, 2.24, 1.49, 4.88, GREEN, 2.4)
    evidence = [
        (2.02, "3 + 1", "transparency records", "three tool receipts + one complete inference bundle", PURPLE),
        (3.19, "78,468", "signed training samples", "DICOM-inspired fixture tampering rejected", GREEN),
        (4.36, "10 / 50 / 100", "logical participants", "local Docker simulations reached round 50", BLUE),
    ]
    for y, value, label, detail, accent in evidence:
        add_oval(slide, 0.91, y, 1.16, 1.16, WHITE, accent, 2.2)
        add_text(
            slide,
            value,
            1.00,
            y + 0.37,
            0.98,
            0.30,
            12.5 if value != "10 / 50 / 100" else 8.8,
            accent,
            True,
            align=PP_ALIGN.CENTER,
            valign=MSO_ANCHOR.MIDDLE,
            margin=0,
        )
        add_text(slide, label, 2.34, y + 0.15, 2.50, 0.26, 12.5, DARK, True)
        add_text(slide, detail, 2.34, y + 0.51, 3.60, 0.34, 9.4, DARK)

    add_oval(slide, 8.59, 2.00, 2.28, 2.28, ORANGE_TINT, ORANGE, 2.4)
    add_oval(slide, 8.82, 2.23, 1.82, 1.82, WHITE, WHITE, 0.5)
    add_text(slide, "≈ 0.50", 8.99, 2.80, 1.48, 0.40, 23, ORANGE, True, align=PP_ALIGN.CENTER)
    add_text(slide, "macro AUROC", 9.05, 3.28, 1.36, 0.25, 10.3, DARK, True, align=PP_ALIGN.CENTER)
    add_arrow(slide, 11.39, 2.21, 11.39, 4.16, ORANGE, 2.2)
    add_text(slide, "F1", 11.05, 2.43, 0.68, 0.28, 16, ORANGE, True, align=PP_ALIGN.CENTER)
    add_text(slide, "→ 0", 10.96, 3.65, 0.86, 0.34, 18, DARK, True, align=PP_ALIGN.CENTER)
    add_text(slide, "NOT DEMONSTRATED", 7.45, 4.53, 2.34, 0.25, 10.0, ORANGE, True)
    add_text(slide, "Clinical validity · diagnostic utility", 7.45, 4.88, 4.86, 0.30, 13.0, DARK, True)
    add_box(slide, 1.12, 5.57, 11.10, 0.50, fill=TU_RED, line=TU_RED, radius=False)
    add_text(
        slide,
        "The evidence chain supports the process claim—not the medical correctness of the model.",
        1.32,
        5.71,
        10.70,
        0.25,
        14,
        WHITE,
        True,
        align=PP_ALIGN.CENTER,
    )
    add_note(
        slide,
        "The complete inference path produced three receiver-signed tool receipts and one complete "
        "evidence-bundle record. The provenance evaluation accepted all 78,468 prepared training samples "
        "and rejected targeted changes to pixels, labels, and signer policy in DICOM-inspired synthetic "
        "fixtures. The single-host Docker simulations for 10, 50, and 100 logical participants replayed "
        "one recorded quote and reached round 50. However, macro AUROC remained close to 0.50 and the F1 scores "
        "approached zero. These results demonstrate protocol execution and evidence binding, not useful "
        "diagnostic performance.",
    )


def slide_conclusion(prs):
    slide = new_content_slide(
        prs,
        23,
        "Conclusion and outlook",
        "Composed evidence works · next: strengthen source-to-deployment trust",
    )
    add_text(slide, "CORE CONCLUSION", 0.78, 1.48, 2.10, 0.24, 10.3, TU_RED, True)
    add_text(
        slide,
        "VITA-FL composes scoped evidence from decentralized model production\nto agent consumption.",
        0.78,
        1.76,
        11.80,
        0.78,
        19.5,
        DARK,
        True,
        align=PP_ALIGN.CENTER,
        valign=MSO_ANCHOR.MIDDLE,
    )
    add_text(
        slide,
        "Reproducible proof of concept—not a trustless or clinically validated platform.",
        1.32,
        2.55,
        10.72,
        0.28,
        11.2,
        TU_RED,
        True,
        align=PP_ALIGN.CENTER,
    )

    add_text(slide, "DEMONSTRATED", 0.86, 2.91, 2.12, 0.24, 10.5, GREEN, True)
    add_text(slide, "NEXT", 8.10, 2.91, 1.22, 0.24, 10.5, ORANGE, True)
    add_line_segment(slide, 1.22, 3.63, 6.05, 3.63, GREEN, 3.0)
    add_line_segment(slide, 7.27, 3.63, 12.05, 3.63, ORANGE, 3.0, arrow=True)

    left_milestones = [
        (1.45, "SIGNED INPUT", "independent provenance"),
        (3.25, "DFL MODEL", "selection + atomic handoff"),
        (5.05, "ATTESTED USE", "TDX/AIR + receipts + SCITT"),
    ]
    right_milestones = [
        (8.18, "SUPPLY CHAIN", "source→build · SBOM · signatures"),
        (10.00, "INDEPENDENT LOGS", "witness · gossip · anchoring"),
        (11.82, "ASSURANCE AT SCALE", "poisoning · native DICOM · repeated runs"),
    ]
    for x, heading, detail in left_milestones:
        add_oval(slide, x - 0.34, 3.29, 0.68, 0.68, WHITE, GREEN, 2.2)
        add_text(slide, "✓", x - 0.22, 3.44, 0.44, 0.30, 16, GREEN, True, align=PP_ALIGN.CENTER, margin=0)
        add_text(slide, heading, x - 0.70, 4.20, 1.40, 0.25, 9.2, GREEN, True, align=PP_ALIGN.CENTER)
        add_text(slide, detail, x - 0.72, 4.53, 1.44, 0.48, 8.0, DARK, align=PP_ALIGN.CENTER)

    add_oval(slide, 6.03, 3.00, 1.25, 1.25, RED_TINT, TU_RED, 1.8)
    add_text(slide, "VITA-FL", 6.18, 3.34, 0.95, 0.22, 10.2, TU_RED, True, align=PP_ALIGN.CENTER)
    add_text(slide, "PoC", 6.29, 3.63, 0.73, 0.20, 9.0, DARK, True, align=PP_ALIGN.CENTER)

    for x, heading, detail in right_milestones:
        add_oval(slide, x - 0.34, 3.29, 0.68, 0.68, WHITE, ORANGE, 2.2)
        add_text(slide, "→", x - 0.22, 3.44, 0.44, 0.30, 15, ORANGE, True, align=PP_ALIGN.CENTER, margin=0)
        add_text(slide, heading, x - 0.76, 4.17, 1.52, 0.40, 8.3 if x < 11 else 8.0, ORANGE, True, align=PP_ALIGN.CENTER)
        add_text(slide, detail, x - 0.77, 4.61, 1.54, 0.52, 8.0, DARK, align=PP_ALIGN.CENTER)

    add_text(
        slide,
        "Future-work milestones strengthen the chain; they are not demonstrated properties of the prototype.",
        1.10,
        5.37,
        11.12,
        0.24,
        9.3,
        ORANGE,
        True,
        align=PP_ALIGN.CENTER,
    )
    add_divider(slide, 1.75, 5.79, 9.83, BORDER, 0.012)
    add_text(slide, "Thank you · Questions?", 9.92, 5.93, 2.30, 0.22, 10.4, TU_RED, True, align=PP_ALIGN.RIGHT)
    add_note(
        slide,
        "The conclusion is specific to the evaluated systems path. VITA-FL connects the ledger-selected "
        "model, encrypted and signed handoff, TDX/AIR inference evidence, three receiver-signed tool "
        "receipts, and SCITT recording without making the conversational model a root of trust. Exact "
        "identities, freshness values, artifacts, inputs, and outputs are checked across component "
        "boundaries and mismatches fail closed. The prioritized outlook follows Chapter 8. First, the "
        "image digest needs a complete signed source-to-build-to-deployment chain through reproducible or "
        "attestable builds, signed provenance, verified software bills of materials, image signatures, "
        "vulnerability gates, and digest-pinned automation. Second, transparency should move to independent "
        "operators with durable replication, witnessed or gossiped checkpoints, external anchoring, and "
        "split-view testing. Third, assurance should expand to robust aggregation and poisoning tests, native "
        "DICOM provenance, purpose-specific inference identities with attested key delegation, larger and "
        "batched inference, and repeated failure-injection runs. These are future-work items, not demonstrated "
        "properties. The result remains a reproducible proof of concept rather than a production-ready or "
        "clinically validated platform.",
    )


def slide_worker_roles_backup(prs):
    slide = new_content_slide(
        prs,
        24,
        "One worker image—two authorized measured roles",
        "Backup · per-worker RTMR3 replay and separate policy authorization",
    )

    add_box(slide, 3.37, 1.43, 6.60, 0.76, fill=LIGHT, line=TU_RED, line_width=1.2)
    add_text(
        slide,
        "ONE DIGEST-PINNED dfl-worker IMAGE",
        3.63,
        1.64,
        6.08,
        0.25,
        14.2,
        TU_RED,
        True,
        align=PP_ALIGN.CENTER,
    )
    add_text(
        slide,
        "The packaged image contains both training and native inference code.",
        3.73,
        1.91,
        5.88,
        0.19,
        9.0,
        DARK,
        True,
        align=PP_ALIGN.CENTER,
    )

    # Route the branch around the role boxes so no connector crosses content.
    add_line_segment(slide, 6.67, 2.19, 6.67, 2.43, TU_RED, 1.6)
    add_line_segment(slide, 3.43, 2.43, 9.91, 2.43, TU_RED, 1.6)
    add_line_segment(slide, 3.43, 2.43, 3.43, 2.66, BLUE, 1.6, arrow=True)
    add_line_segment(slide, 9.91, 2.43, 9.91, 2.66, GREEN, 1.6, arrow=True)

    roles = [
        (
            0.66,
            "WORKERS 1 AND 2",
            "TRAINING-ONLY PROFILE",
            [
                "TEE_INFERENCE_ENABLED = 0",
                "Inference process and endpoint are not started",
                "Training-only policy-v2 identity",
                "Worker-specific Compose, event log, Quote V4, and RTMR3",
            ],
            BLUE_TINT,
            BLUE,
        ),
        (
            6.99,
            "WORKER 0",
            "COMBINED PROFILE",
            [
                "TEE_INFERENCE_ENABLED = 1",
                "Receiver starts beside the DFL services in the same CVM",
                "Combined training-and-inference policy-v2 identity",
                "Its own Compose, event log, Quote V4, and RTMR3",
            ],
            GREEN_TINT,
            GREEN,
        ),
    ]
    for x, heading, profile, bullets, fill, accent in roles:
        add_box(slide, x, 2.72, 5.68, 2.16, fill=fill, line=accent, line_width=1.2)
        add_text(slide, heading, x + 0.22, 2.96, 5.24, 0.28, 15.0, accent, True, align=PP_ALIGN.CENTER)
        add_text(slide, profile, x + 0.22, 3.33, 5.24, 0.22, 10.0, DARK, True, align=PP_ALIGN.CENTER)
        add_bullets(slide, bullets, x + 0.33, 3.70, 5.02, 0.96, 9.0, DARK, accent, 3)

    add_box(slide, 0.74, 5.08, 7.56, 0.56, fill=LIGHT, line=BORDER, radius=False)
    add_text(slide, "PER-WORKER REPLAY", 0.94, 5.20, 1.76, 0.20, 8.8, PURPLE, True)
    add_text(
        slide,
        "Compose preimage → ordered events → reconstructed RTMR3 = quoted RTMR3",
        2.65,
        5.17,
        5.42,
        0.26,
        8.7,
        DARK,
        True,
        align=PP_ALIGN.CENTER,
        valign=MSO_ANCHOR.MIDDLE,
    )
    add_box(slide, 8.48, 5.08, 4.13, 0.56, fill=LIGHT, line=BORDER, radius=False)
    add_text(slide, "AUTHORIZATION", 8.66, 5.20, 1.34, 0.20, 8.8, ORANGE, True)
    add_text(
        slide,
        "expected image digest + allowed role-policy hash",
        9.98,
        5.16,
        2.40,
        0.29,
        8.3,
        DARK,
        True,
        align=PP_ALIGN.CENTER,
        valign=MSO_ANCHOR.MIDDLE,
    )
    add_box(slide, 1.02, 5.84, 11.31, 0.42, fill=TU_RED, line=TU_RED, radius=False)
    add_text(
        slide,
        "Different Compose and RTMR3 values may pass; an injected image or unapproved role misses the admitted policy.",
        1.22,
        5.94,
        10.91,
        0.22,
        10.2,
        WHITE,
        True,
        align=PP_ALIGN.CENTER,
        valign=MSO_ANCHOR.MIDDLE,
    )
    add_note(
        slide,
        "All three live workers used the same digest-pinned dfl-worker OCI image, and that image packaged "
        "both the decentralized-training implementation and the native inference code. Role activation is "
        "separate from image contents. Worker 0 used the combined start profile and enabled the receiver; "
        "Workers 1 and 2 used the training-only profile and did not start that process. Each worker submitted "
        "its own canonical Compose preimage, ordered event log, fresh quote, and final RTMR3 value. The verifier "
        "replays each event log only against RTMR3 in its associated quote; it does not require one global final "
        "RTMR3. Replay establishes internal measurement consistency. A separate policy check authorizes the "
        "shared image digest and one of the two approved role-policy identities. Adding another image or an "
        "unapproved service changes the measured and policy-bound configuration and is rejected by the admitted "
        "profile. Phala user_config fields such as authorized SSH keys remain outside the measured app_compose "
        "and are therefore a separate deployment trust assumption.",
    )


def add_threat_tile(slide, threat_id: str, label: str, image_name: str, x: float, y: float):
    path = THREAT_DIAGRAMS / image_name
    if not path.exists():
        raise FileNotFoundError(f"Threat diagram not found: {path}")
    add_box(slide, x, y, 2.82, 1.96, fill=LIGHT, line=BORDER, radius=False)
    add_rich_text(
        slide,
        [
            (f"{threat_id}  ", TU_RED, True, 9.5),
            (label, DARK, True, 9.5),
        ],
        x + 0.11,
        y + 0.08,
        2.60,
        0.28,
        size=9.5,
        align=PP_ALIGN.LEFT,
        valign=MSO_ANCHOR.MIDDLE,
    )
    image_fit(slide, path, x + 0.08, y + 0.38, 2.66, 1.48)


def slide_threats_dfl(prs):
    slide = new_content_slide(
        prs,
        25,
        "Use and misuse cases: DFL production",
        "Backup · Threat views T1–T7",
    )
    threats = [
        ("T1", "Admission / identity", "T1.png"),
        ("T2", "Replay / stale context", "T2.png"),
        ("T3", "Training-input provenance", "T3.png"),
        ("T4", "Artifact substitution", "T4.png"),
        ("T5", "Model/key disclosure", "T5.png"),
        ("T6", "Aggregator omission", "T6.png"),
        ("T7", "Valid malicious updates", "T7.png"),
    ]
    top_x = [0.66, 3.72, 6.78, 9.84]
    bottom_x = [2.19, 5.25, 8.31]
    for index, threat in enumerate(threats):
        x = top_x[index] if index < 4 else bottom_x[index - 4]
        y = 1.50 if index < 4 else 3.72
        add_threat_tile(slide, *threat, x, y)
    add_note(
        slide,
        "This backup slide summarizes the use and misuse case views for the DFL production path. "
        "The diagrams relate workload admission, replay protection, signed training inputs, artifact "
        "identity, model confidentiality, aggregator availability, and valid-but-malicious updates to "
        "their corresponding controls. The following backup slides show each diagram at full size.",
    )


def slide_threats_agent(prs):
    slide = new_content_slide(
        prs,
        26,
        "Use and misuse cases: agent and infrastructure",
        "Backup · Threat views T8–T14",
    )
    threats = [
        ("T8", "Inference evidence", "T8.png"),
        ("T9", "Agent/tool manipulation", "T9.png"),
        ("T10", "Evidence suppression", "T10.png"),
        ("T11", "Log omission/equivocation", "T11.png"),
        ("T12", "Infrastructure DoS", "T12.png"),
        ("T13", "Root/key compromise", "T13.png"),
        ("T14", "Systemic collusion", "T14.png"),
    ]
    top_x = [0.66, 3.72, 6.78, 9.84]
    bottom_x = [2.19, 5.25, 8.31]
    for index, threat in enumerate(threats):
        x = top_x[index] if index < 4 else bottom_x[index - 4]
        y = 1.50 if index < 4 else 3.72
        add_threat_tile(slide, *threat, x, y)
    add_note(
        slide,
        "This backup slide summarizes the use and misuse case views for the agent, attested inference, "
        "transparency log, and infrastructure path. The diagrams distinguish forged or suppressed "
        "evidence from log equivocation, denial of service, root compromise, and collusion by otherwise "
        "valid participants. The following backup slides show each diagram at full size.",
    )


THREAT_DETAIL_SLIDES = [
    ("T1", "Unauthorized workload admission or identity substitution", "DFL production", "T1.png"),
    ("T2", "Replay or stale-context reuse", "DFL production", "T2.png"),
    ("T3", "Training-input or signer-policy manipulation", "DFL production", "T3.png"),
    ("T4", "Artifact substitution or stale publication", "DFL production", "T4.png"),
    ("T5", "Unauthorized model or key disclosure", "DFL production", "T5.png"),
    ("T6", "Aggregator omission or availability failure", "DFL production", "T6.png"),
    ("T7", "Semantically malicious but valid data or updates", "DFL production", "T7.png"),
    ("T8", "Inference substitution or forged evidence", "Agent and inference", "T8.png"),
    ("T9", "Agent or tool manipulation", "Agent and inference", "T9.png"),
    ("T10", "Evidence or result suppression", "Agent and transparency", "T10.png"),
    ("T11", "Transparency-log omission or equivocation", "Agent and transparency", "T11.png"),
    ("T12", "Infrastructure denial of service", "Cross-cutting residual threat", "T12.png"),
    ("T13", "Cryptographic, key, or platform-root compromise", "Cross-cutting residual threat", "T13.png"),
    ("T14", "Systemic collusion or economic manipulation", "Cross-cutting residual threat", "T14.png"),
]


def slide_threat_detail(prs, number, threat_id, title, group, image_name):
    slide = new_content_slide(
        prs,
        number,
        f"{threat_id} · {title}",
        f"Backup · Use and misuse case · {group}",
    )
    path = THREAT_DIAGRAMS / image_name
    if not path.exists():
        raise FileNotFoundError(f"Threat diagram not found: {path}")
    image_fit(slide, path, 0.70, 1.43, 11.95, 5.22)
    add_note(
        slide,
        f"This backup slide presents the full-size use and misuse case diagram for {threat_id}: "
        f"{title}. The corresponding threat specification and residual-risk discussion appear in "
        "Chapter 4 of the thesis.",
    )


def build():
    build_assets()
    prs = prepare_template()
    slide_title(prs)
    slide_about(prs)
    slide_problem(prs)
    slide_engineering_response(prs)
    slide_gap(prs)
    slide_architecture(prs)
    slide_dfl_hospitals(prs)
    slide_tee_vs_zk(prs)
    slide_phala_attestation_keys(prs)
    slide_aggregator_selection(prs)
    slide_aggregator_recovery(prs)
    slide_close_compare_commit(prs)
    slide_handoff(prs)
    slide_sello_protocol(prs)
    slide_agent(prs)
    slide_external_audit(prs)
    slide_cryptographic_chain(prs)
    slide_evaluation(prs)
    slide_learning_trajectories(prs)
    slide_learning_quality(prs)
    slide_conclusion(prs)
    slide_worker_roles_backup(prs)
    slide_threats_dfl(prs)
    slide_threats_agent(prs)
    for number, threat in enumerate(THREAT_DETAIL_SLIDES, start=25):
        slide_threat_detail(prs, number, *threat)
    assert len(prs.slides) == 38
    assert len(prs.slide_masters) == 2
    for index, slide in enumerate(prs.slides, start=1):
        assert slide.notes_slide.notes_text_frame.text.strip()
        if index > 1:
            assert any(
                getattr(shape, "has_text_frame", False)
                and shape.text.strip() == f"Page {index}"
                for shape in slide.shapes
            )
    assert any(
        shape.name == "Page 3 physician illustration with tablet"
        for shape in prs.slides[2].shapes
    )
    assert any(
        shape.name == "Page 4 computer scientist illustration with tablet"
        for shape in prs.slides[3].shapes
    )
    prs.save(DESTINATION)
    print(DESTINATION)


if __name__ == "__main__":
    build()
