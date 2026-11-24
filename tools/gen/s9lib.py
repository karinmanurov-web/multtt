import json,random
exec(open('s5lib2.py').read().split("# ───── бульдозер")[0])
random.seed(9)
# ───── локация cottage: разрез коттеджа (сюжет 9). Пол 1 этажа y=1250, пол 2 этажа y=690 (lift −560), подвал 1274..1810
WALL='#c9b99d'; K='#f6e7c8'; LV='#e4e9f0'; F2='#ece4f2'; BSM='#7c828e'
sky=[R(-2400,-1600,6400,4000,['#f6c98a','#f9dfb4','#fdf1dc'],None,None,0),C(1900,-250,150,'rgba(255,230,160,.4)',None,0),C(1900,-250,90,'#ffd27a',None,0)]
for (x,y,w,h) in [(-300,-500,300,60),(600,-900,260,56),(1500,-600,300,62),(-900,-700,280,60),(2100,-900,280,60)]: sky.append(E(x,y,w,h,'#fff3df',None))
sky.append(P([(-2400,1250),(-2400,1000),(-1500,930),(-700,1010),(0,950),(1200,990),(2200,930),(3000,1000),(3600,960),(3600,1250)],'#d9b36b',None,0))
# осенние деревья по краям
def tree(x,h=520,col='#e08a2f',col2='#c9622a'):
    return [R(x-22,1250-h*0.45,44,h*0.45,'#7a5a3a',8,OUT,5),C(x,1250-h*0.62,h*0.30,col,OUT,5),C(x-h*0.2,1250-h*0.5,h*0.2,col2,OUT,5),C(x+h*0.2,1250-h*0.52,h*0.22,col,OUT,5)]
for x,h,a,b_ in [(-260,620,'#e08a2f','#c9622a'),(-650,520,'#e8b53a','#d98d2a'),(-1050,600,'#c9622a','#e08a2f'),(1460,640,'#e8b53a','#d98d2a'),(1850,540,'#e08a2f','#c9622a'),(2250,600,'#c9622a','#e8b53a')]:
    sky.append({"t":"g","x":0,"y":0,"anim":{"k":"sway","s":0.35,"a":1.2,"ph":x%7,"pt":[x,1250]},"shapes":tree(x,h,a,b_)})
sky+= [R(-2400,1250,6400,1600,'#7a5a3a',None,None,0),R(-2400,1250,6400,26,'#b79a52',None,None,0),L(-2400,1250,3999,1250,'#6b8a3d',6)]
for i in range(30):
    sky.append(E(random.randint(-2300,3800),random.randint(1330,2700),random.randint(14,40),random.randint(6,12),'#6a4d30',None,0))
# корпус дома
house=[]
house.append(P([(-20,150),(600,-250),(1220,150)],'#b5523b',OUT,6))
house.append(P([(0,150),(600,-230),(1200,150)],'#c9654a',None,0))
house.append(R(950,-120,70,170,'#a8553f',None,OUT,6))   # декоративная труба (старая)
# интерьер
house.append(R(40,150,1120,540,F2,None,None,0))                  # 2 этаж
house.append(R(40,714,560,536,K,None,None,0)); house.append(R(624,714,536,536,LV,None,None,0))   # кухня / гостиная
house.append(R(40,1274,1120,536,BSM,None,None,0))                # подвал
for k in range(10): house.append(L(40,1310+k*52,1160,1310+k*52,'rgba(0,0,0,.12)',3))
for k in range(22): house.append(L(60+k*50,1274,60+k*50,1810,'rgba(0,0,0,.08)',3))
# обои: полоса-плинтус
house.append(R(40,1224,560,26,'#d9c39a',None,None,0)); house.append(R(624,1224,536,26,'#c5ccd6',None,None,0))
# перекрытия
house.append(R(10,130,1180,24,'#9aa1ad',None,OUT,5))                       # потолок 2 этажа
house.append(R(10,690,770,24,'#9aa1ad',None,OUT,5)); house.append(R(1160,690,30,24,'#9aa1ad',None,OUT,5))   # пол 2 этажа (с проёмом лестницы 780..1160)
house.append(R(10,1250,1180,24,'#a9855a',None,OUT,5))                       # пол 1 этажа
house.append(R(10,1810,1180,30,'#7d838f',None,OUT,5))
# наружные стены
house.append(R(10,130,30,1710,WALL,None,OUT,5)); house.append(R(1160,130,30,1710,WALL,None,OUT,5))
# перегородки: кухня | гостиная (проём 900..1250), 2 этаж, подвал
house.append(R(600,714,24,200,'#d9c39a',None,OUT,5)); house.append(R(600,150,24,540,'#d6cce0',None,OUT,5))
house.append(R(600,1274,24,536,'#6c727d',None,OUT,5))
# окна
def window(x,y,w,h,tr=True):
    s=[R(x-10,y-10,w+20,h+20,'#fff',8,OUT,5),R(x,y,w,h,['#f4d28a','#fbe9c4'],None,None,0),C(x+w*0.3,y+h*0.7,h*0.28,'#e08a2f',None,0),C(x+w*0.65,y+h*0.62,h*0.22,'#c9622a',None,0),
       L(x+w/2,y,x+w/2,y+h,'#fff',8),L(x,y+h/2,x+w,y+h/2,'#fff',8)]
    return s
