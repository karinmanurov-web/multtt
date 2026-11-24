import os; REPO=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..'))+'/'
import json, math, random
LIB=REPO+'library.json'
lib=json.load(open(LIB))
OUT='#1e1b26'
def R(x,y,w,h,fill,r=None,st=OUT,sw=5):
    d={"t":"rect","x":x,"y":y,"w":w,"h":h,"fill":fill}
    if r: d["r"]=r
    if st: d["stroke"]=st; d["sw"]=sw
    return d
def C(x,y,r,fill,st=OUT,sw=5):
    d={"t":"circle","x":x,"y":y,"r":r,"fill":fill}
    if st: d["stroke"]=st; d["sw"]=sw
    return d
def E(x,y,rx,ry,fill,st=None,sw=4):
    d={"t":"ellipse","x":x,"y":y,"rx":rx,"ry":ry,"fill":fill}
    if st: d["stroke"]=st; d["sw"]=sw
    return d
def P(pts,fill,st=OUT,sw=5):
    d={"t":"poly","pts":[[round(a,1),round(b,1)] for a,b in pts],"fill":fill}
    if st: d["stroke"]=st; d["sw"]=sw
    return d
def L(x1,y1,x2,y2,col,sw=5): return {"t":"line","x1":x1,"y1":y1,"x2":x2,"y2":y2,"stroke":col,"sw":sw}
random.seed(5)
# ───────── локация field ─────────
X0,X1=-9000,10000
main=[
 {"p":1,"v":"main","shapes":[R(X0,-9000,X1-X0,10250,['#5fb4ee','#bfe6fb','#f4fbff'],None,None,0),
   E(300,200,260,70,'#fff'),E(560,170,200,60,'#fff'),E(1020,330,300,80,'#fff'),E(-400,420,280,70,'#fff'),E(1700,260,320,80,'#fff'),E(-1500,300,300,80,'#fff'),E(2600,380,300,70,'#fff'),
   # далёкие холмы и лес на горизонте
   E(200,1260,900,150,'#9bd08a'),E(1200,1260,1100,190,'#8bc57c'),E(-1400,1260,1300,170,'#9bd08a'),E(2800,1260,1300,180,'#8bc57c'),
   R(X0,1250,X1-X0,8000,['#79c258','#5fa745','#4d9238'],None,None,0),R(X0,1250,X1-X0,14,'#3f7d2f',None,None,0)]}]
tufts=[]
random.seed(7)
for i in range(60):
    x=random.randint(-1800,3000); y=random.randint(1290,1880); w=random.randint(30,60)
    tufts.append(P([(x-w/2,y),(x-w/6,y-w*.9),(x,y),(x+w/6,y-w*1.1),(x+w/2,y)],'#4b9035',None,0))
main.append({"p":1,"v":"main","shapes":tufts})
# аэро-вид: лоскутное поле
random.seed(11)
aer=[R(X0,-16000,X1-X0,32000,'#8cc45f',None,None,0)]
cols=['#8cc45f','#9ccf6a','#7fb855','#b5c966','#c9c96e','#a98f5a','#6fae4f','#a5cf75']
for gx in range(-6400,8000,900):
    for gy in range(-12600,8000,700):
        if abs(gx-300)<500 and abs(gy-1000)<500: continue
        aer.append(R(gx+random.randint(-40,40),gy+random.randint(-40,40),random.randint(700,880),random.randint(560,680),random.choice(cols),None,None,0))
for i in range(45):
    x=random.randint(-6000,7800); y=random.randint(-12000,7800)
    if abs(x-540)<500 and abs(y-1000)<900: continue
    aer.append(C(x,y,random.randint(110,260),'#2f7a3a',None,0))
for i in range(10): aer.append(L(random.randint(-6000,7000),random.randint(-8000,7000),random.randint(-6000,7000),random.randint(-8000,7000),'#b8aa86',34))
# деревня далеко наверху (y≈-6000)
for j in range(9):
    hx=540+random.randint(-900,700); hy=-6000+random.randint(-250,250)
    aer.append(R(hx,hy,330,240,'#f0dcb8',None,None,0)); aer.append(P([(hx-26,hy),(hx+165,hy-150),(hx+356,hy)],'#c4543a',None,0))
aer.append(R(-3,-6000,10,10,'#000',None,None,0)) if False else None
# скошенная полоска в начале и пины
aer+=[R(520,1000,40,260,'#d9e88a',None,None,0),C(540,1250,60,'#3a6fd8',None,0),C(540,1000,50,'#e5342b',None,0)]
# календарь
cal=[R(X0,-9000,X1-X0,18000,['#e9dfcc','#d8ccb3'],None,None,0),
 R(150,230,780,960,'#fdfdf8',24),R(150,230,780,150,'#e5342b',24),R(150,310,780,70,'#e5342b',None,None,0),
 C(300,215,22,'#8a8a96'),C(540,215,22,'#8a8a96'),C(780,215,22,'#8a8a96')]
def calgrid(xo=0,yo=0,marks=()):
    s=[]
    for r in range(5):
        for c in range(7):
            s.append(R(190+c*106+xo,420+r*148+yo,92,128,'#fff',10,'#cfcfd8',3))
    for (r,c) in marks:
        s.append(L(200+c*106+xo,430+r*148+yo,270+c*106+xo,530+r*148+yo,'#e5342b',9)); s.append(L(270+c*106+xo,430+r*148+yo,200+c*106+xo,530+r*148+yo,'#e5342b',9))
    return s
