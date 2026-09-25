#!/usr/bin/env python3
"""Build the English VITA-FL presentation from the TU Berlin template."""

from __future__ import annotations

import csv
import json
import sys
from copy import deepcopy
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

from technology_icons import (
    add_icon,
    add_architecture_technology_icons,
    add_project_technology_icons,
    add_research_gap_sequence,
)


ROOT = Path(__file__).resolve().parent
OUT = ROOT
SOURCE_ROOT = Path("/home/ramon/master/Master-Thesis/presentation")
ASSETS = SOURCE_ROOT / "assets"
THREAT_DIAGRAMS = ASSETS / "threat-diagrams"
EVALUATION_DATA = SOURCE_ROOT / "data" / "evaluation"
AUTHORITATIVE_RUN = EVALUATION_DATA / "authoritative_phala_6w_24r.csv"
AUTHORITATIVE_SUMMARY = EVALUATION_DATA / "authoritative_phala_6w_24r_first_best_final.csv"
AUTHORITATIVE_WORKERS = EVALUATION_DATA / "authoritative_phala_6w_24r_worker_activity.csv"
AUTHORITATIVE_MANIFEST = EVALUATION_DATA / "authoritative_phala_6w_24r_manifest.json"
EVALUATED_TIER1_ACTIVE_TEE_LIMIT = 8
EVALUATED_NON_WORKER_CVMS = ("contract/control runtime", "Ollama")
TEMPLATE = SOURCE_ROOT / "TU_Berlin_Praesentation_Master_einfarbig_Rot.pptx"
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


def load_authoritative_evaluation():
    required = [
        AUTHORITATIVE_RUN,
        AUTHORITATIVE_SUMMARY,
        AUTHORITATIVE_WORKERS,
        AUTHORITATIVE_MANIFEST,
    ]
    for path in required:
        if not path.is_file():
            raise FileNotFoundError(f"Missing authoritative evaluation input: {path}")

    numeric_fields = {
        "federated_round": int,
        "global_model_round": int,
        "timestamp_unix_ms": int,
        "participant_count": int,
        "aggregated_model_count": int,
        "expected_models": int,
        "accuracy_percent": float,
        "exact_match_percent": float,
        "loss": float,
        "micro_f1": float,
        "macro_f1": float,
        "macro_auroc": float,
    }
    with AUTHORITATIVE_RUN.open(newline="", encoding="utf-8") as handle:
        rows = []
        for source in csv.DictReader(handle):
            row = dict(source)
            for field, conversion in numeric_fields.items():
                row[field] = conversion(row[field])
            rows.append(row)

    expected_federated_rounds = list(range(1, 25))
    if [row["federated_round"] for row in rows] != expected_federated_rounds:
        raise ValueError(f"Unexpected federated-round trajectory in {AUTHORITATIVE_RUN}")
    if [row["global_model_round"] for row in rows] != list(range(2, 26)):
        raise ValueError(f"Unexpected global-model trajectory in {AUTHORITATIVE_RUN}")
    if any(
        row["participant_count"] != 6
        or row["aggregated_model_count"] != 5
        or row["expected_models"] != 5
        for row in rows
    ):
        raise ValueError(f"Unexpected worker/update count in {AUTHORITATIVE_RUN}")

    with AUTHORITATIVE_SUMMARY.open(newline="", encoding="utf-8") as handle:
        summary = {row["metric"]: row for row in csv.DictReader(handle)}
    with AUTHORITATIVE_WORKERS.open(newline="", encoding="utf-8") as handle:
        workers = []
        for source in csv.DictReader(handle):
            row = dict(source)
            for field in (
                "training_rounds",
                "model_transfers",
                "aggregator_rounds",
                "selection_gap_recoveries",
                "transactions",
                "registration_gas",
                "gas_used",
            ):
                row[field] = int(row[field])
            workers.append(row)
    with AUTHORITATIVE_MANIFEST.open(encoding="utf-8") as handle:
        manifest = json.load(handle)

    if manifest.get("evidence_policy") != "sole evaluation run used by thesis, journal, and presentation":
        raise ValueError("The presentation only accepts the declared sole authoritative evaluation run")
    training = manifest["training"]
    if training["successful_federated_rounds"] != 24 or training["aborted_round_attempts"] != 0:
        raise ValueError("The authoritative run must contain 24 successful rounds and zero aborts")
    worker_count = manifest["runtime"]["worker_count"]
    if worker_count != training["training_shards"]:
        raise ValueError("The authoritative run must assign one training shard to every worker")
    if training["training_samples"] != worker_count * training["samples_per_shard"]:
        raise ValueError("The authoritative training samples must be fully represented by the six shards")
    if worker_count + len(EVALUATED_NON_WORKER_CVMS) != EVALUATED_TIER1_ACTIVE_TEE_LIMIT:
        raise ValueError("The evaluated Tier-1 capacity allocation must account for all eight TEE slots")
    gas_accounting = manifest["gas_accounting"]
    if len(workers) != worker_count or any(worker["registration_gas"] <= 0 for worker in workers):
        raise ValueError("Every authoritative worker must have one reconciled RTMR3 registration receipt")
    if sum(worker["registration_gas"] for worker in workers) != gas_accounting["registration"]["gas"]:
        raise ValueError("Per-worker RTMR3 registration gas does not match the authoritative subtotal")
    if sum(worker["gas_used"] for worker in workers) != gas_accounting["worker"]["gas"]:
        raise ValueError("Per-worker gas does not match the authoritative worker total")
    return {"rows": rows, "summary": summary, "workers": workers, "manifest": manifest}


def add_run_metric_chart(
    slide,
    x,
    y,
    w,
    h,
    title,
    rows,
    metric,
    y_min,
    y_max,
    y_ticks,
    color=BLUE,
    reference=None,
    reference_label=None,
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

    plot_x = x + 0.52
    plot_y = y + 0.77
    plot_w = w - 0.72
    plot_h = h - 1.31
    x_ticks = (2, 6, 11, 18, 25)
    x_min, x_max = 2, 25

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
        "Global model round",
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
        px = plot_x + ((round_number - x_min) / (x_max - x_min)) * plot_w
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
            reference_label or "reference",
            plot_x + plot_w - 0.54,
            py - 0.18,
            0.50,
            0.14,
            7.0,
            "686868",
            align=PP_ALIGN.RIGHT,
            margin=0,
        )

    points = []
    for row in rows:
        px = plot_x + ((row["global_model_round"] - x_min) / (x_max - x_min)) * plot_w
        value = max(y_min, min(y_max, row[metric]))
        py = plot_y + plot_h - ((value - y_min) / (y_max - y_min)) * plot_h
        points.append((px, py))
    for first, second in zip(points, points[1:]):
        add_line_segment(slide, first[0], first[1], second[0], second[1], color, 1.9)
    for index in (0, len(points) - 1):
        px, py = points[index]
        add_oval(slide, px - 0.045, py - 0.045, 0.09, 0.09, color, color, 0.5)
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


def add_domain_navigation(slide, page_number: int, *, active_domains: set[str] | None = None):
    """Show the active DFL/agent responsibilities after the introductory slides."""
    prefix = "Domain navigation: "
    for shape in list(slide.shapes):
        if shape.name.startswith(prefix):
            remove_shape(shape)
    if page_number <= 6:
        return

    # Literature, FL/DFL foundations, and lifecycle precede the detailed architecture.
    dfl_pages = {7, 8, 9} | {page + 4 for page in {*range(6, 13), *range(17, 24), *range(25, 32), *range(36, 39)}}
    agent_pages = {7, 9} | {page + 4 for page in {6, *range(13, 19), 21, 22, 24, *range(32, 38)}}
    # Provision the shared worker-image policy before the attestation details.
    dfl_pages = {page + (page >= 13) for page in dfl_pages} | {13}
    agent_pages = {page + (page >= 13) for page in agent_pages} | {13}
    # Separate on-chain verification (14) from shared dstack-derived keys (15).
    dfl_pages = {page + (page >= 15) for page in dfl_pages} | {15}
    agent_pages = {page + (page >= 15) for page in agent_pages} | {15}
    # The implemented-test inventory follows the cloud-run overview on Page 24.
    dfl_pages = {page + (page >= 25) for page in dfl_pages} | {25}
    agent_pages = {page + (page >= 25) for page in agent_pages} | {25}
    x, y, height = 10.40, .55, .25
    gap, padding = 8 / 120, 4 / 120
    domains = (
        ("DFL", .45, "207548", page_number in dfl_pages if active_domains is None else "DFL" in active_domains),
        ("Agent", .55, "1764A1", page_number in agent_pages if active_domains is None else "Agent" in active_domains),
    )
    background = add_box(
        slide, x - padding, y - padding, .45 + gap + .55 + 2 * padding,
        height + 2 * padding, fill=WHITE, line=WHITE, radius=False, line_width=0,
    )
    background.name = prefix + "background"
    for label, width, color, active in domains:
        badge = add_box(
            slide, x, y, width, height,
            fill=color if active else "F5F6F7",
            line=color if active else "D7DEE3", radius=False, line_width=.55,
        )
        badge.name = prefix + label + " badge"
        caption = add_text(
            slide, label, x, y, width, height, 8.4,
            WHITE if active else "5D6973", True,
            align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE, margin=0,
        )
        caption.name = prefix + label + " label"
        x += width + gap


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
        ASSETS / "ramon-mehrpoya-portrait-2026-09-08.jpg",
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
    add_domain_navigation(slide, len(prs.slides))
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


