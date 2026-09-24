"""B: aligned mappings from cited source to concrete implementation."""
import common as c


def row(s, y, label, left, right, *, height=.73):
    c.label(s, label, .74, y+.16, 1.93, c.INK)
    c.panel(s, 2.78, y, 4.22, height, c.INK)
    c.text(s, left, 2.96, y+.06, 3.86, height-.12, 16.5, center=True)
    c.route(s, [(7.06,y+height/2),(7.64,y+height/2)], c.BLUE)
    c.panel(s, 7.70, y, 4.94, height, c.BLUE)
    c.text(s, right, 7.90, y+.06, 4.54, height-.12, 16.5, c.BLUE, center=True)


def build_sello(prs):
    s = c.page(prs, 'B · Sello', 'Sello: from receiver receipts to VITA-FL', 'sello')
    c.text(s, 'FIGUERA · SELLO', 2.79, 1.66, 4.21, .38, 19, c.INK, True, True)
    c.text(s, 'VITA-FL IMPLEMENTATION', 7.70, 1.66, 4.94, .38, 19, c.BLUE, True, True)
    row(s, 2.22, 'SIGNER', 'Receiving service', 'dstack key + DeviceRegistry admission')
    row(s, 3.09, 'CONTENT', 'Encrypted action I/O commitments', 'Model fetch · Image pick · Inference')
    row(s, 3.96, 'LOG / OWNER', 'Witnessed log\nIndependent owner discovery', 'SCITT inclusion; agent decrypts\nNo witnesses / independent discovery')
    c.panel(s, .69, 4.91, 11.95, .44, c.BLUE)
    c.text(s, 'Added in VITA-FL: mandatory mTLS + scoped, certificate-bound tokens',
           .88, 4.95, 11.57, .35, 17, c.BLUE, True, True)
    c.text(s, 'Different trust boundary: owner and issuer secrets reside in the agent runtime.',
           .74, 5.53, 11.88, .35, 16, c.AMBER, True, True)
    c.source(s, 'sello')
    return s


def build_air(prs):
    s = c.page(prs, 'B · AIR', 'AIR: a receipt format inside a larger evidence path', 'air')
    c.text(s, 'AIR · DRAFT 02', 2.79, 1.66, 4.21, .38, 19, c.INK, True, True)
    c.text(s, 'VITA-FL IMPLEMENTATION', 7.70, 1.66, 4.94, .38, 19, c.BLUE, True, True)
    row(s, 2.22, 'INFERENCE', 'Model + request + response', 'DFL manifest + pixels + prediction')
    row(s, 3.09, 'SIGNATURE', 'COSE / CWT receipt\nAttestation-linked signing key', 'dstack Ed25519 key\nPer-call TDX REPORTDATA binding')
    row(s, 3.96, 'VERIFICATION', 'Receipt validation\nSeparate platform appraisal', 'Receipt + RTMR3 / Image Digest\nPer-call DCAP not implemented')
    c.panel(s, .69, 4.91, 11.95, .44, c.PURPLE)
    c.text(s, 'VITA-FL integration: agent publishes the complete evidence bundle to SCITT',
           .88, 4.95, 11.57, .35, 17, c.PURPLE, True, True)
    c.text(s, 'AIR-style: trust relies on the admitted receiver; recentness is not replay protection.',
           .74, 5.53, 11.88, .35, 16, c.AMBER, True, True)
    c.source(s, 'air')
    return s
