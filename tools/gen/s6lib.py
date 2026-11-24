import json,random,sys
exec(open('s5lib2.py').read().split("# ───── бульдозер")[0])
# ───── комната
wall=[R(-100,0,1280,1250,['#e3e8ee','#d3dae2'],None,None,0),R(-100,1170,1280,80,'#c3cbd5',None,None,0),R(-100,1226,1280,26,'#f4f6f9',None,None,0),R(-100,1222,1280,5,'#aab2bf',None,None,0),
 # окно
 R(110,690,330,400,'#fff',10),R(130,710,290,360,['#9ad0f5','#d9efff'],6,None,0),R(274,710,12,360,'#fff',None,None,0),R(130,880,290,12,'#fff',None,None,0),R(100,1090,350,24,'#f4f6f9',8),
 # дверной проём
 R(738,660,264,592,'#6b5a48',6),R(752,674,236,578,'#2a2f3d',None,None,0)]
floor=[R(-100,1250,1280,670,['#d2ad74','#b89358'],None,None,0)]
for y in range(1300,1920,70): floor.append(L(-100,y,1180,y,'#a9854e',3))
rr=random.Random(2)
for y in range(1250,1920,70):
    for x in range(rr.randint(0,250)-100,1180,300): floor.append(L(x,y,x,y+70,'#a9854e',3))
lib['locations']['room']={"groundY":1250,"views":{},"layers":[{"p":1,"shapes":wall},{"p":1,"shapes":floor}]}
# ───── предметы
def door(h,top=-575):
    return [R(-114,top,228,-top-h+0 if False else (-top)-(-h) if False else -top+h,'#c18652',8) if False else R(-114,top,228,(-top)-h,'#c18652',8),
            R(-88,top+30,176,170,None,6,'#a56a38',5),R(-88,top+240,176,230 if h==0 else 150,None,6,'#a56a38',5),C(-84,-300,15,'#e6e9ee')]
pr('door_closed',door(0)); pr('door_cut',door(90))
pr('door_open',[R(-114,-575,228,575,'#1e1b26',None,None,0),P([(-114,0),(-34,-38),(-34,-540),(-114,-575)],'#c18652'),L(-70,-480,-70,-120,'#a56a38',5),C(-52,-300,10,'#e6e9ee')])
pr('socket',[R(-28,-44,56,44,'#fff',8),C(-10,-22,5,'#2a2f3d',None,0),C(10,-22,5,'#2a2f3d',None,0)])
pr('mark_x',[L(-30,-30,30,30,'#e5342b',9),L(30,-30,-30,30,'#e5342b',9)])
pr('slab',[R(-100,-38,200,38,['#c9ccd3','#a9adb6'],4),R(-100,-38,200,7,'#e8eaee',None,None,0)]+[C(rr.randint(-90,90),-rr.randint(8,30),3,'#8d919b',None,0) for _ in range(6)])
pr('ball',[C(0,-28,28,'#e5342b'),L(-28,-28,28,-28,'#fff',8),C(-9,-38,6,'rgba(255,255,255,.6)',None,0)])
def level(ok):
    bx=0 if ok else -34
    return [R(-170,-22,340,44,'#f4c52a',8),R(-36,-14,72,28,'#f3f7c8' if not ok else '#c9f2c0',10),E(bx,0,15,9,'#5ec45e' if ok else '#7fb2e6',OUT,3),L(-12,-14,-12,14,OUT,3),L(12,-14,12,14,OUT,3),C(-120,0,7,'#d9a416'),C(120,0,7,'#d9a416')]
pr('level_tilt',level(False),upright=True); pr('level_ok',level(True),upright=True)
pr('bucket',[P([(-50,-90),(50,-90),(40,0),(-40,0)],'#9aa3b5'),E(0,-90,50,12,'#6b7384'),P([(-46,-90),(46,-90),(30,-130),(-30,-130)],'#b8bcc4',None,0),R(-4,-60,8,40,'#7d8699',None,None,0)])
pr('rake',[R(-70,-10,140,16,'#9aa3b5',5),L(0,-10,-74,-190,'#8a6a47',9)],grip=(-74,-190),upright=True)
pr('saw',[{"t":"g","x":0,"y":0,"anim":{"k":"slide","s":5,"a":22},"shapes":[P([(-80,-8),(70,-14),(70,14),(-80,10)],'#c7ced8'),R(70,-22,50,40,'#8a6a47',8)]}],grip=(95,0),upright=True)
pr('ceiling',[R(-700,-1700,1400,1700,'#efeadf',None,None,0),R(-700,-26,1400,26,'#cfc8b6',None,None,0),R(-700,-30,1400,5,'#a8a18f',None,None,0)])
json.dump(lib,open(LIB,'w'),ensure_ascii=False,indent=2); print('ok6')
