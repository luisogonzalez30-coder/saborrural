import os
OUT='svg'; os.makedirs(OUT,exist_ok=True)
DK='#3A2412'; BODY='#E4B06A'; EDGE='#C98A3C'; SES='#FFF3D6'; BL='#F4A28C'
def seeds():
    import math
    pts=[(52,70),(70,48),(128,44),(150,66),(160,100),(150,150),(48,112),(60,150),(110,176),(86,170),(138,168),(45,90)]
    return ''.join(f'<ellipse cx="{x}" cy="{y}" rx="4.5" ry="2.2" fill="{SES}" transform="rotate({(i*47)%180} {x} {y})"/>' for i,(x,y) in enumerate(pts))
def body(hole=True):
    return (f'<path fill-rule="evenodd" fill="{BODY}" stroke="{EDGE}" stroke-width="4" d="M100 38a72 72 0 1 0 .01 0Z M100 62a24 24 0 1 1-.01 0Z"/>'
            f'<path d="M48 78a62 62 0 0 1 40-34" stroke="#F7D49B" stroke-width="6" stroke-linecap="round" fill="none"/>' + seeds())
def face(kind='smile',y=140):
    e=''
    if kind in('smile','tongue','open','determined','wink'):
        e+=f'<ellipse cx="78" cy="{y}" rx="5.5" ry="7" fill="{DK}"/><circle cx="76" cy="{y-3}" r="2" fill="#fff"/>'
        if kind=='wink': e+=f'<path d="M116 {y} q7 -7 14 0" stroke="{DK}" stroke-width="4" fill="none" stroke-linecap="round"/>'
        else: e+=f'<ellipse cx="122" cy="{y}" rx="5.5" ry="7" fill="{DK}"/><circle cx="120" cy="{y-3}" r="2" fill="#fff"/>'
    if kind=='sleep':
        e+=f'<path d="M72 {y} q6 6 12 0 M116 {y} q6 6 12 0" stroke="{DK}" stroke-width="4" fill="none" stroke-linecap="round"/>'
    if kind=='kawaii':
        e+=f'<ellipse cx="74" cy="{y}" rx="8" ry="10" fill="{DK}"/><circle cx="71" cy="{y-4}" r="3.2" fill="#fff"/><ellipse cx="126" cy="{y}" rx="8" ry="10" fill="{DK}"/><circle cx="123" cy="{y-4}" r="3.2" fill="#fff"/>'
    e+=f'<ellipse cx="62" cy="{y+12}" rx="9" ry="5.5" fill="{BL}" opacity=".8"/><ellipse cx="138" cy="{y+12}" rx="9" ry="5.5" fill="{BL}" opacity=".8"/>'
    m={'smile':f'<path d="M90 {y+10} q10 9 20 0" stroke="{DK}" stroke-width="4" fill="none" stroke-linecap="round"/>',
       'wink':f'<path d="M88 {y+9} q12 12 24 0" stroke="{DK}" stroke-width="4" fill="none" stroke-linecap="round"/>',
       'tongue':f'<path d="M88 {y+9} q12 12 24 0Z" fill="#8E2F3C" stroke="{DK}" stroke-width="3"/><path d="M96 {y+17} q4 9 9 0" fill="#F27C8E" stroke="{DK}" stroke-width="2"/>',
       'open':f'<path d="M88 {y+8} q12 22 24 0Z" fill="#8E2F3C" stroke="{DK}" stroke-width="3" stroke-linejoin="round"/>',
       'determined':f'<path d="M90 {y+12} h20" stroke="{DK}" stroke-width="4" stroke-linecap="round"/><path d="M68 {y-14} l18 5 M132 {y-14} l-18 5" stroke="{DK}" stroke-width="4" stroke-linecap="round"/>',
       'sleep':f'<ellipse cx="100" cy="{y+14}" rx="5" ry="4" fill="{DK}"/>',
       'kawaii':f'<path d="M92 {y+12} q8 7 16 0" stroke="{DK}" stroke-width="3.5" fill="none" stroke-linecap="round"/>'}[kind]
    return e+m
