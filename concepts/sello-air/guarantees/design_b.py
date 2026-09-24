"""Variant B: editable, sequential Sello / AIR assurance workflow."""
import slidekit as k


def build(prs):
    s = k.page(
        prs, 'B', 'Sello + AIR: checks along the inference workflow',
        'Sello authorizes and records the tool call; AIR binds the numeric inference evidence.',
    )

    columns = [
        (
            .69, k.SELLO, 'SELLO', 'Authorize',
            'mTLS + token:\nidentity, receiver,\nscope, certificate,\nexpiry; job owner.',
            'Authorized caller',
        ),
        (
            3.74, k.AIR, 'AIR', 'Build AIR bundle',
            'Sign model / I/O /\nquote hashes.\nAttach REPORTDATA,\nRTMR3 log and\nCompose evidence.',
            'Bound workload',
        ),
        (
            6.79, k.SELLO, 'SELLO', 'Seal receipt',
            'HPKE encrypts body.\nReceiver signature\nbinds action, I/O\nhashes, token ref.\nand result status.',
            'Protected receipt',
        ),
        (
            9.84, k.LOG, 'RECEIVER + AGENT', 'Log and verify',
            'Log Sello first.\nAgent checks Sello,\nAIR + runtime policy;\nchecks SCITT and\nthen registers AIR.',
            'Recorded evidence',
        ),
    ]
    w = 2.79
    # A continuous route expresses execution order; colours identify ownership.
    for i, (x, color, _role, _title, _detail, _result) in enumerate(columns[:-1]):
        next_x = columns[i + 1][0]
        k.route(s, [(x + w / 2 + .23, 2.29), (next_x + w / 2 - .26, 2.29)], color, 2)

    for i, (x, color, role, title, detail, result) in enumerate(columns, 1):
        k.number(s, str(i), x + w / 2 - .20, 2.09, color, diameter=.40)
        k.panel(s, x, 2.66, w, 2.44, color)
        k.tag(s, role, x + .15, 2.53, w - .30, color, size=12.5, h=.30)
        k.text(s, title, x + .16, 2.98, w - .32, .36, 18, color, True)
        k.text(s, detail, x + .16, 3.43, w - .32, 1.50, 16)

    k.panel(s, .69, 5.34, 11.94, .59, k.LOG)
    k.text(s, 'Release rule', .88, 5.45, 2.19, .33, 16, k.LOG, True)
    k.text(
        s, 'A verified result is returned only after receipt, AIR and log checks succeed.',
        3.13, 5.40, 9.24, .44, 16.5,
    )
    k.footer(s)
    return s
