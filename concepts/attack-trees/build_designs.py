#!/usr/bin/env python3
"""Four Chapter-4 attack trees, each in three editable presentation looks."""
from copy import deepcopy
from pathlib import Path
import hashlib
import html
import json
import re
import sys

from PIL import Image, ImageDraw, ImageFont
from pptx import Presentation
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
CHAPTER=ROOT.parent/'overleaf/chapters/chapter4.tex'
MAIN=ROOT/'VITA-FL_Thesis_Presentation_TU_Berlin.pptx'
sys.path.insert(0,str(ROOT))
import build_presentation as b
import render_preview as renderer
sys.path.insert(0,str(ROOT/'concepts/color-navigation'))
from build_concepts import check_layout

INK,MUTED,WHITE,LINE='263440','65737D','FFFFFF','DCE3E8'
RED,BLUE,PURPLE,AMBER='C40D1E','1764A1','7446A6','9A6100'
PALE,BLUE_TINT,RED_TINT,AMBER_TINT='F2F5F7','EDF4FA','FBECEF','FFF5E5'
NAVY,DARK_CARD,DARK_LINE='172A3A','223E53','7096B3'
DATA=json.loads((HERE/'trees.json').read_text())
TREES=DATA['trees']
STYLES=[('a','A · Klassischer Baum','A_classic'),
        ('b','B · Horizontal auf dunklem Grund','B_horizontal'),
        ('c','C · Angriffspfade mit Grenzen','C_annotated')]

NOTES='''PURPOSE
Editable attack-tree proposals derived from Chapter 4, Security Model and System
Requirements. The chapter contains a threat catalogue and use/misuse cases, not
these attack trees. The goal decomposition and its grouping are an explanatory
synthesis for the presentation; they are not quoted thesis figures or a formal
completeness result. The chapter and main presentation are left unchanged.

HOW TO READ THE TREE
A parent is the attacker's goal or subgoal. OR means any one child is sufficient
for the modeled parent; AND means every child condition must hold together.
Edges are decomposition, not a chronological sequence or a message flow.
Attack leaves refer to hypothetical successful subgoals, not instructions for
exploiting a demonstrated implementation vulnerability. AND joins only joint
conditions, never an attack and the control designed to stop it.
Leaf T-identifiers refer to Chapter 4. Repeated T-identifiers represent different
facets or effects of the same threat, not additional threats. The four diagrams
together reference T1 through T14. They are intentionally selective abstractions;
not every attack described under each T-identifier is expanded into a leaf.

ASSURANCE BOUNDARY
Requirements F1–F11 and NF1–NF7 specify expected controls and claim limits; their
appearance here is not a claim of successful implementation, proof or test.
Residual risks and assumption failures remain distinct from attacks intended to
be rejected. In particular T7 concerns valid harmful data/updates, T13 breaks a
cryptographic/platform/key/governance premise, and T14 covers sufficient collusion.
A correct attestation/signature does not establish semantic truth or independent
organizational ownership. T10 allows whole-interaction suppression before a
receipt exists; T11 retains a split-view boundary without independent witnesses.
Targeted aggregator replacement does not establish availability of all services.
Style C separates requirement/limit annotations from the actual tree edges.
Amber highlights a stated residual or assumption boundary, not measured risk,
probability or attack severity. No numbers in these diagrams are risk scores.

VERSION SCOPE
The source is Chapter 4 as inspected for this task, including its stated legacy
per-inference attestation limitations. Newer RA-TLS/Phala verification code and
recent experiments are not silently substituted for the chapter's specification.
No experiment, exploitation, cloud call or change to Chapter 4 was performed.

SOURCE
Workspace-relative: overleaf/chapters/chapter4.tex.
Exact source fingerprint, threat/requirement references and modeling rationale
are stored alongside these slides in trees.json, source-map.json and README.md.
'''


def txt(s,value,x,y,w,h=.32,size=15,color=INK,bold=False,center=False):
    q=b.add_text(s,value,x,y,w,h,size,color,bold,
                 align=PP_ALIGN.CENTER if center else PP_ALIGN.LEFT,
                 valign=MSO_ANCHOR.MIDDLE,margin=0)
    q.name='Attack tree: '+value.replace('\n',' / ')
    return q