def limbs(arms='wave',legs=True):
    s=''
    a={'wave':f'<path d="M30 118 q-24 -4 -22 -34" /><path d="M170 118 q22 14 24 36" />',
       'both':f'<path d="M30 118 q-26 4 -24 36" /><path d="M170 118 q26 4 24 36" />',
       'up':f'<path d="M30 118 q-26 4 -24 36" /><path d="M170 112 q26 -22 14 -52" />',
       'run':f'<path d="M30 112 q-26 -12 -28 -40" /><path d="M170 120 q26 14 22 40" />',
       'hold':f'<path d="M30 118 q-26 4 -24 36" /><path d="M170 120 q16 6 22 -14" />',
       'none':''}[arms]
    if a: s+=f'<g stroke="{EDGE}" stroke-width="9" fill="none" stroke-linecap="round">{a}</g>'
    if legs: s+=f'<g stroke="{DK}" stroke-width="8" stroke-linecap="round"><path d="M80 178v32"/><path d="M120 178v32"/></g><ellipse cx="72" cy="214" rx="15" ry="7" fill="#E08A2E"/><ellipse cx="128" cy="214" rx="15" ry="7" fill="#E08A2E"/>'
    return s
def wrap(inner,back=''):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-30 0 260 240" width="260" height="240">{back}{inner}</svg>'
def mk(face_k='smile',arms='wave',legs=True,front='',back='',top=''):
    return wrap(limbs(arms,legs)+body()+face(face_k)+front+top,back)
