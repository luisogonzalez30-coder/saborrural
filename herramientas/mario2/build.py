# Torta Super Mario · grid (portada collage + carrusel) y 2 reels · estilo de marca
import subprocess, numpy as np, wave, sys
from PIL import Image, ImageDraw, ImageFont, ImageOps
U="/root/.claude/uploads/3bdc22a0-44b6-5463-a581-9b7d84b08b80/"; AS="/home/user/saborrural/enlaces-assets/"
OUT="/home/user/saborrural/media/mario2/"; T="/tmp/claude-0/-home-user/3bdc22a0-44b6-5463-a581-9b7d84b08b80/scratchpad/mario2/"
P={n:U+i+"-image.jpg" for n,i in enumerate("65016087 13617df5 e19fb63d 124c0efb eb5cc4d7 9464c753 92ec1cbb d823ac3c f899b234 5416a407 1cf644fe 10b342c5 b8e99451 68d5a924".split(),1)}
F=lambda n,s: ImageFont.truetype(AS+n,s)
BG=(12,13,15); CREAM=(243,241,234); PINK=(245,154,172); MUTE=(169,171,163)
from PIL import ImageFilter
def quitar_qr(im):
    # tapa la etiqueta QR de la mesa copiando madera contigua (difuminada en los bordes)
    x0,y0,x1,y1=1360,715,1740,915; w,h=x1-x0,y1-y0
    patch=im.crop((x0+w+20,y0,x1+w+20,y1)); m=Image.new("L",(w,h),0); ImageDraw.Draw(m).rounded_rectangle([14,14,w-14,h-14],radius=22,fill=255)
    m=m.filter(ImageFilter.GaussianBlur(10)); im.paste(patch,(x0,y0),m); return im
def photo(n):
    im=ImageOps.exif_transpose(Image.open(P[n]).convert("RGB"))
    if n==14: im=quitar_qr(im)
    return im.resize((1512,2016),Image.LANCZOS)   # 3:4, 1512x2016
def frame_logo(W,H):
    im=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(im)
    d.rounded_rectangle([22,22,W-22,H-22],radius=40,outline=PINK+(255,),width=3)
    lg=Image.open(AS+"logo.png").convert("RGBA"); L=int(W*0.115); lg=lg.resize((L,int(L*lg.height/lg.width))); im.alpha_composite(lg,(54,54)); return im
def shade(im,y0,h,W,a=215):
    g=Image.new("RGBA",(W,h),(0,0,0,0)); gd=ImageDraw.Draw(g)
    for i in range(h): gd.line([(0,i),(W,i)],fill=(8,8,10,int(a*min(1,(i/(h*0.55))**1.4))))
    im.alpha_composite(g,(0,y0))
def text_block(im,W,y,pill,lines,sub,tsize):
    d=ImageDraw.Draw(im)
    if pill:
        f=F("bricolage800.ttf",38); w=int(d.textlength(pill,font=f))+54
        d.rounded_rectangle([70,y,70+w,y+68],radius=34,fill=PINK); d.text((70+27,y+34),pill,font=f,fill=BG,anchor="lm"); y+=96
    for segs in lines:
        x=70
        for t,col in segs:
            f=F("bricolage800.ttf",tsize); d.text((x,y),t,font=f,fill=col); x+=int(d.textlength(t,font=f))
        y+=int(tsize*1.08)
    if sub: d.text((70,y+12),sub,font=F("hanken700.ttf",36),fill=CREAM)
    return y
C=CREAM; K=PINK
# ======================= CARRUSEL 4:5 =======================
W,H=1080,1350
def crop_photo(n,fy=0.5,fx=0.5,size=(W,H)):
    im=photo(n); ar=size[0]/size[1]; w,h=im.size
    if w/h>ar: nw=int(h*ar); x=int((w-nw)*fx); im=im.crop((x,0,x+nw,h))
    else: nh=int(w/ar); y=int((h-nh)*fy); im=im.crop((0,y,w,y+nh))
    return im.resize(size,Image.LANCZOS)
def slide(name,n,pill,lines,sub,fy=0.5,fx=0.5):
    im=crop_photo(n,fy,fx).convert("RGBA"); shade(im,H-560,560,W)
    text_block(im,W,H-330 if pill else H-300,pill,lines,sub,76)
    im.alpha_composite(frame_logo(W,H)); im.convert("RGB").save(OUT+name,quality=95)
