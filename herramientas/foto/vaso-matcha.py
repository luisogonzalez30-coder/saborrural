# Vaso matcha: borra el texto original y estampa el logo (blanco) envuelto en el cilindro del vaso
import numpy as np, sys
from PIL import Image, ImageFilter
SRC="/root/.claude/uploads/3bdc22a0-44b6-5463-a581-9b7d84b08b80/5c233134-image.jpg"; OUT="/home/user/saborrural/media/fotos/"
im=Image.open(SRC).convert("RGB"); A=np.asarray(im).astype(np.float32); H,W,_=A.shape
bl=lambda ch,s: np.asarray(Image.fromarray(np.clip(ch,0,255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(s))).astype(np.float32)
# 1) borrar texto
x0,y0,x1,y1=495,822,760,970
m=np.zeros((H,W),np.float32); sub=A[y0:y1,x0:x1]
m[y0:y1,x0:x1]=((sub[...,0]>150)&(sub[...,1]>150)&(sub[...,2]>120)&(sub[...,0]-sub[...,2]<90)).astype(np.float32)
mk=np.asarray(Image.fromarray((m*255).astype(np.uint8)).filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(1.2))).astype(np.float32)/255
good=1-(mk>0.03).astype(np.float32)
def nf(S):
    n=np.stack([bl(A[...,c]*good,S) for c in range(3)],-1); d=bl(good*255,S)[...,None]/255; return n/np.maximum(d,1e-3), d
fill,_=nf(70)
for S in (35,16,8):
    f,d=nf(S); w=np.clip(d/0.25,0,1); fill=fill*(1-w)+f*w
fill=fill+np.random.default_rng(3).normal(0,3,(H,W))[...,None]
a=np.clip(mk*1.8,0,1)[...,None]; B=A*(1-a)+fill*a
# 1b) sabor cereza: el verde pasa a rojo cereza (se excluye el mango, abajo a la izquierda)
import colorsys
hsv=np.asarray(Image.fromarray(np.clip(B,0,255).astype(np.uint8)).convert("HSV")).astype(np.float32)
h=hsv[...,0]/255*360; sat=hsv[...,1]/255; val=hsv[...,2]/255
wg0=np.clip((h-56)/8,0,1)*np.clip((195-h)/14,0,1)*np.clip((sat-0.10)/0.15,0,1)
wg1=np.clip((h-39)/5,0,1)*np.clip((200-h)/14,0,1)*np.clip((sat-0.05)/0.1,0,1)

yy0,xx0=np.mgrid[0:H,0:W].astype(np.float32)
Lc=np.where(yy0<590,380,380+(yy0-590)*0.135); Rc=np.where(yy0<590,857,857-(yy0-590)*0.104)
cup=((xx0>Lc-6)&(xx0<Rc+6)&(yy0>480)&(yy0<1345)).astype(np.float32)
excl=((xx0<462)&(yy0>815)).astype(np.float32)*(1-cup)
excl=np.asarray(Image.fromarray((excl*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(2))).astype(np.float32)/255
cupb=np.asarray(Image.fromarray((cup*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(2))).astype(np.float32)/255
wg=(wg0*(1-cupb)+wg1*cupb)*(1-excl)
nh=356/360*255   # tono cereza ~352 grados
hsv2=hsv.copy(); hsv2[...,0]=nh
hsv2[...,1]=np.clip(sat*1.25+0.18,0,0.95)*255
hsv2[...,2]=np.clip(val*1.12+0.06,0,1)*255
Cf=np.asarray(Image.fromarray(hsv2.astype(np.uint8),"HSV").convert("RGB")).astype(np.float32)
wgs=np.asarray(Image.fromarray((np.clip(wg,0,1)*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.8))).astype(np.float32)[...,None]/255
B=B*(1-wgs)+Cf*wgs
# 2) logo envuelto
LOGO="/home/user/saborrural/enlaces-assets/logo.png"
lg=Image.open(LOGO).convert("RGBA"); la=np.asarray(lg.getchannel("A")).astype(np.float32)/255
S=700; la=np.asarray(Image.fromarray((la*255).astype(np.uint8)).resize((S,S),Image.LANCZOS)).astype(np.float32)/255
CX=float(sys.argv[1]) if len(sys.argv)>1 else 623.0; CY=float(sys.argv[2]) if len(sys.argv)>2 else 800.0; D=float(sys.argv[3]) if len(sys.argv)>3 else 232.0
def hw(y): return 204-(y-880)*0.105          # semiancho del vaso (se angosta hacia abajo)
yy,xx=np.mgrid[0:H,0:W].astype(np.float32)
hwy=hw(yy); dx=xx-CX; ratio=np.clip(dx/hwy,-0.999,0.999); phi=np.arcsin(ratio)
u=hwy*phi; v=(yy-CY)-6*np.cos(phi)**2*0     # curvatura vertical leve: ninguna (vista frontal)
lu=u/D*S+S/2; lv=v/D*S+S/2
ins=(np.abs(ratio)<0.995)&(lu>=0)&(lu<S-1)&(lv>=0)&(lv<S-1)
xs=np.clip(lu,0,S-1.001); ys=np.clip(lv,0,S-1.001); x0_=np.floor(xs).astype(int); y0_=np.floor(ys).astype(int); fx=xs-x0_; fy=ys-y0_
al=(la[y0_,x0_]*(1-fx)*(1-fy)+la[y0_,x0_+1]*fx*(1-fy)+la[y0_+1,x0_]*(1-fx)*fy+la[y0_+1,x0_+1]*fx*fy)*ins
al=np.asarray(Image.fromarray((al*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.7))).astype(np.float32)/255
# sombreado del vaso: la tinta toma la luz local (brillo a la derecha, sombra a la izquierda)
lum=B.mean(2); ls=bl(lum,22); ref=ls[int(CY)-40:int(CY)+40,int(CX)-20:int(CX)+20].mean()
shade=np.clip(0.86+0.55*(ls-ref)/255+0.12*(ratio),0.78,1.06)[...,None]
ink=np.array([244,242,235],np.float32)*shade
alpha=(al*0.93)[...,None]
C=B*(1-alpha)+ink*alpha
# textura de impresión: deja pasar un poco de grano/arrugas del vaso
tex=(lum-ls)/255*0.8; C=C+(tex*alpha[...,0]*60)[...,None]
out=Image.fromarray(np.clip(C,0,255).astype(np.uint8))
# 3) quitar ícono de volumen de la captura
cx,cy,r=1160,1525,48; box=(cx-r-8,cy-r-8,cx+r+8,cy+r+8); w=box[2]-box[0]
from PIL import ImageDraw
src=out.crop((box[0]-6,box[1]-100,box[2]-6,box[3]-100)); mm=Image.new("L",(w,w),0); ImageDraw.Draw(mm).ellipse([8,8,w-8,w-8],fill=255); mm=mm.filter(ImageFilter.GaussianBlur(5)); out.paste(src,(box[0],box[1]),mm)
out.save(OUT+"vaso-cereza-logo.jpg",quality=95)
out.crop((380,560,880,1360)).save("/tmp/cupv2.png")
