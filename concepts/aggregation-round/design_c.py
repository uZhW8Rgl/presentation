"""Variant C: a signed statement connects the computed model to finalization."""
import common as c


def build(prs):
    s = c.page(
        prs, 'C', 'One signed statement binds the round to its result',
        'Evidence-centred view: frozen round context and an already published '
        'global model feed the action-key-signed aggregation statement. '
        'GMStorage verifies the registered signer and context, then publishes '
        'references and advances the round in a single transaction.')

    c.text(s, 'TEE AGGREGATOR', .65, 1.53, 3.0, .32, 14, c.GREEN, True)
    c.text(s, 'BOUND BY ONE SIGNATURE', 4.26, 1.53, 4.17, .32,
           14, c.GREEN, True)
    c.text(s, 'ON-CHAIN FINALIZATION', 9.10, 1.53, 3.57, .32,
           14, c.PURPLE, True)

    # Two concrete sources feed a single evidence object.  Publication precedes
    # signing: the statement commits to the CIDs that IPFS has already returned.
    c.panel(s, .65, 2.02, 3.0, 1.48, c.GREEN)
    c.text(s, 'Closed inputs', .85, 2.12, 2.6, .35, 21, c.GREEN, True)
    c.text(s, 'Round + aggregator', .84, 2.57, 2.62, .27, 14)
    c.text(s, 'Input fingerprint + count', .84, 2.87, 2.62, .27, 14)
    c.text(s, 'FedAvg + active policy', .84, 3.17, 2.62, .27, 14)

    c.panel(s, .65, 3.89, 3.0, 1.75, c.GREEN)
    c.text(s, 'Published output', .83, 3.99, 2.64, .36, 18, c.GREEN, True)
    c.text(s, 'Signed, encrypted model', .80, 4.42, 2.7, .31, 13.5)
    c.pill(s, 'IPFS', .84, 4.88, .76, c.BLUE, 15, .41)
    c.text(s, 'Model + signature\nRecipient keys', 1.72, 4.79,
           1.70, .60, 13, c.INK, False, False)
    c.text(s, 'Three CIDs returned', .84, 5.30, 2.62, .27, 14, c.BLUE, True)

    c.route(s, [(3.67, 2.79), (4.23, 2.79)], c.GREEN, 2.0)
    c.route(s, [(3.67, 4.76), (4.23, 4.76)], c.GREEN, 2.0)

    # A native document, visually grouped by the facts covered by the signature.
    c.panel(s, 4.26, 2.02, 4.17, 3.62, c.GREEN, c.WHITE, 1.8)
    c.text(s, 'Aggregation statement', 4.47, 2.15, 3.75, .38,
           19, c.GREEN, True)
    c.route(s, [(4.49, 2.66), (8.20, 2.66)], c.GREEN, .8, False)
    rows = [
        'Round · aggregator · nonce',
        'Frozen input fingerprint + count',
        'Algorithm + policy',
        'Model hash + encrypted-bundle hash',
        'Publication hash: three IPFS CIDs',
    ]
    for i, value in enumerate(rows):
        y = 2.78 + .47*i
        c.text(s, value, 4.52, y, 3.67, .32, 13.5, c.INK, False, False)
    c.panel(s, 4.46, 5.22, 3.76, .28, c.GREEN, c.GREEN, 0)
    c.text(s, 'EIP-712 signature · action key', 4.50, 5.225, 3.68, .25,
           13.5, c.WHITE, True)

    c.route(s, [(8.46, 3.47), (9.04, 3.47)], c.PURPLE, 2.0)

    c.panel(s, 9.10, 2.02, 3.57, 2.17, c.PURPLE)
    c.text(s, 'GMStorage', 9.32, 2.16, 3.13, .40,
           24, c.PURPLE, True)
    c.text(s, 'Checks via AggregationPolicy', 9.25, 2.65, 3.27, .31,
           14, c.PURPLE, True)
    c.text(s, 'Registered action-key signature', 9.30, 3.12, 3.17, .30, 14)
    c.text(s, 'Aggregator + closed inputs', 9.26, 3.48, 3.25, .30, 14)
    c.text(s, 'Policy + publication context', 9.26, 3.84, 3.25, .30, 14)
    c.route(s, [(10.88, 4.22), (10.88, 4.48)], c.PURPLE, 2.0)

    c.panel(s, 9.10, 4.52, 3.57, 1.12, c.PURPLE, c.WHITE, 1.8)
    c.text(s, 'Single transaction', 9.27, 4.65, 3.23, .34,
           17.5, c.PURPLE, True)
    c.text(s, 'Store references + evidence\nComplete round → next round',
           9.27, 5.06, 3.23, .51, 14)

    c.text(s, 'FedAvg executes inside the attested TEE; the chain checks the signed statement.',
           .68, 5.88, 11.99, .33, 16, c.INK, False)
    return s
