import json,math,random
exec(open('s5lib.py').read().split("random.seed(5)")[0])
PR=lib['props']
def pr(n,sh,grip=(0,0),upright=False):
    d={"grip":list(grip),"shapes":sh}
    if upright: d["upright"]=True
    PR[n]=d
EARTH='#8a6a47'; ASPH='#4a4f5c'; BASE='#8f8878'; SOIL='#6b4d33'; GRAV='#a39d92'
# ───── заплатки, трамбовка, бугор ─────
pr('patch',[E(0,0,125,20,'#3a3e49',None,0),E(0,-2,112,14,'#2c2f38',None,0),E(-30,-4,50,4,'rgba(255,255,255,.12)',None,0)])
pr('bump',[E(0,0,170,30,'#6b7282',None,0),E(-20,-8,120,14,'#868ea0',None,0)])
pr('rubble',[C(-40,0,12,'#9a948a',OUT,3),C(0,4,16,'#aaa49a',OUT,3),C(38,0,11,'#8c867c',OUT,3),C(14,-8,9,'#b3ada3',OUT,3)])
# ───── траншеи (в полосе дороги, начало — центр) ─────
def trench(w,kind):
    h=w/2; s=[R(-h,-40,w,84,'#6b4d33',12,OUT,5),R(-h+14,-26,w-28,64,'#3b2a1c',8,None,0)]
    if kind=='pipe': s+=[R(-h+6,-20,w-12,34,'#4d9be6',17,OUT,5),R(-h+30,-12,w-60,8,'rgba(255,255,255,.45)',4,None,0)]+[R(x-8,-22,16,38,'#2f6db8',4,OUT,3) for x in range(int(-h+120),int(h-60),200)]
    if kind=='cable': s+=[R(-h+6,-20,w-12,34,'#4d9be6',17,OUT,5),R(-h+30,-12,w-60,8,'rgba(255,255,255,.45)',4,None,0),R(-h+20,22,w-40,12,'#222',6,OUT,3)]+[R(x,22,26,12,'#ffd24a',2,None,0) for x in range(int(-h+60),int(h-60),90)]
    if kind=='new': s+=[R(-h+6,-20,w-12,34,'#5fbf6a',17,OUT,5),R(-h+30,-12,w-60,8,'rgba(255,255,255,.45)',4,None,0)]+[R(x-8,-22,16,38,'#2f8a3a',4,OUT,3) for x in range(int(-h+120),int(h-60),200)]
    if kind=='gravel': s=[R(-h,-40,w,84,GRAV,12,OUT,5)]+[C(-h+30+((i*53)%int(w-60)),-20+(i*29)%60,8,'#8c867c',None,0) for i in range(14)]
    return s
for k in ('empty','pipe','cable','new','gravel'): pr('trench_'+k,trench(640,k))
# ───── разрезы дороги в «небе» (без слов) ─────
def xs(dip=0,pipe=None,cable=False,fix=False,tilt=0):
    s=[R(-360,-230,720,460,'#fffdf5',22,OUT,6),R(-330,-200,660,70,'#cfe9f7',None,None,0)]
    def band(y0,y1,col,d):   # слой с прогибом посередине
        top=[(x,y0+d*(1-(x/330)**2)) for x in range(-330,331,55)]; bot=[(x,y1+d*(1-(x/330)**2)) for x in range(330,-331,-55)]
        return P(top+bot,col,OUT,4)
    s+=[R(-330,-30,660,200,SOIL,None,None,0)]
    s+=[band(-70,-30,BASE,dip),band(-110,-70,ASPH,dip)] if not fix else [band(-110,-90,ASPH,0),band(-90,-60,'#2f333d',0),band(-60,-30,GRAV,0),band(-30,10,BASE,0)]
    s+=[C(-250+i*80,-50+((i*37)%20),5,'#77716a',None,0) for i in range(8)] if not fix else [C(-300+i*40,-45,5,'#8c867c',None,0) for i in range(16)]
    if dip: s+=[L(-60,-100+dip,-20,-70+dip,'#222',4),L(20,-100+dip,50,-76+dip,'#222',4)]
    if pipe=='old': s+=[C(0,70,38,'#4d9be6',OUT,6),C(0,70,24,'#bfe0fa',None,0)]
    if pipe=='new': s+=[C(0,120,38,'#5fbf6a',OUT,6),C(0,120,24,'#c9f0cf',None,0)]
    if cable: s+=[C(140,20,16,'#ffd24a',OUT,4),C(140,20,8,'#222',None,0)]
    if tilt:
        a=math.radians(tilt); s=[R(-360,-230,720,460,'#fffdf5',22,OUT,6),R(-330,-200,660,400,'#cfe9f7',None,None,0),
          L(-320,60,320,60,'#999',4),P([(-320,60-320*math.sin(a)*0.9+30),(320,60+320*math.sin(a)*0.9+30),(320,120+320*math.sin(a)*0.9+30),(-320,120-320*math.sin(a)*0.9+30)],ASPH,OUT,5),
          R(-120,-120,240,60,'#f4c52a',14,OUT,5),R(-60,-108,120,36,'#c9f2c0',10,OUT,4),E(40,-90,18,10,'#5ec45e',OUT,3)]
    return s
