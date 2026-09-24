"""Guarantee-driven comparison of Sello, AIR and their publication checks."""
import slidekit as k


def build(prs):
    s = k.page(
        prs,
        'D',
        'Sello + AIR: which changes are detected?',
        'Sello verifies the tool interaction; AIR binds the numeric inference evidence.',
    )

    left, right = .69, 12.63
    scenario_x, check_x, outcome_x = .84, 3.48, 8.99
    scenario_w, check_w, outcome_w = 2.42, 5.18, 3.44
    k.text(s, 'SCENARIO', scenario_x, 2.05, scenario_w, .29, 12, k.MUTED, True)
    k.text(s, 'IMPLEMENTED CHECK', check_x, 2.05, check_w, .29, 12, k.MUTED, True)
    k.text(s, 'ENFORCED OUTCOME', outcome_x, 2.05, outcome_w, .29, 12, k.MUTED, True)
    k.route(s, [(left, 2.40), (right, 2.40)], k.INK, 1.3, arrow=False)

    rows = [
        (
            'Unauthorized caller',
            'Sello · mTLS + signed token: subject, audience,\nscope, certificate thumbprint and expiry',
            'Rejects identity, scope\nor token mismatches',
            k.SELLO,
        ),
        (
            'Substituted tool result',
            'Sello · receiver signature: action, exact I/O,\ntoken reference and result status',
            'Detects substituted\ntool input or output',
            k.SELLO,
        ),
        (
            'Exposed receipt body',
            'Sello · HPKE encryption to the owner’s key',
            'Hides the Sello body;\nAIR bundle is plaintext',
            k.SELLO,
        ),
        (
            'Swapped inference data',
            'AIR · signed data / quote hashes; REPORTDATA\nbinds AIR key, manifest and request',
            'Detects data and\nquote-binding mismatches',
            k.AIR,
        ),
        (
            'Different deployment',
            'AIR · RTMR3 replay; Compose / image;\nchain, storage, registry and RPC checks',
            'Rejects configuration\noutside the expected policy',
            k.AIR,
        ),
        (
            'Missing log entry',
            'SCITT · publication receipts verified\nbefore a successful verified tool result',
            'Withholds success;\nexecution is not rolled back',
            k.LOG,
        ),
    ]

    row_y, row_h = 2.43, .585
    for index, (scenario, check, outcome, color) in enumerate(rows):
        y = row_y + index * row_h
        k.b.add_box(s, left, y + .105, .035, .36, fill=color, line=color,
                    radius=False, line_width=0)
        k.text(s, scenario, scenario_x, y + .002, scenario_w, .575,
               16.4, k.INK, True)
        k.text(s, check, check_x, y + .002, check_w, .575,
               15.4, color)
        k.text(s, outcome, outcome_x, y + .002, outcome_w, .575,
               15.4, k.INK)
        k.route(s, [(left, y + row_h), (right, y + row_h)],
                'DEE4E8', .65, arrow=False)

    k.footer(s)
    return s
