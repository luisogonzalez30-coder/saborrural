# Contexto de Sabor Rural para cualquier sesión de Claude

Léelo entero antes de trabajar. Es la memoria común entre conversaciones: lo que no esté escrito aquí o en `conocimiento.md` y `carta.md`, otra sesión no lo sabe. Actualizado el 30-oct-2026.

## El negocio
- **Sabor Rural**: cafetería y pastelería en Ruta J-60 km 95, Sector Lora, Licantén, Región del Maule, Chile.
- WhatsApp +56 9 9210 1764 · Instagram @sabor_rural.
- Tienda Shopify: `saborruralcafeteria.myshopify.com`.
- Página de enlaces (la de la bio): https://luisogonzalez30-coder.github.io/saborrural/ (`index.html`).
- Horario: lunes a viernes 9:00–21:00, sábado y domingo 14:00–21:00.

## Cómo quiere el usuario que se trabaje
- Español, directo, sin saludos ni relleno. Tablas y viñetas, no bloques largos.
- **No inventar datos** (precios, sabores, horarios). Los hechos están en `conocimiento.md` y `carta.md`.
- Matemática exacta en precios. Marketing para Chile, enfocado en video corto orgánico (Reels, TikTok).
- Si algo falla, decirlo con claridad. No dar por hecho lo que no se verificó.

## Dónde está cada cosa
| Carpeta o archivo | Qué es |
|---|---|
| `calendario.json`, `estado.json` | Calendario de Instagram y registro de lo publicado |
| `publicar.mjs`, `.github/workflows/vigia.yml` | Publicador automático: cada ~4 min publica lo vencido |
| `media/` | Fotos, historias y reels |
| `media/como-encargar-torta/` | Video "Cómo encargar tu torta" (móvil y escritorio, con la voz del usuario) |
| `tema-v12/` | Código del tema de Shopify (`sections/sr-*.liquid`, `archivos/`) |
| `.claude/skills/InstaAgente` | Reglas y módulos para Instagram |

## Instagram
- Para publicar "ahora": agregar a `calendario.json` una entrada con `fecha` pasada (formato `2026-10-30T19:36:00-03:00`), `tipo` (`feed`, `story` o `reel`), `media` y `caption`. Hacer commit y push a `main`; el vigía lo publica en unos minutos y lo anota en `estado.json`.
- **Reels:** H.264 High, 1080x1920, unos 8 Mbps, audio AAC 48 kHz, `+faststart`. Un archivo con bitrate bajo y audio a 96 kHz fue rechazado una vez (error 2207076).
- Instagram **no permite borrar** publicaciones por API. Hay que borrarlas a mano en la app.
- No más de 1–2 reels por día. Los captions terminan con link en la bio, dirección y WhatsApp.

## Shopify (tema)
- Tema publicado al 30-oct: **v31**. Borrador: **v32** (botón "Activar sonido" del video). Nunca publicar el **v27**.
- No se puede escribir en el tema publicado. Procedimiento: duplicar el tema, subir archivos con `themeFilesUpsert` (tipo URL a `raw.githubusercontent.com/luisogonzalez30-coder/saborrural/<SHA>/tema-v12/...`), verificar con `checksumMd5`, y **el usuario publica**.
- Archivos (videos, imágenes) van a Contenido > Archivos con `fileCreate` o `fileUpdate`.
- Antes de tocar nada, comprobar con `get-shop-info` que la tienda conectada es "Cafetería Sabor Rural". Una vez la conexión apuntó a otra tienda.
- La página de tortas (`sr-tortas-lista.liquid`) tiene un bloque "Cómo encargar" con el video; usa `sr-como-encargar-movil.mp4/.jpg` y `sr-como-encargar-escritorio.mp4/.jpg`.

## Pendientes (30-oct-2026)
1. **Usuario:** publicar el tema v32.
2. **Reconectar Shopify a Sabor Rural** y subir los videos y portadas corregidos de `tema-v12/archivos/sr-como-encargar-*` (el video corregido arranca en movimiento; la tienda aún tiene la versión anterior).
3. **Usuario:** borrar de Instagram el reel horizontal https://www.instagram.com/reel/DfGGU_DDLeK/ (quedó el vertical https://www.instagram.com/reel/DfGPLiRkeqA/).
4. `media/r6-limon.mp4` está listo y sin programar.
5. Pendientes antiguos: confirmar horarios de retiro, `responder.yml` en rojo por créditos de Anthropic.

