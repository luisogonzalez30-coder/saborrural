// Asistente de Instagram — Sabor Rural
// Responde comentarios y mensajes directos (DM) de @sabor_rural con Claude.
// Revisa lo nuevo, responde solo lo que corresponde y anota todo en estado-respuestas.json.
// Requiere Node 20+ y @anthropic-ai/sdk.
import { readFile, writeFile } from 'node:fs/promises';
import Anthropic from '@anthropic-ai/sdk';

const GRAPH = process.env.GRAPH_BASE || 'https://graph.facebook.com/v21.0';
const IG_USER_ID = process.env.IG_USER_ID;
const TOKEN = process.env.IG_PAGE_TOKEN;
const DRY = process.env.DRY_RUN === '1';
const MODELO = process.env.CLAUDE_MODEL || 'claude-opus-5-5';
const MAX_RESPUESTAS = Number(process.env.MAX_RESPUESTAS || 12);        // tope por corrida
const AHORA = Date.now();
const ARCHIVO_ESTADO = 'estado-respuestas.json';
const DIAS_COMENTARIO = 7;                                             // no responde comentarios más viejos
const HORAS_DM = 23;                                                   // Instagram solo permite responder DM dentro de 24 h

const dormir = (ms) => new Promise((r) => setTimeout(r, ms));
const leer = async (f, d) => { try { return JSON.parse(await readFile(f, 'utf8')); } catch { return d; } };

async function graph(metodo, ruta, params = {}) {
  const url = new URL(`${GRAPH}/${ruta}`);
  const cuerpo = new URLSearchParams({ ...params, access_token: TOKEN });
  const res = await fetch(metodo === 'GET' ? `${url}?${cuerpo}` : url, metodo === 'GET' ? {} : { method: 'POST', body: cuerpo });
  const datos = await res.json().catch(() => ({}));
  if (!res.ok || datos.error) {
    const e = datos.error || {};
    throw Object.assign(new Error(`Meta respondió ${res.status}: ${e.message || 'sin detalle'} (código ${e.code ?? '?'})`), { codigo: e.code });
  }
  return datos;
}

// ---------- Claude ----------
const conocimiento = (await readFile(new URL('./conocimiento.md', import.meta.url), 'utf8')) + '\n\n' + (await readFile(new URL('./carta.md', import.meta.url), 'utf8'));
const SISTEMA = `Eres quien atiende las redes de Sabor Rural, una cafetería y pastelería de Licantén (Chile). Respondes comentarios y mensajes directos de Instagram en nombre del local.

TONO: cálido, cercano y breve, en español de Chile pero neutro (sin modismos fuertes). Máximo 1 emoji. Nada de frases de call center.
LARGO: comentarios públicos, 1 o 2 frases (máx. 220 caracteres). Mensajes directos, hasta 4 frases cortas.

REGLAS:
1. Afirma solo lo que está en la base de conocimiento. Los precios de la carta, el horario, la dirección y los medios de pago sí los puedes dar. Si preguntan por el precio de una torta por encargo, stock del día, promociones, talleres u otra cosa que no está ahí, no inventes: invita a escribir al WhatsApp +56 9 9210 1764. Si preguntan si están abiertos, usa la FECHA ACTUAL que se te da y el único horario de la base de conocimiento. Los precios se dan exactos, nunca como rango.
2. En comentarios públicos nunca pongas links (no son clicables): di "link en la bio" o da el WhatsApp. En mensajes directos sí puedes dar el link de la web y el WhatsApp.
3. Encargos de tortas: explica el proceso en pocas palabras y deriva al WhatsApp o a la web para enviar la idea. No fijes precios ni fechas.
4. Comentarios que son solo emojis, "bello", "rico", etiquetas a amigos o elogios: agradece de forma breve y distinta cada vez; si no aportan nada, accion "ignorar".
5. Spam, publicidad, estafas, links sospechosos, ofensas o provocaciones: accion "ignorar". No discutas.
6. Reclamos, quejas, problemas de salud o alergias, temas legales, prensa, proveedores o cualquier cosa delicada: accion "escalar". En la respuesta, un mensaje breve y empático que diga que alguien del equipo lo contactará personalmente (por DM o WhatsApp). No prometas compensaciones.
7. Nunca digas que eres una IA salvo que pregunten directo; en ese caso, di que eres el asistente virtual de Sabor Rural y que una persona del equipo revisa los casos especiales.
8. No pidas datos personales sensibles. Teléfono solo si el cliente quiere que lo llamen.
9. Si el mensaje es un saludo, responde con un saludo y pregunta en qué puedes ayudar.

BASE DE CONOCIMIENTO:
${conocimiento}`;

