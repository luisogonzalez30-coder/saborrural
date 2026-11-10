# Video "Agenda tu torta de Navidad" v2: ambiente navideño real (guirnalda, luces, esferas, pino, nieve), sin subtítulos
import subprocess, math, random, importlib.util
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageOps
spec=importlib.util.spec_from_file_location("nb","/home/user/saborrural/herramientas/navidad/build.py"); N=importlib.util.module_from_spec(spec); spec.loader.exec_module(N)
B=N.B; T=B.T; F=B.F; OUT=N.OUT; W,H=1080,1920; FPS=30
UP="/root/.claude/uploads/3bdc22a0-44b6-5463-a581-9b7d84b08b80/"
FOTOS=[("2ddca46d","jpg"),("f7bc744c","png"),("2168d3b5","jpg"),("f37eba40","jpg"),("f2f12815","jpg"),("688b509b","jpg"),("0d43dd2c","jpg"),("fcbabaa0","jpg"),("0c525da4","jpg"),("653600ac","jpg"),("acc33b63","jpg")]
SCREEN="/home/user/saborrural/media/como-encargar-torta/movil-con-voz-1080x1920.mp4"; LOGO=N.LOGO
CRE,PINK,GOLD=N.CRE,N.PINK,N.GOLD
rnd=random.Random(5)
# ---------- fondo festivo para escenas con celular ----------
def fondo():
    g=np.zeros((H,W,3),np.float32); y=np.linspace(0,1,H)[:,None]
    top=np.array([92,14,28]); bot=np.array([22,52,40])
    g[:]=(top*(1-y)[...,None]+bot*y[...,None]).reshape(H,1,3)
    im=Image.fromarray(g.astype(np.uint8)).convert("RGBA"); bk=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(bk)
    for _ in range(46):
        x,yy,r=rnd.randint(0,W),rnd.randint(150,H),rnd.randint(30,95); c=rnd.choice([(255,210,120),(255,120,120),(255,235,190),(120,220,150)])
        d.ellipse([x-r,yy-r,x+r,yy+r],fill=c+(rnd.randint(28,60),))
    bk=bk.filter(ImageFilter.GaussianBlur(14)); im.alpha_composite(bk); im.convert("RGB").save(T+"nv2-bg.png")
# ---------- decoración estática ----------
GREENS=[(18,86,52),(26,110,64),(14,66,42),(40,128,78)]
def needles(d,x,y,ang,n=1,L=(34,64)):
    for _ in range(n):
        a=ang+rnd.uniform(-1.1,1.1); l=rnd.uniform(*L); c=rnd.choice(GREENS)
        d.line([(x,y),(x+math.cos(a)*l,y+math.sin(a)*l)],fill=c+(255,),width=rnd.randint(4,6))
def bauble(d,x,y,r,col):
    d.line([(x,y-r-34),(x,y-r)],fill=(220,190,110,255),width=3)
    d.rectangle([x-8,y-r-12,x+8,y-r],fill=(232,199,120,255))
    d.ellipse([x-r,y-r,x+r,y+r],fill=col+(255,))
    hl=Image.new("RGBA",(2*r,2*r),(0,0,0,0)); hd=ImageDraw.Draw(hl); hd.ellipse([r*0.35,r*0.25,r*0.85,r*0.7],fill=(255,255,255,140)); hl=hl.filter(ImageFilter.GaussianBlur(r*0.12)); return (int(x-r),int(y-r),hl)
LIGHTS=[]
def deco():
    im=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(im); hl=[]
    pts=[]
    for i in range(0,W+30,12):
        t=i/W; yy=250+110*math.sin(math.pi*t)*(1-0.0)-30*math.sin(2*math.pi*t)*0
        pts.append((i,yy+8))
    # cable de luces
    d.line(pts,fill=(60,40,20,255),width=4)
    for (x,y) in pts:
        for _ in range(3): needles(d,x,y,math.pi/2,1)
    for k,(x,y) in enumerate(pts[::6]):
        LIGHTS.append((x,y+22,rnd.random()*6.28))
    # esferas colgantes
    for x,r,c in ((130,36,(196,30,50)),(330,30,(232,199,120)),(540,42,(196,30,50)),(760,30,(232,199,120)),(950,38,(196,30,50))):
        t=x/W; y=250+110*math.sin(math.pi*t)+62
        hl.append(bauble(d,x,y,r,c))
    for (x0,y0,hli) in hl: im.alpha_composite(hli,(x0,y0))
    # lazo rojo al centro
    cx,cy=540,250+110+4
    for s in (-1,1):
        d.ellipse([cx+s*70-52,cy-34,cx+s*70+10,cy+34] if s==1 else [cx-70-10,cy-34,cx-70+52,cy+34],fill=(196,30,50,255))
    d.ellipse([cx-22,cy-22,cx+22,cy+22],fill=(150,18,36,255))
    # ramas de pino en las esquinas inferiores
    for side in (0,1):
        bx=0 if side==0 else W; ang0=-0.35 if side==0 else math.pi+0.35
        for i in range(70):
            t=i/70; x=bx+(1 if side==0 else -1)*t*430; y=H-30-t*170+ (0)
            needles(d,x,y,ang0+(math.pi/2*0.6)*(1 if side==0 else -1),3,(40,90))
            needles(d,x,y,ang0-(math.pi/2*0.6)*(1 if side==0 else -1),3,(40,90))
        for (x,y,r,c) in ((60 if side==0 else W-60,H-150,32,(196,30,50)),(150 if side==0 else W-150,H-110,26,(232,199,120))):
            h=bauble(d,x,y,r,c); im.alpha_composite(h[2],(int(h[0]),int(h[1])))
    im.save(T+"nv2-deco.png")
