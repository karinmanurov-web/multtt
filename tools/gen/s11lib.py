import json,math,random
exec(open('s5lib.py').read().split("random.seed(5)")[0])
random.seed(11)
PR=lib['props']
def pr(n,sh,grip=(0,0),upright=False):
    d={"grip":list(grip),"shapes":sh}
    if upright: d["upright"]=True
    PR[n]=d
def txt(key,x,y,size,fill='#fff',st=OUT,sw=0,align='center'):
    return {"t":"text","key":key,"x":x,"y":y,"size":size,"fill":fill,"stroke":st,"sw":sw,"align":align}
PINK='#ff5fa2'; PINK2='#ffd0e4'; GR='#b8bcc6'
# ───── листы с эскизами (в руке; ≈150×190) ─────
def sheet(inner,col='#fffdf5'):
    return [R(-75,-95,150,190,col,6,OUT,5),*inner]
def hs(x=0,y=0,k=1.0,roof=True,walls=True,fnd=True):   # маленький домик на эскизе, основание в (x,y)
    s=[]
    if fnd: s.append(R(x-50*k,y-6*k,100*k,10*k,'#9aa3b2',None,OUT,3))
    if walls: s.append(R(x-42*k,y-52*k,84*k,46*k,'#f1d58a',None,OUT,3))
    if roof: s.append(P([(x-50*k,y-52*k),(x,y-86*k),(x+50*k,y-52*k)],'#d9533b',OUT,3))
    return s
pr('sk_house',sheet(hs(0,40,1.1)),upright=True)
pr('sk_garage',sheet(hs(-18,40,0.9)+[R(18,10,48,30,'#c6ccd8',None,OUT,3),R(24,22,36,18,'#8f98a8',None,OUT,2),
    {"t":"text","key":"_","x":0,"y":0,"size":1,"fill":"#0000"}][:-1]),upright=True)
pr('sk_tower',sheet(hs(-20,50,0.8)+[R(26,-60,34,110,'#c9a27a',None,OUT,3),P([(22,-60),(43,-92),(64,-60)],'#d9533b',OUT,3),C(43,-34,7,'#bfe3f7',OUT,2)]),upright=True)
def lolli(x,y,r,stick=14):
    s=[R(x-stick/2,y,stick,60,'#f4f4f4',None,OUT,3),C(x,y,r,PINK,OUT,4),C(x,y,r*.55,PINK2,None,0),C(x,y,r*.2,PINK,None,0)]
    return s
pr('sk_lolli',sheet(lolli(0,-10,44)+[L(-50,50,50,50,'#9aa3b2',4)]),upright=True)
pr('sk_lolli2',sheet(lolli(0,-30,60,22)+[L(-50,50,50,50,'#9aa3b2',4)]),upright=True)
pr('sk_float',sheet([C(-34,-56,16,'#fff3a0',None,0),E(40,-60,30,12,'#e6f2fb',None,0)]+lolli(0,-20,40)+[E(0,52,38,8,'rgba(0,0,0,.2)',None,0)]),upright=True)
def arc_arrow(cx,cy,r,col):
    pts=[(cx+r*math.cos(a),cy+r*math.sin(a)) for a in [i*0.35-0.2 for i in range(14)]]
    out=[L(pts[i][0],pts[i][1],pts[i+1][0],pts[i+1][1],col,5) for i in range(len(pts)-1)]
    e=pts[-1]; out.append(P([(e[0]+9,e[1]-3),(e[0]-8,e[1]-10),(e[0]-5,e[1]+9)],col,None,0)); return out
