#!/usr/bin/env python3
"""Build the English VITA-FL presentation from the TU Berlin template."""

from __future__ import annotations

import csv
from io import BytesIO
from pathlib import Path
from typing import Sequence

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

    legend = [(10, BLUE), (50, TU_RED), (100, GREEN)]
    legend_width = min(2.92, w - 0.40)
    legend_x = x + (w - legend_width) / 2
    for index, (participants, color) in enumerate(legend):
        item_x = legend_x + index * (legend_width / 3)
        add_line_segment(slide, item_x, y + 0.49, item_x + 0.24, y + 0.49, color, 2.0)
        add_text(
            slide,
            f"N={participants}",
            item_x + 0.29,
            y + 0.42,
            0.60,
            0.15,
            7.5,
            color,
            True,
            valign=MSO_ANCHOR.MIDDLE,
            margin=0,
        )

    plot_x = x + 0.52
    plot_y = y + 0.73
    plot_w = w - 0.72
    plot_h = h - 1.22
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


def build_assets():
    ASSETS.mkdir(parents=True, exist_ok=True)
    required_assets = [
        ASSETS / "xray_concept.png",
        ASSETS / "physician-editorial-illustration-tablet.png",
        ASSETS / "computer-scientist-editorial-illustration.png",
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
    slide = prs.slides.add_slide(prs.slide_masters[0].slide_layouts[1])
    remove_slide_placeholders(slide)
    return slide


def new_content_slide(prs, number, title, kicker):
    slide = prs.slides.add_slide(prs.slide_masters[1].slide_layouts[0])
    remove_slide_placeholders(slide)
    add_content_title(slide, title, kicker, number)
    return slide


def slide_title(prs):
    slide = new_title_slide(prs)
    add_text(slide, "MASTER'S THESIS · SHORT PRESENTATION", 0.63, 0.60, 5.8, 0.28, 12, TU_RED, True)
    add_text(
        slide,
        "Verifiable Decentralized Federated\nMachine Learning and Inference\nfor AI Agent Systems",
        0.67,
        2.20,
        6.95,
        1.45,
        24,
        WHITE,
        False,
    )
    add_text(
        slide,
        "ARCHITECTURE DESIGN FOR VERIFIABLE AI WORKFLOWS",
        7.71,
        2.38,
        4.86,
        0.24,
        9.4,
        "F7BBC1",
        True,
    )
    title_questions = [
        (2.87, 3.37, "Which model?"),
        (3.65, 4.15, "Which input?"),
        (4.43, 4.93, "Which workload?"),
    ]
    for text_y, line_y, question in title_questions:
        add_text(slide, question, 7.71, text_y, 4.86, 0.38, 20.5, WHITE, True)
        add_divider(slide, 7.71, line_y, 4.86, "E66B77", 0.012)
    add_text(slide, "Ramon Mehrpoya", 0.68, 6.48, 2.7, 0.28, 15, WHITE, True)
    add_text(slide, "Master's Thesis", 0.68, 6.84, 4.0, 0.24, 11, WHITE)
    add_text(slide, "19 August 2026", 10.85, 6.84, 1.88, 0.24, 11, WHITE, align=PP_ALIGN.RIGHT)
    add_note(
        slide,
        "This presentation introduces VITA-FL, a prototype that connects verifiable decentralized "
        "federated learning to attested inference in an AI-agent system. The central question is not "
        "only whether a prediction appears plausible. It is whether a user can inspect which model, "
        "which input, and which measured workload actually produced that result—and whether the "
        "supporting evidence was retained independently of the conversational claim.",
    )


def slide_about(prs):
    slide = new_content_slide(
        prs,
        2,
        "About me",
        "Academic background · project experience · Master's thesis",
    )

    # Editable portrait placeholder; replace these native shapes with a real
    # portrait later without rasterizing the remainder of the slide.
    add_box(slide, 0.67, 1.57, 4.08, 4.33, fill=DARK, line="686868", line_width=1.5)
    head = slide.shapes.add_shape(
        MSO_AUTO_SHAPE_TYPE.OVAL,
        Inches(2.13),
        Inches(2.81),
        Inches(1.15),
        Inches(1.15),
    )
    set_fill(head, TU_RED)
    head.line.fill.background()
    shoulders = slide.shapes.add_shape(
        MSO_AUTO_SHAPE_TYPE.ROUNDED_RECTANGLE,
        Inches(1.56),
        Inches(4.04),
        Inches(2.30),
        Inches(0.90),
    )
    set_fill(shoulders, TU_RED)
    shoulders.line.fill.background()
    add_text(
        slide,
        "PORTRAIT",
        1.91,
        5.49,
        1.61,
        0.22,
        9.0,
        WHITE,
        True,
        align=PP_ALIGN.CENTER,
        valign=MSO_ANCHOR.MIDDLE,
    )

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
        ("RQ 1", "How can a DFL model be integrated into an agent system through a trust-minimized, user-inspectable path?", GREEN_TINT, GREEN),
        ("RQ 1.1", "How can DFL strengthen integrity, accountable provenance, and selected availability properties?", BLUE_TINT, BLUE),
        ("RQ 1.2", "How can inference over the current DFL model be bound to attested execution and transparently recorded tool use?", PURPLE_TINT, PURPLE),
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
            4.45,
            3.35,
            1.30,
            14.5,
            DARK,
            True,
            valign=MSO_ANCHOR.MIDDLE,
        )
    add_note(
        slide,
        "Prior work typically treats decentralized model production, agent orchestration, and "
        "verifiable inference as separate concerns. The gap lies in composing these "
        "mechanisms into one deployment-oriented path. The thesis therefore asks how a DFL model can "
        "remain attributable from production to inference, how integrity and selected availability "
        "properties can be strengthened during training, and how a concrete inference can be bound to "
        "measured execution and transparent tool use.",
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
    update_paths = [
        ((3.71, 2.36), (3.79, 4.67), (5.83, 5.10)),
        ((9.63, 2.36), (9.54, 4.67), (7.50, 5.10)),
        ((9.83, 4.29), (9.13, 5.50), (7.50, 5.29)),
        ((3.50, 4.29), (4.21, 5.50), (5.83, 5.29)),
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
    slide = new_content_slide(prs, 8, "Block 1: verifiable model production", "Four control points before model publication")
    stages = [
        ("01", "INPUT", "Device signs image\nRadiologist signs label", GREEN_TINT, GREEN),
        ("02", "ADMISSION", "TDX/DCAP · RTMR3 replay\nREPORTDATA binding", BLUE_TINT, BLUE),
        ("03", "ROUND", "Ledger fixes aggregator,\ninput root, and policy", PURPLE_TINT, PURPLE),
        ("04", "AGGREGATION", "Candidate comparison\nParent-loss guard", ORANGE_TINT, ORANGE),
    ]
    for index, (number, label, body, fill, accent) in enumerate(stages):
        x = 0.65 + index * 3.05
        add_box(slide, x, 1.53, 2.72, 1.38, fill=fill, line=accent)
        add_text(slide, number, x + 0.16, 1.75, 0.38, 0.25, 11, accent, True)
        add_text(slide, label, x + 0.61, 1.72, 1.83, 0.3, 13.5, accent, True)
        add_text(slide, body, x + 0.17, 2.18, 2.38, 0.5, 12.5, DARK, True, align=PP_ALIGN.CENTER)
        if index < 3:
            add_arrow(slide, x + 2.74, 2.22, x + 3.01, 2.22, MID, 1.2)
    cards = [
        ("Measured workload identity", "Registration binds the image, policy, participant, action key, endpoints, and freshness.", BLUE_TINT, BLUE),
        ("Input provenance", "Independent RSA signatures authenticate pixels and labels; active signers are resolved from the ledger.", GREEN_TINT, GREEN),
        ("Publication integrity", "Atomic finalization binds the closed input root to the algorithm, policy, output, and nonce.", PURPLE_TINT, PURPLE),
    ]
    for index, (heading, body, fill, accent) in enumerate(cards):
        x = 0.70 + index * 4.03
        add_box(slide, x, 3.28, 3.68, 2.08, fill=fill, line=accent)
        add_text(slide, heading, x + 0.22, 3.53, 3.24, 0.36, 16, accent, True)
        add_text(slide, body, x + 0.22, 4.10, 3.22, 0.92, 14, DARK)
    add_note(
        slide,
        "Before publication, the system checks several distinct claims. Attestation determines whether "
        "an admitted participant runs the expected workload. Independent source signatures authenticate "
        "the image and its annotation. The ledger fixes the round context, aggregator, accepted inputs, "
        "and policy. Finally, deterministic candidate selection can retain the parent model when "
        "validation loss degrades beyond the configured threshold. This narrows specific attack paths, "
        "but it is not a proof of general Byzantine-robust learning.",
    )


def slide_tee_vs_zk(prs):
    slide = new_content_slide(
        prs,
        9,
        "Why attested off-chain execution—not ZK everywhere?",
        "Both execute off-chain · The evidence and trust assumptions differ",
    )

    add_box(slide, 0.66, 1.47, 12.00, 0.51, fill=LIGHT, line=TU_RED, radius=False)
    add_rich_text(
        slide,
        [
            ("ASK FIRST   ", TU_RED, True, 10.5),
            ("Do we need proof of one circuit—or provenance for a stateful native service?", DARK, True, 12.6),
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
            "TEE + REMOTE ATTESTATION",
            "SELECTED",
            "MEASURED NATIVE WORKLOAD",
            [
                "Native PyTorch, ledger/IPFS I/O, and key custody stay in one stateful workflow",
                "TDX isolation protects model, data, and secrets while they are in use",
                "DCAP evidence plus policy bind the TCB, image/Compose, identities, endpoints, and freshness",
                "The finalized model stays in its native training representation",
            ],
            BLUE_TINT,
            BLUE,
            GREEN,
        ),
        (
            6.82,
            "ZK-PROVED COMPUTATION",
            "EXPERIMENTAL",
            "EXACT ENCODED RELATION",
            [
                "Strong correctness for one precisely encoded model–input–output relation",
                "Circuit setup/keys → witness → proof → verify",
                "Translation, quantization, setup, and proving cost change with the model or circuit",
                "The proof alone does not establish native runtime identity, training history, or key custody",
            ],
            PURPLE_TINT,
            PURPLE,
            ORANGE,
        ),
    ]
    for x, heading, status, claim, bullets, fill, accent, status_color in panels:
        add_box(slide, x, 2.17, 5.88, 2.62, fill=fill, line=accent, line_width=1.2)
        add_text(slide, heading, x + 0.25, 2.40, 3.93, 0.29, 14.2, accent, True)
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
        add_text(slide, claim, x + 0.27, 2.80, 5.30, 0.22, 9.8, accent, True)
        add_bullets(
            slide,
            bullets,
            x + 0.26,
            3.10,
            5.34,
            1.48,
            10.5,
            DARK,
            accent,
            2,
        )

    add_box(slide, 0.92, 5.15, 11.50, 0.51, fill=TU_RED, line=TU_RED, radius=False)
    add_rich_text(
        slide,
        [
            ("VITA-FL DECISION   ", WHITE, True, 10.2),
            (
                "TEE/RA for native lifecycle provenance; ZK remains complementary for narrow computation claims.",
                WHITE,
                True,
                11.5,
            ),
        ],
        1.15,
        5.28,
        11.04,
        0.25,
        align=PP_ALIGN.CENTER,
        valign=MSO_ANCHOR.MIDDLE,
    )
    add_text(
        slide,
        "Sources: RFC 9334 · Intel TDX/DCAP · Chen et al., EuroSys ’24 · EZKL docs.",
        0.77,
        5.85,
        11.78,
        0.13,
        7.3,
        DARK,
        False,
        align=PP_ALIGN.CENTER,
        margin=0,
    )
    add_note(
        slide,
        "The first clarification is that both alternatives execute off chain. The design question is "
        "which evidence accompanies that execution. A zero-knowledge proof can establish strong "
        "computational correctness for exactly the relation encoded by a circuit and may keep witness "
        "values private. It does not by itself identify the native software stack, prove training history, "
        "or establish operational key custody. The experimental ZK branch required circuit setup, proof keys, "
        "witness generation, proving, and verification. VITA-FL instead needs a stateful workflow "
        "with native training and inference, ledger and IPFS interaction, protected model recovery, and "
        "application-bound keys. Intel TDX isolation and DCAP evidence, appraised against explicit policy, "
        "address that operational-provenance claim directly while retaining Intel, Phala/dstack, policy, "
        "and key custody as trust anchors. The choice therefore does not reject ZK: it reserves ZK "
        "for narrow encoded-computation claims where the additional translation and proving cost is justified. "
        "References: IETF RFC 9334; Intel TDX/DCAP documentation; Chen et al., ZKML, EuroSys 2024, "
        "https://doi.org/10.1145/3627703.3650088; and https://docs.ezkl.xyz/getting-started/.",
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
    steps = [
        ("01", "OBSERVE", "Workers detect repeated lack of round progress.", BLUE_TINT, BLUE),
        ("02", "REPORT", "Action key signs the exact round and aggregator; duplicates reject.", GREEN_TINT, GREEN),
        ("03", "FREEZE QUORUM", "First report snapshots E reporters; q = ceil(E·p/100), p = 50%.", PURPLE_TINT, PURPLE),
        ("04", "ABORT", "Penalize the failed aggregator, mark round r aborted, advance to r+1.", RED_TINT, TU_RED),
        ("05", "REPLACE", "Weighted draw excludes the failed address; state returns to TRAINING.", ORANGE_TINT, ORANGE),
    ]
    for index, (number, heading, body, fill, accent) in enumerate(steps):
        x = 0.48 + index * 2.55
        add_box(slide, x, 1.53, 2.26, 2.05, fill=fill, line=accent)
        add_text(slide, number, x + 0.15, 1.72, 0.34, 0.22, 10.5, accent, True)
        add_text(slide, heading, x + 0.52, 1.70, 1.54, 0.27, 11.2, accent, True)
        add_text(
            slide,
            body,
            x + 0.18,
            2.16,
            1.90,
            1.12,
            10.5,
            DARK,
            True,
            align=PP_ALIGN.CENTER,
            valign=MSO_ANCHOR.MIDDLE,
        )
        if index < 4:
            add_arrow(slide, x + 2.28, 2.55, x + 2.50, 2.55, MID, 1.2)

    add_text(slide, "STATE TRANSITION", 0.78, 3.94, 1.80, 0.24, 11.5, TU_RED, True)
    state_boxes = [
        (0.78, "LAST FINALIZED STATE", "Model M(r−1) remains authoritative", GREEN_TINT, GREEN),
        (4.72, "FAILED ATTEMPT", "Round r is recorded as aborted", RED_TINT, TU_RED),
        (8.66, "SUCCESSOR ROUND", "Round r+1 restarts from M(r−1)", BLUE_TINT, BLUE),
    ]
    for index, (x, heading, body, fill, accent) in enumerate(state_boxes):
        add_box(slide, x, 4.24, 3.58, 1.07, fill=fill, line=accent)
        add_text(slide, heading, x + 0.18, 4.44, 3.22, 0.22, 10.5, accent, True, align=PP_ALIGN.CENTER)
        add_text(slide, body, x + 0.18, 4.76, 3.22, 0.26, 11.5, DARK, True, align=PP_ALIGN.CENTER)
        if index < 2:
            add_arrow(slide, x + 3.60, 4.77, x + 3.90, 4.77, MID, 1.4)
    add_box(slide, 1.42, 5.57, 10.50, 0.49, fill=TU_RED, line=TU_RED, radius=False)
    add_text(
        slide,
        "No blockchain rewind: the failed attempt is abandoned and the previous finalized model is preserved.",
        1.64,
        5.68,
        10.06,
        0.27,
        12.8,
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


def slide_handoff(prs):
    slide = new_content_slide(prs, 13, "The critical boundary: authoritative model handoff", "Artifact identity survives untrusted storage")
    boxes = [
        (0.75, "LEDGER", "Round · publisher\nModel, key, and signature CIDs", RED_TINT, TU_RED),
        (4.72, "IPFS", "AES-GCM model ciphertext\nRSA-OAEP key envelopes", PURPLE_TINT, PURPLE),
        (8.68, "MEASURED RECEIVER", "Resolve · decrypt\nVerify signature and hashes", GREEN_TINT, GREEN),
    ]
    for x, heading, body, fill, accent in boxes:
        add_box(slide, x, 1.84, 3.26, 2.13, fill=fill, line=accent, line_width=1.2)
        add_text(slide, heading, x + 0.18, 2.14, 2.90, 0.32, 17, accent, True, align=PP_ALIGN.CENTER)
        add_text(slide, body, x + 0.20, 2.80, 2.86, 0.72, 16, DARK, True, align=PP_ALIGN.CENTER)
    add_arrow(slide, 4.04, 2.91, 4.66, 2.91, TU_RED, 2.0)
    add_arrow(slide, 8.01, 2.91, 8.62, 2.91, TU_RED, 2.0)
    add_box(slide, 1.31, 4.39, 10.70, 0.64, fill=LIGHT, line=TU_RED, radius=False)
    add_rich_text(
        slide,
        [
            ("Bound identity:  ", DARK, False, 14),
            ("publication hash", TU_RED, True, 15),
            ("  ·  ", MID, False, 15),
            ("model hash", GREEN, True, 15),
            ("  ·  ", MID, False, 15),
            ("publisher key", PURPLE, True, 15),
        ],
        1.46,
        4.59,
        10.40,
        0.30,
        align=PP_ALIGN.CENTER,
        valign=MSO_ANCHOR.MIDDLE,
    )
    add_box(slide, 2.15, 5.26, 9.01, 0.80, fill=TU_RED, line=TU_RED, radius=False)
    add_text(
        slide,
        "The agent never supplies a model path—the measured receiver resolves the current publication itself.",
        2.38,
        5.38,
        8.55,
        0.56,
        14,
        WHITE,
        True,
        align=PP_ALIGN.CENTER,
        valign=MSO_ANCHOR.MIDDLE,
    )
    add_note(
        slide,
        "The model handoff connects decentralized production to inference. Large artifacts remain "
        "outside the ledger, but the ledger authoritatively identifies the current publication and its "
        "references. Encryption protects model confidentiality, the publisher signature authenticates "
        "its origin, and content identifiers bind the retrieved objects. The measured receiver resolves "
        "and verifies this state itself. As a result, the agent cannot substitute an arbitrary local path "
        "or silently select a stale model.",
    )


def slide_sello_protocol(prs):
    slide = new_content_slide(
        prs,
        14,
        "Sello: the receiving service becomes the witness",
        "Proposed by Juan Figuera (2026) · Receiver-attested confidential receipts",
    )

    add_box(slide, 0.64, 1.46, 12.04, 0.52, fill=RED_TINT, line=TU_RED, radius=False)
    add_rich_text(
        slide,
        [
            ("TRUST-BOUNDARY INVERSION   ", TU_RED, True, 10.8),
            ("Instead of trusting agent-side traces, the called service records what it observed.", DARK, True, 12.5),
        ],
        0.84,
        1.59,
        11.64,
        0.25,
        align=PP_ALIGN.CENTER,
        valign=MSO_ANCHOR.MIDDLE,
    )

    stages = [
        (
            0.55,
            2.35,
            "1  AGENT",
            "Action + signed JWS token\nOwner HPKE key · log policy",
            BLUE_TINT,
            BLUE,
        ),
        (
            3.38,
            2.55,
            "2  RECEIVING SERVICE",
            "Verify token · execute action\nHash exact input + output",
            GREEN_TINT,
            GREEN,
        ),
        (
            6.42,
            2.60,
            "3  SELLO RECEIPT",
            "HPKE encrypt to owner\nCOSE_Sign1 with service key",
            ORANGE_TINT,
            ORANGE,
        ),
        (
            9.51,
            3.16,
            "4  TRANSPARENCY LOG",
            "Append encrypted envelope\nReturn Merkle inclusion proof",
            PURPLE_TINT,
            PURPLE,
        ),
    ]
    for x, width, heading, body, fill, accent in stages:
        add_box(slide, x, 2.23, width, 1.36, fill=fill, line=accent, line_width=1.2)
        add_text(
            slide,
            heading,
            x + 0.14,
            2.45,
            width - 0.28,
            0.27,
            11.3,
            accent,
            True,
            align=PP_ALIGN.CENTER,
        )
        add_text(
            slide,
            body,
            x + 0.17,
            2.82,
            width - 0.34,
            0.57,
            9.8,
            DARK,
            True,
            align=PP_ALIGN.CENTER,
            valign=MSO_ANCHOR.MIDDLE,
        )

    add_arrow(slide, 2.92, 2.91, 3.32, 2.91, BLUE, 1.5)
    add_arrow(slide, 5.95, 2.91, 6.36, 2.91, GREEN, 1.5)
    add_arrow(slide, 9.04, 2.91, 9.45, 2.91, PURPLE, 1.5)
    add_arrow(slide, 11.10, 3.63, 11.10, 3.91, PURPLE, 1.5)

    add_box(slide, 1.19, 3.96, 10.91, 0.80, fill=LIGHT, line=TU_RED, line_width=1.2)
    add_text(slide, "5  OWNER RECONSTRUCTS THE TRAIL", 1.41, 4.12, 2.93, 0.24, 10.8, TU_RED, True)
    add_text(
        slide,
        "Query by token_ref  →  verify witnessed log + service signature  →  decrypt locally",
        4.24,
        4.10,
        7.56,
        0.29,
        11.2,
        DARK,
        True,
        align=PP_ALIGN.CENTER,
        valign=MSO_ANCHOR.MIDDLE,
    )

    properties = [
        ("P1", "Receiver signs", BLUE_TINT, BLUE),
        ("P2", "Owner-encrypted", GREEN_TINT, GREEN),
        ("P3", "Witness-cosigned log", ORANGE_TINT, ORANGE),
        ("P4", "Owner discovery", PURPLE_TINT, PURPLE),
    ]
    for index, (number, label, fill, accent) in enumerate(properties):
        x = 0.64 + index * 3.06
        add_box(slide, x, 5.05, 2.83, 0.58, fill=fill, line=accent)
        add_text(slide, number, x + 0.14, 5.20, 0.43, 0.20, 9.8, accent, True)
        add_text(
            slide,
            label,
            x + 0.55,
            5.18,
            2.12,
            0.23,
            10.3,
            DARK,
            True,
            align=PP_ALIGN.CENTER,
        )

    add_rich_text(
        slide,
        [
            ("BOUNDARY   ", ORANGE, True, 9.2),
            ("No receipt can prove an unmade call; service collusion remains outside the guarantee.", DARK, True, 9.8),
        ],
        0.80,
        5.83,
        11.72,
        0.22,
        align=PP_ALIGN.CENTER,
        valign=MSO_ANCHOR.MIDDLE,
    )
    add_text(
        slide,
        "Source: J. Figuera, Notarized Agents, arXiv:2606.04193 (2026).",
        0.80,
        6.05,
        11.72,
        0.18,
        8.4,
        DARK,
        False,
        align=PP_ALIGN.CENTER,
    )
    add_note(
        slide,
        "Figuera's Sello protocol starts from a trust-boundary problem: a compromised agent or operator "
        "cannot be the sole source of truth about its own actions. The agent presents a signed JWS "
        "authorization token that binds the owner's HPKE public key and permitted log policy. The called "
        "service verifies that token, performs or denies the action, and hashes the exact input and output. "
        "It encrypts the receipt body to the owner with HPKE, signs the encrypted envelope with its own "
        "Ed25519 key in COSE_Sign1, and submits it to a witness-cosigned Merkle transparency log. The owner "
        "later discovers entries by the token-derived reference, verifies inclusion and the service key, and "
        "decrypts locally. VITA-FL adopts a Sello-inspired profile and additionally fails closed unless the "
        "receiver publishes its receipt before returning a successful tool result. Sello does not prove that "
        "a call was never made and does not prevent collusion by a receiving service. Source: Juan Figuera, "
        "Notarized Agents: Receiver-Attested Confidential Receipts for AI Agent Actions, arXiv:2606.04193, 2026.",
    )


def slide_agent(prs):
    slide = new_content_slide(prs, 15, "Block 2: agent-mediated attested inference", "Three bounded MCP operations, four log records")
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
    add_text(
        slide,
        "The log establishes accepted inclusion and ordering—not the semantic truth of the evidence.",
        1.18,
        5.96,
        10.97,
        0.23,
        11,
        DARK,
        True,
        align=PP_ALIGN.CENTER,
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


def slide_cryptographic_chain(prs):
    slide = new_content_slide(
        prs,
        16,
        "Cryptographic chain of custody",
        "Who produced it · who may read it · which exact bytes are bound",
    )
    cards = [
        (
            "01  MEDICAL INPUT",
            [
                ("SIGN\n", GREEN, True, 9.2),
                ("Device: RSA-2048 + SHA-256\nRadiologist: separate RSA signature\n\n", DARK, False, 8.8),
                ("VERIFY\n", GREEN, True, 9.2),
                ("Current on-chain role, key, and certificate snapshot", DARK, False, 8.8),
            ],
            GREEN_TINT,
            GREEN,
        ),
        (
            "02  PARTICIPANT TEE",
            [
                ("SIGN\n", BLUE, True, 9.2),
                ("dstack-bound secp256k1 action key\n\n", DARK, False, 8.8),
                ("KEY CUSTODY\n", BLUE, True, 9.2),
                ("RSA-3072 key sealed with dstack-derived AES-256-GCM\n\n", DARK, False, 8.8),
                ("BIND\n", BLUE, True, 9.2),
                ("REPORTDATA + RTMR3", DARK, False, 8.8),
            ],
            BLUE_TINT,
            BLUE,
        ),
        (
            "03  WORKER UPDATE",
            [
                ("ENCRYPT\n", ORANGE, True, 9.2),
                ("AES-256-CBC update; RSA-OAEP-SHA-256 key wrap\n\n", DARK, False, 8.8),
                ("SIGN + BIND\n", ORANGE, True, 9.2),
                ("Worker RSA-SHA-256 package signature + EIP-712 commitment", DARK, False, 8.8),
            ],
            ORANGE_TINT,
            ORANGE,
        ),
        (
            "04  GLOBAL MODEL",
            [
                ("ENCRYPT\n", PURPLE, True, 9.2),
                ("AES-256-GCM model; per-recipient RSA-OAEP key wrap\n\n", DARK, False, 8.8),
                ("SIGN + BIND\n", PURPLE, True, 9.2),
                ("Aggregator RSA-SHA-256 + EIP-712 finalization; IPFS CIDs", DARK, False, 8.8),
            ],
            PURPLE_TINT,
            PURPLE,
        ),
        (
            "05  INFERENCE + LOG",
            [
                ("VERIFY\n", TU_RED, True, 9.2),
                ("Finalized tuple + publisher signatures\n\n", DARK, False, 8.8),
                ("SIGN / ENCRYPT\n", TU_RED, True, 9.2),
                ("Ed25519 AIR + TDX; HPKE receiver receipt\n\n", DARK, False, 8.8),
                ("LOG\n", TU_RED, True, 9.2),
                ("ES256 statement + CCF inclusion receipt", DARK, False, 8.8),
            ],
            RED_TINT,
            TU_RED,
        ),
    ]
    for index, (heading, parts, fill, accent) in enumerate(cards):
        x = 0.42 + index * 2.55
        add_box(slide, x, 1.50, 2.36, 4.20, fill=fill, line=accent, line_width=1.1)
        add_text(
            slide,
            heading,
            x + 0.14,
            1.72,
            2.08,
            0.42,
            11.0,
            accent,
            True,
            align=PP_ALIGN.CENTER,
            valign=MSO_ANCHOR.MIDDLE,
        )
        add_divider(slide, x + 0.18, 2.25, 2.00, accent, 0.012)
        add_rich_text(
            slide,
            parts,
            x + 0.20,
            2.43,
            1.96,
            2.93,
            8.8,
            align=PP_ALIGN.LEFT,
            valign=MSO_ANCHOR.TOP,
        )
        if index < 4:
            add_arrow(slide, x + 2.38, 3.60, x + 2.51, 3.60, MID, 1.1)
    add_box(slide, 0.98, 5.83, 11.38, 0.35, fill=LIGHT, line=BORDER, radius=False)
    add_text(
        slide,
        "TLS protects transport hops; application signatures, recipient encryption, and ledger/log bindings survive intermediary storage.",
        1.18,
        5.91,
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
    slide = new_content_slide(prs, 17, "Evaluation: what was actually tested?", "Three evidence levels—not one blanket success claim")
    cards = [
        ("LIVE INTEGRATION", "3 TEE workers", "5 observed training rounds", "All three MCP operations\nplus attested inference", "LIVE", BLUE_TINT, BLUE),
        ("SCALE EXPERIMENTS", "10 · 50 · 100", "participants", "50 rounds per configuration", "COMPLETED", GREEN_TINT, GREEN),
        ("FAIL-CLOSED TESTS", "Admission · data", "Provenance · bindings", "Receipts · recovery", "AUTOMATED", ORANGE_TINT, ORANGE),
    ]
    for index, (heading, kpi, unit, detail, status, fill, accent) in enumerate(cards):
        x = 0.70 + index * 4.03
        add_box(slide, x, 1.52, 3.68, 4.20, fill=fill, line=accent, line_width=1.2)
        add_text(slide, heading, x + 0.18, 1.82, 3.32, 0.30, 13, accent, True, align=PP_ALIGN.CENTER)
        add_text(slide, kpi, x + 0.18, 2.48, 3.32, 0.65, 27 if index < 2 else 23, DARK, True, align=PP_ALIGN.CENTER)
        add_text(slide, unit, x + 0.18, 3.20, 3.32, 0.34, 15, accent, True, align=PP_ALIGN.CENTER)
        add_divider(slide, x + 0.48, 3.83, 2.72, BORDER)
        add_text(slide, detail, x + 0.34, 4.22, 3.0, 0.68, 15, DARK, True, align=PP_ALIGN.CENTER)
        add_box(slide, x + 0.92, 5.15, 1.84, 0.36, fill=accent, line=accent, radius=False)
        add_text(slide, status, x + 0.98, 5.24, 1.72, 0.18, 9.5, WHITE, True, align=PP_ALIGN.CENTER)
    add_text(
        slide,
        "Not evaluated: clinical suitability · formal Byzantine fault tolerance · general poisoning robustness",
        1.0,
        5.89,
        11.32,
        0.25,
        11.5,
        TU_RED,
        True,
        align=PP_ALIGN.CENTER,
    )
    add_note(
        slide,
        "The evaluation distinguishes live integration, participant-scale experiments, and automated "
        "negative tests. The Phala run exercised the connected services, training, all three MCP "
        "operations, and attested inference. Separate experiments completed 50-round runs with 10, 50, "
        "and 100 participants. Negative tests checked whether manipulated, stale, or context-mismatched "
        "objects fail closed. The later adaptive aggregation extension has component and binding tests, "
        "but no dedicated live adversarial-robustness experiment.",
    )


def slide_learning_trajectories(prs):
    slide = new_content_slide(
        prs,
        18,
        "Observed optimization trajectories overlap across scale",
        "One completed run for 10, 50, and 100 participants",
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
    )
    findings = [
        ("LOSS", "≈ 0.62  →  ≈ 0.188", BLUE_TINT, BLUE),
        ("EXACT MATCH", "≈ 0%  →  ≈ 53.16%", GREEN_TINT, GREEN),
        ("OBSERVATION", "Nearly identical curves at all three tested scales", LIGHT, DARK),
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
            9.8,
            DARK,
            True,
            align=PP_ALIGN.CENTER,
            valign=MSO_ANCHOR.MIDDLE,
        )
    add_note(
        slide,
        "The three completed ChestMNIST runs each expose forty-nine learned global models from rounds "
        "two through fifty; round one is the bootstrap state. Loss falls from approximately 0.62 to "
        "0.188 and exact match rises to approximately fifty-three percent. The trajectories for ten, "
        "fifty, and one hundred participants almost overlap. This is an observed single run per scale, "
        "so it validates repeatable protocol execution but is not statistical evidence of scale invariance.",
    )


def slide_learning_quality(prs):
    slide = new_content_slide(
        prs,
        19,
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
    )
    add_box(slide, 1.00, 5.57, 11.33, 0.51, fill=TU_RED, line=TU_RED, radius=False)
    add_text(
        slide,
        "The model converges toward majority-negative predictions: protocol execution succeeds, diagnostic learning quality does not.",
        1.24,
        5.68,
        10.85,
        0.27,
        12.2,
        WHITE,
        True,
        align=PP_ALIGN.CENTER,
        valign=MSO_ANCHOR.MIDDLE,
    )
    add_note(
        slide,
        "The optimization curves must not be read as clinical success. At round fifty, macro AUROC is "
        "approximately 0.504, 0.507, and 0.508 for ten, fifty, and one hundred participants. Micro F1 "
        "falls to about 0.0001 and macro F1 to about 0.0005 to 0.001. Loss reduction and rising exact "
        "match are therefore explained by majority-negative behavior under severe class imbalance. "
        "These runs validate protocol execution and participant scaling, not diagnostic utility.",
    )


def slide_results(prs):
    slide = new_content_slide(prs, 20, "Results: demonstrated chain and explicit limits", "System integration is not a clinical claim")
    kpis = [
        ("3 + 1", "transparency records", "Three tool receipts plus one complete inference bundle", PURPLE_TINT, PURPLE),
        ("78,468", "signed training samples", "Pixel, label, and policy tampering rejected", GREEN_TINT, GREEN),
        ("10 · 50 · 100", "participants", "Every scale experiment reached round 50", BLUE_TINT, BLUE),
    ]
    for index, (value, label, body, fill, accent) in enumerate(kpis):
        x = 0.70 + index * 4.03
        add_box(slide, x, 1.53, 3.68, 1.78, fill=fill, line=accent)
        add_text(slide, value, x + 0.17, 1.78, 3.34, 0.52, 27, accent, True, align=PP_ALIGN.CENTER)
        add_text(slide, label, x + 0.17, 2.40, 3.34, 0.30, 14, DARK, True, align=PP_ALIGN.CENTER)
        add_text(slide, body, x + 0.24, 2.84, 3.20, 0.32, 10.8, DARK, align=PP_ALIGN.CENTER)
    add_box(slide, 0.72, 3.66, 5.78, 1.66, fill=GREEN_TINT, line=GREEN)
    add_text(slide, "DEMONSTRATED", 0.98, 3.91, 2.1, 0.30, 14, GREEN, True)
    add_bullets(
        slide,
        ["End-to-end execution of the prototype", "Rejection of tampered and stale-context objects"],
        0.96,
        4.38,
        5.20,
        0.72,
        14.5,
        DARK,
        GREEN,
        5,
    )
    add_box(slide, 6.80, 3.66, 5.78, 1.66, fill=ORANGE_TINT, line=ORANGE)
    add_text(slide, "NOT DEMONSTRATED", 7.06, 3.91, 2.6, 0.30, 14, ORANGE, True)
    add_bullets(
        slide,
        ["Clinical validity or diagnostic utility", "Macro AUROC ≈ 0.50; F1 scores trend toward zero"],
        7.04,
        4.38,
        5.18,
        0.72,
        14.5,
        DARK,
        ORANGE,
        5,
    )
    add_box(slide, 1.32, 5.60, 10.70, 0.48, fill=TU_RED, line=TU_RED, radius=False)
    add_text(
        slide,
        "The evidence chain supports the process claim—not the medical correctness of the model.",
        1.52,
        5.71,
        10.30,
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
        "and rejected targeted changes to pixels, labels, and signer policy. All participant-scale "
        "experiments reached round 50. However, macro AUROC remained close to 0.50 and the F1 scores "
        "approached zero. These results demonstrate protocol execution and evidence binding, not useful "
        "diagnostic performance.",
    )


def slide_conclusion(prs):
    slide = new_content_slide(
        prs,
        21,
        "Conclusion and outlook",
        "Composed evidence works · next: strengthen source-to-deployment trust",
    )
    add_box(slide, 0.70, 1.52, 5.75, 3.67, fill=GREEN_TINT, line=GREEN)
    add_text(slide, "CONCLUSION · DEMONSTRATED", 0.98, 1.82, 4.50, 0.32, 15, GREEN, True)
    add_bullets(
        slide,
        [
            "End-to-end chain: ledger-selected model → encrypted handoff → TDX/AIR result → three tool receipts → SCITT record",
            "Deterministic trust path: selection, decryption, validation, and inference remain outside the language model",
            "Fail-closed bindings: identities, freshness, artifacts, inputs, and outputs are checked across component boundaries",
        ],
        0.98,
        2.25,
        5.13,
        2.62,
        10.8,
        DARK,
        GREEN,
        6,
    )
    add_box(slide, 6.82, 1.52, 5.75, 3.67, fill=ORANGE_TINT, line=ORANGE)
    add_text(slide, "CONCRETE NEXT STEPS", 7.10, 1.82, 3.1, 0.32, 15, ORANGE, True)
    add_bullets(
        slide,
        [
            "Supply chain: signed source → build → image provenance, reproducible or attestable builds, verified SBOMs, image signatures, and vulnerability gates",
            "Independent logs: replicated SCITT/CCF operators, witnessed or gossiped checkpoints, external anchoring, and split-view tests",
            "Assurance at scale: robust aggregation and poisoning tests, native DICOM provenance, separated inference keys, and repeated runs",
        ],
        7.10,
        2.25,
        5.12,
        2.62,
        10.4,
        DARK,
        ORANGE,
        6,
    )
    add_box(slide, 1.05, 5.39, 11.20, 0.65, fill=TU_RED, line=TU_RED, radius=False)
    add_text(slide, "CORE CONCLUSION", 1.30, 5.61, 1.75, 0.24, 10.5, WHITE, True)
    add_text(
        slide,
        "VITA-FL composes scoped evidence from decentralized model production to agent consumption—"
        "a reproducible proof of concept, not a trustless or clinically validated platform.",
        3.12,
        5.48,
        8.78,
        0.42,
        10.8,
        WHITE,
        True,
        align=PP_ALIGN.CENTER,
        valign=MSO_ANCHOR.MIDDLE,
    )
    add_text(slide, "Thank you · Questions?", 10.03, 6.15, 2.18, 0.22, 11, TU_RED, True, align=PP_ALIGN.RIGHT)
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
        22,
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
        23,
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
    slide_dfl(prs)
    slide_tee_vs_zk(prs)
    slide_phala_attestation_keys(prs)
    slide_aggregator_selection(prs)
    slide_aggregator_recovery(prs)
    slide_handoff(prs)
    slide_sello_protocol(prs)
    slide_agent(prs)
    slide_cryptographic_chain(prs)
    slide_evaluation(prs)
    slide_learning_trajectories(prs)
    slide_learning_quality(prs)
    slide_results(prs)
    slide_conclusion(prs)
    slide_threats_dfl(prs)
    slide_threats_agent(prs)
    for number, threat in enumerate(THREAT_DETAIL_SLIDES, start=24):
        slide_threat_detail(prs, number, *threat)
    assert len(prs.slides) == 37
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
