#!/usr/bin/env python3
"""Four lifecycle variants based on A1/A2, with Blockchain and IPFS."""

from __future__ import annotations

import hashlib
from pathlib import Path
import sys

from PIL import Image, ImageDraw, ImageFont

HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent
ROOT=HERE.parents[2]
sys.path.insert(0,str(SOURCE/'a-variants'))
import build_variants as a

c=a.c
INFRA_NOTES=(
    'Blockchain and IPFS are parallel publication and retrieval sources, not a serial pipeline. '
    'The active aggregator publishes the finalized model reference to the blockchain and the encrypted '
    'model bundle and associated artifacts to IPFS. Arrows from the global or published model summarize '
    'this publication by the aggregator, rather than assigning agency to a model file. '
    'The inference receiver independently resolves the authoritative reference and retrieves the artifacts. '
    'Outgoing arrows from the stores represent information consumed by inference; retrieval is initiated by the receiver. '
    'The blockchain also coordinates DFL membership and rounds; IPFS also carries training artifacts. '
    'Those interactions remain abstracted inside the DFL circle on this lifecycle overview. '
    'The transparency log is separate from the blockchain and stores the receiver-issued tool receipt. '
    'A grouping frame denotes one conceptual publication, not one deployed service or trust boundary.'
)


def page(prs,code,description):
    s=c.page(prs,code,a.TITLE,description)
    c.b.add_note(s,description+'\n\n'+c.COMMON_NOTES+'\n\n'+INFRA_NOTES)
    return s


def infra_card(s,title,detail,cx,cy,width=2.18,height=.90):
    shape=c.box(s,cx-width/2,cy-height/2,width,height,c.PURPLE,c.WHITE,1.3)
    shape.name='Infrastructure: '+title
    c.text(s,title,cx-width/2+.08,cy-.34,width-.16,.36,18,c.PURPLE,True)
    c.text(s,detail,cx-width/2+.08,cy+.10,width-.16,.28,13,c.PURPLE)


def model_symbol(s,cx,cy,label_above=False):
    c.circle(s,cx,cy,.40,c.PURPLE,c.TINT[c.PURPLE],1.2)
    c.model_icon(s,cx,cy,.70)
    c.text(s,'Published\nmodel',cx-.87,cy-1.15 if label_above else cy+.54,
           1.74,.72,17,c.PURPLE,True)


def use_path(s,ix=9.02,y=4.15,lx=11.85,agent_y=1.98):
    c.pill(s,'Attested\ninference',ix,y,1.98,c.BLUE,20,1.05)
    a.agent_above(s,ix,y,agent_y)
    c.route(s,[(ix+1.04,y),(lx-.56,y)],c.BLUE,2.1)
    gap=lx-ix-1.60
    if gap<1.10:
        c.text(s,'Tool\nreceipt',ix+1.12,y-.84,gap,.67,13,c.BLUE)
    else:
        c.text(s,'Tool receipt',ix+1.08,y-.51,gap,.33,13,c.BLUE)
    c.icon_node(s,'log','Transparency\nlog',lx,y,c.BLUE,18)


def variant_a1a(prs):
    s=page(prs,'A1a','A1a: One published-model field with two explicit sources. '
           'The model symbol and header group Blockchain and IPFS into one publication; each source feeds inference separately.')
    y=4.15
    panel=c.box(s,4.70,1.77,2.62,3.89,c.PURPLE,'F8F5FB',.85)
    panel.name='Conceptual publication grouping'
    c.circle(s,6.01,2.31,.37,c.PURPLE,c.TINT[c.PURPLE],1.0)
    c.model_icon(s,6.01,2.31,.63)
    c.text(s,'Model\npublication',4.85,2.71,2.32,.64,16,c.PURPLE,True)
    end=a.loop_with_model_exit(s,2.25,y,1.25)
    c.route(s,[end,(4.61,y)],c.PURPLE,2.1,False)
    for sy in [3.84,4.95]:
        c.route(s,[(4.61,y),(4.61,sy),(4.88,sy)],c.PURPLE,2.1)
    infra_card(s,'Blockchain','Model reference',6.01,3.84)
    infra_card(s,'IPFS','Model files',6.01,4.95)
    c.route(s,[(7.14,3.84),(7.70,3.84),(7.70,3.91),(7.98,3.91)],c.PURPLE,2.1)
    c.route(s,[(7.14,4.95),(7.70,4.95),(7.70,4.41),(7.98,4.41)],c.PURPLE,2.1)
    use_path(s)
    return s


def variant_a1b(prs):
    s=page(prs,'A1b','A1b: Keep the published-model symbol as a separate handoff. '
           'Its publication branches to Blockchain and IPFS, then both sources converge on inference.')
    y=4.15
    end=a.loop_with_model_exit(s,2.25,y,1.25)
    c.route(s,[end,(4.72,y)],c.PURPLE,2.1)
    model_symbol(s,5.17,y,True)
    for sy in [3.10,5.20]:
        c.route(s,[(5.62,y),(5.99,sy)],c.PURPLE,2.1)
    infra_card(s,'Blockchain','Model reference',7.00,3.10,1.94)
    infra_card(s,'IPFS','Model files',7.00,5.20,1.94)
    c.route(s,[(8.01,3.10),(8.30,3.89)],c.PURPLE,2.1)
    c.route(s,[(8.01,5.20),(8.30,4.41)],c.PURPLE,2.1)
    use_path(s,9.34,y,11.95)
    return s


