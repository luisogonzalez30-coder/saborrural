// Publicador automático de Instagram — Sabor Rural
// Lee calendario.json, publica lo que ya venció y anota el resultado en estado.json.
// Requiere Node 20+ (usa fetch nativo). Sin dependencias.
import { readFile, writeFile } from 'node:fs/promises';

const GRAPH = process.env.GRAPH_BASE || 'https://graph.facebook.com/v21.0';
const IG_USER_ID = process.env.IG_USER_ID;
const TOKEN = process.env.IG_PAGE_TOKEN;
const DRY = process.env.DRY_RUN === '1';
const AHORA = process.env.AHORA ? new Date(process.env.AHORA) : new Date();
const MAX_ATRASO_H = Number(process.env.MAX_ATRASO_H || 24);          // más viejo que esto se marca "vencido"
const REPO = process.env.GITHUB_REPOSITORY;                            // dueño/repo, lo pone GitHub Actions
const RAMA = process.env.GITHUB_REF_NAME || 'main';
const MEDIA_BASE = (process.env.MEDIA_BASE_URL || (REPO ? `https://raw.githubusercontent.com/${REPO}/${RAMA}/` : '')).replace(/\/?$/, '/');
const ESPERA_MAX_MS = Number(process.env.ESPERA_MAX_MS || 6 * 60 * 1000);
const PAUSA_MS = Number(process.env.PAUSA_MS || 5000);

