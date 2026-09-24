# Lifecycle: Blockchain and IPFS

Current proposal deck: **`VITA-FL_Lifecycle_Blockchain_IPFS.pptx`**.
Four editable variants, all based on A1 or A2:

| Variant | Layout |
|---|---|
| A1a | One published-model field with Blockchain and IPFS inside |
| A1b | A separate model symbol branches into the two stores |
| A2a | Global model at the circle boundary, directly followed by the two stores |
| A2b | Blockchain and IPFS as shared infrastructure below the main flow |

Blockchain supplies the authoritative model reference; IPFS supplies the model
files. Both feed the inference receiver. Their arrows show consumed information;
the receiver initiates retrieval. The global/published-model output summarizes
publication by the aggregator. Other DFL coordination and intermediate training
artifact transfers are abstracted inside the training circle.

The agent invokes inference through MCP. The transparency log receives the tool
receipt and remains distinct from the blockchain. The speaker notes explain
these boundaries without adding implementation details to the visible slides.

The original A and the preceding A1/A2 remain available in the parent proposal
folders. A3 has been removed from the preceding A-variant deck and its generator.

Individual PNGs and `overview.png` are approximate layout previews. All diagram
elements are editable PowerPoint shapes; PowerPoint determines exact font metrics.

Regenerate from the presentation directory:

```bash
.venv/bin/python concepts/lifecycle/infrastructure/build_variants.py
```