def slide_hospital_motivation(prs):
    """Introduce the hospital scenario after the research questions."""
    slide = new_content_slide(
        prs,
        3,
        "Several hospitals. One shared model.",
        "Motivation · Learning together, keeping patient data local",
    )

    add_box(slide, 0.78, 1.85, 4.20, 3.05, fill=GREEN_TINT, line=GREEN, line_width=1.0)
    add_text(slide, "Hospital consortium", 1.02, 2.04, 3.72, 0.35, 17, DARK, True, align=PP_ALIGN.CENTER)
    for label, cx in zip(("A", "B", "C"), (1.59, 2.88, 4.17)):
        add_hospital_campus_icon(slide, cx, 3.06, GREEN, 1.75)
        add_text(slide, f"Hospital {label}", cx - 0.53, 3.57, 1.06, 0.25, 11, DARK, True, align=PP_ALIGN.CENTER)
    add_text(
        slide, "Complementary datasets\nPatient data stay local",
        1.04, 4.08, 3.68, 0.58, 14, DARK, align=PP_ALIGN.CENTER,
    )

    add_arrow(slide, 5.12, 3.17, 5.60, 3.17, GREEN, 2.0)
    add_box(slide, 5.74, 1.85, 3.05, 3.05, fill=LIGHT, line=BORDER, line_width=1.0)
    add_text(slide, "Jointly trained", 5.95, 2.04, 2.63, 0.35, 17, DARK, True, align=PP_ALIGN.CENTER)
    layers = (
        ((6.43, 2.74), (6.43, 3.10), (6.43, 3.46)),
        ((7.27, 2.62), (7.27, 3.10), (7.27, 3.58)),
        ((8.09, 2.90), (8.09, 3.30)),
    )
    for first, second in zip(layers, layers[1:]):
        for x1, y1 in first:
            for x2, y2 in second:
                add_line_segment(slide, x1, y1, x2, y2, MID, 0.9)
    for layer in layers:
        for cx, cy in layer:
            add_oval(slide, cx - 0.09, cy - 0.09, 0.18, 0.18, TU_RED, TU_RED, 0.7)
    add_text(
        slide, "Custom-trained model\nfor chest X-rays",
        5.96, 4.08, 2.61, 0.58, 14, DARK, align=PP_ALIGN.CENTER,
    )

    add_arrow(slide, 8.93, 3.17, 9.41, 3.17, BLUE, 2.0)
    add_box(slide, 9.55, 1.85, 3.03, 3.05, fill=BLUE_TINT, line=BLUE, line_width=1.0)
    add_text(slide, "Later use", 9.77, 2.04, 2.59, 0.35, 17, DARK, True, align=PP_ALIGN.CENTER)
    add_icon(slide, "agent", 10.57, 2.60, 0.98, BLUE, BLUE_TINT, prefix="Hospital motivation: ")
    add_text(
        slide, "Physician accesses the model\nthrough an AI assistant",
        9.72, 4.06, 2.70, 0.65, 12.5, DARK, align=PP_ALIGN.CENTER,
    )

    add_box(slide, 0.80, 5.30, 11.77, 0.72, fill=WHITE, line=BORDER, radius=False, line_width=0.7)
    add_box(slide, 0.80, 5.30, 0.075, 0.72, fill=TU_RED, line=TU_RED, radius=False, line_width=0)
    add_text(
        slide, "Shared control during training. Evidence for each prediction.",
        1.04, 5.49, 11.18, 0.32, 17, DARK, True, align=PP_ALIGN.CENTER,
    )
    add_note(
        slide,
        "Imagine a hospital consortium developing a chest X-ray model together. Each institution "
        "contributes experience from its own patient population while keeping the underlying records "
        "local. The three hospitals illustrate a wider consortium; they are not the participant count "
        "of the prototype evaluation. The hospitals also want shared control over participation and "
        "model development, confidence that contributions are processed correctly, and a way to "
        "continue if the participant coordinating training becomes unavailable. Later, a physician "
        "accesses this custom-trained specialist model through an AI assistant. The value of joint "
        "training depends on being able to establish that this model processed the submitted image "
        "and produced the reported result. The arrows summarize model development and later use; "
        "they do not depict patient-data transfers or an implementation architecture. This is the "
        "motivating scenario from Chapter 1, not a claim of clinical validation.",
    )
    return slide


def slide_about(prs):
    slide = new_content_slide(
        prs,
        2,
        "About me",
        "Academic background · project experience · Master's thesis",
    )

    portrait_path = ASSETS / "ramon-mehrpoya-portrait-2026-09-08.jpg"
    portrait = slide.shapes.add_picture(
        str(portrait_path),
        Inches(0.67),
        Inches(1.49),
        Inches(4.08),
        Inches(4.44),
    )
    # Fill the existing frame, removing excess wall above the portrait.
    with Image.open(portrait_path) as photo:
        portrait.crop_top = 1 - (photo.width / photo.height) / (4.08 / 4.44)
    portrait.auto_shape_type = MSO_AUTO_SHAPE_TYPE.ROUNDED_RECTANGLE
    portrait.name = "Page 2 Ramon Mehrpoya portrait"
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
        (5.42, "GAIA-X 4 PLC-AAD", GREEN_TINT, GREEN),
        (7.63, "ZOKRATES PLUS", BLUE_TINT, BLUE),
        (9.83, "ZODIAC", ORANGE_TINT, ORANGE),
    ]
    for x, project, fill, accent in projects:
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
        add_arrow(slide, x + 1.065, 4.65, x + 1.065, 5.00, TU_RED, 1.8)

    add_project_technology_icons(slide)

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
    add_box(slide, 4.47, 1.88, 3.52, 1.90, fill=WHITE, line=TU_RED, line_width=1.5)
    add_box(slide, 4.47, 1.88, 0.10, 1.90, fill=TU_RED, line=TU_RED, radius=False)
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

    add_box(slide, 5.35, 1.88, 3.52, 1.90, fill=WHITE, line=TU_RED, line_width=1.5)
    add_box(slide, 8.77, 1.88, 0.10, 1.90, fill=TU_RED, line=TU_RED, radius=False)
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
    add_architecture_technology_icons(slide)
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
    slide = new_content_slide(prs, 6, "Research gap and research questions", "Research positioning")
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
        "Focus: attestation-based DFL → inference → verifiable agent use.",
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
    add_research_gap_sequence(slide)
    questions = [
        (
            "RQ 1:",
            "Trustworthy integration",
            GREEN_TINT,
            GREEN,
        ),
        (
            "RQ 1.1:",
            "Integrity & availability",
            BLUE_TINT,
            BLUE,
        ),
        (
            "RQ 1.2:",
            "Verifiable inference",
            PURPLE_TINT,
            PURPLE,
        ),
    ]
    for index, (label, body, fill, accent) in enumerate(questions):
        x = 0.68 + index * 4.07
        add_box(slide, x, 4.82, 3.83, 1.12, fill=fill, line=accent)
        add_text(
            slide,
            label,
            x + 0.24,
            4.94,
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
            5.42,
            3.35,
            0.36,
            17,
            DARK,
            True,
            valign=MSO_ANCHOR.MIDDLE,
        )
    add_note(
        slide,
        "The main research question asks how DFL models can be integrated into AI agent-based system "
        "architectures while preserving trustworthiness across the complete training and inference "
        "pipeline. The first sub-question focuses on integrity and availability during verifiable DFL "
        "training. The second asks how inference and model predictions can be made verifiable, for "
        "example through cryptographic proofs of execution. Existing work already connects lifecycle "
        "stages, as shown on the following comparison slide. The thesis studies a concrete "
        "attestation-based implementation and its trust assumptions; it does not claim to be the "
        "first end-to-end verifiable AI system.",
    )


