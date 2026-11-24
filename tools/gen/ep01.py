"""Эпизод 1 «Изменение №10»: предметы (в library.json), 4 сцены, тексты ru, сценарий в scripts/.
Запуск: python3 ep01.py <корень репозитория>
Библиотека и манифест не перезаписываются, а дополняются."""
import json, math, os, sys

ROOT = sys.argv[1]
DK = "#1e1b26"


def fmt(o, ind=0, maxw=118):
    s = json.dumps(o, ensure_ascii=False, separators=(', ', ': '))
    if len(s) <= maxw or not isinstance(o, (dict, list)):
        return s
    pad = '  ' * (ind + 1)
    if isinstance(o, dict):
        items = [pad + json.dumps(k, ensure_ascii=False) + ': ' + fmt(v, ind + 1) for k, v in o.items()]
        return '{\n' + ',\n'.join(items) + '\n' + '  ' * ind + '}'
    items = [pad + fmt(v, ind + 1) for v in o]
    return '[\n' + ',\n'.join(items) + '\n' + '  ' * ind + ']'


def write(path, obj):
    p = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, 'w', encoding='utf-8') as f:
        f.write(fmt(obj) + '\n')


def shp(t, **kw):
    d = {"t": t}
    d.update({k: v for k, v in kw.items() if v is not None})
    return d


def R(x, y, w, h, fill=None, stroke=None, sw=None, r=None, **kw):
    return shp("rect", x=x, y=y, w=w, h=h, fill=fill, stroke=stroke, sw=sw, r=r, **kw)


def LN(x1, y1, x2, y2, stroke, sw=4, **kw):
    return shp("line", x1=x1, y1=y1, x2=x2, y2=y2, stroke=stroke, sw=sw, **kw)


def PL(pts, fill=None, stroke=None, sw=None, **kw):
    return shp("poly", pts=pts, fill=fill, stroke=stroke, sw=sw, **kw)


def E(x, y, rx, ry, fill=None, **kw):
    return shp("ellipse", x=x, y=y, rx=rx, ry=ry, fill=fill, **kw)


def G(shapes, **kw):
    return shp("g", x=0, y=0, shapes=shapes, **kw)


# ───────────────────────── предметы ─────────────────────────
def brick_wall():
    sh = [E(0, 4, 215, 13, "rgba(0,0,0,0.25)"), R(-190, -432, 380, 432, "#c4553a", DK, 5)]
    for i in range(1, 12):
        sh.append(LN(-188, -432 + 36 * i, 188, -432 + 36 * i, "#8f4528", 3))
    for i in range(12):
        y0 = -432 + 36 * i
        x = -190 + (0 if i % 2 == 0 else 38) + 76
        while x < 190:
            sh.append(LN(x, y0, x, y0 + 36, "#8f4528", 3))
            x += 76
    sh += [R(-186, -428, 372, 10, "rgba(255,255,255,0.12)"), R(-202, -454, 404, 22, "#9aa0a8", DK, 5, r=4)]
    # окно в стене (справа)
    sh += [R(40, -340, 100, 120, ["#32406a", "#1d2338"]), PL([[52, -330], [86, -330], [54, -286]], "rgba(255,255,255,0.18)"),
           R(36, -344, 108, 128, None, "#e8e6df", 9, r=3), LN(90, -344, 90, -216, "#e8e6df", 6), LN(36, -280, 144, -280, "#e8e6df", 6),
           R(26, -216, 128, 13, "#c9ced4", DK, 4, r=3), R(24, -358, 132, 14, "#9aa0a8", DK, 4, r=3)]
    return {"grip": [0, 0], "shapes": sh}


def win_new():
    sh = [R(-50, -340, 100, 120, "rgba(229,52,43,0.22)", "#e5342b", 10, r=4, dash=[22, 10]),
          LN(96, -384, 30, -384, "#e5342b", 12), PL([[34, -410], [-6, -384], [34, -358]], "#e5342b", "#e5342b", 4)]
    return {"grip": [0, 0], "shapes": [G(sh, anim={"k": "blink", "s": 1.2, "a": 0.6})]}