pr('sk_spin',sheet(lolli(0,-5,38,12)+arc_arrow(0,-5,54,'#2d6cdf')+[L(-50,50,50,50,'#9aa3b2',4),C(30,-62,6,'#ffd24a',OUT,2),C(-34,-60,6,'#7ad06b',OUT,2)]),upright=True)
pr('sk_pool',sheet(hs(0,50,1.0)+[R(-26,-56,52,14,'#6fc3ff',3,OUT,3),L(-16,-56,-16,-70,GR,3),L(-8,-56,-8,-70,GR,3)]),upright=True)
pr('sk_pool_big',[R(-190,-150,380,300,'#fffdf5',10,OUT,6),*[*hs(0,100,3.0,),R(-80,-195,160,40,'#6fc3ff',10,OUT,5)] ,L(-50,-195,-50,-240,GR,6),L(-20,-195,-20,-240,GR,6),
    E(-10,-172,50,6,'rgba(255,255,255,.7)',None,0)],upright=True)
# ───── лопата ─────
pr('shovel',[R(-5,-92,10,150,'#a9855a',3,OUT,4),R(-18,-104,36,16,'#a9855a',6,OUT,4),P([(-22,58),(22,58),(28,110),(0,128),(-28,110)],'#9aa3b5',OUT,5)],grip=(0,0),upright=True)
# ───── домик (три части) ─────
pr('house_f',[R(-250,-34,500,34,['#b9bdc7','#8f95a3'],4,OUT,5),*[L(-230+i*50,-34,-230+i*50,0,'rgba(0,0,0,.14)',3) for i in range(10)]])
pr('house_w',[R(-210,-236,420,236,'#f3d88e',None,OUT,5),*[L(-210,-236+i*30,210,-236+i*30,'rgba(160,110,40,.18)',3) for i in range(1,8)],
    R(-170,-170,90,86,'#bfe3f7',6,OUT,5),L(-125,-170,-125,-84,OUT,4),L(-170,-127,-80,-127,OUT,4),
    R(70,-170,90,86,'#bfe3f7',6,OUT,5),L(115,-170,115,-84,OUT,4),L(70,-127,160,-127,OUT,4),
    R(-30,-150,68,150,'#8a5f3a',6,OUT,5),C(22,-76,6,'#ffd24a',None,0)])