def slide_literature_comparison(prs):
    """Source-linked comparison of system coverage and verification mechanisms."""
    slide = new_content_slide(
        prs, 7, "Prior work: system coverage and verification",
        "Existing lifecycle links · Different evidence and trust assumptions",
    )

    # These are representative scopes, not an exhaustive feature/quality ranking.
    stage_x = (3.35, 4.55, 5.83, 6.89)
    stage_w = (1.02, 1.10, .88, 1.33)
    stage_colors = (GREEN, BLUE, ORANGE, PURPLE)
    mechanism_x = (8.77, 9.49, 10.61, 12.00)
    add_text(slide, "WORK", .82, 1.51, 2.4, .27, 12, DARK, True)
    add_text(slide, "SYSTEM COVERAGE", 3.35, 1.51, 4.87, .27, 12, DARK, True, align=PP_ALIGN.CENTER)
    add_text(slide, "VERIFICATION MECHANISMS", 8.34, 1.51, 4.24, .27, 12, DARK, True, align=PP_ALIGN.CENTER)
    for x, w, label, accent in zip(stage_x, stage_w, ("DFL", "Inference", "Agent", "Transparency\nLog"), stage_colors):
        add_text(slide, label, x - .055, 2.07, w + .11, .44, 11.5, accent, True,
                 align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE, margin=0)
    add_text(slide, "Remote attestation", 9.98, 1.78, 2.63, .27, 11.5, DARK, True, align=PP_ALIGN.CENTER)
    add_line_segment(slide, 10.12, 2.06, 12.46, 2.06, BORDER, 1.0)
    for x in (10.12, 12.46):
        add_line_segment(slide, x, 2.06, x, 2.13, BORDER, 1.0)
    for x, label, w in zip(mechanism_x, ("ZKP", "TEE", "Quote\nverification", "RTMR3\nreplay"), (.62, .61, 1.22, 1.08)):
        add_text(slide, label, x - w / 2, 2.12, w, .42, 11.3, DARK, True,
                 align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE, margin=0)

    # (label, source, stage labels/status, mechanisms). Status 2: implemented;
    # 1: discussed/framework; 0: not described in the checked system/paper.
    rows = (
        ("Lee, Heiss et al. · 2024", "https://arxiv.org/abs/2404.12623",
         (("DFL", 2), None, None, None), (2, 0, 0, 0)),
        ("Ebrahimi et al. · 2024", "https://doi.org/10.1109/Blockchain62396.2024.00017",
         (("DFL", 2), None, None, None), (2, 0, 0, 0)),
        ("Voltran · 2024", "https://arxiv.org/abs/2408.06885",
         (("Aggregate", 2), None, None, None), (0, 2, "SGX RA", 0)),
        ("Hartmann · 2024", None,
         (("DFL", 2), None, None, None), (2, 2, "Simulated", 0)),
        ("ZKML · 2024", "https://doi.org/10.1145/3627703.3650088",
         (None, ("Inference", 2), None, None), (2, 0, 0, 0)),
        ("ZkAudit · 2024", "https://proceedings.mlr.press/v235/waiwitlikhit24a.html",
         (None, ("Audits", 2), None, None), (2, 0, 0, 0)),
        ("Balan et al. · 2025", "https://arxiv.org/abs/2503.22573",
         (("DFL", 1), ("Inference", 1), None, None), (1, 1, 0, 0)),
        ("AIR-02 · draft + demo", "https://www.ietf.org/archive/id/draft-tsyrulnikov-rats-attested-inference-receipt-02.html",
         (None, ("Receipts", 2), None, None), (0, 2, "Platform RA", 0)),
        ("VET · 2025", "https://arxiv.org/abs/2512.15892",
         (None, ("API trace", 2), ("Agent", 2), None), (2, 2, 0, 0)),
        ("Sello · 2026", "https://arxiv.org/abs/2606.04193",
         (None, None, ("Tools", 2), ("Receipts", 2)), (0, 0, 0, 0)),
        ("VITA-FL · this thesis", None,
         (("DFL", 2), ("Inference", 2), ("Agent", 2), ("Receipts", 2)), (0, 2, 2, 2)),
    )

    def marker(cx, cy, status, accent=DARK):
        if status:
            add_oval(slide, cx - .082, cy - .082, .164, .164,
                     accent if status == 2 else WHITE, accent, 1.5)
        else:
            add_line_segment(slide, cx - .07, cy, cx + .07, cy, MID, 1.4)

    for index, (label, url, stages, mechanisms) in enumerate(rows):
        y = 2.59 + index * .295
        cy = y + .14
        own = index == len(rows) - 1
        row_fill = RED_TINT if own else (LIGHT if index % 2 == 0 else WHITE)
        add_box(slide, .70, y, 11.94, .28, fill=row_fill, line=row_fill, radius=False, line_width=0)
        if own:
            add_box(slide, .70, y, .045, .28, fill=TU_RED, line=TU_RED, radius=False, line_width=0)
        name = add_text(slide, label, .83, y + .005, 2.43, .27, 11.4, TU_RED if own else DARK, own,
                        valign=MSO_ANCHOR.MIDDLE, margin=0)
        if url:
            name.text_frame.paragraphs[0].runs[0].hyperlink.address = url
        for i in range(3):
            if stages[i] and stages[i + 1]:
                add_arrow(slide, stage_x[i] + stage_w[i] + .015, cy,
                          stage_x[i + 1] - .015, cy,
                          TU_RED if own else DARK, 1.2, dashed=min(stages[i][1], stages[i + 1][1]) == 1)
        for i, stage in enumerate(stages):
            if stage is None:
                marker(stage_x[i] + stage_w[i] / 2, cy, 0)
                continue
            text, status = stage
            accent = TU_RED if own else stage_colors[i]
            chip = add_box(slide, stage_x[i], y + .0125, stage_w[i], .255,
                           fill=accent if status == 2 else WHITE, line=accent, line_width=1.1)
            chip.name = f"Literature: {label}: {text}"
            add_text(slide, text, stage_x[i], y + .0125, stage_w[i], .255,
                     10.8, WHITE if status == 2 else accent, True,
                     align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE, margin=0)
        for x, status in zip(mechanism_x, mechanisms):
            if isinstance(status, str):
                add_text(slide, status, x - .59, y + .005, 1.18, .27, 10.8, DARK,
                         align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE, margin=0)
            else:
                marker(x, cy, status, TU_RED if own else DARK)

    # A single readable legend keeps qualifications out of the table cells.
    for x, status, caption, width in (
        (2.48, 2, "Implemented", 1.45),
        (5.11, 1, "Discussed / framework", 2.65),
        (8.92, 0, "Not described", 1.75),
    ):
        marker(x, 6.07, status)
        add_text(slide, caption, x + .18, 5.92, width, .30, 11.5, DARK, valign=MSO_ANCHOR.MIDDLE, margin=0)

    add_note(slide,
        "Reading this slide: System coverage distinguishes DFL, inference, agents, and a "
        "transparency log. General training proofs do not automatically count as DFL; "
        "an execution transcript, provenance database, or model ledger does not automatically "
        "count as a transparency log for inference/tool statements. The columns are not an "
        "exhaustive capability list. Filled blocks/dots mean implemented or "
        "evaluated in the described prototype. Outlines mean discussed, proposed, or framework "
        "options. A dash means not described as a mechanism of the checked work, not proof of "
        "absence from every related implementation. ZKP includes the zero-knowledge proofs "
        "used by each system, including certificate or transcript proofs; it is not limited "
        "to ML computation. Proof scope remains specific to each row. "
        "Paper names link to primary sources. The representative selection is not a systematic "
        "literature review or a security ranking. Quote verification and RTMR3 replay are "
        "grouped under remote attestation as two selected checks, not an exhaustive definition "
        "of attestation. RTMR3 is specific to the TDX measurement path.\n\n"
        "Lee, Heiss et al., End-to-End Verifiable Decentralized Federated Learning (ICBC 2024), "
        "https://arxiv.org/html/2404.12623v1, sections V–VII: Groth16 zkSNARKs with ZoKrates cover "
        "registration and per-round signed-data provenance, device binding, and local update "
        "computation. A smart contract verifies local updates and performs aggregation. Their "
        "device attestation is not TEE remote attestation. End-to-end refers to the learning "
        "workflow; downstream inference and agent execution are not described.\n\n"
        "Ebrahimi, Sober, Hoang, Ileri, Sanders and Schulte, Blockchain-Based Federated Learning "
        "Utilizing Zero-Knowledge Proofs for Verifiable Training and Aggregation (IEEE Blockchain "
        "2024), pp. 54–63, https://doi.org/10.1109/Blockchain62396.2024.00017. The author's "
        "companion implementation, https://github.com/ElmiraEbrahimi/Veriblock-FL, supplies "
        "separate ZoKrates zk-SNARK circuits for local training and global aggregation, with "
        "Solidity proof verification. Model parameters remain off chain; the ledger holds "
        "hashes and global-model IPFS references. FederatedModel.sol, "
        "getStakeWinnersAndSelectedAggregatorIndex, and devices/middleware/aggregator_selection.py "
        "implement changing off-chain aggregators. Hence DFL and ZKP are filled as implemented. "
        "The checked implementation does not describe a served inference/agent lifecycle, "
        "a tool/inference-receipt transparency log, TEEs, quote verification or RTMR3 replay. "
        "A model ledger is not the receipt transparency log meant by this slide. Both training "
        "and aggregation are already verifiable here; VITA-FL's distinction is its TEE/remote-"
        "attestation mechanism and its continuation to inference, agent use and receipts. "
        "The classification was checked against the public companion implementation; the "
        "publisher full text was inaccessible, so no paper section numbers or exact historical "
        "code correspondence are asserted.\n\n"
        "Voltran (2024), https://arxiv.org/html/2408.06885v1, sections III-C, IV, VII: Intel SGX "
        "aggregation with remote attestation and encrypted channels; enclave-result signatures "
        "are checked on chain. A trusted committee provisions signing keys. The focus is "
        "confidential distributed aggregation within FL, not later inference or agent use. "
        "On-chain result-signature checks are not on-chain RA. The Quote verification cell "
        "reads SGX RA because RA is used and evaluated (Appendix D-C), but concrete quote fields, "
        "certificate/collateral checks, and verifier implementation are not specified. This "
        "is not a claim that Voltran omits quote verification. Its model ledger is not a "
        "separate tool/inference-receipt transparency log. No TDX/RTMR3 replay is described.\n\n"
        "Hartmann (2024), Advancing the Efficiency of Verifiable Decentralized Federated Learning, "
        "TU Berlin master's thesis: the original implementation is present in the vita-fl Git "
        "history at 3362a185929b355b69099f2819b8b42638055957 (Johann Hartmann, 5 October 2024). "
        "Worker training and aggregation use TEEs with smart-contract coordination. RISC Zero "
        "proves certificate-signature verification in the simulated attestation path, not ML "
        "training or aggregation; the filled ZKP marker refers to that certificate proof. "
        "In remote_attestation/methods/guest/src/bin/verify_ar.rs, "
        "lines 74–142 parse CA/VCEK certificates, verify an RSA-PSS/SHA-384 signature, and "
        "commit a Boolean result; the guest does not consume a hardware report or app measurements. "
        "remote_attestation/apps/src/bin/publisher.rs, lines 167–174, selects Groth16 proving. "
        "The Simulated cell distinguishes this registration design from authenticated production "
        "hardware quotes. cloud_setup/terraform/main.tf configures an AMD SEV-SNP VM. No "
        "downstream inference/agent/transparency-log path or RTMR3 replay is described in the "
        "examined predecessor. The original thesis PDF and a public publication URL were not "
        "available locally; the bibliography entry is hartmann2024dfl.\n\n"
        "ZKML (EuroSys 2024), https://ddkang.github.io/papers/2024/zkml-eurosys.pdf, sections 2–4 "
        "and 8–9: implemented halo2-based compiler and inference-proof optimizations. Table 2 also "
        "lists CNN training as supported; section 4.4 explicitly makes training proofs a "
        "non-focus. Thus the single inference stage on this slide does not mean training is "
        "impossible. Attested sensors are mentioned as a combinable input source, not a deployed "
        "TEE/TDX inference attestation mechanism.\n\n"
        "ZkAudit, Trustless Audits without Revealing Data or Models (ICML 2024), "
        "https://proceedings.mlr.press/v235/waiwitlikhit24a.html and "
        "https://arxiv.org/html/2404.04500v1, sections 3–6: ZkAudit-T proves training with "
        "committed data/weights; ZkAudit-I proves later audit functions using the same bindings, "
        "including inference in the implemented audits. This is an implemented training-to-audit "
        "lifecycle link, although generic training is not a column in this version of the slide. "
        "There is no agent or DFL coordination protocol. The Inference cell reads Audits to "
        "distinguish this application from a served native inference API. Published commitments "
        "do not themselves establish a transparency log.\n\n"
        "Balan et al., A Framework for Cryptographic Verifiability of End-to-End AI Pipelines "
        "(2025), https://arxiv.org/html/2503.22573v1, sections 3–5: conceptual linkage of data, "
        "training, evaluation, inference, and unlearning through signatures, commitments, and "
        "ZKPs. Section 4.2.2 explicitly discusses decentralized FL approaches, including PTDFL; "
        "the outlined DFL cell refers to this discussion, not an own implemented DFL protocol. "
        "The slide shows selected parts of that broader lifecycle. This is a framework and "
        "tooling analysis, not a new fully implemented pipeline. The outlined ZKP marker "
        "denotes the framework's discussion and mapping of existing ZKP approaches. The outlined "
        "TEE marker refers only to related verifiable-database techniques discussed in section "
        "5.1; no own remote-attestation or image-measurement verification pipeline is specified. "
        "The discussed DECORAIT blockchain metadata registry is not a specified transparency "
        "service with verified inclusion receipts in this framework.\n\n"
        "AIR revision 02, Attested Inference Receipt: A COSE/CWT Profile for Confidential AI "
        "Inference, https://www.ietf.org/archive/id/"
        "draft-tsyrulnikov-rats-attested-inference-receipt-02.html, sections 7.2–7.3 and 14: "
        "an Internet-Draft with a demonstration implementation, EphemeralML. Filled cells refer "
        "to the reported receipt emission/verification and TEE execution, not to a finalized "
        "standard. The Platform RA cell summarizes platform-specific attestation: full "
        "single-document AIR provenance is implemented for Nitro; TDX/GCP evidence remains "
        "split across boot-time and transport/platform verification paths. Full single-document "
        "TDX validation is future work. The profile explicitly specifies TDX/DCAP quote checks, "
        "and can carry RTMR3 measurements, but does not specify replay of a dstack application "
        "event log. An external transparency log is outside the current profile (section 11.4). "
        "No DFL or agent workflow is established by the receipt format.\n\n"
        "VET Your Agent (2025 preprint), https://arxiv.org/html/2512.15892v1, sections 6–10 and "
        "Appendix A: framework plus evaluated implementation. TLSNotary/Web Proofs bind API "
        "transcripts; VeriTrade combines a Claude API trace with a TEE proxy. A self-hosted "
        "Intel TDX notary is evaluated. The filled ZKP marker refers to interactive ZK proofs "
        "inside TLSNotary/MPC-TLS for TLS records and plaintext, confirmed in the pinned "
        "alpha.12 verifier: https://github.com/tlsnotary/tlsn/blob/v0.1.0-alpha.12/"
        "crates/verifier/src/lib.rs#L253. Exported Web Proofs rely on the notary; they do not "
        "prove LLM inference arithmetic. SNARK/STARK computation proofs remain framework "
        "options. RA is discussed, but concrete quote/certificate/app-policy verification and "
        "RTMR3/dstack replay are not specified. This does not mean VET never uses attestation. "
        "Locally collected traces are not an append-only transparency log with inclusion "
        "proofs; selective-disclosure and freshness limitations remain.\n\n"
        "Sello / Figuera (2026), Notarized Agents: Receiver-Attested Confidential Receipts for "
        "AI Agent Actions, https://arxiv.org/html/2606.04193v1, sections 4, 6–7: the receiving "
        "service signs owner-encrypted tool receipts and publishes them to a transparency log. "
        "The reference implementation and cryptographic microbenchmarks use a local mock log; "
        "hosted-log submission latency is not measured first-party. Filled cells describe this "
        "implemented receipt lifecycle, not a production deployment or proof of all agent "
        "reasoning. Receiver-attested means service signatures, not TEE remote attestation. "
        "Suppression before a call reaches the receiver and receiver collusion remain outside "
        "the guarantee. The protocol does not by itself verify ML inference arithmetic.\n\n"
        "VITA-FL: native training, aggregation, and inference use TEEs and bound evidence "
        "rather than ZK proofs of those ML computations. The evaluated runtime also uses no "
        "ZK proof for admission: AutomataDcapTdxV4Attestation.sol rejects "
        "verifyAndAttestWithZKProof with ZK_Verification_Not_Supported, and DeviceRegistry.sol "
        "calls verifyAndAttestOnChainWithRtmr3EventLog. The ZKP dash concerns this operational "
        "prototype, not the thesis's discussion of explored alternatives. Full TDX/DCAP quote-signature, "
        "certificate, QE, and TCB verification occurs at admission. The image policy parses "
        "the exact app_compose preimage, derives its compose hash and immutable image digest, "
        "checks the approved image/base-runtime policy, and replays the ordered RTMR3 event "
        "chain against the authenticated quote. RTMR3 alone does not identify an image, and "
        "replay alone does not authenticate a quote. This dstack/TDX-specific mechanism is "
        "an implementation distinction, not a general security advantage over SGX or ZKPs. "
        "See https://docs.phala.com/phala-cloud/attestation/verify-your-application. "
        "For each inference the agent verifies signed AIR bindings and RTMR3 consistency, "
        "but does not authenticate the quote signature or validate the DCAP certificate/"
        "collateral chain: "
        "dcap_collateral_verified is false. It relies on prior receiver admission and the "
        "registered receipt key. The Agent stage means authenticated tool receipts, deterministic "
        "model resolution, and recorded inference evidence, not a proof of all LLM reasoning. "
        "The Transparency Log cell refers to receiver-published Sello-style tool receipts "
        "and inclusion checks, not the training ledger alone. This part builds on existing "
        "work: Sello, https://arxiv.org/abs/2606.04193, and the SCITT architecture, "
        "https://www.rfc-editor.org/rfc/rfc9943.html. "
        "Local code references: "
        "vita-fl/smart_contracts/src/attestation/AutomataDcapTdxV4Attestation.sol and "
        "vita-fl/agent/tee_inference_client.py.\n\n"
        "Technical background references: SCITT / RFC 9943, "
        "https://www.rfc-editor.org/rfc/rfc9943.html, defines signed statements, registration "
        "policy, verifiable data structures, and inclusion receipts. It is a transparency "
        "architecture rather than a DFL/agent system. Phala/dstack application verification, "
        "https://docs.phala.com/phala-cloud/attestation/verify-your-application, supplies the "
        "technical precedent for quote authentication, manifest/digest policy, and RTMR3 replay. "
        "VITA-FL applies those mechanisms; it does not introduce RTMR3 image binding.\n\n"
        "Takeaway: lifecycle connections already exist. VITA-FL studies an attestation-based "
        "DFL-to-inference integration with agent evidence and concrete image-policy checks. "
        "No first-system claim, no exhaustive research-gap proof, and no measured TEE-vs-ZKP "
        "performance advantage follow from this comparison. Sources checked 20 September 2026."
    )
    return slide


