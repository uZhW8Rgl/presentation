#!/usr/bin/env python3
"""Render an approximate PNG preview of the generated deck.

This is intentionally a lightweight visual QA renderer. PowerPoint remains the
authoritative renderer, but the preview catches misplaced shapes, clipping, and
unbalanced layouts in environments without LibreOffice or Microsoft Office.
"""

from __future__ import annotations

import math
import re
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from pptx import Presentation
from pptx.enum.dml import MSO_FILL_TYPE
from pptx.enum.shapes import MSO_AUTO_SHAPE_TYPE, MSO_SHAPE_TYPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN


ROOT = Path(__file__).resolve().parent
DECK = ROOT / "VITA-FL_Thesis_Presentation_TU_Berlin.pptx"
OUTPUT = ROOT / "preview"

WIDTH = 1600
HEIGHT = 900
FONT_REGULAR = "/usr/share/fonts/dejavu/DejaVuSans.ttf"
FONT_BOLD = "/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf"
FONT_MONO = "/usr/share/fonts/dejavu/DejaVuSansMono.ttf"


def rgb_tuple(value, fallback=(0, 0, 0)):
    try:
        return tuple(value.rgb)
    except Exception:
        return fallback


def alpha_for(color_format):
    try:
        color_element = color_format._color._xClr
        alpha = color_element.find("{http://schemas.openxmlformats.org/drawingml/2006/main}alpha")
        if alpha is not None:
            return round(int(alpha.get("val")) * 255 / 100000)
    except Exception:
        pass
    return 255


def font_for(run, scale):
    size_pt = float(run.font.size.pt) if run.font.size is not None else 16.0
    size_px = max(8, round(size_pt * scale))
    name = (run.font.name or "").lower()
    if "mono" in name:
        path = FONT_MONO
    elif run.font.bold:
        path = FONT_BOLD
    else:
        path = FONT_REGULAR
    return ImageFont.truetype(path, size_px)


def text_color(run):
    try:
        return tuple(run.font.color.rgb) + (255,)
    except Exception:
        return (244, 250, 253, 255)


def split_tokens(text):
    return [token for token in re.split(r"(\s+)", text) if token]


def paragraph_lines(draw, paragraph, max_width, scale):
    lines = [[]]
    line_width = 0
    runs = list(paragraph.runs)
    if not runs and paragraph.text:
        return [[(paragraph.text, ImageFont.truetype(FONT_REGULAR, round(16 * scale)), (244, 250, 253, 255))]]

    for run in runs:
        font = font_for(run, scale)
        color = text_color(run)
        chunks = run.text.split("\n")
        for chunk_index, chunk in enumerate(chunks):
            for token in split_tokens(chunk):
                token_width = draw.textlength(token, font=font)
                if not token.isspace() and line_width + token_width > max_width and lines[-1]:
                    lines.append([])
                    line_width = 0
                if token.isspace() and not lines[-1]:
                    continue
                lines[-1].append((token, font, color))
                line_width += token_width
            if chunk_index < len(chunks) - 1:
                lines.append([])
                line_width = 0
    return lines


