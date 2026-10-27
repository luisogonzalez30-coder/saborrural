// Revisa que IG_PAGE_TOKEN siga vivo y no esté por vencer. Falla (y GitHub avisa por correo) si hay que renovarlo.
const GRAPH = process.env.GRAPH_BASE || 'https://graph.facebook.com/v21.0';
const T = process.env.IG_PAGE_TOKEN;
if (!T) { console.error('Falta el secreto IG_PAGE_TOKEN'); process.exit(1); }
const NECESARIOS = ['instagram_content_publish'];
const OPCIONALES = ['instagram_manage_comments', 'instagram_manage_messages', 'pages_messaging', 'pages_manage_posts', 'pages_manage_engagement'];

const res = await fetch(`${GRAPH}/debug_token?input_token=${encodeURIComponent(T)}&access_token=${encodeURIComponent(T)}`);
const j = await res.json().catch(() => ({}));
if (!res.ok || j.error) { console.error(`::error::Token inválido o vencido: ${j.error?.message || res.status}. Renueva IG_PAGE_TOKEN (LEEME.md).`); process.exit(1); }
const d = j.data || {};
if (!d.is_valid) { console.error(`::error::El token ya no es válido (${d.error?.message || 'sin detalle'}). Renueva IG_PAGE_TOKEN.`); process.exit(1); }

const dias = d.expires_at ? (d.expires_at * 1000 - Date.now()) / 864e5 : Infinity;
console.log(`Token válido · tipo ${d.type} · ${dias === Infinity ? 'no vence' : `vence en ${dias.toFixed(1)} días`}`);
const scopes = d.scopes || [];
const faltan = NECESARIOS.filter((p) => !scopes.includes(p));
const sinOpc = OPCIONALES.filter((p) => !scopes.includes(p));
if (sinOpc.length) console.log(`::notice::Permisos del asistente que aún no tiene el token: ${sinOpc.join(', ')}`);
if (faltan.length) { console.error(`::error::Faltan permisos para publicar: ${faltan.join(', ')}`); process.exit(1); }
if (dias < 7) { console.error(`::error::El token vence en ${dias.toFixed(1)} días. Renuévalo ya.`); process.exit(1); }
