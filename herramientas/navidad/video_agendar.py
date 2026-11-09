# Video "Cómo agendar tu torta de Navidad" (sin voz, con subtítulos del guión + música) para grabar la voz encima
import subprocess, importlib.util
from PIL import Image, ImageDraw, ImageFilter, ImageOps
spec=importlib.util.spec_from_file_location("nb","/home/user/saborrural/herramientas/navidad/build.py"); N=importlib.util.module_from_spec(spec); spec.loader.exec_module(N)
B=N.B; T=B.T; F=B.F; OUT=N.OUT; W,H=1080,1920
SCREEN="/home/user/saborrural/media/como-encargar-torta/movil-con-voz-1080x1920.mp4"; LOGO=N.LOGO
CRE,PINK,GOLD,BG=N.CRE,N.PINK,N.GOLD,N.BG
rojo=N.photo("rojo"); bg=ImageOps.fit(rojo,(W,H),Image.LANCZOS).filter(ImageFilter.GaussianBlur(30)); bg=Image.blend(bg,Image.new("RGB",(W,H),(20,8,12)),0.55); bg.save(T+"nav-bg.png")
PW,PH=618,1100; PX,PY=(W-PW)//2,400
m=Image.new("L",(PW,PH),0); ImageDraw.Draw(m).rounded_rectangle([0,0,PW-1,PH-1],radius=46,fill=255); m.save(T+"nav-mask.png")
def overlay(name,title,sub,phone,y=250):
    im=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(im)
    if not phone:
        g=Image.new("RGBA",(W,820),(0,0,0,0)); gd=ImageDraw.Draw(g)
        for i in range(820): gd.line([(0,i),(W,i)],fill=(8,8,10,int(225*max(0,1-i/820)**1.2)))
        im.alpha_composite(g,(0,0))
        d=ImageDraw.Draw(im)
    if phone: d.rounded_rectangle([PX-3,PY-3,PX+PW+3,PY+PH+3],radius=49,outline=GOLD+(255,),width=5)
    f=F("bricolage800.ttf",64); d.text((W/2+2,y+3),title,font=f,fill=(0,0,0,150),anchor="ma"); d.text((W/2,y),title,font=f,fill=CRE+(255,),anchor="ma")
    f2=F("hanken700.ttf",44); lines=sub
    for i,t in enumerate(lines):
        yy=1560+i*72; w=int(d.textlength(t,font=f2))+56; d.rounded_rectangle([(W-w)//2,yy,(W+w)//2,yy+62],radius=26,fill=(10,10,12,235)); d.text((W/2,yy+31),t,font=f2,fill=(255,255,255,255),anchor="mm")
    im.save(T+name+".png")
def phone(name,ss,dur,png):
    fc=(f"[0:v]scale={PW}:{PH}:flags=lanczos,format=yuva420p[s];[3:v]format=gray[m];[s][m]alphamerge[ph];[1:v]fps=30[b];[b][ph]overlay={PX}:{PY}[c];[c][2:v]overlay=0:0[d];[d][4:v]overlay=10:280,format=yuv420p[o]")
    subprocess.run(["ffmpeg","-v","error","-y","-ss",str(ss),"-t",str(dur),"-i",SCREEN,"-loop","1","-t",str(dur),"-i",T+"nav-bg.png","-loop","1","-t",str(dur),"-i",T+png+".png","-loop","1","-t",str(dur),"-i",T+"nav-mask.png","-i",LOGO,"-filter_complex",fc,"-map","[o]","-t",str(dur),"-an","-c:v","libx264","-preset","slow","-crf","17",T+name+".mp4"],check=True)
def photo(name,dur,png):
    im=rojo; w,h=im.size; nw=int(h*9/16); x=int((w-nw)*.5); im.crop((x,0,x+nw,h)).resize((1620,2880),Image.LANCZOS).save(T+name+".jpg",quality=95)
    n=int(dur*30); fc=f"[0:v]zoompan=z='1.0+0.07*on/{n}':x='iw/2-(iw/zoom/2)':y='ih*0.95-(ih/zoom*0.95)':d={n}:s={W}x{H}:fps=30,eq=saturation=1.08[v];[v][1:v]overlay=0:0[a];[a][2:v]overlay=10:280,format=yuv420p[o]"
    subprocess.run(["ffmpeg","-v","error","-y","-loop","1","-i",T+name+".jpg","-i",T+png+".png","-i",LOGO,"-filter_complex",fc,"-map","[o]","-t",str(dur),"-an","-c:v","libx264","-preset","slow","-crf","17",T+name+".mp4"],check=True)
G=[("a","photo",4.5,["¿Ya pensaste en tu torta de Navidad?","Agéndala en nuestra página web"],"Navidad 2026",None),
   ("b","phone",4.2,["Primero, elige para cuántas personas:","de 15 a 40"],"1. ¿Cuántas personas?",9.0),
   ("c","phone",4.6,["Después, escoge tu sabor entre","nuestros 28 sabores, con el precio al tiro"],"2. Elige tu sabor",15.1),
   ("d","phone",5.0,["Luego, elige la fecha y el horario","de retiro, y agrega un mensaje"],"3. Fecha y mensaje",33.5),
   ("e","phone",4.6,["Paga en línea de forma segura:","tu pedido queda agendado"],"4. Paga en línea",44.5),
   ("f","photo",4.0,["Reserva con tiempo en nuestra web.","Hacemos especial tu Navidad"],"Reserva tu torta",None)]
names=[];durs=[]
for k,typ,d,sub,title,ss in G:
    overlay("ov"+k,title,sub,typ=="phone",y=270 if typ=="phone" else 380)
    (photo if typ=="photo" else (lambda n,dd,p,ss=ss: phone(n,ss,dd,p)))("s"+k,d,"ov"+k); names.append("s"+k); durs.append(d)
with open(T+"nav-concat.txt","w") as f:
    for n in names: f.write(f"file '{T}{n}.mp4'\n")
subprocess.run(["ffmpeg","-v","error","-y","-f","concat","-safe","0","-i",T+"nav-concat.txt","-c","copy",T+"nav-v.mp4"],check=True)
tot=sum(durs); B.music(tot,96,77,T+"nav-m.wav")
subprocess.run(["ffmpeg","-v","error","-y","-i",T+"nav-v.mp4","-i",T+"nav-m.wav","-map","0:v","-map","1:a","-c:v","copy","-c:a","aac","-ar","48000","-b:a","160k","-shortest","-movflags","+faststart",OUT+"video-agendar-navidad-con-musica.mp4"],check=True)
subprocess.run(["ffmpeg","-v","error","-y","-i",T+"nav-v.mp4","-c:v","copy","-an","-movflags","+faststart",OUT+"video-agendar-navidad-sin-audio.mp4"],check=True)
print("total",tot)
