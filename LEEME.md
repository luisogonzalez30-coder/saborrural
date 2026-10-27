# Publicador automático de Instagram — Sabor Rural

Publica solo, a la hora que tú definas, las piezas de `calendario.json` en `@sabor_rural`: fotos de feed, historias y reels. Corre gratis en GitHub Actions cada 30 minutos entre las 09:00 y las 23:30 (hora de Chile).

**Cómo funciona:** cada 30 minutos, GitHub ejecuta `publicar.mjs`. El script revisa qué piezas ya llegaron a su hora y no se han publicado, las sube con la API oficial de Instagram y anota el resultado en `estado.json`. Una pieza nunca se publica dos veces.

**Qué incluye**

| Archivo | Para qué sirve |
|---|---|
| `publicar.mjs` | El script (Node 20, sin dependencias) |
| `calendario.json` | Qué se publica y cuándo (10 piezas del 27 oct al 6 nov) |
| `estado.json` | Registro de lo publicado (lo escribe el script) |
| `media/` | Las 9 imágenes y el reel |
| `.github/workflows/publicar.yml` | El programador de GitHub |

---

## Paso a paso para dejarlo listo hoy (60 a 90 minutos)

> **Regla de oro:** los tokens y claves se pegan **solo** en GitHub (Secrets), nunca en un chat ni en un archivo del repositorio.

### 1. Crear el repositorio en GitHub
1. En github.com → **New repository**. Nombre: `sabor-rural-instagram`.
2. Elige **Public**. Es necesario: Instagram descarga las imágenes desde una dirección pública, y en un repositorio privado esa dirección no funciona. Las imágenes ya serán públicas al publicarse. El calendario también será visible, y ahí no hay nada secreto.
3. Sube todo el contenido de esta carpeta (**Add file → Upload files**), incluida la carpeta `.github`. Si tu navegador no deja subir carpetas ocultas, crea el archivo `.github/workflows/publicar.yml` a mano con el contenido que trae.

### 2. Crear la app en Meta
1. Entra a **developers.facebook.com** con la misma cuenta de Facebook que administra la página SABOR RURAL. Si te lo pide, regístrate como desarrollador.
2. **Mis apps → Crear app**. Elige el caso de uso relacionado con **Instagram / administrar contenido** (el nombre cambia con frecuencia) y tipo **Empresa**.
3. Nombre de la app: `Sabor Rural Publicador`. Asócialo al portafolio `sabor_rural`.
4. La app queda en **modo Desarrollo**: está bien. Como tú eres administrador de la app y dueño de la cuenta, no necesitas pasar por la revisión de Meta para publicar en tu propio Instagram.

> Los nombres de los menús de Meta cambian seguido. Si algo no coincide, busca la opción equivalente o mándame una captura.

### 3. Generar el token en el Explorador de la API
1. Abre **developers.facebook.com/tools/explorer**.
2. Arriba a la derecha elige tu app `Sabor Rural Publicador` y el tipo **Token de usuario**.
3. En **Permisos** agrega: `instagram_basic`, `instagram_content_publish`, `pages_show_list`, `pages_read_engagement` y `business_management`.
4. Pulsa **Generate Access Token**. En la ventana de Facebook, marca la página **SABOR RURAL** y la cuenta de Instagram `@sabor_rural`.

### 4. Convertirlo en un token que no vence
1. Con ese token abre el **Depurador de tokens** (developers.facebook.com/tools/debug/accesstoken) y pulsa **Extender token de acceso**. Copia el token largo (dura unos 60 días).
2. Vuelve al Explorador, pega el token largo y haz la consulta **`me/accounts`**. Aparecerá la página SABOR RURAL con su `id` y su `access_token`.
3. Ese `access_token` de la **página** es el que usarás. Pégalo en el Depurador: debe decir **"Nunca vence"**.
4. Anota el `id` de la página (en tu captura de Meta es `1794429974182040`).

### 5. Obtener el ID de Instagram
En el Explorador, usa el token de la página y consulta:
`1794429974182040?fields=instagram_business_account`
La respuesta trae un `id`: ese es tu **IG_USER_ID**.

### 6. Guardar los secretos en GitHub
En el repositorio: **Settings → Secrets and variables → Actions → New repository secret**. Crea dos:

| Nombre | Valor |
|---|---|
| `IG_USER_ID` | El ID del paso 5 |
| `IG_PAGE_TOKEN` | El `access_token` de la página del paso 4 |

Si el token deja de funcionar (cambias la contraseña de Facebook, quitas permisos), repite los pasos 3 y 4 y reemplaza el secreto `IG_PAGE_TOKEN`.

### 7. Ensayo (no publica nada)
1. En la pestaña **Actions → Publicar en Instagram → Run workflow**, con **ensayo** marcado.
2. Abre la ejecución y revisa el registro: debe decir cuántas piezas publicaría y qué dirección de imagen usaría.
3. Copia una de esas direcciones en el navegador: la imagen debe verse.

### 8. Prueba real
1. Edita `calendario.json` y agrega una pieza de prueba con fecha de hace unos minutos (por ejemplo, una historia con `07_story_novios.jpg`).
2. Vuelve a ejecutar el workflow, esta vez **sin** marcar ensayo.
3. Revisa que la historia aparezca en Instagram y que `estado.json` registre "publicado". Luego borra la pieza de prueba del calendario.

