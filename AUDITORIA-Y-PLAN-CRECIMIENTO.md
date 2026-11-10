# Auditoría completa y plan de crecimiento · Sabor Rural (10-nov-2026)

Fuentes: datos de la tienda Shopify (productos, analítica de 30 días y de 6 meses), el HTML publicado de la web, tus capturas de Instagram del 7-nov y todo lo trabajado en estas sesiones. Lo que no pude medir está marcado **[verificar]**. Las cifras de precios y metas son **propuestas** para ajustar con tus costos reales.

---
## 1. Resumen: dónde está el dinero que hoy se pierde

| # | Hallazgo | Impacto |
|---|---|---|
| 1 | **0 pedidos en línea en los últimos 6 meses** y conversión 0,0 % (analítica de Shopify). Hay 896 visitas en 30 días. **[verificar en el admin que sea esta tienda y que los pedidos no entren por otra vía]** | La web recibe gente y no vende. Es el mayor hueco. |
| 2 | **No hay ningún medidor**: sin Meta Pixel, sin Google Analytics ni Google Tag. | Imposible hacer anuncios con retargeting ni saber qué pieza vende. |
| 3 | **La web se muestra en modo computador en los celulares** (ajuste fijo `width=980` en el tema). | La mayoría del tráfico llega desde Instagram, en celular: letra diminuta, botones difíciles. Daña ventas y posicionamiento en Google. |
| 4 | **Sin dominio propio**: la tienda vive en `saborruralcafeteria.myshopify.com` y la bio apunta a `/bio`. | Poca confianza, no se recuerda, no posiciona. |
| 5 | **SEO vacío**: título "Saborrural – Cafetería Sabor Rural", **sin descripción**, sin imagen al compartir, y **los ~60 productos sin título ni descripción SEO**. | Casi nadie te encuentra en Google por "torta personalizada Licantén" o "galletas Nueva York". |
| 6 | **No se puede comprar nada para enviar**: no hay perfil de envío a Chile; los "delivery" son 5 productos locales (Licantén, Huapi, Placilla, Curepto, Sector Lora). | Imposible vender galletas NY a todo el país. |
| 7 | El 85 % de las visitas es "directo" y solo 6 % "social" | Instagram no está llevando tráfico medible al sitio (enlaces sin etiquetas UTM). |
| 8 | En Instagram: **las plantillas con texto rinden ~4,4 veces menos** que el producto real (≈350 vs ≈1.550 vistas) | Ver `PLAN-INSTAGRAM.md`. |
| 9 | Productos de alto valor sin vender en línea: **café en grano de Nicaragua**, cajas de regalo, tortas de matrimonio, packs de once | Margen alto, envío fácil, recompra. |

## 2. Auditoría de la web

### 2.1 Técnica
| Área | Estado | Qué hacer |
|---|---|---|
| Móvil | Fuerza diseño de computador (980 px) | Cambiar a `width=device-width,initial-scale=1` (la hoja ya tiene reglas para ≤760 px). Probar en v35 y publicar. |
| Velocidad | HTML 320 KB, **90 scripts** en la portada, 111 imágenes (8 sin texto alternativo) | Reducir scripts, imágenes en formato ligero, `loading=lazy`, texto alternativo en todas. |
| Título y descripción | Sin descripción; título genérico | Título: "Cafetería y pastelería en Licantén · Tortas por encargo | Sabor Rural". Descripción de 150 caracteres con la ruta y la oferta. |
| Redes al compartir | Sin imagen (`og:image` ausente) | Imagen 1200×630 de marca para cada página. |
| Datos estructurados | Solo en la carta | Agregar `LocalBusiness`, `Product`, `FAQPage`. |
| Analítica | Ninguna | Instalar GA4 + Meta Pixel + Conversions API + evento "Pedido iniciado" y "Pedido pagado". |
| Dominio | `.myshopify.com` | Comprar `saborrural.cl` y apuntarlo a la tienda. |
| Dirección | Se corrigió "Sector Lora" en v34 (falta publicar) | Publicar v34. La zona de reparto "Sector Lora" ($1.000) es un nombre de zona, no la dirección: se puede dejar. |
| Taller | "Taller de tartas" está activo con precio $0 | Ponerle precio o pasarlo a borrador. |

