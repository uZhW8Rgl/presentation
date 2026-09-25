"""Variant B: implemented checks attached to their architecture boundary."""

import common as c


def _check(slide, x, y, color, kind, example, suite):
    """An editable test probe with a scope label and an actual suite name."""
    c.panel(slide, x, y, 2.78, 1.17, color, width=.8)
    c.tag(slide, kind, x + .13, y + .12, 2.52, color, size=12, h=.29)
    c.text(slide, example, x + .14, y + .40, 2.50, .50,
           size=13.5, bold=True)
    c.text(slide, suite, x + .14, y + .95, 2.50, .20,
           size=11.5, color=c.MUTED)


def build(prs):
    slide = c.page(
        prs, "B", "Evaluation along the architecture",
        "IMPLEMENTED CHECKS AT FOUR SYSTEM BOUNDARIES",
    )
    xs = [.72, 3.75, 6.78, 9.81]
    width = 2.78
    center_y = 3.12
    colors = [c.GREEN, c.PURPLE, c.BLUE, c.BLUE]
    names = ["Training data", "Round coordination", "Inference receiver", "Agent / tool result"]

    # Draw the data/model/result route before its component nodes.
    for i in range(3):
        c.route(slide, [(xs[i] + width, center_y),
                        (xs[i + 1], center_y)], colors[i], 1.8)
    for i, (x, color, name) in enumerate(zip(xs, colors, names)):
        c.panel(slide, x, 2.80, width, .64, color, fill=color,
                width=0, radius=False)
        c.text(slide, name, x + .09, 2.93, width - .18, .33,
               size=16, color=c.WHITE, bold=True, center=True)

    # Alternating probes make the distinction between route and tests explicit.
    _check(slide, xs[0], 1.51, c.GREEN, "Component test",
           "Altered label → rejected", "test_dicom_provenance.py")
    _check(slide, xs[1], 3.86, c.PURPLE, "Local EVM test",
           "Abort → model preserved", "GMStorageAbort.t.sol")
    _check(slide, xs[2], 1.51, c.BLUE, "Local integration test",
           "Log failure → HTTP 503", "test_authorization.py")
    _check(slide, xs[3], 3.86, c.BLUE, "Component test",
           "Altered output → rejected", "test_sello_v1.py")

    for index in (0, 2):
        x = xs[index] + width / 2
        c.route(slide, [(x, 2.68), (x, 2.80)], colors[index], 1.1,
                arrow=False)
    for index in (1, 3):
        x = xs[index] + width / 2
        c.route(slide, [(x, 3.44), (x, 3.86)], colors[index], 1.1,
                arrow=False)

    # Short location annotations identify the modules independently of test files.
    c.text(slide, "dfl/neural_network", xs[0], 3.52, width, .22,
           size=11.5, color=c.GREEN, center=True)
    c.text(slide, "smart_contracts", xs[1], 2.43, width, .22,
           size=11.5, color=c.PURPLE, center=True)
    c.text(slide, "tee_inference", xs[2], 3.52, width, .22,
           size=11.5, color=c.BLUE, center=True)
    c.text(slide, "agent", xs[3], 2.43, width, .22,
           size=11.5, color=c.BLUE, center=True)

    # Existing deployed execution is a separate evidence layer across the route.
    c.panel(slide, .72, 5.28, 11.87, .53, c.INK,
            fill=c.TINT[c.INK], width=.6, radius=False)
    c.tag(slide, "CLOUD END-TO-END", .83, 5.395, 2.05, c.INK,
          size=11, h=.29)
    c.text(slide, "Existing Phala run: 6 workers · 24 training rounds · 1 inference",
           3.04, 5.36, 9.36, .32, size=15)
    c.scope(slide, "Local test cases use controlled dependencies. The cloud run demonstrates the deployed workflow; recovery was not triggered.")
    return slide