def variant_a2a(prs):
    s=page(prs,'A2a','A2a: Compact split handoff. The global model at the circle boundary is published '
           'into Blockchain and IPFS; their reference and artifact paths feed inference separately.')
    y=4.15
    end=a.loop_with_model_exit(s,2.25,y,1.25,c.PURPLE)
    c.route(s,[end,(4.66,y)],c.PURPLE,2.1,False)
    for sy in [3.36,4.95]:
        c.route(s,[(4.66,y),(4.66,sy),(4.99,sy)],c.PURPLE,2.1)
    infra_card(s,'Blockchain','Model reference',6.13,3.36)
    infra_card(s,'IPFS','Model files',6.13,4.95)
    c.route(s,[(7.26,3.36),(7.71,3.36),(7.71,3.90),(8.03,3.90)],c.PURPLE,2.1)
    c.route(s,[(7.26,4.95),(7.71,4.95),(7.71,4.40),(8.03,4.40)],c.PURPLE,2.1)
    use_path(s,9.07,y,11.89)
    return s


def variant_a2b(prs):
    s=page(prs,'A2b','A2b: Blockchain and IPFS form a shared infrastructure band below the lifecycle. '
           'Publication reaches each store from below; their reference and model-file outputs enter inference from above the band. '
           'There is no direct model transfer bypassing these sources.')
    y=3.92
    c.box(s,4.62,4.80,4.29,1.07,c.PURPLE,'F8F5FB',.85)
    end=a.loop_with_model_exit(s,2.22,y,1.15,c.PURPLE)
    s.shapes[-1].left-=c.b.Inches(.15)
    # Publication runs below the infrastructure so it does not intersect retrieval.
    c.route(s,[end,(4.48,y),(4.48,6.00)],c.PURPLE,2.0,False)
    c.text(s,'Publish',4.62,4.03,1.16,.33,16,c.PURPLE)
    for cx in [5.73,7.93]:
        c.route(s,[(4.48,6.00),(cx,6.00),(cx,5.85)],c.PURPLE,2.0)
    infra_card(s,'Blockchain','Model reference',5.73,5.35,1.98,.90)
    infra_card(s,'IPFS','Model files',7.93,5.35,1.76,.90)
    c.route(s,[(5.73,4.86),(5.73,4.63),(8.69,4.63),(8.69,4.50)],c.PURPLE,2.1)
    c.route(s,[(7.93,4.86),(7.93,4.75),(9.43,4.75),(9.43,4.50)],c.PURPLE,2.1)
    use_path(s,9.06,y,11.87,1.85)
    return s


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    protected=[p for p in SOURCE.iterdir() if p.is_file()]
    protected.extend(p for p in (SOURCE/'a-variants').iterdir() if p.is_file())
    protected.append(ROOT/'VITA-FL_Thesis_Presentation_TU_Berlin.pptx')
    before={p:digest(p) for p in protected}
    prs=c.b.prepare_template()
    prs.core_properties.title='VITA-FL — Lifecycle with Blockchain and IPFS'
    slides=[variant_a1a(prs),variant_a1b(prs),variant_a2a(prs),variant_a2b(prs)]
    destination=HERE/'VITA-FL_Lifecycle_Blockchain_IPFS.pptx'
    prs.save(destination)
    names=['a1a-publication-field','a1b-two-stores','a2a-split-handoff','a2b-shared-infrastructure']
    previews=[]
    for name,slide in zip(names,slides):
        preview=c.renderer.render_slide(prs,slide)
        preview.save(HERE/(name+'.png'))
        previews.append(preview)
    w,h,gutter,caption=1000,563,30,53
    sheet=Image.new('RGB',(2*w+3*gutter,2*(h+caption)+3*gutter),'#E9EDF0')
    draw=ImageDraw.Draw(sheet)
    font=ImageFont.truetype('/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf',25)
    labels=['A1a · Gemeinsamer Veröffentlichungsbereich','A1b · Zwei Zweige am Modellsymbol',
            'A2a · Kompakte geteilte Übergabe','A2b · Gemeinsame Infrastruktur darunter']
    for i,(preview,label) in enumerate(zip(previews,labels)):
        x=gutter+(i%2)*(w+gutter)
        y=gutter+(i//2)*(h+caption+gutter)
        draw.text((x+5,y+8),label,font=font,fill='#263440')
        sheet.paste(preview.resize((w,h),Image.Resampling.LANCZOS),(x,y+caption))
    sheet.save(HERE/'overview.png')
    assert all(digest(p)==value for p,value in before.items()), 'A retained original changed'
    print('Four editable Blockchain/IPFS lifecycle variants created; retained originals unchanged.')
    print(destination)


if __name__=='__main__':
    main()
