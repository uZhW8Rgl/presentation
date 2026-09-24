"""A — balanced comparison, with checks immediately below each guarantee."""
import slidekit as k


def build(prs):
    s = k.page(prs, 'A', 'Sello and AIR: two layers of evidence',
               'Sello checks the tool interaction. AIR binds the numeric inference.')
    k.b.add_domain_navigation(s, 28, active_domains={"Agent"})
    groups = [
        (.69, k.SELLO, 'Sello', 'Tool interaction', [
            ('An authorised agent may call',
             'mTLS + token: identity, Inference TEE,\nscope, certificate, expiry; job ownership.'),
            ('A signed record of the tool call',
             'Inference TEE signs action, input/output hashes,\ntoken reference and result status.'),
            ('The receipt body stays encrypted',
             'HPKE seals the Sello receipt for the owner.'),
        ]),
        (6.80, k.AIR, 'AIR', 'Attested Inference Receipt', [
            ('Model, input and result stay linked',
             'Ed25519 signs their hashes and the quote hash.'),
            ('The receipt key is bound to the quote',
             'REPORTDATA: key + manifest + request.\nThe AIR signature binds the result.'),
            ('Deployment policy is checked',
             'Replay RTMR3; compare Compose, image digest,\nchain, contracts and RPC.'),
        ]),
    ]
    for x, color, name, purpose, rows in groups:
        k.b.add_box(s, x, 2.08, 5.83, 3.20, fill=k.WHITE, line=color, radius=False, line_width=1.1)
        k.b.add_box(s, x+.015, 2.095, 5.80, .61, fill=k.TINT[color], line=k.TINT[color], radius=False, line_width=0)
        k.text(s, name, x+.20, 2.20, 1.45, .48, 26, color, True)
        k.text(s, purpose, x+1.65, 2.24, 3.94, .33, 18, color)
        for i, (claim, check) in enumerate(rows):
            y = 2.80 + i*.81
            k.number(s, str(i+1), x+.20, y+.015, color, .28)
            k.text(s, claim, x+.62, y, 4.99, .32, 16.4, color, True)
            k.text(s, check, x+.62, y+.32, 4.97, .49, 14.0, k.INK)
    k.panel(s, .69, 5.43, 11.94, .67, k.LOG)
    k.tag(s, 'SHARED LOG', .86, 5.625, 1.46, k.LOG, 11.5, .28)
    k.text(s, 'Inference TEE logs Sello before reply', 2.51, 5.605, 4.66, .32, 15, k.LOG, True)
    k.route(s, [(7.28,5.765),(7.59,5.765)], k.LOG, 1.5)
    k.text(s, 'Agent verifies Transparency Log\nand logs AIR', 7.78, 5.485, 4.62, .56, 15, k.LOG, True)
    k.footer(s, show_scope=False)
    return s
