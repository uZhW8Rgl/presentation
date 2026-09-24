"""Alternative D: interfaces around the worker and its distinct key roles."""

import common as c


def actor(s, title, lines, x, y, w, h, color, symbol):
    c.panel(s, x, y, w, h, color)
    if symbol == 'model':
        for a, b in [((.19,.19),(.47,.32)), ((.19,.46),(.47,.32))]:
            c.route(s, [(x+a[0],y+a[1]),(x+b[0],y+b[1])], color, 1.2, False)
        for px, py in [(.19,.19),(.19,.46),(.47,.32)]:
            c.b.add_oval(s, x+px-.05, y+py-.05, .10, .10, c.WHITE, color, 1.2)
    elif symbol == 'log':
        c.panel(s, x+.17, y+.13, .34, .43, color, c.WHITE)
        for py in [.24,.34,.44]:
            c.route(s, [(x+.24,y+py),(x+.44,y+py)], color, 1.0, False)
    else:
        c.icon(s, symbol, x+.16, y+.16, .40, color)
    c.text(s, title, x+.67, y+.12, w-.80, .34, 18, color, True, False)
    c.text(s, lines, x+.18, y+.59, w-.36, h-.68, 15.2, c.INK,
           False, False)


def key(s, label, x, y, w, color):
    c.panel(s, x, y, w, .78, color, c.WHITE)
    c.icon(s, 'key', x+.12, y+.17, .36, color)
    c.text(s, label, x+.55, y+.10, w-.65, .58, 14.5, color, True)


def build(prs):
    s = c.page(prs, 'D', 'Key use at the system interfaces',
               'Actor map: a worker holds separate keys for blockchain actions, '
               'model exchange, tool receipts, and inference evidence. The AES '
               'sealing key is internal custody of a randomly generated RSA key. '
               'Model payload bytes use separate symmetric encryption keys.')

    # The worker is the visual centre. External boxes describe concrete uses,
    # while internal boxes name the corresponding key identities.
    c.text(s, 'dstack GetKey(path): action, wrapping and receipt keys',
           .65, 1.49, 12.03, .36, 19, c.INK)
    c.panel(s, 4.29, 2.03, 4.74, 3.98, c.INK, 'F8F9FA', 1.3)
    c.icon(s, 'tee', 5.05, 2.16, .46, c.INK)
    c.text(s, 'Worker TEE', 5.58, 2.14, 2.23, .44, 24, c.INK, True)

    actor(s, 'Blockchain',
          'Protocol transactions\nUpdate commitments\nAggregation statements',
          .55, 2.55, 3.10, 1.46, c.PURPLE, 'blockchain')
    actor(s, 'Model exchange',
          'Sign model packages\nUnwrap symmetric keys',
          .55, 4.36, 3.10, 1.40, c.GREEN, 'model')
    actor(s, 'Receipt log',
          'Signed tool-action receipts\nRecording and audit trail',
          9.68, 2.55, 3.10, 1.46, c.BLUE, 'log')
    actor(s, 'Agent',
          'Verify signed inference\nevidence (AIR)',
          9.68, 4.36, 3.10, 1.40, c.BLUE, 'agent')

    key(s, 'Derived\nsecp256k1', 4.48, 2.91, 2.08, c.PURPLE)
    key(s, 'Sello\nEd25519', 6.77, 2.91, 2.08, c.BLUE)
    key(s, 'Random\nRSA-3072', 4.48, 4.42, 2.08, c.GREEN)
    key(s, 'AIR\nEd25519', 6.77, 4.42, 2.08, c.BLUE)

    c.route(s, [(4.45, 3.29), (3.69, 3.29)], c.PURPLE)
    c.route(s, [(8.88, 3.29), (9.64, 3.29)], c.BLUE)
    c.route(s, [(4.45, 4.81), (3.69, 4.81)], c.GREEN)
    c.route(s, [(8.88, 4.81), (9.64, 4.81)], c.BLUE)

    # AES is deliberately shown only inside the TEE: it protects persisted RSA
    # private-key state rather than being the model-payload encryption key.
    c.pill(s, 'Derived AES-GCM seals RSA state',
           4.48, 5.51, 4.37, c.GREEN, 14.0, .34)
    c.route(s, [(5.53, 5.48), (5.53, 5.23)], c.GREEN, 1.5)
    return s
