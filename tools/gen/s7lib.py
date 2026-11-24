import json,random,sys
exec(open('s5lib2.py').read().split("# ───── бульдозер")[0])
# ───── двор (story 7)
random.seed(3)
sky=[R(-100,-200,1280,1500,['#7cc4f2','#c9e9fa','#f6fbff'],None,None,0),
 E(250,260,230,60,'#fff',None),E(520,230,170,50,'#fff',None),E(880,380,260,62,'#fff',None),E(1100,200,200,50,'#fff',None),
 # далёкая линия кустов/домов
 E(150,1235,420,90,'#a9cfa0',None),E(620,1240,520,110,'#9bc794',None),E(1050,1235,420,95,'#a9cfa0',None),
 R(60,1020,200,230,'#eadfc9',None,None,0),P([(40,1020),(160,930),(280,1020)],'#c9735b',None,0),R(130,1100,60,70,'#9ad0f5',None,None,0),
 R(-100,1250,1280,670,['#cbb58a','#b59c6d'],None,None,0),R(-100,1250,1280,14,'#7fae5c',None,None,0)]
for i in range(40):
    x=random.randint(-80,1160);y=random.randint(1290,1900);w=random.randint(18,44)
    sky.append(E(x,y,w,5,'#a89264',None))
lib['locations']['yard']={"groundY":1250,"views":{},"layers":[{"p":1,"shapes":sky}]}
# ───── забор
PW=62; PH=340
def picket(fill,hl,peel=False,raw=False):
    x0=-PW/2+2
    sh=[R(x0,-PH,PW-4,PH,fill,None,OUT,4),P([(x0,-PH),(0,-PH-26),(x0+PW-4,-PH)],fill,OUT,4),
        R(-PW/2-1,-250,PW+2,26,hl,None,None,0),R(-PW/2-1,-110,PW+2,26,hl,None,None,0),
        L(-PW/2+9,-PH+10,-PW/2+9,-6,'rgba(255,255,255,.22)',6)]
    if raw:
        sh+= [L(-14,-300,-8,-180,'#8f7f66',3),L(10,-120,6,-40,'#8f7f66',3),C(0,-200,4,'#8f7f66',None,0)]
    if peel:
        for (x,y,w,h) in [(-24,-320,26,40),(2,-250,20,58),(-20,-180,34,44),(-6,-100,24,50),(-22,-40,30,34)]:
            sh.append(P([(x,y),(x+w,y+4),(x+w-4,y+h),(x+2,y+h-6)],'#c9b88f','#6d8f4b',2))
    return sh
pr('pk_raw',picket('#c4b392','#a79574',raw=True),upright=True)
pr('pk_g1',picket('#3b9a5c','#2f8049'),upright=True)
pr('pk_g2',picket('#63c07f','#4aa466'),upright=True)
pr('pk_g1p',picket('#3b9a5c','#2f8049',peel=True),upright=True)
# банки краски
def can(col,empty=False):
    sh=[R(-55,-90,110,90,'#b9bfca',10),R(-55,-62,110,34,col,None,OUT,4),E(0,-90,55,12,'#8c93a1',OUT,4),
        L(-52,-90,-40,-150,OUT,4),L(52,-90,40,-150,OUT,4),L(-40,-150,40,-150,OUT,4)]
    sh.append(E(0,-90,42,8,'#2a2f3d' if empty else col,None,0))
    return sh
pr('can_g1',can('#3b9a5c'),grip=(0,-150),upright=True)
pr('can_g2',can('#63c07f'),grip=(0,-150),upright=True)
pr('can_e',can('#3b9a5c',True),grip=(0,-150),upright=True)
# кисть (хват на рукояти, щетина вперёд-вниз)
def brush(col):
    return [R(-8,-10,16,100,'#8a6a47',6),R(-16,88,32,30,'#c7ced8',4),R(-18,114,36,36,col,6)]
pr('brush_g1',brush('#3b9a5c'),grip=(0,0),upright=True)
pr('brush_g2',brush('#63c07f'),grip=(0,0),upright=True)
pr('brush_dry',brush('#b7a784'),grip=(0,0),upright=True)
pr('flake',[P([(-9,-4),(9,-8),(7,6),(-6,7)],'#3b9a5c','#2f8049',2)])
# пятно-силуэт жилетки на заборе (тёмно-зелёное), origin: низ по центру
pr('vest_stain',[R(-66,-215,132,215,'#1f6b3c',22,None,0),P([(-30,-215),(30,-215),(0,-165)],'#63c07f',None,0),R(-62,-132,124,14,'#175a31',None,None,0),R(-62,-80,124,14,'#175a31',None,None,0),
  E(-38,-205,26,12,'#1f6b3c',None,0),E(38,-205,26,12,'#1f6b3c',None,0)])
json.dump(lib,open(LIB,'w'),ensure_ascii=False,indent=2); print('ok7')
