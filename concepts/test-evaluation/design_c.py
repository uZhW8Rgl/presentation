"""Concept C: three editable fault-to-response experiment lanes."""

import common as c


def build(prs):
    slide = c.page(
        prs,
        "C",
        "What happens when evidence is wrong?",
        "EXISTING TESTS · THREE CONTROLLED FAULT SCENARIOS",
    )

    lanes = [
        {
            "y": 1.52,
            "color": c.GREEN,
            "label": "01  TRAINING DATA",
            "fault": "Modified signed label",
            "check": "Training provenance\nverifier",
            "reaction": "Reject\ninvalid signature",
            "source": "test_dicom_provenance.py",
            "kind": "Component · Python",
        },
        {
            "y": 2.95,
            "color": c.BLUE,
            "label": "02  INFERENCE EVIDENCE",
            "fault": "Substituted\ninference request",
            "check": "AIR bundle verifier",
            "reaction": "Reject\nrequest mismatch",
            "source": "test_tee_inference_client.py",
            "kind": "Component · Python",
        },
        {
            "y": 4.38,
            "color": c.PURPLE,
            "label": "03  TOOL COMPLETION",
            "fault": "Log publication\nfailure",
            "check": "Receiver API",
            "reaction": "HTTP 503\nNo receipt",
            "source": "test_authorization.py",
            "kind": "Local integration · ASGI, mocked log",
        },
    ]

    for lane in lanes:
        y, color = lane["y"], lane["color"]
        c.text(slide, lane["label"], .68, y, 3.8, .23, 11.5, color, True)
        c.text(slide, "COMPONENT UNDER TEST", 4.70, y, 3.25, .23, 11.5, c.MUTED)
        c.text(slide, "EXPECTED RESPONSE", 9.35, y, 3.08, .23, 11.5, color, True)

        box_y, box_h = y + .34, .72
        # An open input, an outlined production component, and a tinted reaction
        # keep each case readable as a left-to-right experiment, not a matrix.
        c.text(slide, lane["fault"], .88, box_y, 2.90, box_h, 19, c.INK, True)
        c.line(slide, .68, box_y + .10, .06, color)
        c.route(slide, [(3.82, box_y + .36), (4.40, box_y + .36)], color, 2.2)

        c.panel(slide, 4.57, box_y, 3.63, box_h, color, c.WHITE, 1.3, False)
        c.text(slide, lane["check"], 4.72, box_y + .03, 3.33, box_h - .06,
               18, c.INK, True, True)
        c.route(slide, [(8.35, box_y + .36), (9.02, box_y + .36)], color, 2.2)

        c.panel(slide, 9.19, box_y, 3.45, box_h, color, c.TINT[color], 0, False)
        c.text(slide, lane["reaction"], 9.36, box_y + .03, 3.11, box_h - .06,
               18, color, True)

        c.text(slide, lane["source"], .88, y + 1.13, 5.15, .22, 12, c.MUTED)
        c.text(slide, lane["kind"], 6.33, y + 1.13, 6.10, .22, 12, c.MUTED,
               center=False)
        if lane is not lanes[-1]:
            c.line(slide, .68, y + 1.40, 11.96)

    c.scope(slide, "Implemented scenarios; expected outcomes shown. Controlled dependencies; no new test-run results.")
    return slide
