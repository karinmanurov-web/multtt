import json,random,copy
exec(open('s5lib2.py').read().split("# ───── бульдозер")[0])
random.seed(10)
F2='#ece4f2'
def txt(key,x,y,size,fill='#fff',st=OUT,sw=0,align='center'):
    return {"t":"text","key":key,"x":x,"y":y,"size":size,"fill":fill,"stroke":st,"sw":sw,"align":align}
def bricks_(*a): return []
# ───── локация cottage2 = cottage + доработки для сюжета 10
base=lib['locations']['cottage']
ex=[]
ex.append(R(655,612,112,82,F2,None,None,0))                                   # убрали тумбочку справа
# ванная (этаж 2, справа): плитка, зеркало, раковина
ex.append(R(626,520,154,170,'#cfe6ee',None,None,0))
for k in range(5): ex.append(L(626,520+k*34,780,520+k*34,'rgba(0,0,0,.10)',2))
for k in range(5): ex.append(L(626+k*38,520,626+k*38,690,'rgba(0,0,0,.10)',2))
ex+=[R(648,380,90,110,'#f2f8fb',10,OUT,5),L(660,470,700,400,'rgba(255,255,255,.9)',8)]
ex+=[R(676,630,38,60,'#fff',6,OUT,4),R(650,596,90,36,'#fff',14,OUT,5)]
# тумбочка у кровати и дверь, шахта в котельную
ex+=[R(376,326,138,366,F2,None,None,0),R(552,616,46,74,'#a9855a',6,OUT,5),L(552,650,598,650,OUT,4),R(568,660,14,8,'#6f4a2b',3,None,0)]
ex+=[R(10,1060,30,190,'#8a5f3a',None,OUT,5),C(32,1160,6,'#ffd24a',None,0)]
steps=[(-380,1250)]
for k in range(14):
    xk=-380+k*25.7; yk=1250+k*40
    steps+=[(xk+25.7,yk),(xk+25.7,yk+40)]
steps=steps[:-1]+[(10,1810),(10,1250)]
ex.append(P(steps,'#3a3342',OUT,5))
for k in range(14): ex.append(L(-380+k*25.7+25.7-3,1250+k*40+40,-380+k*25.7+25.7+22,1250+k*40+40,'#b79a7a',5))
ex.append(R(10,1690,30,120,'#4a3220',None,OUT,5))
lib['locations']['cottage2']={"groundY":1250,"views":{},"layers":copy.deepcopy(base_layers:=base["layers"])+[{"p":1,"shapes":ex}]}
# ───── ночь
def stars(xr,yr,n):
    return [C(random.randint(*xr),random.randint(*yr),random.choice([2,3,3,4]),'rgba(255,255,255,.9)',None,0) for _ in range(n)]
NF='rgba(8,14,40,.80)'
pr('night_out',[R(-2400,-1700,2410,2956,NF,None,None,0),R(1190,-1700,2410,2956,NF,None,None,0),P([(10,-1700),(1190,-1700),(1190,140),(600,-240),(10,140)],NF,None,0),
    *stars((-2300,0),(-1500,1100),40),*stars((1200,3500),(-1500,1100),40),*stars((20,1180),(-1500,-300),14)],upright=True)