pr('xs_ok',xs(),upright=True); pr('xs_sag',xs(dip=26),upright=True); pr('xs_pipe',xs(dip=26,pipe='old'),upright=True)
pr('xs_cable',xs(dip=26,pipe='old',cable=True),upright=True); pr('xs_fix',xs(fix=True,pipe='new'),upright=True); pr('xs_tilt',xs(tilt=6),upright=True)
# ───── танк ─────
pr('army_tank',[R(-270,-92,540,92,'#3d4a3a',46,OUT,6),*[C(x,-46,34,'#59664f',OUT,4) for x in range(-210,211,84)],*[C(x,-46,8,'#2a3328',None,0) for x in range(-210,211,84)],
  P([(-230,-92),(-190,-170),(180,-170),(240,-92)],'#5b7a4a',OUT,6),R(-110,-236,230,70,'#6b8c58',18,OUT,6),R(100,-212,260,22,'#3d4a3a',8,OUT,5),R(340,-216,24,30,'#2a3328',6,OUT,4),C(-40,-250,16,'#3d4a3a',OUT,4)],upright=True)
# ───── насыпь и съезд ─────
def mound(W,Wt,H):
    s=[P([(-W/2,0),(-Wt/2,-H),(Wt/2,-H),(W/2,0)],EARTH,OUT,6),P([(-W/2+160,0),(-Wt/2+60,-H+40),(Wt/2-60,-H+40),(W/2-160,0)],'#9b7a54',None,0),
       R(-Wt/2-6,-H-26,Wt+12,30,ASPH,6,OUT,6)]+[R(-Wt/2+30+i*90,-H-14,50,8,'#fff',3,None,0) for i in range(int((Wt-60)//90))]
    return s
pr('emb_a',mound(1000,640,150),upright=True); pr('emb_b',mound(1500,640,290),upright=True); pr('emb_c',mound(2200,640,430),upright=True)
H=430
pr('cliff',[R(-1500,-H,1500,H,EARTH,None,OUT,6),*[L(-1500,-H+i*86,0,-H+i*86,'rgba(0,0,0,.12)',4) for i in range(1,5)],R(-1500,-H-26,1500,30,ASPH,6,OUT,6),*[R(-1450+i*100,-H-14,56,8,'#fff',3,None,0) for i in range(15)]],upright=True)
for k in range(1,6):
    x0,x1=300*(k-1),300*k; y0,y1=-H+86*(k-1),-H+86*k
    pr(f'ramp_{k}',[P([(x0,y0),(x1,y1),(x1,0),(x0,0)],EARTH,OUT,6),P([(x0,y0-26),(x1,y1-26),(x1,y1+4),(x0,y0+4)],ASPH,OUT,6),P([(x0+60,y0-14),(x0+110,y0-14+ (y1-y0)/6),(x0+110,y0-8+(y1-y0)/6),(x0+60,y0-8)],'#fff',None,0)],upright=True)
# ───── дома деревни (сбоку) ─────
def vh(wall,roof,w=230,h=150):
    return [R(-w/2,-h,w,h,wall,None,OUT,5),P([(-w/2-16,-h),(0,-h-84),(w/2+16,-h)],roof,OUT,5),R(w/2-60,-h-80,26,54,'#8f4528',None,OUT,4),R(-w/2+26,-h+36,56,50,'#bfe3f7',5,OUT,4),R(10,-h+30,64,h-30,'#8a5f3a',6,OUT,4),C(62,-h+78,5,'#ffd24a',None,0)]
pr('vh_a',vh('#f3d88e','#d9533b'),upright=True); pr('vh_b',vh('#cfe0ee','#3f6fb0',250,160),upright=True); pr('vh_c',vh('#e8c7a4','#5a8a4a',210,140),upright=True)
json.dump(lib,open(LIB,'w'),ensure_ascii=False,indent=2); print('ok12 props')
