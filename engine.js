/* multtt engine v0.1
 * Canvas 2D, 1080x1920. Сцена = JSON (без слов), слова = отдельный JSON по языкам.
 * Время детерминированное: render(t) можно звать в любом порядке (перемотка, запись).
 */
(function (root) {
'use strict';

const W = 1080, H = 1920, GROUND = 1250;
const OUT = '#1e1b26';

// ───────────────────────── утилиты ─────────────────────────
const clamp = (v, a, b) => Math.min(b, Math.max(a, v));
const lerp = (a, b, t) => a + (b - a) * t;
const rad = d => d * Math.PI / 180;
const isNum = v => typeof v === 'number' && isFinite(v);

const EASE = {
  linear: t => t,
  easeInOut: t => t < .5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2,
  easeIn: t => t * t,
  easeOut: t => 1 - (1 - t) * (1 - t),
  soft: t => 0.7 * t + 0.3 * (t < .5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2),
  back: t => { const c1 = 1.70158, c3 = c1 + 1; return 1 + c3 * Math.pow(t - 1, 3) + c1 * Math.pow(t - 1, 2); },
  backSoft: t => { const c1 = 1.1, c3 = c1 + 1; return 1 + c3 * Math.pow(t - 1, 3) + c1 * Math.pow(t - 1, 2); },
  bounce: t => {
    const n = 7.5625, d = 2.75;
    if (t < 1 / d) return n * t * t;
    if (t < 2 / d) return n * (t -= 1.5 / d) * t + .75;
    if (t < 2.5 / d) return n * (t -= 2.25 / d) * t + .9375;
    return n * (t -= 2.625 / d) * t + .984375;
  },
  snap: t => t < 0.5 ? 0 : 1
};
const EASE_NAMES = Object.keys(EASE);
function ease(name, t) { return (EASE[name] || EASE.easeInOut)(clamp(t, 0, 1)); }

function rng(seed) {
  let a = seed >>> 0;
  return () => {
    a |= 0; a = a + 0x6D2B79F5 | 0;
    let t = Math.imul(a ^ a >>> 15, 1 | a);
    t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
    return ((t ^ t >>> 14) >>> 0) / 4294967296;
  };
}
function hashStr(s) { let h = 2166136261; for (let i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 16777619); } return h >>> 0; }
function noise(x) { return (Math.sin(x * 1.7) + Math.sin(x * 2.9 + 1.3) + Math.sin(x * 4.3 + 2.1)) / 3; }

function lastBefore(arr, t) {
  let r = arr[0];
  for (let i = 0; i < arr.length; i++) { if (arr[i].t <= t) r = arr[i]; else break; }
  return r;
}
function mixObj(a, b, f) {
  const o = {};
  for (const k in a) {
    const va = a[k], vb = b[k];
    if (Array.isArray(va)) o[k] = va.map((v, i) => lerp(v, vb[i], f));
    else if (typeof va === 'number') o[k] = lerp(va, vb, f);
    else o[k] = vb;
  }
  return o;
}
function rr(ctx, x, y, w, h, r) {
  r = Math.min(r, w / 2, h / 2);
  ctx.beginPath();
  ctx.moveTo(x + r, y);
  ctx.arcTo(x + w, y, x + w, y + h, r);
  ctx.arcTo(x + w, y + h, x, y + h, r);
  ctx.arcTo(x, y + h, x, y, r);
  ctx.arcTo(x, y, x + w, y, r);
  ctx.closePath();
}

// ───────────────────────── герои ─────────────────────────
const CHARS = {
  eng: { name: 'Инженер', skin: '#f4cfae', shirt: '#7fb2e6', sleeve: '#7fb2e6', pants: '#33405e', shoe: '#4a3328', sy: 1.04, tw: 116 },
  bld: { name: 'Строитель', skin: '#dfa57a', shirt: '#8d93a3', sleeve: '#8d93a3', pants: '#8c7a55', shoe: '#3b3028', sy: 0.98, tw: 134 }
};
const ALIASES = { eng: 'eng', engineer: 'eng', 'инженер': 'eng', bld: 'bld', builder: 'bld', 'строитель': 'bld' };
const CHAR_IDS = ['eng', 'bld'];

// Статисты: тип "extra" — безликий человек, внешность задаётся в JSON (цвета, шапка, очки, галстук, свои фигуры)
const EXTRA_BASE = {
  kind: 'extra', name: 'Статист', skin: '#f1cba6', shirt: '#c9b25a', sleeve: null, pants: '#3a4152', shoe: '#2d2a30',
  sy: 1.0, tw: 122, hair: null, hat: null, glasses: false, tie: null, browY: -32
};
const LOOK_KEYS = ['skin', 'shirt', 'sleeve', 'pants', 'shoe', 'sy', 'tw', 'hair', 'hat', 'glasses', 'tie'];
function resolveCharDef(type, inst, types, err, id) {
  let base;
  if (type === 'eng' || type === 'bld') base = Object.assign({ kind: type }, CHARS[type]);
  else if (type === 'extra') base = Object.assign({}, EXTRA_BASE);
  else if (types[type] && typeof types[type] === 'object') base = Object.assign({}, EXTRA_BASE, types[type], { kind: 'extra' });
  else {
    err(`Персонаж "${id}": неизвестный тип "${type}" (есть: eng, bld, extra${Object.keys(types).map(k => ', ' + k).join('')})`);
    base = Object.assign({}, EXTRA_BASE);
  }
  for (const k of LOOK_KEYS) {
    if (inst && inst[k] != null) {
      if ((k === 'sy' || k === 'tw') && !isNum(inst[k])) err(`Персонаж "${id}": "${k}" должно быть числом`);
      else base[k] = inst[k];
    }
  }
  if (!base.sleeve) base.sleeve = base.shirt;
  return base;
}
const CALLOUT_STYLES = ['pop', 'shake', 'slam'];

const HIP_Y = -160, LEG = 88, UARM = 92, FARM = 88, SHOULDER_Y = -172;

// ───────────────────────── позы ─────────────────────────
// L/R = положение кисти относительно плеча [наружу, вниз] (px). Руки считаются через IK.
const BASE = { L: [24, 164], R: [24, 164], by: 0, air: 0, lean: 0, head: 0, sq: 1 };
const P = o => Object.assign({}, BASE, o);
const POSES = {
  idle: (lt, t) => { const b = Math.sin(t * 2.2) * 3; return P({ L: [24, 164 + b], R: [24, 164 - b], by: Math.sin(t * 2.2) * 1.5 }); },
  wave: (lt) => P({ R: [78 + Math.sin(lt * 10) * 30, -140], head: -4 }),
  point: () => P({ R: [168, -6], lean: 3 }),
  point_up: () => P({ R: [40, -175], lean: -2 }),
  present: () => P({ R: [150, 30], head: -3 }),
  hands_up: (lt, t) => P({ L: [70 + Math.sin(t * 30) * 3, -150], R: [70 + Math.sin(t * 30 + 1) * 3, -150], by: -4 }),
  shrug: () => P({ L: [110, 40], R: [110, 40], by: -10, head: 7 }),
  facepalm: () => P({ R: [-52, -92], head: 8, lean: 4 }),
  think: (lt, t) => P({ R: [-48, -40], L: [-30, 80], head: -7 + Math.sin(t * 1.5) * 2 }),
  arms_cross: () => P({ L: [-44, 30], R: [-44, 30] }),
  hips: () => P({ L: [58, 108], R: [58, 108], lean: -2 }),
  write: (lt) => P({ R: [-6 + Math.sin(lt * 14) * 10, 74 + Math.sin(lt * 9) * 4], L: [-20, 92], head: 6, lean: 3 }),
  measure: () => P({ L: [118, 50], R: [118, 50] }),
  tired: (lt, t) => P({ L: [16, 175], R: [16, 175], head: 14, lean: -6, by: 6 + Math.sin(t * 1.4) * 2, sq: .97 }),
  angry: (lt, t) => P({ L: [40, 60 + Math.sin(t * 40) * 4], R: [40, 60 + Math.sin(t * 40 + 2) * 4], lean: 5, head: -3, by: Math.sin(t * 50) * 2 }),
  cheer: (lt) => P({ L: [60 + Math.sin(lt * 8) * 10, -170], R: [60 - Math.sin(lt * 8) * 10, -170], by: -Math.abs(Math.sin(lt * 8)) * 14 }),
  dizzy: (lt) => P({ L: [30, 150], R: [30, 150], lean: Math.sin(lt * 3) * 10, head: Math.sin(lt * 3 + 1) * 14 }),
  dance: (lt) => P({
    L: [70, -60 + Math.sin(lt * 9) * 100], R: [70, -60 + Math.sin(lt * 9 + Math.PI) * 100],
    by: -Math.abs(Math.sin(lt * 9)) * 30, lean: Math.sin(lt * 4.5) * 8, head: Math.sin(lt * 4.5) * 10
  }),
  hammer: (lt) => {
    const p = (lt * 2.2) % 1; let ox, oy, lean;
    if (p < 0.6) { const k = ease('easeInOut', p / 0.6); ox = lerp(70, 36, k); oy = lerp(30, -170, k); lean = lerp(0, -6, k); }
    else if (p < 0.72) { const k = (p - 0.6) / 0.12; ox = lerp(36, 100, k * k); oy = lerp(-170, 100, k * k); lean = lerp(-6, 12, k); }
    else { const k = ease('easeOut', (p - 0.72) / 0.28); ox = lerp(100, 70, k); oy = lerp(100, 30, k); lean = lerp(12, 0, k); }
    return P({ R: [ox, oy], L: [40, 80], lean, by: lean > 6 ? 5 : 0 });
  },
  jump: (lt) => {
    const T = 0.8, u = (lt % T) / T;
    const air = u < 0.15 ? 0 : Math.sin(Math.PI * ((u - 0.15) / 0.85));
    const crouch = u < 0.15 ? Math.sin(Math.PI * u / 0.15) * 0.14 : (u > 0.9 ? Math.sin(Math.PI * (u - 0.9) / 0.1) * 0.08 : 0);
    return P({ air: -air * 250, sq: 1 - crouch + air * 0.06, L: [56, -120], R: [56, -120] });
  }
};
const POSE_NAMES = Object.keys(POSES);

function evalPose(name, lt, t) {
  const f = POSES[name] || POSES.idle;
  const o = f(lt, t);
  o._name = name;
  return o;
}

// ───────────────────────── эмоции ─────────────────────────
// mw ширина рта, mc изгиб (+улыбка), mo открытие, mk перекос; vis появление бровей, bh высота, bt наклон (+ нахмурены), bd асимметрия
const EMO0 = { mw: 46, mc: 0.05, mo: 0, mk: 0, vis: 0, bh: 0, bt: 0, bd: 0 };
const EMOS = {
  neutral: {},
  happy: { mw: 60, mc: 1, vis: 1, bh: 8, bt: -6 },
  laugh: { mw: 68, mc: 1, mo: 30, vis: 1, bh: 10, bt: -8 },
  angry: { mw: 54, mc: -0.9, vis: 1, bh: -6, bt: 24 },
  furious: { mw: 58, mc: -0.8, mo: 22, vis: 1, bh: -8, bt: 28 },
  surprised: { mw: 30, mc: 0, mo: 34, vis: 1, bh: 22, bt: -8 },
  shocked: { mw: 34, mc: 0, mo: 48, vis: 1, bh: 30, bt: -10 },
  sad: { mw: 44, mc: -0.7, vis: 1, bh: 2, bt: -22 },
  worried: { mw: 46, mc: -0.4, mo: 6, vis: 1, bh: 8, bt: -18 },
  smug: { mw: 56, mc: 0.6, mk: 10, vis: 1, bh: 6, bt: 6, bd: 14 },
  tired: { mw: 40, mc: -0.2, vis: 1, bh: -12, bt: 4 },
  confused: { mw: 40, mc: -0.3, mk: -6, vis: 1, bh: 10, bt: 0, bd: -16 }
};
for (const k in EMOS) EMOS[k] = Object.assign({}, EMO0, EMOS[k]);
const EMO_NAMES = Object.keys(EMOS);

// ───────────────────────── IK ─────────────────────────
function ik(sx, sy, tx, ty, l1, l2, side, wx, wy) {
  const dx = tx - sx, dy = ty - sy;
  const d = Math.hypot(dx, dy) || 1e-6;
  const dd = clamp(d, Math.abs(l1 - l2) + 2, (l1 + l2) * 0.999);
  const ux = dx / d, uy = dy / d;
  const hx = sx + ux * dd, hy = sy + uy * dd;
  const a = Math.acos(clamp((l1 * l1 + dd * dd - l2 * l2) / (2 * l1 * dd), -1, 1));
  const ang = Math.atan2(uy, ux);
  let best = null, bs = -1e9;
  for (const th of [ang + a, ang - a]) {
    const ex = sx + Math.cos(th) * l1, ey = sy + Math.sin(th) * l1;
    const s = ey * wy + side * ex * wx;
    if (s > bs) { bs = s; best = [ex, ey]; }
  }
  return { ex: best[0], ey: best[1], hx, hy };
}

// ───────────────────────── рисование фигур из JSON ─────────────────────────
const pathCache = new Map();
function getPath(d) {
  let p = pathCache.get(d);
  if (!p) { p = new Path2D(d); pathCache.set(d, p); }
  return p;
}
function fillStyle(ctx, f, bbox) {
  if (Array.isArray(f)) {
    if (!bbox) return f[0];
    const g = ctx.createLinearGradient(0, bbox[1], 0, bbox[1] + bbox[3]);
    f.forEach((c, i) => g.addColorStop(f.length === 1 ? 0 : i / (f.length - 1), c));
    return g;
  }
  return f;
}
function shapeBBox(s) {
  switch (s.t) {
    case 'rect': return [s.x, s.y, s.w, s.h];
    case 'circle': return [s.x - s.r, s.y - s.r, s.r * 2, s.r * 2];
    case 'ellipse': return [s.x - s.rx, s.y - s.ry, s.rx * 2, s.ry * 2];
    case 'poly': {
      let x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9;
      for (const p of s.pts) { x0 = Math.min(x0, p[0]); y0 = Math.min(y0, p[1]); x1 = Math.max(x1, p[0]); y1 = Math.max(y1, p[1]); }
      return [x0, y0, x1 - x0, y1 - y0];
    }
    case 'path': return s.box || null;
    default: return null;
  }
}
function applyAnim(ctx, a, t, px, py) {
  const ph = a.ph || 0, sp = a.s == null ? 0.5 : a.s, am = a.a == null ? 1 : a.a;
  ctx.translate(px, py);
  switch (a.k) {
    case 'sway': ctx.rotate(rad(am * Math.sin(2 * Math.PI * sp * t + ph))); break;
    case 'bob': ctx.translate(0, am * Math.sin(2 * Math.PI * sp * t + ph)); break;
    case 'slide': ctx.translate(am * Math.sin(2 * Math.PI * sp * t + ph), 0); break;
    case 'spin': ctx.rotate(2 * Math.PI * sp * t + ph); break;
    case 'pulse': { const k = 1 + am * Math.sin(2 * Math.PI * sp * t + ph); ctx.scale(k, k); break; }
    case 'drift': ctx.translate(sp * t, 0); break;
    case 'shake': ctx.translate(am * noise(t * 40 * sp + ph), am * noise(t * 37 * sp + ph + 5)); break;
    case 'blink': ctx.globalAlpha *= (Math.sin(2 * Math.PI * sp * t + ph) > 0 ? 1 : clamp(a.a == null ? 0.2 : a.a, 0, 1)); break;
  }
  ctx.translate(-px, -py);
}
function drawShapes(ctx, shapes, t, T) {
  for (const s of shapes) drawShape(ctx, s, t, T);
}
function drawShape(ctx, s, t, T) {
  ctx.save();
  if (s.alpha != null) ctx.globalAlpha *= s.alpha;
  if (s.anim) {
    const pv = s.pivot || [s.x || 0, s.y || 0];
    applyAnim(ctx, s.anim, t, pv[0], pv[1]);
  }
  switch (s.t) {
    case 'g': {
      ctx.translate(s.x || 0, s.y || 0);
      if (s.rot) ctx.rotate(rad(s.rot));
      if (s.sc != null) ctx.scale(s.sc, s.sc);
      drawShapes(ctx, s.shapes || [], t, T);
      break;
    }
    case 'text': {
      const txt = T(s.key);
      ctx.font = `${s.weight || 800} ${s.size || 60}px ${s.font || '"Arial Black", Arial, sans-serif'}`;
      ctx.textAlign = s.align || 'center'; ctx.textBaseline = 'middle';
      ctx.translate(s.x || 0, s.y || 0);
      if (s.rot) ctx.rotate(rad(s.rot));
      if (s.stroke) { ctx.lineJoin = 'round'; ctx.lineWidth = s.sw || 6; ctx.strokeStyle = s.stroke; ctx.strokeText(txt, 0, 0); }
      ctx.fillStyle = s.fill || '#fff';
      ctx.fillText(txt, 0, 0);
      break;
    }
    case 'line': {
      ctx.beginPath(); ctx.moveTo(s.x1, s.y1); ctx.lineTo(s.x2, s.y2);
      ctx.strokeStyle = s.stroke || '#000'; ctx.lineWidth = s.sw || 4; ctx.lineCap = s.cap || 'round';
      if (s.dash) ctx.setLineDash(s.dash);
      ctx.stroke();
      break;
    }
    default: {
      let filled = false;
      switch (s.t) {
        case 'rect':
          if (s.r) rr(ctx, s.x, s.y, s.w, s.h, s.r); else { ctx.beginPath(); ctx.rect(s.x, s.y, s.w, s.h); }
          break;
        case 'circle': ctx.beginPath(); ctx.arc(s.x, s.y, s.r, 0, Math.PI * 2); break;
        case 'ellipse': ctx.beginPath(); ctx.ellipse(s.x, s.y, s.rx, s.ry, rad(s.rot || 0), 0, Math.PI * 2); break;
        case 'poly':
          ctx.beginPath();
          s.pts.forEach((p, i) => i ? ctx.lineTo(p[0], p[1]) : ctx.moveTo(p[0], p[1]));
          if (s.closed !== false) ctx.closePath();
          break;
        case 'path': break;
        default: filled = true;
      }
      if (filled) break;
      const bb = shapeBBox(s);
      const p2 = s.t === 'path' ? getPath(s.d) : null;
      if (s.fill) { ctx.fillStyle = fillStyle(ctx, s.fill, bb); p2 ? ctx.fill(p2) : ctx.fill(); }
      if (s.stroke) {
        ctx.strokeStyle = s.stroke; ctx.lineWidth = s.sw || 4; ctx.lineJoin = 'round'; ctx.lineCap = s.cap || 'round';
        if (s.dash) ctx.setLineDash(s.dash);
        p2 ? ctx.stroke(p2) : ctx.stroke();
      }
    }
  }
  ctx.restore();
}

const SHAPE_TYPES = ['rect', 'circle', 'ellipse', 'poly', 'path', 'line', 'text', 'g'];
function validateShapes(shapes, where, err, texts) {
  if (!Array.isArray(shapes)) { err(`${where}: shapes должен быть массивом`); return; }
  shapes.forEach((s, i) => {
    const w = `${where} → shapes[${i}]`;
    if (!s || typeof s !== 'object') { err(`${w}: ожидался объект`); return; }
    if (!SHAPE_TYPES.includes(s.t)) { err(`${w}: неизвестный тип "${s.t}" (есть: ${SHAPE_TYPES.join(', ')})`); return; }
    const need = { rect: ['x', 'y', 'w', 'h'], circle: ['x', 'y', 'r'], ellipse: ['x', 'y', 'rx', 'ry'], line: ['x1', 'y1', 'x2', 'y2'] }[s.t];
    if (need) for (const k of need) if (!isNum(s[k])) err(`${w}: ${s.t} требует число "${k}"`);
    if (s.t === 'poly' && !(Array.isArray(s.pts) && s.pts.length >= 2 && s.pts.every(p => Array.isArray(p) && isNum(p[0]) && isNum(p[1])))) err(`${w}: poly требует pts: [[x,y],...]`);
    if (s.t === 'path') { if (typeof s.d !== 'string') err(`${w}: path требует строку d`); }
    if (s.t === 'text' && typeof s.key !== 'string') err(`${w}: text требует key (ключ из файла текстов, не сам текст)`);
    if (s.t === 'g') validateShapes(s.shapes || [], w, err, texts);
    if (s.anim && !['sway', 'bob', 'slide', 'spin', 'pulse', 'drift', 'shake', 'blink'].includes(s.anim.k)) err(`${w}: неизвестная анимация "${s.anim.k}"`);
  });
}

// ───────────────────────── эффекты ─────────────────────────
function star(ctx, x, y, r, n = 5) {
  ctx.beginPath();
  for (let i = 0; i < n * 2; i++) {
    const a = -Math.PI / 2 + i * Math.PI / n, rr_ = i % 2 ? r * 0.45 : r;
    ctx.lineTo(x + Math.cos(a) * rr_, y + Math.sin(a) * rr_);
  }
  ctx.closePath();
}
const FX = {
  exclaim: (c, x, y, lt, d) => bubble(c, x, y, lt, d, '!', '#e5342b'),
  question: (c, x, y, lt, d) => bubble(c, x, y, lt, d, '?', '#2d6cdf'),
  idea: (c, x, y, lt, d) => {
    const k = ease('back', lt / 0.25), fade = clamp((d - lt) / 0.2, 0, 1);
    c.save(); c.translate(x, y - 50); c.scale(k, k); c.globalAlpha = fade;
    for (let i = 0; i < 8; i++) {
      const a = i * Math.PI / 4 + lt * 0.5, on = Math.sin(lt * 14 + i) > -0.2;
      if (!on) continue;
      c.beginPath(); c.moveTo(Math.cos(a) * 52, Math.sin(a) * 52); c.lineTo(Math.cos(a) * 78, Math.sin(a) * 78);
      c.strokeStyle = '#ffd400'; c.lineWidth = 9; c.lineCap = 'round'; c.stroke();
    }
    c.fillStyle = '#ffe45e'; c.strokeStyle = OUT; c.lineWidth = 7;
    c.beginPath(); c.arc(0, 0, 38, 0, Math.PI * 2); c.fill(); c.stroke();
    rr(c, -16, 34, 32, 22, 6); c.fillStyle = '#9aa3b2'; c.fill(); c.stroke();
    c.restore();
  },
  anger: (c, x, y, lt, d) => {
    const k = ease('back', lt / 0.2) * (1 + 0.08 * Math.sin(lt * 20)), fade = clamp((d - lt) / 0.2, 0, 1);
    c.save(); c.translate(x + 40, y - 20); c.scale(k, k); c.globalAlpha = fade;
    c.strokeStyle = '#e5342b'; c.lineWidth = 11; c.lineCap = 'round';
    for (let i = 0; i < 4; i++) {
      c.save(); c.rotate(i * Math.PI / 2 + Math.PI / 4);
      c.beginPath(); c.arc(30, 0, 30, Math.PI * 0.55, Math.PI * 1.45); c.stroke(); c.restore();
    }
    c.restore();
  },
  sweat: (c, x, y, lt, d) => {
    const fade = clamp((d - lt) / 0.3, 0, 1);
    c.save(); c.globalAlpha = fade;
    for (let i = 0; i < 3; i++) {
      const dir = i === 1 ? 0 : (i === 0 ? -1 : 1), u = (lt * 1.3 + i * 0.33) % 1;
      const px = x + dir * (50 + 80 * u) + (i === 1 ? 0 : 0), py = y + 20 + 40 * u + 260 * u * u;
      c.fillStyle = '#7fd0ff'; c.strokeStyle = '#2b7bb9'; c.lineWidth = 4;
      c.beginPath(); c.moveTo(px, py - 20); c.quadraticCurveTo(px + 14, py + 4, px, py + 12); c.quadraticCurveTo(px - 14, py + 4, px, py - 20); c.fill(); c.stroke();
    }
    c.restore();
  },
  stars: (c, x, y, lt, d) => {
    const fade = clamp((d - lt) / 0.25, 0, 1), k = ease('back', lt / 0.25);
    c.save(); c.globalAlpha = fade; c.fillStyle = '#ffd400'; c.strokeStyle = OUT; c.lineWidth = 4;
    for (let i = 0; i < 5; i++) {
      const a = lt * 5 + i * Math.PI * 2 / 5;
      star(c, x + Math.cos(a) * 80 * k, y - 20 + Math.sin(a) * 20, 18 * k); c.fill(); c.stroke();
    }
    c.restore();
  },
  sparks: (c, x, y, lt, d, seed) => {
    const r = rng(seed), life = Math.min(d, 0.7);
    if (lt > life) return;
    c.save(); c.lineCap = 'round';
    for (let i = 0; i < 16; i++) {
      const a = -Math.PI * (0.1 + 0.8 * r()), sp = 260 + 520 * r();
      const px = x + Math.cos(a) * sp * lt, py = y + Math.sin(a) * sp * lt + 0.5 * 1800 * lt * lt;
      const fade = 1 - lt / life;
      c.globalAlpha = fade; c.strokeStyle = r() > 0.5 ? '#ffb020' : '#fff2a0'; c.lineWidth = 6 * fade + 2;
      c.beginPath(); c.moveTo(px, py); c.lineTo(px - Math.cos(a) * 16, py - Math.sin(a) * 16 - 4); c.stroke();
    }
    c.restore();
  },
  dust: (c, x, y, lt, d, seed) => {
    const r = rng(seed), life = Math.min(d, 0.9);
    if (lt > life) return;
    c.save();
    for (let i = 0; i < 7; i++) {
      const dir = (i % 2 ? 1 : -1), sp = 40 + 90 * r(), u = lt / life;
      c.globalAlpha = 0.55 * (1 - u);
      c.fillStyle = '#e9e2d3';
      c.beginPath(); c.arc(x + dir * sp * u * (1 + i * 0.12), y - 10 - 36 * u * r() - 6, 18 + 36 * u * (0.5 + r() * 0.5), 0, Math.PI * 2); c.fill();
    }
    c.restore();
  },
  hair_sprout: (c, x, y, lt, d) => {
    const u = clamp(lt / 0.72, 0, 1);
    const grow = ease('back', u);
    const fade = clamp((d - lt) / 0.22, 0, 1);
    const x0 = x + 4, y0 = y - 72;
    const x1 = x + 24 * grow, y1 = y - 132 * grow;
    const cx = x + 32 * grow, cy = y - 112 * grow;
    const endT = grow;
    const ex = (1-endT)*(1-endT)*x0 + 2*(1-endT)*endT*cx + endT*endT*x1;
    const ey = (1-endT)*(1-endT)*y0 + 2*(1-endT)*endT*cy + endT*endT*y1;
    c.save(); c.globalAlpha = fade; c.lineCap = 'round'; c.lineJoin = 'round';
    if (lt < 0.32) {
      const k = 1 - lt / 0.32;
      c.strokeStyle = '#fff2a6'; c.lineWidth = 5;
      for (let i = 0; i < 5; i++) {
        const a = i * Math.PI * 2 / 5 - Math.PI / 2;
        c.beginPath(); c.moveTo(x0 + Math.cos(a)*10, y0 + Math.sin(a)*10);
        c.lineTo(x0 + Math.cos(a)*(10+22*k), y0 + Math.sin(a)*(10+22*k)); c.stroke();
      }
    }
    c.beginPath(); c.moveTo(x0,y0); c.quadraticCurveTo(cx,cy,ex,ey);
    c.strokeStyle = OUT; c.lineWidth = 13; c.stroke();
    c.beginPath(); c.moveTo(x0,y0); c.quadraticCurveTo(cx,cy,ex,ey);
    c.strokeStyle = '#d8dce2'; c.lineWidth = 7; c.stroke();
    c.beginPath(); c.arc(x0,y0,5+3*Math.sin(lt*18),0,Math.PI*2); c.fillStyle='#f7f7f7'; c.fill();
    c.restore();
  },
  boom: (c, x, y, lt, d) => {
    const u = clamp(lt / 0.35, 0, 1), k = ease('back', u), fade = clamp((d - lt) / 0.15, 0, 1);
    c.save(); c.translate(x, y); c.rotate(lt * 0.4); c.globalAlpha = fade;
    const R = 120 * k;
    c.beginPath();
    for (let i = 0; i < 16; i++) { const a = i * Math.PI / 8, rad_ = i % 2 ? R * 0.55 : R; c.lineTo(Math.cos(a) * rad_, Math.sin(a) * rad_); }
    c.closePath(); c.fillStyle = '#ffe14d'; c.strokeStyle = OUT; c.lineWidth = 8; c.lineJoin = 'round'; c.fill(); c.stroke();
    c.beginPath(); c.arc(0, 0, R * 0.32, 0, Math.PI * 2); c.fillStyle = '#ff6a3d'; c.fill();
    c.restore();
  },
  confetti: (c, x, y, lt, d, seed) => {
    const r = rng(seed), cols = ['#ff4d6d', '#ffd23f', '#3bceac', '#4d9de0', '#b56bff'];
    c.save();
    for (let i = 0; i < 60; i++) {
      const px = r() * W, vy = 280 + r() * 380, ph = r() * 6, delay = r() * 0.5;
      const tt = lt - delay; if (tt < 0) continue;
      const py = -60 + vy * tt;
      c.globalAlpha = clamp((d - lt) / 0.4, 0, 1);
      c.save(); c.translate(px + Math.sin(tt * 3 + ph) * 40, py); c.rotate(tt * 6 + ph);
      c.fillStyle = cols[i % cols.length]; c.fillRect(-9, -5, 18, 10); c.restore();
    }
    c.restore();
  },
  flash: (c, x, y, lt, d) => {
    c.save(); c.globalAlpha = clamp(1 - lt / Math.min(d, 0.25), 0, 1) * 0.9; c.fillStyle = '#fff'; c.fillRect(0, 0, W, H); c.restore();
  }
};
const FX_SCREEN = { confetti: 1, flash: 1 };
const FX_KINDS = Object.keys(FX);
function bubble(c, x, y, lt, d, ch, col) {
  const k = ease('back', lt / 0.25), fade = clamp((d - lt) / 0.2, 0, 1);
  c.save(); c.translate(x + 30, y - 40); c.scale(k, k); c.rotate(Math.sin(lt * 18) * 0.06); c.globalAlpha = fade;
  c.font = '900 170px "Arial Black", Impact, sans-serif'; c.textAlign = 'center'; c.textBaseline = 'middle';
  c.lineJoin = 'round'; c.lineWidth = 22; c.strokeStyle = OUT; c.strokeText(ch, 0, 0);
  c.lineWidth = 10; c.strokeStyle = '#fff'; c.strokeText(ch, 0, 0);
  c.fillStyle = col; c.fillText(ch, 0, 0);
  c.restore();
}

// ───────────────────────── движок ─────────────────────────
class Engine {
  constructor(canvas) {
    this.canvas = canvas || null;
    this.ctx = canvas ? canvas.getContext('2d') : null;
    this.q = 1;
    this.lib = { locations: {}, props: {}, characters: {} };
    this.texts = { lang: '', cps: 14, lines: {} };
    this.flags = { subs: true, titles: true, safe: false };
    this.C = null;
    this.missing = new Set();
  }
  setQuality(q) { this.q = q; if (this.canvas) { this.canvas.width = Math.round(W * q); this.canvas.height = Math.round(H * q); } }
  setLibrary(lib) { this.lib = { locations: (lib && lib.locations) || {}, props: (lib && lib.props) || {}, characters: (lib && lib.characters) || {} }; }
  setTexts(tx) { this.texts = Object.assign({ lang: '', cps: 14, lines: {} }, tx || {}); this.texts.lines = (tx && tx.lines) || {}; this.missing.clear(); }
  T(key) {
    const v = this.texts.lines[key];
    if (typeof v === 'string') return v;
    this.missing.add(key);
    return `⟦${key}⟧`;
  }

  // ───── компиляция сцены ─────
  load(scene) {
    const rep = { errors: [], warnings: [], info: {} };
    const err = m => rep.errors.push(m), warn = m => rep.warnings.push(m);
    this.C = null;
    if (!scene || typeof scene !== 'object' || Array.isArray(scene)) { err('Сцена: ожидался JSON-объект'); return rep; }
    const beats = scene.beats;
    if (!Array.isArray(beats)) { err('Сцена: нет массива "beats"'); return rep; }

    const defs = scene.defs || {};
    const locs = Object.assign({}, this.lib.locations, defs.locations || {});
    const propDefs = Object.assign({}, this.lib.props, defs.props || {});
    for (const k in locs) {
      const L = locs[k];
      if (!L || !Array.isArray(L.layers)) { err(`Локация "${k}": нужен массив layers`); continue; }
      L.layers.forEach((ly, i) => validateShapes(ly.shapes, `Локация "${k}" → layers[${i}]`, err));
    }
    for (const k in propDefs) {
      const p = propDefs[k];
      if (!p || !Array.isArray(p.shapes)) { err(`Предмет "${k}": нужен массив shapes`); continue; }
      validateShapes(p.shapes, `Предмет "${k}"`, err);
    }

    const charTypes = Object.assign({}, this.lib.characters || {}, defs.characters || {});
    for (const k in charTypes) {
      const d = charTypes[k];
      if (!d || typeof d !== 'object') { err(`Тип персонажа "${k}": ожидался объект`); continue; }
      for (const part of ['torso', 'head_back', 'head_front']) if (d[part] != null) validateShapes(d[part], `Тип персонажа "${k}" → ${part}`, err);
    }

    const start = scene.start || {};
    const C = {
      locs, propDefs, chars: {}, props: {}, camSegs: [], shakes: [], fx: [], titles: [], callouts: [], locEv: [], says: [], markers: [],
      cam0: Object.assign({ x: 540, y: 960, zoom: 1, rot: 0 }, start.camera || {}), beatsFlat: []
    };
    const defaultStart = { eng: { x: 300, face: 'right' }, bld: { x: 780, face: 'left' } };
    const startChars = start.chars && typeof start.chars === 'object' && !Array.isArray(start.chars) ? start.chars : null;
    const charIds = [...new Set([...CHAR_IDS, ...(startChars ? Object.keys(startChars) : [])])];
    for (const id of charIds) {
      const s = startChars ? (id in startChars ? startChars[id] : null) : (defaultStart[id] || null);
      const inst = s && typeof s === 'object' ? s : {};
      const type = inst.type || (CHARS[id] ? id : 'extra');
      C.chars[id] = {
        id, def: resolveCharDef(type, inst, charTypes, err, id),
        x0: s && isNum(s.x) ? s.x : (defaultStart[id] ? defaultStart[id].x : 540), vis: [{ t: 0, v: !!s && !inst.hidden }],
        face: [{ t: 0, v: s && s.face === 'left' ? -1 : 1 }], segs: [], cum: 0, poses: [], emos: [], says: [], holds: [], seed: hashStr(id) % 100
      };
    }
    const locStart = start.location || (scene.location);
    if (!locStart) err('Сцена: не указана стартовая локация (start.location)');
    else if (!locs[locStart]) err(`Стартовая локация "${locStart}" не найдена (ни в library.json, ни в defs.locations)`);
    C.locEv.push({ t: 0, id: locStart, transition: 'cut', dur: 0 });

    const sorted = beats.map((b, i) => ({ b, i })).filter(o => o.b && typeof o.b === 'object')
      .sort((a, c) => (a.b.t - c.b.t) || (a.i - c.i));
    beats.forEach((b, i) => { if (!b || typeof b !== 'object') err(`beats[${i}]: ожидался объект`); });

    const eng = this;
    const resolveId = v => {
      const raw = String(v);
      if (C.chars[raw]) return raw;
      const a = ALIASES[raw.toLowerCase()];
      return a && C.chars[a] ? a : null;
    };
    const who = (b, i, key = 'who') => {
      const id = resolveId(b[key]);
      if (!id) { err(`beats[${i}] (${b.do}): неизвестный персонаж "${b[key]}" (есть: ${Object.keys(C.chars).join(', ')})`); return null; }
      return id;
    };

    for (const { b, i } of sorted) {
      const tag = `beats[${i}] (${b.do})`;
      if (!isNum(b.t) || b.t < 0) { err(`${tag}: "t" должно быть числом ≥ 0`); continue; }
      const t = b.t;
      const needDur = () => { if (!isNum(b.dur) || b.dur <= 0) { err(`${tag}: "dur" должно быть числом > 0`); return false; } return true; };
      C.beatsFlat.push({ t, do: b.do, who: b.who });
      switch (b.do) {
        case 'place': {
          const id = who(b, i); if (!id) break;
          if (!isNum(b.x)) { err(`${tag}: нужен x`); break; }
          const ch = C.chars[id];
          ch.segs.push({ t0: t, t1: t, x0: b.x, x1: b.x, ease: 'linear', moving: false });
          ch.vis.push({ t, v: true });
          if (b.face) ch.face.push({ t, v: b.face === 'left' ? -1 : 1 });
          break;
        }
        case 'show': case 'hide': {
          const id = who(b, i); if (!id) break;
          C.chars[id].vis.push({ t, v: b.do === 'show' });
          break;
        }
        case 'walk': {
          const id = who(b, i); if (!id) break;
          if (!isNum(b.x)) { err(`${tag}: нужен x`); break; }
          const ch = C.chars[id];
          const x0 = eng._posAt(ch, t);
          const dur = isNum(b.dur) && b.dur > 0 ? b.dur : Math.max(0.3, Math.abs(b.x - x0) / 220);
          const last = ch.segs[ch.segs.length - 1];
          if (last && last.t1 > t) { last.x1 = x0; last.t1 = t; last.moving = Math.abs(last.x1 - last.x0) > 0.5 && last.t1 > last.t0; }
          ch.segs.push({ t0: t, t1: t + dur, x0, x1: b.x, ease: b.ease || 'soft', moving: Math.abs(b.x - x0) > 0.5 });
          if (b.face !== 'keep' && Math.abs(b.x - x0) > 0.5) ch.face.push({ t, v: b.x > x0 ? 1 : -1 });
          if (b.face === 'left' || b.face === 'right') ch.face.push({ t: t + dur, v: b.face === 'left' ? -1 : 1 });
          const sp = Math.abs(b.x - x0) / dur;
          if (sp > 520) warn(`${tag}: очень быстрый бег (${Math.round(sp)} px/с) — увеличьте dur`);
          break;
        }
        case 'face': {
          const id = who(b, i); if (!id) break;
          const ch = C.chars[id];
          let v;
          if (b.dir === 'left') v = -1; else if (b.dir === 'right') v = 1;
          else if (resolveId(b.dir)) { const o = C.chars[resolveId(b.dir)]; v = eng._posAt(o, t) >= eng._posAt(ch, t) ? 1 : -1; }
          else { err(`${tag}: dir = left | right | id персонажа (${Object.keys(C.chars).join(', ')})`); break; }
          ch.face.push({ t, v });
          break;
        }
        case 'pose': {
          const id = who(b, i); if (!id) break;
          if (!POSES[b.pose]) { err(`${tag}: неизвестная поза "${b.pose}" (есть: ${POSE_NAMES.join(', ')})`); break; }
          const ch = C.chars[id];
          ch.poses.push({ t, name: b.pose, auto: false });
          if (isNum(b.dur) && b.dur > 0) ch.poses.push({ t: t + b.dur, name: 'idle', auto: true, src: t });
          break;
        }
        case 'emote': {
          const id = who(b, i); if (!id) break;
          if (!EMOS[b.emotion]) { err(`${tag}: неизвестная эмоция "${b.emotion}" (есть: ${EMO_NAMES.join(', ')})`); break; }
          const ch = C.chars[id];
          ch.emos.push({ t, name: b.emotion, auto: false });
          if (isNum(b.dur) && b.dur > 0) ch.emos.push({ t: t + b.dur, name: 'neutral', auto: true, src: t });
          break;
        }
        case 'say': {
          const id = who(b, i); if (!id) break;
          if (typeof b.line !== 'string') { err(`${tag}: нужен "line" (id реплики, не текст)`); break; }
          if (!needDur()) break;
          C.chars[id].says.push({ t0: t, t1: t + b.dur, line: b.line });
          C.says.push({ t0: t, t1: t + b.dur, line: b.line, who: id });
          break;
        }
        case 'spawn': {
          if (typeof b.id !== 'string') { err(`${tag}: нужен id экземпляра`); break; }
          if (!propDefs[b.prop]) { err(`${tag}: предмет "${b.prop}" не найден (library.json или defs.props)`); break; }
          if (!isNum(b.x)) { err(`${tag}: нужен x`); break; }
          const floor = isNum(b.y) ? b.y : GROUND + 4;
          C.props[b.id] = { id: b.id, def: propDefs[b.prop], floor, layer: b.layer === 'front' ? 'front' : 'back', ev: [{ type: 'spawn', t, x: b.x, y: floor, rot: b.rot || 0, scale: isNum(b.scale) ? b.scale : 1 }] };
          break;
        }
        case 'move': case 'remove': case 'hold': case 'release': {
          const P = C.props[b.id];
          if (!P) { err(`${tag}: предмет "${b.id}" не создан (нужен spawn раньше)`); break; }
          if (b.do === 'remove') P.ev.push({ type: 'remove', t });
          else if (b.do === 'move') {
            if (!needDur()) break;
            P.ev.push({ type: 'move', t, t1: t + b.dur, x: isNum(b.x) ? b.x : null, y: isNum(b.y) ? b.y : null, arc: b.arc || 0, ease: b.ease || 'easeInOut', rot: isNum(b.rot) ? b.rot : null });
          } else if (b.do === 'hold') {
            const id = who(b, i); if (!id) break;
            const hand = b.hand === 'L' ? 'L' : 'R';
            P.ev.push({ type: 'hold', t, who: id, hand });
            C.chars[id].holds.push({ t, id: b.id, hand });
          } else {
            const hold = P.ev.slice().reverse().find(e => e.type === 'hold' && e.t <= t);
            if (!hold) { warn(`${tag}: предмет "${b.id}" не держали`); break; }
            P.ev.push({ type: 'release', t, drop: b.drop !== false, who: hold.who, hand: hold.hand });
            C.chars[hold.who].holds.push({ t, id: null, hand: hold.hand });
          }
          break;
        }
        case 'location': {
          if (!locs[b.id]) { err(`${tag}: локация "${b.id}" не найдена`); break; }
          C.locEv.push({ t, id: b.id, transition: b.transition || 'fade', dur: isNum(b.dur) ? b.dur : 0.5 });
          break;
        }
        case 'camera': {
          const seg = { t0: t, t1: t + (isNum(b.dur) ? b.dur : 0.6), ease: b.ease || 'easeInOut', reset: !!b.reset, on: b.on || null, focus: b.focus || 'body', follow: !!b.follow, zoom: b.zoom, x: b.x, y: b.y, dx: b.dx || 0, dy: b.dy || 0, rot: b.rot };
          if (seg.on && seg.on !== 'both' && !resolveId(seg.on)) { err(`${tag}: on = id персонажа (${Object.keys(C.chars).join(', ')}) или both`); break; }
          if (seg.on && seg.on !== 'both') seg.on = resolveId(seg.on);
          C.camSegs.push(seg);
          break;
        }
        case 'shake': if (needDur()) C.shakes.push({ t0: t, t1: t + b.dur, amp: isNum(b.amp) ? b.amp : 14 }); break;
        case 'fx': {
          if (!FX[b.kind]) { err(`${tag}: неизвестный эффект "${b.kind}" (есть: ${FX_KINDS.join(', ')})`); break; }
          let on = null;
          if (b.on) { on = resolveId(b.on); if (!on) { err(`${tag}: on = id персонажа (${Object.keys(C.chars).join(', ')})`); break; } }
          C.fx.push({ t0: t, dur: isNum(b.dur) ? b.dur : 1, kind: b.kind, on, anchor: b.anchor || 'head', x: b.x, y: b.y, seed: hashStr(b.kind + t) });
          break;
        }
        case 'title': {
          if (typeof b.key !== 'string') { err(`${tag}: нужен key (id текста, не сам текст)`); break; }
          if (!needDur()) break;
          C.titles.push({ t0: t, t1: t + b.dur, key: b.key, pos: b.pos || 'top', style: b.style || 'pop', color: b.color || '#fff' });
          break;
        }
        case 'callout': {
          // акцентная надпись рядом с героем: только для самых эмоциональных моментов
          const id = who(b, i, 'on'); if (!id) break;
          if (typeof b.key !== 'string') { err(`${tag}: нужен key (id текста, не сам текст)`); break; }
          if (!needDur()) break;
          if (b.style != null && !CALLOUT_STYLES.includes(b.style)) { err(`${tag}: style = ${CALLOUT_STYLES.join(' | ')}`); break; }
          if (b.side != null && !['left', 'right', 'auto'].includes(b.side)) { err(`${tag}: side = left | right | auto`); break; }
          C.callouts.push({ t0: t, t1: t + b.dur, on: id, key: b.key, style: b.style || 'pop', color: b.color || '#ffd400', side: b.side || 'auto', size: isNum(b.size) ? b.size : 84 });
          break;
        }
        case 'marker': case 'sfx': C.markers.push({ t, name: b.name || b.do }); break;
        default: err(`${tag}: неизвестное действие "${b.do}"`);
      }
    }

    // авто-возвраты в idle/neutral отменяются, если между ними была другая явная команда
    for (const id of Object.keys(C.chars)) {
      const ch = C.chars[id];
      for (const k of ['poses', 'emos']) {
        const arr = ch[k];
        const keep = arr.filter(e => !(e.auto && arr.some(o => !o.auto && o.t > e.src && o.t <= e.t)));
        keep.sort((a, c) => a.t - c.t);
        ch[k] = keep;
      }
      ch.face.sort((a, c) => a.t - c.t); ch.vis.sort((a, c) => a.t - c.t); ch.holds.sort((a, c) => a.t - c.t);
      ch.segs.sort((a, c) => a.t0 - c.t0);
      // кумулятивная дистанция для ходьбы без скольжения ног
      let cum = 0; for (const s of ch.segs) { s.d0 = cum; if (s.moving) cum += Math.abs(s.x1 - s.x0); }
    }
    C.locEv.sort((a, c) => a.t - c.t);
    C.camSegs.sort((a, c) => a.t0 - c.t0);
    for (const k in C.props) C.props[k].ev.sort((a, c) => a.t - c.t);
    C.says.sort((a, c) => a.t0 - c.t0);

    C.callouts.sort((a, c) => a.t0 - c.t0);
    if (C.callouts.length > 2) warn(`Акцентов (callout) в сцене ${C.callouts.length}: этот приём работает, пока он редкий. Оставьте 1–2 самых эмоциональных момента`);
    for (let k = 1; k < C.callouts.length; k++) {
      if (C.callouts[k].t0 < C.callouts[k - 1].t1) warn(`Акценты "${C.callouts[k - 1].key}" и "${C.callouts[k].key}" одновременно на экране`);
    }

    let maxEnd = 0;
    for (const s of C.says) maxEnd = Math.max(maxEnd, s.t1);
    for (const o of beats) if (o && isNum(o.t)) maxEnd = Math.max(maxEnd, o.t + (isNum(o.dur) ? o.dur : 0));
    C.dur = isNum(scene.duration) && scene.duration > 0 ? scene.duration : maxEnd + 0.5;
    if (maxEnd > C.dur + 0.01) warn(`Действия заходят за duration (${C.dur}с): последнее заканчивается на ${maxEnd.toFixed(1)}с`);

    // проверка реплик: пересечения и «влезает ли текст в слот»
    for (let k = 1; k < C.says.length; k++) {
      if (C.says[k].t0 < C.says[k - 1].t1 - 0.05) warn(`Реплики "${C.says[k - 1].line}" и "${C.says[k].line}" пересекаются по времени`);
    }
    const cps = this.texts.cps || 14;
    rep.info.says = C.says.map(s => {
      const txt = this.texts.lines[s.line];
      const slot = s.t1 - s.t0;
      const need = typeof txt === 'string' ? txt.replace(/\s+/g, ' ').length / cps : null;
      if (txt == null) warn(`Нет текста для реплики "${s.line}" в языке "${this.texts.lang || '?'}"`);
      else if (need > slot * 1.05) warn(`Реплика "${s.line}": ≈${need.toFixed(1)}с речи на слот ${slot.toFixed(1)}с — сократите или увеличьте dur`);
      return { line: s.line, who: s.who, t0: s.t0, t1: s.t1, need, text: txt };
    });
    for (const k of new Set([...C.titles.map(x => x.key), ...C.callouts.map(x => x.key)])) if (this.texts.lines[k] == null) warn(`Нет текста для титра/акцента "${k}" в языке "${this.texts.lang || '?'}"`);
    rep.info.callouts = C.callouts;
    rep.info.duration = C.dur;
    rep.info.markers = C.markers;
    rep.info.beats = C.beatsFlat;
    rep.info.titles = C.titles;
    rep.info.cps = cps;

    this.C = C;
    this.scene = scene;
    this._camCache = new WeakMap();
    return rep;
  }

  // ───── сэмплеры треков ─────
  _posAt(ch, t) {
    let x = ch.x0;
    for (const s of ch.segs) {
      if (s.t0 > t) break;
      if (t >= s.t1) { x = s.x1; continue; }
      x = lerp(s.x0, s.x1, ease(s.ease, (t - s.t0) / (s.t1 - s.t0)));
      break;
    }
    return x;
  }
  _distAt(ch, t) {
    let d = 0;
    for (const s of ch.segs) {
      if (s.t0 > t) break;
      if (!s.moving) continue;
      if (t >= s.t1) d = s.d0 + Math.abs(s.x1 - s.x0);
      else { d = s.d0 + Math.abs(this._posAt(ch, t) - s.x0); break; }
    }
    return d;
  }
  _poseAt(ch, t, depth = 0) {
    const ev = ch.poses;
    let i = -1;
    for (let k = 0; k < ev.length; k++) { if (ev[k].t <= t) i = k; else break; }
    if (i < 0) return evalPose('idle', t, t);
    const e = ev[i], lt = t - e.t;
    const cur = evalPose(e.name, lt, t);
    const BL = 0.35;
    if (lt < BL && depth < 4) {
      const prev = this._poseAt(ch, e.t - 1e-4, depth + 1);
      const f = EASE.backSoft(lt / BL);
      const m = mixObj(prev, cur, f); m._name = e.name; return m;
    }
    return cur;
  }
  _emoAt(ch, t, depth = 0) {
    const ev = ch.emos;
    let i = -1;
    for (let k = 0; k < ev.length; k++) { if (ev[k].t <= t) i = k; else break; }
    if (i < 0) return Object.assign({}, EMOS.neutral);
    const e = ev[i], lt = t - e.t, cur = EMOS[e.name], BL = 0.22;
    if (lt < BL && depth < 4) {
      const prev = this._emoAt(ch, e.t - 1e-4, depth + 1);
      return mixObj(prev, cur, EASE.back(lt / BL));
    }
    return Object.assign({}, cur);
  }

  charState(id, t) {
    const C = this.C, ch = C.chars[id], def = ch.def;
    const vis = lastBefore(ch.vis, t).v;
    const x = this._posAt(ch, t);
    const face = lastBefore(ch.face, t).v;
    let seg = null;
    for (const s of ch.segs) if (s.moving && s.t0 <= t && t < s.t1) { seg = s; break; }
    let speed = 0, wk = 0;
    if (seg) { speed = Math.abs(seg.x1 - seg.x0) / (seg.t1 - seg.t0); wk = clamp(Math.min((t - seg.t0) / 0.12, (seg.t1 - t) / 0.12), 0, 1); }
    const dist = this._distAt(ch, t);
    const pose = this._poseAt(ch, t);
    const emo = this._emoAt(ch, t);
    let say = null;
    for (const s of ch.says) if (s.t0 <= t && t < s.t1) { say = s; break; }

    const run = clamp((speed - 230) / 180, 0, 1);
    const phase = dist / (46 - 10 * run) * Math.PI;
    const A = (34 + 30 * run) * wk;
    const sw = Math.sin(phase) * A;
    const liftK = 18 * wk * (1 + run * .6);
    const legs = {
      L: { x: -34 + sw, lift: Math.max(0, Math.cos(phase)) * liftK },
      R: { x: 34 - sw, lift: Math.max(0, -Math.cos(phase)) * liftK }
    };
    let L = pose.L.slice(), R = pose.R.slice();
    let head = pose.head, lean = pose.lean + wk * (3 + 9 * run);
    let by = pose.by + Math.abs(Math.sin(phase)) * 7 * wk;
    const idleish = pose._name === 'idle';
    if (idleish && wk > 0) {
      L[1] -= Math.sin(phase) * 14 * wk; R[1] += Math.sin(phase) * 14 * wk;
      L = [lerp(L[0], 46, run), lerp(L[1], 100, run)]; R = [lerp(R[0], 46, run), lerp(R[1], 100, run)];
    }
    // речь
    let mo = emo.mo;
    if (say) {
      const lt = t - say.t0;
      const open = (0.25 + 0.75 * Math.abs(Math.sin(lt * 12.4 + ch.seed))) * (0.6 + 0.4 * Math.abs(Math.sin(lt * 3.7 + ch.seed))) * 26;
      mo = Math.max(mo, open);
      head += Math.sin(lt * 9 + ch.seed) * 2.2;
      if (idleish && wk === 0) {
        const g1 = Math.max(0, Math.sin(lt * 1.9 + ch.seed)), g2 = Math.max(0, Math.sin(lt * 1.5 + ch.seed * 0.7 + 2));
        R = [24 + 34 * g1, 164 - 100 * g1]; L = [24 + 30 * g2, 164 - 90 * g2];
      }
    }
    return { vis, x, y: 0, face, legs, L, R, head, lean, by, air: pose.air, sq: pose.sq, emo, mo, wk, run, say, def, id };
  }

  // кисть в мировых координатах (для падения/удержания предметов и камеры)
  _bodyGeo(st) {
    const def = st.def;
    const upper = st.by;
    const hipY = HIP_Y + upper;
    const sxn = def.tw / 2 - 8;
    return { hipY, sxn, def };
  }
  handWorld(id, t, hand) {
    const st = this.charState(id, t);
    return this._handWorldSt(st, hand);
  }
  _handWorldSt(st, hand) {
    const g = this._bodyGeo(st), side = hand === 'L' ? -1 : 1;
    const tgt = hand === 'L' ? st.L : st.R;
    const sx = side * g.sxn, sy = SHOULDER_Y;
    const r = ik(sx, sy, sx + side * tgt[0], sy + tgt[1], UARM, FARM, side, 0.8, 0.6);
    return { ...this._hipToWorld(st, g, r.hx, r.hy), ik: r, g };
  }
  _hipToWorld(st, g, px, py) {
    const a = rad(st.lean), c = Math.cos(a), s = Math.sin(a);
    const rx = px * c - py * s, ry = px * s + py * c;
    const fx = rx, fy = g.hipY + ry + st.air;
    const sx = st.face * 1 / Math.sqrt(st.sq), sy = st.def.sy * st.sq;
    return { x: st.x + fx * sx, y: GROUND + st.y + fy * sy };
  }

  // ───── камера ─────
  _camTarget(seg, from, tt) {
    const to = { x: from.x, y: from.y, zoom: from.zoom, rot: from.rot };
    if (seg.reset) { to.x = 540; to.y = 960; to.zoom = 1; to.rot = 0; }
    if (isNum(seg.zoom)) to.zoom = seg.zoom;
    if (isNum(seg.rot)) to.rot = seg.rot;
    if (seg.on) {
      const FY = { head: 430, face: 445, body: 260, feet: 90 };
      if (seg.on === 'both') {
        // середина между крайними видимыми героями (для двух — ровно их среднее)
        const xs = [];
        for (const cid in this.C.chars) { const s = this.charState(cid, tt); if (s.vis) xs.push(s.x); }
        if (xs.length) to.x = (Math.min(...xs) + Math.max(...xs)) / 2;
        to.y = GROUND - 300;
      } else {
        const s = this.charState(seg.on, tt);
        to.x = s.x; to.y = GROUND - (FY[seg.focus] || 260) * s.def.sy;
      }
    }
    if (isNum(seg.x)) to.x = seg.x;
    if (isNum(seg.y)) to.y = seg.y;
    to.x += seg.dx; to.y += seg.dy;
    return to;
  }
  camAt(t) {
    const C = this.C;
    let st = Object.assign({}, C.cam0);
    for (const seg of C.camSegs) {
      if (seg.t0 > t) break;
      let from = this._camCache.get(seg);
      if (!from) { from = Object.assign({}, st); this._camCache.set(seg, from); }
      const tt = seg.follow ? Math.min(t, 1e9) : seg.t1;
      const to = this._camTarget(seg, from, tt);
      if (t >= seg.t1) { st = to; continue; }
      const k = ease(seg.ease, (t - seg.t0) / (seg.t1 - seg.t0));
      st = { x: lerp(from.x, to.x, k), y: lerp(from.y, to.y, k), zoom: lerp(from.zoom, to.zoom, k), rot: lerp(from.rot, to.rot, k) };
      break;
    }
    const hw = W / 2 / st.zoom, hh = H / 2 / st.zoom;
    st.x = clamp(st.x, hw, W - hw); st.y = clamp(st.y, hh, H - hh);
    return st;
  }

  // ───── предметы ─────
  propState(P, t) {
    let pos = null, rot = 0, scale = 1, vis = false, held = null, floor = P.floor;
    for (let i = 0; i < P.ev.length; i++) {
      const e = P.ev[i];
      if (e.t > t) break;
      switch (e.type) {
        case 'spawn': pos = { x: e.x, y: e.y }; rot = e.rot; scale = e.scale; vis = true; held = null; break;
        case 'remove': vis = false; break;
        case 'hold': held = { who: e.who, hand: e.hand }; break;
        case 'release': {
          const hw = this.handWorld(e.who, e.t, e.hand);
          held = null;
          if (e.drop) {
            const dt = t - e.t, y0 = hw.y, fl = Math.max(floor, y0), G = 3200;
            const tl = Math.sqrt(2 * (fl - y0) / G);
            let y;
            if (dt < tl) y = y0 + 0.5 * G * dt * dt;
            else { const u = clamp((dt - tl) / 0.26, 0, 1), hb = Math.min(50, (fl - y0) * 0.12); y = fl - 4 * hb * u * (1 - u); }
            pos = { x: hw.x, y, free: false };
            rot = 0;
          } else pos = { x: hw.x, y: hw.y };
          break;
        }
        case 'move': {
          if (!pos) break;
          const tx = e.x == null ? pos.x : e.x, ty = e.y == null ? pos.y : e.y;
          if (t >= e.t1) { pos = { x: tx, y: ty }; if (e.rot != null) rot = e.rot; }
          else {
            const k = ease(e.ease, (t - e.t) / (e.t1 - e.t));
            pos = { x: lerp(pos.x, tx, k), y: lerp(pos.y, ty, k) - Math.sin(Math.PI * k) * e.arc };
            if (e.rot != null) rot = lerp(rot, e.rot, k);
            return { vis, pos, rot, scale, held, floor };
          }
          break;
        }
      }
    }
    return { vis, pos, rot, scale, held, floor };
  }
  _drawProp(ctx, P, t, scale, grip) {
    const g = P.def.grip || [0, 0];
    ctx.save();
    ctx.scale((P.def.scale || 1) * scale, (P.def.scale || 1) * scale);
    ctx.translate(-g[0], -g[1]);
    drawShapes(ctx, P.def.shapes, t, k => this.T(k));
    ctx.restore();
  }

  // ───── отрисовка ─────
  render(t, opts = {}) {
    const ctx = this.ctx, C = this.C;
    if (!ctx || !C) return;
    const q = this.q;
    this._t = t;
    ctx.setTransform(q, 0, 0, q, 0, 0);
    ctx.clearRect(0, 0, W, H);
    ctx.fillStyle = '#000'; ctx.fillRect(0, 0, W, H);
    const cam = this.camAt(t);
    let sx = 0, sy = 0;
    for (const s of C.shakes) if (t >= s.t0 && t < s.t1) {
      const k = 1 - (t - s.t0) / (s.t1 - s.t0);
      sx += s.amp * k * noise(t * 55); sy += s.amp * k * noise(t * 49 + 3);
    }
    const locEv = lastBefore(C.locEv, t);
    const loc = C.locs[locEv.id];
    const T = k => this.T(k);

    const withCam = (p, fn) => {
      ctx.save();
      const zl = 1 + (cam.zoom - 1) * p, cx = 540 + (cam.x - 540) * p, cy = 960 + (cam.y - 960) * p;
      ctx.translate(W / 2 + sx * p, H / 2 + sy * p);
      if (cam.rot) ctx.rotate(rad(cam.rot) * Math.max(p, 0.0));
      ctx.scale(zl, zl); ctx.translate(-cx, -cy);
      fn(); ctx.restore();
    };

    if (loc) for (const ly of loc.layers) if (ly.z !== 'front') withCam(ly.p == null ? 1 : ly.p, () => drawShapes(ctx, ly.shapes, t, T));

    withCam(1, () => {
      // предметы сзади
      const props = Object.values(C.props);
      for (const P of props) {
        if (P.layer !== 'back') continue;
        const s = this.propState(P, t);
        if (!s.vis || s.held || !s.pos) continue;
        ctx.save(); ctx.translate(s.pos.x, s.pos.y); ctx.rotate(rad(s.rot)); this._drawProp(ctx, P, t, s.scale); ctx.restore();
      }
      // герои (по x, чтобы перекрытие было естественным)
      const ids = Object.keys(C.chars).sort((a, b) => this._posAt(C.chars[a], t) - this._posAt(C.chars[b], t));
      for (const id of ids) {
        const st = this.charState(id, t);
        if (st.vis) this._drawChar(ctx, st, t);
      }
      for (const P of props) {
        if (P.layer !== 'front') continue;
        const s = this.propState(P, t);
        if (!s.vis || s.held || !s.pos) continue;
        ctx.save(); ctx.translate(s.pos.x, s.pos.y); ctx.rotate(rad(s.rot)); this._drawProp(ctx, P, t, s.scale); ctx.restore();
      }
    });

    if (loc) for (const ly of loc.layers) if (ly.z === 'front') withCam(ly.p == null ? 1 : ly.p, () => drawShapes(ctx, ly.shapes, t, T));

    // эффекты
    withCam(1, () => {
      for (const f of C.fx) {
        const lt = t - f.t0;
        if (lt < 0 || lt > f.dur || FX_SCREEN[f.kind]) continue;
        const pt = this._fxPoint(f, t);
        FX[f.kind](ctx, pt.x, pt.y, lt, f.dur, f.seed);
      }
    });
    for (const f of C.fx) {
      const lt = t - f.t0;
      if (lt >= 0 && lt <= f.dur && FX_SCREEN[f.kind]) FX[f.kind](ctx, 0, 0, lt, f.dur, f.seed);
    }

    // акценты рядом с героем (выключаются вместе с титрами)
    if (this.flags.titles && C.callouts.length) {
      withCam(1, () => { for (const c of C.callouts) if (t >= c.t0 && t < c.t1) this._drawCallout(ctx, c, t, cam); });
    }

    // переход между локациями
    for (const e of C.locEv) {
      if (e.t === 0 || e.transition === 'cut' || !e.dur) continue;
      const half = e.dur / 2, d = t - e.t;
      if (Math.abs(d) >= half) continue;
      const k = 1 - Math.abs(d) / half;
      if (e.transition === 'fade') { ctx.fillStyle = `rgba(0,0,0,${k})`; ctx.fillRect(0, 0, W, H); }
      else if (e.transition === 'flash') { ctx.fillStyle = `rgba(255,255,255,${k})`; ctx.fillRect(0, 0, W, H); }
      else if (e.transition === 'wipe') {
        const u = (d + half) / e.dur; // 0..1 слева направо
        ctx.fillStyle = '#1e1b26';
        const x0 = u < 0.5 ? 0 : (u - 0.5) * 2 * W, x1 = u < 0.5 ? u * 2 * W : W;
        ctx.fillRect(x0, 0, x1 - x0, H);
      }
    }

    // титры (язык-зависимые, но привязаны к ключам)
    if (this.flags.titles) for (const ti of C.titles) {
      if (t < ti.t0 || t >= ti.t1) continue;
      this._drawTitle(ctx, ti, t);
    }
    // субтитры
    if (this.flags.subs) for (const s of C.says) {
      if (t >= s.t0 && t < s.t1) { this._drawSub(ctx, this.T(s.line)); break; }
    }
    if (this.flags.safe) this._drawSafe(ctx);
  }

  _fxPoint(f, t) {
    if (f.on) {
      const st = this.charState(f.on, t);
      const sy = st.def.sy;
      if (f.anchor === 'feet') return { x: st.x, y: GROUND };
      if (f.anchor === 'body') return { x: st.x, y: GROUND - 260 * sy };
      if (f.anchor === 'hand') { const h = this._handWorldSt(st, 'R'); return { x: h.x, y: h.y }; }
      return { x: st.x, y: GROUND + st.air - 545 * sy };
    }
    return { x: isNum(f.x) ? f.x : 540, y: isNum(f.y) ? f.y : 700 };
  }

  _wrap(ctx, text, maxW) {
    const words = String(text).split(/\s+/), lines = [];
    let cur = '';
    for (const w of words) {
      const test = cur ? cur + ' ' + w : w;
      if (ctx.measureText(test).width > maxW && cur) { lines.push(cur); cur = w; } else cur = test;
    }
    if (cur) lines.push(cur);
    return lines;
  }
  _drawSub(ctx, text) {
    ctx.save();
    ctx.font = '800 56px "Arial Black", Arial, sans-serif'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
    const lines = this._wrap(ctx, text, 860), lh = 70, y0 = 1470 - (lines.length - 1) * lh / 2;
    ctx.lineJoin = 'round';
    lines.forEach((ln, i) => {
      ctx.lineWidth = 14; ctx.strokeStyle = OUT; ctx.strokeText(ln, 500, y0 + i * lh);
      ctx.fillStyle = '#fff'; ctx.fillText(ln, 500, y0 + i * lh);
    });
    ctx.restore();
  }
  _drawTitle(ctx, ti, t) {
    const lt = t - ti.t0, d = ti.t1 - ti.t0, text = this.T(ti.key);
    ctx.save();
    const y = ti.pos === 'center' ? 820 : ti.pos === 'bottom' ? 1370 : 380;
    ctx.font = '900 92px "Arial Black", Impact, Arial, sans-serif'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
    const lines = this._wrap(ctx, text, 880), lh = 108;
    const fade = clamp(Math.min(lt / 0.12, (d - lt) / 0.2), 0, 1);
    ctx.globalAlpha = fade;
    ctx.translate(500, y);
    if (ti.style === 'slide') ctx.translate(0, (1 - ease('easeOut', lt / 0.35)) * 140);
    else { const k = ease('back', lt / 0.3); ctx.scale(k, k); }
    if (ti.style === 'shake') ctx.rotate(Math.sin(lt * 40) * 0.025);
    ctx.lineJoin = 'round';
    lines.forEach((ln, i) => {
      const yy = (i - (lines.length - 1) / 2) * lh;
      ctx.lineWidth = 24; ctx.strokeStyle = OUT; ctx.strokeText(ln, 0, yy);
      ctx.fillStyle = ti.color; ctx.fillText(ln, 0, yy);
    });
    ctx.restore();
  }
  _drawCallout(ctx, c, t, cam) {
    const st = this.charState(c.on, t);
    if (!st.vis) return;
    const lt = t - c.t0, d = c.t1 - c.t0, z = cam.zoom;
    const text = this.T(c.key);
    ctx.save();
    ctx.font = `900 ${c.size}px "Arial Black", Impact, Arial, sans-serif`;
    ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
    const lines = this._wrap(ctx, text, 540), lh = c.size * 1.08;
    let w = 0; for (const l of lines) w = Math.max(w, ctx.measureText(l).width);
    const h = lines.length * lh;
    // надпись рядом с головой, со стороны центра кадра; в видимой области и вне зон интерфейса TikTok
    const side = c.side === 'left' ? -1 : c.side === 'right' ? 1 : (st.x < cam.x ? 1 : -1);
    const headY = GROUND + st.air - 545 * st.def.sy;
    let x = st.x + side * (100 + w / 2), y = headY - 60;
    const hw = 540 / z, hh = 960 / z, m = 26 / z;
    const x0 = cam.x - hw + w / 2 + m, x1 = cam.x + hw - w / 2 - m;
    const y0 = cam.y - hh + 190 / z + h / 2, y1 = cam.y + hh - 520 / z - h / 2;
    x = clamp(x, x0, Math.max(x0, x1)); y = clamp(y, y0, Math.max(y0, y1));
    const fade = clamp(Math.min(lt / 0.05, (d - lt) / 0.2), 0, 1);
    let sc = 1, rot = -side * 0.06, jx = 0, jy = 0;
    if (c.style === 'slam') {
      const u = clamp(lt / 0.16, 0, 1); sc = lerp(2.5, 1, ease('easeOut', u));
      if (lt > 0.16) sc *= 1 + 0.07 * Math.sin((lt - 0.16) * 34) * Math.exp(-(lt - 0.16) * 7);
    } else if (c.style === 'shake') {
      sc = ease('back', lt / 0.25); jx = Math.sin(lt * 70) * 5; jy = Math.cos(lt * 63) * 4; rot += Math.sin(lt * 55) * 0.035;
    } else sc = ease('back', lt / 0.28);
    ctx.globalAlpha = fade; ctx.translate(x + jx, y + jy); ctx.rotate(rot); ctx.scale(sc, sc);
    ctx.lineJoin = 'round';
    lines.forEach((ln, i) => {
      const yy = (i - (lines.length - 1) / 2) * lh;
      ctx.lineWidth = c.size * 0.3; ctx.strokeStyle = OUT; ctx.strokeText(ln, 0, yy);
      ctx.fillStyle = c.color; ctx.fillText(ln, 0, yy);
    });
    ctx.restore();
  }
  _drawSafe(ctx) {
    ctx.save(); ctx.fillStyle = 'rgba(255,40,80,0.22)';
    ctx.fillRect(0, 0, W, 150); ctx.fillRect(0, H - 380, W, 380); ctx.fillRect(W - 130, 150, 130, H - 530);
    ctx.fillStyle = 'rgba(255,255,255,0.8)'; ctx.font = '700 28px Arial'; ctx.textAlign = 'left';
    ctx.fillText('TikTok UI', 20, 40); ctx.fillText('описание / кнопки', 20, H - 340);
    ctx.restore();
  }

  // ───── персонаж ─────
  _drawChar(ctx, st, t) {
    const def = st.def, g = this._bodyGeo(st), id = st.id;
    const C = this.C;
    ctx.save();
    ctx.translate(st.x, GROUND + st.y);
    const sh = 1 - clamp(-st.air / 400, 0, 0.6);
    ctx.fillStyle = 'rgba(0,0,0,0.24)';
    ctx.beginPath(); ctx.ellipse(0, 6, 84 * sh, 17 * sh, 0, 0, Math.PI * 2); ctx.fill();
    ctx.scale(st.face / Math.sqrt(st.sq), def.sy * st.sq);
    ctx.translate(0, st.air);
    ctx.lineCap = 'round'; ctx.lineJoin = 'round';

    // ноги
    const hipX = 30;
    for (const side of [-1, 1]) {
      const leg = side < 0 ? st.legs.L : st.legs.R;
      const hx = side * hipX, hy = g.hipY;
      const fx = leg.x, fy = -leg.lift - st.air * 0.0;
      const r = ik(hx, hy + 4, fx, fy, LEG, LEG, side, 1, 0.1);
      this._limb(ctx, [hx, hy + 4], [r.ex, r.ey], [r.hx, r.hy], 38, def.pants);
      ctx.fillStyle = def.shoe; ctx.strokeStyle = OUT; ctx.lineWidth = 6;
      ctx.beginPath(); ctx.ellipse(r.hx + 8, r.hy - 4, 36, 19, 0, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
    }

    // верх тела (в системе бёдер, с наклоном)
    ctx.save();
    ctx.translate(0, g.hipY);
    ctx.rotate(rad(st.lean));
    const tw = def.tw;
    this._torso(ctx, def.kind, def, tw);

    // руки (держат предметы)
    for (const hand of ['L', 'R']) this._arm(ctx, st, g, hand, t);

    // голова
    ctx.save();
    ctx.translate(0, -200); ctx.rotate(rad(st.head)); ctx.translate(0, -80);
    this._head(ctx, st, def.kind, def, t);
    ctx.restore();
    ctx.restore();

    ctx.restore();
  }
  _limb(ctx, a, b, c, w, col) {
    ctx.lineCap = 'round'; ctx.lineJoin = 'round';
    for (const [ww, cc] of [[w + 10, OUT], [w, col]]) {
      ctx.beginPath(); ctx.moveTo(a[0], a[1]); ctx.lineTo(b[0], b[1]); ctx.lineTo(c[0], c[1]);
      ctx.strokeStyle = cc; ctx.lineWidth = ww; ctx.stroke();
    }
  }
  _torso(ctx, id, def, tw) {
    ctx.lineWidth = 6; ctx.strokeStyle = OUT; ctx.lineJoin = 'round';
    // шея
    ctx.fillStyle = def.skin; rr(ctx, -16, -214, 32, 28, 8); ctx.fill(); ctx.stroke();
    if (id === 'eng') {
      ctx.fillStyle = def.shirt; rr(ctx, -tw / 2, -198, tw, 216, 28); ctx.fill(); ctx.stroke();
      // воротник
      ctx.fillStyle = '#fff';
      for (const s of [-1, 1]) { ctx.beginPath(); ctx.moveTo(s * 2, -200); ctx.lineTo(s * 30, -200); ctx.lineTo(s * 4, -160); ctx.closePath(); ctx.fill(); ctx.stroke(); }
      // галстук
      ctx.fillStyle = '#b03a48';
      ctx.beginPath(); ctx.moveTo(-8, -170); ctx.lineTo(8, -170); ctx.lineTo(13, -104); ctx.lineTo(0, -88); ctx.lineTo(-13, -104); ctx.closePath(); ctx.fill(); ctx.stroke();
      // карман и ручка
      ctx.fillStyle = '#6a9bd0'; rr(ctx, 20, -130, 30, 34, 5); ctx.fill(); ctx.stroke();
      ctx.beginPath(); ctx.moveTo(35, -126); ctx.lineTo(35, -144); ctx.strokeStyle = '#2d6cdf'; ctx.lineWidth = 6; ctx.stroke();
      ctx.strokeStyle = OUT; ctx.lineWidth = 6;
      // ремень
      ctx.fillStyle = '#2a2f3d'; rr(ctx, -tw / 2 + 2, 2, tw - 4, 16, 6); ctx.fill(); ctx.stroke();
    } else if (id === 'bld') {
      ctx.fillStyle = def.shirt; rr(ctx, -tw / 2, -198, tw, 216, 28); ctx.fill(); ctx.stroke();
      // жилет
      ctx.fillStyle = '#ff7a1a'; rr(ctx, -tw / 2 + 2, -196, tw - 4, 200, 24); ctx.fill(); ctx.stroke();
      ctx.fillStyle = def.shirt;
      ctx.beginPath(); ctx.moveTo(-30, -198); ctx.lineTo(30, -198); ctx.lineTo(0, -146); ctx.closePath(); ctx.fill(); ctx.stroke();
      // световозвращающие полосы
      ctx.fillStyle = '#e8f27a';
      for (const y of [-118, -66]) { ctx.fillRect(-tw / 2 + 4, y, tw - 8, 14); }
      ctx.lineWidth = 4;
      for (const y of [-118, -66]) { ctx.strokeRect(-tw / 2 + 4, y, tw - 8, 14); }
      ctx.lineWidth = 6;
      ctx.fillStyle = '#3b2e22'; rr(ctx, -tw / 2 + 2, 2, tw - 4, 16, 6); ctx.fill(); ctx.stroke();
      ctx.fillStyle = '#d8b24a'; rr(ctx, -10, 3, 20, 14, 3); ctx.fill();
    } else {
      // статист: рубашка, ремень, необязательный галстук и свои фигуры из JSON (координаты от бёдер, торс y от −198 до 18)
      ctx.fillStyle = def.shirt; rr(ctx, -tw / 2, -198, tw, 216, 28); ctx.fill(); ctx.stroke();
      if (def.tie) {
        ctx.fillStyle = '#fff';
        for (const s of [-1, 1]) { ctx.beginPath(); ctx.moveTo(s * 2, -200); ctx.lineTo(s * 30, -200); ctx.lineTo(s * 4, -160); ctx.closePath(); ctx.fill(); ctx.stroke(); }
        ctx.fillStyle = def.tie;
        ctx.beginPath(); ctx.moveTo(-8, -170); ctx.lineTo(8, -170); ctx.lineTo(13, -104); ctx.lineTo(0, -88); ctx.lineTo(-13, -104); ctx.closePath(); ctx.fill(); ctx.stroke();
      }
      ctx.fillStyle = '#2a2f3d'; rr(ctx, -tw / 2 + 2, 2, tw - 4, 16, 6); ctx.fill(); ctx.stroke();
      if (def.torso && def.torso.length) drawShapes(ctx, def.torso, this._t || 0, k => this.T(k));
    }
  }
  _arm(ctx, st, g, hand, t) {
    const side = hand === 'L' ? -1 : 1;
    const tgt = hand === 'L' ? st.L : st.R;
    const sx = side * g.sxn, sy = SHOULDER_Y;
    const r = ik(sx, sy, sx + side * tgt[0], sy + tgt[1], UARM, FARM, side, 0.8, 0.6);
    this._limb(ctx, [sx, sy], [r.ex, r.ey], [r.hx, r.hy], 30, st.def.sleeve);
    // предмет в руке
    const ch = this.C.chars[st.id];
    const hold = lastBefore(ch.holds.filter(h => h.hand === hand).length ? ch.holds.filter(h => h.hand === hand) : [{ t: 0, id: null }], t);
    if (hold && hold.id && hold.t <= t) {
      const P = this.C.props[hold.id];
      const ps = P && this.propState(P, t);
      if (P && ps.vis && ps.held) {
        ctx.save();
        ctx.translate(r.hx, r.hy);
        if (P.def.upright) ctx.rotate(-rad(st.lean));
        else ctx.rotate(Math.atan2(r.hx - r.ex, -(r.hy - r.ey)) + rad(P.def.holdRot || 0));
        this._drawProp(ctx, P, t, ps.scale);
        ctx.restore();
      }
    }
    ctx.fillStyle = st.def.skin; ctx.strokeStyle = OUT; ctx.lineWidth = 6;
    ctx.beginPath(); ctx.arc(r.hx, r.hy, 19, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
  }
  _head(ctx, st, id, def, t) {
    ctx.lineWidth = 6; ctx.strokeStyle = OUT; ctx.fillStyle = def.skin;
    // уши
    for (const s of [-1, 1]) { ctx.beginPath(); ctx.arc(s * 76, 6, 15, 0, Math.PI * 2); ctx.fill(); ctx.stroke(); }
    ctx.beginPath(); ctx.arc(0, 0, 77, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
    // блик
    ctx.save(); ctx.globalAlpha = 0.22; ctx.fillStyle = '#fff';
    ctx.beginPath(); ctx.ellipse(-32, -38, 22, 13, -0.6, 0, Math.PI * 2); ctx.fill(); ctx.restore();

    const e = st.emo, look = 8;
    const browY = id === 'eng' ? -54 : (id === 'extra' ? (def.glasses ? -54 : def.browY) : -32);
    // очки инженера (и статистов с glasses)
    if (id === 'eng' || (id === 'extra' && def.glasses)) {
      ctx.fillStyle = '#f6fbff'; ctx.strokeStyle = '#20242c'; ctx.lineWidth = 8;
      for (const s of [-1, 1]) { ctx.beginPath(); ctx.arc(s * 31 + look, -8, 26, 0, Math.PI * 2); ctx.fill(); ctx.stroke(); }
      ctx.beginPath(); ctx.moveTo(-5 + look, -10); ctx.lineTo(5 + look, -10); ctx.stroke();
      for (const s of [-1, 1]) { ctx.beginPath(); ctx.moveTo(s * 57 + look, -12); ctx.lineTo(s * 76, -16); ctx.stroke(); }
      ctx.save(); ctx.globalAlpha = 0.6; ctx.strokeStyle = '#fff'; ctx.lineWidth = 5;
      for (const s of [-1, 1]) { ctx.beginPath(); ctx.arc(s * 31 + look, -8, 16, Math.PI * 1.15, Math.PI * 1.5); ctx.stroke(); }
      ctx.restore();
    }
    // причёска и свои детали статиста (позади бровей и рта)
    if (id === 'extra') {
      if (def.hair) {
        ctx.fillStyle = def.hair; ctx.strokeStyle = OUT; ctx.lineWidth = 6;
        const a0 = Math.PI * 1.06, a1 = Math.PI * 1.94;
        ctx.beginPath(); ctx.moveTo(Math.cos(a0) * 79, Math.sin(a0) * 79); ctx.arc(0, 0, 79, a0, a1);
        ctx.quadraticCurveTo(0, -92, Math.cos(a0) * 79, Math.sin(a0) * 79); ctx.closePath(); ctx.fill(); ctx.stroke();
      }
      if (def.head_back && def.head_back.length) drawShapes(ctx, def.head_back, this._t || 0, k => this.T(k));
    }
    // брови — только когда есть эмоция
    if (e.vis > 0.03) {
      ctx.save(); ctx.globalAlpha = clamp(e.vis, 0, 1);
      ctx.strokeStyle = '#2a2230'; ctx.lineWidth = 12; ctx.lineCap = 'round';
      const hh = e.bh * (e.vis > 1 ? e.vis : 1);
      for (const s of [-1, 1]) {
        ctx.save();
        const extra = s > 0 ? e.bd : -e.bd * 0.5;
        ctx.translate(s * 31 + look, browY - hh - extra);
        ctx.rotate(rad(s < 0 ? e.bt : -e.bt));
        ctx.beginPath(); ctx.moveTo(-19, 0); ctx.lineTo(19, 0); ctx.stroke();
        ctx.restore();
      }
      ctx.restore();
    }
    // рот
    ctx.save(); ctx.translate(look, 34);
    this._mouth(ctx, e.mw, e.mc, st.mo, e.mk);
    ctx.restore();
    // каска строителя
    if (id === 'bld') {
      ctx.lineWidth = 6; ctx.strokeStyle = OUT;
      ctx.fillStyle = '#ffc61a';
      ctx.beginPath(); ctx.moveTo(-84, -48); ctx.quadraticCurveTo(-90, -118, 0, -122); ctx.quadraticCurveTo(90, -118, 84, -48); ctx.closePath(); ctx.fill(); ctx.stroke();
      ctx.fillStyle = '#ffd95c'; rr(ctx, -12, -122, 24, 60, 8); ctx.fill(); ctx.stroke();
      ctx.fillStyle = '#e6a800'; rr(ctx, -96, -58, 192, 18, 9); ctx.fill(); ctx.stroke();
      ctx.save(); ctx.globalAlpha = 0.35; ctx.fillStyle = '#fff'; ctx.beginPath(); ctx.ellipse(-48, -86, 20, 9, -0.5, 0, Math.PI * 2); ctx.fill(); ctx.restore();
    }
    if (id === 'extra') {
      if (def.hat) this._cap(ctx, def.hat);
      if (def.head_front && def.head_front.length) drawShapes(ctx, def.head_front, this._t || 0, k => this.T(k));
    }
  }
  _cap(ctx, col) {
    ctx.lineWidth = 6; ctx.strokeStyle = OUT; ctx.fillStyle = col;
    ctx.beginPath(); ctx.moveTo(-82, -44); ctx.quadraticCurveTo(-88, -112, 0, -116); ctx.quadraticCurveTo(88, -112, 82, -44); ctx.closePath(); ctx.fill(); ctx.stroke();
    rr(ctx, -94, -54, 188, 16, 8); ctx.fill(); ctx.stroke();
    ctx.save(); ctx.globalAlpha = 0.3; ctx.fillStyle = '#fff'; ctx.beginPath(); ctx.ellipse(-46, -84, 20, 9, -0.5, 0, Math.PI * 2); ctx.fill(); ctx.restore();
  }
  _mouth(ctx, w, c, o, mk) {
    const hw = w / 2, cl = -c * 16 + mk * 0.4, cr = -c * 16 - mk * 0.6;
    ctx.lineCap = 'round'; ctx.lineJoin = 'round'; ctx.strokeStyle = OUT; ctx.lineWidth = 7;
    if (o < 2.5) {
      ctx.beginPath(); ctx.moveTo(-hw, cl); ctx.quadraticCurveTo(0, c * 40 + (cl + cr) / 2 * 0, hw, cr); ctx.stroke();
      return;
    }
    const top = c * 14 - 2, low = Math.max(cl, cr);
    const shape = () => {
      ctx.beginPath();
      ctx.moveTo(-hw, cl); ctx.quadraticCurveTo(0, top, hw, cr);
      ctx.quadraticCurveTo(0, low + o * 1.9, -hw, cl); ctx.closePath();
    };
    shape(); ctx.fillStyle = '#4a1f27'; ctx.fill();
    // язык внутри рта (обрезается по контуру)
    ctx.save(); shape(); ctx.clip();
    ctx.fillStyle = '#e8737f'; ctx.beginPath(); ctx.ellipse(0, low + o * 0.8, hw * 0.55, o * 0.3, 0, 0, Math.PI * 2); ctx.fill();
    ctx.restore();
    // обводка рта — строго по его контуру
    shape(); ctx.stroke();
  }
}

const api = { Engine, W, H, GROUND, POSE_NAMES, EMO_NAMES, FX_KINDS, EASE_NAMES, SHAPE_TYPES, CHAR_IDS, LOOK_KEYS, CALLOUT_STYLES };
if (typeof module !== 'undefined' && module.exports) module.exports = api;
else root.Mult = api;
})(typeof window !== 'undefined' ? window : globalThis);