def slide_fl_dfl_roles(prs):
    """Compare coordinator placement and introduce the two training roles."""
    slide = new_content_slide(
        prs,
        7,
        "FL and DFL: who trains, who coordinates?",
        "Federated learning · Decentralized coordination · Roles and responsibilities",
    )

    for x, heading, subtitle in (
        (0.76, "Centrally coordinated FL", "Permanent central coordinator"),
        (6.89, "DFL used in VITA-FL", "Each participant can take the aggregator role"),
    ):
        add_box(slide, x, 1.53, 5.68, 2.80, fill=WHITE, line=BORDER, line_width=0.8)
        add_text(slide, heading, x + 0.19, 1.69, 5.30, 0.29, 16, DARK, True, align=PP_ALIGN.CENTER)
        add_text(slide, subtitle, x + 0.19, 2.08, 5.30, 0.24, 12.5 if x > 6 else 11.5, DARK, bold=x > 6, align=PP_ALIGN.CENTER)

    def role_node(x, y, w, text, aggregator=False):
        accent, fill = (TU_RED, RED_TINT) if aggregator else (GREEN, GREEN_TINT)
        add_box(slide, x, y, w, 0.52, fill=fill, line=accent, line_width=1.05)
        add_text(slide, text, x + 0.06, y + 0.035, w - 0.12, 0.43, 11, accent, True, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE, margin=0)

    def model_exchange(worker_x, worker_y, aggregator_x, aggregator_y):
        dx, dy = aggregator_x - worker_x, aggregator_y - worker_y
        length = (dx * dx + dy * dy) ** 0.5
        ox, oy = -dy / length * 0.045, dx / length * 0.045
        add_arrow(slide, worker_x + ox, worker_y + oy, aggregator_x + ox, aggregator_y + oy, DARK, 1.0)
        add_arrow(slide, aggregator_x - ox, aggregator_y - oy, worker_x - ox, worker_y - oy, DARK, 1.0)

    # The fixed server is separate from the three local-training participants.
    for worker_x in (1.66, 3.60, 5.54):
        model_exchange(worker_x, 3.50, 3.60, 2.98)
    role_node(2.65, 2.46, 1.90, "Fixed server\nAggregator", aggregator=True)
    for letter, worker_x in zip(("A", "B", "C"), (1.66, 3.60, 5.54)):
        role_node(worker_x - 0.64, 3.50, 1.28, f"Worker {letter}")

    # Keep participants in the same positions; the red role moves each round.
    for round_number, (cx, aggregator) in enumerate(zip((7.96, 9.73, 11.50), "ABC"), start=1):
        add_text(slide, f"Round {round_number}", cx - 0.73, 2.53, 1.46, 0.25, 12.5, DARK, True, align=PP_ALIGN.CENTER)
        participants = {"A": (cx, 3.07), "B": (cx - 0.40, 3.65), "C": (cx + 0.40, 3.65)}
        ax, ay = participants[aggregator]
        for label, (px, py) in participants.items():
            if label != aggregator:
                add_line_segment(slide, ax, ay, px, py, MID, 1.4)
        for label, (px, py) in participants.items():
            active = label == aggregator
            accent, fill = (TU_RED, TU_RED) if active else (GREEN, GREEN_TINT)
            add_oval(slide, px - 0.23, py - 0.23, 0.46, 0.46, fill, accent, 1.4)
            add_text(slide, label, px - 0.23, py - 0.23, 0.46, 0.46, 14, WHITE if active else GREEN, True, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE, margin=0)
        add_text(slide, f"{aggregator} aggregates", cx - 0.77, 4.02, 1.54, 0.24, 12, TU_RED, True, align=PP_ALIGN.CENTER, margin=0)
        if round_number < 3:
            add_arrow(slide, cx + 0.69, 3.30, cx + 1.07, 3.30, DARK, 1.6)

    add_text(
        slide, "Both keep training records local and exchange model parameters.",
        0.91, 4.47, 11.55, 0.28, 13, DARK, True, align=PP_ALIGN.CENTER,
    )

    roles = (
        (0.76, "WORKER · LOCAL TRAINING", GREEN, GREEN_TINT, (
            "Start from the shared global model.",
            "Train on local data → local model.",
            "Submit the local model / parameter update.",
        )),
        (6.89, "AGGREGATOR · SHARED MODEL", TU_RED, RED_TINT, (
            "Collect and check contributions.",
            "Combine the accepted local models.",
            "Publish the next global model.",
        )),
    )
    for x, heading, accent, fill, tasks in roles:
        add_box(slide, x, 4.91, 5.68, 1.14, fill=fill, line=accent, line_width=0.8)
        add_text(slide, heading, x + 0.19, 5.03, 5.29, 0.21, 11.5, accent, True)
        for index, task in enumerate(tasks, start=1):
            add_text(slide, f"{index}. {task}", x + 0.19, 5.29 + (index - 1) * 0.22, 5.29, 0.21, 11.5, DARK)
    add_note(
        slide,
        "Federated learning lets participants train a model together while retaining their records "
        "locally. DFL is a decentralized form of FL; the left diagram specifically shows centrally "
        "coordinated FL. A global model is the shared starting model of a round. A worker is the "
        "computing process at a participant, for example a hospital. It starts from that model, trains "
        "on local records, and submits its local parameter set or update. The aggregator collects and "
        "checks contributions, combines accepted local models, and publishes the next global model. "
        "The arrows on the left represent model exchange, never raw patient records. A permanent "
        "central server holds the coordination role; continued progress depends on it or an explicit "
        "replacement mechanism. On the right, the same participants A, B, and C appear in three "
        "successive rounds. Red identifies the aggregator: first A, then B, then C. The other participants "
        "perform local training. The horizontal arrows indicate progression between rounds. This is an "
        "illustrative assignment sequence, not a mandatory round-robin schedule. Weighted selection can "
        "also choose the same aggregator in consecutive rounds. Each eligible participant "
        "can assume the role under VITA-FL's shared contract rules. A stalled aggregator "
        "can be replaced through the recovery protocol. Rotation alone does not establish availability: "
        "decentralization requires agreement and recovery rules and retains infrastructure dependencies. "
        "Other DFL designs use peer-to-peer mixing instead of a single rotating aggregator. In the "
        "prototype, the current aggregator does not train during its aggregation round: six participants "
        "therefore provide five local models. Contribution checks enforce protocol rules; they do not "
        "establish that training data are benign. Sources: thesis Chapter 2, Section 2.1; McMahan et al., "
        "AISTATS 2017, https://arxiv.org/abs/1602.05629; Martínez Beltrán et al., IEEE Communications "
        "Surveys & Tutorials 2023, https://doi.org/10.1109/COMST.2023.3315746.",
    )
    return slide


