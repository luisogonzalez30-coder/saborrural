import subprocess, numpy as np, wave, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
U='/root/.claude/uploads/3bdc22a0-44b6-5463-a581-9b7d84b08b80/'
A='/home/user/saborrural/enlaces-assets/'
P={3:'6701abdd',4:'a4bdd0cb',6:'5cdc37a7',7:'d8066b95',8:'7e620a33',9:'bd5a4917',1:'43e296cc'}
F=lambda n,s: ImageFont.truetype(A+n,s)
PINK=(245,154,172); DARK=(12,13,15)
def photo(n): return Image.open(U+P[n]+'-image.jpg').convert('RGB')
def crop(im,ar,fx=0.5,fy=0.5):
    w,h=im.size
    if w/h>ar: nw=int(h*ar); x=int((w-nw)*fx); return im.crop((x,0,x+nw,h))
    nh=int(w/ar); y=int((h-nh)*fy); return im.crop((0,y,w,y+nh))
def lines(d,text,font,maxw):
    out=[];cur=''
    for w in text.split():
        t=(cur+' '+w).strip()
        if d.textlength(t,font=font)<=maxw: cur=t
        else: out.append(cur);cur=w
    out.append(cur);return out
def overlay(size,title,sub,y,tsize=90,ssize=54):
    W,H=size; im=Image.new('RGBA',size,(0,0,0,0)); d=ImageDraw.Draw(im)
    ft=F('bricolage800.ttf',tsize); fs=F('hanken700.ttf',ssize)
    tl=lines(d,title,ft,W-150); sl=lines(d,sub,fs,W-190)
    lh=int(tsize*1.08); sh=int(ssize*1.3)
    bh=len(tl)*lh+len(sl)*sh+70
    box=Image.new('RGBA',size,(0,0,0,0)); bd=ImageDraw.Draw(box)
    bd.rounded_rectangle((50,y,W-50,y+bh),radius=38,fill=(12,13,15,205),outline=PINK+(255,),width=4)
    im=Image.alpha_composite(im,box); d=ImageDraw.Draw(im); yy=y+28
    for l in tl: d.text((W/2,yy),l,font=ft,fill=(255,255,255),anchor='ma'); yy+=lh
    yy+=6
    for l in sl: d.text((W/2,yy),l,font=fs,fill=PINK,anchor='ma'); yy+=sh
    return im
