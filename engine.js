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
// Архитекторша (жена Инженера): готовый тип "arch" — {"type":"arch"} у статиста; сама рисует причёску-пучок, шарф, серьгу и юбку
const O='#1e1b26';
const ARCH = {
  name: 'Архитекторша', skin: '#f6d2b4', shirt: '#e8765a', sleeve: '#e8765a', pants: '#2f8f8a', shoe: '#7a2f4a',
  sy: 0.98, tw: 108, hair: '#5a2d4a', hat: null, glasses: false, tie: null, browY: -34,
  torso: [
    { t: 'poly', pts: [[-52, 6], [52, 6], [92, 112], [-92, 112]], fill: '#2f8f8a', stroke: O, sw: 6 },
    { t: 'poly', pts: [[-30, 20], [-52, 112]], stroke: '#7fd0c6', sw: 6, closed: false },
    { t: 'poly', pts: [[0, 20], [0, 112]], stroke: '#7fd0c6', sw: 6, closed: false },
    { t: 'poly', pts: [[30, 20], [52, 112]], stroke: '#7fd0c6', sw: 6, closed: false },
    { t: 'rect', x: -56, y: 0, w: 112, h: 16, r: 6, fill: '#f2c14e', stroke: O, sw: 6 },
    { t: 'poly', pts: [[-40, -204], [40, -204], [34, -172], [0, -150], [-34, -172]], fill: '#f2c14e', stroke: O, sw: 6 },
    { t: 'poly', pts: [[10, -168], [42, -90], [24, -84], [2, -150]], fill: '#f2c14e', stroke: O, sw: 6 },
    { t: 'circle', x: 0, y: -160, r: 12, fill: '#e8765a', stroke: O, sw: 5 }
  ],
  head_front: [
    { t: 'circle', x: -10, y: -106, r: 34, fill: '#5a2d4a', stroke: O, sw: 6 },
    { t: 'poly', pts: [[-4, -118], [30, -150]], stroke: '#f2c14e', sw: 8, closed: false },
    { t: 'path', d: 'M -76 -10 Q -60 -78 8 -76 Q 52 -70 72 -30 Q 38 -52 4 -44 Q -34 -38 -76 -10 Z', fill: '#5a2d4a', stroke: O, sw: 6 },
    { t: 'circle', x: -60, y: 36, r: 11, fill: '#f2c14e', stroke: O, sw: 5 },
    { t: 'poly', pts: [[-60, 46], [-60, 66]], stroke: '#f2c14e', sw: 6, closed: false },
    { t: 'circle', x: -60, y: 70, r: 7, fill: '#e8765a', stroke: O, sw: 4 }
  ]
};

