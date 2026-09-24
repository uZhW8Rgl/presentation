"""B: Follow the encrypted model through the combined worker image."""
import common as c


def build(prs):
    s = c.page(
        prs, 'B', 'Inference uses the worker’s keys inside the same image',
        'B follows model use: the encrypted model enters the combined worker '
        'application; the existing participant RSA key unwraps its transport '
        'key; native inference runs and separate Ed25519 keys sign evidence. '
        'Training and inference are both present in the same container image. '
        'The external agent receives outputs and signed evidence, without a '
        'private-key transfer through the intended interface.')

    # The two enclosing borders distinguish the CVM and its one container image.
    c.panel(s, 2.18, 1.61, 8.73, 4.06, c.INK, c.WHITE, 1.5)
    c.icon(s, 'tee', 2.42, 1.75, .39, c.INK)
    c.text(s, 'WORKER 0 · ONE TEE', 2.95, 1.77, 4.60, .32,
           18, c.INK, True, False)
    c.panel(s, 2.43, 2.23, 8.23, 3.16, c.BLUE, 'F8FBFE', 1.5)
    c.text(s, 'ONE dfl-worker IMAGE · one verified Digest',
           2.65, 2.37, 7.79, .35, 18, c.BLUE, True)

    # Training remains enabled in Worker 0 and shares the participant RSA key.
    c.panel(s, 2.73, 2.96, 2.17, .58, c.GREEN)
    c.text(s, 'Training', 2.81, 3.07, 2.01, .33,
           16, c.GREEN, True)
    c.route(s, [(3.815, 3.57), (3.815, 3.86)], c.GREEN, 1.8)
    c.text(s, 'Native inference process', 5.21, 3.04, 5.09, .35,
           17, c.BLUE, True)

    # An outside model publication supplies encrypted bytes, not private keys.
    c.icon(s, 'encryption', .99, 3.01, .58, c.PURPLE)
    c.text(s, 'Encrypted\nmodel', .52, 3.71, 1.58, .64,
           17, c.PURPLE, True)
    c.text(s, '+ wrapped\nmodel key', .52, 4.44, 1.58, .60,
           15, c.MUTED)
    c.route(s, [(2.04, 4.24), (2.66, 4.24)], c.PURPLE, 2)

    # Keep key purposes distinct: RSA unwraps; Ed25519 signs evidence.
    c.panel(s, 2.73, 3.91, 2.17, .91, c.GREEN, c.WHITE)
    c.text(s, 'Shared RSA key', 2.80, 4.04, 2.03, .31,
           16, c.GREEN, True)
    c.text(s, 'Unwrap model key', 2.85, 4.43, 1.93, .29,
           14.5, c.INK)
    c.route(s, [(4.97, 4.36), (5.28, 4.36)], c.BLUE, 2)

    c.panel(s, 5.35, 3.91, 2.12, .91, c.BLUE, c.WHITE)
    c.text(s, 'Run inference', 5.47, 4.04, 1.88, .31,
           16, c.BLUE, True)
    c.text(s, 'Decrypted model', 5.47, 4.43, 1.88, .29,
           14.5, c.INK)
    c.route(s, [(7.54, 4.36), (7.85, 4.36)], c.BLUE, 2)

    c.panel(s, 7.92, 3.91, 2.40, .91, c.BLUE, c.WHITE)
    c.text(s, 'Sign evidence', 8.04, 4.04, 2.16, .31,
           16, c.BLUE, True)
    c.text(s, 'Ed25519 keys', 8.02, 4.43, 2.20, .29,
           14, c.INK)
    c.route(s, [(10.38, 4.36), (11.19, 4.36)], c.BLUE, 2)

    c.icon(s, 'agent', 11.64, 3.09, .66, c.BLUE)
    c.text(s, 'Agent', 11.22, 3.90, 1.50, .32,
           18, c.BLUE, True)
    c.text(s, 'Prediction\n+ evidence', 11.16, 4.54, 1.64, .66,
           15, c.INK)

    c.text(s, 'No private keys sent to the agent',
           2.70, 4.98, 7.70, .30, 16, c.BLUE, True)
    c.scope(s)
    return s
