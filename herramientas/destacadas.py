# Portadas de historias destacadas · estilo de marca (fondo #0C0D0F, rosa #F59AAC, Bricolage + Caveat)
from PIL import Image, ImageDraw, ImageFont
A="/home/user/saborrural/enlaces-assets/"; O="/home/user/saborrural/media/perfil/"
F=lambda n,s: ImageFont.truetype(A+n,s); BG=(12,13,15); PINK=(245,154,172); CREAM=(243,241,234)
items=[("Tortas","encarga tu"),("Carta","mira la"),("Sándwiches","con papas"),("Tartas","hechas en casa"),("Eventos","celebra con"),("Café","origen Nicaragua")]
for name,top in items:
    im=Image.new("RGB",(1080,1920),BG); d=ImageDraw.Draw(im)
    cx,cy,r=540,960,400
    d.ellipse([cx-r,cy-r,cx+r,cy+r],outline=PINK,width=14)
    d.ellipse([cx-r+36,cy-r+36,cx+r-36,cy+r-36],outline=(60,40,46),width=3)
    d.text((cx,cy-150),top,font=F("caveat700.ttf",110),fill=PINK,anchor="mm")
    fs=170
    while d.textlength(name,font=F("bricolage800.ttf",fs))>600: fs-=8
    d.text((cx,cy+30),name,font=F("bricolage800.ttf",fs),fill=CREAM,anchor="mm")
    lg=Image.open(A+"logo.png").convert("RGBA").resize((120,119)); im.paste(lg,(cx-60,cy+190),lg)
    im.save(O+f"destacada-{name.lower().replace('é','e').replace('á','a')}.png")
# hoja de contactos circular (vista previa tal como se verá en el perfil)
sheet=Image.new("RGB",(6*260,300),(20,20,22))
for i,(name,_) in enumerate(items):
    im=Image.open(O+f"destacada-{name.lower().replace('é','e').replace('á','a')}.png").crop((140,560,940,1360)).resize((220,220))
    m=Image.new("L",(220,220),0); ImageDraw.Draw(m).ellipse([0,0,219,219],fill=255); sheet.paste(im,(i*260+20,20),m)
    ImageDraw.Draw(sheet).text((i*260+130,268),name,font=F("hanken700.ttf",26),fill=CREAM,anchor="mm")
sheet.save(O+"destacadas-vista-previa.jpg")
