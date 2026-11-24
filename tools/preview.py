import json,sys,glob
from PIL import Image,ImageDraw
pack=sys.argv[1] if len(sys.argv)>1 else 'asas-de-cera'
adv=json.load(open(glob.glob(f'src/packs/{pack}/*.json')[0]))
for sc in adv['scenes']:
    if not sc['tokenVision']: continue
    im=Image.open(sc['background']['src'].replace('modules/mesa-alta/','')).convert('RGB')
    d=ImageDraw.Draw(im); g=sc['grid']['size']
    for w in sc['walls']:
        col=(255,140,0) if w['door']==1 else (180,0,255) if w['door']==2 else (0,200,255) if w['sight']==0 else (255,255,0)
        d.line(w['c'],fill=col,width=10)
    for l in sc['lights']:
        r=l['config']['dim']*g; d.ellipse((l['x']-r,l['y']-r,l['x']+r,l['y']+r),outline=(255,255,255),width=3)
    for t in sc['tokens']:
        tok=Image.open(t['texture']['src'].replace('modules/mesa-alta/','')).resize((g,g))
        im.paste(tok,(t['x'],t['y']),tok)
        if t['hidden']: d.rectangle((t['x'],t['y'],t['x']+g,t['y']+g),outline=(255,0,0),width=6)
    im.thumbnail((1400,1400)); im.save('/tmp/prev_'+sc['name'].split('— ')[1][:10].replace(' ','_')+'.jpg')