def slide_lifecycle(prs):
    """Place the approved F3 native shapes under the main deck's title/footer."""
    approved = Presentation(ASSETS / "lifecycle-f3.pptx")
    assert len(approved.slides) == 1
    slide = new_content_slide(prs, 9, "VITA-FL: from training to verifiable use", "")
    for shape in approved.slides[0].shapes:
        # The approved asset includes its proposal title/footer. Copy only the
        # editable diagram so numbering, date, and domain chips remain standard.
        if shape.top < Inches(1.43) or shape.top + shape.height > Inches(6.28):
            continue
        element = deepcopy(shape.element)
        assert not element.xpath(".//a:blip | .//a:hlinkClick | .//a:hlinkMouseOver"), \
            "Lifecycle diagram must contain only self-contained native shapes"
        for properties in element.xpath(".//p:cNvPr"):
            properties.set("id", str(slide.shapes._next_shape_id))
        slide.shapes._spTree.insert_element_before(element, "p:extLst")
    add_note(
        slide,
        "Lifecycle overview before the detailed architecture. Workers train locally and "
        "send encrypted local updates directly to the current aggregator over authenticated "
        "HTTPS. The aggregator combines the updates, stores the encrypted global-model "
        "bundle in IPFS, and finalizes its references on blockchain. Workers resolve the "
        "finalized reference and load the model from IPFS for the next training round. "
        "The Global model segment therefore represents both publication and retrieval. "
        "The blockchain also coordinates rounds and records accepted submission commitments; "
        "those interactions are abstracted here. Aggregation is an assigned participant role, "
        "and selection can choose the same participant in successive rounds.\n\n"
        "A finalized model can also be used for inference. The Published model arrow "
        "summarizes the receiver resolving its authoritative blockchain reference and "
        "retrieving the corresponding IPFS bundle. The agent invokes the attested inference "
        "service through MCP and receives its result. The receiver publishes the tool "
        "receipt to the separate transparency log. Domain evidence binds the model, "
        "inference input, and output; log inclusion alone does not verify computation. "
        "Admission and retained signing identities underpin execution; this overview "
        "does not imply a fresh full DCAP check for every call. No inference-to-training "
        "feedback is implied. The circle groups functions, not a shared TEE or trust boundary.\n\n"
        "Prototype references: vita-fl/dfl/node_server/src/server.ts:463-533,672-702,"
        "2110-2180,2313-2330; vita-fl/dfl/node_server/src/ipfs.ts:315-346,380-435; "
        "vita-fl/smart_contracts/src/core/GMStorage.sol:180-248; "
        "vita-fl/smart_contracts/src/core/AggregatorSelection.sol:171-195.",
    )
    return slide


def slide_image_policy(prs):
    """Use the approved editable CI/CD diagram independently of its concept folder."""
    approved = Presentation(ASSETS / "ci-cd-image-policy.pptx")
    assert len(approved.slides) == 1
    source = approved.slides[0]
    slide = new_content_slide(prs, 13, "From worker image to on-chain policy", "")
    for shape in source.shapes:
        if shape.top < Inches(1.43) or shape.top + shape.height > Inches(6.28):
            continue
        element = deepcopy(shape.element)
        assert not element.xpath(".//a:blip | .//a:hlinkClick | .//a:hlinkMouseOver"), \
            "Image-policy diagram must contain only self-contained native shapes"
        for properties in element.xpath(".//p:cNvPr"):
            properties.set("id", str(slide.shapes._next_shape_id))
        slide.shapes._spTree.insert_element_before(element, "p:extLst")
    add_note(slide, source.notes_slide.notes_text_frame.text)
    return slide


def slide_architecture(prs):
    """Draw the approved architecture with shared blockchain/IPFS infrastructure."""
    green, purple, blue = "207548", "7446A6", "1764A1"
    tints = {green: "EDF6F0", purple: "F3EEF8", blue: "EDF4FA"}

    def text(value, x, y, w, h, size=12, color=DARK, bold=False, center=False):
        return add_text(
            slide, value, x, y, w, h, size, color, bold,
            align=PP_ALIGN.CENTER if center else PP_ALIGN.LEFT,
            valign=MSO_ANCHOR.MIDDLE, margin=0,
        )

    def panel(x, y, w, h, color):
        return add_box(slide, x, y, w, h, fill=tints[color], line=color, line_width=1.1)

    def card(name, heading, detail, x, y, w, h, color, heading_size=12):
        shape = add_box(slide, x, y, w, h, fill=WHITE, line=color, line_width=1.2)
        shape.name = name
        text(heading, x + .10, y + .10, w - .20, .30, heading_size, color, True, True)
        text(detail, x + .10, y + .51, w - .20, h - .60, 10.5, DARK, False, True)
        return shape

    def route(name, points, color, width=1.8):
        for index, (start, end) in enumerate(zip(points, points[1:]), start=1):
            shape = add_line_segment(
                slide, *start, *end, color, width, arrow=index == len(points) - 1,
            )
            shape.name = f"{name} / {index}"

    slide = new_content_slide(prs, 6, "VITA-FL: two responsibility blocks", "")

    panel(.63, 1.65, 3.40, 3.50, green)
    panel(4.25, 1.65, 2.66, 3.95, purple)
    panel(7.13, 1.65, 5.57, 3.50, blue)

    # The overlapping frames include shared infrastructure in both functional
    # groups; they do not represent deployment or attestation boundaries.
    for name, x1, y1, x2, y2 in (
        ("DFL and infrastructure", .48, 1.51, 6.99, 5.74),
        ("Infrastructure and agent", 4.14, 1.42, 12.86, 5.88),
    ):
        corners = [(x1, y1), (x2, y1), (x2, y2), (x1, y2), (x1, y1)]
        for index, (start, end) in enumerate(zip(corners, corners[1:]), start=1):
            line = add_line_segment(slide, *start, *end, "000000", 1.1, dashed=True)
            line.name = f"Shared group frame: {name} / {index}"

    text("DFL BLOCK", .87, 1.88, 2.90, .30, 13.5, green, True)
    text("BLOCKCHAIN / IPFS", 4.45, 1.88, 2.26, .30, 11.5, purple, True, True)
    text("AGENT AND INFERENCE BLOCK", 7.36, 1.88, 5.10, .30, 13.5, blue, True)

    card("Data", "DATA", "Signed\ninput", .87, 2.56, 1.24, 1.15, green)
    card("Worker", "WORKER TEE", "Attested\ntraining", 2.37, 2.56, 1.39, 1.15, green, heading_size=10.5)
    card("Ledger", "LEDGER", "Finalized\nmodel reference", 4.48, 2.56, 2.20, 1.15, purple)
    card("IPFS", "IPFS", "Signed, encrypted\nmodel bundle", 4.48, 4.03, 2.20, 1.20, purple)
    card("Receiver", "RECEIVER TEE", "Resolve\nand infer", 7.41, 2.56, 2.11, 1.15, blue)
    card("MCP", "MCP", "Bounded\ntools", 9.82, 2.56, 1.14, 1.15, blue)
    card("Log", "LOG", "Receipts /\nevidence", 11.25, 2.56, 1.18, 1.15, blue)

    route("Data to worker", [(2.14, 3.135), (2.34, 3.135)], green, 1.4)
    route("Publish reference", [(3.79, 3.135), (4.44, 3.135)], green)
    route("Publish artifacts", [(3.065, 3.75), (3.065, 4.63), (4.44, 4.63)], green)
    route("Ledger to receiver", [(6.71, 3.135), (7.37, 3.135)], purple, 2.2)
    route("IPFS to receiver", [(6.71, 4.63), (7.06, 4.63), (7.06, 3.46), (7.37, 3.46)], purple, 2.2)
    route("Receiver to MCP", [(9.55, 3.135), (9.78, 3.135)], blue, 1.4)
    route("MCP to log", [(10.99, 3.135), (11.21, 3.135)], blue, 1.4)

    text("Produces the model", .87, 5.32, 2.90, .27, 11.5, green, True, True)
    text("The agent orchestrates tools and evidence.", 7.44, 5.31, 4.96, .30, 12, blue, True, True)
    add_note(
        slide,
        "Green denotes model production; purple denotes blockchain and IPFS; "
        "blue denotes agent orchestration, inference and evidence logging. "
        "The DFL and agent/inference responsibilities remain separate; shared infrastructure "
        "is not a third execution responsibility. These boxes are functional groups, not "
        "deployment or attestation boundaries.\n\n"
        "Ledger -> Receiver TEE supplies the finalized model reference: CIDs, round and "
        "publisher key. IPFS -> Receiver TEE supplies the signed, encrypted model bundle "
        "and associated artifacts. The receiver independently resolves, retrieves and verifies "
        "them. Purple arrowheads depict incoming information; the receiver initiates retrieval. "
        "The ledger does not upload model bytes to IPFS. DFL publication arrows summarize "
        "the active aggregator publishing artifacts and their references.\n\n"
        "Local code references: vita-fl/tee_inference/service/model_source.py:218; "
        "vita-fl/agent/blockchain_source.py:354,544. "
        "The MCP/log chain is the existing slide's compact view of tools and evidence, "
        "not a detailed call-sequence diagram.",
    )
    return slide


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


def slide_phala_attestation(prs):
    from attestation_slides import verification
    return verification(prs, sys.modules[__name__])


