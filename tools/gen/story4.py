import os; REPO=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..'))+'/'
import json, math, copy, sys
sys.path.insert(0,'.')
from bp2_parts import poly,line,ell,rect
OUT='#1e1b26'
LIB=REPO+'library.json'
lib=json.load(open(LIB))
base=copy.deepcopy(lib['locations']['office']['layers'][0])
win=copy.deepcopy(lib['locations']['office']['layers'][1]); win['v']='desk'
def R(x,y,w,h,fill,r=None,st=OUT,sw=5): return rect(x,y,w,h,fill,r,st,sw)
def C(x,y,r,fill,st=OUT,sw=5): return {"t":"circle","x":x,"y":y,"r":r,"fill":fill,**({"stroke":st,"sw":sw} if st else {})}
def T(x,y,key,size,fill='#fff',stroke=None,sw=6,rot=0,align='center'):
    s={"t":"text","x":x,"y":y,"key":key,"size":size,"fill":fill,"align":align}
    if stroke: s["stroke"]=stroke; s["sw"]=sw
    if rot: s["rot"]=rot
    return s

# ───────── desk view: back layer ─────────
desk_back=[ # доска/плакат справа, лампа, стул
  R(700,300,260,170,'#fff',8),R(716,320,230,16,'#d9d9d9',4,None,0),R(716,350,180,12,'#d9d9d9',4,None,0),R(716,376,200,12,'#d9d9d9',4,None,0),
  R(120,600,140,90,'#f2e6a7',4),   # стикер
  # монитор
  {"t":"g","x":0,"y":62,"shapes":[  R(570,740,330,210,'#2a2f3d',14),R(588,758,294,170,'#1c2a3d',6,None,0),
  R(588,758,294,170,['#27415f','#1c2a3d'],6,None,0),
  R(700,950,70,70,'#4a5568',6),R(640,1008,190,22,'#3a4252',9),
  {"t":"rect","x":700,"y":820,"w":70,"h":10,"fill":"#7fb2e6","r":4,"anim":{"k":"blink","s":.25,"a":.25}}]},
  # спинка стула
  R(250,860,190,170,'#4b5568',24),R(330,1030,30,120,'#2f3542',4),
]
desk_front=[ # стол: столешница + тумба; всё остальное за ним скрыто
  R(110,1090,860,26,'#a5784a',6),R(130,1116,820,160,'#8d6a44',4),
  R(150,1132,230,120,'#795a39',6),R(170,1180,190,10,'#5e4429',4,None,0),
  R(700,1132,230,120,'#795a39',6),R(720,1180,190,10,'#5e4429',4,None,0),
  # клавиатура и мышка на столешнице (аккуратно)
  R(420,1072,200,22,'#d9dde6',6),R(650,1078,34,18,'#d9dde6',9),
  R(240,1050,70,42,'#fff',4),R(250,1062,50,5,'#9aa3b5',2,None,0),R(250,1074,40,5,'#9aa3b5',2,None,0),
  R(790,1034,52,58,'#e5342b',8),R(802,1004,8,34,'#2a2f3d',3,None,0),R(818,1010,8,28,'#e6a928',3,None,0),
]
# ───────── clock view ─────────
cx,cy=540,640
clock=[R(0,0,1080,1250,['#e6dfd0','#d6ccb6'],None,None,0),
  C(cx,cy,372,'#2a2f3d',OUT,8),C(cx,cy,340,'#fbfbf4',OUT,6)]
for i in range(60):
    a=math.radians(i*6); big=i%5==0
    r1=330; r2=r1-(34 if big else 14)
    clock.append(line(cx+r1*math.sin(a),cy-r1*math.cos(a),cx+r2*math.sin(a),cy-r2*math.cos(a),'#1e1b26',9 if big else 4))
clock+= [R(cx-14,cy-120,28,0.1,'#000',None,None,0)] if False else []
clock+= [ # метки 12 / 6 ярче
  ell(cx,cy-260,0.1,0.1,'#000')]
# ───────── kitchen view ─────────
kit=[R(0,0,1080,1250,['#e4ecef','#cdd9de'],None,None,0)]
for y in range(0,1000,90):
    kit.append(line(0,y,1080,y,'#b7c5cc',3))
