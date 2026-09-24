"""A: concrete execution flows with a short source and prototype boundary."""
import common as c


def build_sello(prs):
    s = c.page(prs, 'A · Sello', 'Sello: the receiver records each tool call', 'sello')
    c.panel(s, .66, 1.62, 12, .61, c.INK)
    c.label(s, 'PAPER', .86, 1.80, 1.08, c.MUTED)
    c.text(s, 'Service-signed, owner-encrypted receipts in a witnessed log',
           2.0, 1.75, 10.4, .34, 18)
    c.label(s, 'VITA-FL', .68, 2.39, 1.32)
    c.text(s, 'Model fetch   →   Image selection   →   Inference',
           2.10, 2.33, 10.48, .36, 18, c.BLUE, True)

    c.card(s, 'Agent', 'mTLS +\nscoped token', .7, 2.99, 2.55, 1.33, c.BLUE, 17)
    c.card(s, 'Worker 0 · receiver', 'Input / output Digests\nHPKE encrypt · Ed25519 sign',
           4.1, 2.99, 4.25, 1.33, c.BLUE, 17)
    c.card(s, 'SCITT / CCF', 'Receipt publication\n+ inclusion proof', 9.3, 2.99, 3.3, 1.33, c.PURPLE, 17)
    c.route(s, [(3.30,3.65),(4.04,3.65)], c.BLUE)
    c.text(s, 'Call', 3.31, 3.26, .70, .28, 14, c.BLUE, center=True)
    c.route(s, [(8.40,3.65),(9.24,3.65)], c.PURPLE)
    c.text(s, 'Publish', 8.39, 3.26, .86, .28, 13.5, c.PURPLE, center=True)
    c.route(s, [(10.97,4.36),(10.97,4.76),(6.23,4.76),(6.23,4.36)], c.PURPLE)
    c.panel(s, 6.69, 4.54, 3.92, .40, c.PURPLE, c.WHITE, .6)
    c.text(s, 'Inclusion before response', 6.82, 4.58, 3.66, .32, 14, c.PURPLE, center=True)
    c.route(s, [(4.04,4.13),(3.30,4.13)], c.BLUE)
    c.text(s, 'Result', 3.28, 3.81, .78, .28, 13.5, c.BLUE, center=True)
    c.text(s, 'Receiver key: dstack → DeviceRegistry', .70, 4.59, 5.30, .35, 15, c.BLUE, True)
    c.caveat(s, 'Prototype\ndifferences',
             'No independent log witnesses or owner discovery.\nOwner decryption and issuer keys live in the agent runtime.', y=5.14)
    c.source(s, 'sello')
    return s


def build_air(prs):
    s = c.page(prs, 'A · AIR', 'AIR: connect the prediction to its model', 'air')
    c.panel(s, .66, 1.62, 12, .61, c.INK)
    c.label(s, 'AIR DRAFT', .86, 1.80, 1.45, c.MUTED)
    c.text(s, 'Signed commitments to model, request, response and attestation',
           2.52, 1.75, 9.90, .34, 18)
    c.label(s, 'VITA-FL', .68, 2.43, 1.32)

    for y, title in [(2.95,'DFL manifest'), (3.53,'Numeric input'), (4.11,'Prediction')]:
        c.panel(s, .69, y, 2.85, .43, c.GREEN if y == 2.95 else c.BLUE)
        c.text(s, title, .85, y+.035, 2.52, .35, 18, center=True)
        c.route(s, [(3.59,y+.215),(3.93,y+.215),(3.93,3.73),(4.27,3.73)], c.BLUE)
    c.card(s, 'AIR-style receipt', 'Signed Digests', 4.31, 3.16, 3.72, 1.14, c.BLUE, 17)
    c.text(s, 'Per-call TDX quote\nKey + manifest + request binding',
           4.35, 4.49, 3.63, .61, 15, c.BLUE, center=True)
    c.route(s, [(6.17,4.45),(6.17,4.35)], c.BLUE)
    c.route(s, [(8.08,3.73),(8.78,3.73)], c.BLUE)
    c.card(s, 'Agent checks', 'Signature · RTMR3 replay\nCompose + Image Digest',
           8.83, 2.82, 3.8, 1.33, c.BLUE, 16)
    c.route(s, [(10.74,4.20),(10.74,4.43)], c.PURPLE)
    c.panel(s, 8.83, 4.48, 3.8, .57, c.PURPLE)
    c.text(s, 'SCITT · full evidence bundle', 8.96, 4.58, 3.55, .34, 16, c.PURPLE, True, True)
    c.caveat(s, 'AIR-style\nimplementation',
             'Per-call quote authenticity relies on the admitted receiver.\nNo independent per-call DCAP check or full replay protection.', y=5.24)
    c.source(s, 'air')
    return s
