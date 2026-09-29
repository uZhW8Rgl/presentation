"""Concrete test actions and verification targets for the three slide proposals."""

DESCRIPTIONS = [
    ['Vier Testfragen mit konkreten Antworten', '5 / 2 / 0 Uploads und der jeweilige Abschluss', 'Unberechtigte Aufrufe mit erwarteter Ablehnung', 'Log-, AIR/TDX- und Sello-Prüfungen benannt'],
    ['Die einzelnen Testfälle direkt vergleichbar', 'Testeingriff oder geladener Nachweis links', 'Tatsächlich geprüfte Eigenschaft rechts', 'Empfehlung für die genaue Testabdeckung'],
    ['Vier getrennte Prüfpfade von links nach rechts', 'Eingriff / Evidenz → System → Prüfergebnis', 'Auch beim Audit ist der Prüfweg sichtbar', 'Geeignet für die mündliche Erklärung'],
]


def context(a, s):
    a.txt(s, 'Phala · 6 workers · 5 successful training rounds per run · client limit 5 · timeout 45 s',
          .75, 1.49, 11.84, .28, 12, a.MUTED)


def footer(a, s):
    a.rule(s, .73, 5.91, 11.88)
    a.txt(s, 'Green = passed in these scenarios · Contracts: eth_call · Audit: shared verifier code + fresh Phala quote checks',
          .76, 5.93, 11.81, .18, 8.8, a.MUTED)
    a.txt(s, '25 Sep: recovery · 29 Sep: collection / security / audit · Separate runs; same images, changed provisioning configuration',
          .76, 6.11, 11.81, .17, 8.6, a.MUTED)


def badge(a, s, value, x, y, w=1.30):
    a.tag(s, value, x, y, w, a.GREEN, a.GREEN_TINT)


def card(a, s, x, y, w, h, label, question, status):
    a.box(s, x, y, w, h)
    a.txt(s, label, x+.16, y+.11, w-1.75, .22, 9.4, a.MUTED, True)
    badge(a, s, status, x+w-1.47, y+.09, 1.30)
    a.txt(s, question, x+.16, y+.42, w-.32, .31, 15.1, a.INK, True)


def design_a(p, a):
    s = a.page(p, 'A', 'External tests: four questions, concrete answers')
    context(a, s)
    x1, x2, w = .73, 6.80, 5.82
    card(a,s,x1,1.88,w,1.77,'01  COLLECTION / TIMEOUT','When are the received updates processed?','3 / 3 PASS')
    for i,(stimulus,result) in enumerate([
        ('Allow all 5 uploads', 'Close early: 16 s'),
        ('Allow 2 uploads; block 3', 'Close at timeout: 45 s'),
        ('Zero: block all 5 uploads', 'No empty publication'),
    ]):
        y=2.68+i*.28
        a.txt(s,stimulus,x1+.16,y,3.02,.25,12.2)
        a.txt(s,'→',x1+3.14,y,.22,.25,12,a.MUTED,center=True)
        a.txt(s,result,x1+3.43,y,2.24,.25,11.9,a.GREEN,True)
    card(a,s,x2,1.88,w,1.77,'02  AGGREGATOR RECOVERY','Can voting recover a stopped aggregator?','PASS')
    a.txt(s,'Stop the aggregator CVM; send timeout reports.',x2+.16,2.67,w-.32,.26,12.2)
    a.txt(s,'1–2 reports: keep state → 3 of 5: abort + reselect',x2+.16,2.95,w-.32,.26,12.0,a.GREEN,True)
    a.txt(s,'Resume: 5 successful rounds; all 6 workers participate.',x2+.16,3.25,w-.32,.25,11.6)

    card(a,s,x1,3.80,w,2.05,'03  ACCESS / CONTRACT GUARDS','Are unauthorized actions rejected?','16 / 16 PASS')
    a.txt(s,'No / wrong credentials → 10 requests return HTTP 401',x1+.16,4.57,w-.32,.25,11.8,a.GREEN,True)
    a.txt(s,'UI · Control · model download · job lookup / execution',x1+.16,4.85,w-.32,.24,11.3)
    a.txt(s,'Stale round · wrong aggregator · unknown action key\nNon-owner policy change → 4 expected eth_call reverts',x1+.16,5.11,w-.32,.47,11.6)
    a.txt(s,'Config unchanged · authorized inference passed',x1+.16,5.61,w-.32,.20,11.2,a.GREEN,True)

    card(a,s,x2,3.80,w,2.05,'04  PUBLISHED EVIDENCE AUDIT','Can receipts from the log be verified again?','17 / 17 PASS')
    lines = [
        ('SCITT', 'Statement signatures + log inclusion'),
        ('AIR / TDX', 'Signature; model / input / output hashes'),
        ('', 'Quote; RTMR3 replay + image policy'),
        ('Sello', 'Signature; owner permission + tool input / output'),
        ('Sessions', 'Attested receiver keys + session bindings'),
    ]
    for i,(label,body) in enumerate(lines):
        y=4.57+i*.245
        a.txt(s,label,x2+.16,y,1.01,.23,11.1,a.INK,True)
        a.txt(s,body,x2+1.25,y,w-1.41,.23,11.05)
    footer(a,s)


