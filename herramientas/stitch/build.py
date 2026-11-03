# Reel "Así se hace una torta Stitch" · estilo de marca (Bricolage 800, Hanken 700, Caveat; #0C0D0F, #F3F1EA, #F59AAC)
import subprocess, numpy as np, wave
from PIL import Image, ImageDraw, ImageFont
U="/root/.claude/uploads/3bdc22a0-44b6-5463-a581-9b7d84b08b80/"
V={k:U+v+".mp4" for k,v in dict(A="d359b5a0-VID-20261103-WA0004",B="8f8e727e-VID-20261103-WA0007",C="d480a931-VID-20261103-WA0008",D="bab798be-VID-20261103-WA0009",E="29faae71-VID-20261103-WA0010").items()}
AS="/home/user/saborrural/enlaces-assets/"; OUT="/home/user/saborrural/media/stitch/"; T="/tmp/claude-0/-home-user/3bdc22a0-44b6-5463-a581-9b7d84b08b80/scratchpad/v5/"
F=lambda n,s: ImageFont.truetype(AS+n,s)
BG=(12,13,15); CREAM=(243,241,234); PINK=(245,154,172); MUTE=(169,171,163)
W,H=1080,1920
def frame_logo():
    im=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(im)
    d.rounded_rectangle([22,22,W-22,H-22],radius=40,outline=PINK+(255,),width=3)
    lg=Image.open(AS+"logo.png").convert("RGBA"); L=int(W*0.115); lg=lg.resize((L,int(L*lg.height/lg.width))); im.alpha_composite(lg,(54,54)); return im
def shade(im,y0,h=700):
    g=Image.new("RGBA",(W,h),(0,0,0,0)); gd=ImageDraw.Draw(g)
    for i in range(h): gd.line([(0,i),(W,i)],fill=(8,8,10,int(215*min(1,(i/(h*0.55))**1.4))))
    im.alpha_composite(g,(0,y0))
def card(name,step,title,sub,hook=False):
    im=frame_logo(); d=ImageDraw.Draw(im); shade(im,1150,770); d=ImageDraw.Draw(im)
    y=1470
    if step:
        f=F("bricolage800.ttf",40); w=int(d.textlength(step,font=f))+56
        d.rounded_rectangle([70,y,70+w,y+70],radius=35,fill=PINK); d.text((70+28,y+35),step,font=f,fill=BG,anchor="lm"); y+=100
    for t,col in title:
        f=F("bricolage800.ttf",96 if hook else 84); d.text((70,y),t,font=f,fill=col); y+=int(f.size*1.08)
    if sub: d.text((70,y+14),sub,font=F("hanken700.ttf",38),fill=MUTE if not hook else CREAM)
    im.save(T+name+".png")
card("h",None,[("¿Cómo se hace una",CREAM),("torta de ",CREAM)],None,hook=True)
# hook: "torta de Stitch?" con Stitch en rosa
im=Image.open(T+"h.png"); d=ImageDraw.Draw(im); f=F("bricolage800.ttf",96); x=70+int(d.textlength("torta de ",font=f)); y=1470+int(96*1.08)
d.text((x,y),"Stitch?",font=f,fill=PINK); d.text((70,y+int(96*1.08)+14),"Mira el proceso, paso a paso",font=F("hanken700.ttf",40),fill=CREAM); im.save(T+"h.png")
card("p1","PASO 1",[("Relleno y cobertura",CREAM)],"Hecha desde cero, sin premezclas")
card("p2","PASO 2",[("Detalles a mano",CREAM)],"Pétalos y corazones, uno a uno")
card("p3","PASO 3",[("Flores y topper",CREAM)],"Un diseño único para cada cliente")
card("p4","PASO 4",[("¡Lista!",PINK)],"Torta Stitch personalizada")
# tarjeta final
im=Image.new("RGBA",(W,H),BG+(255,)); im.alpha_composite(frame_logo()); d=ImageDraw.Draw(im)
cx=lambda t,f,y,c: d.text((W/2,y),t,font=f,fill=c,anchor="ma")
cx("Tu torta,",F("caveat700.ttf",110),330,PINK); cx("a tu medida",F("bricolage800.ttf",120),450,CREAM)
y=660
for t in ("De 15 a 40 personas","28 sabores para elegir","Pagas en línea y la retiras gratis","en nuestro local"):
    if t=="en nuestro local": cx(t,F("hanken700.ttf",44),y-18,MUTE); y+=70; continue
    cx(t,F("bricolage800.ttf",58),y,CREAM); y+=96
