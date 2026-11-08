import pdfplumber, json, math, sys
SRC, OUT = sys.argv[1], sys.argv[2]
K = 150/72
OFF = {'Z','H','Q','Y','RT','RG','C','LG','LT','X','F','U'}
def col(x):
    if not isinstance(x,(tuple,list)): return None
    x=tuple(round(v,2) for v in x)
    if len(x)==1: x=(x[0],)*3
    if x[0]>0.8 and x[1]<0.1: return 'red'
    if x[0]<0.1 and 0.4<x[1]<0.5: return 'teal'
    if 0.28<=x[0]<=0.32 and abs(x[0]-x[1])<0.01: return 'gray'
    if 0.2<x[0]<0.25: return 'slate'
    return None
def rdp(pts, eps):
    if len(pts)<3: return pts
    a,b=pts[0],pts[-1]; dx,dy=b[0]-a[0],b[1]-a[1]; L=math.hypot(dx,dy) or 1e-9
    dmax,idx=0,0
    for i in range(1,len(pts)-1):
        d=abs(dy*pts[i][0]-dx*pts[i][1]+b[0]*a[1]-b[1]*a[0])/L
        if d>dmax: dmax,idx=d,i
    if dmax>eps: return rdp(pts[:idx+1],eps)[:-1]+rdp(pts[idx:],eps)
    return [a,b]
def smooth(pts, w=4):
    # moving average to kill zig-zag teeth, keep endpoints
    out=[pts[0]]
    for i in range(1,len(pts)-1):
        seg=pts[max(0,i-w):i+w+1]
        out.append((sum(p[0] for p in seg)/len(seg), sum(p[1] for p in seg)/len(seg)))
    out.append(pts[-1]); return out
def wavy(pts):
    if len(pts)<6: return False
    L=sum(math.dist(pts[i],pts[i+1]) for i in range(len(pts)-1)); D=math.dist(pts[0],pts[-1])
    return L > D*1.25