function resolveCharDef(type, inst, types, err, id) {
  let base;
  if (type === 'eng' || type === 'bld') base = Object.assign({ kind: type }, CHARS[type]);
  else if (type === 'extra') base = Object.assign({}, EXTRA_BASE);
  else if (type === 'arch') base = Object.assign({}, EXTRA_BASE, ARCH, { kind: 'extra' });
  else if (types[type] && typeof types[type] === 'object') base = Object.assign({}, EXTRA_BASE, types[type], { kind: 'extra' });
  else {
    err(`Персонаж "${id}": неизвестный тип "${type}" (есть: eng, bld, arch, extra${Object.keys(types).map(k => ', ' + k).join('')})`);
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
const DEFAULT_VIEW = 'main';
// имена ракурсов локации: из L.views и из меток v у слоёв
function viewNamesOf(L) {
  const set = new Set([DEFAULT_VIEW]);
  if (L && L.views && typeof L.views === 'object') for (const k in L.views) set.add(k);
  if (L && Array.isArray(L.layers)) for (const ly of L.layers) if (ly && ly.v != null) for (const v of [].concat(ly.v)) set.add(String(v));
  return set;
}
function layerInView(ly, view) { return ly.v == null || [].concat(ly.v).map(String).includes(view); }
const PORTRAIT_BG = ['blur', 'dark'];
const ANGLES = ['side', 'back'];          // углы героев в обычном кадре: 90° (как раньше) и 270° (со спины)
const PORTRAIT_ANGLES = ['side', 'q45'];  // в портрете: 90° и 45° (три четверти); со спины портрет не бывает
const isMain = d => d && (d.kind === 'eng' || d.kind === 'bld');

const HIP_Y = -160, LEG = 88, UARM = 92, FARM = 88, SHOULDER_Y = -172;

// ───────────────────────── позы ─────────────────────────
// L/R = положение кисти относительно плеча [наружу, вниз] (px). Руки считаются через IK.
const BASE = { L: [24, 164], R: [24, 164], by: 0, air: 0, lean: 0, head: 0, sq: 1, roll: 0 };
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
  drill: (lt, t) => P({ R: [88 + Math.sin(t * 72) * 2.4, 54 + Math.sin(t * 83) * 1.7], L: [42 + Math.sin(t * 69 + 1) * 1.6, 82 + Math.sin(t * 77) * 1.3], lean: 1, head: 1 + Math.sin(t * 2.2) * 0.8, by: Math.sin(t * 2.2) * 1.2 }),
  drill_think: (lt, t) => P({ R: [88, 54], L: [-30, 80], head: -7 + Math.sin(t * 1.5) * 2 }),
  drill_point: (lt, t) => P({ R: [88, 54], L: [132, 20], lean: 2, head: -2 }),
  drill_tired: (lt, t) => P({ R: [88, 54], L: [16, 175], head: 9, lean: -2, by: 0, sq: 0.99 }),

  drill_cheer: (lt, t) => P({ R: [88, 54], L: [72 + Math.sin(lt * 8) * 8, -142], lean: 1, by: -Math.abs(Math.sin(lt * 8)) * 7, head: -3 }),
  drill_sad: (lt, t) => P({ R: [24, 164], L: [16, 175], lean: -2, by: 0, head: 9, sq: 0.99 }),
  drill_wave: (lt, t) => P({ R: [88, 54], L: [78 + Math.sin(lt * 10) * 28, -140], lean: 1, head: -4 }),
  hammer: (lt) => {
    const p = (lt * 2.2) % 1; let ox, oy, lean;
    if (p < 0.6) { const k = ease('easeInOut', p / 0.6); ox = lerp(70, 36, k); oy = lerp(30, -170, k); lean = lerp(0, -6, k); }
    else if (p < 0.72) { const k = (p - 0.6) / 0.12; ox = lerp(36, 100, k * k); oy = lerp(-170, 100, k * k); lean = lerp(-6, 12, k); }
    else { const k = ease('easeOut', (p - 0.72) / 0.28); ox = lerp(100, 70, k); oy = lerp(100, 30, k); lean = lerp(12, 0, k); }
    return P({ R: [ox, oy], L: [40, 80], lean, by: lean > 6 ? 5 : 0 });
  },
  sit: (lt, t) => P({ L: [46, 150], R: [46, 150], sq: .86, air: -30, by: Math.sin(t * 1.6) * 1 }),
  sit_tap: (lt, t) => P({ L: [46, 150], R: [46, 142 + Math.abs(Math.sin(t * 11)) * 12], sq: .86, air: -30, head: -3 }),
  sit_up: (lt, t) => P({ L: [46, 150], R: [-20, 80], sq: .86, air: -30, head: -13, lean: -4 }),
  sit_slump: (lt, t) => P({ L: [40, 150], R: [40, 150], sq: .84, air: -30, head: 12, lean: 5, by: 4 }),
  sit_lean: (lt, t) => P({ L: [46, 150], R: [-10, 60], sq: .86, air: -30, head: 6, lean: 8 }),
  crank: (lt, t) => P({ R: [112 + Math.sin(t * 18) * 8, 6 + Math.cos(t * 18) * 8], L: [46, 100], lean: 4 }),
  valve_pull: (lt, t) => P({ L: [120, -4 + Math.sin(t * 26) * 3], R: [120, -4 - Math.sin(t * 26) * 3], lean: -14, by: 6, head: 4 }),
  pull: (lt, t) => P({ L: [128, 12 + Math.sin(t * 24) * 3], R: [128, 12 - Math.sin(t * 24) * 3], lean: -14, by: 6 }),
  fall_back: (lt, t) => P({ L: [74, -70], R: [74, -70], lean: -30, by: 8, head: -8 }),
  wipe: (lt, t) => P({ L: [30, 120 + Math.sin(t * 9) * 8], R: [30, 120 - Math.sin(t * 9) * 8], head: 8, lean: -2, by: 3 }),
  drive: (lt, t) => P({ L: [74, 104], R: [74, 104], sq: .86, air: -30, by: Math.sin(t * 2.2) * 1, head: 0 }),
  drive_rev: (lt, t) => P({ L: [74, 104], R: [74, 104], sq: .86, air: -30, lean: 5 + Math.sin(t * 26) * 3, head: 4, by: Math.sin(t * 30) * 3 }),
  mow: (lt, t) => P({ L: [84, 134], R: [84, 134], lean: 7, by: Math.abs(Math.sin(t * 6)) * 3 }),
  drive_sink: (lt, t) => P({ L: [74, 104], R: [74, 104], sq: .86, air: 22, lean: 4 + Math.sin(t * 20) * 2, head: 3, by: Math.sin(t * 26) * 2 }),
  rake: (lt, t) => P({ L: [86 + Math.sin(t * 3.2) * 20, 134], R: [92 + Math.sin(t * 3.2) * 20, 118], lean: 12 + Math.sin(t * 3.2) * 3, by: 2 }),
  saw: (lt, t) => P({ R: [100 + Math.sin(t * 10.5) * 16, 150], L: [40, 130], lean: 24, head: 6, sq: .86 }),
  paint: (lt, t) => P({ R: [118, 20 + Math.sin(t * 6.5) * 55], L: [40, 125], lean: 8, head: -4, by: 1 }),
  lie: (lt, t) => P({ L: [8, 178], R: [8, 178], roll: -88, head: -4, by: Math.sin(t * 1.3) * 1.2 }),
  lie_ear: (lt, t) => P({ L: [8, 178], R: [-30, -60], roll: -88, head: 8 }),
  poke: (lt, t) => P({ L: [24, 164], R: [112, 64], lean: 6, head: -4 }),
  touch: (lt, t) => P({ L: [24, 164], R: [120, 8], lean: 4, head: 0 }),
  lie_look: (lt, t) => P({ L: [8, 178], R: [8, 178], roll: -88, head: 34 }),
  valve_up: (lt, t) => P({ L: [24, 164], R: [118, -44 + Math.sin(t * 6) * 3], lean: 5, head: -6 }),
  rub: (lt, t) => P({ L: [52 + Math.sin(t * 16) * 9, 84], R: [52 - Math.sin(t * 16) * 9, 84], head: 3, lean: 2, sq: .97 }),
  sit_rub: (lt, t) => P({ L: [52 + Math.sin(t * 16) * 9, 96], R: [52 - Math.sin(t * 16) * 9, 96], sq: .86, air: -30, head: 4 }),
  sit_cozy: (lt, t) => P({ L: [30, 70], R: [30, 70], sq: .86, air: -30, head: 6, by: Math.sin(t * 1.6) }),
  hands_warm: (lt, t) => P({ L: [120, 20 + Math.sin(t * 5) * 3], R: [130, 28 + Math.sin(t * 5 + 1) * 3], lean: 5, head: -2 }),
  crouch_idle: (lt, t) => P({ sq: .8, lean: 14, head: -6, L: [20, 120], R: [20, 120], by: Math.sin(t * 2) * 1 }),
  crouch_walk: (lt, t) => P({ sq: .8, lean: 15, head: -8, L: [24 + Math.sin(t * 7) * 10, 118], R: [24 - Math.sin(t * 7) * 10, 118], by: Math.abs(Math.sin(t * 7)) * 2 }),
  ouch: (lt, t) => P({ sq: .92, lean: 6, head: 14, L: [10, -160], R: [40, 110], by: 4 }),
  hop: (lt) => {
    const T = 0.5, u = Math.min(1, (lt % T) / T), air = Math.sin(Math.PI * u);
    return P({ air: -air * 70, sq: 1 - (u < 0.12 ? 0.1 * Math.sin(Math.PI * u / 0.12) : 0), L: [50, -60], R: [50, -60], lean: 6 });
  },
  balance: (lt) => P({ L: [60, -70 + Math.sin(lt * 7) * 55], R: [60, -70 - Math.sin(lt * 7) * 55], lean: Math.sin(lt * 7) * 9, head: Math.sin(lt * 7) * -5 }),
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
  frown: { mw: 76, mc: -1.7 },   // сильно перевёрнутая улыбка без бровей (финал сюжета №6)
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
    case 'fall': { const wr = a.a || 160, off = (t * (a.s || 1800)) % wr; ctx.translate(off * (a.dx || 0) / wr, off); break; }   // дождь: узор с периодом a падает со скоростью s px/с, снос dx на период
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
    if (s.anim && !['sway', 'bob', 'slide', 'spin', 'pulse', 'drift', 'shake', 'blink', 'fall'].includes(s.anim.k)) err(`${w}: неизвестная анимация "${s.anim.k}"`);
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
      L.layers.forEach((ly, i) => {
        validateShapes(ly.shapes, `Локация "${k}" → layers[${i}]`, err);
        if (ly.v != null && !(typeof ly.v === 'string' || (Array.isArray(ly.v) && ly.v.every(x => typeof x === 'string')))) err(`Локация "${k}" → layers[${i}]: v — строка или массив строк (имена ракурсов)`);
      });
      if (L.views != null) {
        if (typeof L.views !== 'object' || Array.isArray(L.views)) err(`Локация "${k}": views — объект {имя: {title, cam}}`);
        else for (const vn in L.views) { const c = L.views[vn] && L.views[vn].cam; if (c && !(isNum(c.x) || isNum(c.y) || isNum(c.zoom))) err(`Локация "${k}" → views.${vn}.cam: нужны x, y и/или zoom`); }
      }
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
      locs, propDefs, chars: {}, props: {}, camSegs: [], shakes: [], fx: [], titles: [], callouts: [], viewEv: [], mirrorEv: [{ t: 0, m: false }], portraits: [], locEv: [], says: [], markers: [],
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
        id, def: resolveCharDef(type, inst, charTypes, err, id), renderLayer: inst.renderLayer === 'behindProps' ? 'behindProps' : 'normal',
        x0: s && isNum(s.x) ? s.x : (defaultStart[id] ? defaultStart[id].x : 540), vis: [{ t: 0, v: !!s && !inst.hidden }],
        angs: [{ t: 0, v: inst.angle === 'back' ? 'back' : 'side', prev: 'side', dur: 0 }],
        face: [{ t: 0, v: s && s.face === 'left' ? -1 : 1 }], segs: [], lifts: [], cum: 0, poses: [], emos: [], says: [], holds: [], vests: [], outfits: [], seed: hashStr(id) % 100
      };
    }
    for (const id in C.chars) {
      const a = startChars && startChars[id] && startChars[id].angle;
      if (a != null && !ANGLES.includes(a)) err(`Персонаж "${id}": angle = ${ANGLES.join(' | ')} (45° только в портрете)`);
      else if (a === 'back' && !isMain(C.chars[id].def)) err(`Персонаж "${id}": вид со спины есть только у eng и bld`);
    }
    const locStart = start.location || (scene.location);
    if (!locStart) err('Сцена: не указана стартовая локация (start.location)');
    else if (!locs[locStart]) err(`Стартовая локация "${locStart}" не найдена (ни в library.json, ни в defs.locations)`);
    C.locEv.push({ t: 0, id: locStart, transition: 'cut', dur: 0 });
    C.viewEv.push({ t: 0, view: start.view || null, transition: 'cut', dur: 0, cam: false });

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
          if (isNum(b.y)) ch.lifts.push({ t0: t, t1: t, y0: b.y, y1: b.y, ease: 'linear' });
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
          if (isNum(b.y)) ch.lifts.push({ t0: t, t1: t + dur, y0: eng._liftAt(ch, t), y1: b.y, ease: b.yease || b.ease || 'soft' });
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
          C.props[b.id] = { id: b.id, def: propDefs[b.prop], floor, layer: ['front', 'back'].includes(b.layer) ? b.layer : 'auto', ev: [{ type: 'spawn', t, x: b.x, y: floor, rot: b.rot || 0, scale: isNum(b.scale) ? b.scale : 1 }] };
          break;
        }
        case 'move': case 'remove': case 'hold': case 'release': case 'layer': {
          const P = C.props[b.id];
          if (!P) { err(`${tag}: предмет "${b.id}" не создан (нужен spawn раньше)`); break; }
          if (b.do === 'remove') P.ev.push({ type: 'remove', t });
          else if (b.do === 'layer') {
            if (!['front', 'back'].includes(b.layer)) { err(`${tag}: layer = front | back`); break; }
            P.ev.push({ type: 'layer', t, layer: b.layer });
          } else if (b.do === 'move') {
            if (!needDur()) break;
            P.ev.push({ type: 'move', t, t1: t + b.dur, x: isNum(b.x) ? b.x : null, y: isNum(b.y) ? b.y : null, arc: b.arc || 0, ease: b.ease || 'easeInOut', rot: isNum(b.rot) ? b.rot : null, sc: isNum(b.scale) ? b.scale : null });
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
          C.viewEv.push({ t, view: b.view || null, transition: 'cut', dur: 0, cam: true, tag });
          break;
        }
        case 'lift': {
          // вертикальное смещение героя (склон, мост): y < 0 — выше земли; можно и в walk: {do:"walk",x,y,dur}
          const id = who(b, i); if (!id) break;
          if (!isNum(b.y)) { err(`${tag}: lift требует y`); break; }
          const ch = C.chars[id], dur = isNum(b.dur) ? Math.max(0, b.dur) : 0;
          ch.lifts.push({ t0: t, t1: t + dur, y0: eng._liftAt(ch, t), y1: b.y, ease: b.ease || 'linear' });
          break;
        }
        case 'outfit': {
          // смена одежды: {do:"outfit",who:"eng",shirt:"#b5654a",sleeve:"#b5654a"}; sleeve:"#f4cfae" = голые руки (футболка)
          const id = who(b, i); if (!id) break;
          if (typeof b.shirt !== 'string') { err(`${tag}: outfit требует shirt`); break; }
          C.chars[id].outfits.push({ t, shirt: b.shirt, sleeve: typeof b.sleeve === 'string' ? b.sleeve : undefined, pants: b.pants, shoe: b.shoe, pj: !!b.pj, stripe: b.stripe });
          break;
        }
        case 'vest': {
          // перекраска жилета строителя: {do:"vest",who:"bld",color:"#2f8049",stripe:"#2a6f40"}
          const id = who(b, i); if (!id || id !== 'bld') { err(`${tag}: vest только у bld`); break; }
          if (typeof b.color !== 'string') { err(`${tag}: vest требует color`); break; }
          C.chars[id].vests.push({ t, color: b.color, stripe: typeof b.stripe === 'string' ? b.stripe : null });
          break;
        }
        case 'angle': {
          // поворот главного героя: side (как обычно) или back (спиной к камере)
          if (!ANGLES.includes(b.angle)) { err(`${tag}: angle = ${ANGLES.join(' | ')}${b.angle === 'q45' ? ' (45° только в портрете: portrait с angle:"q45")' : ''}`); break; }
          const ids = b.who === 'both' ? ['eng', 'bld'].filter(k => C.chars[k]) : [who(b, i)];
          for (const id of ids) {
            if (!id) continue;
            if (!isMain(C.chars[id].def)) { err(`${tag}: поворот есть только у eng и bld, не у "${id}"`); continue; }
            C.chars[id].angs.push({ t, v: b.angle, prev: null, dur: isNum(b.dur) ? clamp(b.dur, 0, 1.5) : 0.3 });
          }
          break;
        }
        case 'view': {
          // смена ракурса текущей локации (другой «кадр» того же места)
          if (typeof b.id !== 'string') { err(`${tag}: нужен id ракурса`); break; }
          if (b.transition != null && !['cut', 'fade', 'flash', 'wipe'].includes(b.transition)) { err(`${tag}: transition = cut | fade | flash | wipe`); break; }
          if (b.angle != null && !ANGLES.includes(b.angle)) { err(`${tag}: angle = ${ANGLES.join(' | ')} (камера: side — как обычно, back — камера за спинами героев)`); break; }
          C.viewEv.push({ t, view: b.id, transition: b.transition || 'cut', dur: isNum(b.dur) ? b.dur : 0.4, cam: b.keepCam ? false : true, tag, angle: b.angle || null });
          if (b.angle) {
            // камера перешла за спины героев (или вернулась): мир отзеркаливается, герои разворачиваются мгновенно
            C.mirrorEv.push({ t, m: b.angle === 'back' });
            for (const k of ['eng', 'bld']) if (C.chars[k]) C.chars[k].angs.push({ t, v: b.angle, prev: null, dur: 0 });
          }
          break;
        }
        case 'portrait': {
          // портретная камера: резкая смена кадра на крупное лицо героя
          const id = who(b, i, 'on'); if (!id) break;
          if (!needDur()) break;
          const bgOk = b.bg == null || PORTRAIT_BG.includes(b.bg) || typeof b.bg === 'string' && /^(#|rgb|hsl)/i.test(b.bg) || (Array.isArray(b.bg) && b.bg.length >= 2);
          if (!bgOk) { err(`${tag}: bg = blur | dark | цвет "#rrggbb" | массив цветов (градиент)`); break; }
          if (!PORTRAIT_ANGLES.includes(b.angle == null ? 'side' : b.angle)) { err(`${tag}: angle портрета = ${PORTRAIT_ANGLES.join(' | ')} (со спины лицо не показывают)`); break; }
          if (b.angle === 'q45' && !isMain(C.chars[id].def)) { err(`${tag}: 45° есть только у eng и bld`); break; }
          C.portraits.push({ t0: t, t1: t + b.dur, on: id, angle: b.angle == null ? 'side' : b.angle, zoom: isNum(b.zoom) ? clamp(b.zoom, 1.6, 4) : 2.5, solo: b.solo !== false, bg: b.bg == null ? 'blur' : b.bg, punch: b.punch !== false, dy: isNum(b.dy) ? b.dy : 0, tag });
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
      ch.angs.sort((a, c) => a.t - c.t); for (let k = 1; k < ch.angs.length; k++) ch.angs[k].prev = ch.angs[k - 1].v;
      ch.face.sort((a, c) => a.t - c.t); ch.vis.sort((a, c) => a.t - c.t); ch.holds.sort((a, c) => a.t - c.t);
      ch.segs.sort((a, c) => a.t0 - c.t0);
      ch.lifts.sort((a, c) => a.t0 - c.t0);
      // кумулятивная дистанция для ходьбы без скольжения ног
      let cum = 0; for (const s of ch.segs) { s.d0 = cum; if (s.moving) cum += Math.abs(s.x1 - s.x0); }
    }
    C.locEv.sort((a, c) => a.t - c.t);
    C.viewEv.sort((a, c) => a.t - c.t);
    C.mirrorEv.sort((a, c) => a.t - c.t);
    for (const e of C.viewEv) {
      if (e.t > 0 && !e.angle && C.mirrorEv.length > 1 && lastBefore(C.mirrorEv, e.t - 1e-6).m) warn(`${e.tag}: камера всё ещё за спинами героев (angle back). Новый ракурс без angle оставляет всё как есть; для кадра с лица укажите angle:"side"`);
    }
    for (const e of C.viewEv) {
      const L = locs[lastBefore(C.locEv, e.t).id]; if (!L) continue;
      const names = viewNamesOf(L);
      if (e.view && !names.has(e.view)) { err(`${e.tag || 'start'}: у локации "${lastBefore(C.locEv, e.t).id}" нет ракурса "${e.view}" (есть: ${[...names].join(', ')})`); e.view = null; }
      const vc = L.views && L.views[e.view || DEFAULT_VIEW] && L.views[e.view || DEFAULT_VIEW].cam;
      if (e.cam && vc) C.camSegs.push({ t0: e.t, t1: e.t, ease: 'snap', reset: false, on: null, focus: 'body', follow: false, zoom: vc.zoom, x: vc.x, y: vc.y, dx: 0, dy: 0, rot: 0 });
    }
    C.portraits.sort((a, c) => a.t0 - c.t0);
    for (const p of C.portraits) {
      const ch = C.chars[p.on];
      const backAt = lastBefore(ch.angs, p.t0).v === 'back' || ch.angs.some(a => a.t > p.t0 && a.t < p.t1 && a.v === 'back');
      if (backAt) err(`${p.tag}: портрет героя "${p.on}", пока он стоит спиной (angle back). Сначала верните angle side`);
    }
    for (let k = 1; k < C.portraits.length; k++) if (C.portraits[k].t0 < C.portraits[k - 1].t1) warn('Портретные кадры пересекаются по времени');
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
    rep.info.portraits = C.portraits;
    rep.info.angles = Object.values(C.chars).flatMap(ch => ch.angs.filter(a => a.t > 0).map(a => ({ t: a.t, who: ch.id, v: a.v })));
    rep.info.views = C.viewEv.filter(e => e.t > 0).map(e => ({ t: e.t, view: e.view || DEFAULT_VIEW, transition: e.transition, dur: e.dur }));
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
  _liftAt(ch, t) {
    let y = 0;
    for (const s of ch.lifts) {
      if (s.t0 > t) break;
      if (t >= s.t1) { y = s.y1; continue; }
      y = lerp(s.y0, s.y1, ease(s.ease, (t - s.t0) / (s.t1 - s.t0)));
      break;
    }
    return y;
  }
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

  _mirrorAt(t) { return !!lastBefore(this.C.mirrorEv, t).m; }
  // raw = координаты «мира» без зеркала камеры (для логики предметов)
  charState(id, t, raw) {
    const C = this.C, ch = C.chars[id], def = ch.def;
    const vis = lastBefore(ch.vis, t).v;
    const mir = !raw && this._mirrorAt(t);
    const x = mir ? W - this._posAt(ch, t) : this._posAt(ch, t);
    const face = lastBefore(ch.face, t).v * (mir ? -1 : 1);
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
    let vest = null; for (const e of ch.vests) if (e.t <= t) vest = e;
    let of = null; for (const e of ch.outfits) if (e.t <= t) of = e;
    const odef = of ? Object.assign({}, def, { shirt: of.shirt || def.shirt, sleeve: of.sleeve === undefined ? def.sleeve : of.sleeve, pants: of.pants || def.pants, shoe: of.shoe || def.shoe, pj: of.pj, stripe: of.stripe }) : def;
    const ae = lastBefore(ch.angs, t);
    const ang = { v: ae.v, prev: ae.prev || ae.v, lt: t - ae.t, dur: ae.dur };
    return { ang, pname: pose._name, vis, x, y: this._liftAt(ch, t), face, legs, L, R, head, lean, by, air: pose.air, sq: pose.sq, roll: pose.roll || 0, emo, mo, wk, run, say, def: odef, id, vest, renderLayer: ch.renderLayer || 'normal' };
  }

  // кисть в мировых координатах (для падения/удержания предметов и камеры)
  _bodyGeo(st) {
    const def = st.def;
    const upper = st.by;
    const hipY = HIP_Y + upper;
    const sxn = def.tw / 2 - 8;
    return { hipY, sxn, def };
  }
  handWorld(id, t, hand, raw) {
    const st = this.charState(id, t, raw);
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
        to.x = s.x; to.y = GROUND + (s.y || 0) - (FY[seg.focus] || 260) * s.def.sy;
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
    if (st.zoom >= 1) {   // zoom < 1 («дрон»): камера свободна, локация должна быть нарисована шире мира
      const hw = W / 2 / st.zoom, hh = H / 2 / st.zoom;
      st.x = clamp(st.x, hw, W - hw); st.y = clamp(st.y, hh, H - hh);
    }
    return st;
  }

  // ───── предметы ─────
  // предмет с учётом зеркала камеры (камера за спинами героев)
  propState(P, t) {
    const r = this._propRaw(P, t);
    if (!r.pos || !this._mirrorAt(t)) return r;
    return Object.assign({}, r, { pos: Object.assign({}, r.pos, { x: W - r.pos.x }), rot: -r.rot });
  }
  _propRaw(P, t) {
    let pos = null, rot = 0, scale = 1, vis = false, held = null, floor = P.floor, layer = P.layer;
    for (let i = 0; i < P.ev.length; i++) {
      const e = P.ev[i];
      if (e.t > t) break;
      switch (e.type) {
        case 'spawn': pos = { x: e.x, y: e.y }; rot = e.rot; scale = e.scale; vis = true; held = null; break;
        case 'remove': vis = false; break;
        case 'layer': layer = e.layer; break;
        case 'hold': held = { who: e.who, hand: e.hand }; break;
        case 'release': {
          const hw = this.handWorld(e.who, e.t, e.hand, true);
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
          if (t >= e.t1) { pos = { x: tx, y: ty }; if (e.rot != null) rot = e.rot; if (e.sc != null) scale = e.sc; }
          else {
            const k = ease(e.ease, (t - e.t) / (e.t1 - e.t));
            pos = { x: lerp(pos.x, tx, k), y: lerp(pos.y, ty, k) - Math.sin(Math.PI * k) * e.arc };
            if (e.rot != null) rot = lerp(rot, e.rot, k);
            if (e.sc != null) scale = lerp(scale, e.sc, k);
            return { vis, pos, rot, scale, held, floor, layer };
          }
          break;
        }
      }
    }
    return { vis, pos, rot, scale, held, floor, layer };
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
    let cam = this.camAt(t);
    const por = C.portraits.find(p => t >= p.t0 && t < p.t1) || null;
    if (por) cam = this._portraitCam(por, t);
    let sx = 0, sy = 0;
    for (const s of C.shakes) if (t >= s.t0 && t < s.t1) {
      const k = 1 - (t - s.t0) / (s.t1 - s.t0);
      sx += s.amp * k * noise(t * 55); sy += s.amp * k * noise(t * 49 + 3);
    }
    const locEv = lastBefore(C.locEv, t);
    const loc = C.locs[locEv.id];
    const view = (lastBefore(C.viewEv, t) || {}).view || DEFAULT_VIEW;
    const T = k => this.T(k);

    const withCam = (p, fn) => {
      ctx.save();
      const zl = 1 + (cam.zoom - 1) * p, cx = 540 + (cam.x - 540) * p, cy = 960 + (cam.y - 960) * p;
      ctx.translate(W / 2 + sx * p, H / 2 + sy * p);
      if (cam.rot) ctx.rotate(rad(cam.rot) * Math.max(p, 0.0));
      ctx.scale(zl, zl); ctx.translate(-cx, -cy);
      fn(); ctx.restore();
    };

    if (por) this._portraitBg(ctx, por, t, loc, view, withCam, T);
    else if (loc) for (const ly of loc.layers) if (ly.z !== 'front' && layerInView(ly, view)) withCam(ly.p == null ? 1 : ly.p, () => drawShapes(ctx, ly.shapes, t, T));

    withCam(1, () => {
      const props = Object.values(C.props);
      const mirK = this._mirrorAt(t) ? -1 : 1;
      const ids = Object.keys(C.chars).sort((a, b) => mirK * (this._posAt(C.chars[a], t) - this._posAt(C.chars[b], t)));
      // Персонажи с renderLayer: behindProps рисуются позади всех предметов сцены.
      for (const id of ids) {
        const st = this.charState(id, t);
        if (st.renderLayer !== 'behindProps' || (por && por.solo && id !== por.on)) continue;
        if (st.vis) this._drawChar(ctx, st, t, por && por.on === id ? por.angle : null);
      }
      // Явные back-объекты остаются на дальнем плане.
      for (const P of props) {
        const s = this.propState(P, t);
        if (s.layer !== 'back' || por) continue;
        if (!s.vis || s.held || !s.pos) continue;
        ctx.save(); ctx.translate(s.pos.x, s.pos.y); ctx.rotate(rad(s.rot)); this._drawProp(ctx, P, t, s.scale); ctx.restore();
      }
      // Автоматическая глубина: самостоятельные объекты сортируются по нижней точке.
      // Чем ниже основание объекта в кадре, тем позже он рисуется и тем ближе он к зрителю.
      if (!por) {
        const depthItems = [];
        for (const id of ids) {
          const st = this.charState(id, t);
          if (st.renderLayer !== 'behindProps' && st.vis) depthItems.push({kind:'char', id, y:GROUND + (st.y || 0)});
        }
        for (const P of props) {
          const s = this.propState(P, t);
          if (s.layer === 'auto' && s.vis && !s.held && s.pos) depthItems.push({kind:'prop', P, s, y:s.pos.y});
        }
        depthItems.sort((a,b)=>a.y-b.y);
        for (const item of depthItems) {
          if (item.kind === 'char') {
            const st = this.charState(item.id, t);
            this._drawChar(ctx, st, t, por && por.on === item.id ? por.angle : null);
          } else {
            const {P,s}=item;
            ctx.save(); ctx.translate(s.pos.x,s.pos.y); ctx.rotate(rad(s.rot)); this._drawProp(ctx,P,t,s.scale); ctx.restore();
          }
        }
      } else {
        for (const id of ids) {
          const st = this.charState(id, t);
          if (st.renderLayer !== 'behindProps' && !(por && por.solo && id !== por.on) && st.vis)
            this._drawChar(ctx, st, t, por && por.on === id ? por.angle : null);
        }
      }
      // Явные front-объекты остаются поверх автоматической сортировки.
      for (const P of props) {
        const s = this.propState(P, t);
        if (s.layer !== 'front' || por) continue;
        if (!s.vis || s.held || !s.pos) continue;
        ctx.save(); ctx.translate(s.pos.x, s.pos.y); ctx.rotate(rad(s.rot)); this._drawProp(ctx, P, t, s.scale); ctx.restore();
      }
    });

    if (loc) for (const ly of loc.layers) if (ly.z === 'front' && layerInView(ly, view)) withCam(ly.p == null ? 1 : ly.p, () => drawShapes(ctx, ly.shapes, t, T));

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

    if (por) this._portraitFx(ctx, por, t);

    // переход между локациями и ракурсами
    for (const e of [...C.locEv, ...C.viewEv]) {
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

  // камера портретного кадра: лицо героя крупно, чуть выше центра (внизу место для субтитров)
  _portraitCam(p, t) {
    const lt = t - p.t0;
    const seg = { on: p.on, focus: 'face', zoom: p.zoom, dx: 0, dy: 0 };
    const to = this._camTarget(seg, { x: 540, y: 960, zoom: p.zoom, rot: 0 }, t);
    let zoom = p.zoom;
    if (p.punch) zoom *= 1 + 0.14 * Math.exp(-lt * 16) * Math.cos(lt * 22);   // «щелчок» при смене кадра
    to.y += 120 / p.zoom + p.dy;
    const hw = W / 2 / zoom, hh = H / 2 / zoom;
    return { x: clamp(to.x, hw, W - hw), y: to.y < hh ? to.y : clamp(to.y, hh, H - hh), zoom, rot: 0 };   // лицо выше мира (герой на высоте) — не прижимаем
  }
  _portraitBg(ctx, p, t, loc, view, withCam, T) {
    const bg = p.bg;
    if (bg === 'blur' || bg === 'dark') {
      if (loc) {
        const blur = bg === 'blur' && this._canBlur();
        if (blur) ctx.filter = 'blur(16px)';
        for (const ly of loc.layers) if (ly.z !== 'front' && layerInView(ly, view)) withCam(ly.p == null ? 1 : ly.p, () => drawShapes(ctx, ly.shapes, t, T));
        if (blur) ctx.filter = 'none';
      }
      ctx.fillStyle = bg === 'dark' ? 'rgba(18,14,28,.62)' : 'rgba(18,14,28,.28)'; ctx.fillRect(0, 0, W, H);
    } else {
      const g = ctx.createLinearGradient(0, 0, 0, H);
      const cols = Array.isArray(bg) ? bg : [bg, bg];
      cols.forEach((c, i) => g.addColorStop(i / (cols.length - 1), c));
      ctx.fillStyle = g; ctx.fillRect(0, 0, W, H);
    }
    // мягкое пятно света за головой
    const sp = ctx.createRadialGradient(W / 2, 800, 60, W / 2, 800, 620);
    sp.addColorStop(0, 'rgba(255,255,255,.20)'); sp.addColorStop(1, 'rgba(255,255,255,0)');
    ctx.fillStyle = sp; ctx.fillRect(0, 0, W, H);
  }
  _portraitFx(ctx, p, t) {
    // виньетка и короткая вспышка при смене кадра
    const v = ctx.createRadialGradient(W / 2, H / 2, 380, W / 2, H / 2, 1150);
    v.addColorStop(0, 'rgba(0,0,0,0)'); v.addColorStop(1, 'rgba(0,0,0,.5)');
    ctx.fillStyle = v; ctx.fillRect(0, 0, W, H);
    const lt = t - p.t0;
    if (p.punch && lt < 0.12) { ctx.fillStyle = `rgba(255,255,255,${0.45 * (1 - lt / 0.12)})`; ctx.fillRect(0, 0, W, H); }
  }
  _canBlur() {
    if (this._blurOk == null) { try { this._blurOk = 'filter' in this.ctx && !/^((?!chrome|android).)*safari/i.test(typeof navigator !== 'undefined' ? navigator.userAgent : ''); } catch (e) { this._blurOk = false; } }
    return this._blurOk;
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
    const fx = isNum(f.x) ? f.x : 540;
    return { x: this._mirrorAt(t) ? W - fx : fx, y: isNum(f.y) ? f.y : 700 };
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
    const csz = c.size * Math.min(1, 1.3 / z);   // на крупных планах не раздуваем надпись
    ctx.save();
    ctx.font = `900 ${csz}px "Arial Black", Impact, Arial, sans-serif`;
    ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
    const lines = this._wrap(ctx, text, 540), lh = csz * 1.08;
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
      ctx.lineWidth = csz * 0.3; ctx.strokeStyle = OUT; ctx.strokeText(ln, 0, yy);
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
  _drawChar(ctx, st, t, portraitAngle) {
    const def = st.def, g = this._bodyGeo(st), id = st.id;
    this._vestNow = st.vest;
    // угол показа: в портрете 'side' или 'q45', иначе из timeline поворотов; во время поворота герой «схлопывается» по ширине
    let view = portraitAngle || st.ang.v, turnK = 1;
    if (!portraitAngle && st.ang.dur > 0 && st.ang.lt >= 0 && st.ang.lt < st.ang.dur) {
      const u = st.ang.lt / st.ang.dur;
      view = u < 0.5 ? st.ang.prev : st.ang.v;
      turnK = Math.max(0.1, Math.abs(Math.cos(Math.PI * u)));
    }
    const back = view === 'back' && isMain(def), q45 = view === 'q45';
    // В водительских позах персонаж находится внутри машины: оставляем только верх тела.
    const inVehicle = ['drive', 'drive_rev', 'drive_sink'].includes(st.pname);
    // сверление со спины: инструмент направлен от камеры. Руки сведены у груди за торсом, предмет не виден, тело мелко дрожит
    if (back && st.pname === 'drill') {
      const j = Math.sin(t * 72) * 1.6, sxn = this._bodyGeo(st).sxn;
      st = Object.assign({}, st, { L: [-sxn + 6 + j, 70 + j], R: [-sxn + 6 - j, 64], by: (st.by || 0) + Math.sin(t * 61) * 1.4 });
    }
    const C = this.C;
    ctx.save();
    ctx.translate(st.x, GROUND + st.y);
    const sh = 1 - clamp(-st.air / 400, 0, 0.6);
    if (!inVehicle && !st.roll) {
      ctx.fillStyle = 'rgba(0,0,0,0.24)';
      ctx.beginPath(); ctx.ellipse(0, 6, 84 * sh, 17 * sh, 0, 0, Math.PI * 2); ctx.fill();
    }
    if (st.roll) ctx.rotate(rad(st.roll) * st.face);   // лёжа: поворот всего тела вокруг ступней
    ctx.scale((st.face / Math.sqrt(st.sq)) * turnK * (q45 ? 0.9 : 1), def.sy * st.sq);
    ctx.translate(0, st.air);
    ctx.lineCap = 'round'; ctx.lineJoin = 'round';

    if (back && !inVehicle) {
      ctx.save();
      ctx.translate(0, g.hipY);
      ctx.rotate(rad(st.lean));
      this._arm(ctx, st, g, 'L', t);
      this._arm(ctx, st, g, 'R', t);
      ctx.restore();
    }

    // Ноги и обувь не рисуем, когда герой сидит в машине.
    if (!inVehicle) {
      const hipX = 30;
      for (const side of [-1, 1]) {
      const leg = side < 0 ? st.legs.L : st.legs.R;
      const hx = side * hipX, hy = g.hipY;
      const fx = leg.x, fy = -leg.lift - st.air * 0.0;
      const r = st.roll ? ik(hx, hy + 4, hx, hy + 4 + LEG * 2 * 0.998, LEG, LEG, side, 1, 0.1) : ik(hx, hy + 4, fx, fy, LEG, LEG, side, 1, 0.1);
      this._limb(ctx, [hx, hy + 4], [r.ex, r.ey], [r.hx, r.hy], 38, def.pants);
      ctx.fillStyle = def.shoe; ctx.strokeStyle = OUT; ctx.lineWidth = 6;
        ctx.beginPath(); ctx.ellipse(r.hx + (back ? 0 : 8), r.hy - 4, back ? 30 : 36, back ? 22 : 19, 0, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
      }
    }

    // верх тела (в системе бёдер, с наклоном)
    ctx.save();
    ctx.translate(0, g.hipY);
    ctx.rotate(rad(st.lean));
    const tw = def.tw;
    // со спины всё, что руки держат перед телом, закрыто торсом: такие руки (и предмет в них) рисуем ДО торса
    const hid = { L: false, R: false };
    if (back) for (const hand of ['L', 'R']) {
      const side = hand === 'L' ? -1 : 1, tgt = hand === 'L' ? st.L : st.R, sx = side * g.sxn;
      const r = ik(sx, SHOULDER_Y, sx + side * tgt[0], SHOULDER_Y + tgt[1], UARM, FARM, side, 0.8, 0.6);
      const held = lastBefore((C.chars[st.id].holds || []).filter(h => h.hand === hand), t);
      // Со спины предмет в руке и сама рука находятся на дальней стороне торса.
      // Рисуем их до торса, чтобы корпус естественно перекрывал предмет.
      hid[hand] = !!(held && held.id) || (Math.abs(r.hx) < tw / 2 - 6 && r.hy > -190 && r.hy < 40);
    }
    if (!back) {
      this._torso(ctx, def.kind, def, tw, back);
      // В машине руки и удерживаемые предметы скрыты; остаются только торс и голова.
      if (!inVehicle) for (const hand of ['L', 'R']) this._arm(ctx, st, g, hand, t);
    } else {
      // При back руки и предмет уже нарисованы под ногами и торсом.
      this._torso(ctx, def.kind, def, tw, back);
    }

    // голова
    ctx.save();
    ctx.translate(0, -200); ctx.rotate(rad(st.head)); ctx.translate(0, -80);
    this._head(ctx, st, def.kind, def, t, back ? 'back' : (q45 ? 'q45' : 'side'));
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
  _torso(ctx, id, def, tw, back) {
    ctx.lineWidth = 6; ctx.strokeStyle = OUT; ctx.lineJoin = 'round';
    // шея
    ctx.fillStyle = def.skin; rr(ctx, -16, -214, 32, 28, 8); ctx.fill(); ctx.stroke();
    if (back && (id === 'eng' || id === 'bld')) return this._torsoBack(ctx, id, def, tw);
    if (id === 'eng' && def.pj) {
      ctx.fillStyle = def.shirt; rr(ctx, -tw / 2, -198, tw, 216, 28); ctx.fill(); ctx.stroke();
      ctx.fillStyle = def.stripe || '#dfe8ff';
      for (let x = -tw / 2 + 12; x < tw / 2 - 6; x += 24) ctx.fillRect(x, -190, 8, 200);
      ctx.strokeStyle = def.stripe || '#dfe8ff'; ctx.lineWidth = 8; ctx.beginPath(); ctx.moveTo(-26, -198); ctx.lineTo(0, -150); ctx.lineTo(26, -198); ctx.stroke();
      ctx.strokeStyle = OUT; ctx.lineWidth = 6; ctx.beginPath(); ctx.moveTo(0, -150); ctx.lineTo(0, 10); ctx.stroke();
      ctx.fillStyle = '#fff'; for (const y of [-120, -70, -20]) { ctx.beginPath(); ctx.arc(0, y, 6, 0, Math.PI * 2); ctx.fill(); ctx.stroke(); }
      ctx.fillStyle = def.pants; rr(ctx, -tw / 2 + 2, 2, tw - 4, 16, 6); ctx.fill(); ctx.stroke();
    } else if (id === 'eng') {
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
      ctx.fillStyle = (this._vestNow && this._vestNow.color) || '#ff7a1a'; rr(ctx, -tw / 2 + 2, -196, tw - 4, 200, 24); ctx.fill(); ctx.stroke();
      ctx.fillStyle = def.shirt;
      ctx.beginPath(); ctx.moveTo(-30, -198); ctx.lineTo(30, -198); ctx.lineTo(0, -146); ctx.closePath(); ctx.fill(); ctx.stroke();
      // световозвращающие полосы
      ctx.fillStyle = (this._vestNow && this._vestNow.stripe) || '#e8f27a';
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
  // спина: без галстука, кармана и V-выреза
  _torsoBack(ctx, id, def, tw) {
    ctx.lineWidth = 6; ctx.strokeStyle = OUT; ctx.lineJoin = 'round';
    ctx.fillStyle = def.shirt; rr(ctx, -tw / 2, -198, tw, 216, 28); ctx.fill(); ctx.stroke();
    if (id === 'eng' && def.pj) {
      ctx.fillStyle = def.stripe || '#dfe8ff';
      for (let x = -tw / 2 + 12; x < tw / 2 - 6; x += 24) ctx.fillRect(x, -190, 8, 200);
      ctx.strokeStyle = OUT; ctx.lineWidth = 6; ctx.beginPath(); ctx.moveTo(0, -160); ctx.lineTo(0, -4); ctx.stroke();
      ctx.fillStyle = def.pants; rr(ctx, -tw / 2 + 2, 2, tw - 4, 16, 6); ctx.fill(); ctx.stroke();
    } else if (id === 'eng') {
      ctx.fillStyle = '#fff'; rr(ctx, -34, -210, 68, 24, 10); ctx.fill(); ctx.stroke();            // воротник сзади
      ctx.strokeStyle = 'rgba(30,27,38,.35)'; ctx.lineWidth = 4;
      ctx.beginPath(); ctx.moveTo(-tw / 2 + 6, -150); ctx.quadraticCurveTo(0, -176, tw / 2 - 6, -150); ctx.stroke();  // кокетка
      ctx.beginPath(); ctx.moveTo(0, -160); ctx.lineTo(0, -4); ctx.stroke();                         // шов по центру
      ctx.strokeStyle = OUT; ctx.lineWidth = 6;
      ctx.fillStyle = '#2a2f3d'; rr(ctx, -tw / 2 + 2, 2, tw - 4, 16, 6); ctx.fill(); ctx.stroke();
      ctx.fillStyle = '#1b1f2a'; for (const x of [-46, -16, 16, 46]) rr(ctx, x - 4, 0, 8, 20, 2), ctx.fill();
    } else {
      ctx.fillStyle = (this._vestNow && this._vestNow.color) || '#ff7a1a'; rr(ctx, -tw / 2 + 2, -196, tw - 4, 200, 24); ctx.fill(); ctx.stroke();
      ctx.fillStyle = (this._vestNow && this._vestNow.stripe) || '#e8f27a'; ctx.lineWidth = 4;
      for (const y of [-118, -66]) { ctx.fillRect(-tw / 2 + 4, y, tw - 8, 14); ctx.strokeRect(-tw / 2 + 4, y, tw - 8, 14); }
      for (const x of [-34, 20]) { ctx.fillRect(x, -192, 14, 192); ctx.strokeRect(x, -192, 14, 192); }   // вертикальные лямки сзади
      ctx.lineWidth = 6;
      ctx.fillStyle = def.shirt; ctx.beginPath(); ctx.moveTo(-34, -198); ctx.lineTo(34, -198); ctx.lineTo(0, -176); ctx.closePath(); ctx.fill(); ctx.stroke();
      ctx.fillStyle = '#3b2e22'; rr(ctx, -tw / 2 + 2, 2, tw - 4, 16, 6); ctx.fill(); ctx.stroke();
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
      if (P && ps.vis && ps.held && !st.hideHeld) {
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
  _head(ctx, st, id, def, t, ang) {
    ctx.lineWidth = 6; ctx.strokeStyle = OUT; ctx.fillStyle = def.skin;
    if (ang === 'back') return this._headBack(ctx, id, def);
    const q = ang === 'q45';
    // уши (в три четверти дальнее ухо прячется за головой)
    if (!q) for (const s of [-1, 1]) { ctx.beginPath(); ctx.arc(s * 76, 6, 15, 0, Math.PI * 2); ctx.fill(); ctx.stroke(); }   // в три четверти уши не рисуем
    ctx.beginPath(); ctx.arc(0, 0, 77, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
    // блик
    ctx.save(); ctx.globalAlpha = 0.22; ctx.fillStyle = '#fff';
    ctx.beginPath(); ctx.ellipse(-32, -38, 22, 13, -0.6, 0, Math.PI * 2); ctx.fill(); ctx.restore();

    if (q) { ctx.save(); ctx.translate(15, 0); ctx.scale(0.78, 1); }
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
    if (q) ctx.restore();
    // каска строителя
    if (id === 'bld' && q) {
      // каска в три четверти: купол сдвинут и сужен, козырёк вынесен вперёд, центральная полоса изогнута по куполу
      ctx.save(); ctx.translate(12, 0);
      ctx.lineWidth = 6; ctx.strokeStyle = OUT; ctx.fillStyle = '#ffc61a';
      ctx.beginPath(); ctx.moveTo(-72, -48); ctx.quadraticCurveTo(-76, -118, 4, -122); ctx.quadraticCurveTo(78, -118, 74, -48); ctx.closePath(); ctx.fill(); ctx.stroke();
      // центральная полоса: заходит под купол и обрезается его контуром, края изогнуты по кривизне каски
      ctx.save();
      ctx.beginPath(); ctx.moveTo(-72, -48); ctx.quadraticCurveTo(-76, -118, 4, -122); ctx.quadraticCurveTo(78, -118, 74, -48); ctx.closePath(); ctx.clip();
      ctx.fillStyle = '#ffd95c';
      ctx.beginPath(); ctx.moveTo(47, -52); ctx.quadraticCurveTo(45, -100, 28, -132); ctx.lineTo(-46, -138); ctx.quadraticCurveTo(-22, -128, -2, -112); ctx.quadraticCurveTo(18, -96, 21, -52); ctx.closePath(); ctx.fill();
      ctx.strokeStyle = OUT; ctx.lineWidth = 6; ctx.lineCap = 'butt';
      ctx.beginPath(); ctx.moveTo(47, -52); ctx.quadraticCurveTo(45, -100, 28, -132); ctx.stroke();
      ctx.beginPath(); ctx.moveTo(21, -52); ctx.quadraticCurveTo(18, -96, -2, -112); ctx.quadraticCurveTo(-22, -128, -46, -138); ctx.stroke();
      ctx.restore();
      ctx.beginPath(); ctx.moveTo(-72, -48); ctx.quadraticCurveTo(-76, -118, 4, -122); ctx.quadraticCurveTo(78, -118, 74, -48); ctx.closePath(); ctx.stroke();
      ctx.fillStyle = '#e6a800'; ctx.strokeStyle = OUT; ctx.lineWidth = 6;
      ctx.beginPath(); ctx.moveTo(-70, -58); ctx.lineTo(86, -58); ctx.quadraticCurveTo(114, -58, 114, -49); ctx.quadraticCurveTo(114, -40, 86, -40); ctx.lineTo(-70, -40); ctx.quadraticCurveTo(-82, -40, -82, -49); ctx.quadraticCurveTo(-82, -58, -70, -58); ctx.closePath(); ctx.fill(); ctx.stroke();
      ctx.save(); ctx.globalAlpha = 0.35; ctx.fillStyle = '#fff'; ctx.beginPath(); ctx.ellipse(-30, -88, 16, 8, -0.5, 0, Math.PI * 2); ctx.fill(); ctx.restore();
      ctx.restore();
    } else if (id === 'bld') {
      ctx.save();
      ctx.lineWidth = 6; ctx.strokeStyle = OUT;
      ctx.fillStyle = '#ffc61a';
      ctx.beginPath(); ctx.moveTo(-84, -48); ctx.quadraticCurveTo(-90, -118, 0, -122); ctx.quadraticCurveTo(90, -118, 84, -48); ctx.closePath(); ctx.fill(); ctx.stroke();
      ctx.fillStyle = '#ffd95c'; rr(ctx, -12, -122, 24, 60, 8); ctx.fill(); ctx.stroke();
      ctx.fillStyle = '#e6a800'; rr(ctx, -96, -58, 192, 18, 9); ctx.fill(); ctx.stroke();
      ctx.save(); ctx.globalAlpha = 0.35; ctx.fillStyle = '#fff'; ctx.beginPath(); ctx.ellipse(-48, -86, 20, 9, -0.5, 0, Math.PI * 2); ctx.fill(); ctx.restore();
      ctx.restore();
    }
    if (id === 'extra') {
      if (def.hat) this._cap(ctx, def.hat);
      if (def.head_front && def.head_front.length) drawShapes(ctx, def.head_front, this._t || 0, k => this.T(k));
    }
  }
  // затылок: без лица, очки видны дужками, каска со стороны затылка
  _headBack(ctx, id, def) {
    ctx.lineWidth = 6; ctx.strokeStyle = OUT; ctx.fillStyle = def.skin;
    for (const s of [-1, 1]) { ctx.beginPath(); ctx.arc(s * 76, 6, 15, 0, Math.PI * 2); ctx.fill(); ctx.stroke(); }
    ctx.beginPath(); ctx.arc(0, 0, 77, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
    ctx.save(); ctx.fillStyle = 'rgba(0,0,0,.07)'; ctx.beginPath(); ctx.ellipse(0, 46, 54, 22, 0, 0, Math.PI * 2); ctx.fill(); ctx.restore();
    if (id === 'eng') {
      ctx.strokeStyle = '#20242c'; ctx.lineWidth = 8; ctx.lineCap = 'round';
      for (const s of [-1, 1]) { ctx.beginPath(); ctx.moveTo(s * 66, -8); ctx.quadraticCurveTo(s * 86, -4, s * 84, 14); ctx.stroke(); }
      ctx.save(); ctx.globalAlpha = 0.22; ctx.fillStyle = '#fff'; ctx.beginPath(); ctx.ellipse(-30, -38, 22, 13, -0.6, 0, Math.PI * 2); ctx.fill(); ctx.restore();
    } else if (id === 'bld') {
      ctx.lineWidth = 6; ctx.strokeStyle = OUT; ctx.fillStyle = '#ffc61a';
      ctx.beginPath(); ctx.moveTo(-86, -26); ctx.quadraticCurveTo(-92, -118, 0, -122); ctx.quadraticCurveTo(92, -118, 86, -26); ctx.quadraticCurveTo(60, -6, 0, -4); ctx.quadraticCurveTo(-60, -6, -86, -26); ctx.closePath(); ctx.fill(); ctx.stroke();
      ctx.fillStyle = '#ffd95c'; rr(ctx, -12, -122, 24, 100, 8); ctx.fill(); ctx.stroke();
      ctx.fillStyle = '#e6a800'; rr(ctx, -92, -34, 184, 16, 8); ctx.fill(); ctx.stroke();
      ctx.fillStyle = '#4a4f5a'; rr(ctx, -30, -22, 60, 22, 8); ctx.fill(); ctx.stroke();                // храповик затылочного ремня
      ctx.save(); ctx.globalAlpha = 0.35; ctx.fillStyle = '#fff'; ctx.beginPath(); ctx.ellipse(-48, -86, 20, 9, -0.5, 0, Math.PI * 2); ctx.fill(); ctx.restore();
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

const api = { Engine, W, H, GROUND, POSE_NAMES, EMO_NAMES, FX_KINDS, EASE_NAMES, SHAPE_TYPES, CHAR_IDS, LOOK_KEYS, CALLOUT_STYLES, DEFAULT_VIEW, ANGLES, PORTRAIT_ANGLES };
if (typeof module !== 'undefined' && module.exports) module.exports = api;
else root.Mult = api;
})(typeof window !== 'undefined' ? window : globalThis);
