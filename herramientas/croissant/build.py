# Croissant de jamón colonial y queso · historia 9:16 + reel · estilo de marca
import sys, subprocess
sys.path.insert(0,"/home/user/saborrural/herramientas/mario2")
import build as B
from PIL import Image, ImageDraw
SRC="/root/.claude/uploads/3bdc22a0-44b6-5463-a581-9b7d84b08b80/98bcc313-image.jpg"
OUT="/home/user/saborrural/media/croissant/"; T=B.T; W,H=1080,1920; C,K,BG,MUTE=B.CREAM,B.PINK,B.BG,B.MUTE
F=B.F
base=Image.open(SRC).convert("RGB"); print(base.size)
# lienzo: foto subida 420 px para que el texto no tape el relleno; degradado a fondo de marca abajo
canvas=Image.new("RGB",(W,H),BG); canvas.paste(base.resize((W,H),Image.LANCZOS),(0,-420))
g=Image.new("RGBA",(W,H),(0,0,0,0)); gd=ImageDraw.Draw(g)
for yy in range(1280,1500): gd.line([(0,yy),(W,yy)],fill=BG+(int(255*min(1,(yy-1280)/200)),))
gd.rectangle([0,1500,W,H],fill=BG+(255,)); canvas=canvas.convert("RGBA"); canvas.alpha_composite(g); canvas=canvas.convert("RGB")
big=canvas.resize((2160,3840),Image.LANCZOS); big.save(T+"croi-big.jpg",quality=95)
def price_chip(im,y):
    d=ImageDraw.Draw(im); t="$4.500"; f=F("bricolage800.ttf",64); w=int(d.textlength(t,font=f))+60
    d.rounded_rectangle([70,y,70+w,y+92],radius=46,fill=K); d.text((70+30,y+46),t,font=f,fill=BG,anchor="lm"); return y+120
def card(name,pill,lines,sub,size=84,chip=False):
    im=B.frame_logo(W,H); pass
    y=1470 if not chip else 1340
    if chip: y=price_chip(im,y)
    B.text_block(im,W,y if chip else y,pill,lines,sub,size); im.save(T+name+".png")
# ---------- HISTORIA ----------
def historia():
    im=canvas.convert("RGBA")
    y=price_chip(im,1330)
    B.text_block(im,W,y-0,"CROISSANT",[[("Jamón colonial",C)],[("y queso",K)]],"Mira la carta en nuestra página web",96)
    d=ImageDraw.Draw(im); d.text((W/2,1840),"Ruta J-60 km 95, Licantén · @sabor_rural",font=F("hanken700.ttf",30),fill=MUTE,anchor="ma")
    im.alpha_composite(B.frame_logo(W,H)); im.convert("RGB").save(OUT+"historia-croissant.jpg",quality=95)
# ---------- REEL ----------
def scene(name,dur,png,z0,z1,fx,fy,fx2=None,fy2=None):
    N=int(dur*30); fx2=fx if fx2 is None else fx2; fy2=fy if fy2 is None else fy2
    z=f"{z0}+({z1}-{z0})*on/{N}"; cx=f"({fx}+({fx2}-{fx})*on/{N})"; cy=f"({fy}+({fy2}-{fy})*on/{N})"
    fc=(f"[0:v]zoompan=z='{z}':x='iw*{cx}-(iw/zoom*{cx})':y='ih*{cy}-(ih/zoom*{cy})':d={N}:s={W}x{H}:fps=30,eq=contrast=1.05:saturation=1.1[v];[v][1:v]overlay=0:0,format=yuv420p[o]")
    subprocess.run(["ffmpeg","-v","error","-y","-loop","1","-i",T+"croi-big.jpg","-i",T+png+".png","-filter_complex",fc,"-map","[o]","-t",str(dur),"-an","-c:v","libx264","-preset","slow","-crf","17",T+name+".mp4"],check=True)
def reel():
    B.rend if False else None
    card("c0",None,[[("¿Antojo de algo",C)],[("salado?",K)]],"Mira lo que tenemos en Sabor Rural",size=96)
    card("c1","EL RELLENO",[[("Jamón colonial",C)],[("y queso",K)]],None,size=92)
    card("c2","EL PAN",[[("Croissant ",C),("dorado",K)]],"Hojaldrado y crujiente")
    card("c3","EN LA CARTA",[[("Croissant de jamón",C)],[("colonial y queso",K)]],None,size=80,chip=True)
    # tarjeta final de marca
    im=Image.new("RGBA",(W,H),BG+(255,)); im.alpha_composite(B.frame_logo(W,H)); d=ImageDraw.Draw(im)
    cx=lambda t,f,y,c: d.text((W/2,y),t,font=f,fill=c,anchor="ma")
    cx("Croissant de",F("caveat700.ttf",100),330,K); cx("jamón colonial",F("bricolage800.ttf",100),440,C); cx("y queso",F("bricolage800.ttf",100),550,C)
    d.rounded_rectangle([360,730,720,860],radius=65,fill=K); cx("$4.500",F("bricolage800.ttf",78),754,BG)
    cx("Mira la carta y pide",F("bricolage800.ttf",56),960,C); cx("en nuestra página web",F("bricolage800.ttf",56),1040,C)
    d.rounded_rectangle([190,1160,890,1290],radius=65,outline=K+(255,),width=4); cx("Link en la bio",F("caveat700.ttf",82),1176,K)
    cx("Ruta J-60 km 95, Licantén · @sabor_rural",F("hanken700.ttf",32),1760,MUTE); im.save(T+"cend.png")
    scene("k0",2.8,"c0",1.0,1.10,0.5,0.45)
    scene("k1",2.8,"c1",1.0,1.25,0.45,0.52)
    scene("k2",2.8,"c2",1.28,1.0,0.5,0.45,0.5,0.42)
    scene("k3",2.8,"c3",1.0,1.12,0.5,0.45)
    subprocess.run(["ffmpeg","-v","error","-y","-loop","1","-t","3.6","-i",T+"cend.png","-vf","fps=30,format=yuv420p","-c:v","libx264","-crf","17",T+"kend.mp4"],check=True)
    B.OUT=OUT; B.T=T
    B.assemble(["k0","k1","k2","k3","kend"],[2.8,2.8,2.8,2.8,3.6],"reel-croissant",104,31)
if __name__=="__main__": historia(); reel()
