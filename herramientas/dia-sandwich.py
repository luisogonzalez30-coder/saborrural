from PIL import Image, ImageDraw, ImageFont
B="/home/user/saborrural/media/sandwich/fotos/"; O="/home/user/saborrural/media/dia-sandwich/"
SB="/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"; SN="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
CREAM=(250,243,232); GOLD=(222,190,120); BG=(22,16,13)
F=lambda p,s: ImageFont.truetype(p,s)
def ctr(d,t,f,y,col,W=1080):
    w=d.textlength(t,font=f); d.text(((W-w)/2,y),t,font=f,fill=col)
def tarjeta(d,x,y,w,nombre,antes,ahora):
    d.rounded_rectangle([x,y,x+w,y+120],radius=26,fill=(40,30,24,255))
    d.text((x+30,y+14),nombre,font=F(SB,44),fill=CREAM)
    d.text((x+30,y+70),"Incluye papas fritas caseras",font=F(SN,26),fill=GOLD)
    fa=F(SN,30); fn=F(SB,52)
    wn=d.textlength(ahora,font=fn); d.text((x+w-30-wn,y+12),ahora,font=fn,fill=GOLD)
    wa=d.textlength(antes,font=fa); xa=x+w-30-wa; d.text((xa,y+76),antes,font=fa,fill=(190,180,165))
    d.line([(xa,y+93),(xa+wa,y+93)],fill=(190,180,165),width=3)
def foto(canvas,fn,box,pos,size):
    im=Image.open(B+fn).convert("RGB").crop(box).resize(size,Image.LANCZOS); canvas.paste(im,pos)
def pieza(W,H,name,hdr,two_line,y1,pw,fh,gap,foot):
    c=Image.new("RGB",(W,H),BG); d=ImageDraw.Draw(c,"RGBA")
    ctr(d,"DÍA DEL SÁNDWICH",F(SN,44),hdr,GOLD,W)
    if two_line:
        ctr(d,"10% DE",F(SB,150),hdr+80,CREAM,W); ctr(d,"DESCUENTO",F(SB,120),hdr+235,GOLD,W); ty=hdr+385
    else:
        ctr(d,"10% DE DESCUENTO",F(SB,84),hdr+70,CREAM,W); ty=hdr+175
    ctr(d,"en compras presenciales",F(SN,40),ty,GOLD if not two_line else CREAM,W)
    ph=int(fh*pw/1080); x=(W-pw)//2; y=y1
    for fn,top,nom,a,n in (("lorino-post-4x5.jpg",390,"Lorino","$8.000","$7.200"),("barros-luco-post-4x5.jpg",540,"Clásico Barros Luco","$7.000","$6.300")):
        im=Image.open(B+fn).convert("RGB").crop((0,top,1080,top+fh)).resize((pw,ph),Image.LANCZOS); c.paste(im,(x,y))
        tarjeta(d,x,y+ph+8,pw,nom,a,n); y+=ph+8+120+gap
    ctr(d,"Válido solo comprando en el local",F(SN,32),foot,CREAM,W)
    ctr(d,"Ruta J-60 km 95, Licantén · @sabor_rural",F(SN,30),foot+55,GOLD,W)
    c.save(O+name,quality=95)
pieza(1080,1920,"dia-sandwich-9x16.jpg",90,True,540,1080,440,26,1760)
pieza(1080,1350,"dia-sandwich-post-4x5.jpg",40,False,275,820,440,22,1240)