## Google Flow (generación de video con IA)
- Es un MCP **local** del PC del usuario (`C:\Users\Administrador\flow-mcp`). Solo funciona en la pestaña **Code** de la app de escritorio, en un chat nuevo, con el PC encendido y Chrome de Flow abierto con un proyecto. No funciona desde la nube.
- Herramientas: `flow_status`, `flow_generate`, `flow_wait`, `flow_cancel`, `flow_retry`, `flow_assets`, `flow_download`, `flow_agent_images`, `flow_edit`, `flow_continue`, `flow_trash`, `flow_character`, `flow_character_edit`, `flow_characters`, `flow_techniques`, `flow_narrate`, `flow_voices`, `flow_assemble`, `flow_transcribe`, `flow_captions`.
- Estado: plan PRO, 543 créditos (30-oct-2026).
- Regla: llamar `flow_status` primero, **decir el costo en créditos y esperar la aprobación del usuario** antes de generar.
- Partir siempre de **fotos reales** del local; la IA puede deformar las tortas. Fotos útiles: `media/04-jue-tortas-bluey-paw.jpg`, `media/02_cookies_feed.jpg`, `media/02-mar-tarta-pistacho.jpg`.
- Lo generado se guarda en `media/` y se publica solo si el usuario lo pide.

---
# ANEXO: historial detallado de decisiones (hasta el 30-oct-2026)

## Preferencias y correcciones del usuario (respetarlas)
- Quiere ver **imágenes y videos antes de publicar** ("muéstrame los creativos"). Mostrarlos con una hoja de contacto o enviando el archivo.
- Rechazó un collage y una torta en forma de corazón para el feed ("se ven feas esas tortas, busca otro producto"). Usó sus propias fotos de tortas Bluey y Paw Patrol, con el texto: "Tu idea, hecha realidad. 🎂 La realizamos aquí con cariño, profesionalismo y materiales de la más alta calidad".
- Probé quitar el fondo de las fotos con una herramienta local: el resultado fue malo (fotos con letrero o plato). Descartado. El usuario dijo "No lo hagas" a probar una herramienta de pago más fuerte. Recomendación pendiente: tomar fotos nuevas de tortas sobre fondo oscuro con rosado, para que la página se vea armoniosa.
- Pidió que el video de la página **arrancara en movimiento** ("parece una imagen"). Se corrigió.
- Le gusta el resultado cuando dice "Quedó hermoso" o "Me encantó". Los textos de los captions: cálidos, cortos, con emoji y hashtags regionales.
- Preguntó si automatizar Instagram baja el alcance: no se penaliza el método oficial por API. Lo que cuesta alcance: no poder usar la música o audios de moda de Instagram, publicar varias piezas el mismo día, y el formato horizontal. Recomendé 1 o 2 reels por día y subir a mano 1 o 2 reels por semana con audio de moda.

## Precios y productos verificados
- Kuchen, pies y tartas: **solo pieza entera**. Kuchen y tartas $17.000 completos; **tarta de chocolate y pistacho $19.000**; **Banoffee $19.000** (corregido en Shopify el 30-oct desde $17.000).
- Producto Shopify `kuchen-tarta-entera` (id 15267123331147), opción Sabor con 11 variantes: Kuchen Berries, Frambuesa, Frutilla, Manzana canela, Nuez, Pie de limón, Pie de coco, Banoffee, Tarta snickers, Tarta chocolate pistacho, Frambuesa miga.
- Tortas por encargo: producto `torta-encargo`, 28 sabores × 6 tamaños (15, 20, 25, 30, 35, 40 personas). Ejemplos: Durazno 20 personas $34.000; Lúcuma manjar 30 personas $54.000. Más de 40 personas, diseños, fondant: por WhatsApp. Mínimo 3 días completos de anticipación; retiro gratis en el local; pago en línea con Mercado Pago.
- Gift cards: colección `gift-cards` (id 513179222091), productos 15266881142859, 15267123200075, 15266881175627, 15266881208395.

## Shopify: detalles técnicos
- Tema Horizon con secciones propias `sr-*`. Temas: v29 (189616422987), v30 que pasó a llamarse **v31** (189617242187, hoy publicado), **v32** (189632053323, borrador con botón de sonido), v28 (189601873995), v27 (189600923723, **nunca publicar**).
- Las colecciones deben estar publicadas en el canal "Tienda online" (Publication 223343116363) con `publishablePublish`, o `collections['handle']` queda vacío en Liquid y las gift cards no aparecen.
- `fileCreate` con `contentType: IMAGE` para imágenes y `FILE` para mp4 (queda como GenericFile y se usa con `file_url`). Para reemplazar uno existente: `fileUpdate` con `originalSource`.
- Ids de archivos del video: móvil GenericFile 46237824647243, escritorio GenericFile 46237824680011, portadas MediaImage 46237824581707 (móvil) y 46237824614475 (escritorio).
- Redirect `/bio` (id 434835849291). Dominio principal para todos los links: `https://saborruralcafeteria.myshopify.com/...`.
- Algunos campos de GraphQL están en desuso: usar `publishedOnPublication`, `productByIdentifier(identifier:{handle:...})`.
- Modo liviano `html.sr-lite` (`sr-lite.css`): apaga animaciones y filtros. El video de cookies y el del bloque "Cómo encargar" no se descargan solos con modo liviano, ahorro de datos, 2G o `prefers-reduced-motion`; en ese caso muestran portada y botón de play.
- Sección de cookies (`sr-cookies.liquid`): video de fondo en bucle y difuminado (`sr-cookies-bg.mp4`); portada del taller de galletas `sr-taller-galletas-2.jpg` en `page.talleres.json`.
- Gift cards (`sr-gift-page.liquid`): tarjetas con colores `gp-c1..4`, destello y botón crema. Quedó pendiente un detalle: el subtítulo del botón dice "paga por WhatsApp" aunque ya cobra en línea.
- Kuchen (`sr-kuchen.liquid`, `snippets/sr-kc-chip.liquid`): chip "Entera $X" y sin selector de modo.

