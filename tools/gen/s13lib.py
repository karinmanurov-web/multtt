import json,math,random
exec(open('s5lib.py').read().split("random.seed(5)")[0])
PR=lib['props']
def pr(n,sh,grip=(0,0),upright=False):
    d={"grip":list(grip),"shapes":sh}
    if upright: d["upright"]=True
    PR[n]=d
CONC='#b8b3aa'; BRK='#c5694a'; BRKS='#e09a62'; MOR='#ddd7c9'; DARK='#2b2f3a'; WOOD='#d9a45b'; TILE='#a8472f'
WALL_W=820; WALL_H=340; GATE_H=270
# ───── фундаменты (начало — центр, низ = уровень земли, часть уходит под землю) ─────
def fnd(w,h,rods=0,inner=False):
    s=[R(-w/2,-10,w,h+10,CONC,8,OUT,5)]+[C(-w/2+30+((i*97)%int(w-60)),8+(i*31)%max(8,int(h-10)),4,'#9b968d',None,0) for i in range(16)]
    if inner: s+=[R(-w/2+16,y,w-32,5,'#c0522d',2,None,0) for y in (6,22,38)]
    if rods: s+=[R(-w/2-rods,y,w+2*rods,7,'#c0522d',3,OUT,3) for y in (2,16,30)]+[R(x,-4,7,44,'#c0522d',2,OUT,2) for x in (-w/2+10,w/2-17)]
    return s
