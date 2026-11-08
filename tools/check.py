# usage: check.py data.json imgdir outdir  -> draws transcription over source image
import sys,json,os
from PIL import Image, ImageDraw
data=json.load(open(sys.argv[1])); imgdir=sys.argv[2]; out=sys.argv[3]
plays=data if isinstance(data,list) else [data]
for p in plays:
    im=Image.open(os.path.join(imgdir,p['file'])).convert('RGB')
    if 'crop' in p: im=im.crop(tuple(p['crop']))
    ox,oy=(p['crop'][0],p['crop'][1]) if 'crop' in p else (0,0)
    im=im.convert('RGBA'); ov=Image.new('RGBA',im.size,(0,0,0,0)); d=ImageDraw.Draw(ov)
    T=lambda pt:(pt[0]-ox,pt[1]-oy)
    a=p.get('anchor')
    if a:
        d.line([(0,a['losY']-oy),(im.width,a['losY']-oy)],fill=(0,200,0,160),width=1)
        cx=a['cx']-ox; d.line([(cx,0),(cx,im.height)],fill=(0,200,0,160),width=1)
        for k in range(-3,4): d.ellipse([cx+k*a['unit']-3,a['losY']-oy-3,cx+k*a['unit']+3,a['losY']-oy+3],outline=(0,200,0,255))
    for z in p.get('zones',[]):
        x,y=T((z['x'],z['y'])); r=z['r']; d.ellipse([x-r,y-r,x+r,y+r],outline=(0,0,255,255),width=2)
    for pl in p['players']:
        x,y=T((pl['x'],pl['y']))
        d.ellipse([x-9,y-9,x+9,y+9],outline=(0,0,0,255),width=3)
        d.text((x+10,y-16),pl['id'],fill=(0,0,0,255))
        pts=[(x,y)]+[T(q) for q in pl.get('motion',[])]
        if len(pts)>1: d.line(pts,fill=(0,160,255,230),width=4)
        pts2=[pts[-1]]+[T(q) for q in pl.get('path',[])]
        if len(pts2)>1: d.line(pts2,fill=(0,0,0,200),width=3)
        if len(pts2)>1:
            ex,ey=pts2[-1]; d.ellipse([ex-5,ey-5,ex+5,ey+5],fill=(0,0,0,255))
    im=Image.alpha_composite(im,ov).convert('RGB')
    im.save(os.path.join(out,os.path.splitext(p['file'])[0]+'_'+p.get('id','x')+'.png'))
print('ok',len(plays))