def slide_dstack_keys(prs):
    """Place the approved D actor map using its independent editable asset."""
    approved = Presentation(ASSETS / "dstack-key-usage-d.pptx")
    assert len(approved.slides) == 1
    source = approved.slides[0]
    slide = new_content_slide(prs, 15, "Key use at the system interfaces", "")
    for shape in source.shapes:
        if shape.top < Inches(1.43) or shape.top + shape.height > Inches(6.28):
            continue
        element = deepcopy(shape.element)
        assert not element.xpath(".//a:blip | .//a:hlinkClick | .//a:hlinkMouseOver"), \
            "Key-use diagram must contain only self-contained native shapes"
        for properties in element.xpath(".//p:cNvPr"):
            properties.set("id", str(slide.shapes._next_shape_id))
        slide.shapes._spTree.insert_element_before(element, "p:extLst")
    add_note(slide, source.notes_slide.notes_text_frame.text)
    return slide


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
    """Use the approved actor flow; arrows define the sequence without step numbers."""
    approved = Presentation(ASSETS / "aggregation-round-a.pptx")
    assert len(approved.slides) == 1
    source = approved.slides[0]
    slide = new_content_slide(prs, 18, "Who does what during aggregation?", "")
    for shape in source.shapes:
        if shape.top < Inches(1.43) or shape.top + shape.height > Inches(6.28):
            continue
        element = deepcopy(shape.element)
        assert not element.xpath(".//a:blip | .//a:hlinkClick | .//a:hlinkMouseOver"), \
            "Aggregation diagram must contain only self-contained native shapes"
        for properties in element.xpath(".//p:cNvPr"):
            properties.set("id", str(slide.shapes._next_shape_id))
        slide.shapes._spTree.insert_element_before(element, "p:extLst")
    add_note(slide, source.notes_slide.notes_text_frame.text)
    return slide