def render_text(layer, shape, sx, sy):
    frame = shape.text_frame
    draw = ImageDraw.Draw(layer)
    left = round(shape.left * sx + frame.margin_left * sx)
    top = round(shape.top * sy + frame.margin_top * sy)
    right = round((shape.left + shape.width) * sx - frame.margin_right * sx)
    bottom = round((shape.top + shape.height) * sy - frame.margin_bottom * sy)
    max_width = max(1, right - left)
    scale = HEIGHT / (7.5 * 72)

    paragraph_blocks = []
    for paragraph in frame.paragraphs:
        lines = paragraph_lines(draw, paragraph, max_width, scale)
        line_metrics = []
        for line in lines:
            ascents = []
            descents = []
            for _, font, _ in line:
                ascent, descent = font.getmetrics()
                ascents.append(ascent)
                descents.append(descent)
            max_ascent = max(ascents or [round(16 * scale)])
            max_descent = max(descents or [round(4 * scale)])
            line_height = (max_ascent + max_descent) * 1.08
            line_metrics.append((line_height, max_ascent))
        paragraph_blocks.append((paragraph, lines, line_metrics))

    total_height = 0
    for index, (_, _, metrics) in enumerate(paragraph_blocks):
        total_height += sum(line_height for line_height, _ in metrics)
        if index < len(paragraph_blocks) - 1:
            total_height += round(5 * scale)

    anchor = frame.vertical_anchor
    if anchor == MSO_ANCHOR.MIDDLE:
        y = top + max(0, (bottom - top - total_height) / 2)
    elif anchor == MSO_ANCHOR.BOTTOM:
        y = bottom - total_height
    else:
        y = top

    for block_index, (paragraph, lines, metrics) in enumerate(paragraph_blocks):
        for line, (line_height, max_ascent) in zip(lines, metrics):
            widths = [draw.textlength(text, font=font) for text, font, _ in line]
            line_width = sum(widths)
            if paragraph.alignment == PP_ALIGN.CENTER:
                x = left + (max_width - line_width) / 2
            elif paragraph.alignment == PP_ALIGN.RIGHT:
                x = right - line_width
            else:
                x = left
            baseline = y + max_ascent
            for (text, font, color), token_width in zip(line, widths):
                draw.text(
                    (round(x), round(baseline)),
                    text,
                    font=font,
                    fill=color,
                    anchor="ls",
                )
                x += token_width
            y += line_height
        if block_index < len(paragraph_blocks) - 1:
            y += round(5 * scale)


def render_shape(canvas, shape, sx, sy):
    layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    x0 = round(shape.left * sx)
    y0 = round(shape.top * sy)
    x1 = round((shape.left + shape.width) * sx)
    y1 = round((shape.top + shape.height) * sy)
    if x1 <= 0 or y1 <= 0 or x0 >= canvas.width or y0 >= canvas.height:
        return

    if shape.shape_type == MSO_SHAPE_TYPE.PICTURE:
        image = Image.open(BytesIO(shape.image.blob)).convert("RGBA")
        image = image.resize((max(1, x1 - x0), max(1, y1 - y0)), Image.Resampling.LANCZOS)
        layer.alpha_composite(image, (x0, y0))

    elif shape.shape_type == MSO_SHAPE_TYPE.LINE:
        transform = shape._element.spPr.xfrm
        flip_h = bool(transform.flipH)
        flip_v = bool(transform.flipV)
        start = (x1 if flip_h else x0, y1 if flip_v else y0)
        end = (x0 if flip_h else x1, y0 if flip_v else y1)
        color = rgb_tuple(shape.line.color, (175, 196, 207))
        width = max(1, round((shape.line.width or 12700) / 12700 * HEIGHT / (7.5 * 72)))
        dashed = shape.line.dash_style is not None
        if dashed:
            length = math.dist(start, end)
            if length:
                ux = (end[0] - start[0]) / length
                uy = (end[1] - start[1]) / length
                step = max(8, width * 4)
                pos = 0
                while pos < length:
                    stop = min(length, pos + step)
                    draw.line((start[0] + ux * pos, start[1] + uy * pos, start[0] + ux * stop, start[1] + uy * stop), fill=color + (255,), width=width)
                    pos += step * 1.75
        else:
            draw.line((*start, *end), fill=color + (255,), width=width)

        line_properties = shape._element.spPr.ln
        tail = None if line_properties is None else line_properties.find("{http://schemas.openxmlformats.org/drawingml/2006/main}tailEnd")
        if tail is not None and tail.get("type") != "none":
            angle = math.atan2(end[1] - start[1], end[0] - start[0])
            length = max(10, width * 5)
            spread = math.pi / 6
            points = [
                end,
                (end[0] - length * math.cos(angle - spread), end[1] - length * math.sin(angle - spread)),
                (end[0] - length * math.cos(angle + spread), end[1] - length * math.sin(angle + spread)),
            ]
            draw.polygon(points, fill=color + (255,))

    elif shape.shape_type in {MSO_SHAPE_TYPE.AUTO_SHAPE, MSO_SHAPE_TYPE.FREEFORM}:
        fill = None
        if shape.fill.type == MSO_FILL_TYPE.SOLID:
            fill = rgb_tuple(shape.fill.fore_color, (16, 44, 58)) + (alpha_for(shape.fill.fore_color),)
        outline = None
        try:
            outline = rgb_tuple(shape.line.color, (49, 82, 99)) + (alpha_for(shape.line.color),)
        except Exception:
            pass
        line_width = max(1, round((shape.line.width or 12700) / 12700 * HEIGHT / (7.5 * 72)))
        try:
            kind = shape.auto_shape_type
        except (AttributeError, ValueError):
            kind = None
        if kind == MSO_AUTO_SHAPE_TYPE.OVAL:
            draw.ellipse((x0, y0, x1, y1), fill=fill, outline=outline, width=line_width)
        elif kind == MSO_AUTO_SHAPE_TYPE.ROUNDED_RECTANGLE:
            radius = max(4, round(min(x1 - x0, y1 - y0) * 0.12))
            draw.rounded_rectangle((x0, y0, x1, y1), radius=radius, fill=fill, outline=outline, width=line_width)
        else:
            draw.rectangle((x0, y0, x1, y1), fill=fill, outline=outline, width=line_width)

    if shape.has_text_frame and any(paragraph.text for paragraph in shape.text_frame.paragraphs):
        render_text(layer, shape, sx, sy)
    canvas.alpha_composite(layer)


