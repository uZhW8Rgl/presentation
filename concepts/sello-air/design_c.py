"""Variant C: editable receipt anatomy, with explicit prototype boundaries."""
import common as c


def build_sello(prs):
    s = c.page(prs, 'C · Sello', 'Inside a Sello receipt', 'sello')
    c.text(s, 'Paper: receiver-signed, owner-encrypted receipts + witnessed logging',
           .66, 1.49, 12.0, .42, 18, c.INK)

    # The tool sequence is separate from the structure of a single receipt.
    c.text(s, 'Three fixed tools', .66, 2.20, 2.24, .34, 17, c.BLUE, True)
    for y, title in [(2.79, 'Fetch model'), (3.42, 'Select image'),
                     (4.05, 'Run inference')]:
        c.panel(s, .66, y, 2.24, .47, c.BLUE)
        c.text(s, title, .81, y+.04, 1.94, .37, 17, c.BLUE, True, True)
    for center_y in (3.025, 3.655, 4.285):
        c.route(s, [(2.94, center_y), (3.14, center_y)], c.BLUE, 1.6, False)
    c.route(s, [(3.14, 3.025), (3.14, 4.285)], c.BLUE, 1.6, False)
    c.route(s, [(3.14, 3.65), (3.36, 3.65)], c.BLUE, 1.9)

    # Public routing data is visibly outside the owner-encrypted body.
    c.panel(s, 3.41, 2.15, 5.84, 2.52, c.PURPLE, c.WHITE, 1.5)
    c.text(s, 'VITA-FL · signed receipt', 3.60, 2.26, 5.46, .36,
           19, c.PURPLE, True)
    c.panel(s, 3.59, 2.77, 5.48, .60, c.INK)
    c.text(s, 'Public header', 3.75, 2.80, 5.16, .29, 15.5, c.INK, True)
    c.text(s, 'Receiver key ID · token reference · log URL',
           3.75, 3.07, 5.16, .30, 16, c.INK)
    c.panel(s, 3.59, 3.49, 5.48, .67, c.PURPLE)
    c.text(s, 'HPKE-encrypted body', 3.75, 3.53, 5.16, .27,
           17, c.PURPLE, True)
    c.text(s, 'Tool · input/output Digests · status · time',
           3.75, 3.85, 5.16, .30, 16, c.INK)
    c.text(s, 'Ed25519 signature over the envelope',
           3.62, 4.30, 5.42, .30, 16, c.PURPLE, True)

    c.route(s, [(9.30, 3.65), (9.90, 3.65)], c.PURPLE, 1.9)
    c.text(s, 'Receiver publishes', 9.92, 2.80, 2.74, .32,
           16, c.PURPLE, True, True)
    c.card(s, 'SCITT / CCF', 'Before response',
           9.96, 3.25, 2.70, 1.12, c.PURPLE, 17)
    c.text(s, 'Added: dstack key + DeviceRegistry binding · mandatory mTLS',
           .66, 4.76, 12.0, .34, 17, c.BLUE, True)

    c.caveat(s, 'Prototype\nboundary',
             'No independent witnesses or owner discovery.\n'
             'Owner keys reside in the agent runtime.', y=5.19)
    c.source(s, 'sello')
    return s


def build_air(prs):
    s = c.page(prs, 'C · AIR', 'An AIR receipt inside the inference evidence', 'air')
    c.text(s, 'Draft: signed evidence for one inference; separate attestation appraisal',
           .66, 1.49, 12.0, .42, 18, c.INK)

    # The outer bundle is specific to this prototype; the receipt is one layer.
    c.panel(s, .66, 2.11, 7.55, 2.78, c.BLUE, c.WHITE, 1.5)
    c.text(s, 'VITA-FL evidence bundle', .87, 2.24, 7.12, .35,
           19, c.BLUE, True)
    rows = [
        (2.83, 'Exact image pixels + prediction', c.INK, False),
        (3.30, 'Model manifest → DFL artifact Digest', c.INK, False),
        (3.77, 'AIR-style receipt · signed Digests', c.PURPLE, True),
        (4.24, 'TDX quote + measured Compose + event log', c.BLUE, False),
    ]
    for y, title, color, bold in rows:
        c.panel(s, .89, y, 7.09, .40, color)
        c.text(s, title, 1.08, y+.02, 6.71, .34, 17, color, bold)

    c.route(s, [(8.27, 3.22), (8.88, 3.22)], c.BLUE, 1.9)
    c.card(s, 'Agent verifies', 'Signature · RTMR3 replay\nBindings + Image Digest',
           8.94, 2.47, 3.72, 1.49, c.BLUE, 16.5)
    c.route(s, [(10.80, 4.02), (10.80, 4.34)], c.PURPLE, 1.9)
    c.panel(s, 8.94, 4.40, 3.72, .49, c.PURPLE)
    c.text(s, 'SCITT · published bundle', 9.08, 4.45, 3.44, .35,
           17, c.PURPLE, True, True)

    c.caveat(s, 'Prototype\nboundary',
             'No independent DCAP appraisal per call: relies on admitted receiver.\n'
             'Published bundle includes unencrypted input pixels.', y=5.19)
    c.source(s, 'air')
    return s