def collage():
    im=Image.new("RGBA",(W,H),BG+(255,)); d=ImageDraw.Draw(im)
    d.text((W/2,86),"Torta personalizada",font=F("caveat700.ttf",78),fill=PINK,anchor="ma")
    d.text((W/2,172),"Super Mario",font=F("bricolage800.ttf",118),fill=CREAM,anchor="ma")
    cw,ch=495,300; gx=(W-2*cw-26)//2; y0=300
    sel=[(3,0.62,0.5),(2,0.52,0.5),(9,0.66,0.5),(10,0.62,0.5),(14,0.50,0.5),(12,0.58,0.5)]
    for k,(n,fy,fx) in enumerate(sel):
        c=crop_photo(n,fy,fx,(cw,ch)); r=Image.new("L",(cw,ch),0); ImageDraw.Draw(r).rounded_rectangle([0,0,cw-1,ch-1],radius=26,fill=255)
        c=c.convert("RGBA"); c.putalpha(r); im.alpha_composite(c,(gx+(k%2)*(cw+26),y0+(k//2)*(ch+22)))
    d.text((W/2,1268),"Hecha a tu medida en Sabor Rural",font=F("hanken700.ttf",36),fill=MUTE,anchor="ma")
    im.alpha_composite(frame_logo(W,H)); im.convert("RGB").save(OUT+"carrusel-01-portada.jpg",quality=95)
def info_slide():
    im=Image.new("RGBA",(W,H),BG+(255,)); im.alpha_composite(frame_logo(W,H)); d=ImageDraw.Draw(im)
    cx=lambda t,f,y,c: d.text((W/2,y),t,font=f,fill=c,anchor="ma")
    cx("Tu torta,",F("caveat700.ttf",100),230,PINK); cx("a tu medida",F("bricolage800.ttf",110),330,CREAM)
    y=520
    for t in ("De 15 a 40 personas","28 sabores para elegir","Pagas en línea y la retiras gratis"):
        cx(t,F("bricolage800.ttf",54),y,CREAM); y+=90
    cx("en nuestro local",F("hanken700.ttf",40),y-18,MUTE)
    d.rounded_rectangle([90,950,990,1090],radius=70,fill=PINK); cx("Reserva en nuestra página web",F("bricolage800.ttf",50),993,BG)
    cx("Link en la bio",F("caveat700.ttf",80),1135,PINK)
    cx("Ruta J-60 km 95, Licantén · @sabor_rural",F("hanken700.ttf",30),1252,MUTE)
    im.convert("RGB").save(OUT+"carrusel-08-reserva.jpg",quality=95)
def carrusel():
    collage()
    slide("carrusel-02-mario.jpg",2,"EL PERSONAJE",[[("Mario, ",C),("modelado a mano",K)]],None,fy=0.55)
    slide("carrusel-03-pirana.jpg",9,"EL DETALLE",[[("La Planta ",C),("Piraña",K)]],"Cada figura, hecha una a una",fy=0.62,fx=0.15)
    slide("carrusel-04-bloque.jpg",10,"EL MUNDO MARIO",[[("Bloque ",C),("?",K),(" y Bob-omb",C)]],None,fy=0.6,fx=0.75)
    slide("carrusel-05-nombre.jpg",14,"PERSONALIZADA",[[("Con el nombre de",C)],[("quien cumple",K)]],None,fy=0.45)
    slide("carrusel-06-completa.jpg",3,"VISTA COMPLETA",[[("Un mundo entero,",C)],[("en una torta",K)]],None,fy=0.6)
    slide("carrusel-07-lado.jpg",12,"CADA ÁNGULO",[[("Detalles que ",C),("se disfrutan",K)]],None,fy=0.55)
    info_slide()
# ======================= REELS 9:16 =======================
RW,RH=1080,1920
def rcard(name,pill,lines,sub,hook=False):
    im=frame_logo(RW,RH); shade(im,1180,740,RW); text_block(im,RW,1480 if pill else 1500,pill,lines,sub,92 if hook else 80); im.save(T+name+".png")
def rend():
    im=Image.new("RGBA",(RW,RH),BG+(255,)); im.alpha_composite(frame_logo(RW,RH)); d=ImageDraw.Draw(im)
    cx=lambda t,f,y,c: d.text((RW/2,y),t,font=f,fill=c,anchor="ma")
    cx("Tu torta,",F("caveat700.ttf",110),330,PINK); cx("a tu medida",F("bricolage800.ttf",120),450,CREAM)
    y=660
    for t in ("De 15 a 40 personas","28 sabores para elegir","Pagas en línea y la retiras gratis"): cx(t,F("bricolage800.ttf",58),y,CREAM); y+=96
    cx("en nuestro local",F("hanken700.ttf",44),y-18,MUTE)
    d.rounded_rectangle([90,1180,990,1330],radius=75,fill=PINK); cx("Reserva en nuestra página web",F("bricolage800.ttf",54),1228,BG)
    cx("Link en la bio",F("caveat700.ttf",86),1390,PINK); cx("Ruta J-60 km 95, Licantén · @sabor_rural",F("hanken700.ttf",32),1760,MUTE)
    im.save(T+"end.png")
def scene(name,n,dur,png,fx=0.5,zin=True,fy=0.5):
    im=photo(n); w,h=im.size; nw=int(h*9/16); x=int((w-nw)*fx); im=im.crop((x,0,x+nw,h)).resize((1620,2880),Image.LANCZOS); im.save(T+f"{name}.jpg",quality=95)
    N=int(dur*30); z=f"1.0+0.10*on/{N}" if zin else f"1.10-0.10*on/{N}"
    fc=(f"[0:v]zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih*{fy}-(ih/zoom*{fy})':d={N}:s={RW}x{RH}:fps=30,eq=contrast=1.04:saturation=1.08[v];[v][1:v]overlay=0:0,format=yuv420p[o]")
    subprocess.run(["ffmpeg","-v","error","-y","-loop","1","-i",T+f"{name}.jpg","-i",T+png+".png","-filter_complex",fc,"-map","[o]","-t",str(dur),"-an","-c:v","libx264","-preset","slow","-crf","17",T+name+".mp4"],check=True)
def music(total,bpm,seed,path):
    sr=44100; beat=60/bpm; Tm=total+0.3; n=int(sr*Tm); out=np.zeros(n); rng=np.random.default_rng(seed)
    def add(sig,st,g=1.0):
        i=int(st*sr); j=min(n,i+len(sig))
        if i<n: out[i:j]+=sig[:j-i]*g
    def pluck(f,d=0.5):
        x=np.arange(int(sr*d))/sr; return (np.sin(2*np.pi*f*x)+0.3*np.sin(4*np.pi*f*x)*np.exp(-x*8))*np.exp(-x*7)*np.minimum(1,x*400)
    def pad(f,d):
        x=np.arange(int(sr*d))/sr; w=sum(np.sin(2*np.pi*f*k*x+p) for k,p in ((1,0),(2,1.1),(3,2.2)))/3; return w*np.minimum(1,x/0.6)*np.minimum(1,(d-x)/0.8)
    Cn=lambda m:440*2**((m-69)/12); prog=[(48,[60,64,67]),(43,[59,62,67]),(45,[60,64,69]),(41,[60,65,69])]
    for bar in range(int(Tm/(beat*4))+1):
        root,ch=prog[bar%4]; st=bar*beat*4
        for m in ch: add(pad(Cn(m),beat*4.2),st,0.09)
        add(pad(Cn(root),beat*4.2),st,0.15)
        for k in range(8): add(pluck(Cn(ch[(k*2+bar)%3]+12)),st+k*beat/2,0.17 if k%2==0 else 0.10)
        for bi in range(4):
            x=np.arange(int(sr*0.3))/sr; f=55+70*np.exp(-x*32); add(np.sin(2*np.pi*np.cumsum(f)/sr)*np.exp(-x*11),st+bi*beat,0.24)
            x=np.arange(int(sr*0.05))/sr; nz=rng.standard_normal(len(x)); add((nz-np.convolve(nz,np.ones(8)/8,mode='same'))*np.exp(-x*70),st+bi*beat+beat/2,0.06)
    out=np.tanh(out*1.1); fi=int(sr*0.5); out[:fi]*=np.linspace(0,1,fi); fo=int(sr*1.6); out[-fo:]*=np.linspace(1,0,fo)
    pcm=(out/np.max(np.abs(out))*0.8*32767).astype('<i2')
    with wave.open(path,"wb") as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes(pcm.tobytes())
def assemble(names,durs,dest,bpm,seed):
    xf=0.25; cmd=["ffmpeg","-v","error","-y"]+sum([["-i",T+n+".mp4"] for n in names],[])
    fc="";prev="[0:v]";off=0
    for i in range(1,len(names)):
        off+=durs[i-1]-xf; fc+=f"{prev}[{i}:v]xfade=transition=fade:duration={xf}:offset={off:.2f}[x{i}];"; prev=f"[x{i}]"
    total=sum(durs)-xf*(len(names)-1)
    subprocess.run(cmd+["-filter_complex",fc.rstrip(";"),"-map",prev,"-c:v","libx264","-profile:v","high","-b:v","8M","-maxrate","10M","-bufsize","16M","-pix_fmt","yuv420p","-r","30","-an",T+dest+"-v.mp4"],check=True)
    music(total,bpm,seed,T+dest+".wav")
    subprocess.run(["ffmpeg","-v","error","-y","-i",T+dest+"-v.mp4","-i",T+dest+".wav","-map","0:v","-map","1:a","-c:v","copy","-c:a","aac","-ar","48000","-b:a","160k","-shortest","-movflags","+faststart",OUT+dest+".mp4"],check=True)
    print(dest,round(total,1),"s")
def reels():
    rend()
    # --- Reel A: showcase ---
    rcard("a0",None,[[("Torta ",C),("Super Mario",K)]],"Personalizada, hecha en Sabor Rural",hook=True)
    rcard("a1","EL PERSONAJE",[[("Mario, ",C),("modelado a mano",K)]],None)
    rcard("a2","EL DETALLE",[[("La Planta ",C),("Piraña",K)]],None)
    rcard("a3","EL MUNDO MARIO",[[("Bloque ",C),("?",K),(" y Bob-omb",C)]],None)
    rcard("a4","PERSONALIZADA",[[("Con el nombre de",C)],[("quien cumple",K)]],None)
    rcard("a5","CADA ÁNGULO",[[("Detalles que ",C),("se disfrutan",K)]],None)
    S=[("ra0",3,2.8,"a0",0.5,True,0.5),("ra1",6,2.3,"a1",0.5,True,0.5),("ra2",9,2.3,"a2",0.08,False,0.5),("ra3",10,2.3,"a3",0.5,True,0.5),
       ("ra4",14,2.6,"a4",0.5,True,0.5),("ra5",12,2.3,"a5",0.5,False,0.5)]
    for n,ph,d,png,fx,z,fy in S: scene(n,ph,d,png,fx,z,fy)
    subprocess.run(["ffmpeg","-v","error","-y","-loop","1","-t","3.6","-i",T+"end.png","-vf","fps=30,format=yuv420p","-c:v","libx264","-crf","17",T+"rend.mp4"],check=True)
    assemble([s[0] for s in S]+["rend"],[s[2] for s in S]+[3.6],"reel-mario-A-showcase",106,11)
    # --- Reel B: ¿cuántos detalles encuentras? ---
    rcard("b0",None,[[("¿Cuántos detalles de",C)],[("Mario ",K),("encuentras?",C)]],"Cuéntalos y comenta cuántos viste",hook=True)
    for k,(p,t) in enumerate([("1 de 6",[[("Mario, ",C),("el héroe",K)]]),("2 de 6",[[("La Planta ",C),("Piraña",K)]]),("3 de 6",[[("El ",C),("Bob-omb",K)]]),
                              ("4 de 6",[[("El bloque ",C),("?",K)]]),("5 de 6",[[("La Súper ",C),("Estrella",K)]]),("6 de 6",[[("Ladrillos y ",C),("monedas",K)]])],1): rcard(f"b{k}",p,t,None)
    rcard("b7",None,[[("¿Cuántos ",C),("contaste?",K)]],"Escríbelo en los comentarios",hook=True)
    S2=[("rb0",3,3.0,"b0",0.5,True,0.5),("rb1",2,2.1,"b1",0.5,True,0.5),("rb2",9,2.1,"b2",0.08,True,0.5),("rb3",10,2.1,"b3",0.5,True,0.5),
        ("rb4",10,2.1,"b4",1.0,False,0.5),("rb5",8,2.1,"b5",0.0,True,0.5),("rb6",13,2.1,"b6",0.0,False,0.5),("rb7",5,2.5,"b7",0.5,True,0.5)]
    for n,ph,d,png,fx,z,fy in S2: scene(n,ph,d,png,fx,z,fy)
    assemble([s[0] for s in S2]+["rend"],[s[2] for s in S2]+[3.6],"reel-mario-B-detalles",110,23)
if __name__=="__main__":
    what=sys.argv[1] if len(sys.argv)>1 else "all"
    if what in("all","carrusel"): carrusel()
    if what in("all","reels"): reels()
