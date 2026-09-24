"""Native PowerPoint helpers for combined Sello/AIR assurance concepts."""
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import common as c
sys.path.insert(0, str(HERE))

b, renderer, ROOT = c.b, c.renderer, c.ROOT
INK, MUTED, WHITE = c.INK, c.MUTED, c.WHITE
SELLO, AIR, LOG, AMBER = c.BLUE, c.GREEN, c.PURPLE, c.AMBER
TINT = c.TINT
text, panel, route, icon = c.text, c.panel, c.route, c.icon

IMPLEMENTATION_NOTES = '''
USER REQUEST: Explain together, on one slide, the implemented responsibilities and guarantees of Sello and AIR. This is the current prototype, not the proposed RA-TLS + Phala API extension.

EXACT TASKS AND ENFORCED CHECKS
AIR data integrity: Ed25519 signature and SHA-256 commitments to the exact deterministic-CBOR model manifest, complete numeric inference request, response and quote. Substitution is detected relative to the authenticated signing identity. The manifest commits to model artifacts; model weights themselves are not placed inside the receipt.
AIR quote binding: REPORTDATA = SHA256("MasterThesis.AIR.key.v1" || AIR_public_key || manifest_hash) || request_hash. The response is bound by the AIR signature, not directly by the existing REPORTDATA. The receipt also hashes the quote.
AIR configuration: RTMR3 is replayed from the ordered event log. Compose hash, expected image digest and configured Chain-ID, GMStorage, DeviceRegistry and RPC endpoint are compared. This is quote-field consistency and deployment policy checking; per-inference Intel quote cryptography remains unverified.
Sello authorization: mandatory PKI mTLS plus signed, short-lived token; agent subject, receiver origin/audience, allowed action scope, certificate thumbprint and expiration must match. Jobs belong to the authenticated subject. This transport is not RA-TLS.
Sello response evidence: admitted receiver's Ed25519 signature binds action, exact logical tool input hash, exact output hash, token reference and result status. Agent compares them to the actual invocation. For run inference, tool input is the canonical job_id object, while output is the complete AIR evidence bundle. It is not evidence about the LLM's reasoning or original chat prompt.
Sello confidentiality: HPKE encrypts the receipt body for the owner. Signature covers the encrypted receipt; public envelope metadata remain visible. The owner private key and token issuer seed are currently in the agent runtime.
Publication: receiver publishes Sello before releasing a successful response; agent verifies Sello and its SCITT receipt, checks AIR and separately registers the AIR bundle. No successful verified tool result is released on publication failure. Computation precedes publication and is not rolled back when logging fails.

SCOPE OF GUARANTEES
Current AIR verifier reports dcap_collateral_verified=False. Prior on-chain admission and registry-bound receiver identity remain trust inputs. It does not reconcile every signed measurement-map entry with the quote. AIR nonce is receiver-generated, and neither AIR nor Sello provides an exactly-once execution guarantee.
The separate AIR bundle contains unencrypted input and output bytes. HPKE privacy applies only to the Sello receipt. SCITT is a single CCF Virtual Mode node without independent witnesses or a pinned log key; development TLS disables server certificate verification and the Phala log uses tmpfs. Registration proves inclusion against the obtained service keys, not permanent availability or a globally unique history. No medical accuracy or independent arithmetic proof is claimed.

LAYOUT: All diagrams are native, editable PowerPoint shapes. Main deck is kept as a separate artifact. Colour role: blue = Sello/tool interaction; green = AIR/numeric DFL inference; purple = shared logging.
'''


def page(prs, letter, title, subtitle):
    s = b.new_content_slide(prs, len(prs.slides)+1, title, 'CURRENT VITA-FL IMPLEMENTATION')
    # Keep the existing footer text while reserving a clean source band above it.
    b.add_box(s, 0, 6.27, 13.333333, .43, fill=WHITE, line=WHITE, radius=False, line_width=0)
    b.add_domain_navigation(s, 28)
    for shape in s.shapes:
        if shape.has_text_frame and shape.text.startswith('Page '):
            shape.text_frame.paragraphs[0].runs[0].text = f'Variant {letter}'
            shape.width = b.Inches(1.10)
    text(s, subtitle, .68, 1.47, 11.96, .51, 19, INK)
    b.add_note(s, f'COMBINED ASSURANCE VARIANT {letter}\n\n' + c.SELLO_NOTES + '\n' + c.AIR_NOTES + IMPLEMENTATION_NOTES)
    return s


def tag(s, value, x, y, w, color, size=12, h=.29):
    b.add_box(s, x, y, w, h, fill=color, line=color, radius=False, line_width=0)
    text(s, value, x+.07, y+.015, w-.14, h-.03, size, WHITE, True, True)


def number(s, value, x, y, color, diameter=.33):
    b.add_oval(s, x, y, diameter, diameter, color, color)
    text(s, value, x, y+.01, diameter, diameter-.02, 12, WHITE, True, True)


def footer(s, *, show_scope=True):
    # Technical qualifications remain in the notes when the visible scope is omitted.
    if show_scope:
        text(s, 'Scope: per-inference Intel quote verification is absent; TEE trust relies on prior worker admission.',
             .69, 6.09, 11.96, .29, 12, AMBER)
    left = text(s, 'Sello-inspired profile · Figuera (2026)', .69, 6.43, 5.7, .22, 10, MUTED)
    left.text_frame.paragraphs[0].runs[0].hyperlink.address = c.SELLO_URL
    right = text(s, 'AIR-style profile · Tsyrulnikov, Internet-Draft 02 (2026)', 6.50, 6.43, 6.1, .22, 10, MUTED)
    right.text_frame.paragraphs[0].runs[0].hyperlink.address = c.AIR_URL


def bar(s, title, detail, y=5.32, h=.60):
    panel(s, .69, y, 11.94, h, LOG)
    text(s, title, .89, y+.08, 2.0, h-.16, 15, LOG, True)
    text(s, detail, 3.01, y+.06, 9.38, h-.12, 14.5, INK)