def slide_original_hybrid_r(prs):
    slide = new_content_slide(
        prs,
        13,
        "Original Hybrid-R: several rules, one aggregate",
        "Related work by Yue et al. · one central server, not several aggregator nodes",
    )

    add_box(slide, 0.55, 2.05, 2.18, 2.78, fill=BLUE_TINT, line=BLUE, radius=True, line_width=1.4)
    add_text(slide, "ONE CENTRAL SERVER", 0.76, 2.33, 1.76, 0.25, 10.0, BLUE, True, align=PP_ALIGN.CENTER)
    add_text(slide, "same client-update\ncollection", 0.76, 3.02, 1.76, 0.58, 13.0, DARK, True, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)
    add_text(slide, "every rule receives\nthe same inputs", 0.76, 4.08, 1.76, 0.42, 8.8, DARK, align=PP_ALIGN.CENTER)

    add_arrow(slide, 2.84, 3.43, 3.24, 3.43, BLUE, 1.8)
    add_arrow(slide, 8.35, 3.43, 8.76, 3.43, PURPLE, 1.8)

    add_box(slide, 3.25, 1.42, 5.08, 4.45, fill=LIGHT, line=MID, radius=True, line_width=1.2)
    add_text(slide, "PORTFOLIO OF SERVER-SIDE DEFENSE FUNCTIONS", 3.52, 1.69, 4.54, 0.25, 9.5, DARK, True, align=PP_ALIGN.CENTER)
    methods = (
        "BALANCE",
        "CENTERED CLIPPING",
        "FREQFED",
        "SIGNGUARD",
        "KRUM / MULTI-KRUM",
        "DIVIDE-AND-CONQUER",
        "TRIMMED MEAN",
        "COORDINATE MEDIAN",
    )
    for index, label in enumerate(methods):
        column = index % 2
        row = index // 2
        x = 3.55 + column * 2.26
        y = 2.18 + row * 0.73
        accent = (BLUE, PURPLE, ORANGE, GREEN)[row]
        tint = (BLUE_TINT, PURPLE_TINT, ORANGE_TINT, GREEN_TINT)[row]
        add_box(slide, x, y, 2.16, 0.54, fill=tint, line=accent, radius=True, line_width=1.0)
        add_text(slide, label, x + 0.10, y + 0.16, 1.96, 0.20, 8.0, accent, True, align=PP_ALIGN.CENTER, margin=0)
    add_text(slide, "each function produces one aggregate model", 3.62, 5.28, 4.34, 0.23, 9.2, DARK, True, align=PP_ALIGN.CENTER)

    add_box(slide, 8.78, 1.42, 4.03, 4.45, fill=PURPLE_TINT, line=PURPLE, radius=True, line_width=1.3)
    add_text(slide, "ONE CANDIDATE PER RULE", 9.03, 1.76, 3.53, 0.24, 10.0, PURPLE, True, align=PP_ALIGN.CENTER)
    add_box(slide, 9.14, 2.34, 3.31, 0.74, fill=WHITE, line=PURPLE, radius=True, line_width=1.0)
    add_text(slide, "evaluate every model on the\nsame reference dataset", 9.36, 2.50, 2.87, 0.42, 9.5, DARK, True, align=PP_ALIGN.CENTER)
    add_arrow(slide, 10.80, 3.16, 10.80, 3.52, PURPLE, 1.6)
    add_box(slide, 9.14, 3.58, 3.31, 0.74, fill=WHITE, line=TU_RED, radius=True, line_width=1.0)
    add_text(slide, "compare one empirical-risk\nmeasure across all candidates", 9.36, 3.74, 2.87, 0.42, 9.2, DARK, True, align=PP_ALIGN.CENTER)
    add_arrow(slide, 10.80, 4.40, 10.80, 4.76, TU_RED, 1.6)
    add_box(slide, 9.14, 4.82, 3.31, 0.66, fill=GREEN_TINT, line=GREEN, radius=True, line_width=1.2)
    add_text(slide, "ADOPT LOWEST-RISK MODEL", 9.36, 5.03, 2.87, 0.22, 9.3, GREEN, True, align=PP_ALIGN.CENTER)

    add_text(
        slide,
        "“Hybrid” = several aggregation rules · “R” = reference data · not a multi-aggregator topology",
        1.05,
        6.04,
        11.23,
        0.25,
        10.3,
        TU_RED,
        True,
        align=PP_ALIGN.CENTER,
    )

    add_note(
        slide,
        "This slide describes the original Hybrid-R approach from Yue and co-authors as related work. One central "
        "federated-learning server receives one collection of client updates and runs every defense function in its "
        "portfolio over that same collection. The functions include Balance, Centered Clipping, FreqFed, SignGuard, "
        "Krum and Multi-Krum, Divide-and-Conquer, Trimmed Mean, and coordinate-wise Median. Each function produces "
        "a complete aggregate model. The server evaluates all resulting models with the same empirical-risk measure "
        "on the same reference dataset and adopts the model with the lowest risk. Hybrid-R therefore selects among "
        "aggregate results; it does not assign a different metric to each client update and does not require several "
        "aggregator nodes. The rules could be executed in parallel, but that is only an implementation optimization. "
        "This related-work mechanism is not the active VITA-FL aggregation path; VITA-FL uses the single equal-weight "
        "FedAvg rule shown on the preceding slide.",
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


def apply_sello_air_asset(slide, page_number: int):
    """Populate one slide from the approved editable Sello/AIR comparison."""
    approved = Presentation(ASSETS / "sello-air-a.pptx")
    assert len(approved.slides) == 1
    source = approved.slides[0]
    for shape in list(slide.shapes):
        remove_shape(shape)
    add_content_title(
        slide, "Sello and AIR: two layers of evidence",
        "CURRENT VITA-FL IMPLEMENTATION", page_number,
    )
    add_domain_navigation(slide, page_number, active_domains={"Agent"})
    for shape in source.shapes:
        # Include the subtitle, native diagram, white source band and citations.
        # Keep the main deck's own title, page number, navigation and footer.
        if shape.top < Inches(1.43) or shape.top + shape.height > Inches(6.71):
            continue
        element = deepcopy(shape.element)
        assert not element.xpath(".//a:blip"), \
            "Sello/AIR diagram must contain only native editable shapes"
        for node in element.iter():
            for attribute, value in list(node.attrib.items()):
                if attribute.startswith("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"):
                    relationship = source.part.rels[value]
                    assert relationship.is_external, "Only external source hyperlinks are expected"
                    node.set(attribute, slide.part.relate_to(
                        relationship.target_ref, relationship.reltype, is_external=True,
                    ))
        for properties in element.xpath(".//p:cNvPr"):
            properties.set("id", str(slide.shapes._next_shape_id))
        slide.shapes._spTree.insert_element_before(element, "p:extLst")
    notes = source.notes_slide.notes_text_frame.text.replace(
        "COMBINED ASSURANCE VARIANT A", "SELLO AND AIR — TASKS AND GUARANTEES",
    ).replace(
        "Main deck is kept as a separate artifact.",
        "Approved comparison integrated as Page 20 of the main presentation.",
    )
    add_note(slide, notes)
    return slide


def slide_sello_protocol(prs):
    """Use the approved comparison of Sello and AIR responsibilities."""
    slide = prs.slides.add_slide(prs.slide_masters[1].slide_layouts[0])
    return apply_sello_air_asset(slide, len(prs.slides))


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
    evidence = load_authoritative_evaluation()
    manifest = evidence["manifest"]
    training = manifest["training"]
    gas_accounting = manifest["gas_accounting"]["total"]
    inference = manifest["tee_inference"]
    slide = new_content_slide(
        prs,
        19,
        "One end-to-end Phala FedAvg run",
        "Current equal-weight FedAvg path · six worker TEEs · two infrastructure TEEs · 24 federated rounds",
    )

    # A single horizontal protocol line makes the evaluated path explicit.
    stages = [
        (1.20, "6", "TEE WORKERS", BLUE, BLUE_TINT),
        (3.40, "24/24", "ROUNDS", GREEN, GREEN_TINT),
        (5.60, "5", "UPDATES / ROUND", ORANGE, ORANGE_TINT),
        (7.80, "120", "TRAINS + TRANSFERS", PURPLE, PURPLE_TINT),
        (10.00, "0", "ABORTED ATTEMPTS", TU_RED, RED_TINT),
        (12.05, "0", "GAP RECOVERIES", DARK, LIGHT),
    ]
    for first, second in zip(stages, stages[1:]):
        add_arrow(slide, first[0] + 0.62, 2.35, second[0] - 0.62, 2.35, MID, 1.5)
    for x, value, label, accent, fill in stages:
        add_oval(slide, x - 0.56, 1.78, 1.12, 1.12, fill, accent, 1.8)
        add_text(slide, value, x - 0.47, 2.08, 0.94, 0.35, 16.5 if len(value) < 4 else 12.0, accent, True, align=PP_ALIGN.CENTER, margin=0)
        add_text(slide, label, x - 0.78, 3.02, 1.56, 0.34, 8.0, DARK, True, align=PP_ALIGN.CENTER)

    add_box(slide, 0.68, 3.62, 3.78, 1.48, fill=BLUE_TINT, line=BLUE, line_width=1.3)
    add_text(slide, "RUN CLOCK", 0.94, 3.86, 1.16, 0.22, 10.0, BLUE, True)
    add_text(slide, f"{training['first_to_last_evaluation_seconds'] / 60:.2f} min", 0.94, 4.21, 2.98, 0.30, 18.0, DARK, True)
    add_text(slide, f"{training['mean_evaluation_interval_seconds']:.2f} s mean evaluation interval", 0.94, 4.65, 3.10, 0.22, 9.2, DARK)

    add_box(slide, 4.78, 3.62, 3.78, 1.48, fill=PURPLE_TINT, line=PURPLE, line_width=1.3)
    add_text(slide, "ROUND-25 TEE INFERENCE", 5.04, 3.86, 2.88, 0.22, 10.0, PURPLE, True)
    add_text(slide, f"{inference['duration_microseconds'] / 1000:.3f} ms", 5.04, 4.21, 1.54, 0.30, 18.0, DARK, True)
    add_text(slide, f"{inference['quote_bytes']:,} B quote · {inference['rtmr3_event_count']} RTMR3 events", 5.04, 4.65, 3.14, 0.22, 9.2, DARK)

    add_box(slide, 8.88, 3.62, 3.78, 1.48, fill=ORANGE_TINT, line=ORANGE, line_width=1.3)
    add_text(slide, "ANVIL GAS ACCOUNTING", 9.14, 3.86, 3.04, 0.22, 9.6, ORANGE, True)
    add_text(slide, f"{gas_accounting['gas']:,} gas", 9.14, 4.18, 3.10, 0.32, 17.0, DARK, True)
    registration = manifest["gas_accounting"]["registration"]
    add_text(
        slide,
        f"{registration['transactions']}/6 registrations · {registration['gas']:,} gas",
        9.14,
        4.65,
        3.14,
        0.22,
        8.8,
        DARK,
    )

    capacity_cards = [
        (0.68, "RUN CAPACITY", f"Tier 1: at most {EVALUATED_TIER1_ACTIVE_TEE_LIMIT} active TEEs", TU_RED, RED_TINT),
        (4.54, "TRAINING", "6 workers · 6 × 13,078 = 78,468 samples", GREEN, GREEN_TINT),
        (8.40, "INFRASTRUCTURE", "2 CVMs · contract/control runtime + Ollama", PURPLE, PURPLE_TINT),
    ]
    for x, heading, body, accent, fill in capacity_cards:
        add_box(slide, x, 5.34, 3.62, 0.72, fill=fill, line=accent, line_width=1.2)
        add_text(slide, heading, x + 0.16, 5.47, 3.30, 0.18, 8.5, accent, True, align=PP_ALIGN.CENTER)
        add_text(slide, body, x + 0.16, 5.72, 3.30, 0.20, 8.5, DARK, True, align=PP_ALIGN.CENTER)
    add_note(
        slide,
        "This is the sole evaluation run reported by the thesis, journal, and presentation. It executed the "
        "current deterministic equal-weight FedAvg path. Six Phala "
        "tdx.small confidential VMs used fresh measured worker profiles: Worker 0 combined training and "
        "native inference, while Workers 1 through 5 were training-only. After one bootstrap completion, "
        "the evaluated Tier-1 account permitted at most eight concurrently active TEEs. Six slots were "
        "therefore assigned to workers, while the other two ran the contract/control runtime and the Ollama "
        "service. The 78,468 ChestMNIST training samples were split evenly across the six workers, producing "
        "six shards of 13,078 samples. This is a run-specific capacity decision rather than a protocol limit "
        "or a scalability claim. All 24 requested federated rounds succeeded. Every round received all five expected client "
        "updates, giving 120 local training completions and 120 transfers, with no aborted round attempt. "
        "The run recorded no aborted attempt or selection-gap recovery. The 24 model evaluations span 689.22 seconds, "
        "or 29.97 seconds between evaluations on average. The final round-25 model was then consumed through "
        "the measured TEE inference path in 2.839 milliseconds; its evidence contains a 5,010-byte quote and "
        "ten RTMR3 events and was bound to receiver receipts and a transparency record. The verifier scope "
        "covered the AIR signature, REPORTDATA, RTMR3 replay, measured Compose, pinned image, contract endpoint, "
        "and trust-root policy; quote collateral was not independently marked as verified in this record. "
        "Receipt-level reconciliation in the observability export accounts for all six registrations. "
        "The 329 unique transactions and 616,141,147 gas quantify the simulated Anvil EVM protocol execution, "
        "including 472,240,960 gas for RTMR3 registration.",
    )


TEST_EVALUATION_SLIDE_NAME = "VITA-FL implemented test evaluation"


def apply_test_evaluation_asset(slide, page_number: int):
    """Import the approved editable test matrix without its concept framing."""
    approved = Presentation(ASSETS / "test-evaluation-a.pptx")
    assert len(approved.slides) == 1, "The test-evaluation asset must contain one slide"
    source = approved.slides[0]
    titles = [shape.text for shape in source.shapes if shape.has_text_frame
              and shape.top < Inches(.95) and shape.left < Inches(1)
              and shape.width > Inches(5)]
    kickers = [shape.text for shape in source.shapes if shape.has_text_frame
               and Inches(.95) <= shape.top < Inches(1.30)
               and shape.left < Inches(1) and shape.width > Inches(5)]
    assert len(titles) == 1 and len(kickers) == 1, "Expected the standard asset heading"
    assert source.notes_slide.notes_text_frame.text.strip(), "Test classification notes are required"
    for shape in list(slide.shapes):
        remove_shape(shape)
    slide.name = TEST_EVALUATION_SLIDE_NAME
    add_content_title(slide, titles[0], kickers[0], page_number)
    add_domain_navigation(slide, page_number, active_domains={"DFL", "Agent"})
    elements = [deepcopy(shape.element) for shape in source.shapes
                if shape.top >= Inches(1.43)
                and shape.top + shape.height <= Inches(6.71)]
    assert elements, "The test-evaluation asset has no content shapes"
    ids = {}
    next_id = slide.shapes._next_shape_id
    for element in elements:
        assert not element.xpath(".//a:blip"), "The test matrix must use native editable shapes"
        for properties in element.xpath(".//p:cNvPr"):
            old_id = properties.get("id")
            assert old_id not in ids, "Duplicate shape identifier in the source asset"
            ids[old_id] = str(next_id)
            next_id += 1
    for element in elements:
        for properties in element.xpath(".//p:cNvPr"):
            properties.set("id", ids[properties.get("id")])
        for connection in element.xpath(".//a:stCxn | .//a:endCxn"):
            connection.set("id", ids[connection.get("id")])
        for node in element.iter():
            for attribute, value in list(node.attrib.items()):
                if attribute.startswith("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"):
                    relationship = source.part.rels[value]
                    assert relationship.is_external, "Only external source hyperlinks are expected"
                    node.set(attribute, slide.part.relate_to(
                        relationship.target_ref, relationship.reltype, is_external=True,
                    ))
        slide.shapes._spTree.insert_element_before(element, "p:extLst")
    add_note(slide, source.notes_slide.notes_text_frame.text)
    return slide


def slide_test_evaluation(prs):
    """Use the approved inventory of implemented test types and their locations."""
    slide = prs.slides.add_slide(prs.slide_masters[1].slide_layouts[0])
    return apply_test_evaluation_asset(slide, len(prs.slides))


def slide_learning_trajectories(prs):
    slide = new_content_slide(
        prs,
        20,
        "What changed over the 24 federated rounds?",
        "Equal-weight FedAvg · five complementary views of model behavior",
    )
    evidence = load_authoritative_evaluation()
    rows = evidence["rows"]
    learning = evidence["manifest"]["learning"]
    final = learning["final"]
    add_run_metric_chart(
        slide,
        0.45,
        1.43,
        4.05,
        2.10,
        "Unweighted test BCE",
        rows,
        "loss",
        0.30,
        0.42,
        [(0.30, "0.30"), (0.33, "0.33"), (0.36, "0.36"), (0.39, "0.39"), (0.42, "0.42")],
        color=BLUE,
        descriptor=f"Lower is better · best {learning['best_test_bce']:.3f} at global round {learning['best_test_bce_round']}",
    )
    add_run_metric_chart(
        slide,
        4.64,
        1.43,
        4.05,
        2.10,
        "Macro AUROC",
        rows,
        "macro_auroc",
        0.48,
        0.73,
        [(0.50, "0.50"), (0.60, "0.60"), (0.65, "0.65"), (0.70, "0.70")],
        color=GREEN,
        reference=0.50,
        reference_label="chance",
        descriptor=f"Higher is better · best {learning['best_macro_auroc']:.3f} at global round {learning['best_macro_auroc_round']}",
    )
    add_run_metric_chart(
        slide,
        8.83,
        1.43,
        4.05,
        2.10,
        "Macro F1",
        rows,
        "macro_f1",
        0.14,
        0.20,
        [(0.15, "0.15"), (0.17, "0.17"), (0.19, "0.19")],
        color=ORANGE,
        descriptor=f"Higher is better · best {learning['best_macro_f1']:.3f} at global round {learning['best_macro_f1_round']}",
    )
    add_run_metric_chart(
        slide,
        1.55,
        3.77,
        5.10,
        2.14,
        "Label-wise accuracy",
        rows,
        "accuracy_percent",
        85.5,
        90.0,
        [(86.0, "86%"), (87.0, "87%"), (88.0, "88%"), (89.0, "89%")],
        color=PURPLE,
        descriptor=f"Negative-dominated · final {final['accuracy_percent']:.2f}% · interpret with the baseline",
    )
    add_run_metric_chart(
        slide,
        6.78,
        3.77,
        5.10,
        2.14,
        "Exact match",
        rows,
        "exact_match_percent",
        24.0,
        34.0,
        [(25.0, "25%"), (27.0, "27%"), (30.0, "30%"), (32.0, "32%")],
        color=TU_RED,
        descriptor=f"All 14 labels must match · best 32.75% · final {final['exact_match_percent']:.2f}%",
    )
    add_note(
        slide,
        "The plots show every learned global model from the sole Phala run: federated rounds 1 through 24 "
        "produce global-model rounds 2 through 25. Binary cross-entropy is the mean probabilistic error over "
        "fourteen independent labels, so lower is better. It falls from 0.414148 to its minimum of 0.329733 "
        "at global round 24 and ends at 0.332544. Macro AUROC evaluates per-label ranking and weights every "
        "label equally; 0.5 is chance and 1 is ideal. It rises from 0.655573 to 0.720301 at round 13 and ends "
        "at 0.711352, providing non-random ranking evidence. Macro F1 is the per-label harmonic mean of "
        "precision and recall; it reaches 0.195377 at global round 8 and ends at 0.177471. Label-wise accuracy "
        "starts at 88.6936 percent and ends at 85.8592 percent. Exact match requires all fourteen binary labels "
        "of a sample to be correct simultaneously; it peaks at 32.7509 percent and ends at 26.0242 percent. "
        "Because only 5.2569 percent of label positions are positive, both accuracy curves are dominated by "
        "negatives and must be read with the all-negative baselines on the next slide. Every point belongs to "
        "the same current equal-weight FedAvg model lineage.",
    )


def slide_learning_quality(prs):
    slide = new_content_slide(
        prs,
        21,
        "Why do the headline scores look modest?",
        "Current FedAvg run · imbalance makes AUROC and F1 more informative than accuracy",
    )
    evidence = load_authoritative_evaluation()
    manifest = evidence["manifest"]
    final = manifest["learning"]["final"]
    imbalance = manifest["imbalance_baselines"]

    add_text(slide, "TEST LABEL POSITIONS", 0.72, 1.51, 3.28, 0.22, 10.0, TU_RED, True)
    add_box(slide, 0.72, 1.92, 3.28, 0.54, fill=LIGHT, line=BORDER, radius=False)
    positive_w = 3.28 * imbalance["positive_label_rate"]
    add_box(slide, 0.72, 1.92, positive_w, 0.54, fill=TU_RED, line=TU_RED, radius=False)
    add_text(slide, "5.26% positive", 0.74, 2.62, 1.55, 0.22, 11.2, TU_RED, True)
    add_text(slide, "94.74% negative", 2.20, 2.62, 1.80, 0.22, 11.2, DARK, True, align=PP_ALIGN.RIGHT)
    add_text(
        slide,
        "A classifier that always predicts 'negative' already scores 94.74% label accuracy.",
        0.72,
        3.08,
        3.28,
        0.78,
        12.2,
        DARK,
        True,
        align=PP_ALIGN.CENTER,
        valign=MSO_ANCHOR.MIDDLE,
    )

    add_text(slide, "BASELINE VS FINAL MODEL", 4.42, 1.51, 4.45, 0.22, 10.0, TU_RED, True, align=PP_ALIGN.CENTER)
    headers = ["", "ALL-NEGATIVE", "VITA-FL r25"]
    for index, header in enumerate(headers):
        add_text(slide, header, 4.42 + index * 1.48, 1.91, 1.42, 0.28, 8.4, TU_RED if index == 2 else DARK, True, align=PP_ALIGN.CENTER)
    comparison = [
        ("LABEL ACC.", f"{imbalance['all_negative_label_accuracy_percent']:.2f}%", f"{final['accuracy_percent']:.2f}%"),
        ("EXACT MATCH", f"{imbalance['all_negative_exact_match_percent']:.2f}%", f"{final['exact_match_percent']:.2f}%"),
        ("MACRO F1", "0.000", f"{final['macro_f1']:.3f}"),
        ("MACRO AUROC", "0.500", f"{final['macro_auroc']:.3f}"),
    ]
    for row_index, row in enumerate(comparison):
        y = 2.31 + row_index * 0.53
        fill = LIGHT if row_index % 2 == 0 else WHITE
        add_box(slide, 4.42, y, 4.45, 0.47, fill=fill, line=BORDER, radius=False, line_width=0.5)
        for col_index, value in enumerate(row):
            add_text(slide, value, 4.53 + col_index * 1.44, y + 0.12, 1.26, 0.19, 9.0, GREEN if col_index == 2 and row_index >= 2 else DARK, col_index != 1, align=PP_ALIGN.CENTER)

    add_box(slide, 9.25, 1.51, 3.36, 2.90, fill=ORANGE_TINT, line=ORANGE, line_width=1.3)
    add_text(slide, "WHY F1 REMAINS LOW", 9.52, 1.77, 2.82, 0.22, 10.2, ORANGE, True, align=PP_ALIGN.CENTER)
    reasons = [
        "rare positive labels",
        "one fixed 0.5 threshold",
        "two local epochs",
        "compact two-convolution CNN",
    ]
    for index, reason in enumerate(reasons):
        y = 2.27 + index * 0.48
        add_oval(slide, 9.54, y, 0.25, 0.25, WHITE, ORANGE, 1.2)
        add_text(slide, "•", 9.60, y + 0.025, 0.13, 0.12, 8.5, ORANGE, True, align=PP_ALIGN.CENTER, margin=0)
        add_text(slide, reason, 9.93, y - 0.01, 2.25, 0.25, 9.7, DARK, True)

    add_box(slide, 0.78, 4.75, 11.78, 0.58, fill=GREEN_TINT, line=GREEN, line_width=1.2)
    add_text(
        slide,
        "Interpretation: lower raw accuracy is compatible with learning positives; AUROC 0.711 shows ranking signal, while F1 0.177 calls for label-specific threshold calibration.",
        1.05,
        4.90,
        11.24,
        0.29,
        10.8,
        DARK,
        True,
        align=PP_ALIGN.CENTER,
        valign=MSO_ANCHOR.MIDDLE,
    )
    add_box(slide, 1.36, 5.64, 10.62, 0.43, fill=TU_RED, line=TU_RED, radius=False)
    add_text(slide, "Functional distributed-learning evidence — not a clinical validation.", 1.62, 5.76, 10.10, 0.20, 11.4, WHITE, True, align=PP_ALIGN.CENTER)
    add_note(
        slide,
        "Only 16,510 of 314,062 label positions in the ChestMNIST test split are positive, a rate of "
        "5.2569 percent. Therefore an all-negative classifier obtains 94.7431 percent label-wise accuracy "
        "and 53.1717 percent exact match, while its macro F1 is zero and its AUROC is 0.5. Those two raw "
        "accuracy measures are dominated by correct negatives and are not suitable headline success metrics. "
        "The final model has lower label accuracy, 85.8592 percent, and lower exact match, 26.0242 "
        "percent, because positive class weighting deliberately makes positive predictions instead of choosing "
        "the trivial all-negative shortcut. Its macro AUROC of 0.711352 demonstrates non-random per-label ranking. "
        "Its macro F1 of 0.177471 and micro F1 of 0.262582 are modest because rare labels are evaluated with one "
        "fixed 0.5 threshold after only two local epochs in a compact CNN. The next learning step is label-specific "
        "threshold calibration and repeated model-selection experiments. The current result supports the claim "
        "that the distributed and verifiable pipeline learned a measurable signal; it is not evidence of clinical "
        "validity or diagnostic utility.",
    )


def slide_results(prs):
    slide = new_content_slide(prs, 22, "Results: demonstrated chain and explicit limits", "System integration is not a clinical claim")
    add_text(slide, "DEMONSTRATED PROCESS EVIDENCE", 0.74, 1.51, 5.42, 0.31, 13.5, GREEN, True)
    add_text(slide, "CLINICAL CLAIM BOUNDARY", 7.15, 1.51, 5.43, 0.31, 13.5, ORANGE, True, align=PP_ALIGN.CENTER)
    add_divider(slide, 6.61, 1.48, 0.024, TU_RED, 3.92)
    add_text(slide, "≠", 6.27, 3.04, 0.70, 0.58, 29, TU_RED, True, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)

    add_line_segment(slide, 1.49, 2.24, 1.49, 4.88, GREEN, 2.4)
    evidence = [
        (2.02, "24/24", "federated rounds", "all five expected updates received per round", BLUE),
        (3.19, "6", "admitted TDX workers", "Worker 0 combined training and inference", GREEN),
        (4.36, "3 + 1", "transparency records", "three tool receipts + one inference bundle", PURPLE),
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
            16.0,
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
    add_text(slide, "0.704", 8.99, 2.80, 1.48, 0.40, 23, GREEN, True, align=PP_ALIGN.CENTER)
    add_text(slide, "macro AUROC", 9.05, 3.28, 1.36, 0.25, 10.3, DARK, True, align=PP_ALIGN.CENTER)
    add_arrow(slide, 11.39, 2.21, 11.39, 4.16, ORANGE, 2.2)
    add_text(slide, "F1", 11.05, 2.43, 0.68, 0.28, 16, ORANGE, True, align=PP_ALIGN.CENTER)
    add_text(slide, "0.185", 10.96, 3.65, 0.86, 0.34, 18, DARK, True, align=PP_ALIGN.CENTER)
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
        "The sole Phala run completed all 24 requested federated rounds with six admitted TDX workers and "
        "all five expected client updates in every round. Worker 0 then served the final round-25 model "
        "through the attested inference path. That path produced three receiver-signed tool receipts and one "
        "complete inference-evidence record. The final macro AUROC of 0.704 demonstrates ranking signal, while "
        "macro F1 of 0.185 remains limited by rare labels, a fixed 0.5 threshold, two local epochs, and the "
        "compact CNN. These results demonstrate protocol execution and measurable learning, not diagnostic utility.",
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
        (3.25, "DFL MODEL", "closed set + atomic handoff"),
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
        "The conclusion is specific to the sole evaluated systems path: six admitted TDX workers completed "
        "all 24 requested FedAvg rounds, the final model reached macro AUROC 0.711 and macro F1 0.177, and Worker 0 "
        "consumed that model through the measured inference path. The modest F1 reflects rare ChestMNIST "
        "positives, one fixed 0.5 threshold, two local epochs, and the compact CNN. "
        "VITA-FL connects the ledger-authoritative "
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
    """Use approved A: one image contains training, inference and internal keys."""
    approved = Presentation(ASSETS / "worker-inference-a.pptx")
    assert len(approved.slides) == 1
    source = approved.slides[0]
    slide = new_content_slide(prs, 28, "Training and inference share one verified image", "")
    for shape in source.shapes:
        if shape.top < Inches(1.43) or shape.top + shape.height > Inches(6.28):
            continue
        element = deepcopy(shape.element)
        assert not element.xpath(".//a:blip | .//a:hlinkClick | .//a:hlinkMouseOver"), \
            "Worker/inference diagram must contain only self-contained native shapes"
        for properties in element.xpath(".//p:cNvPr"):
            properties.set("id", str(slide.shapes._next_shape_id))
        slide.shapes._spTree.insert_element_before(element, "p:extLst")
    add_note(slide, source.notes_slide.notes_text_frame.text)
    return slide


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
    slide_hospital_motivation(prs)
    slide_literature_comparison(prs)
    slide_fl_dfl_roles(prs)
    slide_lifecycle(prs)
    slide_architecture(prs)
    slide_dfl_hospitals(prs)
    slide_tee_vs_zk(prs)
    slide_image_policy(prs)
    slide_phala_attestation(prs)
    slide_dstack_keys(prs)
    slide_aggregator_selection(prs)
    slide_aggregator_recovery(prs)
    slide_close_compare_commit(prs)
    slide_handoff(prs)
    slide_sello_protocol(prs)
    slide_agent(prs)
    slide_external_audit(prs)
    slide_cryptographic_chain(prs)
    slide_evaluation(prs)
    slide_test_evaluation(prs)
    slide_learning_trajectories(prs)
    slide_learning_quality(prs)
    slide_conclusion(prs)
    slide_worker_roles_backup(prs)
    slide_threats_dfl(prs)
    slide_threats_agent(prs)
    for number, threat in enumerate(THREAT_DETAIL_SLIDES, start=32):
        slide_threat_detail(prs, number, *threat)
    assert len(prs.slides) == 45
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