def wall_hole():
    pts = [[-62, -8], [-40, -50], [-12, -42], [6, -72], [34, -46], [64, -28], [50, 6], [66, 36], [22, 50], [2, 68], [-26, 46], [-58, 54], [-46, 22]]
    inner = [[round(x * 0.66), round(y * 0.66)] for x, y in pts]
    sh = [PL(pts, "#4a3029", DK, 5), PL(inner, "#241512"),
          R(-86, -26, 20, 11, "#c4553a", DK, 3), R(62, -48, 20, 11, "#c4553a", DK, 3), R(64, 24, 22, 11, "#c4553a", DK, 3),
          R(-18, 62, 22, 11, "#c4553a", DK, 3), R(-4, -92, 20, 11, "#c4553a", DK, 3),
          LN(-62, -8, -112, -22, DK, 4), LN(64, -28, 114, -50, DK, 4), LN(66, 36, 110, 62, DK, 4), LN(2, 68, 12, 106, DK, 4), LN(6, -72, -2, -106, DK, 4)]
    return {"grip": [0, 0], "shapes": sh}


lib_path = os.path.join(ROOT, 'library.json')
lib = json.load(open(lib_path, encoding='utf-8'))
lib['props']['brick_wall'] = brick_wall()
lib['props']['win_new'] = win_new()
lib['props']['wall_hole'] = wall_hole()
write('library.json', lib)

# ───────────────────────── реплики ─────────────────────────
LINES = {
    "l1": ("bld", "Ровная, как по линейке. Хоть на выставку."),
    "l2": ("eng", "Отличная новость! Изменение проекта!"),
    "l3": ("bld", "Какое по счёту?"),
    "l4": ("eng", "Ну... десятое."),
    "l5": ("bld", "А я, между прочим, по девятому построил."),
    "l6": ("eng", "Да ерунда! Там окно сдвинулось. На полметра."),
    "l7": ("bld", "Так. Дай-ка сюда."),
    "l8": ("bld", "Это не окно. Это вся стена!"),
    "l9": ("eng", "Зато окно теперь по центру!"),
    "l10": ("bld", "Опять разбирать?"),
    "l11": ("eng", "Зачем сразу разбирать? Я сфотографирую. Для отчёта."),
    "l12": ("bld", "Сфотографируй лучше моё терпение."),
    "l13": ("eng", "Терпение... записал. Приложу к отчёту."),
    "l14": ("bld", "Ладно. Давай сюда своё десятое."),
    "l15": ("eng", "Вот и славно! Пойду дорисую одиннадцатое."),
    "l16": ("bld", "Одиннадцатое... Ну конечно."),
}
TITLES = {"title_continue": "Продолжение следует..."}
CPS = 14


def dur(lid):
    return math.ceil((len(LINES[lid][1]) / CPS + 0.3) * 10 - 1e-9) / 10


class S:
    def __init__(self, sid):
        self.id, self.b, self.says = sid, [], []

    def a(self, t, do, **kw):
        d = {"t": round(t, 2), "do": do}
        d.update(kw)
        self.b.append(d)

    def say(self, t, lid):
        who = LINES[lid][0]
        self.a(t, "say", who=who, line=lid, dur=dur(lid))
        self.says.append((round(t, 2), round(t + dur(lid), 2), lid))
        return round(t + dur(lid), 2)

    def props(self, hammer_for="bld", plan=None, hand_plan="R", plan_layer="front"):
        self.a(0, "spawn", id="wall", prop="brick_wall", x=860)
        self.a(0, "spawn", id="hm", prop="hammer", x=0)
        self.a(0, "hold", who="bld", id="hm")
        if plan:
            self.a(0, "spawn", id="pl", prop="plan", x=0, layer=plan_layer)
            self.a(0, "hold", who=plan[0], id="pl", hand=hand_plan)

    def out(self, start, duration):
        return {"id": self.id, "duration": duration, "start": start, "beats": self.b}


