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