def box(s,x,y,w,h,fill=WHITE,border=LINE,radius=True,width=1):
    return b.add_box(s,x,y,w,h,fill=fill,line=border,radius=radius,line_width=width)


def path(s,points,color=INK,width=1.3,dashed=False):
    for start,end in zip(points,points[1:]):
        b.add_line_segment(s,*start,*end,color=color,width=width,dashed=dashed)


def gate(s,operator,cx,y,dark=False):
    assert operator in ('OR','AND')
    w=.52 if operator=='AND' else .43
    fill=AMBER_TINT if operator=='AND' else (DARK_CARD if dark else PALE)
    fg=AMBER if operator=='AND' else (WHITE if dark else INK)
    box(s,cx-w/2,y,w,.28,fill,AMBER if operator=='AND' else (DARK_LINE if dark else LINE),True,.85)
    txt(s,operator,cx-w/2+.025,y+.015,w-.05,.25,10.5,fg,True,True)


def page(prs,style,tree):
    s=b.new_content_slide(prs,len(prs.slides)+1,tree['title'],
                          f"CHAPTER 4 · ATTACK TREE {tree['number']} / 4 · LOOK {style.upper()}")
    b.add_domain_navigation(s,31,active_domains=set(tree['domains']))
    for q in s.shapes:
        if q.has_text_frame and q.text.startswith('Page '):
            q.text_frame.paragraphs[0].runs[0].text=f"{style.upper()} · Tree {tree['number']}"
            q.width=b.Inches(1.1)
    b.add_note(s,NOTES+'\nTREE-SPECIFIC MODEL\n'+json.dumps(tree,indent=2,ensure_ascii=False))
    return s


def leaf_text(leaf):
    return ' / '.join(leaf['threats'])+' · '+leaf['label']


def legend(s,annotation=False):
    text='OR = any child · AND = all children · T-identifiers refer to Chapter 4.'
    if annotation: text+='  Amber: residual risk or assumption boundary.'
    txt(s,text,.72,6.00,11.90,.27,11.1,MUTED)


def classic(prs,tree):
    s=page(prs,'a',tree)
    centers=[2.60,6.67,10.74]
    # Connectors precede native nodes, keeping branch geometry visible and clean.
    path(s,[(6.67,2.12),(6.67,2.69)])
    path(s,[(centers[0],2.69),(centers[-1],2.69)])
    for cx in centers: path(s,[(cx,2.69),(cx,2.89)])
    box(s,3.75,1.54,5.84,.59,RED,RED,True,1)
    txt(s,tree['goal'],3.93,1.61,5.48,.43,17,WHITE,True,True)
    gate(s,tree['operator'],6.67,2.28)
    for x,cx,branch in zip([.70,4.77,8.84],centers,tree['branches']):
        path(s,[(cx,3.55),(cx,3.78),(x+.16,3.78),(x+.16,5.19)])
        for y in (4.15,4.88): path(s,[(x+.16,y+.31),(x+.39,y+.31)])
        box(s,x,2.89,3.80,.66,PALE,LINE,True)
        txt(s,branch['label'],x+.14,2.96,3.52,.55,15.5,INK,True,True)
        gate(s,branch['operator'],cx,3.64)
        for y,leaf in zip((4.15,4.88),branch['leaves']):
            box(s,x+.39,y,3.41,.62,WHITE,LINE,True)
            txt(s,leaf_text(leaf),x+.52,y+.055,3.15,.51,13.5,INK)
    legend(s)


