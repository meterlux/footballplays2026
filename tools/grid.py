# usage: grid.py in.png out.png [step] [x0 y0 x1 y1 crop] [scale]
import sys
from PIL import Image, ImageDraw
a=sys.argv
im=Image.open(a[1]).convert('RGB')
step=int(a[3]) if len(a)>3 else 25
ox,oy=0,0
if len(a)>7:
    x0,y0,x1,y1=map(int,a[4:8]); im=im.crop((x0,y0,x1,y1)); ox,oy=x0,y0
sc=float(a[8]) if len(a)>8 else 1.0
if sc!=1: im=im.resize((int(im.width*sc),int(im.height*sc)),Image.LANCZOS)
d=ImageDraw.Draw(im,'RGBA')
def gx(v): return (v-ox)*sc
def gy(v): return (v-oy)*sc
X0=(ox//step)*step
for x in range(X0, ox+int(im.width/sc)+step, step):
    big = x%(step*4)==0
    d.line([(gx(x),0),(gx(x),im.height)],fill=(0,120,255,110 if big else 45),width=1)
    if big: d.text((gx(x)+2,2),str(x),fill=(0,0,200,255)); d.text((gx(x)+2,im.height-12),str(x),fill=(0,0,200,255))
Y0=(oy//step)*step
for y in range(Y0, oy+int(im.height/sc)+step, step):
    big = y%(step*4)==0
    d.line([(0,gy(y)),(im.width,gy(y))],fill=(255,0,120,110 if big else 45),width=1)
    if big: d.text((2,gy(y)+2),str(y),fill=(200,0,0,255)); d.text((im.width-30,gy(y)+2),str(y),fill=(200,0,0,255))
im.save(a[2])
