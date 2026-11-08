# Reel 2 con la voz real de Luis (voz-original.opus) explicando cómo encargar en la web · subtítulos · música baja
import sys, subprocess, importlib.util
spec=importlib.util.spec_from_file_location("rosa_build","/home/user/saborrural/herramientas/rosa/build.py"); R=importlib.util.module_from_spec(spec); spec.loader.exec_module(R)
from PIL import Image, ImageDraw
B=R.B; T=R.T; F=R.F; W,H=R.W,R.H; OUT=R.OUT
VOZ="/home/user/saborrural/media/como-encargar-torta/voz-original.opus"
def sub_extra(txt):
    def f(im):
        d=ImageDraw.Draw(im); font=F("hanken700.ttf",46); w=int(d.textlength(txt,font=font))+60
        d.rounded_rectangle([(W-w)//2,1430,(W+w)//2,1430+84],radius=30,fill=(10,10,12,235)); d.text((W/2,1430+42),txt,font=font,fill=(255,255,255,255),anchor="mm")
        if R.phone_flag[0]: R.phone_frame(im)
    return f
R.phone_flag=[False]
def png(name,lines,sub,phone,y=250,size=66,col=None,acc=None):
    R.phone_flag[0]=phone
    if phone: R.text_png(name,lines,R.WHITE,R.WHITE,y=y,size=size,shadow=True,extra=sub_extra(sub))
    else: R.text_png(name,lines,R.DARK,R.PINKD,y=y,size=size,extra=sub_extra(sub))
# (nombre, tipo, ss, dur, título, subtítulo)
G=[
 [("c1","photo",0,2.35,["¿Quieres una","torta así?"],"¿Buscas una torta para una ocasión especial?",(1.0,1.10,0.5,0.45)),
  ("c2","photo",0,2.40,["Encargarla es","muy fácil"],"Encargarla en Sabor Rural es muy fácil",(1.10,1.16,0.5,0.45)),
  ("c3","photo",0,2.79,["Desde nuestra","página web"],"y lo haces en nuestra página web",(1.16,1.26,0.5,0.45))],
 [("c4","phone",9.0,2.40,["1. ¿Cuántas personas?"],"Primero, elige el tamaño",None),
  ("c5","phone",11.4,2.87,["1. ¿Cuántas personas?"],"desde 15 hasta 40 personas",None)],
 [("c6","phone",15.1,3.32,["2. Elige el sabor"],"Después, descubre nuestros 28 sabores",None)],
 [("c7","phone",28.0,2.00,["3. Fecha y mensaje"],"Luego, personaliza tu pedido",None),
  ("c8","phone",33.5,2.69,["3. Fecha y mensaje"],"Elige la fecha y el horario",None)],
 [("c9","phone",44.5,2.60,["4. Paga en línea"],"Ya casi está: revisa los detalles",None),
  ("c10","phone",47.1,3.26,["4. Paga en línea"],"y paga de forma segura",None)],
 [("c11","photo",0,3.34,["Reserva en","nuestra web"],"Entra en nuestra web y encarga la tuya",(1.14,1.0,0.5,0.5))],
]
AUD=[(0.73,8.27),(9.08,14.35),(15.09,18.41),[(26.11,28.05),(28.45,31.08)],(36.79,42.65),(48.74,50.88)]
GAP=0.15
def build():
    B.OUT=OUT; B.T=T
    names=[]; durs=[]
    for gi,grp in enumerate(G):
        for k,(n,typ,ss,d,title,sub,zoom) in enumerate(grp):
            last=(k==len(grp)-1); dd=d+(GAP if (last and gi<len(G)-1) else 0)
            png(n+"t",title,sub,typ=="phone",y=250,size=72 if typ=="photo" else 62)
            if typ=="photo":
                z0,z1,fx,fy=zoom; R.scene_photo(n,dd,n+"t",z0,z1,fx,fy)
            else: R.scene_phone(n,ss,dd,n+"t")
            names.append(n); durs.append(dd)
    total=sum(durs); print("video",round(total,2))
    # lista de concatenación (cortes secos, sincronizados con la voz)
    with open(T+"concat.txt","w") as f:
        for n in names: f.write(f"file '{T}{n}.mp4'\n")
    subprocess.run(["ffmpeg","-v","error","-y","-f","concat","-safe","0","-i",T+"concat.txt","-c","copy",T+"voz-v.mp4"],check=True)
    # voz: segmentos + huecos
    parts=[]; inputs=[]; fi=""; idx=0
    segs=[]
    for g in AUD:
        segs.append(g if isinstance(g,list) else [g])
    chain=[]
    for gi,g in enumerate(segs):
        for k,(a,b) in enumerate(g):
            fi+=f"[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d=0.02,afade=t=out:st={b-a-0.04:.2f}:d=0.04[s{idx}];"; chain.append(f"[s{idx}]"); idx+=1
            gap=0.12 if k<len(g)-1 else (GAP if gi<len(segs)-1 else 1.2)
            fi+=f"aevalsrc=0:d={gap}:s=48000:c=mono[g{idx}];"; chain.append(f"[g{idx}]")
    fi+="".join(chain)+f"concat=n={len(chain)}:v=0:a=1,aresample=48000,loudnorm=I=-16:TP=-1.5[voz]"
    subprocess.run(["ffmpeg","-v","error","-y","-i",VOZ,"-filter_complex",fi,"-map","[voz]",T+"voz-a.wav"],check=True)
    B.music(total,100,47,T+"voz-m.wav")
    subprocess.run(["ffmpeg","-v","error","-y","-i",T+"voz-v.mp4","-i",T+"voz-a.wav","-i",T+"voz-m.wav","-filter_complex","[2:a]volume=0.20[m];[1:a][m]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.95[a]",
        "-map","0:v","-map","[a]","-c:v","copy","-c:a","aac","-ar","48000","-b:a","160k","-shortest","-movflags","+faststart",OUT+"reel-rosa-2-cotizador-voz.mp4"],check=True)
if __name__=="__main__": build()
