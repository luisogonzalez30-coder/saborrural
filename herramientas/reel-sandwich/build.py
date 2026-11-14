# Reel 9:16 de sándwiches (Barros Luco y Lorino) · marca: fondo #0C0D0F, crema, rosa; sin marco; logo blanco en zona segura
import subprocess, os
from PIL import Image, ImageDraw, ImageFont
from _music import music
A="/home/user/saborrural/enlaces-assets/"; T="/tmp/claude-0/-home-user/3bdc22a0-44b6-5463-a581-9b7d84b08b80/scratchpad/rs/"; OUT="/home/user/saborrural/media/sandwich/"
U="/root/.claude/uploads/3bdc22a0-44b6-5463-a581-9b7d84b08b80/"
os.makedirs(T,exist_ok=True)
F=lambda n,s: ImageFont.truetype(A+n,s)
BG=(12,13,15); CREAM=(243,241,234); PINK=(245,154,172); MUTE=(169,171,163)
W,H=1080,1920
def rounded(im,r):
    m=Image.new("L",im.size,0); ImageDraw.Draw(m).rounded_rectangle([0,0,im.width-1,im.height-1],radius=r,fill=255); im=im.convert("RGBA"); im.putalpha(m); return im
def trim_black(im,th=14):
    g=im.convert("L").point(lambda v:255 if v>th else 0); return im.crop(g.getbbox())
BL=trim_black(Image.open(U+"e6385504-image.jpg").convert("RGB"))
LO=Image.open("/home/user/saborrural/media/sandwich/originales/lorino-sin-tabla.jpg").convert("RGB").crop((0,110,1290,985))
logo=Image.open(A+"logo.png").convert("RGBA")
def canvas():
    c=Image.new("RGBA",(W,H),BG+(255,)); L=190; lg=logo.resize((L,int(L*logo.height/logo.width)),Image.LANCZOS); c.alpha_composite(lg,(70,190)); return c
