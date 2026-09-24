#!/usr/bin/env python3
"""Generate alternative aggregation slides while preserving the main deck."""
import hashlib
from PIL import Image, ImageDraw, ImageFont
import common as c
import design_a, design_b, design_c

DESIGNS=[
    ('a-actors-and-messages','A · Zuständigkeiten und Nachrichten',design_a),
    ('b-model-flow','B · Von lokalen Modellen zum globalen Modell',design_b),
    ('c-signed-statement','C · Was die signierte Aussage verknüpft',design_c),
]


def main():
    main_deck=c.ROOT/'VITA-FL_Thesis_Presentation_TU_Berlin.pptx'
    before=hashlib.sha256(main_deck.read_bytes()).digest()
    prs=c.b.prepare_template()
    prs.core_properties.title='VITA-FL — Aggregation round alternatives'
    for _,_,design in DESIGNS:
        design.build(prs)
    c.check_layout(prs)
    prs.save(c.HERE/'VITA-FL_Aggregation_Round_Alternatives.pptx')
    images=[]
    for slide,(slug,_,_) in zip(prs.slides,DESIGNS):
        preview=c.renderer.render_slide(prs,slide)
        preview.save(c.HERE/(slug+'.png'))
        images.append(preview)
    images[0].save(c.HERE/'VITA-FL_Aggregation_Round_Alternatives.pdf',
                   save_all=True,append_images=images[1:],resolution=120)
    overview=Image.new('RGB',(1660,1050),'#E8ECEF')
    draw=ImageDraw.Draw(overview)
    font=ImageFont.truetype(c.renderer.FONT_BOLD,21)
    for index,(preview,(_,label,_)) in enumerate(zip(images,DESIGNS)):
        x=20+index*820 if index<2 else 430
        y=20 if index<2 else 535
        overview.paste(preview.resize((800,450),Image.Resampling.LANCZOS),(x,y))
        draw.text((x+5,y+464),label,font=font,fill='#263440')
    overview.save(c.HERE/'overview.png')
    assert before==hashlib.sha256(main_deck.read_bytes()).digest()
    print('Created three editable alternatives, checked layouts, PNGs, overview and PDF. Main deck unchanged.')


if __name__=='__main__':
    main()
