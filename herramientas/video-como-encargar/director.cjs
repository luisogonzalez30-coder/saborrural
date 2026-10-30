const { chromium } = require('playwright');
const fs = require('fs');
const FPS = 30, TOTAL = 55.6;
const DESK = process.env.MODE === 'desk';
const OUT = process.argv[2] || (DESK ? 'frames_d' : 'frames');
const LIMIT = +(process.argv[3] || 0); // para pruebas: detener tras N segundos
fs.rmSync(OUT, { recursive: true, force: true }); fs.mkdirSync(OUT, { recursive: true });

const OV_JS = `
(function(){
  var DESK = ${DESK};
  var css = document.createElement('style');
  css.textContent = [
  '.ov{position:fixed;z-index:2147483000;pointer-events:none;font-family:var(--font-body)}',
  '#tlFe::-webkit-datetime-edit{color:transparent!important}#tlFe::-webkit-datetime-edit-fields-wrapper{color:transparent!important}',
  '#ovFe{white-space:nowrap;overflow:hidden}',
  '#ovProg{left:0;top:0;height:4px;background:linear-gradient(90deg,#F59AAC,#E2587C);border-radius:0 3px 3px 0}',
  '#ovCap{left:12px;right:12px;top:14px}',
  '.ovpill{display:flex;align-items:center;gap:10px;padding:9px 14px 9px 9px;border-radius:18px;background:rgba(12,13,15,.86);border:1px solid rgba(242,132,151,.5);box-shadow:0 8px 24px rgba(0,0,0,.45)}',
  '.ovchip{flex:none;font:800 11px/1 var(--font-body);letter-spacing:.13em;text-transform:uppercase;color:#1A0A0F;background:linear-gradient(135deg,#F59AAC,#E2587C);padding:8px 10px;border-radius:12px}',
  '.ovtit{font:800 17px/1.15 var(--font-display);color:#fff}',
  '#ovPtr{width:38px;height:38px;margin:-19px 0 0 -19px;border-radius:50%;background:rgba(255,255,255,.35);border:2.5px solid rgba(255,255,255,.95);box-shadow:0 2px 10px rgba(0,0,0,.5)}',
  '#ovRip{width:38px;height:38px;margin:-19px 0 0 -19px;border-radius:50%;border:3px solid #F59AAC}',
  '#ovRing{border:2.5px solid #F59AAC;border-radius:14px;box-shadow:0 0 0 4px rgba(245,154,172,.25)}',
  '#ovDim{inset:0;background:rgba(0,0,0,.6)}',
  '#ovSheet{left:0;right:0;bottom:0;background:#1B1D21;border-radius:22px 22px 0 0;padding:16px 16px 18px;color:#fff;border-top:1px solid rgba(242,132,151,.35)}',
  '#ovSheet h4{margin:0 0 4px;font:800 18px var(--font-display);color:#fff}',
  '#ovSheet .sub{font:600 13px var(--font-body);color:#C9C6BD;margin-bottom:10px}',
  '.cal{display:grid;grid-template-columns:repeat(7,1fr);gap:4px;text-align:center}',
  '.cal i{font:700 12px var(--font-body);color:#9A978E;font-style:normal;padding:4px 0}',
  '.cal b{font:600 15px var(--font-body);height:38px;line-height:38px;border-radius:50%;color:#F3F1EA}',
  '.cal b.off{color:#5A5850}.cal b.sel{background:linear-gradient(135deg,#F59AAC,#E2587C);color:#1A0A0F;font-weight:800}',
  '.sbtn{display:flex;justify-content:flex-end;gap:10px;margin-top:12px}',
  '.sbtn span{font:700 14px var(--font-body);padding:11px 18px;border-radius:12px;color:#E4D6DA}',
  '.sbtn span.ok{background:linear-gradient(135deg,#F59AAC,#E2587C);color:#1A0A0F}',
  '.opt{padding:15px 14px;border-radius:12px;border:1px solid rgba(243,241,234,.18);margin-top:8px;font:700 15.5px var(--font-body);color:#F3F1EA}',
  '.opt.sel{background:linear-gradient(135deg,#F59AAC,#E2587C);color:#1A0A0F;border-color:transparent}',
  '#ovEnd{inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:24px;background:radial-gradient(90% 60% at 50% 0%,rgba(194,48,72,.55),transparent 70%),#0C0D0F}',
  '#ovEnd img{width:124px;margin-bottom:14px}',
  '#ovEnd h2{margin:0;font:800 36px/1.05 var(--font-display);color:#fff}',
  '#ovEnd h2 em{font-style:normal;color:#F59AAC}',
  '#ovEnd .ck{display:flex;flex-wrap:wrap;justify-content:center;gap:8px;margin:18px 0 20px}',
  '#ovEnd .ck span{font:700 13px var(--font-body);color:#F3F1EA;border:1px solid rgba(243,241,234,.3);border-radius:99px;padding:9px 13px;background:rgba(255,255,255,.06)}',
  '#ovEnd .go{font:800 17px var(--font-body);color:#1A0A0F;background:linear-gradient(135deg,#F59AAC,#E2587C);padding:16px 26px;border-radius:14px;box-shadow:0 10px 28px rgba(226,88,124,.45)}',
  '#ovEnd .ad{margin-top:20px;font:600 13.5px/1.5 var(--font-body);color:#C9C6BD}'
  ].join('');
  if (DESK) css.textContent += '#ovCap{left:80px;right:auto;top:16px;display:flex;justify-content:flex-start}.ovpill{padding:10px 18px 10px 10px;border-radius:20px}.ovtit{font-size:20px}.ovchip{font-size:12px;padding:9px 12px}#ovPtr,#ovRip{width:44px;height:44px;margin:-22px 0 0 -22px}#ovSheet{left:50%;right:auto;bottom:auto;top:50%;width:420px;border-radius:22px;padding:22px 22px 20px;border:1px solid rgba(242,132,151,.35)}#ovSheet h4{font-size:20px}.cal b{height:42px;line-height:42px;font-size:16px}#ovEnd{zoom:1.3}';
  document.head.appendChild(css);
  var h = '<div class="ov" id="ovFe"></div><div class="ov" id="ovProg"></div><div class="ov" id="ovCap"></div><div class="ov" id="ovRing"></div><div class="ov" id="ovDim"></div><div class="ov" id="ovSheet"></div><div class="ov" id="ovRip"></div><div class="ov" id="ovPtr"></div>'
   + '<div class="ov" id="ovEnd"><img src="fonts/logo.png" alt=""><h2>Encarga tu torta<br><em>en 1 minuto</em></h2><div class="ck"><span>Pagas en línea</span><span>Retiro gratis</span><span>28 sabores</span></div><div class="go">Elige tu torta ahora</div><div class="ad"><i style="color:#F59AAC;font-style:normal;font-weight:700">Hacemos especiales tus momentos importantes</i><br>Ruta J-60, km 95, Sector Lora, Licantén<br>@sabor_rural</div></div>';
  var w = document.createElement('div'); w.innerHTML = h; while (w.firstChild) document.body.appendChild(w.firstChild);
  var $ = function(i){ return document.getElementById(i); };
  var eo = function(x){ x = Math.max(0, Math.min(1, x)); return 1 - Math.pow(1 - x, 3); };
  var capKey = '', sheetKey = '';
  window.OV = { render: function(s, t) {
    if (s.scroll != null) window.scrollTo(0, s.scroll);
    var fe = document.getElementById('tlFe'), ft = $('ovFe'), fr = fe.getBoundingClientRect(), fs = getComputedStyle(fe);
    ft.style.left = (fr.left + 1) + 'px'; ft.style.top = (fr.top + 1) + 'px'; ft.style.width = (fr.width - 44) + 'px'; ft.style.height = (fr.height - 2) + 'px';
    ft.style.font = fs.font; ft.style.lineHeight = (fr.height - 2) + 'px'; ft.style.paddingLeft = fs.paddingLeft; ft.style.boxSizing = 'border-box'; ft.style.background = fs.backgroundColor === 'rgba(0, 0, 0, 0)' ? '#17191C' : fs.backgroundColor; ft.style.borderRadius = '12px 0 0 12px';
    ft.style.color = fe.value ? fs.color : 'rgba(243,241,234,.45)';
    ft.textContent = fe.value ? fe.value.split('-').reverse().join('/') : 'dd/mm/aaaa';
    $('ovProg').style.width = (100 * Math.min(1, t / s.total)) + '%';
    // leyenda
    var c = $('ovCap'), ck = s.cap ? s.cap.chip + '|' + s.cap.title : '';
    if (ck !== capKey) { capKey = ck; c.innerHTML = s.cap ? '<div class="ovpill"><span class="ovchip">' + s.cap.chip + '</span><span class="ovtit">' + s.cap.title + '</span></div>' : ''; }
    if (s.cap) { var a = eo((t - s.cap.t0) / 0.35); c.style.opacity = a; c.style.transform = 'translateY(' + (-10 * (1 - a)) + 'px)'; } else c.style.opacity = 0;
    // anillo de guía
    var r = $('ovRing');
    if (s.ring) { var k = 1 + 0.035 * Math.sin((t - s.ring.t0) * 9); r.style.display = 'block'; r.style.left = (s.ring.x - 5) + 'px'; r.style.top = (s.ring.y - 5) + 'px'; r.style.width = (s.ring.w + 10) + 'px'; r.style.height = (s.ring.h + 10) + 'px'; r.style.opacity = eo((t - s.ring.t0) / 0.25); r.style.transform = 'scale(' + k + ')'; } else r.style.display = 'none';
    // puntero
    var p = $('ovPtr'), rp = $('ovRip');
    p.style.opacity = s.ptr.vis; p.style.left = s.ptr.x + 'px'; p.style.top = s.ptr.y + 'px';
    var dt = t - s.ptr.tap;
    p.style.transform = 'scale(' + (dt >= 0 && dt < 0.18 ? 0.78 : 1) + ')';
    if (dt >= 0 && dt < 0.55) { var q = dt / 0.55; rp.style.display = 'block'; rp.style.left = s.ptr.x + 'px'; rp.style.top = s.ptr.y + 'px'; rp.style.opacity = 1 - q; rp.style.transform = 'scale(' + (1 + 1.9 * q) + ')'; } else rp.style.display = 'none';
    // hojas (fecha / horario)
    var d = $('ovDim'), sh = $('ovSheet');
    if (s.sheet) {
      var key = s.sheet.kind + '|' + s.sheet.sel;
      if (key !== sheetKey) { sheetKey = key; sh.innerHTML = s.sheet.kind === 'date' ? dateHtml(s.sheet.sel) : timeHtml(s.sheet.sel); }
      var e = eo((t - s.sheet.t0) / 0.38), o = s.sheet.out != null ? 1 - eo((t - s.sheet.out) / 0.3) : 1;
      d.style.display = 'block'; d.style.opacity = e * o; sh.style.display = 'block'; sh.style.transform = DESK ? 'translate(-50%, calc(-50% + ' + (36 * (1 - e * o)) + 'px))' : 'translateY(' + (100 * (1 - e * o)) + '%)'; if (DESK) { sh.style.opacity = e * o; }
    } else { d.style.display = 'none'; sh.style.display = 'none'; sheetKey = ''; }
    // tarjeta final
    var en = $('ovEnd');
    if (s.end != null) { var f = eo((t - s.end) / 0.6); en.style.display = 'flex'; en.style.opacity = f; en.style.transform = 'translateY(' + (16 * (1 - f)) + 'px)'; } else en.style.display = 'none';
  } };
  function dateHtml(sel) {
    var days = ['L','M','M','J','V','S','D'].map(function(x){ return '<i>' + x + '</i>'; }).join('');
    var cells = ''; for (var b = 0; b < 6; b++) cells += '<b></b>';
    for (var n = 1; n <= 30; n++) cells += '<b id="ovDay' + n + '" class="' + (n < 2 ? 'off' : '') + (n === sel ? ' sel' : '') + '">' + n + '</b>';
    return '<h4>Elige la fecha de retiro</h4><div class="sub">Noviembre de 2026</div><div class="cal">' + days + cells + '</div><div class="sbtn"><span>Cancelar</span><span class="ok" id="ovSet">Establecer</span></div>';
  }
  function timeHtml(sel) {
    var o = ['14:00 a 17:00 hrs', '17:00 a 21:00 hrs'];
    return '<h4>Horario de retiro</h4><div class="sub">Sábado y domingo de 14:00 a 21:00</div>' + o.map(function(x, i){ return '<div class="opt' + (sel === i ? ' sel' : '') + '" id="ovOpt' + i + '">' + x + '</div>'; }).join('');
  }
})();`;

