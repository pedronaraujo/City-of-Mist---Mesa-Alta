import json,sys
from PIL import Image,ImageDraw
adv=json.load(open('src/packs/asas-de-cera/Asas_de_Cera.json'))
for sc in adv['scenes']:
    if not sc['tokenVision']: continue
    im=Image.open(sc['background']['src'].replace('modules/asas-de-cera/','')).convert('RGB')
    d=ImageDraw.Draw(im); g=sc['grid']['size']
    for w in sc['walls']:
        col=(255,140,0) if w['door']==1 else (180,0,255) if w['door']==2 else (0,200,255) if w['sight']==0 else (255,255,0)
        d.line(w['c'],fill=col,width=10)
    for l in sc['lights']:
        r=l['config']['dim']*g; d.ellipse((l['x']-r,l['y']-r,l['x']+r,l['y']+r),outline=(255,255,255),width=3)
    for t in sc['tokens']:
        tok=Image.open(t['texture']['src'].replace('modules/asas-de-cera/','')).resize((g,g))
        im.paste(tok,(t['x'],t['y']),tok)
        if t['hidden']: d.rectangle((t['x'],t['y'],t['x']+g,t['y']+g),outline=(255,0,0),width=6)
    im.thumbnail((1400,1400)); im.save('/tmp/prev_'+sc['name'].split('— ')[1][:10].replace(' ','_')+'.jpg')