d.rounded_rectangle([90,1180,990,1330],radius=75,fill=PINK); cx("Reserva en nuestra página web",F("bricolage800.ttf",54),1228,BG)
cx("Link en la bio",F("caveat700.ttf",86),1390,PINK)
cx("Ruta J-60 km 95, Licantén · @sabor_rural",F("hanken700.ttf",32),1760,MUTE)
im.save(T+"end.png")
# ---------- segmentos ----------
def pl(pts,idx,off):
    # interpolación lineal por tramos en función de t (+off = tiempo en el clip original)
    e=str(pts[-1][idx])
    for (t0,*a),(t1,*b) in reversed(list(zip(pts[:-1],pts[1:]))):
        e=f"if(lt(t+{off},{t1}),{a[idx-1]}+({b[idx-1]}-{a[idx-1]})*(t+{off}-{t0})/({t1}-{t0}),{e})"
    return e
BLUR=[(3.2,576,60),(3.6,560,125),(4.0,560,290),(4.4,555,378),(4.8,560,450),(5.2,548,493),(5.6,540,515),(6.0,497,522),(6.4,497,522)]
def xy(off):
    def comp(i):
        e=str(BLUR[-1][i])
        for p0,p1 in reversed(list(zip(BLUR[:-1],BLUR[1:]))):
            e=f"if(lt(t+{off},{p1[0]}),{p0[i]}+({p1[i]}-{p0[i]})*(t+{off}-{p0[0]})/({p1[0]}-{p0[0]}),{e})"
        return e
    cxe,cye=comp(1),comp(2)
    return f"max(0,min(340,({cxe})-190))", f"max(0,min(1110,({cye})-85))"
def seg(name,key,ss,d,speed,png,blur=False,hold=0):
    vf=f"setpts=PTS/{speed},fps=30,"+(f"tpad=stop_mode=clone:stop_duration={hold}," if hold else "")
    if blur:
        X,Y=xy(ss)
        vf="[0:v]split[a][b];[b]boxblur=28:4,crop=w=380:h=170:x='"+X+"':y='"+Y+"'[bl];[a][bl]overlay=x='"+X+"':y='"+Y+"',setpts=PTS/"+str(speed)+",fps=30,"
        pre=""
    else:
        vf="[0:v]"+vf
    fc=vf+f"scale={W}:{H}:flags=lanczos,eq=contrast=1.05:saturation=1.1[v];[v][1:v]overlay=0:0,format=yuv420p[o]"
    subprocess.run(["ffmpeg","-v","error","-y","-ss",str(ss),"-t",str(d),"-i",V[key],"-i",T+png+".png","-filter_complex",fc,"-map","[o]","-an","-c:v","libx264","-preset","slow","-crf","16",T+name+".mp4"],check=True)
segs=[("s0","A",3.4,2.9,1,"h",False),("s1","D",0,20,4,"p1",False),("s2","E",0,9.7,2.2,"p2",False),
      ("s3a","C",0,9.7,2.2,"p3",False),("s3b","B",0,7.7,2.2,"p3",False),("s4","A",0,6.4,1,"p4",False,1.6)]