### 2.2 Conversión (cómo comprar)
- Cotizador de tortas bien armado (personas → sabor → fecha → pago). Se puede mejorar con: **foto en cada sabor**, "las más pedidas", total visible desde el paso 1 y **WhatsApp flotante con mensaje prellenado** del pedido.
- Falta **prueba social en la portada**: 85 reseñas de Google con 4,6 (dato de la web). Mostrarlas con fotos y enlace a Google.
- Falta **captura de contactos**: nadie se va con tu correo ni su cumpleaños. Un cupón de bienvenida (10 %) a cambio del correo y la fecha de cumpleaños es el cliente de torta del próximo año.
- Falta **urgencia honesta**: "pedidos de Navidad hasta el [fecha]" y cuenta regresiva (ya está en el banner de Navidad).

### 2.3 Páginas nuevas que traen clientes de afuera
| Página | Para qué | Palabra de búsqueda |
|---|---|---|
| `/galletas-ny` | Vender galletas a todo Chile | "galletas estilo Nueva York envío a todo Chile" |
| `/regalos` | Cajas, gift cards, torta para regalar en Licantén | "regalo gourmet", "regalar una torta" |
| `/empresas` | Coffee break, desayunos sorpresa, cajas corporativas | "coffee break Curicó / Licantén" |
| `/matrimonios` | Tortas de matrimonio y eventos | "torta de matrimonio Maule" |
| `/ruta-costa` | Pedir de antemano y retirar camino a Iloca y Duao | "dónde comer camino a Iloca" |
| `/blog` (guías cortas) | Posicionamiento local | "qué hacer en Licantén", "panoramas costa del Maule" |

## 3. Auditoría de Instagram

| Dato (7-nov) | Valor | Lectura |
|---|---|---|
| Seguidores / seguidos / publicaciones | 5.446 / 2.793 / 262 | Sigues al 51 % de tu audiencia: resta autoridad. Bajar de a poco. |
| Visualizaciones, últimos 30 días | 34,7 mil | Hay alcance: hay que convertirlo en visitas al perfil y a la web. |
| Mejores piezas | Stitch 2.805 · Cookies NY 2.327 · Tartas 1.935 | Producto real, cerca, sin gráfica encima. |
| Peores piezas | Plantillas 151–627 | Retirar el formato "catálogo". |
| Bio y enlace | Sin ubicación ni acción; enlace largo | Reescritura lista en `PLAN-INSTAGRAM.md`. |
| Respuestas automáticas | Caídas (sin créditos) | Responder a mano o con Meta Business Suite. |
| Música | Los reels automáticos salen sin audio | Subir a mano los de mayor potencial con audio de tendencia. |

Plan detallado de 14 días, 7 guiones y palabras clave por comentario: **`PLAN-INSTAGRAM.md`**.

## 4. Ángulos de venta de mayor potencial

### Ángulo 1 · Galletas Nueva York a todo Chile (el producto estrella)
Es tu pieza más vista y más fácil de enviar. Propuesta de cajas (precios **propuestos**; hoy la unidad es $2.500 y la Dubái $3.000):

| Caja | Precio propuesto | Por galleta | Para qué |
|---|---|---|---|
| Caja 4 | $13.900 | $3.475 | Primera compra / regalo pequeño |
| **Caja 6 (la que se empuja)** | **$19.900** | $3.317 | Regalo estándar |
| Caja 12 | $36.900 | $3.075 | Oficinas y familias |
| Caja Dubái 6 | $23.900 | $3.983 | Producto viral, margen alto |
| Suscripción "Galleta del mes" | $24.900 al mes (6 galletas) | — | Ingreso recurrente |