# ---------- capa animada (nieve + luces) a PNG-sequence por pipe ----------
def soft(r,col=(255,255,255)):
    s=Image.new("RGBA",(4*r,4*r),(0,0,0,0)); d=ImageDraw.Draw(s); d.ellipse([r,r,3*r,3*r],fill=col+(255,)); return s.filter(ImageFilter.GaussianBlur(r*0.55 if r>3 else 0.6))
SPR={r:soft(r) for r in (2,3,4,6,9)}
def animar(total):
    deco(); base=Image.open(T+"nv2-deco.png"); n=int(total*FPS)
    flakes=[(rnd.random()*W,rnd.random()*H,rnd.choice([2,2,3,3,4,6,9]),rnd.uniform(0.5,1.6),rnd.uniform(0,6.28),rnd.uniform(18,70)) for _ in range(240)]
    glow={c:soft(14,c) for c in ((255,210,100),(255,90,90),(130,230,150),(255,240,200))}
    cols=list(glow)
    p=subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","rgba","-s",f"{W}x{H}","-r",str(FPS),"-i","-","-c:v","qtrle",T+"nv2-overlay.mov"],stdin=subprocess.PIPE)
    for f in range(n):
        t=f/FPS; fr=base.copy()
        for k,(x,y,ph) in enumerate(LIGHTS):
            a=0.45+0.55*(0.5+0.5*math.sin(t*3+ph)); g=glow[cols[k%4]].copy(); g.putalpha(g.getchannel("A").point(lambda v,a=a:int(v*a))); fr.alpha_composite(g,(int(x-28),int(y-28)))
        for (x,y,r,sp,ph,dr) in flakes:
            yy=(y+t*sp*60*(1+r/6))%(H+40)-20; xx=(x+math.sin(t*0.8+ph)*dr+t*8*sp)%W
            s=SPR[r]; op=0.55+0.45*(r/9); fr.alpha_composite(s,(int(xx-2*r),int(yy-2*r)))
        p.stdin.write(fr.tobytes())
    p.stdin.close(); p.wait()
# ---------- escenas ----------
PW,PH=620,1102; PX,PY=(W-PW)//2,560
m=Image.new("L",(PW,PH),0); ImageDraw.Draw(m).rounded_rectangle([0,0,PW-1,PH-1],radius=46,fill=255); m.save(T+"nv2-mask.png")
def marco(name):
    im=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(im); d.rounded_rectangle([PX-4,PY-4,PX+PW+4,PY+PH+4],radius=50,outline=GOLD+(255,),width=6); im.save(T+name+".png")
def phone(name,ss,dur):
    fc=f"[0:v]scale={PW}:{PH}:flags=lanczos,format=yuva420p[s];[2:v]format=gray[m];[s][m]alphamerge[ph];[1:v]fps=30[b];[b][ph]overlay={PX}:{PY},format=yuv420p[o]"
    subprocess.run(["ffmpeg","-v","error","-y","-ss",str(ss),"-t",str(dur),"-i",SCREEN,"-loop","1","-t",str(dur),"-i",T+"nv2-bg.png","-loop","1","-t",str(dur),"-i",T+"nv2-mask.png","-filter_complex",fc,"-map","[o]","-t",str(dur),"-an","-c:v","libx264","-preset","slow","-crf","17",T+name+".mp4"],check=True)
def photo(name,dur,idx):
    sub=[]; dd=dur/len(idx)
    for j,i in enumerate(idx):
        h,e=FOTOS[i]; im=ImageOps.exif_transpose(Image.open(f"{UP}{h}-image.{e}").convert("RGB")); w,hh=im.size; nw=int(hh*9/16)
        if nw>w: nh=int(w*16/9); y=(hh-nh)//2; im=im.crop((0,y,w,y+nh))
        else: x=(w-nw)//2; im=im.crop((x,0,x+nw,hh))
        im=im.resize((1620,2880),Image.LANCZOS); im.save(T+f"{name}_{j}.jpg",quality=95)
        n=int(dd*30); fc=f"[0:v]zoompan=z='1.0+0.07*on/{n}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={n}:s={W}x{H}:fps=30,eq=saturation=1.1,format=yuv420p[o]"
        subprocess.run(["ffmpeg","-v","error","-y","-loop","1","-i",T+f"{name}_{j}.jpg","-filter_complex",fc,"-map","[o]","-t",str(dd),"-an","-c:v","libx264","-preset","slow","-crf","17",T+f"{name}_{j}.mp4"],check=True); sub.append(T+f"{name}_{j}.mp4")
    open(T+f"{name}_l.txt","w").write("".join(f"file '{x}'\n" for x in sub))
    subprocess.run(["ffmpeg","-v","error","-y","-f","concat","-safe","0","-i",T+f"{name}_l.txt","-c","copy",T+name+".mp4"],check=True)