def horizontal(prs,tree):
    s=page(prs,'b',tree)
    box(s,.70,1.53,11.93,4.39,NAVY,NAVY,True,0)
    root_cy=3.78
    path(s,[(3.71,root_cy),(4.47,root_cy)],DARK_LINE,1.5)
    row_bases=[1.78,3.15,4.52]
    branch_centers=[y+.64 for y in row_bases]
    path(s,[(4.47,branch_centers[0]),(4.47,branch_centers[-1])],DARK_LINE)
    for cy in branch_centers: path(s,[(4.47,cy),(4.84,cy)],DARK_LINE)
    box(s,.94,3.12,2.77,1.32,RED,RED,True)
    txt(s,'ATTACKER GOAL',1.09,3.25,2.47,.23,10.5,WHITE,True)
    txt(s,tree['goal'],1.09,3.56,2.47,.70,16,WHITE,True)
    gate(s,tree['operator'],4.02,root_cy-.14,True)
    for y,branch in zip(row_bases,tree['branches']):
        cy=y+.64
        path(s,[(7.25,cy),(8.13,cy)],DARK_LINE)
        path(s,[(8.13,y+.29),(8.13,y+.99)],DARK_LINE)
        for ly in (y,y+.70): path(s,[(8.13,ly+.29),(8.45,ly+.29)],DARK_LINE)
        box(s,4.84,y+.28,2.41,.72,DARK_CARD,DARK_LINE,True,.85)
        txt(s,branch['label'],5.00,y+.335,2.09,.61,13.4,WHITE,True)
        gate(s,branch['operator'],7.65,cy-.14,True)
        for ly,leaf in zip((y,y+.70),branch['leaves']):
            box(s,8.45,ly,3.89,.58,DARK_CARD,DARK_LINE,True,.8)
            txt(s,leaf_text(leaf),8.60,ly+.04,3.59,.50,13.2,WHITE)
    legend(s)


def annotated(prs,tree):
    s=page(prs,'c',tree)
    centers=[2.60,6.67,10.74]
    path(s,[(6.67,2.14),(6.67,2.72)])
    path(s,[(centers[0],2.72),(centers[-1],2.72)])
    for cx in centers: path(s,[(cx,2.72),(cx,2.92)])
    box(s,.70,1.54,11.93,.60,RED_TINT,RED_TINT,False,0)
    txt(s,'ATTACKER GOAL',.93,1.72,1.83,.23,10.5,RED,True)
    txt(s,tree['goal'],2.95,1.635,9.40,.39,19,RED,True)
    gate(s,tree['operator'],6.67,2.30)
    for x,cx,branch in zip([.70,4.77,8.84],centers,tree['branches']):
        residual=branch['boundary'] in ('residual','assumption','mixed')
        color=AMBER if residual else BLUE
        tint=AMBER_TINT if residual else BLUE_TINT
        box(s,x,2.92,3.80,2.90,tint,tint,True,0)
        txt(s,branch['label'],x+.19,3.03,3.42,.53,15.5,color,True)
        path(s,[(cx,3.59),(cx,3.81),(x+.15,3.81),(x+.15,5.035)],color,1.2)
        for y in (4.00,4.73): path(s,[(x+.15,y+.305),(x+.36,y+.305)],color,1.2)
        gate(s,branch['operator'],cx,3.67)
        for y,leaf in zip((4.00,4.73),branch['leaves']):
            box(s,x+.36,y,3.25,.61,WHITE,WHITE,True,0)
            txt(s,leaf_text(leaf),x+.49,y+.05,2.99,.51,13.0,INK)
        path(s,[(x+.19,5.43),(x+3.61,5.43)],color,.6)
        txt(s,branch['annotation'],x+.19,5.49,3.42,.27,10.5,color)
    legend(s,True)


BUILDERS={'a':classic,'b':horizontal,'c':annotated}


def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_data():
    assert len(TREES)==4
    covered=set()
    chapter=CHAPTER.read_text()
    assert digest(CHAPTER)==DATA['source_sha256'], 'Chapter 4 changed: refresh the threat-tree source mapping before building'
    for tree in TREES:
        assert tree['operator']=='OR'
        assert len(tree['branches'])==3
        for branch in tree['branches']:
            assert branch['operator'] in ('OR','AND')
            assert len(branch['leaves'])==2
            assert branch['rationale'].strip()
            for leaf in branch['leaves']:
                assert leaf['label'].strip() and leaf['threats']
                for threat in leaf['threats']:
                    assert '\\threatSpecification{threat:'+threat+'}' in chapter
                    covered.add(threat)
            for ref in branch['requirements']:
                assert '{req:'+ref+'}' in chapter,ref
            for ref in branch['assumptions']:
                assert '{assumption:'+ref+'}' in chapter,ref
    assert covered=={f'T{i}' for i in range(1,15)},covered
    return sorted(covered,key=lambda x:int(x[1:]))


