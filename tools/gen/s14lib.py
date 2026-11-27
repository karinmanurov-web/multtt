import json,math
exec(open('s5lib.py').read().split("random.seed(5)")[0])
PR=lib['props']
def pr(n,sh,grip=(0,0),upright=True):
    d={"grip":list(grip),"shapes":sh}
    if upright: d["upright"]=True
    PR[n]=d
# ───── Пиксель — наш пиксельный помощник-«чат» (оригинальный персонаж) ─────
PAL={'a':'#ff9f43','s':'#e07a1f','o':'#fff1a8','W':'#ffffff','B':'#2b2f3a','M':'#7a2e12','c':'#ffe3c2','b':'#6b3a1e'}
def grid(rows,cell=22,ox=None,oy=None,glow=False):
    h=len(rows); w=len(rows[0]); ox=-w*cell/2 if ox is None else ox; oy=-h*cell if oy is None else oy
    out=[]
    for r,row in enumerate(rows):
        for c,ch in enumerate(row):
            if ch!='.': out.append(R(ox+c*cell-4,oy+r*cell-4,cell+8,cell+8,'#2b2f3a',0,None,0))
    for r,row in enumerate(rows):
        for c,ch in enumerate(row):
            if ch!='.': out.append(R(ox+c*cell,oy+r*cell,cell,cell,PAL[ch],0,None,0))
    return out
STAND=["....oo....","....aa....","..aaaaaa..",".aaaaaaaa.",".aWWaaWWa.",".aWBaaWBa.",".aaaaaaaa.",".aaMMMMaa.","..aaaaaa..",".aaccccaa.","saaccccaas",".aaaaaaaa.","..aa..aa..","..bb..bb.."]
RUN=["....oo....","....aa....","..aaaaaa..",".aaaaaaaa.",".aWWaaWWa.",".aWBaaWBa.",".aaaaaaaa.",".aaMMMMaa.","..aaaaaa..",".aaccccaa.","saaccccaas",".aaaaaaaa.","..aaaaaa..","bb......bb"]
SIT=["....oo....","....aa....","..aaaaaa..",".aaaaaaaa.",".aWWaaWWa.",".aWBaaWBa.",".aaaaaaaa.",".aaMMMMaa.","..aaaaaa..",".aaccccaa.","saaccccaas",".aaaaaaaa.","bbbaaaabbb"]
pr('px_idle',grid(STAND)); pr('px_run',grid(RUN)); pr('px_sit',grid(SIT))
# ───── таймер на 5 часов: циферблат из 5 долей ─────
def timer(k,ring=False):
    s=[R(-360,-230,720,460,'#fffdf5',22,OUT,6)]
    s+=[C(-170,0,150,'#e8edf5',OUT,8)]
    for i in range(5):
        a0=-math.pi/2+i*2*math.pi/5; a1=a0+2*math.pi/5
        pts=[(-170,0)]+[(-170+138*math.cos(a0+(a1-a0)*j/8),138*math.sin(a0+(a1-a0)*j/8)) for j in range(9)]
        if i<k: s.append(P(pts,'#ff9f43',OUT,5))
    s+=[C(-170,0,12,OUT,None,0)]
    col='#e0533d' if ring else '#99a0b0'
    s+=[C(-250,-150,34,col,OUT,5),C(-90,-150,34,col,OUT,5),R(-185,-175,30,18,col,4,OUT,4)]
    if ring: s+=[L(-300,-185,-280,-165,'#e0533d',6),L(-40,-185,-60,-165,'#e0533d',6),L(-310,-130,-285,-130,'#e0533d',6),L(-35,-130,-60,-130,'#e0533d',6)]
    # справа: песочные часы (если лимита нет) / галочка
    if k==0: s+=[P([(110,-130),(250,-130),(180,0)],'#e0533d',OUT,6),P([(110,130),(250,130),(180,0)],'#e0533d',OUT,6)]
    else: s+=[P([(110,-130),(250,-130),(180,0)],'#ffe3c2',OUT,6),P([(110,130),(250,130),(180,0)],'#ffcf7a',OUT,6)]
    return s
for k in (5,3,1,0): pr(f'tm_{k}',timer(k,ring=(k==0)))
pr('tm_ring',timer(5,ring=True))
# ───── чат: пузырьки / лимит (замок) ─────
def bub(x,y,w,me): return [R(x,y,w,46,'#cfe3ff' if me else '#ffe3c2',20,OUT,5)]+[R(x+18,y+16,w-60,8,'#8a93a6',4,None,0)]
chat=[R(-360,-230,720,460,'#fffdf5',22,OUT,6)]+bub(-300,-190,300,False)+bub(0,-120,300,True)+bub(-300,-50,260,False)+bub(60,20,240,True)+bub(-300,90,200,False)
pr('chat_ok',chat)
lock=[R(-360,-230,720,460,'#fffdf5',22,OUT,6),R(-110,-30,220,170,'#e0533d',20,OUT,8),P([(-60,-30),(-60,-110),(-30,-150),(30,-150),(60,-110),(60,-30)],None,OUT,0)]
lock=[R(-360,-230,720,460,'#fffdf5',22,OUT,6),C(0,-80,70,None,OUT,22),R(-95,-30,190,150,'#e0533d',18,OUT,8),C(0,40,18,OUT,None,0),R(-6,40,12,50,OUT,3,None,0)]
pr('chat_lock',lock)
json.dump(lib,open(LIB,'w'),ensure_ascii=False,indent=2); print('ok14 props')
# ───── миска и ложка ─────
lib=json.load(open(LIB)); PR=lib['props']
pr('bowl',[E(0,-6,52,12,'#f4efe6',OUT,5),P([(-50,-8),(50,-8),(34,-46),(-34,-46)],'#f4efe6',OUT,5),E(0,-46,36,8,'#e8a23a',OUT,4),C(-12,-48,4,'#7bbf5a',None,0),C(12,-46,4,'#7bbf5a',None,0)])
pr('spoon',[R(-4,-4,8,70,'#cfd3e0',4,OUT,4),E(0,-8,13,17,'#cfd3e0',OUT,4)])
json.dump(lib,open(LIB,'w'),ensure_ascii=False,indent=2); print('ok14 bowl')
