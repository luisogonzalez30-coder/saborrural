import subprocess, sys, os
from PIL import Image, ImageDraw, ImageFont
U="/root/.claude/uploads/3bdc22a0-44b6-5463-a581-9b7d84b08b80/"
A=U+"5a4971a1-VID-20261103-WA0000.mp4"; B=U+"6ca9ba3a-VID-20261103-WA0001.mp4"
OUT="/home/user/saborrural/media/boda/"; T="/tmp/claude-0/-home-user/3bdc22a0-44b6-5463-a581-9b7d84b08b80/scratchpad/boda/"
SB="/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"; SN="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
CREAM=(250,243,232); GOLD=(222,190,120)
def F(p,s): return ImageFont.truetype(p,s)
def card(name, lines, y, shade=True):
    im=Image.new("RGBA",(1080,1920),(0,0,0,0)); d=ImageDraw.Draw(im)
    if shade:
        for i in range(520):
            a=int(150*(1-i/520)**1.6); d.line([(0,y-60+i-100),(1080,y-60+i-100)],fill=(0,0,0,a)) if False else None
        g=Image.new("RGBA",(1080,640),(0,0,0,0)); gd=ImageDraw.Draw(g)
        for i in range(640):
            gd.line([(0,i),(1080,i)],fill=(10,8,8,int(190*min((i/320)**1.5,1)*(1-max(0,(i-480))/160))))
        im.alpha_composite(g,(0,y-200))
    cy=y
    for t,fp,sz,col in lines:
        f=F(fp,sz); w=d.textlength(t,font=f)
        d.text(((1080-w)/2+3,cy+3),t,font=f,fill=(0,0,0,150)); d.text(((1080-w)/2,cy),t,font=f,fill=col+(255,))
        cy+=int(sz*1.25)
    im.save(T+name+".png")
card("c1",[("TORTA DE MATRIMONIO",SN,44,GOLD),("para 45",SB,120,CREAM),("personas",SB,120,CREAM)],1180)
card("c2",[("Elaborada en",SB,70,CREAM),("Sabor Rural",SB,96,CREAM),("Licantén · Costa Maule",SN,40,GOLD)],1250)
card("c3",[("Reserva directo en",SB,76,CREAM),("nuestra página web",SB,76,CREAM),("link en la bio",SN,44,GOLD)],1250)
# end card
im=Image.new("RGBA",(1080,1920),(24,18,16,235)); d=ImageDraw.Draw(im)
def C(t,fp,sz,y,col):
    f=F(fp,sz); w=d.textlength(t,font=f); d.text(((1080-w)/2,y),t,font=f,fill=col)
C("Sabor Rural",SB,120,560,CREAM); C("CAFETERÍA · PASTELERÍA",SN,38,720,GOLD)
d.line([(340,800),(740,800)],fill=GOLD,width=3)
C("Reserva tu torta",SB,84,880,CREAM); C("en nuestra página web",SB,70,990,CREAM)
d.rounded_rectangle([140,1160,940,1290],radius=65,fill=(222,190,120,255)); C("LINK EN LA BIO",SN,58,1195,(30,22,18,255))
C("@sabor_rural",SN,46,1380,GOLD); C("Ruta J-60 km 95, frente a Lora · Licantén",SN,32,1460,(200,190,175,255))
im.save(T+"end.png")
def seg(src,ss,dur,png,idx):
    # lento zoom + leve gradación cálida
    z=f"zoompan=z='1.0+0.06*on/{int(dur*30)}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=30"
    cmd=["ffmpeg","-v","error","-y","-ss",str(ss),"-t",str(dur),"-i",src,"-i",T+png+".png","-filter_complex",
      f"[0:v]scale=1080:1920:flags=lanczos,fps=30,{z},eq=contrast=1.06:saturation=1.1:brightness=0.01[v];[v][1:v]overlay=0:0,format=yuv420p[o]","-map","[o]","-an","-c:v","libx264","-preset","slow","-crf","16",T+f"s{idx}.mp4"]
    subprocess.run(cmd,check=True)
seg(A,0.8,3.6,"c1",1); seg(B,0.4,6.4,"c2",2); seg(A,4.0,3.6,"c3",3); seg(B,6.0,3.2,"end",4)
# xfade chain
d=0.35; durs=[3.6,6.4,3.6,3.2]
cmd=["ffmpeg","-v","error","-y"]+sum([["-i",T+f"s{i}.mp4"] for i in range(1,5)],[])
off=0; fc=""; prev="[0:v]"
for i in range(1,4):
    off+=durs[i-1]-d; fc+=f"{prev}[{i}:v]xfade=transition=fade:duration={d}:offset={off:.2f}[x{i}];"; prev=f"[x{i}]"
fc=fc.rstrip(";"); total=sum(durs)-3*d
cmd+=["-filter_complex",fc,"-map",prev,"-c:v","libx264","-profile:v","high","-b:v","8M","-maxrate","10M","-bufsize","16M","-pix_fmt","yuv420p","-r","30","-movflags","+faststart","-an",OUT+"reel-boda-sin-audio.mp4"]
subprocess.run(cmd,check=True); print("total",total)
