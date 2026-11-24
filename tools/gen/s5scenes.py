import os; REPO=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..'))+'/'
import json
D=REPO+''
def mk(id,dur,start,beats):
    beats=sorted(beats,key=lambda b:b['t'])
    json.dump({"id":id,"duration":dur,"start":start,"defs":{},"beats":beats},open(D+f'scenes/{id}.json','w'),ensure_ascii=False,indent=2)
NARR={"type":"extra","x":540,"face":"left","hidden":True,"shirt":"#24242a","sy":0.8}
def b(t,do,**k): return {"t":t,"do":do,**k}
def say(t,line,d): return b(t,"say",who="narr",line=line,dur=d)
CX=440
# ───── S1: трава, машина, начало покоса ─────
be=[b(0,"spawn",id="seat",prop="car_seat",x=CX,y=1250),b(0,"spawn",id="car",prop="car",x=CX,y=1250,layer="front"),
 b(0,"pose",who="bld",pose="drive",dur=3.2),
 b(0,"camera",x=540,y=1000,zoom=1.0,dur=0.01)]
# передняя трава (закрывает капот и лобовое)
for i,(x,pr) in enumerate([(520,"grass_clump"),(610,"grass_clump"),(700,"grass_clump"),(790,"grass_clump"),(880,"grass_clump"),(970,"grass_clump"),(1060,"grass_clump")]):
    be.append(b(0,"spawn",id=f"gf{i}",prop=pr,x=x,y=1262,layer="front",scale=1.15 if i<3 else 1.0))
for i,x in enumerate([600,760,920,1080]):
    be.append(b(0,"spawn",id=f"gb{i}",prop="grass_mid",x=x,y=1250,layer="back"))
be+=[say(0.2,"n01",3.1),b(0.3,"camera",x=540,y=1050,zoom=1.18,dur=3.0),
 say(3.5,"n02",3.3),
 b(3.6,"pose",who="bld",pose="drive_rev",dur=2.8),b(3.6,"emote",who="bld",emotion="angry",dur=3.0),
 b(3.7,"move",id="car",x=CX+28,dur=0.35),b(3.7,"move",id="seat",x=CX+28,dur=0.35),b(3.7,"walk",who="bld",x=CX-60+28,dur=0.35),
 b(4.1,"move",id="car",x=CX,dur=0.35),b(4.1,"move",id="seat",x=CX,dur=0.35),b(4.1,"walk",who="bld",x=CX-60,dur=0.35),
 b(4.6,"move",id="car",x=CX+24,dur=0.3),b(4.6,"move",id="seat",x=CX+24,dur=0.3),b(4.6,"walk",who="bld",x=CX-60+24,dur=0.3),
 b(4.95,"move",id="car",x=CX,dur=0.3),b(4.95,"move",id="seat",x=CX,dur=0.3),b(4.95,"walk",who="bld",x=CX-60,dur=0.3),
 b(3.7,"fx",kind="dust",x=190,y=1245,dur=2.8),b(3.8,"shake",dur=3,amp=5),b(3.7,"marker",name="мотор, колёса буксуют"),
 b(6.0,"camera",reset=True,dur=0.4),
 b(6.4,"pose",who="bld",pose="sit_slump",dur=1.0),b(6.6,"emote",who="bld",emotion="thinking",dur=1.2) if False else b(6.6,"emote",who="bld",emotion="confused",dur=1.2),
 say(7.0,"n03",3.0),b(7.0,"fx",kind="idea",who="bld",dur=1.2),
 # смена кадра: строитель с газонокосилкой
 b(9.1,"remove",id="car"),b(9.1,"remove",id="seat")]
for i in range(7): be.append(b(9.1,"remove",id=f"gf{i}"))
for i in range(4): be.append(b(9.1,"remove",id=f"gb{i}"))
be+=[b(9.1,"place",who="bld",x=200,face="right"),b(9.1,"spawn",id="mow",prop="mower",x=300,y=1250),b(9.15,"hold",id="mow",who="bld",hand="R"),
 b(9.1,"pose",who="bld",pose="mow",dur=4.6),b(9.1,"emote",who="bld",emotion="neutral",dur=0.1),
 b(9.1,"marker",name="газонокосилка")]
xs=[520,630,740,850,960]
for i,x in enumerate(xs): be.append(b(9.1,"spawn",id=f"c{i}",prop="grass_mid",x=x,y=1250,layer="back",scale=1.0))
for i,x in enumerate([1070,1180]): be.append(b(9.1,"spawn",id=f"c{i+5}",prop="grass_mid",x=x,y=1250,layer="back"))
T0=9.4; V=139
be.append(b(T0,"walk",who="bld",x=700,dur=3.6,ease="linear"))
for i,x in enumerate(xs):
    tt=T0+(x-265-200)/V+0.1
    be+=[b(tt,"remove",id=f"c{i}"),b(tt,"spawn",id=f"s{i}",prop="grass_stub",x=x,y=1250,layer="back"),b(tt,"fx",kind="dust",x=x,y=1230,dur=0.5)]
be+=[b(13.1,"pose",who="bld",pose="idle",dur=1.0)]
mk("story_05_s01",14.3,{"location":"field","view":"main","chars":{"bld":{"x":CX-60,"face":"right"},"narr":NARR}},be)

# ───── S2: путь большой (дрон) ─────
be=[b(0,"place",who="bld",x=640,face="right") if False else b(0,"pose",who="bld",pose="mow",dur=0.8),
 b(0,"spawn",id="mow",prop="mower",x=300,y=1250),b(0.05,"hold",id="mow",who="bld",hand="R")]
