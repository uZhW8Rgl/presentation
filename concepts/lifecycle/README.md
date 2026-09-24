# Lifecycle slide proposals

Four alternatives for a conceptual overview before the detailed architecture
(currently Page 9). Each is one slide in `VITA-FL_Lifecycle_Concepts.pptx`.
All diagram elements are editable PowerPoint shapes and text.

| Concept | Idea | Emphasis |
|---|---|---|
| A — loop and branch | DFL cycle with a model-publication branch | Closest to the requested circle and path |
| B — two loops | Separate training and request/response loops | Repeated training and repeated use |
| C — four stages | Train → Publish → Use → Record | Simple narrative for a broad audience |
| D — two paths | Model and MCP request converge at inference | Clear separation of model flow and agent control |

`overview.png` compares all four. The individual PNGs are larger previews.
They use the presentation's approximate layout renderer; native PowerPoint
remains authoritative for font metrics. Speaker notes explain the abstraction
and the evidence boundary. The proposals do not modify the main deck.

The model flows to the inference service. The agent invokes it through MCP.
The transparency log records a receiver-issued tool receipt; the associated
domain evidence binds the actual model, inference input, and output. The slides
do not imply that inference automatically retrains the DFL model or that all
training activity goes into this log.

Regenerate from the presentation directory:

```bash
.venv/bin/python concepts/lifecycle/build_concepts.py
```
