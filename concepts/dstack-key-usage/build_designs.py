#!/usr/bin/env python3
"""Render four editable alternatives without modifying the main presentation."""

import hashlib
from PIL import Image, ImageDraw, ImageFont
import common as c
import design_a, design_b, design_c, design_d


DESIGNS = [
    ('a-key-use-lanes', 'A · Schlüssel → konkrete Verwendung', design_a),
    ('b-lifecycle-uses', 'B · Schlüssel im Ablauf', design_b),
    ('c-model-key-custody', 'C · RSA-Schutz und Modellzugriff', design_c),
    ('d-actor-map', 'D · Schlüssel und Kommunikationspartner', design_d),
]


def main():
    main_deck=c.ROOT/'VITA-FL_Thesis_Presentation_TU_Berlin.pptx'
    before=hashlib.sha256(main_deck.read_bytes()).digest()
    prs=c.b.prepare_template()
    prs.core_properties.title='VITA-FL — dstack key-use slide alternatives'
    for _,_,design in DESIGNS:
        design.build(prs)
    c.check_layout(prs)
    prs.save(c.HERE/'VITA-FL_Dstack_Key_Usage_Alternatives.pptx')
    images=[]
    for slide,(slug,_,_) in zip(prs.slides,DESIGNS):
        preview=c.renderer.render_slide(prs,slide)
        preview.save(c.HERE/(slug+'.png'))
        images.append(preview)
    images[0].save(c.HERE/'VITA-FL_Dstack_Key_Usage_Alternatives.pdf',
                   save_all=True,append_images=images[1:],resolution=120)
    overview=Image.new('RGB',(1660,1050),'#E8ECEF')
    draw=ImageDraw.Draw(overview)
    font=ImageFont.truetype(c.renderer.FONT_BOLD,22)
    for index,(preview,(_,label,_)) in enumerate(zip(images,DESIGNS)):
        x=20+(index%2)*820
        y=20+(index//2)*515
        overview.paste(preview.resize((800,450),Image.Resampling.LANCZOS),(x,y))
        draw.text((x+5,y+465),label,font=font,fill='#263440')
    overview.save(c.HERE/'overview.png')
    assert before==hashlib.sha256(main_deck.read_bytes()).digest()
    print('Created four checked editable alternatives, PNGs, overview and PDF. Main presentation unchanged.')


if __name__=='__main__':
    main()
