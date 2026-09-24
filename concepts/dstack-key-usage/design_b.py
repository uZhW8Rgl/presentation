"""B: Keys attached to concrete lifecycle operations."""
import common as c


def build(prs):
    s=c.page(prs,'B','Keys at work across the lifecycle',
             'B organizes the slide around operations rather than the derivation tree. '
             'Each stage names both the key and its practical responsibility. '
             'The timeline orders concerns, not key provisioning or every protocol message.')
    c.pill(s,'dstack · separate derivation paths',3.21,1.57,6.91,c.INK,17,.49)
    stages=[(2.36,c.BLUE,'blockchain','Coordinate DFL'),
            (6.67,c.PURPLE,'encryption','Exchange models'),
            (10.98,c.GREEN,'attestation','Prove model use')]
    for cx,color,icon,title in stages:
        c.icon(s,icon,cx-.34,2.30,.68,color)
        c.text(s,title,cx-1.77,3.09,3.54,.41,21,color,True)
    c.route(s,[(2.86,2.66),(6.13,2.66)],c.MUTED,2)
    c.route(s,[(7.20,2.66),(10.45,2.66)],c.MUTED,2)
    c.text(s,'Sign update commitments\nFinalize aggregation',.63,3.72,3.46,.71,17)
    c.text(s,'Sign model packages\nUnwrap model-encryption keys',4.65,3.72,4.04,.71,16)
    c.text(s,'Sign tool receipts\nSign inference evidence',9.13,3.72,3.69,.71,17)
    c.pill(s,'secp256k1',.73,4.70,3.25,c.BLUE,19,.47)
    c.pill(s,'RSA-3072',4.91,4.70,3.51,c.PURPLE,19,.47)
    c.pill(s,'Ed25519 · separate keys',9.15,4.70,3.66,c.GREEN,16,.47)
    c.text(s,'Authorize the participant’s\nblockchain transactions',.68,5.41,3.36,.63,15,c.MUTED)
    c.text(s,'Derived AES-GCM key\nseals the random RSA private key',4.63,5.41,4.08,.63,14.5,c.MUTED)
    c.text(s,'Sello → transparency log\nAIR → agent verification',9.17,5.41,3.62,.63,15,c.MUTED)
    return s