house+=window(90,860,200,210)+window(660,860,110,210)+window(110,300,200,210)+window(660,300,110,210)
# лестница (низ справа 1150,1250 → верх слева 780,690), в глубине
st=[]
n=12; dx=(1150-780)/n; dy=(1250-690)/n
pts=[(1150,1250)]
for k in range(n):
    x=1150-k*dx; y=1250-k*dy
    pts+= [(x,y-dy),(x-dx,y-dy)]
pts+=[(780,1250)]
st.append(P(pts,'#c9a06b',OUT,5))
for k in range(n): st.append(L(1150-k*dx-dx,1250-(k+1)*dy,1150-k*dx,1250-(k+1)*dy,'#8a5f3a',6))
st.append(L(1150,1250-30,780,690-30,'#8a5f3a',10)); 
for k in range(0,n,2): st.append(L(1150-k*dx,1250-k*dy-30,1150-k*dx,1250-k*dy-110,'#8a5f3a',8))
house+=st
# мебель кухни: холодильник, столешница, шкафы
house+=[R(60,870,100,380,['#f3f6fa','#d9dee6'],14,OUT,5),L(70,1010,150,1010,'#9aa3b5',4),R(138,930,10,50,'#9aa3b5',4,None,0),R(138,1040,10,70,'#9aa3b5',4,None,0)]
house+=[R(170,1100,430,150,'#c4895a',6,OUT,5),R(160,1090,450,20,'#f3f0ea',4,OUT,5)]
for xx in (190,330,470): house.append(R(xx,1126,120,100,'#d29c6c',6,OUT,4)); house.append(R(xx+98,1160,8,30,'#6f4a2b',3,None,0))
house+=[R(310,770,300,130,'#c4895a',6,OUT,5),L(460,775,460,895,OUT,4),R(444,830,8,30,'#6f4a2b',3,None,0),R(468,830,8,30,'#6f4a2b',3,None,0)]
# плита (на столешнице) и раковина: отдельные предметы-реквизит ниже; вытяжка
# гостиная: диван, журнальный столик
house+=[R(640,1130,200,120,['#6f93c6','#5b7fb2'],24,OUT,5),R(630,1070,70,180,'#5b7fb2',20,OUT,5),R(640,1100,180,36,'#7ea4d8',14,OUT,4)]
# спальни
house+=[R(70,600,300,90,'#d9d0e8',10,OUT,5),R(70,540,120,70,'#fff',14,OUT,5),R(380,330,130,360,'#a9855a',8,OUT,5),R(660,620,100,70,'#a9855a',8,OUT,5)]
# подвал: колонны и лампочка
house+=[R(300,1274,22,536,'#9aa1ad',None,OUT,4),R(900,1274,22,536,'#9aa1ad',None,OUT,4),L(620,1274,620,1330,'#2a2f3d',4),C(620,1340,16,'#ffe47a',OUT,4)]
lib['locations']['cottage']={"groundY":1250,"views":{},"layers":[{"p":1,"shapes":sky},{"p":1,"shapes":house}]}
# ───── предметы (сюжет 9)
pr('leaves',[{"t":"g","x":0,"y":0,"anim":{"k":"fall","s":130,"a":1900,"dx":90},"shapes":[g for oy in (0,-1900) for g in [P([(x-9,y+oy),(x,y+oy-8),(x+9,y+oy),(x,y+oy+9)],random.choice(['#e08a2f','#c9622a','#e8b53a']),None,0) for x,y in [(random.randint(-1400,0) if i%2 else random.randint(1180,2500),random.randint(-900,950)) for i in range(26)]]]}],upright=True)

def txt(key,x,y,size,fill='#fff',st=OUT,sw=0,align='center'):
    return {"t":"text","key":key,"x":x,"y":y,"size":size,"fill":fill,"stroke":st,"sw":sw,"align":align}
