# Navidad 2026 · destacada, carrusel 4:5 y reel 9:16 (limpio, logo blanco en zona segura)
import sys, subprocess, importlib.util
from PIL import Image, ImageDraw, ImageOps
spec=importlib.util.spec_from_file_location("mb","/home/user/saborrural/herramientas/mario2/build.py"); B=importlib.util.module_from_spec(spec); spec.loader.exec_module(B)
U="/root/.claude/uploads/3bdc22a0-44b6-5463-a581-9b7d84b08b80/"; OUT="/home/user/saborrural/media/navidad/"; T=B.T; F=B.F
G="/tmp/claude-0/-home-user/3bdc22a0-44b6-5463-a581-9b7d84b08b80/scratchpad/gem/white120.png"
PH={"rojo":"2ddca46d","rosas":"0d43dd2c","lazo":"2168d3b5","frambuesa":"f37eba40","nuez":"688b509b","lucuma":"f2f12815"}
CRE=(243,241,234); PINK=(245,154,172); GOLD=(232,199,120); BG=(12,13,15); MUT=(169,171,163)
def photo(k): return ImageOps.exif_transpose(Image.open(U+PH[k]+"-image.jpg").convert("RGB"))
def cover(img,size,fx=.5,fy=.5):
    w,h=img.size; ar=size[0]/size[1]
    if w/h>ar: nw=int(h*ar); x=int((w-nw)*fx); img=img.crop((x,0,x+nw,h))
    else: nh=int(w/ar); y=int((h-nh)*fy); img=img.crop((0,y,w,y+nh))
    return img.resize(size,Image.LANCZOS)
def frame_logo(W,H):
    im=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(im); d.rounded_rectangle([22,22,W-22,H-22],radius=40,outline=GOLD+(255,),width=3)
    lg=Image.open(B.AS+"logo.png").convert("RGBA"); L=int(W*0.115); lg=lg.resize((L,int(L*lg.height/lg.width))); im.alpha_composite(lg,(54,54)); return im
# ---------- destacada ----------
def destacada():
    im=Image.new("RGB",(1080,1920),BG); d=ImageDraw.Draw(im); cx,cy,r=540,960,400
    d.ellipse([cx-r,cy-r,cx+r,cy+r],outline=GOLD,width=14); d.ellipse([cx-r+36,cy-r+36,cx+r-36,cy+r-36],outline=(80,60,40),width=3)
    d.text((cx,cy-150),"reserva tu",font=F("caveat700.ttf",100),fill=PINK,anchor="mm"); d.text((cx,cy+30),"Navidad",font=F("bricolage800.ttf",170),fill=CRE,anchor="mm")
    lg=Image.open(B.AS+"logo.png").convert("RGBA").resize((120,119)); im.paste(lg,(cx-60,cy+190),lg); im.save(OUT+"destacada-navidad.png")
# ---------- carrusel 4:5 ----------
W,H=1080,1350
def topshade(im,h=520):
    g=Image.new("RGBA",(W,h),(0,0,0,0)); gd=ImageDraw.Draw(g)
    for i in range(h): gd.line([(0,i),(W,i)],fill=(8,8,10,int(215*min(1,(i/(h*0.55))**1.4))))
    im.alpha_composite(g.transpose(Image.FLIP_TOP_BOTTOM),(0,0))
def slide(name,k,pill,l1,l2,fx=.5,fy=.5,top=True):
    im=cover(photo(k),(W,H),fx,fy).convert("RGBA")
    if top: topshade(im); y0=215
    else: B.shade(im,H-520,520,W); y0=H-330
    d=ImageDraw.Draw(im); f=F("bricolage800.ttf",38); w=int(d.textlength(pill,font=f))+54
    d.rounded_rectangle([70,y0,70+w,y0+68],radius=34,fill=GOLD); d.text((70+27,y0+34),pill,font=f,fill=BG,anchor="lm")
    d.text((70,y0+92),l1,font=F("bricolage800.ttf",76),fill=CRE); d.text((70,y0+92+82),l2,font=F("bricolage800.ttf",76),fill=PINK)
    im.alpha_composite(frame_logo(W,H)); im.convert("RGB").save(OUT+name,quality=95)
def carrusel():
    im=cover(photo("rojo"),(W,H),.5,1.0).convert("RGBA"); topshade(im,640)
    d=ImageDraw.Draw(im); d.text((70,215),"Navidad 2026",font=F("caveat700.ttf",84),fill=GOLD)
    d.text((70,300),"Reserva tu",font=F("bricolage800.ttf",100),fill=CRE); d.text((70,400),"torta navideña",font=F("bricolage800.ttf",100),fill=PINK)
    d.text((W-70,H-120),"Desliza para ver ideas  →",font=F("hanken700.ttf",36),fill=CRE,anchor="ra"); im.alpha_composite(frame_logo(W,H)); im.convert("RGB").save(OUT+"carrusel-1-portada.jpg",quality=95)
    slide("carrusel-2-corazon.jpg","rojo","IDEA 1","Corazón rojo","para brindar",.5,1.0)
    slide("carrusel-3-rosas.jpg","rosas","IDEA 2","Chocolate y rosas","para regalar",.5,.5,top=False)
    slide("carrusel-4-lazo.jpg","lazo","IDEA 3","Chocolate con lazo","a tu mesa",.5,1.0)
    slide("carrusel-5-frambuesa.jpg","frambuesa","IDEA 4","Manjar y frambuesa","para compartir",.5,1.0)
    im=Image.new("RGBA",(W,H),BG+(255,)); im.alpha_composite(frame_logo(W,H)); d=ImageDraw.Draw(im); cx=lambda t,f,y,c: d.text((W/2,y),t,font=f,fill=c,anchor="ma")
    cx("Navidad 2026",F("caveat700.ttf",100),230,GOLD); cx("Reserva con tiempo",F("bricolage800.ttf",88),340,CRE)
    y=520
    for t in ("Tortas y kuchen por encargo","Hechos desde cero","Pagas en línea","Retiro gratis en el local"): cx(t,F("bricolage800.ttf",50),y,CRE); y+=84
    d.rounded_rectangle([90,950,990,1090],radius=70,fill=PINK); cx("Reserva en nuestra página web",F("bricolage800.ttf",50),993,BG)
    cx("Link en la bio",F("caveat700.ttf",80),1135,PINK); cx("Ruta J-60 km 95, Licantén · @sabor_rural",F("hanken700.ttf",30),1252,MUT); im.convert("RGB").save(OUT+"carrusel-6-reserva.jpg",quality=95)
