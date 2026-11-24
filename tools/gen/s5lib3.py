import json,random,math,sys,copy
exec(open('s5lib2.py').read().split("# ───── бульдозер")[0])   # helpers, wheel(), PR, pr, lib (fresh)
def flipshape(s):
    s=copy.deepcopy(s); t=s['t']
    if t=='rect': s['x']=-s['x']-s['w']
    elif t=='poly': s['pts']=[[-x,y] for x,y in s['pts']]
    elif t in('circle','ellipse'): s['x']=-s['x']
    elif t=='line': s['x1']=-s['x1']; s['x2']=-s['x2']
    elif t=='g': s['x']=-s.get('x',0); s['shapes']=[flipshape(c) for c in s['shapes']]
    return s
def recolor(shapes,mp):
    txt=json.dumps(shapes)
    for a,b in mp.items(): txt=txt.replace(a,b)
    return json.loads(txt)
base=lib['props']['car']['shapes']
def driver(col): return [C(-60,-420,40,'#e8b88a',None,0),R(-120,-390,120,100,col,30,None,0)]
cols={'blue':({"#e8483e":"#4a8fe0","#c4332b":"#2f6fc2","#a82a23":"#245aa0","#d63d33":"#3d7fd0"},'#2f4a7a'),
      'yellow':({"#e8483e":"#f4c52a","#c4332b":"#d9a416","#a82a23":"#b78612","#d63d33":"#e8b81f"},'#6a4a2a'),
      'green':({"#e8483e":"#5cb85c","#c4332b":"#3f9a45","#a82a23":"#2f7d36","#d63d33":"#4da852"},'#8a3a3a'),
      'white':({"#e8483e":"#f2f4f7","#c4332b":"#c7ced8","#a82a23":"#9aa3b5","#d63d33":"#e2e6ec"},'#3a3a4a')}
for n,(mp,dc) in cols.items():
    sh=driver(dc)+recolor(base,mp)
    pr('car_'+n,sh); pr('car_'+n+'_l',[flipshape(s) for s in sh])
# фургон: коробка сзади
def van(mp,dc,flip=False):
    sh=driver(dc)+recolor(base,mp)
    box=[R(-430,-560,330,260,'#f2f4f7',16),R(-415,-540,300,40,'#4a8fe0',6,None,0)]
    sh=box+sh
    return [flipshape(s) for s in sh] if flip else sh
pr('van',van(cols['white'][0],'#3a3a4a')); pr('van_l',van(cols['white'][0],'#3a3a4a',True))
# ───── дорога (полоса в 260 высоты), ямы
pr('road_wide',[R(-3600,-4,7200,266,'#b99768',None,None,0),R(-3600,-4,7200,10,'#d2b588',None,None,0),R(-3600,60,7200,10,'#a58555',None,None,0),R(-3600,150,7200,12,'#a58555',None,None,0),R(-3600,230,7200,10,'#a58555',None,None,0)])
pr('pothole',[E(0,0,120,18,'#4a3826'),E(0,-2,98,11,'#2e2218'),E(-20,-3,50,5,'rgba(140,175,205,.6)')])
pr('puddle_b',[E(0,0,150,20,'#8a6a47'),E(0,-1,126,13,'rgba(130,170,205,.85)'),E(-30,-3,40,4,'rgba(255,255,255,.55)')])
def seg260(col,top,extra=None):
    sh=[R(-122,-4,244,266,col,None,None,0),R(-122,-4,244,10,top,None,None,0)]
    return sh+(extra or [])
pr('base_seg',seg260('#8f8878','#a9a291',[C(x,y,9,c,None,0) for x,y,c in [(-80,40,'#77716a'),(10,110,'#aaa396'),(70,190,'#77716a'),(-60,230,'#aaa396'),(50,50,'#aaa396')]]))
pr('asphalt_seg',seg260('#4a4f5c','#5d6372'))
pr('curbs',[R(-3600,-12,7200,20,'#e6e9ee',None,None,0),R(-3600,250,7200,20,'#e6e9ee',None,None,0)])
pr('marking',[R(x,120,110,14,'#fff',4,None,0) for x in range(-3600,3600,260)]+[R(-3600,40,7200,6,'#fff',None,None,0),R(-3600,210,7200,6,'#fff',None,None,0)])
pr('sign',[R(-8,-380,16,380,'#8a93a5',4),C(0,-420,64,'#fff',OUT,6),C(0,-420,50,'#e5342b',None),C(0,-420,34,'#fff',None),R(-6,-452,12,64,'#2a2f3d',3,None,0)])
pr('lamp',[R(-8,-520,16,520,'#4a5568',4),L(0,-520,70,-540,'#4a5568',12),R(52,-552,64,22,'#ffe27a',8)])
# ───── экскаватор и асфальтоукладчик
ex=[R(-330,-150,660,150,'#2a2f3d',70),R(-300,-300,560,160,['#ff9f2f','#e07f10'],20),R(-320,-340,130,90,'#7d8699',14),R(-30,-390,300,100,['#ff9f2f','#e07f10'],18),
 P([(-250,-300),(-235,-520),(-45,-520),(-30,-300),(-60,-300),(-75,-496),(-210,-496),(-225,-300)],'#e07f10'),R(-240,-528,206,22,'#b0630b',8),
 P([(-235,-300),(-210,-496),(-75,-496),(-60,-300)],'rgba(170,215,240,.22)',None,0)]