(async () => {
  const b = await chromium.launch();
  const ctx = await b.newContext(DESK ? { viewport: { width: 1280, height: 720 }, deviceScaleFactor: 1.5, locale: 'es-CL' } : { viewport: { width: 360, height: 640 }, deviceScaleFactor: 3, locale: 'es-CL', isMobile: true, hasTouch: true });
  const page = await ctx.newPage();
  page.on('pageerror', e => console.log('ERR', e.message));
  await page.goto('file://' + process.cwd() + '/page.html');
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(600);
  await page.evaluate(OV_JS);
  await page.evaluate(() => { const h = document.querySelector('.tl-how'); if (h) h.style.display = 'none'; });

  let T = 0, fi = 0, scroll = 0;
  const S = { total: TOTAL, cap: null, ptr: { x: 180, y: 520, vis: 0, tap: -9 }, ring: null, sheet: null, end: null, scroll: 0 };
  const marks = [];
  const mark = (name) => { marks.push({ t: +T.toFixed(2), name }); console.log(T.toFixed(1) + 's', name); };
  async function frame() {
    if (LIMIT && T > LIMIT) { await b.close(); process.exit(0); }
    S.scroll = scroll;
    await page.evaluate(([s, t]) => window.OV.render(s, t), [S, T]);
    await page.screenshot({ path: `${OUT}/f${String(fi).padStart(5, '0')}.jpg`, type: 'jpeg', quality: 93 });
    fi++; T += 1 / FPS;
  }
  const ease = x => x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2;
  async function until(t) { const n = Math.round((t - T) * FPS); if (n > 0) await hold(n / FPS); else if (n < -2) console.log('ATRASO', (T - t).toFixed(2), 'en', t); }
  async function hold(sec) { for (let n = Math.round(sec * FPS); n > 0; n--) await frame(); }
  async function scrollTo(y, sec) {
    const max = await page.evaluate(() => document.documentElement.scrollHeight - innerHeight);
    y = Math.max(0, Math.min(max, y)); const y0 = scroll, n = Math.max(1, Math.round(sec * FPS));
    for (let i = 1; i <= n; i++) { scroll = y0 + (y - y0) * ease(i / n); await frame(); }
  }
  // desplaza para que el elemento quede a `top` px del borde superior de la pantalla
  async function showEl(sel, top, sec) {
    const y = await page.evaluate(([s]) => document.querySelector(s).getBoundingClientRect().top + window.scrollY, [sel]);
    await scrollTo(y - top, sec);
  }
  const caption = (chip, title) => { S.cap = { chip, title, t0: T }; };
  async function rectOf(sel) { return page.evaluate(s => { const r = document.querySelector(s).getBoundingClientRect(); return { x: r.left, y: r.top, w: r.width, h: r.height }; }, sel); }
  async function movePtr(x, y, sec) {
    const x0 = S.ptr.x, y0 = S.ptr.y, n = Math.max(1, Math.round(sec * FPS)); S.ptr.vis = 1;
    for (let i = 1; i <= n; i++) { const e = ease(i / n); S.ptr.x = x0 + (x - x0) * e; S.ptr.y = y0 + (y - y0) * e; await frame(); }
  }
  async function tap(sel, opts = {}) {
    if (opts.at != null) await until(opts.at - (opts.move ?? 0.55) - (opts.pre ?? 0.12));
    const r = await rectOf(sel), fx = opts.fx ?? 0.5, fy = opts.fy ?? 0.5;
    S.ring = { ...r, t0: T };
    await movePtr(r.x + r.w * fx, r.y + r.h * fy, opts.move ?? 0.55);
    await hold(opts.pre ?? 0.12);
    S.ptr.tap = T;
    if (opts.act) await opts.act(); else await page.evaluate(s => document.querySelector(s).click(), sel);
    S.ring = null;
    await hold(opts.post ?? 0.35);
  }
  const hidePtr = async (sec = 0.2) => { const n = Math.round(sec * FPS); const v0 = S.ptr.vis; for (let i = 1; i <= n; i++) { S.ptr.vis = v0 * (1 - i / n); await frame(); } S.ptr.vis = 0; };
  const setVal = (id, v) => page.evaluate(([i, val]) => { const e = document.getElementById(i); e.value = val; e.dispatchEvent(new Event('input', { bubbles: true })); e.dispatchEvent(new Event('change', { bubbles: true })); }, [id, v]);
  async function typeInto(sel, text, cps = 14) {
    await page.focus(sel);
    const per = Math.max(1, Math.round(FPS / cps)); let i = 0;
    while (i < text.length) { await page.keyboard.type(text[i++]); for (let k = 0; k < per; k++) await frame(); }
  }

  // ───────── 0 · gancho (voz: "¿Estás buscando una torta…? … nuestra página web") ─────────
  mark('gancho');
  caption('Cómo encargar', 'Tu torta en 1 minuto');
  { // arranca en movimiento desde el primer cuadro: la página baja sola y, en celular, un dedo la arrastra
    const y1 = await page.evaluate(() => document.querySelector('.tl-step:nth-child(1) h2').getBoundingClientRect().top + window.scrollY);
    const yEnd = Math.max(0, y1 - (DESK ? 240 : 200)), n = Math.round(7.8 * FPS);
    if (!DESK) { S.ptr.x = 180; S.ptr.y = 540; S.ptr.vis = 1; }
    for (let i = 1; i <= n; i++) {
      scroll = yEnd * Math.sin((i / n) * Math.PI / 2);
      if (!DESK) { const p = Math.min(1, T / 2.0); S.ptr.y = 540 - 230 * Math.sin(p * Math.PI / 2); S.ptr.vis = T < 2.2 ? 1 : Math.max(0, 1 - (T - 2.2) / 0.4); }
      await frame();
    }
    S.ptr.vis = 0;
  }
  await until(9.0);

  // ───────── 1 · personas (voz 9.4–14.4) ─────────
  mark('paso1');
  caption('Paso 1', '¿Para cuántas personas?');
  await showEl('.tl-step:nth-child(1) h2', DESK ? 100 : 84, 1.3);
  await tap('.tl-sz[data-n="30"]', { at: 13.7, move: 0.6, post: 0.4 });
  await hidePtr(0.2);
  await until(15.4);

  // ───────── 2 · sabor (voz 15.7–25.0) ─────────
  mark('paso2');
  caption('Paso 2', 'Elige tu sabor');
  await showEl('.tl-step:nth-child(2) h2', DESK ? 100 : 84, 1.3);
  await tap('.tl-f[data-f="manjar"]', { at: 20.0, move: 0.6, post: 0.4 });
  await hidePtr(0.15);
  const lucuma = await page.evaluate(() => Array.from(document.querySelectorAll('.tl-card')).findIndex(e => e.textContent.indexOf('Lúcuma manjar') === 0));
  await page.evaluate(i => document.querySelectorAll('.tl-card')[i].setAttribute('data-luc', '1'), lucuma);
  await showEl('[data-luc="1"]', DESK ? 300 : 230, 1.3);
  await tap('[data-luc="1"]', { at: 23.1, move: 0.5, post: 0.2 });
  await page.evaluate(() => { const c = document.querySelector('.tl-card.on'); if (c) c.setAttribute('data-luc', '1'); });
  await hidePtr(0.15);
  await showEl('[data-luc="1"]', DESK ? 300 : 200, 0.7);
  if (DESK) S.ring = { ...(await rectOf('.tl-rows')), t0: T };
  await until(26.2);
  S.ring = null;

  // ───────── 3 · fecha, horario, mensaje (voz 26.5–36.1) ─────────
  mark('paso3');
  caption('Paso 3', 'Fecha, horario y mensaje');
  await showEl('.tl-step:nth-child(3) h2', DESK ? 100 : 84, 1.2);
  await tap('#tlFe', { at: 28.3, move: 0.5, pre: 0.05, post: 0.05, act: async () => {} });
  S.sheet = { kind: 'date', sel: null, t0: T }; S.ring = null;
  await hold(0.3);
  await tap('#ovDay7', { move: 0.4, pre: 0.08, post: 0.1, act: async () => { S.sheet.sel = 7; } });
  await tap('#ovSet', { move: 0.35, pre: 0.08, post: 0.05, act: async () => { S.sheet.out = T; await setVal('tlFe', '2026-11-07'); } });
  await hold(0.3); S.sheet = null;
  await tap('#tlHr', { move: 0.4, pre: 0.05, post: 0.05, act: async () => {} });
  S.sheet = { kind: 'time', sel: null, t0: T }; S.ring = null;
  await hold(0.3);
  await tap('#ovOpt0', { move: 0.35, pre: 0.08, post: 0.2, act: async () => { S.sheet.sel = 0; } });
  S.sheet.out = T; await setVal('tlHr', '14:00 a 17:00'); await hold(0.3); S.sheet = null;
  await hidePtr(0.1);
  await showEl('#tlMs', DESK ? 330 : 250, 0.8);
  await tap('#tlMs', { at: 33.0, move: 0.35, pre: 0.08, post: 0.1, act: async () => {} });
  await hidePtr(0.05);
  await typeInto('#tlMs', 'Feliz cumpleaños Sofía', 18);
  await hold(0.15);
  await showEl('#tlNo2', DESK ? 330 : 250, 0.5);
  await tap('#tlNo2', { at: 35.5, move: 0.35, pre: 0.08, post: 0.1, act: async () => {} });
  await hidePtr(0.05);
  await typeInto('#tlNo2', 'Camila', 12);
  await page.evaluate(() => document.activeElement && document.activeElement.blur());
  await until(37.2);

  // ───────── 4 · resumen y pago (voz 37.3–47.8) ─────────
  mark('resumen');
  caption('Listo', 'Paga en línea y retira gratis');
  if (DESK) await scrollTo(scroll, 1.4); else await showEl('.tl-sum', 110, 1.4);
  S.ring = { ...(await rectOf('.tl-total')), t0: T };
  await until(41.0);
  S.ring = null;
  await tap('#sPay', { at: 42.2, move: 0.8, pre: 0.2, post: 0.6 });
  await hidePtr(0.2);
  await until(45.0);
  S.ring = { ...(await rectOf('.tl-rows li:nth-child(3)')), t0: T };
  await until(47.9);
  S.ring = null;
  await until(48.7);

  // ───────── 5 · cierre (voz 48.9–54.5) ─────────
  mark('cierre');
  S.cap = null; S.end = T;
  await until(55.6);
  mark('fin');
  fs.writeFileSync(DESK ? 'marks_d.json' : 'marks.json', JSON.stringify({ fps: FPS, frames: fi, dur: +(fi / FPS).toFixed(2), marks }, null, 1));
  await b.close();
})();