durs=[]
for n,k,ss,d,sp,png,b,*h in segs: seg(n,k,ss,d,sp,png,b,*(h or [0])); durs.append(d/sp+(h[0] if h else 0))
# tarjeta final: foto de la torta terminada al fondo no; fondo sólido de marca (estático) 4.2 s
subprocess.run(["ffmpeg","-v","error","-y","-loop","1","-t","4.2","-i",T+"end.png","-vf","fps=30,format=yuv420p","-c:v","libx264","-crf","16",T+"s5.mp4"],check=True); durs.append(4.2)
names=["s0","s1","s2","s3a","s3b","s4","s5"]; xf=0.25
cmd=["ffmpeg","-v","error","-y"]+sum([["-i",T+n+".mp4"] for n in names],[])
fc="";prev="[0:v]";off=0
for i in range(1,len(names)):
    off+=durs[i-1]-xf; fc+=f"{prev}[{i}:v]xfade=transition=fade:duration={xf}:offset={off:.2f}[x{i}];"; prev=f"[x{i}]"
total=sum(durs)-xf*(len(names)-1)
cmd+=["-filter_complex",fc.rstrip(";"),"-map",prev,"-c:v","libx264","-profile:v","high","-b:v","8M","-maxrate","10M","-bufsize","16M","-pix_fmt","yuv420p","-r","30","-an",T+"video.mp4"]
subprocess.run(cmd,check=True); print("total",total)
# ---------- música original (más enérgica que la del video de encargos) ----------
sr=44100; bpm=106; beat=60/bpm; Tm=total+0.3; n=int(sr*Tm); out=np.zeros(n); rng=np.random.default_rng(5)
def add(sig,st,g=1.0):
    i=int(st*sr); j=min(n,i+len(sig))
    if i<n: out[i:j]+=sig[:j-i]*g
def pluck(f,d=0.5):
    x=np.arange(int(sr*d))/sr; return (np.sin(2*np.pi*f*x)+0.3*np.sin(4*np.pi*f*x)*np.exp(-x*8))*np.exp(-x*7)*np.minimum(1,x*400)
def pad(f,d):
    x=np.arange(int(sr*d))/sr; w=sum(np.sin(2*np.pi*f*k*x+p) for k,p in ((1,0),(2,1.1),(3,2.2)))/3; return w*np.minimum(1,x/0.6)*np.minimum(1,(d-x)/0.8)
C=lambda m:440*2**((m-69)/12); prog=[(48,[60,64,67]),(45,[60,64,69]),(41,[60,65,69]),(43,[59,62,67])]
for bar in range(int(Tm/(beat*4))+1):
    root,ch=prog[bar%4]; st=bar*beat*4
    for m in ch: add(pad(C(m),beat*4.2),st,0.09)
    add(pad(C(root),beat*4.2),st,0.15)
    for k in range(8): add(pluck(C(ch[(k+bar)%3]+12)),st+k*beat/2,0.17 if k%2==0 else 0.10)
    for bi in range(4):
        x=np.arange(int(sr*0.3))/sr; f=55+70*np.exp(-x*32); add(np.sin(2*np.pi*np.cumsum(f)/sr)*np.exp(-x*11),st+bi*beat,0.24)
        x=np.arange(int(sr*0.05))/sr; nz=rng.standard_normal(len(x)); add((nz-np.convolve(nz,np.ones(8)/8,mode='same'))*np.exp(-x*70),st+bi*beat+beat/2,0.06)
out=np.tanh(out*1.1); fi=int(sr*0.6); out[:fi]*=np.linspace(0,1,fi); fo=int(sr*1.6); out[-fo:]*=np.linspace(1,0,fo)
pcm=(out/np.max(np.abs(out))*0.8*32767).astype('<i2')
with wave.open(T+"musica.wav","wb") as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes(pcm.tobytes())
def mux(audio,dest):
    subprocess.run(["ffmpeg","-v","error","-y","-i",T+"video.mp4"]+(["-i",audio,"-map","0:v","-map","1:a","-c:v","copy","-c:a","aac","-ar","48000","-b:a","160k","-shortest"] if audio else ["-c:v","copy","-an"])+["-movflags","+faststart",dest],check=True)
mux(T+"musica.wav",OUT+"reel-stitch-con-musica.mp4"); mux(None,OUT+"reel-stitch-sin-audio.mp4")
