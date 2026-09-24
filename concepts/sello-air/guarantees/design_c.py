"""Variant C: the tool-call scope enclosing numeric-inference evidence."""
import slidekit as k


def build(prs):
    s = k.page(
        prs, 'C', 'Two scopes of evidence, one verified tool result',
        'Sello covers the tool call; AIR binds its model, input and result.'
    )

    # The blue outline is the interaction scope, never an encryption envelope.
    k.panel(s, .69, 2.05, 11.94, 3.15, k.SELLO, fill=k.WHITE, width=1.7)
    k.tag(s, 'SELLO  /  TOOL INTERACTION', .91, 2.19, 3.47, k.SELLO, size=14, h=.32)
    k.text(s, 'Scopes of evidence — separate receipts', 7.91, 2.18, 4.48, .33,
           14, k.MUTED, center=False)

    # Left gate: authorization applies before the inference can be invoked.
    k.text(s, 'Who may call?', .93, 2.79, 2.14, .34, 18, k.SELLO, True)
    k.text(s, 'mTLS + signed token', .93, 3.26, 2.13, .59, 17, k.INK, True)
    k.text(s, 'Identity + scope\nCertificate\nExpiry · job owner', .93, 3.94,
           2.15, .96, 15.5, k.INK)
    k.route(s, [(3.06, 3.73), (3.22, 3.73)], k.SELLO, 1.8)

    # Inner scope: the numerical inference and its domain-specific checks.
    k.panel(s, 3.25, 2.66, 6.01, 2.37, k.AIR, width=1.5)
    k.text(s, 'AIR  /  NUMERIC INFERENCE', 3.45, 2.81, 5.61, .33,
           17, k.AIR, True)
    for label, x, w in [('Model', 3.45, 1.62), ('Input', 5.39, 1.62), ('Result', 7.33, 1.72)]:
        k.panel(s, x, 3.24, w, .42, k.AIR, fill=k.WHITE, width=.9)
        k.text(s, label, x+.04, 3.28, w-.08, .32, 17, k.AIR, True, True)
    k.route(s, [(5.08, 3.45), (5.36, 3.45)], k.AIR, 1.4)
    k.route(s, [(7.02, 3.45), (7.30, 3.45)], k.AIR, 1.4)
    k.text(s, 'Signed hashes detect changed data',
           3.45, 3.78, 5.61, .36, 16, k.INK)
    k.text(s, 'REPORTDATA binds key + model + input',
           3.45, 4.16, 5.61, .34, 15.5, k.INK)
    k.text(s, 'Replay RTMR3; match deployment policy',
           3.45, 4.54, 5.61, .34, 15.5, k.INK)
    k.route(s, [(9.29, 3.73), (9.48, 3.73)], k.SELLO, 1.8)

    # Right evidence: signed call/result binding plus receipt-only encryption.
    k.text(s, 'What was returned?', 9.54, 2.79, 2.84, .34, 18, k.SELLO, True)
    k.text(s, 'Receiver signs the receipt', 9.54, 3.26, 2.83, .59,
           17, k.INK, True)
    k.text(s, 'Action · I/O hashes\nToken · status',
           9.54, 3.96, 2.82, .60, 15.5, k.INK)
    k.text(s, 'HPKE: owner only', 9.54, 4.62, 2.82, .43,
           15.5, k.SELLO, True)

    # Both evidence types are registered separately. This is not envelope nesting.
    k.panel(s, .69, 5.37, 11.94, .63, k.LOG, width=1.1)
    k.text(s, 'Log', .89, 5.49, 1.42, .32, 18, k.LOG, True)
    k.text(s, 'Sello before reply  →  agent checks SCITT  →  AIR registered separately',
           2.51, 5.41, 9.89, .28, 16, k.INK)
    k.text(s, 'HPKE protects the Sello receipt only; the AIR bundle includes plaintext input/output.',
           2.51, 5.71, 9.89, .24, 13.5, k.MUTED)
    k.footer(s)
    return s
