# Reel Navidad "quedan pocos cupos": gancho + demo real de la web (grabación) + urgencia + cierre, con voz de ElevenLabs (Catalina, chilena)
import subprocess, os, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
A="/home/user/saborrural/enlaces-assets/"; D="/home/user/saborrural/media/navidad/"; C=D+"cupos/"
T="/tmp/claude-0/-home-user/3bdc22a0-44b6-5463-a581-9b7d84b08b80/scratchpad/cupos/"; os.makedirs(T,exist_ok=True)
NAV="/home/user/saborrural/tema-v12/archivos/sr-nav-%02d.jpg"
F=lambda n,s: ImageFont.truetype(A+n,s)
W,H=1080,1920; CRE=(243,241,234); PINK=(245,154,172); GOLD=(232,199,120); BG=(12,13,15)
logo=Image.open(A+"logo.png").convert("RGBA")
def grad():
    y=np.linspace(0,1,H)[:,None,None]; top=np.array([92,14,28]); bot=np.array([22,52,40])
    g=(top*(1-y)+bot*y)*np.ones((1,W,1)); return Image.fromarray(g.astype(np.uint8)).convert("RGBA")
def rounded(im,r):
    m=Image.new("L",im.size,0); ImageDraw.Draw(m).rounded_rectangle([0,0,im.width-1,im.height-1],radius=r,fill=255); im=im.convert("RGBA"); im.putalpha(m); return im
def card(c,n,x,y,w):
    im=Image.open(NAV%n).convert("RGB"); h=int(im.height*w/im.width); sh=Image.new("RGBA",(w+60,h+60),(0,0,0,0)); ImageDraw.Draw(sh).rounded_rectangle([30,40,w+30,h+40],radius=30,fill=(0,0,0,120)); sh=sh.filter(ImageFilter.GaussianBlur(14)); c.alpha_composite(sh,(x-30,y-30))
    c.alpha_composite(rounded(im.resize((w,h),Image.LANCZOS),30),(x,y)); return h