# стол и стул (кухня/гостиная)
pr('k_table',[R(-110,-130,220,20,'#e2b070',6,OUT,5),R(-92,-110,16,110,'#a9733f',4,OUT,4),R(76,-110,16,110,'#a9733f',4,OUT,4)],upright=True)
pr('k_chair',[R(-60,-95,16,95,'#a9733f',4,OUT,4),R(-60,-280,16,190,'#a9733f',6,OUT,4),R(-60,-100,110,18,'#c4895a',5,OUT,4),R(34,-85,16,85,'#a9733f',4,OUT,4)],upright=True)
# термометр: корпус-табло + число (разные id для разных чисел)
def therm(key,col):
    return [R(-70,-90,140,90,'#2a2f3d',14,OUT,5),R(-62,-82,124,74,'#1c2230',10,None,0),txt(key,0,-22,46,col)]
for k,col in (("t16","#7fd0ff"),("t17","#7fd0ff"),("t18","#9fe0c0"),("t19","#c9e87a"),("t20","#ffe47a"),("t12","#5aa8ff")):
    pr('th_'+k,therm('th_'+k,col),upright=True)
# плед на плечах (передний слой, в клетку)
pr('plaid',[P([(-62,-10),(62,-10),(80,130),(-80,130)],'#c9444a',OUT,5),L(-40,-10,-52,130,'#f3e1b0',6),L(0,-10,0,130,'#f3e1b0',6),L(40,-10,52,130,'#f3e1b0',6),L(-70,50,70,50,'#2a2f3d',6),L(-76,95,76,95,'#f3e1b0',6)],upright=True)
# кастрюля и пар
def pot(c='#c3cad6'):
    return [R(-50,-70,100,70,c,10,OUT,5),R(-60,-82,120,16,'#9aa3b5',6,OUT,5),R(-14,-100,28,16,'#2a2f3d',6,None,0)]
def steam(n=3):
    return [{"t":"g","x":(i-1)*28,"y":-104-i%2*14,"anim":{"k":"bob","s":1.6+i*0.4,"a":10,"ph":i},"shapes":[E(0,-12,15,11,'rgba(255,255,255,.85)',OUT,3),E(6,-44,12,9,'rgba(255,255,255,.65)',None,0)]} for i in range(n)]
pr('pot',pot(),upright=True)
pr('pot_steam',pot()+steam(),upright=True)
pr('pot_big',pot('#7fa0c8')+steam(),upright=True)
# плита с конфорками (4 штуки), стоит на столешнице: y=1100
pr('stove',[R(-120,-110,240,110,['#e9edf3','#c8cfdb'],10,OUT,5),R(-120,-120,240,16,'#2a2f3d',4,OUT,5),*[C(x,-122,22,'#3a4152',OUT,3) for x in (-85,-28,28,85)],*[C(x,-96,7,'#9aa3b5',None,0) for x in (-85,-28,28,85)],R(-90,-96,10,0,'#000',None,None,0)],upright=True)
# холодные/тёплые наложения (мягкие) — на весь кадр
pr('cold_tint',[R(-2400,-1800,6400,4000,'rgba(90,140,220,.16)',None,None,0)],upright=True)

# ── захват 2: счёт, мысль-костёр, печь
def bill(vk):
    sh=[R(-290,-760,580,760,'#fbfaf3',10,OUT,6),R(-290,-760,580,90,'#4a6fa5',10,OUT,6),txt('b_title',0,-690,46,'#fff'),
        L(-250,-600,250,-600,'#9aa3b5',4),
        txt('b_el',-250,-520,36,OUT,None,0,'left'),txt('b_w',-250,-380,36,OUT,None,0,'left'),L(-250,-300,250,-300,'#9aa3b5',4),txt('b_sum',-250,-200,52,OUT,None,0,'left')]
    if vk:
        sh+=[txt(vk+'e',250,-520,38,'#c0392b',None,0,'right'),txt(vk+'w',250,-380,38,'#c0392b',None,0,'right'),txt(vk+'s',250,-200,56,'#c0392b',None,0,'right')]
    return sh
for k in ('v1','v2','v3','v4'): pr('bill_'+k,bill(k),upright=True)
# мысль с костром
def fire():
    return [R(-62,-22,124,22,'#7a4a2a',6,OUT,4),L(-50,-22,50,0,OUT,4),
            {"t":"g","x":0,"y":0,"anim":{"k":"pulse","s":5,"a":0.12,"pt":[0,0]},"shapes":[P([(-46,-18),(-30,-90),(-12,-50),(0,-130),(14,-60),(32,-100),(46,-18)],'#f08a2a',OUT,4),P([(-22,-18),(-8,-60),(0,-86),(10,-54),(22,-18)],'#ffd24a',None,0)]}]
