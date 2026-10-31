import subprocess, numpy as np, wave
from PIL import Image, ImageDraw, ImageFont, ImageFilter
SRC='/root/.claude/uploads/3bdc22a0-44b6-5463-a581-9b7d84b08b80/ed58a5ee-HnVideoEditor_2026_10_31_093356894.mp4'
A='/home/user/saborrural/enlaces-assets/'; W,H=1080,1920; PINK=(245,154,172); DARK=(12,13,15)
F=lambda n,s: ImageFont.truetype(A+n,s)
def lines(d,text,font,maxw):
    out=[];cur=''
    for w in text.split():
        t=(cur+' '+w).strip()
        if d.textlength(t,font=font)<=maxw: cur=t
        else: out.append(cur);cur=w
    out.append(cur);return out
def cap(title,sub,y=210,ts=88,ss=52):
    im=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(im); ft=F('bricolage800.ttf',ts); fs=F('hanken700.ttf',ss)
    tl=lines(d,title,ft,W-170); sl=lines(d,sub,fs,W-210) if sub else []
    lh=int(ts*1.08); sh=int(ss*1.3); bh=len(tl)*lh+len(sl)*sh+66
    d.rounded_rectangle((50,y,W-50,y+bh),radius=38,fill=(12,13,15,205),outline=PINK+(255,),width=4)
    yy=y+26
    for l in tl: d.text((W/2,yy),l,font=ft,fill=(255,255,255),anchor='ma'); yy+=lh
    yy+=4
    for l in sl: d.text((W/2,yy),l,font=fs,fill=PINK,anchor='ma'); yy+=sh
    return im