def cta(size,ig=False):
    W,H=size; im=Image.new('RGB',size,DARK); d=ImageDraw.Draw(im)
    g=Image.new('RGB',size,DARK); gd=ImageDraw.Draw(g)
    gd.ellipse((-W*0.2,-H*0.25,W*1.2,H*0.55),fill=(150,36,60)); g=g.filter(ImageFilter.GaussianBlur(160)); im=Image.blend(im,g,0.9); d=ImageDraw.Draw(im)
    logo=Image.open(A+'logo.png').convert('RGBA'); lw=int(W*0.30); logo=logo.resize((lw,int(lw*logo.height/logo.width)))
    im.paste(logo,((W-lw)//2,int(H*0.09)),logo)
    y=int(H*0.31)
    for t,f,c in [('Tu torta',F('bricolage800.ttf',int(W*0.12)),(255,255,255)),('personalizada',F('bricolage800.ttf',int(W*0.12)),PINK)]:
        d.text((W/2,y),t,font=f,fill=c,anchor='ma'); y+=int(W*0.13)
    y+=int(H*0.012)
    d.text((W/2,y),'Fondant, diseños y figuras a tu medida',font=F('hanken700.ttf',int(W*0.04)),fill=(230,226,218),anchor='ma'); y+=int(H*0.06)
    bw,bh=int(W*0.82),int(W*0.17)
    d.rounded_rectangle(((W-bw)//2,y,(W+bw)//2,y+bh),radius=30,fill=(52,199,89))
    d.text((W/2,y+bh/2),'Cotiza por WhatsApp',font=F('hanken700.ttf',int(W*0.062)),fill=(8,40,18),anchor='mm'); y+=bh+int(H*0.025)
    d.text((W/2,y),'+56 9 9210 1764',font=F('bricolage800.ttf',int(W*0.085)),fill=(255,255,255),anchor='ma'); y+=int(W*0.11)
    d.text((W/2,y),'Cuéntanos tema, personas y fecha',font=F('hanken700.ttf',int(W*0.038)),fill=PINK,anchor='ma')
    d.text((W/2,H-int(H*0.07)),'Ruta J-60, km 95 · Licantén · @sabor_rural',font=F('hanken700.ttf',int(W*0.036)),fill=(200,196,188),anchor='ma')
    return im
# ---------- REEL ----------
W,H=1080,1920
shots=[(3,0.5,'¿Tu peque ama a Mario?','Su torta soñada existe'),
       (7,0.5,'Hecha a mano en Licantén','cada detalle, uno por uno'),
       (9,0.0,'Monedas, bloques y bombas','como en el videojuego'),
       (4,0.5,'Tu idea, hecha torta','materiales de la más alta calidad'),
       (8,0.0,'Con cariño y profesionalismo','para el cumpleaños de tu peque')]
D=2.3; X=0.25; os.makedirs('out',exist_ok=True)
clips=[]
for i,(n,fx,t,s) in enumerate(shots):
    c=crop(photo(n),9/16,fx).resize((2160,3840),Image.LANCZOS); c.save(f'out/s{i}.jpg',quality=93)
    ov=overlay((W,H),t,s,y=190 if i%2==0 else 1250); ov.save(f'out/o{i}.png')
    frames=int((D+X)*30)
    zoom="min(1.0+0.0009*on,1.14)" if i%2==0 else "max(1.14-0.0009*on,1.0)"
    subprocess.run(['ffmpeg','-y','-loglevel','error','-loop','1','-i',f'out/s{i}.jpg','-loop','1','-i',f'out/o{i}.png','-filter_complex',
      f"[0:v]zoompan=z='{zoom}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s={W}x{H}:fps=30,format=yuva420p[a];[1:v]format=rgba,fade=t=in:st=0.25:d=0.3:alpha=1[b];[a][b]overlay=0:0:shortest=1,format=yuv420p",
      '-t',str(D+X),'-r','30','-c:v','libx264','-crf','17','-preset','slow',f'out/c{i}.mp4'],check=True)
    clips.append(f'out/c{i}.mp4')
cta(( W,H)).save('out/cta.png')
subprocess.run(['ffmpeg','-y','-loglevel','error','-loop','1','-i','out/cta.png','-t','3.2','-r','30','-vf','format=yuv420p','-c:v','libx264','-crf','17',f'out/c{len(shots)}.mp4'],check=True)
clips.append(f'out/c{len(shots)}.mp4')
parts=[];chain='[0:v]';off=0
for i in range(1,len(clips)):
    off+=D if i<len(clips) else 0
    out='[v]' if i==len(clips)-1 else f'[x{i}]'
    tr='slideleft' if i%2 else 'fade'
    parts.append(f"{chain}[{i}:v]xfade=transition={tr}:duration={X}:offset={round(off,3)}{out}"); chain=f'[x{i}]'
total=D*len(shots)+3.2
subprocess.run(['ffmpeg','-y','-loglevel','error',*sum([['-i',c] for c in clips],[]),'-filter_complex',';'.join(parts),'-map','[v]','-c:v','libx264','-crf','17','-preset','slow','-pix_fmt','yuv420p','-r','30','out/video.mp4'],check=True)
print('dur',total)
# ---------- música 8-bit original ----------
sr=44100; T=total+0.3; n=int(sr*T); out=np.zeros(n); bpm=148; beat=60/bpm
def add(sig,t,g=1.0):
    i=int(t*sr); j=min(n,i+len(sig))
    if i<n: out[i:j]+=sig[:j-i]*g
def sq(f,d,duty=.5,dec=4):
    x=np.arange(int(sr*d))/sr; w=np.where((f*x)%1<duty,1.0,-1.0); return w*np.exp(-dec*x/d)*np.minimum(1,x*300)
def tri(f,d):
    x=np.arange(int(sr*d))/sr; return 2/np.pi*np.arcsin(np.sin(2*np.pi*f*x))*np.exp(-2*x/d)*np.minimum(1,x*300)
rng=np.random.default_rng(5)
def hat():
    x=np.arange(int(sr*0.04))/sr; return rng.standard_normal(len(x))*np.exp(-x*90)*0.4
def kick():
    x=np.arange(int(sr*0.2))/sr; return np.sin(2*np.pi*np.cumsum(60+120*np.exp(-x*35))/sr)*np.exp(-x*12)
C=lambda m:440*2**((m-69)/12)
mel=[72,76,79,76,72,76,79,84, 77,81,84,81,77,81,84,89, 74,77,81,77,74,77,81,86, 79,83,86,83,79,83,86,91]
bass=[48,48,53,53,50,50,55,55]
steps=int(T/(beat/2))+1
for k in range(steps):
    t=k*beat/2; m=mel[k%len(mel)]
    add(sq(C(m),beat/2*0.9,0.25,3),t,0.16)
    if k%2==0: add(tri(C(bass[(k//2)%len(bass)]-12),beat*0.9),t,0.5)
    if k%2==1: add(hat(),t,0.5)
    if k%4==0: add(kick(),t,0.8)
    if k%4==2: add(hat()*2,t,0.7)
# moneda en cada corte
for i in range(1,len(clips)):
    t=i*D-X*0.5+ (0 if i<len(clips) else 0)
    add(np.concatenate([sq(C(83),0.07,.5,2),sq(C(88),0.35,.5,5)]),t,0.28)
fi=int(sr*0.2); out[:fi]*=np.linspace(0,1,fi); fo=int(sr*1.0); out[-fo:]*=np.linspace(1,0,fo)
pcm=(out/np.max(np.abs(out))*0.85*32767).astype('<i2')
with wave.open('out/music.wav','wb') as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes(pcm.tobytes())
subprocess.run(['ffmpeg','-y','-loglevel','error','-i','out/video.mp4','-i','out/music.wav','-filter_complex','[1:a]aresample=48000,aformat=channel_layouts=stereo,loudnorm=I=-14:TP=-1.5:LRA=7[a]','-map','0:v','-map','[a]','-c:v','libx264','-profile:v','high','-b:v','8M','-maxrate','10M','-bufsize','16M','-pix_fmt','yuv420p','-r','30','-c:a','aac','-ar','48000','-b:a','128k','-t',str(total),'-shortest','-movflags','+faststart','out/reel-mario.mp4'],check=True)
# ---------- POST (carrusel 4:5) ----------
PW,PH=1080,1350
slides=[(3,0.5,'Torta de Mario Bros','Hecha a mano en Licantén'),(7,0.5,None,None),(9,0.0,None,None),(4,0.5,None,None),(8,0.0,None,None)]
for i,(n,fx,t,s) in enumerate(slides):
    im=crop(photo(n),PW/PH,fx).resize((PW,PH),Image.LANCZOS).convert('RGBA')
    if t: im=Image.alpha_composite(im,overlay((PW,PH),t,s,y=70,tsize=84,ssize=50))
    im.convert('RGB').save(f'out/post{i+1}.jpg',quality=92)
cta((PW,PH)).save('out/post6.jpg',quality=92)
