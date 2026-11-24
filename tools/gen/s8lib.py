import json,random
exec(open('s5lib2.py').read().split("# ───── бульдозер")[0])
random.seed(8)
# ───── река (сюжет 8). Плато y=1030 (lift −220), склоны 40→300 и 960→700, вода 300..700 y=1262
GR='#8fc063'; DT='#a9855a'
def bank(sign):
    f=(lambda x:x) if sign<0 else (lambda x:1000-x)
    pts=[(-900,1030),(40,1030),(300,1250),(300,3400),(-900,3400)]
    band=[(-900,1030),(40,1030),(300,1250),(300,1272),(40,1054),(-900,1054)]
    if sign>0:
        pts=[(1000-x+0,y) for x,y in pts]; pts=[(x,y) for x,y in pts]
        band=[(1000-x,y) for x,y in band]
        pts=[(x if x<1900 else x,y) for x,y in pts]
    return [P(pts,DT,OUT,5),P(band,GR,OUT,5)]
sky=[R(-1000,-1400,3200,4800,['#7cc4f2','#c9e9fa','#f6fbff'],None,None,0)]
for (x,y,w,h) in [(150,380,300,70),(700,300,240,60),(1250,520,320,70),(-350,600,260,60),(450,760,200,50)]:
    sky.append(E(x,y,w,h,'#fff',None))
