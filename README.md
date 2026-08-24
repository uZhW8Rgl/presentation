# VITA-FL — Master's Thesis Presentation

This repository contains the English presentation for the VITA-FL master's
thesis. It comprises twenty-one talk pages, three compact backup and overview
pages (one worker-role overview and two threat overviews), and fourteen
full-size use/misuse-case backup pages, for a total of thirty-eight pages. The complete
timed talk is approximately sixteen minutes. The deck is built directly from
the official TU Berlin PowerPoint template, and its title page preserves the
official TU Berlin branding.

## Files

- `TU_Berlin_Praesentation_Master_einfarbig_Rot.pptx`: unchanged TU Berlin source template
- `VITA-FL_Thesis_Presentation_TU_Berlin.pptx`: editable 16:9 presentation
- `preview/contact-sheet.png`: preview of all thirty-eight pages
- `build_presentation.py`: reproducible deck generator
- `render_preview.py`: lightweight local QA renderer
- `assets/threat-diagrams/T1.png` … `T14.png`: use/misuse-case source diagrams
- `assets/xray_concept.png`: realistic, anonymized chest-radiograph motif used on Page 3
- `assets/physician-editorial-illustration-tablet.png`: illustrated physician used on Page 3
- `assets/computer-scientist-editorial-illustration.png`: illustrated computer scientist used on Page 4
- `data/evaluation/evaluation_run_{10,50,100}.csv`: source data for the editable learning-result plots
- `requirements.txt`: pinned Python dependencies

Every page contains English speaker notes. The PNG renderer is intended only
for layout inspection; PowerPoint remains authoritative for exact font metrics
and line wrapping. Preview rendering expects the DejaVu Sans fonts at their
standard Linux paths.

Pages 22–38 are backup material and are not included in the timing below.

## Suggested timing

| Page | Topic | Time |
|---:|---|---:|
| 1 | Title and guiding idea | 0:25 |
| 2 | Personal background and project experience | 0:30 |
| 3 | Physician's starting point | 0:45 |
| 4 | Computer scientist's engineering response | 0:35 |
| 5 | Research gap and questions | 0:45 |
| 6 | Overall architecture | 0:45 |
| 7 | Decentralized training across hospitals | 0:35 |
| 8 | Worker-training and DCAP-admission ZK scope | 0:50 |
| 9 | Intel-backed attestation and app-bound dstack keys | 0:55 |
| 10 | Weighted aggregator selection | 0:40 |
| 11 | Quorum recovery and aggregator replacement | 0:45 |
| 12 | Freeze → Compare → Finalize | 0:50 |
| 13 | Model handoff | 0:40 |
| 14 | Sello proposal and the selectively adopted VITA-FL profile | 0:45 |
| 15 | Agent-mediated attested inference | 0:55 |
| 16 | Independent audit | 0:50 |
| 17 | Cryptographic chain of custody | 0:55 |
| 18 | Evaluation design | 0:45 |
| 19 | Optimization trajectories across participant counts | 0:45 |
| 20 | Learning-quality limitations | 0:45 |
| 21 | Conclusion and outlook | 0:40 |

Total: approximately sixteen minutes, including brief transitions between the
timed pages. For a shorter slot, Pages 9–11 and 17
can be treated as technical detail pages without breaking the main narrative.

## Regeneration

Run from the repository root:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python build_presentation.py
.venv/bin/python render_preview.py
```

After substantive edits, open the deck once in Microsoft PowerPoint or
LibreOffice Impress to confirm the exact Arial line wrapping on the target
machine.

The bundled TU Berlin template and its marks remain subject to the applicable
TU Berlin branding and usage rules.
