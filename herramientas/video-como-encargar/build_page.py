import re, json, sys
src = open('/home/user/saborrural/tema-v12/sections/sr-tortas-lista.liquid', encoding='utf-8').read()
S = {
 'eyebrow':'Tortas por encargo','titulo_a':'Elige tu','titulo_b':'torta',
 'bajada':'Elige cuántas personas, escoge el sabor y mira el valor al tiro. Pagas en línea y la retiras gratis en el local. Diseños especiales, por WhatsApp.',
 'esp_titulo':'¿Tu torta lleva diseño, fondant o algo especial?','esp_texto':'Cuéntanos tu idea y la cotizamos a tu medida.',
 'esp_boton':'Contáctanos por WhatsApp','esp_mensaje':'x','whatsapp':'56992101764'}
# datos de precios (rama de respaldo del propio archivo) + ids de variante falsos
m = re.search(r'\{%- else -%\}\[(.*?)\]\{%- endif -%\}', src, re.S)
rows = json.loads('[' + m.group(1) + ']')
rows = [r + [[1,2,3,4,5,6]] for r in rows]
data = json.dumps(rows, ensure_ascii=False)
# bloque tlData
src = re.sub(r'\{%- assign tp = .*?<script type="application/json" id="tlData">.*?</script>',
             '<script type="application/json" id="tlData">' + data.replace('\\','\\\\') + '</script>', src, flags=re.S)
src = re.sub(r'\{%- render \'sr-pagar\' -%\}', '<script>window.SRPay={buy:function(){}}</script>', src)
src = re.sub(r'\{% schema %\}.*?\{% endschema %\}', '', src, flags=re.S)
src = re.sub(r'^\{%- liquid.*?-%\}', '', src, flags=re.S)
# inspiración (bucle) -> fotos fijas
A='/home/user/saborrural/tema-v12/archivos/'
src = src.replace("{%- assign pm = section.settings.poster_movil | file_url -%}{%- assign pd = section.settings.poster_escritorio | file_url -%}","")
src = src.replace('{{ pd }}','arch/sr-como-encargar-escritorio.jpg').replace('{{ pm }}','arch/sr-como-encargar-movil.jpg')
src = src.replace('{{ section.settings.video_movil | file_url }}','arch/sr-como-encargar-movil.mp4').replace('{{ section.settings.video_escritorio | file_url }}','arch/sr-como-encargar-escritorio.mp4')
src = src.replace('{% unless section.settings.con_audio %} hidden{% endunless %}',' hidden')
src = re.sub(r'\{%- assign fotos.*?\{%- endfor -%\}', ''.join('<figure><img src="img/%s" alt=""></figure>' % f for f in ['sr-obra-oreo.jpg','sr-obra-lazo.jpg','sr-obra-lucuma.jpg','sr-obra-guindas.jpg']), src, flags=re.S)
src = src.replace('{{ hero_src }}', 'img/sr-encargo-corazon.jpg').replace('{{ wa }}', S['whatsapp']).replace('{{ section.id }}','x').replace('{{ routes.root_url }}','#')
src = re.sub(r'\{\{ section\.settings\.(\w+)( \| url_encode)? \}\}', lambda mm: S[mm.group(1)], src)
src = re.sub(r'\{%-?.*?-?%\}', '', src, flags=re.S)
src = re.sub(r'\{\{.*?\}\}', '', src)
# texto de ayuda sin fecha: atemporal
src = src.replace("'Mínimo 3 días completos de anticipación: la primera fecha disponible es el ' + fecha(MIN) + '.'", "'Mínimo 3 días completos de anticipación.'")
css = """
@font-face{font-family:Bricolage;src:url(fonts/bricolage800.ttf);font-weight:800}
@font-face{font-family:Hanken;src:url(fonts/hanken600.ttf);font-weight:400 600}
@font-face{font-family:Hanken;src:url(fonts/hanken700.ttf);font-weight:700 900}
:root{--font-display:Bricolage,sans-serif;--font-body:Hanken,sans-serif}
html,body{margin:0;background:#0C0D0F;font-family:var(--font-body);-webkit-font-smoothing:antialiased}
*{transition:none!important;animation-play-state:running}
.tl h1,.tl h2,.tl h3{font-weight:800}
html{scroll-behavior:auto!important}
"""
open('page.html','w',encoding='utf-8').write('<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>'+css+'</style></head><body><div class="sr">'+src+'</div></body></html>')
print(len(src))