for i,x in enumerate([520,630]): be.append(b(0,"spawn",id=f"s{i}",prop="grass_stub",x=x,y=1250,layer="back"))
for i in range(0,26):   # уходящая вдаль трава справа и слева
    xr=980+i*115
    be.append(b(0,"spawn",id=f"r{i}",prop="grass_mid" if i%2 else "grass_clump",x=xr,y=1250,layer="back",scale=1.0))
for i in range(0,18):
    xl=300-i*115
    be.append(b(0,"spawn",id=f"l{i}",prop="grass_mid" if i%2 else "grass_clump",x=xl,y=1250,layer="back",scale=1.0))
be+=[say(0.3,"n04",2.4),
 b(0.4,"pose",who="bld",pose="mow",dur=0.5),
 b(1.4,"camera",x=640,y=1000,zoom=0.5,dur=2.6,ease="easeInOut"),
 b(1.4,"marker",name="дрон взлетает: тихий звук косилки, затихает"),
 # на пике — переход на вид сверху
 b(4.1,"view",id="aerial",transition="fade",dur=0.5,keepCam=True),
 b(4.1,"hide",who="bld"),b(4.1,"remove",id="mow")]
for i in range(26): be.append(b(4.2,"remove",id=f"r{i}"))
for i in range(18): be.append(b(4.2,"remove",id=f"l{i}"))
for i in range(2): be.append(b(4.2,"remove",id=f"s{i}"))
be+=[b(4.1,"camera",x=540,y=1100,zoom=0.6,dur=0.01),
 b(4.3,"camera",x=540,y=-2100,zoom=0.1,dur=4.4,ease="easeInOut"),
 say(5.3,"n05",2.9),
 b(9.2,"view",id="main",transition="cut"),b(9.2,"camera",x=540,y=960,zoom=1.0,dur=0.01),b(9.2,"show",who="bld"),
 b(9.2,"spawn",id="mow2",prop="mower",x=300,y=1250),b(9.25,"hold",id="mow2",who="bld",hand="R"),
 b(9.2,"pose",who="bld",pose="mow",dur=0.4),b(9.6,"pose",who="bld",pose="tired",dur=2.0),b(9.6,"emote",who="bld",emotion="sad",dur=2.2),
 b(9.8,"fx",kind="sweat",who="bld",dur=1.2),b(9.8,"marker",name="тихий звук косилки затихает")]
mk("story_05_s02",12.2,{"location":"field","view":"main","chars":{"bld":{"x":640,"face":"right"},"narr":NARR}},be)

# ───── S3: календарь, дорога, трава снова выросла ─────
be=[say(0.2,"n06",2.4)]
for i in range(5):
    t=0.35+i*0.45
    be+=[b(t,"spawn",id=f"pg{i}",prop="cal_page",x=540,y=400,layer="back"),b(t+0.0,"move",id=f"pg{i}",y=380,rot=-172,dur=0.4,ease="easeIn" if False else "easeInOut"),b(t+0.45,"remove",id=f"pg{i}")]
be+=[b(0.3,"marker",name="шелест страниц")]
# вид сбоку: едем по полоске
be+=[b(2.9,"view",id="main",transition="cut"),
 b(2.9,"place",who="bld",x=CX-60,face="right"),b(2.9,"show",who="bld"),
 b(2.9,"spawn",id="seat",prop="car_seat",x=CX,y=1250),b(2.9,"spawn",id="car",prop="car",x=CX,y=1250,layer="front"),
 b(2.9,"pose",who="bld",pose="drive",dur=2.6),b(2.9,"emote",who="bld",emotion="happy",dur=2.4)]
# бегущие мимо кустики срезанной травы (ощущение движения) и растущая трава по краям
for i in range(7):
    x0=1150+i*240
    be+=[b(2.9,"spawn",id=f"st{i}",prop="grass_stub",x=x0,y=1262+((i%3)*70),layer="front" if i%2 else "back"),b(2.9,"move",id=f"st{i}",x=x0-2300,dur=3.2,ease="linear")]
# трава по краям: фронт (низ кадра) и фон растут
for i,x in enumerate([60,260,470,680,890,1060]):
    be+=[b(5.0,"spawn",id=f"gr{i}",prop="grass_clump",x=x,y=1900,layer="front",scale=0.15),b(5.2,"move",id=f"gr{i}",scale=1.5,y=1900,dur=3.4,ease="easeIn")]
for i,x in enumerate([90,300,520,740,980]):
    be+=[b(5.0,"spawn",id=f"gg{i}",prop="grass_clump",x=x,y=1250,layer="back",scale=0.2),b(5.2,"move",id=f"gg{i}",scale=1.1,dur=3.0,ease="easeIn")]
be+=[say(5.2,"n07",3.2),b(5.2,"camera",x=540,y=1050,zoom=1.15,dur=2.5),
 b(5.2,"fx",kind="dust",x=190,y=1245,dur=1.5),b(5.4,"pose",who="bld",pose="drive_rev",dur=2.6),
 b(7.4,"emote",who="bld",emotion="angry",dur=2.5),b(7.6,"shake",dur=1.8,amp=5),b(7.6,"fx",kind="dust",x=190,y=1245,dur=2.0),
 b(8.0,"marker",name="машина застревает"),
 b(9.0,"pose",who="bld",pose="sit_slump",dur=2.5),b(9.1,"emote",who="bld",emotion="tired",dur=2.4),
 say(9.6,"n08",2.2)]
mk("story_05_s03",12.4,{"location":"field","view":"calendar","chars":{"bld":{"x":CX-60,"face":"right","hidden":True},"narr":NARR}},be)
print('ok')