# ───────────────────────── s01 ─────────────────────────
def s01():
    s = S("ep01_s01")
    s.a(0, "spawn", id="wall", prop="brick_wall", x=860)
    s.a(0, "spawn", id="hm", prop="hammer", x=0)
    s.a(0, "hold", who="bld", id="hm")
    s.a(0, "spawn", id="rl", prop="roll", x=0)
    s.a(0, "hold", who="eng", id="rl")
    s.a(0, "pose", who="bld", pose="present", dur=1.4)
    s.a(0, "emote", who="bld", emotion="happy", dur=3.6)
    s.say(0.5, "l1")
    s.a(1.4, "place", who="eng", x=-170, face="right")
    s.a(1.5, "walk", who="eng", x=280, dur=2.0)
    s.a(1.5, "emote", who="eng", emotion="happy", dur=2.4)
    s.a(1.9, "pose", who="bld", pose="tired", dur=1.8)
    s.a(3.8, "face", who="bld", dir="eng")
    s.a(4.0, "remove", id="rl")
    s.a(4.0, "spawn", id="pl", prop="plan", x=0, layer="back")
    s.a(4.0, "hold", who="eng", id="pl")
    s.a(4.0, "pose", who="eng", pose="present", dur=3.0)
    s.a(4.1, "emote", who="eng", emotion="happy", dur=3.0)
    s.say(4.1, "l2")
    s.a(7.3, "emote", who="bld", emotion="confused", dur=2.7)
    s.a(7.3, "fx", kind="question", on="bld", dur=1.4)
    s.say(7.3, "l3")
    s.a(9.0, "emote", who="eng", emotion="worried", dur=2.4)
    s.say(9.0, "l4")
    s.a(9.0, "release", id="pl", drop=False)
    s.a(9.0, "move", id="pl", x=205, y=1090, dur=0.3, ease="easeOut")
    s.a(9.2, "fx", kind="sweat", on="eng", dur=1.6)
    s.a(10.6, "pose", who="bld", pose="angry")
    s.a(10.6, "emote", who="bld", emotion="angry")
    s.a(10.6, "camera", on="bld", focus="face", zoom=1.5, dur=1.6, ease="easeIn")
    s.a(10.8, "shake", dur=1.5, amp=3)
    return s, s.out({"location": "construction_site", "chars": {"bld": {"x": 640, "face": "right"}}}, 12.6)


# ───────────────────────── s02 ─────────────────────────
def s02():
    s = S("ep01_s02")
    s.props(plan=("eng",))
    s.a(0.2, "pose", who="bld", pose="point", dur=1.7)
    s.a(1.9, "pose", who="bld", pose="present", dur=1.8)
    s.a(0.2, "emote", who="bld", emotion="angry", dur=3.6)
    s.say(0.4, "l5")
    s.a(0.3, "emote", who="eng", emotion="worried", dur=3.3)
    s.a(3.8, "face", who="bld", dir="eng")
    s.a(3.8, "pose", who="eng", pose="shrug", dur=1.5)
    s.a(3.8, "emote", who="eng", emotion="smug", dur=3.6)
    s.say(3.8, "l6")
    s.a(5.4, "pose", who="eng", pose="point", dur=1.9)
    s.a(5.3, "camera", x=700, y=1000, zoom=1.3, dur=0.6)
    s.a(5.5, "spawn", id="nw", prop="win_new", x=860, layer="back")
    s.a(7.4, "camera", reset=True, dur=0.5)
    s.a(7.6, "walk", who="bld", x=520, dur=0.7)
    s.say(7.6, "l7")
    s.a(8.4, "release", id="pl", drop=False)
    s.a(8.4, "hold", who="bld", id="pl", hand="L")
    s.a(9.2, "pose", who="bld", pose="measure", dur=1.3)
    s.a(9.2, "emote", who="bld", emotion="confused", dur=1.3)
    s.a(10.6, "camera", on="bld", focus="face", zoom=1.5, dur=0.4)
    s.a(10.6, "emote", who="bld", emotion="shocked", dur=2.4)
    s.a(10.6, "pose", who="bld", pose="angry", dur=2.4)
    s.a(10.6, "shake", dur=0.35, amp=10)
    s.a(10.7, "fx", kind="exclaim", on="bld", dur=1.2)
    s.say(10.6, "l8")
    s.a(13.1, "camera", on="eng", focus="head", zoom=1.5, dur=0.4)
    s.a(13.1, "walk", who="eng", x=210, dur=0.6, face="keep")
    s.a(13.1, "emote", who="eng", emotion="worried", dur=2.6)
    s.a(13.1, "pose", who="eng", pose="shrug", dur=2.0)
    s.a(13.1, "fx", kind="sweat", on="eng", dur=2.4)
    s.say(13.3, "l9")
    return s, s.out({"location": "construction_site", "chars": {"eng": {"x": 280, "face": "right"}, "bld": {"x": 640, "face": "right"}}}, 15.8)