pr('think_fire',[C(-90,-30,14,'#fff',OUT,4),C(-60,-70,22,'#fff',OUT,4),E(0,-210,190,120,'#fff',OUT,5),*[g for g in [{"t":"g","x":0,"y":-190,"shapes":fire()}]]],upright=True)
# печь из кирпича + дымоход
def bricks(x0,y0,w,h,bw=40,bh=20):
    out=[]
    r=0
    y=y0
    while y<y0+h-1:
        off=(bw/2) if r%2 else 0
        out.append(L(x0,y,x0+w,y,'#7e2f1e',3))
        x=x0+off
        while x<x0+w:
            if x>x0+2: out.append(L(x,y,x,min(y+bh,y0+h),'#7e2f1e',3))
            x+=bw
        y+=bh; r+=1
    return out
pr('brick_stove',[R(-80,-170,160,170,'#c4553a',6,OUT,6),*bricks(-80,-170,160,170),R(-44,-100,88,70,'#2a2220',8,OUT,5),R(-80,-182,160,14,'#8f3b27',4,OUT,5)],upright=True)
pr('stove_fire',[{"t":"g","x":0,"y":-30,"shapes":fire()[2:]}],upright=True)
pr('stove_logs',[R(-34,-8,68,12,'#7a4a2a',5,OUT,3),R(-26,-18,52,12,'#8a5a32',5,OUT,3)],upright=True)
pr('chimney',[R(-26,-1500,52,1500,'#c4553a',2,OUT,6),*bricks(-26,-1500,52,1500,40,22),R(-34,-1500,68,18,'#8f3b27',4,OUT,5)],upright=True)
pr('smoke',[{"t":"g","x":0,"y":0,"anim":{"k":"fall","s":-60,"a":160,"dx":18},"shapes":[g for oy in (0,160) for g in [E(0,-oy-20,20,14,'rgba(120,120,130,.7)',None,0),E(10,-oy-90,26,18,'rgba(120,120,130,.5)',None,0)]]}],upright=True)
pr('brick_pile',[R(-50,-30,100,30,'#c4553a',4,OUT,4),R(-40,-58,80,28,'#b84b32',4,OUT,4),R(-28,-84,56,26,'#c4553a',4,OUT,4)],upright=True)

# ── захват 3: трубы, радиаторы, волны
pr('th_t22',therm('th_t22','#ffb04a'),upright=True) if False else None
pr('th_t22',[R(-70,-90,140,90,'#2a2f3d',14,OUT,5),R(-62,-82,124,74,'#1c2230',10,None,0),txt('th_t22',0,-22,46,'#ffb04a')],upright=True)
pr('pipe_h',[R(-27,-18,54,18,'#c98a4a',4,OUT,4),R(-27,-14,54,5,'#e8b27a',None,None,0)],upright=True)
pr('pipe_v',[R(-9,-54,18,54,'#c98a4a',4,OUT,4),R(-5,-54,5,54,'#e8b27a',None,None,0)],upright=True)
pr('pipe_joint',[C(0,-9,13,'#a96f3a',OUT,4)],upright=True)
def rad(c='#f4f4f6'):
    return [R(-58,-118,116,108,c,10,OUT,5),*[R(-46+i*20,-108,12,88,'#d6d9e0',5,None,0) for i in range(6)],R(-52,-10,12,10,'#9aa3b5',2,OUT,3),R(40,-10,12,10,'#9aa3b5',2,OUT,3)]
pr('rad',rad(),upright=True)
def waves(col,n=3,up=True):
    out=[]
    for i in range(n):
        pts=[(-40+i*40+((-1)**j)*10,-j*22) for j in range(8)]
        out.append({"t":"g","x":0,"y":0,"anim":{"k":"sway","s":1.4+i*0.3,"a":5,"ph":i,"pt":[0,0]},"shapes":[L(pts[k][0],pts[k][1],pts[k+1][0],pts[k+1][1],col,7) for k in range(len(pts)-1)]})
    return out
pr('heat_waves',waves('rgba(255,120,60,.85)'),upright=True)
pr('cold_waves',waves('rgba(90,150,235,.9)',4),upright=True)
pr('cold_living',[R(624,714,536,536,'rgba(90,140,220,.2)',None,None,0)],upright=True)
pr('sweater_pr',[R(-40,-30,80,30,'#b5654a',10,OUT,4),R(-60,-26,28,16,'#b5654a',6,OUT,4),R(32,-26,28,16,'#b5654a',6,OUT,4)],upright=True)