# ---------- reel ----------
RW,RH=1080,1920; LOGO=T.replace("mario2","gem")+"white120.png"
def rtext(name,l1,l2=None,y=330,size=90):
    im=Image.new("RGBA",(RW,RH),(0,0,0,0)); d=ImageDraw.Draw(im)
    for t,col,yy in ((l1,CRE,y),(l2,PINK,y+int(size*1.1))):
        if t: d.text((RW/2+2,yy+3),t,font=F("bricolage800.ttf",size),fill=(0,0,0,150),anchor="ma"); d.text((RW/2,yy),t,font=F("bricolage800.ttf",size),fill=col+(255,),anchor="ma")
    im.save(T+name+".png")
def scene(name,k,dur,png,z0,z1,fx,fy,fx2=None,fy2=None):
    im=photo(k); w,h=im.size; nw=int(h*9/16); x=int((w-nw)*fx); im=im.crop((x,0,x+nw,h)).resize((1620,2880),Image.LANCZOS); im.save(T+name+".jpg",quality=95)
    N=int(dur*30); fx2=fx if fx2 is None else fx2; fy2=fy if fy2 is None else fy2
    z=f"{z0}+({z1}-{z0})*on/{N}"; cy=f"({fy}+({fy2}-{fy})*on/{N})"
    fc=f"[0:v]zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih*{cy}-(ih/zoom*{cy})':d={N}:s={RW}x{RH}:fps=30,eq=saturation=1.08[v];[v][1:v]overlay=0:0[a];[a][2:v]overlay=10:280,format=yuv420p[o]"
    subprocess.run(["ffmpeg","-v","error","-y","-loop","1","-i",T+name+".jpg","-i",T+png+".png","-i",LOGO,"-filter_complex",fc,"-map","[o]","-t",str(dur),"-an","-c:v","libx264","-preset","slow","-crf","17",T+name+".mp4"],check=True)
def reel():
    B.OUT=OUT
    rtext("n0","¿Ya pensaste en","tu torta de Navidad?",y=520,size=78)
    rtext("n1","Corazón rojo","para brindar",y=520,size=82); rtext("n2","Chocolate","con lazo",y=520,size=82); rtext("n3","Manjar","y frambuesa",y=520,size=82); rtext("n4","Caramelo","y nueces",y=520,size=82)
    rtext("n5","Reserva con tiempo","Link en la bio",y=1250,size=78)
    S=[("m0","rojo",2.6,"n0",1.0,1.06,.5,.95),("m1","rojo",2.2,"n1",1.06,1.12,.5,.95),("m2","lazo",2.2,"n2",1.0,1.10,.5,.9),
       ("m3","frambuesa",2.2,"n3",1.0,1.10,.5,.9),("m4","nuez",2.2,"n4",1.0,1.10,.5,.9)]
    for n,k,d,png,z0,z1,fx,fy in S: scene(n,k,d,png,z0,z1,fx,fy)
    # cierre limpio
    im=Image.new("RGBA",(RW,RH),BG+(255,)); d=ImageDraw.Draw(im); cx=lambda t,f,y,c: d.text((RW/2,y),t,font=f,fill=c,anchor="ma")
    cx("Navidad 2026",F("caveat700.ttf",110),520,GOLD); cx("Reserva tu torta",F("bricolage800.ttf",92),650,CRE); cx("en nuestra web",F("bricolage800.ttf",92),760,PINK)
    d.rounded_rectangle([190,960,890,1090],radius=65,outline=PINK+(255,),width=4); cx("Link en la bio",F("caveat700.ttf",82),976,PINK)
    cx("Ruta J-60 km 95, Licantén",F("hanken700.ttf",36),1700,MUT); lg=Image.open(LOGO).convert("RGBA"); im.alpha_composite(lg,(10,280)); im.save(T+"nend.png")
    subprocess.run(["ffmpeg","-v","error","-y","-loop","1","-t","3.4","-i",T+"nend.png","-vf","fps=30,format=yuv420p","-c:v","libx264","-crf","17",T+"mend.mp4"],check=True)
    B.assemble(["m0","m1","m2","m3","m4","mend"],[2.6,2.2,2.2,2.2,2.2,3.4],"reel-navidad",100,61)
if __name__=="__main__": destacada(); carrusel(); reel()
