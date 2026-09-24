"""C: Zoom into custody and the two concrete RSA uses."""
import common as c


def build(prs):
    s=c.page(prs,'C','From protected keys to model access',
             'C focuses on the distinction between a derived RSA sealing key, the random RSA '
             'private key, and fresh model-encryption keys. Other dstack paths remain visible '
             'at the bottom. Protects is a sealing relation, not RSA key generation.')
    c.panel(s,.65,1.76,2.36,1.05,c.INK)
    c.text(s,'dstack',.82,1.89,2.02,.40,22,c.INK,True)
    c.text(s,'GetKey(path)',.82,2.40,2.02,.25,14)
    c.route(s,[(3.07,2.285),(3.57,2.285)],c.PURPLE,2)
    c.panel(s,3.63,1.76,2.87,1.05,c.PURPLE)
    c.text(s,'AES-GCM key',3.80,1.91,2.53,.35,18,c.PURPLE,True)
    c.text(s,'Derived with HKDF',3.80,2.40,2.53,.25,14)
    c.text(s,'Seal / restore',6.61,1.88,1.39,.27,12.5,c.PURPLE)
    c.route(s,[(6.56,2.285),(8.06,2.285)],c.PURPLE,2)
    c.panel(s,8.12,1.76,4.56,1.05,c.PURPLE)
    c.text(s,'Random RSA-3072 key',8.31,1.91,4.18,.35,21,c.PURPLE,True)
    c.text(s,'Stored as sealed private-key state',8.31,2.40,4.18,.25,14)

    c.route(s,[(10.40,2.86),(10.40,3.08),(5.865,3.08),(5.865,3.31)],c.PURPLE,2)
    c.route(s,[(10.695,3.08),(10.695,3.31)],c.PURPLE,2)
    c.route(s,[(10.40,3.08),(10.695,3.08)],c.PURPLE,2,False)
    c.panel(s,4.10,3.36,3.53,1.21,c.PURPLE,c.WHITE)
    c.text(s,'Sign model packages',4.23,3.53,3.27,.39,18,c.PURPLE,True)
    c.text(s,'Recipients verify the sender',4.28,4.13,3.17,.27,14)
    c.panel(s,8.76,3.36,3.88,1.21,c.PURPLE,c.WHITE)
    c.text(s,'Unwrap the model key',8.94,3.53,3.52,.39,19,c.PURPLE,True)
    c.text(s,'Fresh AES key → decrypt model',8.94,4.13,3.52,.27,14)
    c.icon(s,'encryption',1.35,3.31,.66,c.PURPLE)
    c.text(s,'KEY PROTECTION\nAND MODEL ACCESS',.65,4.07,2.36,.61,14,c.PURPLE,True)

    c.text(s,'OTHER DSTACK PATHS',.65,4.98,3.60,.26,13,c.MUTED,True,False)
    c.panel(s,.65,5.39,5.78,.77,c.BLUE)
    c.text(s,'secp256k1 · protocol actions',.84,5.47,5.40,.27,16,c.BLUE,True)
    c.text(s,'Sign updates, aggregation and transactions',.84,5.84,5.40,.23,13.5)
    c.panel(s,6.70,5.39,5.98,.77,c.GREEN)
    c.text(s,'Ed25519 · inference and tool receipts',6.89,5.47,5.60,.27,16,c.GREEN,True)
    c.text(s,'Sello → transparency log · AIR → agent verification',6.89,5.84,5.60,.23,13)
    return s