# ───────────────────────── s03 ─────────────────────────
def s03():
    s = S("ep01_s03")
    s.props(plan=("bld",), hand_plan="L")
    s.a(0, "emote", who="bld", emotion="tired", dur=2.8)
    s.a(0.2, "pose", who="bld", pose="present", dur=0.9)
    s.a(0.6, "release", id="pl", drop=False)
    s.a(0.6, "move", id="pl", x=500, y=1080, dur=0.35, arc=30, ease="easeOut")
    s.a(0.95, "hold", who="eng", id="pl")
    s.a(1.2, "pose", who="bld", pose="point", dur=1.4)
    s.a(1.2, "emote", who="bld", emotion="sad", dur=1.6)
    s.say(1.2, "l10")
    s.a(2.8, "spawn", id="ph", prop="phone", x=-300)
    s.a(2.8, "hold", who="eng", id="ph", hand="L")
    s.a(2.8, "face", who="eng", dir="right")
    s.a(2.9, "pose", who="eng", pose="measure", dur=4.0)
    s.a(2.9, "emote", who="eng", emotion="smug", dur=4.0)
    s.say(2.9, "l11")
    s.a(5.9, "fx", kind="flash", dur=0.25)
    s.a(7.1, "camera", on="bld", focus="face", zoom=1.7, dur=0.5)
    s.a(7.1, "emote", who="bld", emotion="confused", dur=1.8)
    s.a(7.1, "pose", who="bld", pose="arms_cross", dur=1.8)
    s.a(8.9, "emote", who="bld", emotion="tired", dur=2.9)
    s.a(8.9, "pose", who="bld", pose="facepalm", dur=2.8)
    s.say(8.9, "l12")
    s.a(11.8, "camera", reset=True, dur=0.4)
    s.a(12.0, "remove", id="ph")
    s.a(12.1, "pose", who="eng", pose="write", dur=3.1)
    s.a(12.1, "emote", who="eng", emotion="smug", dur=3.1)
    s.say(12.1, "l13")
    s.a(13.6, "emote", who="bld", emotion="angry")
    s.a(14.4, "pose", who="bld", pose="point_up")
    return s, s.out({"location": "construction_site", "chars": {"bld": {"x": 330, "face": "right"}, "eng": {"x": 560, "face": "left"}}}, 15.6)