def render_slide(prs, slide):
    sx = WIDTH / prs.slide_width
    sy = HEIGHT / prs.slide_height
    background = (255, 255, 255, 255)
    try:
        if slide.background.fill.type == MSO_FILL_TYPE.SOLID:
            background = rgb_tuple(slide.background.fill.fore_color, background[:3]) + (255,)
    except Exception:
        pass
    canvas = Image.new("RGBA", (WIDTH, HEIGHT), background)
    for shape in slide.slide_layout.slide_master.shapes:
        if not getattr(shape, "is_placeholder", False):
            render_shape(canvas, shape, sx, sy)
    for shape in slide.slide_layout.shapes:
        if not getattr(shape, "is_placeholder", False):
            render_shape(canvas, shape, sx, sy)
    for shape in slide.shapes:
        render_shape(canvas, shape, sx, sy)
    return canvas.convert("RGB")


def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    prs = Presentation(DECK)
    previews = []
    for index, slide in enumerate(prs.slides, 1):
        preview = render_slide(prs, slide)
        destination = OUTPUT / f"slide-{index:02d}.png"
        preview.save(destination, quality=95)
        previews.append(preview)

    thumb_width = 720
    thumb_height = round(thumb_width * HEIGHT / WIDTH)
    gutter = 28
    rows = math.ceil(len(previews) / 2)
    sheet = Image.new(
        "RGB",
        (thumb_width * 2 + gutter * 3, thumb_height * rows + gutter * (rows + 1)),
        (221, 229, 234),
    )
    for index, preview in enumerate(previews):
        thumb = preview.resize((thumb_width, thumb_height), Image.Resampling.LANCZOS)
        column = index % 2
        row = index // 2
        x = gutter + column * (thumb_width + gutter)
        y = gutter + row * (thumb_height + gutter)
        sheet.paste(thumb, (x, y))
    sheet.save(OUTPUT / "contact-sheet.png", quality=95)
    print(OUTPUT / "contact-sheet.png")


if __name__ == "__main__":
    main()