pdf=pdfplumber.open(SRC)
plays=[]
for pi,pg in enumerate(pdf.pages):
    if pi<2: continue
    words=pg.extract_words()
    for half,(ya,yb) in enumerate([(40,396),(396,752)]):
        title=[w for w in words if ya<w['top']<ya+35 and 25<w['x0']<300 and not (88<w['x0']<95 and len(w['text'])==1)]
        if not title or not title[0]['text'].isdigit(): continue
        title=[w for w in title if abs(w['top']-title[0]['top'])<4]
        num=int(title[0]['text']); name=' '.join(w['text'] for w in title[1:])
        inside=lambda o: ya+33<o['top'] and o['bottom']<yb+30
        # triangles (defenders): 12-pt white-filled curve, stroke on the non-fill twin
        tris=[]; circles=[]; paths=[]; heads=[]; zones=[]; bars=[]
        for o in pg.curves:
            if not (ya+33<o['top']<yb): continue
            pts=o.get('pts') or []; c=col(o.get('stroking_color')); fc=o.get('non_stroking_color')
            if o.get('fill'):
                fcc=col(fc)
                if len(pts)==6 and fcc in ('red','teal') and (o['x1']-o['x0'])>40:
                    zones.append({'x':(o['x0']+o['x1'])/2,'y':(o['top']+o['bottom'])/2,'r':(o['x1']-o['x0'])/2,'color':fcc})
                continue
            w=o['x1']-o['x0']; h=o['bottom']-o['top']
            if len(pts)==12 and w<26 and h<22: tris.append({'cx':(o['x0']+o['x1'])/2,'cy':o['top']+h*0.6,'c':c,'box':(o['x0'],o['top'],o['x1'],o['bottom'])}); continue
            if len(pts)==6 and w<24 and h<24: circles.append(o); continue
            if len(pts)==3 and w<14 and h<14: heads.append({'x':sum(p[0] for p in pts)/3,'y':sum(p[1] for p in pts)/3,'c':c}); continue
            if c in ('red','teal','gray'): paths.append({'pts':[tuple(p) for p in pts],'c':c,'dash':bool(o.get('dash'))})
        for o in pg.lines:
            if not (ya+33<o['top']<yb) or o.get('fill'): continue
            c=col(o.get('stroking_color'))
            if c in ('red','teal','gray') and 3<math.dist(o['pts'][0],o['pts'][-1])<14:
                bars.append(((o['pts'][0][0]+o['pts'][-1][0])/2,(o['pts'][0][1]+o['pts'][-1][1])/2)); continue
            if c in ('red','teal','gray') and math.dist(o['pts'][0],o['pts'][-1])>3:
                paths.append({'pts':[tuple(p) for p in o['pts']],'c':c,'dash':bool(o.get('dash'))})
        lab=[w for w in words if ya+33<w['top']<yb-20 and w['text'] not in ('GE6','OPPONENT','G') and not (w['x0']<100 and w['text'].isdigit()) and not w['text'].isdigit() and not (w['x0']>480 and len(w['text'])==1 and w['text'] in 'G')]
        players=[]
        # merge consecutive path pieces that touch end-to-start with same color (polyline split)
        merged=True
        while merged:
            merged=False
            for i in range(len(paths)):
                for j in range(len(paths)):
                    if i!=j and paths[i]['c']==paths[j]['c'] and math.dist(paths[i]['pts'][-1],paths[j]['pts'][0])<1.0:
                        paths[i]['pts']+=paths[j]['pts'][1:]; paths.pop(j); merged=True; break
                if merged: break
        for w in lab:
            x=(w['x0']+w['x1'])/2; y=(w['top']+w['bottom'])/2; t=w['text']
            tri=min(tris,key=lambda T: math.dist((T['cx'],T['cy']),(x,y)),default=None)
            if tri and math.dist((tri['cx'],tri['cy']),(x,y))<9 and t not in ('Z','H','Q','Y','RT','RG','LG','LT','X','F'):
                bx=tri['box']; players.append({'label':t,'team':'def','x':(bx[0]+bx[2])/2,'y':(bx[1]+bx[3])/2+1.5,'c':tri['c']})
            else:
                players.append({'label':t,'team':'opp','x':x,'y':y+0.5})
        # attach paths to defenders
        defs=[p for p in players if p['team']=='def']
        for pa in paths:
            pts=pa['pts']
            best=None
            for d in defs:
                for end in (0,-1):
                    dd=math.dist((d['x'],d['y']),pts[end])
                    if best is None or dd<best[0]: best=(dd,d,end)
            if best is None or best[0]>16: print('unattached',num,pa['c'],[tuple(map(round,p)) for p in pts[:3]],round(best[0]) if best else None); continue
            dd,d,end=best
            if end==-1: pts=pts[::-1]
            wv=wavy(pts)
            pp=smooth(pts,3) if wv else pts
            pp=rdp(pp, 2.5 if wv else 0.8)
            if 'path' in d: print('second path',num,d['label']); d['path2']=pp; continue
            d['path']=pp[1:] if math.dist(pp[0],(d['x'],d['y']))<12 else pp
            d['dashed']=pa['dash']; d['wavy']=wv
            # arrowhead near the end?
            e=pts[-1]; d['end']='arrow' if any(math.dist((h['x'],h['y']),e)<9 for h in heads) else ('block' if any(math.dist(b,e)<6 for b in bars) else 'none')
        # unique ids
        cnt={}
        for p in players: cnt[(p['team'],p['label'])]=cnt.get((p['team'],p['label']),0)+1
        for p in players:
            if cnt[(p['team'],p['label'])]>1:
                same=sorted([q for q in players if q['team']==p['team'] and q['label']==p['label']],key=lambda q:q['x'])
                p['id']=p['label']+'-'+('L' if same.index(p)==0 else 'R')
            else: p['id']=p['label']
        # anchor
        cen=[p for p in players if p['team']=='opp' and p['label']=='C']
        ol=sorted([p for p in players if p['team']=='opp' and p['label'] in ('LT','LG','C','RG','RT')],key=lambda q:q['x'])
        unit=(ol[-1]['x']-ol[0]['x'])/(len(ol)-1)
        hl=sorted(set(round(l['top']) for l in pg.lines if col(l.get('stroking_color')) is None and abs(l['top']-l['bottom'])<0.5 and (l['x1']-l['x0'])>300 and ya+33<l['top']<yb))
        los=[l for l in pg.lines if abs(l['top']-l['bottom'])<0.5 and (l['x1']-l['x0'])>400 and ya+33<l['top']<yb]
        losY=cen[0]['y']
        for p in players:
            if p['team']=='opp' and p['label'] in ('LT','LG','C','RG','RT','Y','X','U'): pass
        # zone owners
        for z in zones:
            cand=[]
            for d in defs:
                end=d['path'][-1] if d.get('path') else (d['x'],d['y'])
                if math.dist(end,(z['x'],z['y']))<=z['r']: cand.append((math.dist(end,(z['x'],z['y'])),d))
            z['owner']=min(cand,key=lambda t:t[0])[1]['id'] if cand else None
        S=lambda v: round(v*K,1)
        out={'id':'d%02d-'%num+name.lower().replace(' ','-').replace('/','-'),'num':num,'page':pi+1,'file':'d-%02d.png'%(pi+1),'name':name,'category':'Defense','note':'',
             'crop':[S(22),S(ya),S(590),S(yb)],
             'anchor':{'cx':S(cen[0]['x']),'losY':S(losY),'unit':S(unit),'yard5':S(52.5*unit/28.0)},
             'players':[],'zones':[{'x':S(z['x']),'y':S(z['y']),'r':S(z['r']),'color':z['color'],'owner':z['owner']} for z in zones]}
        for p in players:
            q={'id':p['id'],'label':p['label'],'team':p['team'],'x':S(p['x']),'y':S(p['y'])}
            if p.get('path'): q['path']=[[S(a),S(b)] for a,b in p['path']]; q['end']=p['end']; q['dashed']=p['dashed']
            if p.get('path2'): q['alt']='second line present'
            out['players'].append(q)
        out['_hlines']=hl
        plays.append(out)
plays.sort(key=lambda p:p['num'])
json.dump(plays,open(OUT,'w'),indent=1)
for p in plays:
    print(p['num'],p['name'],p['anchor']['unit'],'| def:',' '.join(q['id']+('*' if q.get('path') else '') for q in p['players'] if q['team']=='def'),'| zones',len(p['zones']),'| hl',p['_hlines'][:8])