# ---------- títulos (gráficos, no subtítulos) ----------
def titulo(name,lines,y,sizes,cols):
    im=Image.new("RGBA",(W,H),(0,0,0,0)); g=Image.new("RGBA",(W,760),(0,0,0,0)); gd=ImageDraw.Draw(g)
    for i in range(760): gd.line([(0,i),(W,i)],fill=(10,4,8,int(215*max(0,1-i/760)**1.1)))
    im.alpha_composite(g,(0,260)); d=ImageDraw.Draw(im)
    yy=y
    for t,sz,c,fnt in lines:
        f=F(fnt,sz); d.text((W/2+3,yy+4),t,font=f,fill=(0,0,0,170),anchor="ma"); d.text((W/2,yy),t,font=f,fill=c+(255,),anchor="ma"); yy+=int(sz*1.12)
    im.save(T+name+".png")
IDX={"a":[0,1,2,3],"f":[6,4,5,9]}
SC=[("a","photo",4.5,None),("b","phone",4.2,9.0),("c","phone",4.6,15.1),("d","phone",5.0,33.5),("e","phone",4.6,44.5),("f","photo",4.0,None)]
def build():
    fondo(); marco("nv2-marco")
    titulo("t_a",[("Feliz Navidad",118,GOLD,"caveat700.ttf"),("Agenda tu torta",84,CRE,"bricolage800.ttf"),("navideña",84,PINK,"bricolage800.ttf")],470,0,0)
    stp=[("PASO 1","¿Para cuántas personas?"),("PASO 2","Elige tu sabor"),("PASO 3","Fecha y mensaje"),("PASO 4","Paga en línea")]
    for (k,(a,b)) in zip("bcde",stp): titulo("t_"+k,[(b,58,CRE,"bricolage800.ttf")],470,0,0)
    titulo("t_f",[("Reserva con tiempo",84,CRE,"bricolage800.ttf"),("en nuestra web",84,PINK,"bricolage800.ttf"),("Feliz Navidad",110,GOLD,"caveat700.ttf")],470,0,0)
    names=[];durs=[]
    for k,typ,d,ss in SC:
        (photo(k+"_v2",d,IDX[k]) if typ=="photo" else phone(k+"_v2",ss,d)); names.append(k+"_v2"); durs.append(d)
    with open(T+"nv2-concat.txt","w") as f:
        for n in names: f.write(f"file '{T}{n}.mp4'\n")
    subprocess.run(["ffmpeg","-v","error","-y","-f","concat","-safe","0","-i",T+"nv2-concat.txt","-c","copy",T+"nv2-base.mp4"],check=True)
    tot=sum(durs); animar(tot); B.music(tot,100,91,T+"nv2-m.wav")
    # composición: base + título por escena + marco del celular + deco/nieve (+ logo opcional)
    starts=[sum(durs[:i]) for i in range(len(durs))]
    def comp(logo,dest,audio):
        ins=["-i",T+"nv2-base.mp4","-i",T+"nv2-overlay.mov","-i",T+"nv2-marco.png"]+sum([["-i",T+f"t_{k}.png"] for k in "abcdef"],[])
        if logo: ins+=["-i",LOGO]
        fc="[0:v][2:v]overlay=0:0:enable='between(t,%.2f,%.2f)'[v0];"%(starts[1],tot-durs[5])
        prev="v0"
        for i,k in enumerate("abcdef"):
            fc+=f"[{prev}][{3+i}:v]overlay=0:0:enable='between(t,{starts[i]:.2f},{starts[i]+durs[i]:.2f})'[w{i}];"; prev=f"w{i}"
        fc+=f"[{prev}][1:v]overlay=0:0[z]"; prev="z"
        if logo: fc+=f";[z][9:v]overlay=10:290,format=yuv420p[o]"
        else: fc+=";[z]format=yuv420p[o]"
        cmd=["ffmpeg","-v","error","-y"]+ins+(["-i",T+"nv2-m.wav"] if audio else [])+["-filter_complex",fc,"-map","[o]"]+(["-map",f"{10 if logo else 9}:a","-c:a","aac","-ar","48000","-b:a","160k","-shortest"] if audio else ["-an"])+["-c:v","libx264","-preset","slow","-crf","17","-pix_fmt","yuv420p","-movflags","+faststart",OUT+dest]
        subprocess.run(cmd,check=True)
    comp(True,"agendar-navidad-v2-con-logo.mp4",True); comp(False,"agendar-navidad-v2-sin-logo.mp4",True); comp(False,"agendar-navidad-v2-sin-logo-sin-audio.mp4",False)
    print("total",tot)
if __name__=="__main__": build()