def ctr(d,t,f,y,col): d.text((W/2,y),t,font=f,fill=col,anchor="ma")
def put(c,im,y,w=960,box=None):
    if box: im=im.crop(box)
    h=int(im.height*w/im.width); c.alpha_composite(rounded(im.resize((w,h),Image.LANCZOS),34),((W-w)//2,y)); return h
def pill(d,t,y,f=58):
    fo=F("bricolage800.ttf",f); w=int(d.textlength(t,font=fo))+70; d.rounded_rectangle([(W-w)//2,y,(W+w)//2,y+96],radius=48,fill=PINK); d.text((W/2,y+48),t,font=fo,fill=BG,anchor="mm")
sc=[]
# 1 gancho
c=canvas(); d=ImageDraw.Draw(c); ctr(d,"¿Barros Luco",F("bricolage800.ttf",118),430,CREAM); ctr(d,"o Lorino?",F("bricolage800.ttf",118),560,PINK)
h=put(c,BL,760,700); put(c,LO,760+h+30,700); sc.append(("s1",c,2.4))
# 2 Barros Luco
c=canvas(); d=ImageDraw.Draw(c); ctr(d,"Barros Luco",F("bricolage800.ttf",120),430,CREAM)
h=put(c,BL,620,980); pill(d,"$7.000",620+h+50); ctr(d,"Carne de vacuno y queso fundido",F("hanken700.ttf",42),620+h+190,MUTE); sc.append(("s2",c,2.4))
# 3 detalle BL
c=canvas(); d=ImageDraw.Draw(c); ctr(d,"Queso fundido",F("bricolage800.ttf",110),430,PINK)
bw,bh=BL.size; h=put(c,BL,640,980,box=(int(bw*0.10),int(bh*0.22),int(bw*0.62),int(bh*0.96))); ctr(d,"En pan ciabatta horneado",F("hanken700.ttf",44),640+h+40,MUTE); sc.append(("s3",c,2.2))
# 4 Lorino
c=canvas(); d=ImageDraw.Draw(c); ctr(d,"Lorino",F("bricolage800.ttf",130),430,CREAM)
h=put(c,LO,640,980); pill(d,"$8.000",640+h+50); ctr(d,"Palta, tomate y champiñones",F("hanken700.ttf",42),640+h+190,MUTE); sc.append(("s4",c,2.4))
# 5 detalle LO
c=canvas(); d=ImageDraw.Draw(c); ctr(d,"Gratinado",F("bricolage800.ttf",120),430,PINK)
lw,lh=LO.size; h=put(c,LO,640,980,box=(int(lw*0.30),int(lh*0.0),int(lw*0.90),int(lh*0.85))); ctr(d,"Con salsa especial",F("hanken700.ttf",44),640+h+40,MUTE); sc.append(("s5",c,2.2))
# 6 papas
c=canvas(); d=ImageDraw.Draw(c); ctr(d,"Con papas fritas",F("bricolage800.ttf",106),430,CREAM); ctr(d,"caseras",F("caveat700.ttf",140),560,PINK)
h=put(c,LO,740,720); put(c,BL,740+h+28,720); sc.append(("s6",c,2.2))
# 7 cierre
c=Image.new("RGBA",(W,H),BG+(255,)); d=ImageDraw.Draw(c); L=330; lg=logo.resize((L,int(L*logo.height/logo.width)),Image.LANCZOS); c.alpha_composite(lg,((W-L)//2,380))
ctr(d,"Pídelos en",F("bricolage800.ttf",96),780,CREAM); ctr(d,"Sabor Rural",F("bricolage800.ttf",120),890,PINK)
ctr(d,"Barros Luco $7.000  ·  Lorino $8.000",F("hanken700.ttf",44),1090,CREAM)
d.rounded_rectangle([90,1220,990,1360],radius=70,fill=PINK); d.text((W/2,1290),"Mira la carta: link en la bio",font=F("bricolage800.ttf",52),fill=BG,anchor="mm")
ctr(d,"Ruta J-60 km 95, Licantén · @sabor_rural",F("hanken700.ttf",34),1700,MUTE); sc.append(("s7",c,3.0))
xf=0.25; names=[];durs=[]
for i,(n,c,dur) in enumerate(sc):
    c.convert("RGB").save(T+n+".png"); N=int(dur*30); zin=(i%2==0)
    z=f"1.0+0.06*on/{N}" if zin else f"1.06-0.06*on/{N}"
    subprocess.run(["ffmpeg","-v","error","-y","-loop","1","-i",T+n+".png","-vf",f"scale=2160:3840,zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={N}:s={W}x{H}:fps=30,format=yuv420p","-t",str(dur),"-an","-c:v","libx264","-crf","17",T+n+".mp4"],check=True)
    names.append(n);durs.append(dur)
cmd=["ffmpeg","-v","error","-y"]+sum([["-i",T+n+".mp4"] for n in names],[]); fc="";prev="[0:v]";off=0
for i in range(1,len(names)):
    off+=durs[i-1]-xf; fc+=f"{prev}[{i}:v]xfade=transition=fade:duration={xf}:offset={off:.2f}[x{i}];"; prev=f"[x{i}]"
total=sum(durs)-xf*(len(names)-1)
subprocess.run(cmd+["-filter_complex",fc.rstrip(";"),"-map",prev,"-c:v","libx264","-b:v","8M","-pix_fmt","yuv420p","-r","30","-an",T+"v.mp4"],check=True)
music(total,104,5,T+"m.wav")
subprocess.run(["ffmpeg","-v","error","-y","-i",T+"v.mp4","-i",T+"m.wav","-map","0:v","-map","1:a","-c:v","copy","-c:a","aac","-b:a","160k","-shortest","-movflags","+faststart",OUT+"reel-sandwich-v2.mp4"],check=True)
print(round(total,1))