def ctr(d,t,f,y,col): d.text((W/2,y),t,font=f,fill=col,anchor="ma")
def pill(d,t,y,fs=62,col=PINK,tc=BG):
    fo=F("bricolage800.ttf",fs); w=int(d.textlength(t,font=fo))+80; d.rounded_rectangle([(W-w)//2,y,(W+w)//2,y+fs+50],radius=(fs+50)//2,fill=col); d.text((W/2,y+(fs+50)/2),t,font=fo,fill=tc,anchor="mm")
def logo_tl(c,L=170,xy=(64,210)):
    lg=logo.resize((L,int(L*logo.height/logo.width)),Image.LANCZOS); c.alpha_composite(lg,xy)
def garland(c):
    d=ImageDraw.Draw(c); pts=[(i,235+55*math.sin(math.pi*i/W)) for i in range(0,W+1,6)]
    d.line(pts,fill=(26,110,64,255),width=10)
    for i,(x,y) in enumerate(pts[::14]):
        col=[(255,210,120),(255,110,110),(255,235,190),(120,220,150)][i%4]; d.ellipse([x-9,y+8,x+9,y+26],fill=col+(255,))
# 1 gancho
c=grad(); garland(c); d=ImageDraw.Draw(c); logo_tl(c,150,(64,300)); ctr(d,"Navidad 2026",F("caveat700.ttf",110),330,GOLD)
pill(d,"Quedan pocos cupos",450,66)
card(c,1,90,640,900); c.convert("RGB").save(T+"s1.png")
# 2 urgencia
c=grad(); garland(c); d=ImageDraw.Draw(c); logo_tl(c,150,(64,300))
ctr(d,"Las fechas",F("bricolage800.ttf",120),430,CRE); ctr(d,"se llenan rápido",F("bricolage800.ttf",120),560,PINK)
w=320; xs=[60,380,700]
for k,(n,dy) in enumerate(((4,40),(2,0),(8,40))):
    card(c,n,xs[k],820+dy,w)
pill(d,"Reserva hoy",1420,70,GOLD,BG)
ctr(d,"Retiro gratis en el local",F("hanken700.ttf",44),1600,CRE); c.convert("RGB").save(T+"s2.png")
# 3 cierre
c=Image.new("RGBA",(W,H),BG+(255,)); g=grad(); c=Image.blend(c,g,0.55); d=ImageDraw.Draw(c); L=300; lg=logo.resize((L,int(L*logo.height/logo.width)),Image.LANCZOS); c.alpha_composite(lg,((W-L)//2,330))
ctr(d,"Navidad 2026",F("caveat700.ttf",110),700,GOLD); ctr(d,"Reserva tu torta",F("bricolage800.ttf",100),830,CRE); ctr(d,"en nuestra web",F("bricolage800.ttf",100),950,PINK)
pill(d,"Quedan pocos cupos",1140,58,GOLD,BG)
d.rounded_rectangle([210,1330,870,1440],radius=55,outline=PINK,width=4); d.text((W/2,1385),"Link en la bio",font=F("caveat700.ttf",84),fill=PINK,anchor="mm")
ctr(d,"Ruta J-60 km 95, Licantén · @sabor_rural",F("hanken700.ttf",34),1740,(169,171,163)); c.convert("RGB").save(T+"s3.png")
# pastilla para la demo web
c=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(c); logo_tl(c,130,(50,75)); fo=F("bricolage800.ttf",40); t="Quedan pocos cupos"; w=int(d.textlength(t,font=fo))+60; x0=230; d.rounded_rectangle([x0,100,x0+w,180],radius=40,fill=PINK); d.text((x0+w/2,140),t,font=fo,fill=BG,anchor="mm"); c.save(T+"web-ov.png")
def still(n,dur,zin):
    N=int(dur*30); z=f"1.0+0.05*on/{N}" if zin else f"1.05-0.05*on/{N}"
    subprocess.run(["ffmpeg","-v","error","-y","-loop","1","-i",T+n+".png","-vf",f"scale=2160:3840,zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={N}:s={W}x{H}:fps=30,format=yuv420p","-t",str(dur),"-an","-c:v","libx264","-crf","17",T+n+".mp4"],check=True)
still("s1",2.6,True); still("s2",3.2,False); still("s3",4.0,True)
SRC=D+"agendar-navidad-v2-sin-logo-sin-audio.mp4"
subprocess.run(["ffmpeg","-v","error","-y","-ss","4.6","-t","18.8","-i",SRC,"-i",T+"web-ov.png","-filter_complex","[0:v]setpts=PTS/1.74,fps=30[a];[a][1:v]overlay=0:0,format=yuv420p[o]","-map","[o]","-t","10.8","-an","-c:v","libx264","-crf","17",T+"web.mp4"],check=True)
# ensamble con fundidos
names=["s1","web","s2","s3"]; durs=[2.6,10.8,3.2,4.0]; xf=0.2
cmd=["ffmpeg","-v","error","-y"]+sum([["-i",T+n+".mp4"] for n in names],[]); fc="";prev="[0:v]";off=0
for i in range(1,len(names)):
    off+=durs[i-1]-xf; fc+=f"{prev}[{i}:v]xfade=transition=fade:duration={xf}:offset={off:.2f}[x{i}];"; prev=f"[x{i}]"
total=sum(durs)-xf*(len(names)-1)
subprocess.run(cmd+["-filter_complex",fc.rstrip(";"),"-map",prev,"-c:v","libx264","-b:v","8M","-pix_fmt","yuv420p","-r","30","-an",T+"v.mp4"],check=True)
# música festiva suave bajo la voz
import sys; sys.path.insert(0,"/home/user/saborrural/herramientas/reel-sandwich"); from _music import music
music(total,100,9,T+"m.wav")
subprocess.run(["ffmpeg","-v","error","-y","-i",T+"v.mp4","-i",C+"voz.mp3","-i",T+"m.wav","-filter_complex",
 f"[1:a]adelay=300|300,volume=1.25,acompressor=threshold=-18dB:ratio=3[v];[2:a]volume=0.20,afade=t=out:st={total-1.5:.1f}:d=1.5[m];[v][m]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-16:TP=-1.5[a]",
 "-map","0:v","-map","[a]","-c:v","copy","-c:a","aac","-b:a","160k","-t",f"{total:.2f}","-movflags","+faststart",D+"reel-navidad-cupos.mp4"],check=True)
print(round(total,1))
