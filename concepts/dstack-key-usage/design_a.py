"""A: Three explicit key-to-use lanes."""
import common as c


def build(prs):
    s=c.page(prs,'A','Which key does what?',
             'A uses three horizontal paths from dstack to operational uses. '
             'The central lane explicitly distinguishes the derived sealing key from the random RSA key.')
    c.text(s,'APPLICATION-BOUND\nKEY MATERIAL',.65,2.03,2.26,.63,14,c.MUTED,True)
    c.panel(s,.65,3.07,2.26,1.49,c.INK)
    c.icon(s,'key',1.42,3.23,.70,c.INK,c.TINT[c.INK])
    c.text(s,'dstack',.83,3.77,1.90,.38,23,c.INK,True)
    c.text(s,'GetKey(path)',.83,4.23,1.90,.25,14)
    c.route(s,[(2.96,3.82),(3.25,3.82)],c.MUTED,1.8,False)
    c.route(s,[(3.25,2.25),(3.25,5.47)],c.MUTED,1.8,False)
    for y,h,color in [(1.60,1.30,c.BLUE),(3.14,1.43,c.PURPLE),(4.82,1.30,c.GREEN)]:
        c.panel(s,3.63,y,9.05,h,color,c.WHITE)
        c.route(s,[(3.25,y+h/2),(3.59,y+h/2)],color)

    c.text(s,'PROTOCOL ACTIONS',3.88,1.74,4.10,.25,14,c.BLUE,True,False)
    c.pill(s,'secp256k1',3.88,2.17,2.30,c.BLUE,17,.45)
    c.route(s,[(6.25,2.40),(6.72,2.40)],c.BLUE)
    c.text(s,'Sign update commitments / aggregation statements\nAuthorize blockchain transactions',
           6.90,2.08,5.50,.64,14,c.INK,False,False)

    c.text(s,'PROTECT THE RSA KEY, THEN USE IT',3.88,3.28,7.87,.25,14,c.PURPLE,True,False)
    c.pill(s,'AES-GCM',3.88,3.83,1.87,c.PURPLE,16,.43)
    c.text(s,'Derived sealing key',3.77,4.31,2.09,.21,12.5,c.MUTED)
    c.text(s,'Seal / restore',5.78,3.56,1.10,.26,12,c.PURPLE)
    c.route(s,[(5.82,4.04),(6.76,4.04)],c.PURPLE)
    c.pill(s,'RSA-3072',6.81,3.83,1.84,c.PURPLE,16,.43)
    c.text(s,'Randomly generated',6.66,4.31,2.14,.21,12.5,c.MUTED)
    c.route(s,[(8.71,4.04),(9.20,4.04)],c.PURPLE)
    c.text(s,'Sign model packages\nUnwrap model keys',9.35,3.76,3.10,.62,15,c.INK,False,False)

    c.text(s,'INFERENCE AND TOOL RECEIPTS',3.88,4.96,7.87,.25,14,c.GREEN,True,False)
    c.pill(s,'Ed25519 keys',3.88,5.31,2.53,c.GREEN,17,.45)
    c.text(s,'Separate paths',3.98,5.84,2.33,.20,12.5,c.MUTED)
    c.route(s,[(6.48,5.535),(6.90,5.535)],c.GREEN)
    c.text(s,'Sello · tool receipts → transparency log\nAIR · inference evidence → agent verification',
           7.02,5.24,5.41,.64,14.5,c.INK,False,False)
    return s