def gallery():
    tree_choices=''.join(f'<button data-tree="{i}" aria-pressed="{str(i==0).lower()}">{html.escape(t["label_de"])}</button>' for i,t in enumerate(TREES))
    style_choices=''.join(f'<button data-style="{slug}" aria-pressed="{str(slug=="a").lower()}">{html.escape(label)}</button>' for slug,label,_ in STYLES)
    meta=[{k:t[k] for k in ('slug','label_de','goal')} for t in TREES]
    document='''<!doctype html><html lang="de"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>VITA-FL · Attack Trees</title><style>body{margin:0;background:#edf1f4;color:#263440;font:16px/1.5 system-ui,sans-serif}main{max-width:1440px;margin:auto;padding:28px}h1{margin:0}p{max-width:1100px}nav,.choices{display:flex;gap:12px;flex-wrap:wrap;margin:18px 0}button{padding:10px 16px;border:1px solid #cad4dc;border-radius:8px;background:white;color:#263440;font:inherit;cursor:pointer}button[aria-pressed=true]{background:#1764a1;color:white;border-color:#1764a1}a{color:#1764a1}nav{gap:24px}figure{margin:24px 0;background:white;padding:14px;border-radius:12px}img{display:block;width:100%;border:1px solid #dce3e8;box-sizing:border-box}figcaption{padding:12px 4px}small{color:#65737d}</style><main><p><a href="revision-b-light/index.html"><strong>Neue Fassung: B auf hellem Grund mit sechs vertieften Bäumen</strong></a></p><h1>Vier Attack Trees · drei Looks</h1><p>Aus den Bedrohungen T1–T14 in Kapitel 4 abgeleitete Zielzerlegungen. OR bedeutet alternative Wege, AND gemeinsam erforderliche Bedingungen. Keine Darstellung nachgewiesener Schwachstellen oder erfolgreicher Angriffe.</p><nav><a href="VITA-FL_Attack_Tree_Alternatives.pptx">Alle 12 Folien als PowerPoint</a><a href="VITA-FL_Attack_Tree_Alternatives.pdf">PDF-Vorschau</a><a href="looks-overview.png">Looks vergleichen</a><a href="trees-overview.png">Vier Themen vergleichen</a></nav><strong>Thema</strong><div class="choices" id="trees">TREE_CHOICES</div><strong>Look</strong><div class="choices" id="styles">STYLE_CHOICES</div><figure><a id="full" href="a-training.png"><img id="preview" src="a-training.png" alt="Attack tree: training"></a><figcaption id="caption"></figcaption></figure><p><a id="deck" href="VITA-FL_Attack_Trees_A_classic.pptx">Diesen Look als PowerPoint öffnen (4 Bäume)</a></p><small>Hauptpräsentation und Kapitel 4 bleiben unverändert. Alle Diagramme sind native, editierbare PowerPoint-Objekte. Exakte Quellen und logische Abgrenzungen stehen in den Sprechernotizen.</small></main><script>const trees=META;const files={a:'A_classic',b:'B_horizontal',c:'C_annotated'};let state={tree:0,style:'a'};function update(){const t=trees[state.tree],src=state.style+'-'+t.slug+'.png';document.querySelector('#preview').src=src;document.querySelector('#preview').alt=t.goal;document.querySelector('#full').href=src;document.querySelector('#caption').textContent=t.label_de+' · '+t.goal;document.querySelector('#deck').href='VITA-FL_Attack_Trees_'+files[state.style]+'.pptx';document.querySelectorAll('[data-tree]').forEach(b=>b.setAttribute('aria-pressed',Number(b.dataset.tree)===state.tree));document.querySelectorAll('[data-style]').forEach(b=>b.setAttribute('aria-pressed',b.dataset.style===state.style));}document.querySelectorAll('[data-tree]').forEach(b=>b.addEventListener('click',()=>{state.tree=Number(b.dataset.tree);update()}));document.querySelectorAll('[data-style]').forEach(b=>b.addEventListener('click',()=>{state.style=b.dataset.style;update()}));update();</script></html>'''
    document=document.replace('TREE_CHOICES',tree_choices).replace('STYLE_CHOICES',style_choices).replace('META',json.dumps(meta,ensure_ascii=False))
    (HERE/'index.html').write_text(document,encoding='utf-8')