# ───────────────────────── s04 ─────────────────────────
def s04():
    s = S("ep01_s04")
    s.props(plan=("eng",))
    s.a(0, "pose", who="bld", pose="point_up", dur=1.0)
    s.a(0, "emote", who="bld", emotion="angry", dur=1.0)
    s.a(1.0, "pose", who="bld", pose="idle")
    s.a(1.0, "emote", who="bld", emotion="tired", dur=3.4)
    s.say(1.4, "l14")
    s.a(4.3, "emote", who="eng", emotion="happy", dur=3.4)
    s.a(4.3, "pose", who="eng", pose="present", dur=1.4)
    s.say(4.3, "l15")
    s.a(5.9, "walk", who="eng", x=-170, dur=2.6)
    s.a(8.6, "hide", who="eng")
    s.a(8.0, "face", who="bld", dir="right")
    s.a(8.0, "emote", who="bld", emotion="sad", dur=2.5)
    s.say(8.0, "l16")
    s.a(10.4, "camera", on="bld", focus="body", zoom=1.35, dx=110, dur=0.7)
    s.a(10.4, "walk", who="bld", x=590, dur=0.6, face="right")
    H0 = 11.0
    s.a(H0, "pose", who="bld", pose="hammer", dur=4.0)
    s.a(H0, "emote", who="bld", emotion="tired", dur=4.0)
    land = [720, 770, 850, 930, 990, 880]
    for k in range(6):
        t = round(H0 + 0.327 + 0.4545 * k, 2)
        s.a(t, "fx", kind="dust", x=775, y=1040, dur=0.7)
        s.a(t, "shake", dur=0.15, amp=5)
        if k in (0, 2, 4):
            s.a(t, "spawn", id="h%d" % k, prop="wall_hole", x=780, y=1040, scale=[0.6, 1.0, 1.5][k // 2], layer="back")
        if k < 5:
            s.a(t, "spawn", id="fb%d" % k, prop="brick", x=790, y=1030, layer="front")
            s.a(t, "move", id="fb%d" % k, x=land[k], y=1254, dur=0.55, arc=150 + 20 * k, ease="easeOut", rot=[35, -40, 20, -25, 50][k])
    s.a(12.7, "title", key="title_continue", dur=2.2, pos="top", style="shake")
    return s, s.out({"location": "construction_site", "chars": {"bld": {"x": 360, "face": "right"}, "eng": {"x": 600, "face": "left"}}}, 15.0)


# ───────────────────────── запись ─────────────────────────
scenes = [s01(), s02(), s03(), s04()]
total = 0
for s, sc in scenes:
    write('scenes/%s.json' % sc["id"], sc)
    total += sc["duration"]

write('lang/ep01.ru.json', {"lang": "ru", "cps": CPS, "lines": {**{k: v[1] for k, v in LINES.items()}, **TITLES}})

mp = os.path.join(ROOT, 'manifest.json')
man = json.load(open(mp, encoding='utf-8'))
man['scenes'] = [x for x in man['scenes'] if not x['id'].startswith('ep01_')]
names = {"ep01_s01": "Изм. №10 · s01 · Стена готова", "ep01_s02": "Изм. №10 · s02 · Окно сдвинулось",
         "ep01_s03": "Изм. №10 · s03 · Фото для отчёта", "ep01_s04": "Изм. №10 · s04 · Одиннадцатое"}
for s, sc in scenes:
    man['scenes'].append({"id": sc["id"], "title": names[sc["id"]], "file": "scenes/%s.json" % sc["id"], "langs": {"ru": "lang/ep01.ru.json"}})
write('manifest.json', man)

# сценарий (для озвучки)
rows = []
for s, sc in scenes:
    for t0, t1, lid in s.says:
        who = LINES[lid][0]
        rows.append("| %s | %s | %s | %s | %.1f |" % (lid, "Инженер" if who == "eng" else "Строитель", sc["id"][-3:], LINES[lid][1], dur(lid)))
md = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ep01_script.md'), encoding='utf-8').read()
md = md.replace("{{LINES}}", "\n".join(rows)).replace("{{TOTAL}}", "%.1f" % total)
os.makedirs(os.path.join(ROOT, 'scripts'), exist_ok=True)
open(os.path.join(ROOT, 'scripts', 'ep01_izmenenie10.md'), 'w', encoding='utf-8').write(md)
print("ok, total %.1f s" % total)
for s, sc in scenes:
    print(sc["id"], sc["duration"], [(a, b, l) for a, b, l in s.says])
