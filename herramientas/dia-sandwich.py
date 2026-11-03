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
def ahorro(c,x,y):
    d=ImageDraw.Draw(c); t="Ahorras $800"; f=F("bricolage800.ttf",34); w=int(d.textlength(t,font=f))+44
    d.rounded_rectangle([x-w,y,x,y+60],radius=30,fill=PINK); d.text((x-22,y+30),t,font=f,fill=BG,anchor="rm")
def lorino_bloque(c,d,W,y,w,fn,msg_y,msgsz):
    h=int(lor.height*w/lor.width); c.alpha_composite(rounded(lor.resize((w,h),Image.LANCZOS),30),((W-w)//2,y))
    ahorro(c,(W+w)//2-22,y+22)
    d.text(((W-w)//2+30,y+16),"Ejemplo:",font=F("caveat700.ttf",58),fill=PINK)
    chip(d,(W-w)//2,y+h+14,w,"Lorino","$8.000","$7.200",fn,fi=26)
    f=F("hanken700.ttf",msgsz)
    ctr(d,"Todos los años celebramos el Día del Sándwich",f,msg_y,CREAM,W)
    ctr(d,"con este descuento, solo en el local.",f,msg_y+int(msgsz*1.45),CREAM,W)
    return y+h+14+128
def story():
    W,H=1080,1920; c,d=base(W,H)
    ctr(d,"Día del sándwich",F("caveat700.ttf",92),150,PINK,W)
    ctr(d,"10% de descuento",F("bricolage800.ttf",104),265,CREAM,W)
    ctr(d,"en todos nuestros sándwiches",F("hanken700.ttf",44),400,MUTE,W)
    e=lorino_bloque(c,d,W,500,900,48,1475,38)
    foot(d,W,1740); c.convert("RGB").save(O+"dia-sandwich-9x16.jpg",quality=95)
def post():
    W,H=1080,1350; c,d=base(W,H)
    ctr(d,"Día del sándwich",F("caveat700.ttf",78),58,PINK,W)
    ctr(d,"10% de descuento",F("bricolage800.ttf",90),150,CREAM,W)
    ctr(d,"en todos nuestros sándwiches",F("hanken700.ttf",36),262,MUTE,W)
    e=lorino_bloque(c,d,W,318,750,40,1150,27)
    foot(d,W,1226); c.convert("RGB").save(O+"dia-sandwich-post-4x5.jpg",quality=95)
story(); post()