## Página de enlaces (`index.html`, bio de Instagram)
- Orden: carta, "Encarga tu torta" (tono rosado transparente, debajo de la carta, lleva **directo a la página de tortas**), torta de novios, gift cards, kuchen. Todos los links van al dominio principal.
- Quedó opcional: botón "Cotiza por mayor" y poner el link `/bio` en el perfil.

## Instagram: historial relevante
- Feed 12:30 de las tortas infantiles (Bluey y Paw Patrol) publicado el 29-oct.
- Reel "por mayor" de las cookies (escena del limón, dirigido a negocios): `media/r7-mayor.mp4`, publicado: https://www.instagram.com/reel/DfFIk6ACQlk/. Versión para clientes: `media/r6-limon.mp4`, sin programar.
- Reel "Cómo encargar tu torta": horizontal (borrar a mano) https://www.instagram.com/reel/DfGGU_DDLeK/ y vertical https://www.instagram.com/reel/DfGPLiRkeqA/.
- Hoy (30-oct): historia 07:30 (publicada), feed 12:30 `02_cookies_feed.jpg`, reel 19:30 `r-cookies.mp4`. Mañana (31-oct): historia 07:30, feed 12:30 tarta de pistacho, reel 19:30 `r-tartas.mp4`.
- El vigía (`vigia.yml`) se relanza cada ~5 h 40 y tiene un cron cada 3 h; hace `git pull` cada ciclo.
- Un reel con video a 1,4 Mbps y audio a 96 kHz falló (2207076); recodificado a 8 Mbps y audio 48 kHz funcionó.

## Cómo se hizo el video "Cómo encargar tu torta"
- No se grabó la tienda en vivo (desde el entorno de nube no se alcanza el dominio de la tienda). Se construyó una **réplica local de la página de tortas** con su código real: `herramientas/video-como-encargar/build_page.py` convierte `sr-tortas-lista.liquid` a HTML (fuentes Bricolage Grotesque y Hanken Grotesk de `enlaces-assets/`, fotos de obra) y `director.cjs` (Playwright) graba cuadro a cuadro: desplazamiento, toques, calendario y horario simulados, mensaje y resumen. `music.py` genera la música suave original.
- Versiones: móvil 1080x1920 (viewport 360x640 a 3x) y escritorio 1920x1080 (1280x720 a 1,5x). Mismo guion y mismos tiempos.
- **Voz del usuario** (`media/como-encargar-torta/voz-original.opus`): se transcribió con ElevenLabs (unos 7 centavos de dólar) para sincronizar. Texto: "¿Estás buscando una torta para una ocasión especial? En Sabor Rural encargarla es muy fácil y puedes hacerlo a través de nuestra página web. Primero, elige el tamaño que necesitas. Tienes opciones desde quince hasta cuarenta personas. Después, descubre nuestros veintiocho sabores. Puedes filtrar por manjar, chocolate o fruta, ver qué incluye cada torta y conocer su precio al instante. Luego, personaliza tu pedido. Selecciona la fecha y el horario que pasarás a retirarla. Si quieres, agrega un mensaje especial para tu torta y quién será el encargado de retirarla. Ya casi está. Revisa los detalles, paga de forma segura a través de nuestra plataforma y listo. Tu pedido queda agendado. Y lo mejor, puedes retirar tu torta gratis en nuestro local. Entra en nuestra web y encarga la tuya. En Sabor Rural hacemos especiales tus momentos importantes."
- Sincronía: 0 s portada; 9 s paso 1; 15,4 s paso 2; 26,2 s paso 3; 37,2 s resumen; 48,7 s tarjeta final; total 55,6 s. Mezcla: voz con compresión y música suave que baja cuando habla.
- Los valores que se ven (Lúcuma manjar, 30 personas, $54.000) y el texto "Elige una fecha desde el 02/11/2026" son de la fecha de grabación; hay que regrabar si cambian.

## Notas sobre servicios conectados
- **ElevenLabs** (Veo 3.1, Kling, Seedance, Runway, voces), **Artlist** y **Higgsfield** están conectados a la cuenta. Generan video con créditos propios.
- **Google Calendar** y **Drive** conectados. **Google Compute Engine** e **imagen** piden reconectar.
- La conexión de Shopify cambió varias veces de tienda ("LOG-In Spa", "Págacuandollegue" y por último Sabor Rural). Verificar siempre con `get-shop-info`.
- Sandbox de la nube: no alcanza el dominio de la tienda ni claude.ai; GitHub raw sí.
