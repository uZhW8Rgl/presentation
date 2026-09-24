# Sello / AIR — intention and implementation

These revised proposals explain the purpose of each cited work and how that
purpose is applied in VITA-FL. Cryptographic formats and algorithms are in the
speaker notes rather than the main diagram.

| Variant | Sello | AIR |
|---|---|---|
| A — Source intention beside own implementation | [PNG](a-sello-intention.png) | [PNG](a-air-intention.png) |
| B — Start from the agent's claim and show the supporting evidence | [PNG](b-sello-scenario.png) | [PNG](b-air-scenario.png) |

[Overview](overview.png) · [Editable slides](VITA-FL_Sello_AIR_Purpose.pptx) ·
[PDF](VITA-FL_Sello_AIR_Purpose.pdf)

## Core message

**Sello:** The source seeks independent, private oversight of agent actions.
The prototype applies receiver-produced records to three concrete steps in the
model-use workflow. The receiver logs its record before returning success, and
the agent checks the corresponding receipt. Owner independence is not fully
implemented: the decryption and issuer secrets remain in the agent runtime, and
independent receipt discovery and log witnesses are absent.

**AIR:** The draft seeks a portable, checkable record of a single inference.
The prototype connects the published DFL model to its numeric input and result,
then retains checked evidence for later review. That concerns the DFL inference,
not the agent's reasoning or the medical correctness of its response. Per-call
quote authentication is incomplete, so execution trust relies on the previously
admitted worker. The full technical qualifications remain in the notes.

The agent statements in B are illustrative claims, not measured clinical
findings or verbatim experimental conversations.

Sources: [Figuera, Notarized Agents (2026)](https://arxiv.org/html/2606.04193v1)
and [Tsyrulnikov, AIR Internet-Draft 02 (2026)](https://www.ietf.org/archive/id/draft-tsyrulnikov-rats-attested-inference-receipt-02.html).
Implementation/source audit: [parent documentation](../README.md).

Rebuild from the `presentation` directory:

```sh
.venv/bin/python concepts/sello-air/intent/build.py
```

The builder verifies text bounds and preserves the main presentation. These are
native editable PowerPoint shapes; PNG and PDF files are layout previews.