sky.append(C(1150,330,120,'rgba(255,240,170,.35)',None,0)); sky.append(C(1150,330,78,'#ffe47a',None,0))
for (x,y,w,h) in [(-150,260,260,56),(1500,560,300,64),(300,150,220,50),(950,640,200,48),(-600,420,240,56)]: sky.append(E(x,y,w,h,'#fff',None))
for (x,y) in [(250,520),(330,470),(420,540),(1000,430)]: sky.append(P([(x-18,y),(x,y-12),(x+18,y)],None,'#2a2f3d',4) if False else L(x-18,y,x,y-12,'#2a2f3d',4)); sky.append(L(x,y-12,x+18,y,'#2a2f3d',4))
# дальние холмы
sky.append(P([(-1000,1030),(-1000,880),(-500,820),(0,900),(500,860),(1000,920),(1500,830),(2000,900),(2000,1030)],'#b9d9ae',None,0))
sky.append(P([(-1000,1030),(-1000,950),(-300,900),(300,960),(900,930),(1500,960),(2000,920),(2000,1030)],'#a6cf9b',None,0))
# город слева на плато (низ y=1030)
cx=[-760,-620,-520,-400,-300,-190,-90]
hh=[420,300,560,380,640,340,260]
cols=['#d9cbb4','#c3b8a6','#e2d6c0','#b9b2a8','#d0c1ab','#c7baa4','#e0d4bd']
for x,h,c in zip(cx,hh,cols):
    w=100 if h<400 else 110
    sky.append(R(x-w/2,1030-h,w,h,c,None,OUT,5))
    for r in range(int(h//90)):
        for k in (-1,1): sky.append(R(x+k*24-10,1030-h+30+r*80,20,34,'#9ad0f5',None,OUT,3))
# деревня справа: домики и деревья, дорога к деревне
for (x,w,h,c) in [(1100,130,110,'#eadfc9'),(1290,150,120,'#f1e3c3'),(1490,130,100,'#e2d2b4')]:
    sky.append(R(x-w/2,1030-h,w,h,c,None,OUT,5)); sky.append(P([(x-w/2-14,1030-h),(x,1030-h-80),(x+w/2+14,1030-h)],'#c9735b',OUT,5))
    sky.append(R(x-14,1030-60,28,60,'#8a6a47',None,OUT,4))
for x in (1010,1210,1400,1600): sky.append(R(x-8,1030-90,16,90,'#8a6a47',None,OUT,4)); sky.append(C(x,1030-130,56,'#5fa564',OUT,5))
for x in (-850,-700): sky.append(R(x-8,1030-80,16,80,'#8a6a47',None,OUT,4)); sky.append(C(x,1030-120,50,'#5fa564',OUT,5))
loc=bank(-1)+bank(1)
for i in range(60):
    x=random.choice([random.randint(-880,230),random.randint(770,1880)]); y=random.randint(1330,3200)
    ground_y = 1030+max(0,min(220,(x-40)*220/260)) if x<500 else 1030+max(0,min(220,(960-x)*220/260))
    if y>ground_y+30:
        loc.append(E(x,y,random.randint(14,36),random.randint(6,12),'#8f6e47',None,0))
for k in range(5):
    y=1500+k*340
    loc.append(L(-880,y,200,y+40,'rgba(90,60,35,.25)',10)); loc.append(L(800,y+30,1880,y,'rgba(90,60,35,.25)',10))
for x in (-500,-220,-60,1060,1240,1500):
    loc.append(P([(x-30,1030),(x-14,1000),(x,1030)],'#6faa4c',None,0)); loc.append(P([(x,1030),(x+14,990),(x+30,1030)],'#6faa4c',None,0))
# вода
water=[R(300,1262,400,2200,['#6dbcec','#3b86c4'],None,None,0)]
for i in range(26):
    x=random.randint(310,660); y=random.randint(1285,2600)
    water.append(L(x,y,x+random.randint(30,60),y,'rgba(255,255,255,.45)',5))
lib['locations']['river']={"groundY":1250,"views":{},"layers":[{"p":1,"shapes":sky+loc[:0]},{"p":1,"shapes":water},{"p":1,"shapes":loc}]}
# ───── предметы
pr('stone',[E(0,-8,50,24,'#a5a9b0',OUT,5),E(-12,-16,16,6,'#c4c8ce',None,0)],upright=True)
def logshapes(L,d=60):
    h=L/2
    return [R(-h,-d,L,d,'#8a5f3a',d/2.5,OUT,5),L_(-h+30,-d+12,h-60,'#6f4a2b'),L_(-h+80,-14,h-20,'#6f4a2b'),E(h-4,-d/2,10,d/2,'#c9a06b',OUT,4)]
def L_(x1,y,x2,col): return L(x1,y,x2,y,col,4)
pr('log_flat',logshapes(440),upright=True)
# бревно в руках: заднее (у героя) на высоте руки, переднее на земле; хват у заднего конца
def carry(Lg=440,hy=170):
    return [P([(-Lg/2,-hy),(Lg/2,-60),(Lg/2,0),(-Lg/2,-hy+60)],'#8a5f3a',OUT,5),L(-Lg/2+40,-hy+24,Lg/2-40,-30,'#6f4a2b',4),
            E(Lg/2-3,-30,10,30,'#c9a06b',OUT,4),E(-Lg/2,-hy+30,10,30,'#c9a06b',OUT,4)]
pr('log_carry',carry(),grip=(-220,-170),upright=True)
# лежащее упавшее дерево (корни слева), на земле плато
tree=[R(-220,-52,440,52,'#8a5f3a',20,OUT,5),L(-170,-34,170,-34,'#6f4a2b',4),
 P([(-210,-52),(-260,-120),(-210,-90),(-245,-160),(-185,-100),(-175,-170),(-155,-90),(-110,-130),(-130,-52)],'#6f4a2b',OUT,5),
 R(40,-100,14,50,'#8a5f3a',5,OUT,4),C(47,-112,34,'#5fa564',OUT,5),R(130,-90,12,40,'#8a5f3a',5,OUT,4),C(136,-102,28,'#5fa564',OUT,5),E(215,-26,10,26,'#c9a06b',OUT,4)]
pr('tree_log',tree,upright=True)
pr('reeds',[L(-20,0,-30,-90,'#4f8f3f',6),L(0,0,4,-110,'#4f8f3f',6),L(20,0,34,-80,'#4f8f3f',6),R(-4,-130,14,36,'#8a5f3a',6,OUT,3)],upright=True)
json.dump(lib,open(LIB,'w'),ensure_ascii=False,indent=2); print('ok8')
# ───── захват 2
lib=json.load(open(LIB)) if False else lib
def wheel(x,y,r=34):
    return {"t":"g","x":x,"y":y,"anim":{"k":"spin","s":2.5},"shapes":[C(0,0,r,'#2a2f3d',OUT,5),C(0,0,r-9,'#dfe4ea',None,0),L(-r+6,0,r-6,0,'#8c93a1',4),L(0,-r+6,0,r-6,'#8c93a1',4)]}
bike=[wheel(-62,-34),wheel(62,-34),L(-62,-34,-8,-70,'#c4332b',8),L(-8,-70,62,-34,'#c4332b',8),L(-8,-70,-14,-96,'#c4332b',8),L(-62,-34,-14,-96,'#c4332b',8),L(48,-72,62,-34,'#8c93a1',6),L(40,-74,60,-74,'#2a2f3d',8),
 R(-34,-104,40,10,'#2a2f3d',4,None,0),
 L(-10,-100,28,-170,'#7a5ac0',32),C(40,-200,24,'#e0aa7e',OUT,5),P([(18,-208),(30,-232),(58,-222),(60,-204)],'#e8c24a',OUT,4),
 L(24,-160,56,-100,'#7a5ac0',14),L(-4,-96,20,-56,'#3a4a6b',16),L(20,-56,2,-36,'#3a4a6b',14)]
pr('bike_rider',bike,upright=True)
# тележка: хват у рукояти (-80,-170) как у бревна; передний край на земле
cart=[R(-40,-150,170,80,'#b07a45',8,OUT,5),L(-40,-110,130,-110,'#8a5f3a',4),L(-80,-170,-40,-110,'#8a5f3a',10),L(-40,-110,-40,-90,'#8a5f3a',8),
 {"t":"g","x":55,"y":-34,"anim":{"k":"spin","s":2.0},"shapes":[C(0,0,34,'#2a2f3d',OUT,5),C(0,0,20,'#dfe4ea',None,0),L(-20,0,20,0,'#8c93a1',4)]},
 R(0,-190,70,42,'#d6b27a',6,OUT,4),R(60,-176,50,28,'#c4332b',6,OUT,4)]
pr('cart',cart,grip=(-80,-170),upright=True)
# доски настила (72 px, верх на y−16 от origin)
def plank(col='#c9a06b'): return [R(-36,-16,72,16,col,3,OUT,4),L(-26,-8,26,-8,'rgba(90,60,30,.35)',3)]
pr('plank',plank(),upright=True)
pr('plank_crack',[P([(-36,-16),(-4,-16),(-8,-2),(-36,0)],'#c9a06b',OUT,4),P([(6,-16),(36,-16),(36,0),(10,2)],'#c9a06b',OUT,4),L(-4,-16,6,-8,OUT,4),L(-8,-2,10,2,OUT,4),P([(-6,-10),(4,-10),(0,6)],'#6f4a2b',None,0)],upright=True)
pr('plank_sag',[P([(-36,-14),(36,-14),(36,2),(-36,2)],'#c9a06b',OUT,4)],upright=True)
# опора (бетон), origin — вода, высота 232 до уровня плато
pr('pier',[R(-30,-206,60,206,['#c9ccd3','#9aa0ab'],4,OUT,5),R(-46,-232,92,26,'#b1b6c0',6,OUT,5),L(-14,-180,-14,-20,'rgba(0,0,0,.12)',5)],upright=True)
# перила (на 400 px, верх деки y=0 origin)
rl=[L(-200,-74,200,-74,'#d9dee6',8),L(-200,-40,200,-40,'#d9dee6',6)]
for k in range(6): rl.append(R(-200+k*80-6,-84,12,84,'#b1b6c0',3,OUT,4))
rl.append(R(194,-84,12,84,'#b1b6c0',3,OUT,4))
pr('rail',rl,upright=True)
# насыпи подходов: мировые координаты (spawn x=0, y=0)
pr('fill_L',[P([(38,1030),(300,1030),(300,1262),(300,1250)],'#a9855a',None,0),P([(38,1030),(302,1030),(302,1256)],'#a9855a',OUT,5),L(38,1030,302,1030,'#8fc063',16)],upright=True)
pr('fill_R',[P([(962,1030),(698,1030),(698,1256)],'#a9855a',OUT,5),L(962,1030,698,1030,'#8fc063',16)],upright=True)
# балка под настилом
pr('girder',[R(-215,-36,430,36,['#8f98a8','#6f7888'],6,OUT,5)]+[L(-200+k*40,-36,-180+k*40,0,'rgba(0,0,0,.25)',4) for k in range(10)],upright=True)
# ───── захват 3: широкий мост
road=[R(-900,1030,2800,100,'#4a4f5c',None,None,0),L(-900,1030,1900,1030,'#2f333d',8),L(-900,1130,1900,1130,'#2f333d',8),R(-900,1126,2800,10,'#b9bec8',None,None,0)]
for k in range(-12,28):
    road.append(R(-900+k*100,1061,50,6,'#e9edf2',None,None,0)); road.append(R(-900+k*100,1095,50,6,'#e9edf2',None,None,0))
road.append(R(300,1130,400,46,['#b1b6c0','#8e939c'],None,OUT,5))
for k in range(8): road.append(L(318+k*50,1134,318+k*50,1172,'rgba(0,0,0,.15)',4))
pr('road_wide',road,upright=True)
pr('pier_w',[R(-50,-100,100,100,['#c9ccd3','#9aa0ab'],6,OUT,5),R(-62,-118,124,22,'#b1b6c0',6,OUT,5)],upright=True)
# ───── захват 4: огромная река и мост (river_big). Настил y=730 (lift −520), вода y=1262 между 550 и 1550
random.seed(9)
big=[R(-3000,-1800,8000,4000,['#7cc4f2','#c9e9fa','#f6fbff'],None,None,0),C(2100,-300,140,'rgba(255,240,170,.35)',None,0),C(2100,-300,90,'#ffe47a',None,0)]
for (x,y,w,h) in [(-300,-500,300,64),(500,-800,260,60),(1400,-600,320,70),(2300,-900,280,64),(3000,-400,300,66),(-1000,-700,260,60),(900,-300,220,52)]: big.append(E(x,y,w,h,'#fff',None))
big.append(P([(-3000,730),(-3000,560),(-1500,500),(0,590),(1300,520),(2800,600),(4000,540),(5000,580),(5000,730)],'#b9d9ae',None,0))
big.append(P([(-3000,730),(-3000,650),(-800,620),(800,680),(2200,640),(3600,680),(5000,640),(5000,730)],'#a6cf9b',None,0))
# город на левом плато и деревня-пригород справа; башни выше
import itertools
def town(x0,x1,seed):
    random.seed(seed); x=x0; out=[]
    while x<x1:
        w=random.randint(110,190); h=random.randint(280,900)
        out.append(R(x,730-h,w,h,random.choice(['#d9cbb4','#c3b8a6','#e2d6c0','#b9b2a8','#d0c1ab']),None,OUT,5))
        for r in range(int(h//80)):
            for k in range(int(w//46)): out.append(R(x+14+k*46,730-h+24+r*80,22,34,'#9ad0f5',None,OUT,3))
        x+=w+random.randint(10,40)
    return out
big+=town(-2400,-120,1)+town(1980,4300,2)
# эстакады-развязки
def flyover(xa,xb,sign):
    o=[R(xa,560,xb-xa,40,'#4a4f5c',None,OUT,5)]
    for k in range(int((xb-xa)//140)+1): o.append(R(xa+20+k*140,600,30,130,'#b1b6c0',None,OUT,4))
    for k in range(int((xb-xa)//70)): o.append(R(xa+10+k*70,578,36,5,'#e9edf2',None,None,0))
    return o
big+=flyover(-1700,-300,-1)+flyover(2150,3550,1)
big.append(P([(-300,600),(-120,600),(180,730),(-60,730)],'#4a4f5c',OUT,5)); big.append(P([(2150,600),(1980,600),(1700+300,730),(2060,730)],'#4a4f5c',OUT,5))
# берега
GR='#8fc063'; DT='#a9855a'
big.append(P([(-3000,730),(250,730),(550,1262),(550,3400),(-3000,3400)],DT,OUT,5)); big.append(P([(-3000,730),(250,730),(550,1262),(550,1284),(250,754),(-3000,754)],GR,OUT,5))
big.append(P([(5000,730),(1850,730),(1550,1262),(1550,3400),(5000,3400)],DT,OUT,5)); big.append(P([(5000,730),(1850,730),(1550,1262),(1550,1284),(1850,754),(5000,754)],GR,OUT,5))
bw=[R(550,1262,1000,2200,['#6dbcec','#3b86c4'],None,None,0)]
for i in range(70):
    x=random.randint(560,1500); y=random.randint(1290,2800); bw.append(L(x,y,x+random.randint(40,90),y,'rgba(255,255,255,.45)',6))
# дорога по всему плато и настил (передняя грань только над рекой)
rd=[R(-3000,730,8000,100,'#4a4f5c',None,None,0),L(-3000,730,5000,730,'#2f333d',8),L(-3000,830,5000,830,'#2f333d',8),R(-3000,826,8000,10,'#b9bec8',None,None,0)]
for k in range(-30,55):
    rd.append(R(-3000+k*100+3000-3000,761,50,6,'#e9edf2',None,None,0)); rd.append(R(k*100,795,50,6,'#e9edf2',None,None,0))
rd.append(R(250,830,1600,56,['#b1b6c0','#8e939c'],None,OUT,5))
for k in range(32): rd.append(L(270+k*50,834,270+k*50,882,'rgba(0,0,0,.15)',4))
lib['locations']['river_big']={"groundY":1250,"views":{},"layers":[{"p":1,"shapes":big[:-4]},{"p":1,"shapes":bw},{"p":1,"shapes":big[-4:]},{"p":1,"shapes":rd}]}
pr('pier_big',[R(-60,-380,120,380,['#c9ccd3','#9aa0ab'],6,OUT,5),R(-76,-400,152,26,'#b1b6c0',6,OUT,5),L(-24,-350,-24,-30,'rgba(0,0,0,.12)',6)],upright=True)
json.dump(lib,open(LIB,'w'),ensure_ascii=False,indent=2); print('ok8c')