const ESQUEMA = {
  type: 'object',
  properties: {
    accion: { type: 'string', enum: ['responder', 'ignorar', 'escalar'] },
    respuesta: { type: 'string' },
    motivo: { type: 'string' },
  },
  required: ['accion', 'respuesta', 'motivo'],
  additionalProperties: false,
};

const claude = new Anthropic();

const fechaChile = () => new Intl.DateTimeFormat('es-CL', { timeZone: 'America/Santiago', weekday: 'long', day: 'numeric', month: 'long', year: 'numeric', hour: '2-digit', minute: '2-digit' }).format(new Date());

async function decidir(prompt) {
  prompt = `FECHA ACTUAL EN CHILE: ${fechaChile()}\n${prompt}`;
  const r = await claude.messages.create({
    model: MODELO,
    max_tokens: 4000,
    system: SISTEMA,
    messages: [{ role: 'user', content: prompt }],
    output_config: { effort: 'low', format: { type: 'json_schema', schema: ESQUEMA } },
  });
  if (r.stop_reason === 'refusal') return { accion: 'escalar', respuesta: '', motivo: 'El modelo declinó responder: revisar a mano' };
  const texto = r.content.filter((b) => b.type === 'text').map((b) => b.text).join('');
  const d = JSON.parse(texto);
  d.respuesta = (d.respuesta || '').trim();
  return d;
}

// ---------- Estado ----------
const estado = await leer(ARCHIVO_ESTADO, null) || { desde: null, comentarios: {}, mensajes: {} };
const primeraVez = !estado.desde;
if (primeraVez && !DRY) estado.desde = new Date(AHORA).toISOString();        // el asistente empieza desde ahora: no contesta el pasado
const desde = new Date(estado.desde || AHORA - 3 * 864e5).getTime();           // en ensayo mira 3 días atrás para mostrar ejemplos
const guardar = () => (DRY ? null : writeFile(ARCHIVO_ESTADO, JSON.stringify(estado, null, 2) + '\n'));
let enviadas = 0;

async function main() {
  if (!IG_USER_ID || !TOKEN) throw new Error('Faltan los secretos IG_USER_ID e IG_PAGE_TOKEN');
  if (!process.env.ANTHROPIC_API_KEY) throw new Error('Falta el secreto ANTHROPIC_API_KEY');
  const yo = (await graph('GET', IG_USER_ID, { fields: 'username' })).username;
  console.log(`${new Date(AHORA).toISOString()} · asistente de @${yo}${DRY ? ' (ensayo: no se envía nada)' : ''}${primeraVez && !DRY ? ' · primera corrida: queda anotado el punto de partida' : ''}`);
  if (primeraVez && !DRY) { await guardar(); console.log('Desde ahora responderé lo nuevo.'); return; }

  const errores = [];
  try { await comentarios(yo); } catch (e) { errores.push(`comentarios: ${e.message}`); console.error(`comentarios: ${e.message}`); }
  try { await mensajes(yo); } catch (e) { errores.push(`mensajes: ${e.message}`); console.error(`mensajes: ${e.message}`); }
  await guardar();
  const escalados = [...Object.entries(estado.comentarios), ...Object.entries(estado.mensajes)].filter(([, v]) => v.accion === 'escalar' && v.fecha >= new Date(AHORA).toISOString());
  if (escalados.length) console.log(`::warning::${escalados.length} caso(s) nuevo(s) escalado(s) a una persona. Revisa estado-respuestas.json (accion "escalar").`);
  if (errores.length) process.exit(1);
}

// ---------- Comentarios ----------
async function comentarios(yo) {
  const medios = (await graph('GET', `${IG_USER_ID}/media`, { fields: 'id,caption,timestamp,permalink', limit: '15' })).data || [];
  for (const m of medios) {
    if (AHORA - new Date(m.timestamp) > 21 * 864e5) continue;                  // solo publicaciones de las últimas 3 semanas
    let lista;
    try { lista = (await graph('GET', `${m.id}/comments`, { fields: 'id,text,username,timestamp,replies{id,username}', limit: '50' })).data || []; }
    catch (e) { console.error(`- ${m.id}: no pude leer comentarios (${e.message})`); continue; }
    for (const c of lista) {
      if (estado.comentarios[c.id]) continue;
      const t = new Date(c.timestamp).getTime();
      if (c.username === yo || t < desde || AHORA - t > DIAS_COMENTARIO * 864e5) continue;
      if ((c.replies?.data || []).some((r) => r.username === yo)) { estado.comentarios[c.id] = { omitido: 'ya respondido a mano' }; continue; }
      if (enviadas >= MAX_RESPUESTAS) { console.log('Tope de respuestas por corrida alcanzado; el resto queda para la próxima.'); return; }
      const d = await decidir(`CANAL: comentario público en una publicación.\nPUBLICACIÓN: ${(m.caption || '(sin texto)').slice(0, 400)}\nCOMENTARIO de @${c.username}: ${c.text}`);
      const reg = { usuario: c.username, texto: c.text, accion: d.accion, motivo: d.motivo, respuesta: d.respuesta, fecha: new Date().toISOString() };
      if (d.accion === 'ignorar' || !d.respuesta) { reg.accion = d.accion === 'responder' ? 'ignorar' : d.accion; console.log(`- comentario de @${c.username}: ${reg.accion} (${d.motivo})`); estado.comentarios[c.id] = reg; continue; }
      console.log(`- comentario de @${c.username}: "${c.text}" -> ${d.accion}: "${d.respuesta}"`);
      if (!DRY) {
        try { const r = await graph('POST', `${c.id}/replies`, { message: d.respuesta }); reg.respuesta_id = r.id; enviadas++; await dormir(3000); }
        catch (e) { reg.error = e.message; console.error(`  error al responder: ${e.message}`); }
      }
      estado.comentarios[c.id] = reg;
      await guardar();
    }
  }
}

