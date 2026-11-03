# Quita la tabla de madera de la foto del Lorino sin tocar el sándwich: pinta la mesa oscura bajo el borde inferior del pan.
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
src="/home/user/saborrural/media/sandwich/originales/lorino.jpg"; out="/home/user/saborrural/media/sandwich/originales/lorino-sin-tabla.jpg"
im=Image.open(src).convert("RGB"); W,H=im.size
# borde inferior del pan (x,y) de izquierda a derecha, ajustado a la foto original
edge=[(0,770),(35,780),(55,792),(100,830),(150,855),(250,872),(430,880),(600,863),(780,841),(950,817),(1100,795),(1230,783),(1252,781),(1280,752),(1290,746)]
m=Image.new("L",(W,H),0); d=ImageDraw.Draw(m); d.polygon(edge+[(W,H),(0,H)],fill=255)
m=m.filter(ImageFilter.GaussianBlur(3.5))
# mesa oscura con degradado y grano suave
rng=np.random.default_rng(3); yy=np.linspace(0,1,H)[:,None]
base=np.stack([30-14*yy,19-9*yy,13-6*yy],axis=-1)*np.ones((1,W,1))
base+=rng.normal(0,2.2,(H,W,1)); table=Image.fromarray(np.clip(base,0,255).astype("uint8"))
# sombra de contacto bajo el pan
sh=Image.new("L",(W,H),0); ds=ImageDraw.Draw(sh); ds.polygon([(x,y+10) for x,y in edge]+[(W,H),(0,H)],fill=150)
sh=sh.filter(ImageFilter.GaussianBlur(22)); 
res=Image.composite(table,im,m)
dark=Image.new("RGB",(W,H),(6,4,3)); res=Image.composite(dark,res,Image.eval(Image.composite(sh,Image.new("L",(W,H),0),m.point(lambda v:255 if v>0 else 0)),lambda v:int(v*0.55)))
res.save(out,quality=95); print("ok")
