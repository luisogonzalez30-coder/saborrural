# Día del Sándwich · estilo de marca: Bricolage 800 + Hanken 700 + Caveat, fondo #0C0D0F, crema #F3F1EA, rosa #F59AAC
from PIL import Image, ImageDraw, ImageFont, ImageChops
U="/root/.claude/uploads/3bdc22a0-44b6-5463-a581-9b7d84b08b80/"; A="/home/user/saborrural/enlaces-assets/"; O="/home/user/saborrural/media/dia-sandwich/"
F=lambda n,s: ImageFont.truetype(A+n,s)
BG=(12,13,15); CREAM=(243,241,234); PINK=(245,154,172); MUTE=(169,171,163); CARD=(26,28,33)
def rounded(im,r):
    m=Image.new("L",im.size,0); ImageDraw.Draw(m).rounded_rectangle([0,0,im.width-1,im.height-1],radius=r,fill=255); im=im.convert("RGBA"); im.putalpha(m); return im
def trim_black(im,th=14):
    g=im.convert("L").point(lambda v:255 if v>th else 0); return im.crop(g.getbbox())
lor=Image.open(U+"e891bb34-image.jpg").convert("RGB")
bl=trim_black(Image.open(U+"e6385504-image.jpg").convert("RGB"))
def ctr(d,t,f,y,col,W): d.text((W/2,y),t,font=f,fill=col,anchor="ma")
def chip(d,x,y,w,nom,antes,ahora,fn,fi=25):
    d.rounded_rectangle([x,y,x+w,y+128],radius=24,fill=CARD)
    d.text((x+26,y+18),nom,font=F("bricolage800.ttf",fn),fill=CREAM)
    d.text((x+26,y+78),"Incluye papas fritas caseras",font=F("hanken700.ttf",fi),fill=MUTE)
    fp=F("bricolage800.ttf",50); d.text((x+w-26,y+10),ahora,font=fp,fill=PINK,anchor="ra")
    fa=F("hanken700.ttf",26); wa=d.textlength(antes,font=fa); xa=x+w-26-wa
    d.text((xa,y+80),antes,font=fa,fill=MUTE); d.line([(xa,y+96),(xa+wa,y+96)],fill=MUTE,width=3)
def base(W,H):
    c=Image.new("RGBA",(W,H),BG+(255,)); d=ImageDraw.Draw(c)
    d.rounded_rectangle([22,22,W-22,H-22],radius=40,outline=PINK+(255,),width=3)
    lg=Image.open(A+"logo.png").convert("RGBA"); L=int(W*0.115); lg=lg.resize((L,int(L*lg.height/lg.width))); c.alpha_composite(lg,(54,54)); return c,d
def foot(d,W,y):
    ctr(d,"Válido solo comprando en el local",F("hanken700.ttf",32),y,CREAM,W)
    ctr(d,"Ruta J-60 km 95, Licantén · @sabor_rural",F("hanken700.ttf",30),y+48,PINK,W)
def story():
    W,H=1080,1920; c,d=base(W,H)
    ctr(d,"Día del sándwich",F("caveat700.ttf",92),150,PINK,W)
    ctr(d,"10% de descuento",F("bricolage800.ttf",104),265,CREAM,W)
    ctr(d,"en compras presenciales",F("hanken700.ttf",44),400,MUTE,W)
    y=470
    for im,w,nom,a,n in ((lor,620,"Lorino","$8.000","$7.200"),(bl,620,"Clásico Barros Luco","$7.000","$6.300")):
        h=int(im.height*w/im.width); ph=rounded(im.resize((w,h),Image.LANCZOS),28); c.alpha_composite(ph,((W-w)//2,y))
        chip(d,(W-w)//2,y+h+14,w,nom,a,n,36); y+=h+14+128+30
    foot(d,W,y+4); c.convert("RGB").save(O+"dia-sandwich-9x16.jpg",quality=95); print("story y",y)
def post():
    W,H=1080,1350; c,d=base(W,H)
    ctr(d,"Día del sándwich",F("caveat700.ttf",84),70,PINK,W)
    ctr(d,"10% de descuento",F("bricolage800.ttf",96),170,CREAM,W)
    ctr(d,"en compras presenciales",F("hanken700.ttf",40),290,MUTE,W)
    w=480; gx=(W-2*w-30)//2; y0=470
    for i,(im,nom,a,n) in enumerate(((lor,"Lorino","$8.000","$7.200"),(bl,"Barros Luco","$7.000","$6.300"))):
        h=int(im.height*w/im.width); x=gx+i*(w+30)
        c.alpha_composite(rounded(im.resize((w,h),Image.LANCZOS),26),(x,y0+(430-h)//2 if h<430 else y0))
        chip(d,x,y0+456,w,nom if i==0 else "Barros Luco",a,n,38,fi=22)
    ctr(d,"Clásico Barros Luco y Lorino",F("hanken700.ttf",30),y0+450+128+30,MUTE,W) if False else None
    foot(d,W,1190); c.convert("RGB").save(O+"dia-sandwich-post-4x5.jpg",quality=95)
story(); post()
