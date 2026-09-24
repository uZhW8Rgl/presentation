"""A: Actors and the round's cross-boundary messages."""
import common as c


def build(prs):
    s=c.page(prs,'A','Who does what during aggregation?',
             'A follows the actors. Worker packages go directly to the aggregator, '
             'commitments and closure are on chain, computation stays in the TEE, '
             'and IPFS holds the encrypted publication before finalization.')
    for x,w,label,color in [(.65,2.04,'Workers',c.GREEN),
                             (3.11,3.12,'Aggregator TEE',c.GREEN),
                             (6.87,2.15,'IPFS',c.PURPLE),
                             (9.58,3.10,'Blockchain',c.PURPLE)]:
        c.text(s,label,x,1.57,w,.38,21,color,True)
    for x in [2.82,6.52,9.32]:
        c.b.add_line_segment(s,x,2.08,x,5.82,'DCE2E7',1,dashed=True)

    for index in range(3):
        c.model(s,.72+index*.55,2.38,.45,.56)
    c.text(s,'Signed, encrypted\nlocal models',.65,3.13,2.04,.61,15,c.INK)
    c.route(s,[(2.34,2.72),(3.05,2.72)],c.GREEN,2)
    c.panel(s,3.11,2.28,3.12,.91,c.GREEN)
    c.text(s,'Receive + verify',3.28,2.39,2.78,.34,17,c.GREEN,True)
    c.text(s,'Hashes and signatures',3.28,2.84,2.78,.24,13.5)
    c.route(s,[(6.29,2.735),(9.52,2.735)],c.PURPLE,1.8)
    c.text(s,'Record commitments',6.52,2.31,2.80,.27,13,c.PURPLE)
    c.panel(s,9.58,2.28,3.10,.91,c.PURPLE)
    c.text(s,'Accept commitments',9.75,2.39,2.76,.34,16,c.PURPLE,True)
    c.text(s,'Worker · model hash',9.75,2.84,2.76,.24,13.5)

    c.route(s,[(11.13,3.23),(11.13,3.53)],c.PURPLE)
    c.panel(s,9.58,3.58,3.10,.91,c.PURPLE)
    c.text(s,'Aggregator closes',9.75,3.69,2.76,.34,16,c.PURPLE,True)
    c.text(s,'Freeze fingerprint + count',9.72,4.14,2.82,.24,13)
    c.route(s,[(9.52,4.035),(6.29,4.035)],c.PURPLE,1.8)
    c.text(s,'Frozen input set',6.52,3.61,2.80,.27,13,c.PURPLE)
    c.panel(s,3.11,3.58,3.12,.91,c.GREEN)
    c.text(s,'Check input set',3.28,3.69,2.78,.34,15.5,c.GREEN,True)
    c.text(s,'Exact files + exact count',3.28,4.14,2.78,.24,13)
    c.route(s,[(4.67,4.53),(4.67,4.76)],c.GREEN)

    c.panel(s,3.11,4.81,3.12,.99,c.GREEN)
    c.text(s,'Compute FedAvg',3.28,4.91,2.78,.32,16.5,c.GREEN,True)
    c.text(s,'Equal mean per parameter\nEncrypt + sign output',3.28,5.27,2.78,.47,13)
    c.route(s,[(6.29,5.12),(6.81,5.12)],c.PURPLE)
    c.panel(s,6.87,4.81,2.15,.99,c.PURPLE)
    c.text(s,'Store bundle',7.02,4.91,1.85,.32,16,c.PURPLE,True)
    c.text(s,'Model · signature\nrecipient keys',7.02,5.29,1.85,.43,12.8)
    c.panel(s,9.58,4.81,3.10,.99,c.PURPLE)
    c.text(s,'Finalize round',9.75,4.91,2.76,.32,17,c.PURPLE,True)
    c.text(s,'Verify signed statement\nPublish CIDs · advance',9.75,5.27,2.76,.47,13)
    c.route(s,[(4.67,5.85),(4.67,6.16),(11.13,6.16),(11.13,5.85)],c.PURPLE,2)
    c.text(s,'Signed statement + IPFS CIDs · one transaction',
           5.13,5.85,5.63,.24,13,c.PURPLE)
    return s