pr('house_r',[P([(-250,-236),(0,-390),(250,-236)],'#d9533b',OUT,5),R(-250,-246,500,18,'#b3402c',6,OUT,5),R(112,-384,38,70,'#8f4528',None,OUT,5)])
# фундамент разной ширины: a=420, b=640, c=880
def fnd(w,crack=False):
    h=w/2
    sh=[R(-h,-40,w,40,['#b9bdc7','#8f95a3'],4,OUT,5)]+[L(-h+20+i*60,-40,-h+20+i*60,0,'rgba(0,0,0,.14)',3) for i in range(int((w-30)//60)+1)]
    if crack: sh+=[P([(-40,-40),(-24,-24),(-48,-12),(-26,0)],None,OUT,5),P([(120,-40),(104,-26),(130,-14),(112,0)],None,OUT,5),P([(-h+60,-40),(-h+76,-22),(-h+52,-8)],None,OUT,5)]
    return sh
pr('fnd_a',fnd(420)); pr('fnd_b',fnd(640)); pr('fnd_c',fnd(880)); pr('fnd_cx',fnd(880,True))
pr('garage_f',[R(-110,-40,220,40,['#c6ccd8','#a2a9b8'],4,OUT,5)])
pr('garage',[R(-110,-150,220,150,'#c6ccd8',None,OUT,5),R(-80,-110,160,110,'#9aa3b5',4,OUT,4),*[L(-80,-110+i*22,80,-110+i*22,'rgba(0,0,0,.2)',3) for i in range(1,5)],P([(-124,-150),(124,-150),(100,-176),(-100,-176)],'#8f98a8',OUT,5)])
pr('tower_f',[R(-70,-40,140,40,['#b9bdc7','#8f95a3'],4,OUT,5)])
pr('tower',[R(-60,-400,120,400,'#d8b48a',None,OUT,5),*[L(-60,-400+i*50,60,-400+i*50,'rgba(120,80,40,.2)',3) for i in range(1,8)],R(-18,-300,36,52,'#bfe3f7',8,OUT,4),R(-18,-180,36,52,'#bfe3f7',8,OUT,4),P([(-80,-400),(0,-500),(80,-400)],'#d9533b',OUT,5)])
# ───── чупа-чупс ─────
def candy(R_,spin=False):
    wedges=[]
    for i in range(12):
        a0=i*math.pi/6; a1=a0+math.pi/6
        pts=[(0,0)]+[(R_*math.cos(a0+(a1-a0)*k/4),R_*math.sin(a0+(a1-a0)*k/4)) for k in range(5)]
        wedges.append(P(pts,PINK if i%2==0 else '#fff',None,0))
    g={"t":"g","x":0,"y":0,"shapes":wedges}
    if spin: g["anim"]={"k":"spin","s":0.45,"pt":[0,0]}
    s=[C(0,0,R_,'#fff',None,0),g,C(0,0,R_,None,OUT,6)]
    s+=[E(-R_*.38,-R_*.55,R_*.2,R_*.1,'rgba(255,255,255,.55)',None,0)]
    # окна и дверь (не крутятся)
    for sx in (-1,1):
        s+=[C(sx*R_*.38,-R_*.12,R_*.17,'#bfe3f7',OUT,5),L(sx*R_*.38-R_*.17,-R_*.12,sx*R_*.38+R_*.17,-R_*.12,OUT,3),L(sx*R_*.38,-R_*.29,sx*R_*.38,R_*.05,OUT,3)]
    s+=[R(-R_*.17,R_*.3,R_*.34,R_*.5,'#8a5f3a',R_*.1,OUT,5),C(R_*.08,R_*.56,5,'#ffd24a',None,0)]
    return s
pr('lp_ball',candy(250),upright=True)
pr('lp_ball_spin',candy(250,True),upright=True)
def stick(w,bend=0):
    H=400
    n=10; left=[];right=[]
    for i in range(n+1):
        y=-H*i/n; off=bend*(i/n)**2
        left.append((-w/2+off,y)); right.append((w/2+off,y))
    pts=left+right[::-1]
    sh=[P(pts,'#f7f7f7',OUT,5)]
    for i in range(1,n,1):
        y=-H*i/n; off=bend*(i/n)**2
        sh.append(L(-w/2+off,y+14,w/2+off,y-6,'rgba(255,95,162,.55)',max(4,w*.12)))
    return sh
pr('lp_st1',stick(26),upright=True); pr('lp_st2',stick(70),upright=True); pr('lp_st3',stick(120),upright=True)
pr('lp_st_bent',stick(70,bend=150),upright=True)
# гирлянда вокруг шара (центр = центр шара)
cols=['#ff4d4d','#ffd24a','#4dd2ff','#7ad06b','#c06bff']
g=[]
for i in range(18):
    a=i*2*math.pi/18; rr=260
    g.append({"t":"g","x":0,"y":0,"anim":{"k":"blink","s":1.6,"a":0.15,"ph":i*0.9},"shapes":[C(rr*math.cos(a),rr*math.sin(a),11,cols[i%5],OUT,3),C(rr*math.cos(a),rr*math.sin(a),20,cols[i%5],None,0)]})
    g[-1]["shapes"][1]["fill"]='rgba(255,255,255,.0)'
pr('garland',g,upright=True)
pr('garland_g',[R(-70,-28,140,28,'#3d4358',8,OUT,4),*[C(-52+i*26,-30,8,cols[i%5],OUT,3) for i in range(5)]],upright=True)
pr('glow_ball',[C(0,0,340,'rgba(255,230,150,.22)',None,0),C(0,0,285,'rgba(255,230,150,.2)',None,0)],upright=True)
# ───── болото, куски, пыль ─────
pr('bog_chunk',[E(0,-60,120,70,'#6b6a3a',OUT,5),E(-30,-84,50,26,'#8a8a4a',None,0),*[C(x,y,r,'#a9b05a',OUT,3) for x,y,r in ((-50,-70,12),(30,-96,9),(60,-60,14),(0,-40,8))],
    P([(-70,-20),(-62,10),(-54,-14)],'#6b6a3a',OUT,3),P([(20,-10),(30,22),(40,-8)],'#6b6a3a',OUT,3)],upright=True)
pr('bog_pool',[E(0,-8,300,34,'#4e5a2a',OUT,5),E(-40,-14,230,20,'#6b7a38',None,0),*[{"t":"g","x":x,"y":-12,"anim":{"k":"pulse","s":0.9,"a":0.25,"ph":i*1.3,"pt":[0,0]},"shapes":[C(0,0,r,'#9fb04a',OUT,3)]} for i,(x,r) in enumerate(((-150,10),(-40,13),(70,9),(170,12)))],
    *[R(x-3,-70,6,60,'#6d5a2a',2,OUT,3) for x in (-250,-230,230,252)]])
pr('dirt_big',[P([(-160,0),(-120,-70),(-50,-130),(30,-160),(110,-110),(170,-40),(190,0)],'#8a6a47',OUT,5),P([(-70,-5),(-10,-80),(50,-70),(110,-5)],'#9b7a54',None,0)])
# ───── кран ─────
pr('crane_tw',[R(-30,-1500,60,1500,'#e9a822',None,OUT,5),*[L(-30,-i*100,30,-i*100-100,'rgba(30,27,38,.55)',5) for i in range(15)],*[L(30,-i*100,-30,-i*100-100,'rgba(30,27,38,.55)',5) for i in range(15)],
    R(-70,-60,140,60,'#3d4358',6,OUT,5),R(-52,-1550,104,66,'#3a78c4',8,OUT,5),R(-36,-1536,40,34,'#bfe3f7',4,OUT,3)],upright=True)
pr('crane_jib',[R(-760,-30,1020,26,'#e9a822',None,OUT,5),*[P([(-740+i*70,-4),(-705+i*70,-30),(-670+i*70,-4)],None,OUT,3) for i in range(14)],R(180,-30,120,60,'#6f7788',6,OUT,5),L(0,-30,0,-110,OUT,5)],upright=True)
pr('crane_car',[R(-42,-170,84,170,'#3d4358',8,OUT,5),R(-60,-20,120,20,'#6f7788',6,OUT,4)],upright=True)
pr('crane_cab',[R(-4,-500,8,500,'#2a2f3d',None,None,0),P([(-8,-14),(8,-14),(8,0),(-8,0)],'#2a2f3d',None,0),C(0,10,14,None,OUT,8)],upright=True)
# ───── календарь на стене и звуки ─────
pr('cal_w',[R(-80,-120,160,240,'#fffdf5',8,OUT,5),R(-80,-120,160,44,'#d9533b',8,OUT,5),*[R(-64+(i%4)*34,-60+(i//4)*34,26,26,'#fff',3,'#cfcfd8',2) for i in range(12)],
    *[L(-64+(i%4)*34,-60+(i//4)*34,-38+(i%4)*34,-34+(i//4)*34,'#d9333b',4) for i in range(7)],C(-30+34*2,-60+34*1+13,22,None,'#d9333b',5)],upright=True)
SND={'snd_krak':("КРАК!",100,'#ffd24a'),'snd_bum':("БУМ!",110,'#fff'),'snd_shlep':("Шлёп!",80,'#cfe88a'),'snd_trr':("Тр-р-р…",76,'#fff'),'snd_chmok':("Чвяк!",84,'#cfe88a')}
for k,(t_,sz,col) in SND.items(): pr(k,[txt(k,0,0,sz,col,OUT,10)],upright=True)
pr('sun_ray',[C(0,0,110,'rgba(255,244,180,.35)',None,0)],upright=True)
pr('sk_h1',sheet(hs(0,40,1.1,roof=False,walls=False)),upright=True)
pr('sk_h2',sheet(hs(0,40,1.1,roof=False)),upright=True)
json.dump(lib,open(LIB,'w'),ensure_ascii=False,indent=2); print('ok11 props')