def design_b(p, a):
    s=a.page(p,'B','External test catalogue: intervention and assertion')
    context(a,s)
    a.box(s,.73,1.86,11.88,.34,a.INK,a.INK)
    for value,x,w in [('TEST AREA',.88,1.68),('TEST INPUT / INTERVENTION',2.87,4.45),('WHAT WAS VERIFIED',7.80,4.60)]:
        a.txt(s,value,x,1.91,w,.22,10.2,a.WHITE,True)
    groups=[
        (2.24,.83,'COLLECTION','3 / 3',[
            ('Allow 5 of 5 client uploads', '5 inputs; close before timeout at 16 s'),
            ('Allow 2; block the other 3 uploads', '2 inputs; close at the 45 s timeout'),
            ('Zero: block all 5 uploads', 'No empty publication; then 3/5 quorum recovery'),
        ]),
        (3.13,.59,'RECOVERY','PASS',[
            ('Stop aggregator CVM; submit reports 1 → 2 → 3', 'State preserved at 1–2; replacement at 3 of 5'),
            ('Continue training with the replacement aggregator', '5 successful rounds; all 6 workers participate'),
        ]),
        (3.78,1.10,'ACCESS /\nCONTRACTS','16 / 16',[
            ('No / wrong credentials: UI / Control / model / job / run', '10 × HTTP 401; config unchanged'),
            ('Stale round / wrong aggregator', '2 calls rejected: expected eth_call reverts'),
            ('Unregistered action key / non-owner policy change', '2 calls rejected: expected eth_call reverts'),
            ('Run the regular authorized agent workflow', 'Authorized inference passed'),
        ]),
        (4.94,.92,'RECEIPT\nAUDIT','17 / 17',[
            ('Download SCITT statements + inclusion receipts', 'Publisher signatures + inclusion under pinned log key'),
            ('Re-verify AIR and its TDX evidence', 'Model / input / output hashes; quote, RTMR3 + image'),
            ('Re-verify Sello receipts + attested sessions', 'Signatures, owner permission, tool I/O + receiver keys'),
        ]),
    ]
    for i,(y,h,label,status,rows) in enumerate(groups):
        a.box(s,.73,y,11.88,h,a.PALE if i%2==0 else a.WHITE,a.LINE)
        a.box(s,.73,y,1.96,h,a.GREEN_TINT,a.GREEN_TINT)
        a.txt(s,label,.88,y+.09,1.65,.40 if '\n' in label else .23,11.5,a.INK,True)
        a.txt(s,status+' PASS' if status!='PASS' else status,.88,y+h-.28,1.62,.23,11.0,a.GREEN,True)
        for j,(intervention,assertion) in enumerate(rows):
            yy=y+.08+j*.245
            a.txt(s,intervention,2.87,yy,4.62,.24,11.0)
            a.txt(s,assertion,7.80,yy,4.63,.24,10.75,a.GREEN,False)
    footer(a,s)


def arrow(a,s,x1,y,x2):
    a.b.add_line_segment(s,x1,y,x2,y,color=a.MUTED,width=1.4,arrow=True)


def lane(a,s,y,label,status,left_title,left_body,middle_title,middle_body,right_title,right_body,h=.79):
    a.box(s,.73,y,1.65,h,a.PALE,a.PALE)
    a.txt(s,label,.87,y+.10,1.39,.44,11.2,a.INK,True)
    a.txt(s,status,.87,y+h-.27,1.38,.21,10.0,a.GREEN,True)
    blocks=[(2.57,3.42,left_title,left_body,False),(6.23,2.39,middle_title,middle_body,False),(8.87,3.74,right_title,right_body,True)]
    for x,w,title,body,passed in blocks:
        a.box(s,x,y,w,h,a.GREEN_TINT if passed else a.WHITE,a.LINE)
        a.txt(s,title,x+.13,y+.09,w-.26,.23,11.9,a.GREEN if passed else a.INK,True)
        a.txt(s,body,x+.13,y+.36,w-.26,h-.40,10.75,a.INK)
    arrow(a,s,6.03,y+h/2,6.18)
    arrow(a,s,8.67,y+h/2,8.82)


def design_c(p,a):
    s=a.page(p,'C','External tests: follow the path to the assertion')
    context(a,s)
    for title,x,w in [('TEST AREA',.85,1.5),('INJECT / RETRIEVE',2.69,3.1),('EXERCISE / VERIFY',6.36,2.15),('CHECK THE RESULT',9.0,3.40)]:
        a.txt(s,title,x,1.87,w,.22,9.6,a.MUTED,True)
    lane(a,s,2.13,'COLLECTION','3 / 3 PASS',
         'Allow 5 / 2 / zero uploads','Block the remaining client uploads',
         'Aggregator','Client limit 5 · timeout 45 s',
         'Collection follows inputs + timeout','5: close at 16 s · 2: close at 45 s\nZero: no empty publication',.81)
    lane(a,s,3.01,'RECOVERY','PASS',
         'Stop the aggregator CVM','Submit 1 → 2 → 3 timeout reports',
         'Quorum vote','3 of 5 eligible workers',
         'State preserved until quorum','1–2: unchanged · 3: abort + reselect\nResume 5 rounds with all 6 workers',.81)
    lane(a,s,3.89,'ACCESS /\nCONTRACTS','16 / 16 PASS',
         'Send unauthorized calls','No / wrong credentials\nStale round / wrong aggregator\nUnknown key / non-owner policy change',
         'API + contract guards','UI · Control · inference APIs\nContract probes via eth_call',
         '10 × HTTP 401 + 4 expected reverts','Config unchanged;\nauthorized inference passed',1.03)
    lane(a,s,4.99,'RECEIPT\nAUDIT','17 / 17 PASS',
         'Download published evidence','SCITT · AIR/TDX · Sello · sessions',
         'Re-run verification','Signatures + log inclusion\nTDX quote, RTMR3 + image',
         'Evidence binds the recorded action','Model / input / output hashes;\nowner permission + receiver / session',.90)
    footer(a,s)