pr('moon',[C(0,0,150,'rgba(255,240,190,.18)',None,0),C(0,0,100,'rgba(255,240,190,.3)',None,0),C(0,0,64,'#fff3c4',None,0),C(22,-10,56,NF,None,0)],upright=True)
pr('night_dim',[R(10,130,1180,1710,'rgba(10,20,60,.24)',None,None,0)],upright=True)
pr('night_dim2',[R(10,130,1180,1710,'rgba(10,20,60,.22)',None,None,0)],upright=True)
pr('lamp_on',[R(-16,-10,32,10,'#6f4a2b',3,OUT,3),R(-4,-52,8,44,'#6f4a2b',2,None,0),P([(-34,-52),(34,-52),(22,-96),(-22,-96)],'#ffd77a',OUT,4)],upright=True)
pr('lamp_off',[R(-16,-10,32,10,'#6f4a2b',3,OUT,3),R(-4,-52,8,44,'#6f4a2b',2,None,0),P([(-34,-52),(34,-52),(22,-96),(-22,-96)],'#b59a62',OUT,4)],upright=True)
pr('lamp_glow',[E(0,-70,250,190,'rgba(255,215,120,.14)',None,0),E(0,-70,170,130,'rgba(255,215,120,.16)',None,0),E(0,-70,90,70,'rgba(255,230,160,.22)',None,0)],upright=True)
pr('blanket',[R(0,-118,320,118,'#86a9d8',34,OUT,5),R(0,-118,40,118,'#9bbbe3',20,OUT,5),*[L(60+i*52,-112,60+i*52,-8,'rgba(255,255,255,.5)',6) for i in range(5)]],upright=True)
pr('pillow_c',[R(-88,-176,176,176,'#fff',48,OUT,5),L(-50,-120,50,-120,'rgba(0,0,0,.12)',5),L(-40,-70,40,-70,'rgba(0,0,0,.12)',5)],upright=True)
pr('pillow',[R(-70,-52,140,52,'#fff',24,OUT,5)],upright=True)
# кран и капля
pr('tap',[R(-7,-30,14,30,'#b8c0cc',3,OUT,4),P([(-7,-30),(-7,-52),(26,-52),(26,-40),(16,-40),(16,-44),(7,-44),(7,-30)],'#b8c0cc',OUT,4),R(-14,-60,28,10,'#e04a4a',4,OUT,3)],upright=True)
pr('drop',[P([(0,-18),(-7,-4),(0,4),(7,-4)],'#6fc3ff',OUT,3)],upright=True)
# холодильник-двойник (трясётся) и звуковые волны
fr=[R(60,870,100,380,['#a9b1c4','#8f98ae'],14,OUT,5),L(70,1010,150,1010,'#6f7788',4),R(138,930,10,50,'#6f7788',4,None,0),R(138,1040,10,70,'#6f7788',4,None,0)]
pr('fridge_ov',[{"t":"g","x":0,"y":0,"anim":{"k":"shake","s":1.0,"a":3,"pt":[110,1250]},"shapes":fr}],upright=True)
pr('fridge_ov2',[{"t":"g","x":0,"y":0,"anim":{"k":"shake","s":1.6,"a":8,"pt":[110,1250]},"shapes":fr}],upright=True)
def arcs(col,n=3):
    out=[]
    for i in range(n):
        r=40+i*34
        pts=[(r*math.cos(a/6*1.2-0.6),r*math.sin(a/6*1.2-0.6)) for a in range(7)]
        out.append({"t":"g","x":0,"y":0,"anim":{"k":"pulse","s":2.4,"a":0.07,"ph":i*0.8,"pt":[0,0]},"shapes":[L(pts[k][0],pts[k][1],pts[k+1][0],pts[k+1][1],col,8) for k in range(6)]})
    return out
import math
pr('hum_waves',arcs('rgba(255,255,255,.9)'),upright=True)
pr('hum_waves_r',arcs('rgba(255,90,70,.95)',4),upright=True)
# звуковые подписи
SND={'snd_zzz':("Z z z",70,'#bfd3ff'),'snd_kap':("Кап.",64,'#fff'),'snd_uu':("Ууу…",70,'#fff'),'snd_UU':("УУУУ!!!",96,'#ffd24a')}
for k,(t_,sz,col) in SND.items():
    pr(k,[txt(k,0,0,sz,col,OUT,9)],upright=True)
pr('snd_zzz',[{"t":"g","x":0,"y":0,"anim":{"k":"bob","s":0.5,"a":10},"shapes":[txt('snd_zzz',0,0,70,'#bfd3ff',OUT,9)]}],upright=True)

# ── захват 2: радиатор, насос, полив, козырёк
def rad_(c='#f4f4f6'):
    return [R(-58,-118,116,108,c,10,OUT,5),*[R(-46+i*20,-108,12,88,'#d6d9e0',5,None,0) for i in range(6)],R(-52,-10,12,10,'#9aa3b5',2,OUT,3),R(40,-10,12,10,'#9aa3b5',2,OUT,3),C(50,-124,7,'#c98a4a',OUT,3)]
