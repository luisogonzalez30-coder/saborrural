# Foto tarta de frutos rojos: logo negro de Sabor Rural estampado en el vaso (envolviendo la curva) + frambuesa menos esférica
import numpy as np
from PIL import Image, ImageFilter
SRC="/root/.claude/uploads/3bdc22a0-44b6-5463-a581-9b7d84b08b80/01a7a491-image.png"; OUT="/home/user/saborrural/media/fotos/"
LOGO="/home/user/saborrural/enlaces-assets/logo.png"
im=Image.open(SRC).convert("RGB"); A=np.asarray(im).astype(np.float32); H,W,_=A.shape
def bilinear(img,xs,ys):
    xs=np.clip(xs,0,img.shape[1]-1.001); ys=np.clip(ys,0,img.shape[0]-1.001)
    x0=np.floor(xs).astype(int); y0=np.floor(ys).astype(int); fx=(xs-x0)[...,None]; fy=(ys-y0)[...,None]
    return (img[y0,x0]*(1-fx)*(1-fy)+img[y0,x0+1]*fx*(1-fy)+img[y0+1,x0]*(1-fx)*fy+img[y0+1,x0+1]*fx*fy)
# ---------- 1) frambuesa menos redonda ----------
def frambuesa(A,cx=315,cy=807,r=62,seed=7):
    A=A.astype(np.float32)
    yy,xx=np.mgrid[0:H,0:W].astype(np.float32); dx=xx-cx; dy=yy-cy; rho=np.sqrt(dx**2+dy**2)
    w=np.clip(1.25-rho/r,0,1); w=np.minimum(1,w*2.2)**1.5   # 1 dentro, cae suave hacia fuera
    th=np.deg2rad(-14); c,s=np.cos(th),np.sin(th)
    u=c*dx+s*dy; v=-s*dx+c*dy          # coordenadas giradas
    # forma de cono: más ancha arriba, más angosta abajo; algo más alta que ancha
    taper=1+0.14*np.clip(v/r,-1,1); sx=1.03*taper; sy=0.93
    rng=np.random.default_rng(seed); n1=rng.normal(0,1,(H//40+3,W//40+3)).astype(np.float32); n2=rng.normal(0,1,(H//40+3,W//40+3)).astype(np.float32)
    big1=np.asarray(Image.fromarray(n1).resize((W,H),Image.BICUBIC)); big2=np.asarray(Image.fromarray(n2).resize((W,H),Image.BICUBIC))
    nu=big1*3.2; nv=big2*3.2           # ondulación del contorno (px)
    us=u/sx+nu*w; vs=v/sy+nv*w
    xs=cx+(c*us-s*vs); ys=cy+(s*us+c*vs)
    xs=xx*(1-w)+xs*w; ys=yy*(1-w)+ys*w
    return bilinear(A,xs,ys)
B=frambuesa(A)
B=frambuesa(B,cx=620,cy=688,r=56,seed=11)
# ---------- 2) logo negro en el vaso ----------
logo=Image.open(LOGO).convert("RGBA"); LW=logo.width; la=np.asarray(logo).astype(np.float32)[...,3]/255.0   # forma del logo (alfa)
la=np.asarray(Image.fromarray((la*255).astype(np.uint8)).resize((600,600),Image.LANCZOS)).astype(np.float32)/255.0
CX=337.0; Y0=450.0; D=168.0; DEPTH=9.0
def hw(y): return 172-(y-290)*0.17
yy,xx=np.mgrid[0:H,0:W].astype(np.float32)
hwy=hw(yy); dx=xx-CX; ratio=np.clip(dx/hwy,-0.999,0.999); phi=np.arcsin(ratio)
u=hwy*phi                                  # longitud de arco sobre el cilindro
v=(yy-Y0)-DEPTH*np.cos(phi)**2             # curvatura (sonrisa) por la vista desde arriba
lu=u/D*600+300; lv=v/D*600+300
inside=(np.abs(ratio)<0.995)&(lu>=0)&(lu<599)&(lv>=0)&(lv<599)
alpha=np.zeros((H,W),np.float32); alpha[inside]=bilinear(la[...,None],lu[inside],lv[inside])[...,0]
alpha=np.asarray(Image.fromarray((alpha*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.55))).astype(np.float32)/255.0
ink=np.array([30,22,20],np.float32)
# conserva la textura y el sombreado del cartón: la tinta se multiplica por la luminosidad local
lum=B.mean(axis=2,keepdims=True); lum_s=np.asarray(Image.fromarray(lum[...,0].astype(np.uint8)).filter(ImageFilter.GaussianBlur(25))).astype(np.float32)[...,None]
shade=np.clip(lum/ (lum_s+1e-3),0.85,1.15)
printed=(ink*shade)
a=np.clip(alpha*1.3,0,1)[...,None]*0.94
C=B*(1-a)+printed*a
Image.fromarray(np.clip(C,0,255).astype(np.uint8)).save(OUT+"tarta-frutos-rojos-vaso-logo.png")
# comparación
def crop(arr,box): return Image.fromarray(np.clip(arr,0,255).astype(np.uint8)).crop(box)
box=(100,230,700,940)
b0=crop(A,box); b1=crop(C,box); w=Image.new("RGB",(b0.width*2+20,b0.height),(255,255,255)); w.paste(b0,(0,0)); w.paste(b1,(b0.width+20,0)); w.save(OUT+"comparacion.png")