def cta():
    im=Image.new('RGB',(W,H),DARK); g=Image.new('RGB',(W,H),DARK); ImageDraw.Draw(g).ellipse((-200,-450,W+200,1050),fill=(150,36,60)); g=g.filter(ImageFilter.GaussianBlur(170)); im=Image.blend(im,g,0.9); d=ImageDraw.Draw(im)
    lg=Image.open(A+'logo.png').convert('RGBA'); lw=360; lg=lg.resize((lw,int(lw*lg.height/lg.width))); im.paste(lg,((W-lw)//2,230),lg)
    y=720
    d.text((W/2,y),'Ven a visitarnos',font=F('bricolage800.ttf',120),fill=(255,255,255),anchor='ma'); y+=140
    d.text((W/2,y),'a Licantén',font=F('bricolage800.ttf',120),fill=PINK,anchor='ma'); y+=190
    for t in ['Ruta J-60, km 95, frente a Lora','Lun a vie 9:00–21:00','Sáb y dom 14:00–21:00']:
        d.text((W/2,y),t,font=F('hanken700.ttf',54),fill=(235,231,222),anchor='ma'); y+=82
    y+=40; d.rounded_rectangle((120,y,W-120,y+150),radius=36,fill=PINK)
    d.text((W/2,y+75),'Cómo llegar: link en la bio',font=F('hanken700.ttf',56),fill=(26,10,15),anchor='mm')
    d.text((W/2,H-190),'@sabor_rural',font=F('bricolage800.ttf',64),fill=(255,255,255),anchor='ma')
    return im
caps=[(0.2,2.0,'Bienvenido a Sabor Rural','Café y pastelería en pleno campo'),
      (2.1,4.1,'Ruta J-60, km 95','frente a Lora · Licantén'),
      (4.2,7.0,'Un rincón acogedor','para tu pausa de café'),
      (7.1,9.9,'Café de especialidad','preparado al momento en nuestra barra'),
      (10.1,14.0,'Tartas, kuchen y pasteles','hechos en casa, todos los días'),
      (14.2,17.0,'Hecho a mano, con cariño',None),
      (17.2,20.0,'Cookies estilo Nueva York','gruesas y rellenas'),
      (20.1,21.5,'Ven a vivirlo',None)]
inputs=['-i',SRC]; fc=['[0:v]scale=1080:1920:flags=lanczos,unsharp=5:5:0.8,eq=saturation=1.1:contrast=1.04,tpad=stop_mode=clone:stop_duration=3.4,fps=30[b]']
last='b'; idx=1
for i,(a,b,t,s) in enumerate(caps):
    cap(t,s).save(f'c{i}.png'); inputs+=['-loop','1','-i',f'c{i}.png']
    fc.append(f'[{idx}:v]format=rgba,fade=t=in:st={a}:d=0.3:alpha=1,fade=t=out:st={b-0.3}:d=0.3:alpha=1[o{i}]'); fc.append(f'[{last}][o{i}]overlay=0:0:eof_action=pass[v{i}]'); last=f'v{i}'; idx+=1
cta().save('cta.png'); inputs+=['-loop','1','-i','cta.png']
fc.append(f'[{idx}:v]format=rgba,fade=t=in:st=21.6:d=0.5:alpha=1[oc]'); fc.append(f'[{last}][oc]overlay=0:0:eof_action=pass,format=yuv420p[v]')
total=21.5+3.4
subprocess.run(['ffmpeg','-y','-loglevel','error',*inputs,'-filter_complex',';'.join(fc),'-map','[v]','-t',str(total),'-c:v','libx264','-crf','17','-preset','slow','-r','30','video.mp4'],check=True)
# música cálida original
sr=44100; T=total+0.3; n=int(sr*T); out=np.zeros(n); bpm=92; beat=60/bpm
def add(s,t,g=1.0):
    i=int(t*sr); j=min(n,i+len(s))
    if i<n: out[i:j]+=s[:j-i]*g
def pluck(f,d=1.1):
    x=np.arange(int(sr*d))/sr; w=np.sin(2*np.pi*f*x)+0.4*np.sin(4*np.pi*f*x)*np.exp(-x*6)+0.15*np.sin(6*np.pi*f*x)*np.exp(-x*10); return w*np.exp(-x*4.5)*np.minimum(1,x*500)
def pad(f,d):
    x=np.arange(int(sr*d))/sr; w=np.sin(2*np.pi*f*x)+0.5*np.sin(2*np.pi*f*1.003*x); return w*np.minimum(1,x/0.6)*np.minimum(1,(d-x)/0.8)/2
rng=np.random.default_rng(2)
def shaker():
    x=np.arange(int(sr*0.07))/sr; z=rng.standard_normal(len(x)); b=z-np.convolve(z,np.ones(6)/6,mode='same'); return b*np.exp(-x*45)*0.35
C=lambda m:440*2**((m-69)/12)
prog=[(48,[60,64,67,72]),(45,[57,60,64,69]),(41,[60,65,69,72]),(43,[59,62,67,71])]
for bar in range(int(T/(beat*4))+1):
    root,ch=prog[bar%4]; st=bar*beat*4
    for m in ch[:3]: add(pad(C(m-12),beat*4.2),st,0.07)
    add(pad(C(root),beat*4.2),st,0.14)
    for k in range(8): add(pluck(C(ch[[0,1,2,3,2,1,2,3][k]]+12)),st+k*beat/2,0.17 if k%2==0 else 0.11)
    for k in range(8):
        if k%2==1: add(shaker(),st+k*beat/2,0.6)
out=np.tanh(out*1.1); fi=int(sr*0.6); out[:fi]*=np.linspace(0,1,fi); fo=int(sr*1.6); out[-fo:]*=np.linspace(1,0,fo)
with wave.open('music.wav','wb') as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes((out/np.max(np.abs(out))*0.8*32767).astype('<i2').tobytes())
subprocess.run(['ffmpeg','-y','-loglevel','error','-i','video.mp4','-i','music.wav','-filter_complex','[1:a]aresample=48000,aformat=channel_layouts=stereo,loudnorm=I=-15:TP=-1.5:LRA=7[a]','-map','0:v','-map','[a]','-c:v','libx264','-profile:v','high','-b:v','8M','-maxrate','10M','-bufsize','16M','-pix_fmt','yuv420p','-r','30','-c:a','aac','-ar','48000','-b:a','128k','-t',str(total),'-shortest','-movflags','+faststart','reel-tour.mp4'],check=True)
print('ok',total)