pr('rad_shake',[{"t":"g","x":0,"y":0,"anim":{"k":"shake","s":1.4,"a":4,"pt":[0,0]},"shapes":rad_()}],upright=True)
bub=[{"t":"g","x":x,"y":-30,"anim":{"k":"bob","s":1.2+i*0.3,"a":22,"ph":i},"shapes":[C(0,0,r,'rgba(255,255,255,.9)',OUT,3)]} for i,(x,r) in enumerate(((-36,8),(-12,11),(12,7),(36,10)))]
pr('rad_bubbles',[{"t":"g","x":0,"y":0,"anim":{"k":"shake","s":0.8,"a":2,"pt":[0,0]},"shapes":rad_('#cfe4f6')+bub}],upright=True)
pr('air_puffs',[{"t":"g","x":0,"y":0,"anim":{"k":"bob","s":1.5+i*0.4,"a":12,"ph":i},"shapes":[E(i*16,-i*26,12,9,'rgba(255,255,255,.85)',OUT,3)]} for i in range(4)],upright=True)
for k,(t_,sz,col) in {'snd_tuk':("Тук-тук-тук",64,'#fff'),'snd_shsh':("Ш-ш-ш…",70,'#cfeaff'),'snd_bul':("Бульк-бульк!",70,'#8fd8ff'),'snd_zh':("Ж-ж-ж…",80,'#ffd24a'),'snd_dzin':("Дзынь.",64,'#fff'),'snd_ss':("Ш-ш-ш-ш…",86,'#9fe0ff')}.items():
    pr(k,[txt(k,0,0,sz,col,OUT,9)],upright=True)
def pump_(spin=True,shake=0):
    sh=[R(-34,-34,68,34,'#3d7bc4',8,OUT,5),C(0,-48,30,'#5a95de',OUT,5)]
    if spin: sh.append({"t":"g","x":0,"y":-48,"anim":{"k":"spin","s":6,"pt":[0,-48]},"shapes":[L(-18,0,18,0,'#fff',6),L(0,-18,0,18,'#fff',6)]})
    else: sh+=[L(-18,-48,18,-48,'#fff',6),L(0,-66,0,-30,'#fff',6)]
    sh+=[R(-48,-18,16,14,'#c98a4a',3,OUT,4),R(32,-18,16,14,'#c98a4a',3,OUT,4)]
    return [{"t":"g","x":0,"y":0,"anim":{"k":"shake","s":1.8,"a":shake,"pt":[0,0]},"shapes":sh}] if shake else sh
pr('pump_off',pump_(False),upright=True)
pr('pump_ov',pump_(True,4),upright=True)
pr('pump_dead',[*pump_(False)[:2],L(-18,-48,18,-48,'#9aa3b5',6)],upright=True)
# полив и щиток
pr('timer_box',[R(-28,-70,56,70,'#cfd6e2',8,OUT,5),C(0,-48,9,'#e04a4a',OUT,3),R(-14,-26,28,12,'#2a2f3d',3,None,0)],upright=True)
pr('timer_box_off',[R(-28,-70,56,70,'#cfd6e2',8,OUT,5),C(0,-48,9,'#6a7380',OUT,3),R(-14,-26,28,12,'#2a2f3d',3,None,0)],upright=True)
def jet(dx,h,n=7):
    out=[]
    for k in range(n):
        u=k/(n-1); x=-dx*u; y=-30-4*h*u*(1-u)
        out.append(C(x,y,5-1.5*u,'#7fd0ff',None,0))
    return out
pr('sprinkler',[R(-6,-26,12,26,'#2a2f3d',2,None,0),C(0,-32,12,'#3d7bc4',OUT,4),
  *[{"t":"g","x":0,"y":0,"anim":{"k":"bob","s":3.0+i*0.5,"a":6,"ph":i},"shapes":jet(95,100+i*20)} for i in range(3)],
  {"t":"g","x":0,"y":0,"anim":{"k":"bob","s":4,"a":10},"shapes":[C(-98+i*2,-44-i*14,6,'#bfeaff',None,0) for i in range(4)]}],upright=True)
pr('wall_splash',[{"t":"g","x":0,"y":0,"anim":{"k":"bob","s":3.5+i*0.7,"a":8,"ph":i},"shapes":[E(0,-i*24,6,9,'#7fd0ff',None,0)]} for i in range(4)],upright=True)
pr('visor',[P([(-80,2),(20,-16),(20,-4),(-80,14)],'#d5dbe6',OUT,5)],upright=True)