for yi,y in enumerate(range(0,1000,90)):
    for x in range((yi%2)*60-60,1100,120): kit.append(line(x,y,x,y+90,'#b7c5cc',3))
kit+=[R(0,1226,1080,28,'#b9ae9a',None,None,0)]
# труба на стене (справа): вертикальная, с вентилем
kit+=[R(850,0,60,1250,['#9aa3b5','#c9d0dc'],6),R(838,1180,84,40,'#7d8699',6),R(838,780,84,34,'#7d8699',6),R(838,380,84,34,'#7d8699',6),
  R(900,880,90,50,['#9aa3b5','#c9d0dc'],6),R(980,872,30,66,'#7d8699',6)]  # тройник под вентиль
# вентильная площадка: рисуем штурвал отдельным предметом на (940,905)
# тумба/раковина слева-центр
kit+=[R(60,1090,560,28,'#d7d7d2',6),R(80,1118,520,132,['#7a8fa6','#66798f'],4),
  R(110,1140,220,95,'#6b8098',6),R(350,1140,220,95,'#6b8098',6),
  R(230,1050,180,48,['#f4f6f8','#dfe4ea'],8),R(250,1066,140,22,'#c5cdd6',8,None,0),
  # кран: корпус на столешнице, носик над раковиной
  R(312,985,36,70,['#c7ced8','#9aa3b5'],5),
  {"t":"poly","pts":[[322,990],[338,990],[338,962],[400,962],[400,980],[360,980],[360,1000],[322,1000]],"fill":"#aab2bf","stroke":OUT,"sw":5},
  R(374,962,40,26,'#9aa3b5',5),
  # розетка/подоконник/шкафчик сверху
  R(90,340,380,220,'#f6f8fa',10),R(110,360,160,180,'#dfe4ea',6),R(290,360,160,180,'#dfe4ea',6),R(250,440,12,40,'#9aa3b5',4),R(300,440,12,40,'#9aa3b5',4),
  R(500,520,160,0.1,'#000',None,None,0),
]
# ───────── final lib ─────────
office={"groundY":1250,"views":{
  "main":{"title":"общий план: окно и доска (как раньше)"},
  "desk":{"title":"рабочее место инженера, стол спереди"},"corner":{"title":"угол"}}}
loc={"groundY":1250,
 "views":{"desk":{"title":"рабочее место: стол, монитор, стул (герой сидит за столом, поза sit*)"},
          "clock":{"title":"огромные настенные часы 9:00; стрелки — предметы clock_hour/clock_min"},
          "kitchen":{"title":"кухонный угол: раковина, кран слева, вентиль на трубе справа, чайник на столешнице"}},
 "layers":[base,win,
   {"p":1,"v":"desk","shapes":desk_back},
   {"p":1,"v":"desk","z":"front","shapes":desk_front},
   {"p":1,"v":"clock","shapes":clock},
   {"p":1,"v":"kitchen","shapes":kit}]}
lib['locations']['office_day']=loc

# ───────── props ─────────
P=lib['props']
def pr(name,shapes,grip=(0,0),upright=False):
    d={"grip":list(grip),"shapes":shapes}
    if upright: d["upright"]=True
    P[name]=d
# стрелки: основание в (0,0), смотрят вверх
pr('clock_min',[poly([(-14,0),(14,0),(8,-290),(-8,-290)],'#1e1b26'),C(0,0,26,'#1e1b26',None)])
pr('clock_hour',[poly([(-20,0),(20,0),(12,-200),(-12,-200)],'#1e1b26'),C(0,0,30,'#1e1b26',None),C(0,0,10,'#e5342b',None)])
pr('clock_sec',[line(0,40,0,-300,'#e5342b',5),C(0,0,12,'#e5342b',None)])
pr('kettle',[R(-36,-62,72,62,['#e9eef4','#c7ced8'],14),R(-24,-76,48,16,'#aab2bf',6),R(-6,-92,12,18,'#2a2f3d',5),
   poly([(36,-46),(62,-66),(66,-58),(40,-30)],'#c7ced8',OUT,5),
   {"t":"path","box":[-60,-80,30,60]} if False else R(-60,-60,26,34,'#2a2f3d',10,None,0)],grip=(-47,-46),upright=True)