pr('gf_a',fnd(880,70)); pr('gf_b',fnd(800,36)); pr('gf_c',fnd(800,36,rods=90)); pr('gf_d',fnd(1020,70,inner=True))
# ───── стена гаража: stage 0..1, кирпич bw×bh, шов mor, проём gate ─────
def wall(bw,bh,mor,gate,frac,col,W=WALL_W,H=WALL_H):
    h=H*frac; s=[R(-W/2,-h,W,h,MOR,3,OUT,5)]
    rows=int(h//bh)
    for i in range(rows):
        y=-(i+1)*bh; off=(bw/2 if i%2 else 0); x=-W/2-off
        while x<W/2:
            x0=max(x,-W/2)+mor/2; x1=min(x+bw,W/2)-mor/2
            if x1-x0>6: s.append(R(round(x0,1),y+mor/2,round(x1-x0,1),bh-mor,col,2,None,0))
            x+=bw
    if h>bh*rows+2: pass
    gh=min(GATE_H,h)
    s+=[R(-gate/2,-gh,gate,gh,DARK,2,OUT,6),R(-gate/2+8,-gh+8,gate-16,gh-8,'#1d2029',2,None,0)]
    if h>=GATE_H: s.append(R(-gate/2-12,-GATE_H-16,gate+24,16,'#8c867c',3,OUT,5))   # перемычка
    s.append(R(-W/2,-h,W,h,'rgba(0,0,0,0)',3,OUT,6))
    return s
for k in range(1,5):
    pr(f'gwa{k}',wall(70,34,4,500,k/4,BRK)); pr(f'gwb{k}',wall(54,27,10,470,k/4,BRKS))
# трещины на стене
pr('wall_cracks',[L(-330,-330,-300,-270,'#222',5),L(-300,-270,-325,-230,'#222',5),L(-325,-230,-290,-190,'#222',5),L(320,-340,290,-290,'#222',5),L(290,-290,320,-250,'#222',5),L(-150,-330,-140,-300,'#222',4)])
# ───── крыша: фронтон + тяжёлая черепица ─────
def roof(sag=0,braced=False,heavy=True):
    W=WALL_W+90; H=WALL_H; pk=130; ap=-H-pk+sag
    s=[P([(-WALL_W/2,-H),(0,ap+14),(WALL_W/2,-H)],'#e6dfd0',OUT,5)]                  # фронтон (штукатурка)
    if braced:
        s+=[L(-WALL_W/2+30,-H-6,0,ap+26,WOOD,10),L(WALL_W/2-30,-H-6,0,ap+26,WOOD,10),L(-WALL_W/2+30,-H-6,WALL_W/2-30,-H-6,WOOD,10),
            L(0,ap+26,0,-H-6,WOOD,10),L(-WALL_W/2+30,-H-6,0,-H-pk/2+sag/2-20,WOOD,8),L(WALL_W/2-30,-H-6,0,-H-pk/2+sag/2-20,WOOD,8)]
    s+=[P([(-W/2,-H+4),(0,ap-6),(W/2,-H+4),(W/2-26,-H+30),(0,ap+30),(-W/2+26,-H+30)],TILE,OUT,6)]
    for i in range(-5,6): s.append(L(i*70,-H+8+abs(i)*(pk-sag*0.2)/(-5.5)*(-1)*0.0-abs(i)*0,i*70,-H+22,'rgba(0,0,0,.25)',4)) if False else None
    s+=[L(-W/2+40,-H+12,-4,ap+8,'rgba(255,255,255,.3)',6)]
    return s
pr('gr_b',roof()); pr('gr_bs',roof(sag=34)); pr('gr_c',roof(braced=True))
# ───── рамка ворот (сужает проём) ─────
pr('gate_frame',[R(-250,-GATE_H,56,GATE_H,'#7a5a3a',4,OUT,6),R(194,-GATE_H,56,GATE_H,'#7a5a3a',4,OUT,6),R(-250,-GATE_H-4,500,34,'#7a5a3a',4,OUT,6),
  R(-232,-GATE_H+60,20,10,'#cfd3e0',3,OUT,3),R(212,-GATE_H+60,20,10,'#cfd3e0',3,OUT,3)])
# ───── материалы ─────
pile=[]
for r in range(5):
    for c in range(5-r): pile.append(R(-100+r*20+c*42,-(r+1)*22,40,20,BRKS,3,OUT,3))
pr('brick_pile_s',pile)
pr('rebar_bundle',[R(-150,-8-i*9,300,9,'#a0522d',4,OUT,3) for i in range(4)]+[R(-150+30*j,-40,3,0.1,'#000',0,None,0) for j in range(0)]+[R(-60,-44,14,44,'#f4c52a',3,OUT,3),R(60,-44,14,44,'#f4c52a',3,OUT,3)])
# ───── карточки (для inset): смета-столбцы, кирпичи, чертёж ворот, строка сметы ─────
def card(s): return [R(-360,-230,720,460,'#fffdf5',22,OUT,6)]+s
def bars(old,new,red=0,arrow=None):
    b=170; s=[L(-300,b,300,b,'#777',5),L(-300,b-130,300,b-130,'#999',3)]
    s+=[R(-210,b-old,120,old,'#b8bcc8',6,OUT,5),R(60,b-new,120,new,'#5fbf6a',6,OUT,5)]
    if red: s.append(R(60,b-new-red,120,red,'#e0533d',6,OUT,5))
    if arrow=='down': s+=[P([(-20,-120),(20,-120),(20,-40),(40,-40),(0,10),(-40,-40),(-20,-40)],'#5fbf6a',OUT,4)]
    if arrow=='up': s+=[P([(-20,30),(20,30),(20,-50),(40,-50),(0,-100),(-40,-50),(-20,-50)],'#e0533d',OUT,4)]
    s+=[C(-150,-190+0,0.1,'#000',None,0)]
    return s
pr('sm_save',card(bars(130,95,arrow='down')),upright=True)
pr('sm_warn',card(bars(130,95,red=45)),upright=True)
pr('sm_bad',card(bars(130,95,red=170,arrow='up')),upright=True)
bad=[R(-300,-190,260,150,BRK,8,OUT,5)]+[R(-300+(i%2)*10+i*0,0,0,0,'#000',0,None,0) for i in range(0)]
def bk(x,w,h,mor,col):
    s=[R(x,-120,w,240,MOR,6,OUT,5)]
    for r in range(int(240//h)):
        for c in range(int(w//(w/ (w//( (h*2)+mor))) )): pass
    return s
def brickcard(cx,bw,bh,mor,col):
    s=[R(cx-150,-130,300,260,MOR,6,OUT,5)]
    for r in range(int(260//bh)):
        off=(bw/2 if r%2 else 0)
        x=cx-150-off
        while x<cx+150:
            x0=max(x,cx-150)+mor/2; x1=min(x+bw,cx+150)-mor/2
            if x1-x0>5: s.append(R(x0,-130+r*bh+mor/2,x1-x0,bh-mor,col,2,None,0))
            x+=bw
    return s
pr('bk_cmp',card(brickcard(-170,80,40,4,BRK)+brickcard(170,60,30,12,BRKS)+[R(-8,-150,16,300,'#999',3,None,0)]),upright=True)
# чертёж ворот сверху: машина не проходит
pr('gate_fail',card([R(-330,-60,250,120,'#8c867c',6,OUT,5),R(80,-60,250,120,'#8c867c',6,OUT,5),R(-80,-50,160,100,'#e8f3d8',0,None,0),
  R(-150,-40,300,80,'#4d7fd6',24,OUT,6),R(-110,-30,70,60,'#9cc3f2',10,OUT,3),R(-150,-40,70,80,'rgba(224,83,61,.55)',10,None,0),R(80,-40,70,80,'rgba(224,83,61,.55)',10,None,0),
  L(-80,-100,-80,100,'#e0533d',5),L(80,-100,80,100,'#e0533d',5)]),upright=True)
# строка сметы «расширение гаража»
rows=[]
for i in range(5): rows+=[R(-300,-185+i*50,300-(i%3)*40,18,'#cfd3e0',6,None,0),R(180,-185+i*50,100,18,'#b8bcc8',6,None,0)]
rows+=[R(-300,65,360,26,'#f7c6bd',8,OUT,4),R(150,65,130,26,'#e0533d',8,OUT,4),L(-300,100,280,100,'#d94a3d',7)]
rows+=[P([(-330,150),(-300,125),(-270,150),(-285,150),(-285,190),(-315,190),(-315,150)],'#e0533d',OUT,4)]
pr('sm_line',card(rows),upright=True)
json.dump(lib,open(LIB,'w'),ensure_ascii=False,indent=2); print('ok13 props')
