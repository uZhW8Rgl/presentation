"""Variant A: an explicit mapping from system boundary to test implementation."""
import common as c


def build(prs):
    s = c.page(prs, "A", "Existing tests cover specific system guarantees",
               "EVALUATION · TEST CASE, IMPLEMENTATION AND TEST LEVEL")
    c.text(s, "Representative cases link each requirement to an implemented check.",
           .68, 1.52, 11.98, .39, 19)

    headers = [("BOUNDARY", .83, 1.64),
               ("EXAMPLE ASSERTION", 2.64, 3.32),
               ("IMPLEMENTED IN", 6.10, 3.28),
               ("TEST TYPE", 9.73, 2.70)]
    for value, x, w in headers:
        c.text(s, value, x, 2.07, w, .27, 10.5, c.MUTED, True)
    c.line(s, .68, 2.43, 11.98)

    rows = [
        ("Training input", "Changed signed label\nis rejected", "dfl/neural_network/tests/",
         "test_dicom_provenance.py", "Component", "Python · signer fixtures", c.GREEN),
        ("Round state", "Abort preserves the\nlast finalized model", "smart_contracts/test/",
         "GMStorageAbort.t.sol", "Contract component", "Foundry · local EVM", c.PURPLE),
        ("Model exchange", "No recipient key →\nno decryption", "dfl/node_server/test/",
         "gm_crypto.test.js", "Component", "Node.js · local AES/RSA", c.GREEN),
        ("Inference", "Substituted request\nis rejected", "agent/tests/",
         "test_tee_inference_client.py", "Component", "Python · synthetic quote", c.BLUE),
        ("Receiver API", "Log failure → HTTP 503\nand no receipt", "tee_inference/tests/",
         "test_authorization.py", "Local integration", "ASGI · mocked log", c.BLUE),
    ]
    for i, (label, assertion, folder, filename, level, framework, color) in enumerate(rows):
        y = 2.47 + i * .565
        c.b.add_box(s, .68, y, .045, .515, fill=color, line=color, radius=False, line_width=0)
        c.text(s, label, .83, y+.015, 1.65, .49, 13, color, True)
        c.text(s, assertion, 2.64, y+.015, 3.25, .49, 14)
        c.text(s, folder, 6.10, y+.025, 3.38, .20, 10.5, c.MUTED)
        c.text(s, filename, 6.10, y+.235, 3.38, .235, 12, c.INK, True)
        c.text(s, level, 9.73, y+.025, 2.76, .24, 13.5, color, True)
        c.text(s, framework, 9.73, y+.285, 2.76, .20, 10.5, c.MUTED)
        c.line(s, .83, y+.54, 11.80)

    c.panel(s, .68, 5.45, 11.98, .39, c.INK, c.TINT[c.INK], 0, False)
    c.text(s, "Separate end-to-end evidence: one Phala run · 24 training rounds · final inference",
           .85, 5.48, 11.62, .30, 13.5, c.INK, True)
    c.scope(s, "Scope: local fixtures and mocked dependencies; live aggregator failover was not exercised.")
    return s