# ── захват 4: бак, насосы, котёл, снег, чашка, счёт-2
pr('tank',[R(-70,-250,140,250,['#c5d0e0','#8c9ab0'],46,OUT,5),L(-70,-170,70,-170,OUT,4),L(-70,-90,70,-90,OUT,4),R(-18,-275,36,28,'#9aa3b5',4,OUT,4),R(70,-60,30,18,'#c98a4a',4,OUT,4),R(-100,-60,30,18,'#c98a4a',4,OUT,4)],upright=True)
pr('pump',[R(-34,-34,68,34,'#3d7bc4',8,OUT,5),C(0,-48,30,'#5a95de',OUT,5),{"t":"g","x":0,"y":-48,"anim":{"k":"spin","s":4,"pt":[0,-48]},"shapes":[L(-18,0,18,0,'#fff',6),L(0,-18,0,18,'#fff',6)]},R(-48,-18,16,14,'#c98a4a',3,OUT,4),R(32,-18,16,14,'#c98a4a',3,OUT,4)],upright=True)
pr('boiler',[R(-80,-230,160,230,['#e3e6ec','#b9bfcc'],16,OUT,5),R(-50,-120,100,80,'#2a2220',10,OUT,5),
  {"t":"g","x":0,"y":-42,"anim":{"k":"pulse","s":6,"a":0.12,"pt":[0,0]},"shapes":[P([(-30,0),(-18,-42),(-4,-18),(6,-60),(18,-22),(30,0)],'#f08a2a',None,0),P([(-14,0),(-4,-26),(8,0)],'#ffd24a',None,0)]},
  R(-60,-215,120,36,'#2a2f3d',8,OUT,4),C(-30,-197,9,'#5ad06a',None,0),C(0,-197,9,'#ffd24a',None,0),R(-20,-260,40,32,'#9aa3b5',4,OUT,4)],upright=True)
pr('cup',[R(-20,-32,40,32,'#fff',8,OUT,4),C(26,-18,11,None,OUT,4),L(-12,-38,-12,-50,'rgba(255,255,255,.9)',4),L(6,-38,6,-56,'rgba(255,255,255,.9)',4)],grip=(0,-16),upright=True)
pr('bill_flat',[R(-48,-5,96,5,'#fbfaf3',1,OUT,3),R(-36,-5,40,2,'#c0392b',None,None,0)],upright=True)
def bill2(vk):
    sh=[R(-290,-860,580,860,'#fbfaf3',10,OUT,6),R(-290,-860,580,90,'#4a6fa5',10,OUT,6),txt('b_title',0,-790,46,'#fff'),L(-250,-700,250,-700,'#9aa3b5',4),
        txt('b_el',-250,-620,36,OUT,None,0,'left'),txt('b_w',-250,-500,36,OUT,None,0,'left'),txt('b_heat',-250,-380,36,OUT,None,0,'left'),L(-250,-310,250,-310,'#9aa3b5',4),txt('b_sum',-250,-210,52,OUT,None,0,'left')]
    sh+=[txt(vk+'e',250,-620,38,'#c0392b',None,0,'right'),txt(vk+'w',250,-500,38,'#c0392b',None,0,'right'),txt(vk+'h',250,-380,38,'#c0392b',None,0,'right'),txt(vk+'s',250,-210,56,'#c0392b',None,0,'right')]
    return sh
for k in ('w1','w2','w3','w4'): pr('bill_'+k,bill2(k),upright=True)
pr('snow_out',[R(-2400,-1700,2410,2956,'rgba(232,240,250,.8)',None,None,0),R(1190,-1700,2410,2956,'rgba(232,240,250,.8)',None,None,0),R(-2400,1236,2410,30,'#f6f9fd',None,None,0),R(1190,1236,2410,30,'#f6f9fd',None,None,0),P([(10,-1700),(1190,-1700),(1190,140),(600,-240),(10,140)],'rgba(232,240,250,.85)',None,0),
   P([(-20,150),(600,-250),(1220,150),(1180,150),(600,-205),(20,150)],'#f6f9fd',OUT,4)],upright=True)
pr('snowfall',[{"t":"g","x":0,"y":0,"anim":{"k":"fall","s":120,"a":1900,"dx":-60},"shapes":[g for oy in (0,-1900) for g in [C(random.randint(-1500,2600),random.randint(-1000,1000)+oy,random.choice([4,5,6]),'#ffffff',None,0) for i in range(70)]]}],upright=True)
json.dump(lib,open(LIB,'w'),ensure_ascii=False,indent=2); print('ok9')
