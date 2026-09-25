"""Variant D: editable steps showing complementary evaluation scopes."""

import common as c


def build(prs):
    slide = c.page(
        prs,
        "D",
        "Different tests answer different questions",
        "THREE COMPLEMENTARY LEVELS OF EVIDENCE",
    )

    c.text(slide, "Checks explain individual decisions.\nThe deployed run demonstrates composition.",
           .73, 1.63, 7.65, .79, 21, c.INK)

    # Three native editable panels share a baseline; their heights express
    # increasing execution scope, not increasing security or evidence quality.
    baseline = 5.82
    steps = [
        (.73, 3.23, 3.78, c.GREEN),
        (4.70, 2.58, 3.78, c.BLUE),
        (8.67, 1.76, 3.93, c.PURPLE),
    ]
    for x, top, width, color in steps:
        c.panel(slide, x, top, width, baseline - top,
                color=color, width=0, radius=False)
        c.panel(slide, x, top, width, .07,
                color=color, fill=color, width=0, radius=False)

    x = .95
    c.text(slide, "01  COMPONENT / CONTRACT", x, 3.43, 3.35, .25,
           12, c.GREEN, True)
    c.text(slide, "Do the checks\nreject invalid state?", x, 3.74, 3.35, .78,
           19, c.INK, True)
    c.text(slide, "Modified input rejected;\nlast finalized model preserved.",
           x, 4.54, 3.35, .55, 15.5, c.INK)
    c.text(slide, "…/tests/test_dicom_provenance.py", x, 5.20, 3.35, .24,
           12, c.GREEN, True)
    c.text(slide, "…/test/GMStorageAbort.t.sol", x, 5.49, 3.35, .24,
           12, c.GREEN, True)

    x = 4.92
    c.text(slide, "02  LOCAL SERVICE", x, 2.80, 3.35, .25,
           12, c.BLUE, True)
    c.text(slide, "Does the receiver\nfail closed?", x, 3.14, 3.35, .78,
           19, c.INK, True)
    c.text(slide, "ASGI request with an injected\nlog-publication failure:",
           x, 3.93, 3.35, .56, 15.5, c.INK)
    c.text(slide, "HTTP 503 · no receipt", x, 4.56, 3.35, .34,
           18, c.BLUE, True)
    c.text(slide, "tee_inference/tests/", x, 5.18, 3.35, .19,
           12, c.MUTED)
    c.text(slide, "test_authorization.py", x, 5.39, 3.35, .22,
           12.5, c.BLUE, True)

    x = 8.90
    c.text(slide, "03  DEPLOYED WORKFLOW", x, 1.98, 3.44, .25,
           12, c.PURPLE, True)
    c.text(slide, "Do the components\nwork together?", x, 2.36, 3.44, .78,
           19, c.INK, True)
    c.text(slide, "Existing Phala run", x, 3.15, 3.44, .34,
           18, c.PURPLE, True)
    c.text(slide, "6 workers\n24 training rounds\n1 final inference", x, 3.66, 3.44, 1.03,
           20, c.INK)
    c.text(slide, "No injected failure.", x, 4.84, 3.44, .30,
           15, c.INK)
    c.text(slide, "data/evaluation/", x, 5.18, 3.44, .19,
           12, c.MUTED)
    c.text(slide, "Phala run record · 2026-09-01", x, 5.39, 3.44, .22,
           12.5, c.PURPLE, True)

    c.scope(slide,
            "Complementary scopes: controlled checks and local integration support the single deployed functional run.")
    return slide