- **Envío:** cotizar Chilexpress, Starken y Correos Chile para paquetes pequeños; incluir en el precio de la caja un tramo de envío y **envío gratis desde $45.000** para subir el ticket.
- **Regla de margen:** precio ≥ 3 × costo de ingredientes + empaque + envío absorbido. Dame tus costos y ajusto la tabla.
- **Condiciones sanitarias [verificar con la SEREMI de Salud del Maule]:** enviar alimentos fuera de la comuna requiere la autorización sanitaria del lugar de elaboración y **etiquetado del Reglamento Sanitario de los Alimentos** (ingredientes, alérgenos, fecha, y posibles sellos "ALTO EN" por azúcares y calorías). Sin eso no conviene vender a todo Chile.
- **Prueba antes de lanzar:** 5 envíos reales a Santiago, Concepción y Antofagasta para medir cómo llegan (a 2 y 4 días).
- **Lanzamiento:** reel "Así se envía una caja", lista de espera con el 10 % de descuento, y primera tanda limitada de forma honesta (por capacidad, no por escasez inventada).

### Ángulo 2 · "Pide en ruta, retira sin esperar" (veraneantes de Iloca, Duao y Vichuquén)
Verano (dic–mar) pasa por tu puerta mucha gente que no sabe que existes. Cajas y packs pedidos por la web y retirados en la J-60: **Box Playa** (sándwiches + bebida + dulce), **Once para 2**, cajas de galletas. Señalética en el local con QR al pedido, perfil de Google Maps con "pedir en línea" y 3 alianzas con cabañas y campings de la zona (comisión o canje).

### Ángulo 3 · Regalar a Licantén desde cualquier parte
Quien vive en Santiago y quiere sorprender a la familia en la costa: compra en la web, tú entregas la torta o la caja en Licantén, Hualañé o Vichuquén (ya tienes zonas de reparto). Mensaje: **"Sorprende a quien quieres en la costa del Maule"**. Se promociona con gift cards y cajas.

### Ángulo 4 · Empresas, municipalidades y eventos
Coffee break, desayunos sorpresa y cajas de fin de año para oficinas, municipios y empresas de Curicó y Licantén. Un PDF de una página con 3 paquetes y reservas por la web. Un cliente corporativo vale por 20 clientes de torta.

### Ángulo 5 · Café de especialidad en grano (Nicaragua)
Producto de mayor margen y envío simple: bolsa de 250 g y de 1 kg, molido o en grano, y **Club mensual** (1 bolsa al mes). Es la forma más sólida de vender fuera de la comuna y de recomprar. **[confirmar proveedor, tostado y etiquetado]**.

### Ángulo 6 · Tortas de alto valor (matrimonio, aniversarios, premium)
La torta rosa y dorada y la de matrimonio muestran que puedes cobrar más. Crear una **línea "Atelier"** con 5 diseños fijos y precio visible desde X, con foto real, y el cotizador solo para los demás.

### Ángulo 7 · Comunidad y prueba social
Reseñas en Google (meta 300), cliente del mes con permiso, sorteo de una torta en Navidad con reglas claras (seguir, etiquetar a dos y compartir), colaboraciones de publicación con 10 cuentas locales (turismo, cabañas, foodies de Curicó).

## 5. Productos nuevos propuestos (alto valor)

