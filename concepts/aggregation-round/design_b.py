"""B: A concrete model flow with visible frozen-input completeness."""
import common as c


def build(prs):
    s=c.page(prs,'B','One fixed input set becomes one global model',
             'B follows the model data. Three workers are an illustration, not the measured '
             'experiment configuration. All accepted files must be present and hash-matched. '
             'The mean uses every accepted model with equal weight; signed publication follows IPFS upload.')
    c.text(s,'CLOSED INPUT SET',.65,1.55,3.05,.30,15,c.GREEN,True)
    c.panel(s,.65,2.03,3.05,3.59,c.GREEN,c.WHITE)
    for index,worker in enumerate(['A','B','C']):
        y=2.37+index*.80
        c.model(s,.89,y,.58,.61)
        c.text(s,'Worker '+worker,1.64,y+.01,1.64,.29,16,c.GREEN,True,False)
        c.text(s,'Hash matched',1.64,y+.37,1.64,.24,13,c.INK,False,False)
    c.text(s,'3 accepted\n3 must be used',.87,4.87,2.61,.60,15,c.GREEN,True)
    c.text(s,'Example: three accepted models',.65,5.79,3.05,.26,12.5,c.MUTED)
    c.route(s,[(3.76,3.43),(4.40,3.43)],c.GREEN,2)

    c.b.add_oval(s,4.47,2.35,2.28,2.28,c.TINT[c.GREEN],c.GREEN,1.7)
    c.text(s,'FedAvg',4.64,2.88,1.94,.45,25,c.GREEN,True)
    c.text(s,'Average each\nparameter',4.67,3.48,1.88,.64,16,c.INK)
    c.text(s,'Equal weight per model',4.16,1.80,2.90,.28,14,c.GREEN)
    c.route(s,[(6.81,3.43),(7.45,3.43)],c.GREEN,2)
    c.model(s,7.51,2.93,.88,1.00)
    c.text(s,'Global\nmodel',7.34,4.03,1.22,.64,16,c.GREEN,True)
    c.route(s,[(8.45,3.43),(9.70,3.43)],c.PURPLE,2)
    c.text(s,'Encrypt',8.44,3.04,1.23,.27,13,c.PURPLE)
    c.panel(s,9.76,2.71,2.92,1.45,c.PURPLE)
    c.text(s,'IPFS',9.95,2.88,2.54,.37,22,c.PURPLE,True)
    c.text(s,'Encrypted model bundle\nSignature + recipient keys',9.95,3.47,2.54,.55,13.5)

    # IPFS returns references; the aggregator signs and submits the final transaction.
    c.route(s,[(11.22,4.21),(11.22,4.70),(6.02,4.70),(6.02,5.10)],c.PURPLE,1.8)
    c.text(s,'Three IPFS CIDs',8.67,4.34,2.36,.26,13,c.PURPLE)
    c.panel(s,4.28,5.15,3.50,.89,c.GREEN)
    c.text(s,'Aggregator signs',4.47,5.26,3.12,.32,18,c.GREEN,True)
    c.text(s,'Inputs · rule · output · CIDs',4.47,5.72,3.12,.23,13)
    c.route(s,[(7.84,5.595),(9.11,5.595)],c.PURPLE,2)
    c.text(s,'One tx',7.87,5.19,1.21,.26,13,c.PURPLE)
    c.panel(s,9.17,5.15,3.51,.89,c.PURPLE)
    c.text(s,'Blockchain finalizes',9.34,5.26,3.17,.32,17,c.PURPLE,True)
    c.text(s,'Check signature · publish · advance',9.31,5.72,3.23,.23,12.5)
    return s