for wx in (-250,-85,85,250): ex.append(wheel(wx,-75,46,1.0,'#3a4252'))
ex.append({"t":"g","x":150,"y":-330,"anim":{"k":"sway","s":0.45,"a":9},"shapes":[
   P([(-20,14),(300,-150),(330,-120),(8,50)],['#ff9f2f','#e07f10'][1]),
   {"t":"g","x":310,"y":-135,"anim":{"k":"sway","s":0.9,"a":14,"ph":1.2},"shapes":[P([(-14,0),(170,120),(150,160),(-30,34)],'#e07f10'),P([(110,120),(210,110),(240,190),(150,200)],'#7d8699')]}]})
pr('excavator',ex); pr('exc_seat',[R(-200,-320,70,140,'#4a5568',16),R(-200,-200,150,30,'#3c4556',8)])
pv=[R(-260,-150,560,150,'#2a2f3d',66),R(-250,-290,430,150,['#f4c52a','#d9a416'],18),
 P([(180,-290),(380,-420),(420,-290)],'#d9a416'),R(-340,-170,100,70,'#4a5568',10),   # хоппер и выглаживающая плита
 P([(-190,-290),(-190,-520),(-190,-520)],'#d9a416',None,0),
 L(-170,-290,-170,-520,'#b78612',16),L(30,-290,30,-520,'#b78612',16),R(-190,-530,240,22,'#b78612',8)]
for wx in (-190,-60,70,200): pv.append(wheel(wx,-75,44,1.0,'#3a4252'))
pr('paver',pv); pr('paver_seat',[R(-130,-330,70,140,'#4a5568',16),R(-130,-200,150,30,'#3c4556',8)])
# ───── вид сверху: дороги и развязка (origin = (540, y) снизу полосы)
aer_lib=[l for l in lib['locations']['field']['layers'] if l.get('v')=='aerial'][0]
if not any(l.get('v')=='aerial2' for l in lib['locations']['field']['layers']):
    lib['locations']['field']['layers'].append({"p":1,"v":"aerial2","shapes":aer_lib['shapes'][:-3]})
    lib['locations']['field']['views']['aerial2']={"title":"вид сверху без меток: для сцен с дорогой и городом (те же поля, деревня на горизонте)"}
def vroad(w,h,dash=True,median=0,col='#59606e'):
    sh=[R(-w/2,-h,w,h,col,None,None,0),R(-w/2,-h,5,h,'#e8ecf2',None,None,0),R(w/2-5,-h,5,h,'#e8ecf2',None,None,0)]
    if median: sh+= [R(-median/2,-h,median,h,'#7fb668',None,None,0)]
    elif dash: sh+= [R(-3,-h+y,6,40,'#fff',None,None,0) for y in range(0,int(h),120)]
    return sh
pr('aer_road1',vroad(120,7600)); pr('aer_road2',vroad(240,7600,True)); 
pr('aer_road4',vroad(520,7600,False,80))
pr('aer_lights',[C(sx*330,-y,26,'#ffe27a',None,0) for y in range(200,7600,300) for sx in (-1,1)])
pr('aer_barriers',[R(-286,-7600,16,7600,'#c7ced8',None,None,0),R(270,-7600,16,7600,'#c7ced8',None,None,0)])
cross=[R(-6000,-150,12000,300,'#59606e',None,None,0),R(-6000,-6,12000,12,'#fff',None,None,0)]
for sx in (-1,1):
    for sy in (-1,1):
        cross.append({"t":"circle","x":sx*620,"y":sy*620,"r":380,"fill":None,"stroke":"#59606e","sw":120})
pr('aer_cross',cross)
pr('aer_bypass',[{"t":"circle","x":0,"y":0,"r":2300,"fill":None,"stroke":"#59606e","sw":280},{"t":"circle","x":0,"y":0,"r":2300,"fill":None,"stroke":"#fff","sw":16}])
json.dump(lib,open(LIB,'w'),ensure_ascii=False,indent=2)
print('ok3')