| Producto | Precio sugerido | Por qué | Se envía a todo Chile |
|---|---|---|---|
| Caja regalo galletas NY (4 / 6 / 12) | $13.900 / $19.900 / $36.900 | Hero del catálogo | Sí |
| Caja Dubái | $23.900 | Tendencia, alto margen | Sí |
| Café Nicaragua 250 g | por definir con costo | Margen alto, recompra | Sí |
| Club mensual de café o de galletas | $19.900 – $24.900 al mes | Ingreso recurrente | Sí |
| Alfajores de maicena (caja 9) | por definir | Larga duración | Sí |
| Box de Navidad (kuchen + galletas + café) | $35.000 – $45.000 | Regalo corporativo | Local |
| Once para 2 / 4 | por definir | Ticket alto en el local | Retiro |
| Box Playa | por definir | Veraneantes | Retiro |
| Torta de matrimonio "desde" | por definir | Margen y prestigio | Local |
| Taller de galletas / tartas | por definir | Ingreso + comunidad | — |
| Gift cards (ya existen) | $10.000 – $30.000 | Navidad y regalos | Digital |

## 6. Plan de 90 días

| Plazo | Web | Instagram | Ventas |
|---|---|---|---|
| **Días 1-7** | Publicar v34 (dirección). Cambiar a diseño adaptable. Instalar GA4 + Meta Pixel. Escribir título y descripción de las 6 páginas clave. Poner precio al taller. | Perfil nuevo, destacadas, fijados. Pausar plantillas. 1 reel real al día. Sorteo de Navidad. | Activar cupón del 10 % por el correo. |
| **Días 8-30** | Comprar `saborrural.cl`. Páginas `/galletas-ny`, `/regalos`, `/empresas`. SEO de productos (60). Google Merchant gratis. Reseñas visibles. | 7 guiones del plan. Colaboraciones con 10 cuentas locales. Meta Ads de $3.000 al día a tortas de Navidad (Curicó, Hualañé, Licantén). | Pruebas de envío de galletas. Cotizar couriers. Trámites sanitarios. |
| **Días 31-60** | `/ruta-costa`, blog con 4 guías, carrito con venta cruzada, correo de abandono. | Series fijas ("Así se hace", "Cuánto sale"). Reedición del mejor reel cada semana. | **Lanzar galletas a todo Chile** con 10 % de lanzamiento. Club de café. Campaña a empresas. |
| **Días 61-90** | Segmentar clientes por cumpleaños, recordatorios de torta. | Meta Ads a Santiago para galletas (retargeting a visitantes). | Box Playa para enero. Revisar márgenes y subir precios donde corresponda. |

## 7. Metas a 90 días (objetivos, no promesas)
| Indicador | Hoy | Meta |
|---|---|---|
| Pedidos en línea al mes | 0 | 40 – 80 |
| Visitas a la web al mes | ~900 | 4.000 |
| Seguidores | 5.446 | 8.500 – 10.000 |
| Vistas medianas por pieza | ~350 | ≥ 1.000 |
| Reseñas de Google | 85 | 300 |
| Correos capturados | 0 | 600 |
| Clientes de fuera de la comuna | no medido | 25 % de los pedidos |

## 8. Presupuesto sugerido
| Concepto | Propuesta |
|---|---|
| Anuncios Meta | $3.000 – $5.000 diarios (≈ $90.000 – $150.000 al mes) |
| Dominio .cl | valor bajo anual **[cotizar en NIC Chile]** |
| Envíos de prueba y empaque | 10 cajas de prueba |
| Sorteo de Navidad | 1 torta |
| Todo lo demás | Lo hago yo: videos, páginas, textos, SEO y la carga en la tienda |

## 9. Lo que necesito de ti
1. **Costos** de la galleta NY (ingredientes, empaque, tiempo) para fijar precios y márgenes.
2. **Permiso** para publicar v34 y para cambiar a diseño adaptable (lo preparo en v35 y lo revisas).
3. **Sanitario:** ¿tienes resolución sanitaria? ¿Etiquetas de productos envasados?
4. **Café:** ¿proveedor, tostado y presentación?
5. **Capturas de Estadísticas** de Instagram (alcance, retención) y de **Shopify → Análisis → Ventas** para confirmar el "0 pedidos".
6. **Fecha límite** de pedidos de Navidad y los productos navideños con precio.
7. **Dominio:** ¿lo compro con tu cuenta?