S={}
S['01']=('Bagui clásico','Alegre y amistoso. La cara de la marca.',mk('smile','wave'))
chup=('<ellipse cx="100" cy="46" rx="66" ry="12" fill="#E9C97C" stroke="#B88E3A" stroke-width="3"/><path d="M62 44q4 -34 38 -34t38 34Z" fill="#F1D78F" stroke="#B88E3A" stroke-width="3"/><path d="M64 38h72" stroke="#C0392B" stroke-width="7"/>')
S['02']=('Bagui huaso','Orgullo campesino de Licantén: chupalla y buen humor.',mk('wink','wave',top=chup))
chef=('<g fill="#fff" stroke="#CFCFCF" stroke-width="3"><circle cx="76" cy="30" r="20"/><circle cx="124" cy="30" r="20"/><circle cx="100" cy="20" r="22"/><rect x="72" y="36" width="56" height="22" rx="4"/></g>')
bigote=f'<path d="M84 150 q8 -8 16 0 q8 -8 16 0 q-8 12 -16 4 q-8 8 -16 -4Z" fill="{DK}"/>'
S['03']=('Bagui chef','Perfeccionista y orgulloso de su horno.',mk('smile','both',top=chef,front=bigote))
ap='<path d="M62 160h76v26q-38 14 -76 0Z" fill="#2E3440"/>'
cup='<g transform="translate(176 96)"><rect x="-12" y="0" width="26" height="28" rx="4" fill="#fff" stroke="#999" stroke-width="3"/><path d="M14 6q12 2 0 16" stroke="#999" stroke-width="3" fill="none"/><path d="M-4 -6q-5 -8 0 -16M6 -6q-5 -8 0 -16" stroke="#cbbfae" stroke-width="3" fill="none" stroke-linecap="round"/></g>'
S['04']=('Bagui barista','Atento y servicial: te prepara el café de la mañana.',mk('smile','hold',front=ap+cup))
cap='<path d="M56 52q20 -50 82 -22q-2 18 -16 26Z" fill="#E05A6B" stroke="#B53A4B" stroke-width="3"/><circle cx="140" cy="30" r="10" fill="#fff"/><rect x="54" y="48" width="86" height="12" rx="6" fill="#fff"/>'
zz='<text x="150" y="40" font-family="Arial" font-weight="bold" font-size="22" fill="#7A7A99">Z</text><text x="170" y="22" font-family="Arial" font-weight="bold" font-size="16" fill="#7A7A99">z</text>'
S['05']=('Bagui dormilón','Tierno y soñoliento: el personaje del "buenos días".',mk('sleep','both',top=cap+zz))
capa='<path d="M40 112L-22 196 70 176 100 186 130 176 222 196 160 112Z" fill="#C0392B" stroke="#8E2A1F" stroke-width="3"/>'
S['06']=('Bagui superhéroe','Valiente y energético: salva tu desayuno.',mk('determined','up',back=capa,front='<path d="M62 124h76" stroke="none"/>'))
gorro='<path d="M58 52q4 -42 42 -42t42 42Z" fill="#4C7FB5" stroke="#35597F" stroke-width="3"/><rect x="54" y="48" width="92" height="14" rx="7" fill="#EDEDED" stroke="#bbb" stroke-width="2"/><circle cx="100" cy="8" r="9" fill="#fff"/>'
bufa='<path d="M54 160q46 18 92 0l4 16q-50 20 -100 0Z" fill="#D9534F" stroke="#A33A37" stroke-width="3"/><path d="M128 172v34l14 -4 -4 -30Z" fill="#D9534F" stroke="#A33A37" stroke-width="3"/>'
S['07']=('Bagui de invierno','Abrigado y acogedor: promos de café caliente.',mk('smile','both',top=gorro,front=bufa))
queso='<path d="M60 52q10 -16 34 -12q16 4 10 16q-6 10 -20 8q-14 8 -24 -12Z" fill="#fff" stroke="#D8D8D8" stroke-width="3"/><path d="M70 60q-6 14 -2 24" stroke="#fff" stroke-width="8" stroke-linecap="round" fill="none"/>'
S['08']=('Bagui con queso crema','Goloso y travieso: el que provoca antojo.',mk('tongue','wave',front=queso))
S['09']=('Bagui kawaii (sticker)','Sin brazos ni piernas: ideal para stickers y WhatsApp.',mk('kawaii','none',False))
cinta='<rect x="54" y="52" width="92" height="12" rx="6" fill="#fff" stroke="#ddd" stroke-width="2"/><path d="M146 58l20 -8 -4 18Z" fill="#fff" stroke="#ddd" stroke-width="2"/><rect x="54" y="52" width="92" height="4" fill="#E05A6B"/><path d="M160 80q6 8 0 14q-6 -6 0 -14Z" fill="#8FD3F4"/>'
S['10']=('Bagui deportista','Enérgico y motivador: promos de "arranca tu día".',mk('open','run',top=cinta))
import json
json.dump({k:v[:2] for k,v in S.items()},open('meta.json','w'),ensure_ascii=False)
for k,(t,d,svg) in S.items(): open(f'{OUT}/bagui-{k}.svg','w').write(svg)
cards=''.join(f'<div class="c"><div class="n">{k}</div>{svg}<h3>{t}</h3><p>{d}</p></div>' for k,(t,d,svg) in S.items())
open('sheet.html','w').write(f'''<!doctype html><meta charset=utf-8><style>
@font-face{{font-family:B;src:url(/home/user/saborrural/enlaces-assets/bricolage800.ttf)}}@font-face{{font-family:H;src:url(/home/user/saborrural/enlaces-assets/hanken700.ttf)}}
body{{margin:0;background:#F3F1EA;font-family:H}}h1{{font:800 34px B;text-align:center;margin:22px 0 4px;color:#3A2412}}.s{{text-align:center;color:#7a6a58;margin-bottom:10px}}
.g{{display:grid;grid-template-columns:repeat(5,1fr);gap:14px;padding:14px 22px 24px}}.c{{background:#fff;border-radius:18px;padding:12px 10px;text-align:center;position:relative;box-shadow:0 2px 10px #0001}}
.n{{position:absolute;left:12px;top:10px;background:#3A2412;color:#fff;border-radius:99px;width:30px;height:30px;line-height:30px;font:800 14px B}}h3{{font:800 18px B;margin:4px 0 2px;color:#3A2412}}p{{font-size:13px;color:#6b5a48;margin:0 6px}}svg{{width:100%;height:auto}}</style>
<h1>Bagui, la mascota de Sabor Rural · 10 bocetos</h1><div class=s>Bagel con carácter · Licantén</div><div class=g>{cards}</div>''')