def main():
    protected={str(p):digest(p) for p in (MAIN,CHAPTER)}
    coverage=validate_data()
    all_deck=b.prepare_template()
    all_deck.core_properties.title='VITA-FL — Chapter 4 attack trees: three looks'
    images={}
    for slug,label,file_slug in STYLES:
        single=b.prepare_template()
        single.core_properties.title='VITA-FL — Chapter 4 attack trees: '+label
        for tree in TREES:
            BUILDERS[slug](all_deck,tree)
            BUILDERS[slug](single,tree)
        check_layout(single)
        dest=HERE/f'VITA-FL_Attack_Trees_{file_slug}.pptx'
        single.save(dest)
        reopened=Presentation(dest)
        check_layout(reopened)
        assert len(reopened.slides)==4
        for slide,tree in zip(reopened.slides,TREES):
            assert 'TREE-SPECIFIC MODEL' in slide.notes_slide.notes_text_frame.text
            im=renderer.render_slide(reopened,slide)
            im.save(HERE/f'{slug}-{tree["slug"]}.png')
            images[(slug,tree['slug'])]=im
    check_layout(all_deck)
    output=HERE/'VITA-FL_Attack_Tree_Alternatives.pptx'
    all_deck.save(output)
    assert len(Presentation(output).slides)==12
    all_images=[images[(style,tree['slug'])] for style,_,_ in STYLES for tree in TREES]
    all_images[0].save(HERE/'VITA-FL_Attack_Tree_Alternatives.pdf',save_all=True,append_images=all_images[1:],resolution=120)
    font=ImageFont.truetype(renderer.FONT_BOLD,25)
    body=ImageFont.truetype(renderer.FONT_REGULAR,23)
    looks=Image.new('RGB',(1660,1540),'#E8ECEF')
    draw=ImageDraw.Draw(looks)
    texts=[('Klassische Hierarchie','Ziel oben; alternative Wege und gemeinsame','Bedingungen explizit mit OR / AND verbunden.'),
           ('Horizontaler Baum','Leserichtung links nach rechts; dunkle Fläche','und helle Knoten mit deutlicher Zielhierarchie.'),
           ('Angriff plus Einordnung','Gleicher Baum mit getrennten Hinweisen auf','Anforderungen, Restrisiken und Annahmen.')]
    # Same tree across looks, making the visual comparison independent of content.
    comparison=TREES[2]['slug']
    for i,(slug,label,_) in enumerate(STYLES):
        y=14+i*510
        draw.text((30,y),label,font=font,fill='#263440')
        looks.paste(images[(slug,comparison)].resize((800,450),Image.Resampling.LANCZOS),(30,y+43))
        for j,line in enumerate(texts[i]):
            draw.text((875,y+162+j*48),line,font=font if j==0 else body,fill='#263440' if j==0 else '#65737D')
    looks.save(HERE/'looks-overview.png')
    topics=Image.new('RGB',(1660,1040),'#E8ECEF')
    draw=ImageDraw.Draw(topics)
    for i,tree in enumerate(TREES):
        x,y=20+(i%2)*820,15+(i//2)*515
        draw.text((x,y),tree['label_de'],font=font,fill='#263440')
        topics.paste(images[('a',tree['slug'])].resize((800,450),Image.Resampling.LANCZOS),(x,y+43))
    topics.save(HERE/'trees-overview.png')
    gallery()
    assert protected=={str(p):digest(p) for p in (MAIN,CHAPTER)}
    (HERE/'validation.json').write_text(json.dumps({
        'tree_count':4,'look_count':3,'slides':12,'covered_threat_ids':coverage,
        'logic_structure':'OR root; three branches, two leaves each; explicit local OR/AND',
        'layout':'passed','pptx_round_trip':'passed','speaker_notes':'present',
        'native_editable_shapes':True,'source_and_main_preserved':protected,
        'new_experiments_or_cloud_calls':'none','visual_review':'pending',
        'preview_renderer':'Local Pillow renderer; final Arial rendering depends on PowerPoint',
    },indent=2)+'\n')
    print('Built four attack trees in three looks: 12 native slides, three four-slide decks, previews, PDF and gallery.')
    print('Chapter 4 and the main presentation are unchanged.')


if __name__=='__main__': main()
