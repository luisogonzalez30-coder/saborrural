# Torta rosa y dorada · 2 reels limpios (sin marco ni degradado): logo blanco arriba a la izquierda + texto corto
import sys, subprocess
sys.path.insert(0,"/home/user/saborrural/herramientas/mario2")
import build as B
from PIL import Image, ImageDraw, ImageFilter
U="/root/.claude/uploads/3bdc22a0-44b6-5463-a581-9b7d84b08b80/"
PHOTO=U+"5448afe2-image.png"; SCREEN="/home/user/saborrural/media/como-encargar-torta/movil-con-voz-1080x1920.mp4"
T=B.T; OUT="/home/user/saborrural/media/rosa/"; W,H=1080,1920; F=B.F
LOGO=T.replace("mario2","gem")+"white.png"
DARK=(32,22,26); PINKD=(214,76,116); WHITE=(255,255,255); PINK=B.PINK
img=Image.open(PHOTO).convert("RGB"); print(img.size)
crop=img.crop((80,0,944,1536)); crop.resize((1728,3072),Image.LANCZOS).save(T+"rosa-big.png")
bg=img.resize((1080,int(1536*1080/1024)),Image.LANCZOS).crop((0,0,1080,1920)).resize((1080,1920)).filter(ImageFilter.GaussianBlur(26))
bg=Image.blend(bg,Image.new("RGB",(1080,1920),(24,16,20)),0.42); bg.save(T+"rosa-bg.png")
def text_png(name,lines,col_main,col_acc,y=250,size=84,shadow=False,extra=None):
    im=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(im)
    for k,t in enumerate(lines):
        col=col_acc if k==len(lines)-1 and len(lines)>1 else col_main
        f=F("bricolage800.ttf",size)
        if shadow: d.text((W/2+2,y+3),t,font=f,fill=(0,0,0,120),anchor="ma")
        d.text((W/2,y),t,font=f,fill=col+(255,),anchor="ma"); y+=int(size*1.1)
    if extra: extra(im)
    im.save(T+name+".png")
def scene_photo(name,dur,png,z0,z1,fx,fy,fx2=None,fy2=None):
    N=int(dur*30); fx2=fx if fx2 is None else fx2; fy2=fy if fy2 is None else fy2
    z=f"{z0}+({z1}-{z0})*on/{N}"; cx=f"({fx}+({fx2}-{fx})*on/{N})"; cy=f"({fy}+({fy2}-{fy})*on/{N})"
    fc=(f"[0:v]zoompan=z='{z}':x='iw*{cx}-(iw/zoom*{cx})':y='ih*{cy}-(ih/zoom*{cy})':d={N}:s={W}x{H}:fps=30,eq=saturation=1.06[v];[v][1:v]overlay=0:0[a];[a][2:v]overlay=30:40,format=yuv420p[o]")
    subprocess.run(["ffmpeg","-v","error","-y","-loop","1","-i",T+"rosa-big.png","-i",T+png+".png","-i",LOGO,"-filter_complex",fc,"-map","[o]","-t",str(dur),"-an","-c:v","libx264","-preset","slow","-crf","17",T+name+".mp4"],check=True)
PW,PH=756,1344; PX,PY=(W-PW)//2,420
mask=Image.new("L",(PW,PH),0); ImageDraw.Draw(mask).rounded_rectangle([0,0,PW-1,PH-1],radius=46,fill=255); mask.save(T+"rosa-mask.png")
def phone_frame(im):
    ImageDraw.Draw(im).rounded_rectangle([PX-3,PY-3,PX+PW+3,PY+PH+3],radius=49,outline=PINK+(255,),width=5)
def scene_phone(name,ss,dur,png):
    fc=(f"[0:v]scale={PW}:{PH}:flags=lanczos,format=yuva420p[s];[3:v]format=gray[m];[s][m]alphamerge[ph];"
        f"[1:v]fps=30[b];[b][ph]overlay={PX}:{PY}[c];[c][2:v]overlay=0:0[d];[d][4:v]overlay=30:40,format=yuv420p[o]")
    subprocess.run(["ffmpeg","-v","error","-y","-ss",str(ss),"-t",str(dur),"-i",SCREEN,"-loop","1","-t",str(dur),"-i",T+"rosa-bg.png","-loop","1","-t",str(dur),"-i",T+png+".png",
        "-loop","1","-t",str(dur),"-i",T+"rosa-mask.png","-i",LOGO,"-filter_complex",fc,"-map","[o]","-t",str(dur),"-an","-c:v","libx264","-preset","slow","-crf","17",T+name+".mp4"],check=True)
def build():
    B.OUT=OUT; B.T=T
    # ---- Reel 1: Rosa y dorado (macro, 10 s) ----
    text_png("r1a",["Rosa y dorado"],DARK,PINKD,y=250,size=96)
    text_png("r1b",["Detalles","en dorado"],DARK,PINKD,y=1290,size=92)
    text_png("r1c",["Cada detalle,","a tu medida"],DARK,PINKD,y=1290,size=88)
    text_png("r1d",["Hecha en","Sabor Rural"],DARK,PINKD,y=240,size=92)
    text_png("r1e",["Comenta","TORTA"],DARK,PINKD,y=240,size=110)
    scene_photo("p1",2.4,"r1a",1.0,1.30,0.62,0.30)
    scene_photo("p2",2.1,"r1b",1.25,1.45,0.55,0.60,0.45,0.57)
    scene_photo("p3",2.1,"r1c",1.25,1.45,0.12,0.66,0.20,0.62)
    scene_photo("p4",2.3,"r1d",1.15,1.0,0.5,0.45)
    scene_photo("p5",2.6,"r1e",1.0,1.08,0.5,0.52)
    B.assemble(["p1","p2","p3","p4","p5"],[2.4,2.1,2.1,2.3,2.6],"reel-rosa-1-detalle",100,41)
    # ---- Reel 2: Cotiza en 15 s ----
    text_png("r2a",["Cotiza una torta","así en 15 segundos"],DARK,PINKD,y=250,size=78)
    text_png("r2s1",["1. ¿Cuántas personas?"],WHITE,WHITE,y=250,size=66,shadow=True,extra=phone_frame)
    text_png("r2s2",["2. Elige el sabor"],WHITE,WHITE,y=250,size=66,shadow=True,extra=phone_frame)
    text_png("r2s3",["3. Fecha y mensaje"],WHITE,WHITE,y=250,size=66,shadow=True,extra=phone_frame)
    text_png("r2s4",["4. Paga en línea"],WHITE,WHITE,y=250,size=66,shadow=True,extra=phone_frame)
    text_png("r2e",["Retiro gratis.","Comenta TORTA"],DARK,PINKD,y=250,size=84)
    scene_photo("q0",2.6,"r2a",1.0,1.12,0.5,0.45)
    scene_phone("q1",9.5,3.0,"r2s1"); scene_phone("q2",19.0,3.0,"r2s2"); scene_phone("q3",34.3,3.0,"r2s3"); scene_phone("q4",44.5,3.0,"r2s4")
    scene_photo("q5",2.8,"r2e",1.12,1.0,0.5,0.5)
    B.assemble(["q0","q1","q2","q3","q4","q5"],[2.6,3,3,3,3,2.8],"reel-rosa-2-cotizador",104,43)
if __name__=="__main__": build()
