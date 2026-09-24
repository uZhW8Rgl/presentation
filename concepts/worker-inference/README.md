# Worker / inference: alternatives for slide 28

Three native PowerPoint proposals clarify that the inference service is part of
the same digest-pinned `dfl-worker` image and container as training. They show
internal key use and public results/evidence at the agent interface.

- **A — Shared image:** nested TEE/container boundaries, DFL and inference
  processes, internal keys and the external agent.
- **B — Inference path:** encrypted model input, internal RSA-based model access,
  inference and separate Ed25519 evidence signing.
- **C — Worker roles:** the same packaged image in training-only Workers 1–5
  and combined Worker 0, with inference enabled only in Worker 0.

All proposals distinguish on-chain workload admission from KMS key release in
their speaker notes. Variant A uses the requested takeaway "No private keys
sent to the agent" and the arrow label "MCP Tool request"; its two explanatory
sentences above and below the diagram were removed. Speaker notes retain the
KMS/update-policy assumption, lack of process-level key isolation, and the
narrower per-inference verification scope.

Variant A also places the Transparency Log below the agent. The inference
receiver publishes Sello receipts to it; the agent separately publishes AIR
evidence. Both paths are shown as labelled arrows.

`VITA-FL_Worker_Inference_Alternatives.pptx` contains three editable slides.
The matching PDF and PNGs are local previews; PowerPoint is authoritative for
exact rendering. `overview.png` compares all three. `original-slide-28.png`
preserves a preview of the original slide. Revised variant A was adopted as
slide 28, with an independent asset at `../../assets/worker-inference-a.pptx`.

Rebuild from the presentation directory:

```bash
.venv/bin/python concepts/worker-inference/build_designs.py
```

The builder checks text bounds, preserves code-source notes and verifies that
the main presentation remains byte-for-byte unchanged.