# ── захват 3: лист на крыше, лестница, будильник, шторки
th_=math.atan2(380,590); Ax=210; Ay=140-(Ax-10)*380/590
dx_,dy_=-math.cos(th_),math.sin(th_); nx_,ny_=-math.sin(th_),-math.cos(th_)
Ax,Ay=Ax-22*nx_,Ay-22*ny_   # центр листа внутри кровли (на плитке)
def _rot(px,py,cx,cy,ang):
    c,s=math.cos(ang),math.sin(ang); x,y=px-cx,py-cy
    return (cx+x*c-y*s,cy+x*s+y*c)
def sheet(amp,sp,col='#c5ccd8'):
    # лист лежит на скате у верхнего края; свободный конец качается от поверхности наружу (поворот на +amp, качание ±amp)
    pts=[(Ax,Ay),(Ax+200*dx_,Ay+200*dy_),(Ax+200*dx_+16*nx_,Ay+200*dy_+16*ny_),(Ax+16*nx_,Ay+16*ny_)]
    ang=math.radians(amp)
    for sgn in (1,-1):
        t=_rot(pts[1][0],pts[1][1],Ax,Ay,sgn*ang)
        if (t[0]-pts[1][0])*nx_+(t[1]-pts[1][1])*ny_>0: break
    pts=[_rot(x,y,Ax,Ay,sgn*ang) for x,y in pts]
    poly=P(pts,col,OUT,4)
    return [{"t":"g","x":0,"y":0,"anim":{"k":"sway","s":sp,"a":amp,"pt":[Ax,Ay]},"shapes":[poly]},C(Ax,Ay,6,'#6f7788',OUT,3)]
pr('roof_sheet',sheet(7,5),upright=True)
pr('roof_sheet2',sheet(16,8),upright=True)
pr('roof_sheet3',sheet(26,11),upright=True)
rails=[R(-26,-1120,10,1120,'#d9b26a',3,OUT,4),R(16,-1120,10,1120,'#d9b26a',3,OUT,4)]+[R(-24,-y,48,8,'#d9b26a',2,OUT,3) for y in range(60,1120,64)]
pr('ladder',rails,upright=True)
def windl(n,col):
    return [{"t":"g","x":0,"y":0,"anim":{"k":"sway","s":2+i*0.4,"a":3,"ph":i,"pt":[0,0]},"shapes":[L(-300-i*40,-400+i*90,-120-i*40+(i%2)*60,-400+i*90,col,6)]} for i in range(n)]
pr('wind_a',windl(4,'rgba(220,230,250,.55)'),upright=True)
pr('wind_b',windl(8,'rgba(235,242,255,.8)'),upright=True)
pr('shutter',[R(-108,-214,216,214,'#59607a',8,OUT,5),*[L(-100,-y,100,-y,'#3d4358',4) for y in range(20,214,26)]],upright=True)
pr('alarm',[{"t":"g","x":0,"y":-6,"anim":{"k":"shake","s":2.2,"a":3,"pt":[0,0]},"shapes":[C(-26,-82,13,'#c0392b',OUT,4),C(26,-82,13,'#c0392b',OUT,4),C(0,-40,40,'#e04a4a',OUT,5),C(0,-40,31,'#fff',OUT,3),R(-12,-4,24,10,'#9a2d22',3,OUT,3),txt('clk',0,-27,21,OUT,None,0)]}],upright=True)
pr('black_s',[R(-2400,-1800,6400,4800,'rgba(0,0,0,.35)',None,None,0)],upright=True)
pr('black_f',[R(-2400,-1800,6400,4800,'#000',None,None,0)],upright=True)
for k,(t_,sz,col) in {'snd_bam':("Бам!",90,'#fff'),'snd_hlop':("ХЛОП!",110,'#ffd24a'),'snd_shk':("Щёлк.",64,'#fff'),'snd_ring':("Дзынь-дзынь!",96,'#ffd24a')}.items():
    pr(k,[txt(k,0,0,sz,col,OUT,9)],upright=True)
json.dump(lib,open(LIB,'w'),ensure_ascii=False,indent=2); print('ok10')