cal+=calgrid()
lib['locations']['field']={"groundY":1250,
 "views":{"main":{"title":"поле, вид сбоку (земля и небо шире мира — для отъезда камеры zoom<1)"},
          "aerial":{"title":"вид сверху «с дрона»: лоскутное поле, деревня на горизонте; строитель — синяя точка в (540,1250), конец полоски — красная"},
          "calendar":{"title":"настенный календарь; страницы — предмет cal_page"}},
 "layers":main+[{"p":1,"v":"aerial","shapes":aer},{"p":1,"v":"calendar","shapes":cal}]}
# ───────── предметы ─────────
PR=lib['props']
def pr(n,sh,grip=(0,0),upright=False):
    d={"grip":list(grip),"shapes":sh}
    if upright: d["upright"]=True
    PR[n]=d
def blades(h,n,seed,spread=120):
    random.seed(seed); sh=[]
    greens=['#4a9a3a','#5cab45','#3f8a32','#6bb84e']
    for i in range(n):
        bx=-spread/2+spread*i/(n-1); bh=h*random.uniform(.62,1.0); lean=random.uniform(-26,26)*(bh/h)
        w=random.uniform(9,14)
        sh.append({"t":"g","x":bx,"y":0,"anim":{"k":"sway","s":random.uniform(.25,.5),"a":random.uniform(1.5,3.2),"ph":random.uniform(0,6)},
          "shapes":[P([(-w,0),(w,0),(lean+2,-bh)],random.choice(greens),OUT,3)]})
    return sh
pr('grass_clump',blades(440,11,1,150))
pr('grass_mid',blades(300,9,2,140))
pr('grass_stub',blades(48,7,3,120))
# газонокосилка: рукоять вверх-назад, корпус впереди (лицом вправо)
pr('mower',[R(-14,-58,150,42,'#d9332b',10),R(112,-52,22,30,'#9aa3b5',6),C(-4,-24,22,'#2a2f3d'),C(110,-24,22,'#2a2f3d'),
  P([(-6,-58),(-120,-186),(-110,-196),(6,-70)],'#4a5568'),R(-134,-206,40,16,'#2a2f3d',6),R(30,-78,60,22,'#aab2bf',8)],grip=(-114,-198),upright=True)
# машина (лицом вправо, центр по x, длина ~900): передний слой, стёкла прозрачные
car=[
 # кузов низ
 R(-430,-300,880,298,['#e8483e','#c4332b'],40),
 # капот выше
 P([(110,-300),(450,-300),(450,-250),(110,-250)],'#d63d33',None,0),
 # стойки и крыша
 P([(-330,-300),(-300,-520),(30,-520),(120,-300),(95,-300),(10,-490),(-275,-490),(-300,-300)],'#c4332b'),
 R(-300,-526,330,22,'#a82a23',8),
 # стёкла-тонировка
 P([(-300,-300),(-275,-490),(10,-490),(95,-300)],'rgba(170,215,240,.22)',None,0),
 L(-235,-490,-235,-300,'#a82a23',16),
 # дверь, ручка, фара, бампер
 R(-290,-285,200,205,None,24,'#a82a23',4),R(-120,-240,40,12,'#a82a23',6,None,0),
 R(430,-200,30,60,'#ffe27a',8),R(425,-120,40,50,'#8a8fa0',10),R(-440,-170,26,60,'#e5342b',8),
 # руль перед героем (виден через стекло)
 L(55,-330,28,-400,'#2a2f3d',14),
 # арки и колёса (крутятся)
 E(-250,-70,100,70,'#1e1b26'),E(300,-70,100,70,'#1e1b26')]
for wx in (-250,300):
    car.append({"t":"g","x":wx,"y":-70,"anim":{"k":"spin","s":2.2},"shapes":[C(0,0,86,'#2a2f3d'),C(0,0,46,'#c7ced8'),L(-46,0,46,0,'#7d8699',8),L(0,-46,0,46,'#7d8699',8),C(0,0,10,'#7d8699',None)]})
pr('car',car)
pr('car_seat',[R(-190,-330,120,230,'#4a5568',30),R(-190,-120,240,40,'#3c4556',12)])
# страница календаря: ось у верхнего края (по центру), листает вверх
page=[R(-390,0,780,960-230+0,'#fdfdf8',10)]+[s for s in calgrid(-540-0,-230-0,[(0,2),(1,3),(2,4)]) ] if False else None
pg=[R(-390,0,780,790,'#fdfdf8',10,OUT,5)]
for r in range(5):
    for c in range(7): pg.append(R(-350+c*106,40+r*138,92,118,'#fff',10,'#cfcfd8',3))
for (r,c) in [(0,1),(1,3),(2,5),(3,2),(4,4)]: pg+= [L(-340+c*106,50+r*138,-270+c*106,140+r*138,'#e5342b',9),L(-270+c*106,50+r*138,-340+c*106,140+r*138,'#e5342b',9)]
pr('cal_page',pg)
json.dump(lib,open(LIB,'w'),ensure_ascii=False,indent=2)
print('ok')