### 9. Dejarlo corriendo
Desde ahí el programador se ejecuta solo. Las piezas con fecha futura se publican cuando llegan a su hora.

---

## Cómo agregar piezas nuevas

Cada pieza de `calendario.json` tiene:

| Campo | Qué es |
|---|---|
| `id` | Nombre único (no se puede repetir) |
| `fecha` | Fecha, hora y huso de Chile: `2026-11-10T19:30:00-03:00` |
| `tipo` | `feed` (foto), `story` (historia) o `reel` (video) |
| `media` | Ruta del archivo dentro de `media/` (o una dirección `https://` completa) |
| `caption` | Texto con hashtags (máximo 2.200 caracteres). Las historias no llevan texto. |

- **Huso horario:** Chile usa `-03:00` en horario de verano (septiembre a abril) y `-04:00` el resto del año. Hay que cambiarlo en las fechas de abril en adelante.
- **Formatos:** fotos en JPEG, de 4:5 a 1,91:1 para feed y 9:16 para historias. Reels en MP4 vertical, 9:16.
- **Quién actualiza el calendario:** súbelo a mano en GitHub, o pásamelo y te dejo el archivo listo cada semana.

## Cosas que conviene saber

- **Piezas vencidas:** si el programador no corrió y una pieza lleva más de 24 horas de atraso, se omite en vez de publicarse a destiempo. Aparece en `estado.json` como `omitido`.
- **Errores:** si una publicación falla, el registro de GitHub lo muestra y GitHub te manda un correo. Si el error ocurre antes de publicar, el script reintenta hasta 3 veces. Si ocurre justo al publicar, **no** reintenta y avisa que revises Instagram a mano, para evitar duplicados.
- **Retrasos:** GitHub puede demorar unos minutos en los horarios de mayor tráfico, así que una pieza puede salir hasta ~15 minutos tarde.
- **Reel:** si Instagram rechaza el video con un error de tipo de archivo, es porque `raw.githubusercontent.com` no sirve bien el MP4. Activa **GitHub Pages** (Settings → Pages → rama `main`) y crea la variable `MEDIA_BASE_URL` (Settings → Secrets and variables → Actions → Variables) con `https://TU-USUARIO.github.io/sabor-rural-instagram/`.
- **Límite de Meta:** hasta 100 publicaciones por API cada 24 horas. Estás muy por debajo.
- **Probado:** la lógica del script se probó contra un servidor simulado de Meta (publicación de foto, historia y reel, no duplicar, reintentos, token inválido). **No se ha probado contra Instagram real**: el ensayo y la prueba real de los pasos 7 y 8 son para eso.


---

# Asistente de respuestas (comentarios y mensajes directos)

`responder.mjs` revisa cada 15 minutos (08:00 a 23:45 de Chile) los comentarios nuevos y los DMs de `@sabor_rural`, y responde con Claude usando solo lo escrito en `conocimiento.md`.

| Situación | Qué hace |
|---|---|
| Pregunta o saludo | Responde breve y, si no está en `conocimiento.md` (precios, horarios, stock), deriva al WhatsApp |
| Elogio simple, emojis | Agradece o no responde |
| Spam, ofensas, estafas | Lo ignora |
| Reclamo, alergia, tema delicado | Responde con un mensaje empático y lo marca `escalar` en `estado-respuestas.json` para que lo atienda una persona |

- Empieza **desde la primera corrida real**: no contesta comentarios anteriores.
- Máximo 12 respuestas por corrida. Nunca responde dos veces lo mismo.
- DMs: solo dentro de las 24 h desde el último mensaje del cliente (regla de Instagram).
- Modelo por defecto `claude-opus-5-5`; se puede cambiar con la variable del repositorio `CLAUDE_MODEL` (por ejemplo `claude-haiku-5-5`, más barato).
- Hace falta el secreto `ANTHROPIC_API_KEY` y un `IG_PAGE_TOKEN` con los permisos `instagram_manage_comments` e `instagram_manage_messages` (más `pages_messaging`).
- Primero se prueba con **Run workflow → Ensayo marcado**: muestra qué respondería sin enviar nada.


---

# Token de Instagram: cómo renovarlo para que no vuelva a vencer

El token **debe ser de la página y salir de un token de usuario de larga duración**; si sale de uno corto, vence en 1 hora y el publicador se detiene.

1. **Graph API Explorer** (developers.facebook.com/tools/explorer): app *sabor rural mensajes*, token de usuario, con los permisos `instagram_basic`, `instagram_content_publish`, `pages_show_list`, `pages_read_engagement`, `business_management`, `instagram_manage_comments`, `instagram_manage_messages`, `pages_messaging`, `pages_manage_posts`, `pages_manage_engagement`. *Generate Access Token* y marcar la página y la cuenta de Instagram.
2. **Depurador de tokens** (developers.facebook.com/tools/debug/accesstoken): pegar ese token → *Extend Access Token* → copiar el token largo (60 días).
3. En el Explorer, pegar el token largo y consultar `me/accounts`. Copiar el `access_token` de la página SABOR RURAL.
4. GitHub → Settings → Secrets and variables → Actions → `IG_PAGE_TOKEN` → pegarlo.
5. Comprobar en el Depurador: **Expires: Never**.

`token.mjs` (workflow *Revisar token de Instagram*, una vez al día) falla y GitHub avisa por correo si el token venció, le faltan permisos o vence en menos de 7 días.