pr('tap_handle',[R(-10,-40,20,40,'#9aa3b5',4),R(-34,-62,68,24,'#e5342b',10)],grip=(0,-24))
pr('valve',[C(0,0,56,None,'#c4332b',16),line(-56,0,56,0,'#c4332b',12),line(0,-56,0,56,'#c4332b',12),C(0,0,14,'#7d8699')],grip=(0,0))
pr('cartridge',[R(-14,-48,28,48,'#c9a227',5),R(-18,-16,36,10,'#7d8699',3),R(-8,-60,16,14,'#9aa3b5',3)],grip=(0,-24),upright=True)
pr('tap_part',[R(-10,-14,20,28,'#9aa3b5',5),C(0,0,5,'#2a2f3d',None)])
pr('cap_part',[ell(0,0,14,9,'#e5342b',OUT,4)])
# тонкая струя в чайник из носика (носик в 374..414, 962 → струя вниз до раковины)
pr('water_thin',[R(-6,0,12,100,'rgba(140,205,255,.9)',4,None,0),
   {"t":"circle","x":0,"y":104,"r":9,"fill":"rgba(190,230,255,.9)","anim":{"k":"pulse","s":3,"a":.25}}])
# ФОНТАН: «промышленная авария» — столб до потолка + брызги. Начало струи в (0,0), столб вверх
fo=[R(-52,-1000,104,1000,'rgba(130,200,255,.88)',None,None,0),R(-84,-1000,168,1000,"rgba(160,215,255,.35)",None,None,0),
    R(-26,-1000,22,1000,'rgba(255,255,255,.6)',None,None,0),
    ell(0,-1000,170,40,'rgba(160,215,255,.5)'),ell(0,-60,90,24,'rgba(190,230,255,.8)')]
for i,(dx,dy,ph) in enumerate([(-130,-840,0),(150,-780,1.1),(-200,-420,2.0),(190,-300,3.1),(-90,-620,4.2),(110,-560,5.0),(-250,-760,.6),(240,-540,2.6)]):
    fo.append({"t":"circle","x":dx,"y":dy,"r":14 if i%2 else 20,"fill":"rgba(170,220,255,.9)","anim":{"k":"bob","s":1.6,"a":40,"ph":ph}})
for i,(dx,ph) in enumerate([(-180,0),(160,1),(-120,2),(210,3)]):
    fo.append({"t":"line","x1":dx,"y1":-20,"x2":dx*.5,"y2":-300,"stroke":"rgba(160,215,255,.75)","sw":14,"anim":{"k":"sway","s":1.2,"a":6,"ph":ph,"pt":None}})
pr('fountain',fo)
# Вода-потоп: широкая полупрозрачная плита, поднимается move y
fl=[R(-700,-900,1480,900,'rgba(98,175,235,.5)',None,None,0),R(-700,-14,1480,14,'rgba(255,255,255,.55)',None,None,0)]
for i in range(8):
    fl.append({"t":"ellipse","x":-560+i*160,"y":-6,"rx":40,"ry":7,"fill":"rgba(255,255,255,.55)","anim":{"k":"slide","s":.5,"a":16,"ph":i}})
pr('flood',fl)
pr('puddle',[ell(0,0,160,22,'rgba(98,175,235,.55)'),ell(-30,-4,70,8,'rgba(255,255,255,.5)')])
# Кружка/колба "чистой мастерской"
pr('clean_tap',[R(-40,-46,80,46,['#d5dbe4','#aab2bf'],6),poly([(-14,-46),(14,-46),(14,-96),(70,-96),(70,-78),(34,-78),(34,-46)],'#c7ced8',OUT,5),R(-20,-130,40,40,'#e5342b',8),R(-34,-98,68,14,'#c7ced8',5)])
pr('clean_tool',[R(-120,-14,240,28,'#d9dde6',8),R(60,-20,70,40,'#e6a928',10),R(-120,-10,40,20,'#c7ced8',5)])
# Экран телефона с видео: большие пальцы не нужны
if __name__=="__main__": json.dump(lib,open(LIB,'w'),ensure_ascii=False,indent=2)
if __name__=="__main__": print("ok")
