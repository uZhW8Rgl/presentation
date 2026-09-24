# Variations of lifecycle concept A

These are the retained earlier concepts before adding Blockchain and IPFS.
The current proposals are in [`../infrastructure`](../infrastructure/README.md).

`VITA-FL_Lifecycle_A_Variants.pptx` contains three editable slides:

1. **A0 — Original:** the unchanged A slide from the preceding concept deck.
2. **A1 — Model handoff:** the global model is the circle's exit; a model symbol
   represents the published version between DFL and inference.
3. **A2 — Compact:** one model node at the circle boundary, followed by a
   publication arrow to inference. Agent stays above inference.

The green circle in A1–A2 runs counterclockwise: local training, aggregation,
global model, next local training. Arrows make this order explicit. The original
A keeps its original clockwise arrangement.

`overview.png` compares the three retained slides; individual PNGs allow closer inspection.
All new diagram elements are native editable PowerPoint shapes. The PNGs use
the presentation's approximate renderer. PowerPoint is authoritative for exact
font metrics and line wrapping.

The build checks the original slide XML and preview pixels and records hashes
of the preserved source files in `preserved-originals.json`.

Regenerate from the presentation directory:

```bash
.venv/bin/python concepts/lifecycle/a-variants/build_variants.py
```