// ---------- Mensajes directos ----------
async function mensajes(yo) {
  const pagina = await graph('GET', 'me', { fields: 'id' });
  // primero solo la lista (liviana); los mensajes se piden conversación por conversación para no pasarse del límite de datos de Meta
  let lista = null, ultimoError;
  for (const origen of [pagina.id, IG_USER_ID]) {                               // se prueba con el id de la página y con el de Instagram
    for (const limite of ['5', '1']) {                                          // si Meta dice "demasiados datos" o se agota el tiempo, menos datos
      try { lista = (await graph('GET', `${origen}/conversations`, { platform: 'instagram', fields: 'id,updated_time', limit: limite })).data || []; break; }
      catch (e) { ultimoError = e; console.error(`- conversaciones de ${origen === IG_USER_ID ? 'Instagram' : 'la página'} (límite ${limite}): ${e.message}`); await dormir(1500); }
    }
    if (lista) break;
  }
  if (!lista) throw ultimoError;
  for (const cv of lista) {
    const act = new Date(cv.updated_time).getTime();
    if (act < desde || AHORA - act > HORAS_DM * 36e5) continue;                 // sin actividad reciente: nada que responder
    let det;
    try { det = await graph('GET', cv.id, { fields: 'messages.limit(6){id,message,from,created_time}' }); }
    catch (e) { console.error(`- conversación ${cv.id}: no pude leerla (${e.message})`); continue; }
    const msgs = (det.messages?.data || []).slice().reverse();                  // de más viejo a más nuevo
    const ultimo = msgs[msgs.length - 1];
    if (!ultimo) continue;
    const mio = (x) => x.from?.id === IG_USER_ID || x.from?.username === yo;
    if (mio(ultimo) || estado.mensajes[ultimo.id]) continue;                    // lo último ya lo escribió el local, o ya lo atendí
    const t = new Date(ultimo.created_time).getTime();
    if (t < desde) continue;
    if (AHORA - t > HORAS_DM * 36e5) { estado.mensajes[ultimo.id] = { omitido: 'fuera de la ventana de 24 h' }; continue; }
    if (!ultimo.message) { estado.mensajes[ultimo.id] = { omitido: 'sin texto (foto, audio o reacción)' }; continue; }
    if (enviadas >= MAX_RESPUESTAS) { console.log('Tope de respuestas por corrida alcanzado.'); return; }
    const historial = msgs.map((x) => `${mio(x) ? 'LOCAL' : 'CLIENTE'}: ${x.message || '(adjunto)'}`).join('\n');
    const d = await decidir(`CANAL: mensaje directo (DM) de Instagram. Responde al último mensaje del CLIENTE.\nCONVERSACIÓN:\n${historial}`);
    const dest = (ultimo.from || {}).id;
    const reg = { usuario: ultimo.from?.username || dest, texto: ultimo.message, accion: d.accion, motivo: d.motivo, respuesta: d.respuesta, fecha: new Date().toISOString() };
    if (d.accion === 'ignorar' || !d.respuesta) { reg.accion = d.accion === 'responder' ? 'ignorar' : d.accion; console.log(`- DM de @${reg.usuario}: ${reg.accion} (${d.motivo})`); estado.mensajes[ultimo.id] = reg; continue; }
    console.log(`- DM de @${reg.usuario}: "${ultimo.message}" -> ${d.accion}: "${d.respuesta}"`);
    if (!DRY) {
      try { await graph('POST', 'me/messages', { recipient: JSON.stringify({ id: dest }), message: JSON.stringify({ text: d.respuesta }) }); enviadas++; await dormir(3000); }
      catch (e) { reg.error = e.message; console.error(`  error al responder: ${e.message}`); }
    }
    estado.mensajes[ultimo.id] = reg;
    await guardar();
  }
}

main().catch((e) => { console.error(e.message); process.exit(1); });