const dormir = (ms) => new Promise((r) => setTimeout(r, ms));
const leer = async (f, defecto) => { try { return JSON.parse(await readFile(f, 'utf8')); } catch { return defecto; } };
const urlMedia = (m) => (/^https?:\/\//.test(m) ? m : MEDIA_BASE + m.replace(/^\/+/, ''));

async function graph(metodo, ruta, params = {}, reintentos = 0) {
  const url = new URL(`${GRAPH}/${ruta}`);
  const cuerpo = new URLSearchParams({ ...params, access_token: TOKEN });
  for (let i = 0; ; i++) {
    try {
      const res = await fetch(metodo === 'GET' ? `${url}?${cuerpo}` : url, metodo === 'GET' ? {} : { method: 'POST', body: cuerpo });
      const datos = await res.json().catch(() => ({}));
      if (!res.ok || datos.error) {
        const e = datos.error || {};
        throw Object.assign(new Error(`Meta respondió ${res.status}: ${e.message || 'sin detalle'} (código ${e.code ?? '?'}, subcódigo ${e.error_subcode ?? '-'})`), { codigo: e.code, http: res.status });
      }
      return datos;
    } catch (err) {
      const transitorio = !err.http || err.http >= 500;
      if (i < reintentos && transitorio) { await dormir(2000 * (i + 1)); continue; }
      throw err;
    }
  }
}

async function esperarContenedor(id) {
  const limite = Date.now() + ESPERA_MAX_MS;
  while (Date.now() < limite) {
    const r = await graph('GET', id, { fields: 'status_code,status' }, 2);
    if (r.status_code === 'FINISHED') return;
    if (r.status_code === 'ERROR' || r.status_code === 'EXPIRED') throw new Error(`Meta no pudo procesar el archivo: ${r.status || r.status_code}`);
    await dormir(PAUSA_MS);
  }
  throw new Error('Meta tardó demasiado en procesar el archivo');
}

function parametros(p) {
  const base = {};
  if (p.tipo === 'feed') Object.assign(base, { image_url: urlMedia(p.media), caption: p.caption || '' });
  else if (p.tipo === 'story') Object.assign(base, { media_type: 'STORIES', image_url: urlMedia(p.media) });
  else if (p.tipo === 'reel') Object.assign(base, { media_type: 'REELS', video_url: urlMedia(p.media), caption: p.caption || '', share_to_feed: 'true' });
  else if (p.tipo !== 'carrusel') throw new Error(`Tipo desconocido: ${p.tipo}`);
  return base;
}

async function crearContenedor(p) {
  if (p.tipo !== 'carrusel') return graph('POST', `${IG_USER_ID}/media`, parametros(p), 2);
  const hijos = [];                                                              // carrusel: un contenedor por foto y uno padre
  for (const m of p.media) {
    const h = await graph('POST', `${IG_USER_ID}/media`, { image_url: urlMedia(m), is_carousel_item: 'true' }, 2);
    await esperarContenedor(h.id);
    hijos.push(h.id);
  }
  return graph('POST', `${IG_USER_ID}/media`, { media_type: 'CAROUSEL', children: hijos.join(','), caption: p.caption || '' }, 2);
}

async function publicar(p) {
  let contenedor;
  try {
    contenedor = await crearContenedor(p);                                       // crear contenedor: se puede reintentar
    await esperarContenedor(contenedor.id);
  } catch (err) { err.reintentable = true; throw err; }                          // aún no se publicó nada: se puede volver a intentar
  const pub = await graph('POST', `${IG_USER_ID}/media_publish`, { creation_id: contenedor.id }, 0); // publicar: NO se reintenta (evita duplicados)
  let permalink = '';
  try { permalink = (await graph('GET', pub.id, { fields: 'permalink' }, 1)).permalink || ''; } catch { /* opcional */ }
  return { media_id: pub.id, permalink };
}

async function main() {
  const calendario = await leer('calendario.json', null);
  if (!Array.isArray(calendario)) throw new Error('calendario.json no existe o no es una lista');
  const estado = await leer('estado.json', {});
  if (!DRY && (!IG_USER_ID || !TOKEN)) throw new Error('Faltan los secretos IG_USER_ID e IG_PAGE_TOKEN');

  const ids = new Set();
  for (const p of calendario) {
    if (!p.id || ids.has(p.id)) throw new Error(`Cada pieza necesita un id único (repetido o vacío: "${p.id}")`);
    ids.add(p.id);
    if (Number.isNaN(new Date(p.fecha).getTime())) throw new Error(`Fecha inválida en ${p.id}: ${p.fecha}`);
    if (p.tipo === 'carrusel' && (!Array.isArray(p.media) || p.media.length < 2 || p.media.length > 10)) throw new Error(`El carrusel ${p.id} necesita entre 2 y 10 fotos en "media" (lista)`);
    if (p.tipo === 'feed' || p.tipo === 'reel' || p.tipo === 'carrusel') if ((p.caption || '').length > 2200) throw new Error(`Caption de ${p.id} supera 2200 caracteres`);
  }

  const pendientes = calendario
    .filter((p) => { const e = estado[p.id]; return (!e || (e.reintentable && (e.intentos || 1) < 3)) && new Date(p.fecha) <= AHORA; })
    .sort((a, b) => new Date(a.fecha) - new Date(b.fecha));
  console.log(`${AHORA.toISOString()} · ${pendientes.length} pieza(s) por publicar${DRY ? ' (ensayo: no se publica nada)' : ''}`);

  let fallos = 0;
  for (const p of pendientes) {
    const atrasoH = (AHORA - new Date(p.fecha)) / 36e5;
    if (atrasoH > MAX_ATRASO_H) {
      console.log(`- ${p.id}: venció hace ${atrasoH.toFixed(1)} h, se omite`);
      if (!DRY) estado[p.id] = { omitido: AHORA.toISOString(), motivo: `vencido hace ${atrasoH.toFixed(1)} h` };
      continue;
    }
    if (DRY) { console.log(`- ${p.id} (${p.tipo}): se publicaría ${[].concat(p.media).map(urlMedia).join(' + ')}`); continue; }
    try {
      const r = await publicar(p);
      estado[p.id] = { publicado: new Date().toISOString(), ...r };
      console.log(`- ${p.id}: publicado ${r.permalink || r.media_id}`);
    } catch (err) {
      if (err.codigo === 190 || err.codigo === 102) {            // token vencido o inválido: no es culpa de la pieza
        console.error(`ERROR de acceso: ${err.message}\nRenueva IG_PAGE_TOKEN (ver LEEME.md, paso 6). No se tocó estado.json.`);
        process.exit(1);
      }
      fallos++;
      const previos = estado[p.id]?.intentos || 0;
      estado[p.id] = { error: err.message, intento: AHORA.toISOString(), reintentable: !!err.reintentable, intentos: previos + 1,
        ...(err.reintentable ? {} : { aviso: 'Falló al publicar: revisa Instagram a mano antes de reintentar (borra esta entrada para reintentar)' }) };
      console.error(`- ${p.id}: ERROR ${err.message}`);
    }
    await writeFile('estado.json', JSON.stringify(estado, null, 2) + '\n');   // guardar tras cada pieza
  }
  if (!DRY) await writeFile('estado.json', JSON.stringify(estado, null, 2) + '\n');
  if (fallos) process.exit(1);
}

main().catch((e) => { console.error(e.message); process.exit(1); });
