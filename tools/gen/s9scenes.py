import json
exec(open('s5scenes.py').read().split("CX=440")[0])
LANGF='lang/story_09.ru.json'
HERO={"type":"eng","x":-300,"face":"right","sy":0.82}
def START(hx=None,face="right"):
    return {"location":"cottage","chars":{"narr":NARR,"eng":dict(HERO)}}
LEAVES=lambda: b(0,"spawn",id="lv",prop="leaves",x=0,y=0,layer="front")
TH=lambda key,x=180,y=810: [b(0,"spawn",id="th",prop="th_"+key,x=x,y=y,layer="back")]
def setth(t,key,x=180,y=810):
    return [b(t,"remove",id="th"),b(t+0.01,"spawn",id="th",prop="th_"+key,x=x,y=y,layer="back")]
# ═════ S1 ═════
be=[LEAVES(),b(0,"camera",x=600,y=1000,zoom=0.72,dur=0.01),
 b(0,"outfit",who="eng",shirt="#b5654a",sleeve="#b5654a"),
 b(0,"spawn",id="stv",prop="stove",x=330,y=1100,layer="back")]+TH("t16")
be+=[b(0,"spawn",id="tb",prop="k_table",x=420,y=1250,layer="back"),b(0,"spawn",id="ch",prop="k_chair",x=300,y=1250,layer="back"),
 b(0,"place",who="eng",x=350,y=0,face="right"),b(0,"pose",who="eng",pose="sit",dur=0.1),
 b(3.0,"camera",x=420,y=1020,zoom=1.15,dur=2.0,ease="easeInOut"),
 b(5.0,"pose",who="eng",pose="sit_rub",dur=1.8),b(5.0,"emote",who="eng",emotion="tired",dur=2.0),
 b(5.2,"fx",kind="sweat",who="eng",dur=1.0),
 b(7.0,"camera",x=520,y=1030,zoom=1.5,dur=1.0,ease="easeInOut"),b(7.0,"emote",who="eng",emotion="worried",dur=1.2),
 b(8.2,"spawn",id="pl",prop="plaid",x=350,y=1040,layer="front"),b(8.2,"pose",who="eng",pose="sit_cozy",dur=3),
 b(8.4,"camera",x=420,y=1020,zoom=1.15,dur=1.5,ease="easeInOut"),
 say(0.5,"n01",2.0),say(3.2,"n02",2.6),say(6.4,"n03",3.6),b(0.3,"marker",name="шум ветра, шорох листьев")]
mk("story_09_s01",12.0,START(),be)
# ═════ S2 ═════
be=[LEAVES(),b(0,"camera",x=420,y=940,zoom=1.1,dur=0.01),b(0,"outfit",who="eng",shirt="#b5654a",sleeve="#b5654a"),
 b(0,"spawn",id="stv",prop="stove",x=330,y=1100,layer="back")]+TH("t16")
be+=[b(0,"place",who="eng",x=330,y=0,face="right"),b(0,"pose",who="eng",pose="idle",dur=0.3),
 b(0.5,"spawn",id="p1",prop="pot_steam",x=300,y=980,layer="back"),
 b(1.5,"pose",who="eng",pose="write",dur=2.0),
 b(3.5,"emote",who="eng",emotion="surprised",dur=1.5),b(3.6,"fx",kind="exclaim",who="eng",dur=0.8),
 b(3.5,"remove",id="th"),b(3.5,"spawn",id="th",prop="th_t17",x=180,y=810,layer="back"),
 b(5.2,"walk",who="eng",x=500,y=0,dur=1.2,face="right"),b(5.2,"camera",x=620,y=1000,zoom=0.95,dur=1.5,ease="easeInOut"),
 b(6.9,"pose",who="eng",pose="think",dur=2.0),b(6.9,"emote",who="eng",emotion="confused",dur=1.5),
 b(7.5,"spawn",id="ct",prop="cold_tint",x=0,y=0,layer="front"),b(7.5,"camera",x=800,y=1000,zoom=0.95,dur=1.8,ease="easeInOut"),
 b(9.6,"emote",who="eng",emotion="happy",dur=2.0),b(9.7,"fx",kind="idea",who="eng",dur=1.4),b(9.6,"remove",id="ct"),
 say(0.8,"n04",1.8),say(3.2,"n05",3.6),say(8.4,"n06",2.4)]
mk("story_09_s02",12.0,START(),be)
# ═════ S3 ═════
be=[LEAVES(),b(0,"camera",x=420,y=940,zoom=1.1,dur=0.01),b(0,"outfit",who="eng",shirt="#b5654a",sleeve="#b5654a"),
 b(0,"spawn",id="stv",prop="stove",x=330,y=1100,layer="back")]+TH("t17")
be+=[b(0,"place",who="eng",x=480,y=0,face="left"),b(0,"pose",who="eng",pose="idle",dur=0.3),
 b(0.3,"spawn",id="p1",prop="pot_steam",x=245,y=978,layer="back"),
 b(1.8,"spawn",id="p2",prop="pot_steam",x=302,y=978,layer="back",scale=0.01),b(1.82,"move",id="p2",scale=1,dur=0.4),
 b(3.4,"spawn",id="p3",prop="pot_big",x=358,y=978,layer="back",scale=0.01),b(3.42,"move",id="p3",scale=1,dur=0.4),
 b(3.9,"spawn",id="p4",prop="pot_steam",x=415,y=978,layer="back",scale=0.01),b(3.92,"move",id="p4",scale=1,dur=0.4),
 b(2.0,"emote",who="eng",emotion="happy",dur=6),b(4.0,"pose",who="eng",pose="hips",dur=3),
 b(6.2,"walk",who="eng",x=560,y=0,dur=1.8,face="right"),b(8.0,"walk",who="eng",x=420,y=0,dur=1.8,face="left"),
 b(5.0,"camera",x=520,y=1010,zoom=1.0,dur=1.5,ease="easeInOut")]
be+=setth(3.0,"t18")+setth(5.5,"t19")+setth(8.0,"t20")
be+=[say(0.4,"n07",3.5),say(4.2,"n08",1.2),say(5.6,"n09",1.6),say(7.5,"n10",3.2)]
mk("story_09_s03",11.5,START(),be)
print('ok')
# ═════ S4 ═════
def kit(extra_pots=4,th="t20"):
    be=[LEAVES(),b(0,"outfit",who="eng",shirt="#b5654a",sleeve="#b5654a"),b(0,"spawn",id="stv",prop="stove",x=330,y=1100,layer="back")]+TH(th)
    for i,x in enumerate((245,302,358,415)):
        if i<extra_pots: be.append(b(0,"spawn",id=f"p{i+1}",prop="pot_big" if i==2 else "pot_steam",x=x,y=978,layer="back"))
    return be
be=kit()+[b(0,"camera",x=420,y=1000,zoom=1.15,dur=0.01),b(0,"place",who="eng",x=480,y=0,face="left"),b(0,"pose",who="eng",pose="idle",dur=0.3),
 b(0.3,"spawn",id="bl1",prop="bill_v1",x=470,y=1380,layer="front",scale=0.95)]
for i,(k,t0) in enumerate((("v2",2.4),("v3",3.6),("v4",4.8))):
    be+=[b(t0,"remove",id=f"bl{i+1}"),b(t0+0.01,"spawn",id=f"bl{i+2}",prop="bill_"+k,x=470,y=1380,layer="front",scale=0.95),b(t0,"shake",dur=0.4,amp=4)]
be+=[b(6.2,"move",id="bl4",scale=0.01,dur=0.6,ease="easeInOut"),b(6.8,"remove",id="bl4"),
 b(6.8,"pose",who="eng",pose="hands_up",dur=1.0),b(6.8,"emote",who="eng",emotion="shocked",dur=1.8),b(6.9,"fx",kind="exclaim",who="eng",dur=0.8),
 b(8.2,"pose",who="eng",pose="tired",dur=3),b(8.2,"emote",who="eng",emotion="sad",dur=3),
 b(8.4,"move",id="p4",y=1010,dur=2.8,ease="easeInOut"),
 say(0.3,"n11",3.3),say(3.8,"n12",4.3),say(8.3,"n13",3.0)]
mk("story_09_s04",11.8,{"location":"cottage","chars":{"narr":NARR,"eng":dict(HERO)}},be)
# ═════ S5 ═════
be=[LEAVES(),b(0,"outfit",who="eng",shirt="#b5654a",sleeve="#b5654a"),b(0,"spawn",id="stv",prop="stove",x=330,y=1100,layer="back")]+TH("t17")
be+=[b(0,"camera",x=700,y=980,zoom=1.0,dur=0.01),b(0,"place",who="eng",x=660,y=0,face="right"),b(0,"pose",who="eng",pose="think",dur=2.5),b(0,"emote",who="eng",emotion="neutral",dur=1),
 b(1.5,"spawn",id="tf",prop="think_fire",x=770,y=890,layer="front",scale=0.01),b(1.52,"move",id="tf",scale=1,dur=0.6,ease="easeInOut"),
 b(3.5,"emote",who="eng",emotion="happy",dur=1.5),b(3.5,"pose",who="eng",pose="hands_warm",dur=1.6),
 b(5.4,"move",id="tf",scale=1.35,dur=0.25),b(5.65,"remove",id="tf"),b(5.65,"fx",kind="dust",x=770,y=780,dur=0.5),
 b(5.7,"emote",who="eng",emotion="surprised",dur=0.6),
 b(6.4,"pose",who="eng",pose="dizzy",dur=1.4),b(6.4,"emote",who="eng",emotion="frown",dur=2),
 b(8.0,"pose",who="eng",pose="arms_cross",dur=2.5),
 say(0.3,"n14",3.8),say(4.4,"n15",1.0),say(6.6,"n16",2.6)]
mk("story_09_s05",11.0,START(),be)
# ═════ S6 ═════
be=[LEAVES(),b(0,"outfit",who="eng",shirt="#b5654a",sleeve="#b5654a"),b(0,"spawn",id="stv",prop="stove",x=330,y=1100,layer="back")]+TH("t17")
be+=[b(0,"camera",x=420,y=980,zoom=0.95,dur=0.01),b(0,"spawn",id="bp",prop="brick_pile",x=700,y=1250,layer="back"),
 b(0,"place",who="eng",x=700,y=0,face="right"),b(0,"pose",who="eng",pose="idle",dur=0.3)]
t=0.6
for i in range(2):
    be+=[b(t,"spawn",id=f"bk{i}",prop="brick",x=700,y=1250),b(t,"hold",id=f"bk{i}",who="eng",hand="R"),b(t,"pose",who="eng",pose="idle",dur=0.1),
         b(t,"walk",who="eng",x=560,y=0,dur=1.0,face="left")]
    t+=1.0
    be+=[b(t,"release",id=f"bk{i}"),b(t,"remove",id=f"bk{i}"),b(t,"walk",who="eng",x=700,y=0,dur=0.9,face="right")]
    if i==0: be+=[b(t,"spawn",id="bs",prop="brick_stove",x=520,y=1250,layer="back",scale=0.01),b(t+0.02,"move",id="bs",scale=0.55,dur=0.5)]
    else: be+=[b(t+0.02,"move",id="bs",scale=1,dur=0.6)]
    t+=0.9
be+=[b(t,"walk",who="eng",x=420,y=0,dur=1.0,face="right"),
 b(t+0.5,"spawn",id="ch",prop="chimney",x=520,y=1250-182,layer="back",scale=0.01),b(t+0.52,"move",id="ch",scale=1,dur=1.8,ease="easeInOut"),
 b(t+0.5,"camera",x=520,y=700,zoom=0.7,dur=1.6,ease="easeInOut")]
t+=2.6
be+=[b(t,"camera",x=470,y=1000,zoom=1.15,dur=1.2,ease="easeInOut"),b(t,"spawn",id="lg",prop="stove_logs",x=520,y=1250-35,layer="back"),
 b(t+0.6,"spawn",id="fr",prop="stove_fire",x=520,y=1250-35,layer="back",scale=0.01),b(t+0.62,"move",id="fr",scale=1,dur=0.6),
 b(t+0.6,"spawn",id="sm",prop="smoke",x=520,y=-300,layer="back"),
 b(t+1.2,"emote",who="eng",emotion="happy",dur=5),b(t+1.2,"pose",who="eng",pose="hands_warm",dur=5),
 b(t+1.2,"spawn",id="stove_chair",prop="k_chair",x=330,y=1250,layer="back")]
print(t)
be+=[say(0.5,"n17",2.8),say(t-0.5,"n18",4.2)]
mk("story_09_s06",t+6.5,START(),be)
# ═════ захват 3: сцены 7–9 ═════
SW=dict(shirt="#b5654a",sleeve="#b5654a")
def STV(th="t22",fire=True,tint=False):
    be=[LEAVES(),b(0,"outfit",who="eng",**SW),b(0,"spawn",id="stv",prop="stove",x=330,y=1100,layer="back"),
        b(0,"spawn",id="bs",prop="brick_stove",x=520,y=1250,layer="back"),b(0,"spawn",id="ch",prop="chimney",x=520,y=1068,layer="back"),
        b(0,"spawn",id="lg",prop="stove_logs",x=520,y=1215,layer="back"),b(0,"spawn",id="sm",prop="smoke",x=520,y=-300,layer="back")]
    if fire: be.append(b(0,"spawn",id="fr",prop="stove_fire",x=520,y=1215,layer="back"))
    be+=TH(th)
    return be
def PIPES(t0,step=0.15):
    """труба по полу от печи (x=560) через проём до x=1130, y=1250"""
    be=[];t=t0;x=575;k=0
    while x<1130:
        be.append(b(t,"spawn",id=f"pp{k}",prop="pipe_h",x=x,y=1250,layer="back")); x+=54;t+=step;k+=1
    return be,t
# ═════ S7 ═════
be=STV()+[b(0,"camera",x=560,y=1000,zoom=0.95,dur=0.01),b(0,"spawn",id="cl",prop="cold_living",x=0,y=0,layer="back"),
 b(0,"spawn",id="thL",prop="th_t12",x=715,y=840,layer="back"),
 b(0,"place",who="eng",x=440,y=0,face="right"),b(0,"pose",who="eng",pose="hands_warm",dur=1.6),b(0,"emote",who="eng",emotion="happy",dur=1.6),
 b(1.6,"walk",who="eng",x=760,y=0,dur=2.2,face="right"),b(1.6,"camera",x=700,y=1000,zoom=0.95,dur=2.2,ease="easeInOut"),
 b(3.9,"pose",who="eng",pose="tired",dur=1.8),b(3.9,"emote",who="eng",emotion="worried",dur=2),
 b(5.9,"walk",who="eng",x=500,y=0,dur=2.0,face="left"),b(5.9,"camera",x=560,y=1000,zoom=0.95,dur=2.0,ease="easeInOut"),
 b(8.0,"pose",who="eng",pose="think",dur=1.5),b(8.0,"emote",who="eng",emotion="confused",dur=1.5),
 b(9.6,"walk",who="eng",x=500,y=0,dur=0.4,face="right"),b(9.6,"camera",x=900,y=1000,zoom=0.95,dur=2.0,ease="easeInOut"),b(9.6,"pose",who="eng",pose="point",dur=2.0),
 say(0.3,"n19",3.0),say(3.7,"n20",3.5),say(8.0,"n21",3.0)]
mk("story_09_s07",12.0,START(),be)
# ═════ S8 ═════
be=STV()+[b(0,"camera",x=620,y=1000,zoom=0.95,dur=0.01),b(0,"spawn",id="cl",prop="cold_living",x=0,y=0,layer="back"),
 b(0,"spawn",id="thL",prop="th_t12",x=715,y=840,layer="back"),
 b(0,"place",who="eng",x=480,y=0,face="right"),b(0,"pose",who="eng",pose="idle",dur=0.3)]
pb,tp=PIPES(1.0); be+=pb
be+=[b(1.0,"walk",who="eng",x=620,y=0,dur=1.5,face="right"),b(1.0,"pose",who="eng",pose="rake",dur=2.0),
 b(tp+0.2,"spawn",id="r1",prop="rad",x=900,y=1250,layer="front",scale=0.01),b(tp+0.22,"move",id="r1",scale=1,dur=0.5,ease="easeInOut"),
 b(tp+1.4,"spawn",id="r2",prop="rad",x=1040,y=1250,layer="front",scale=0.01),b(tp+1.42,"move",id="r2",scale=1,dur=0.5,ease="easeInOut"),
 b(tp+0.3,"walk",who="eng",x=780,y=0,dur=1.2,face="right"),b(tp+0.3,"pose",who="eng",pose="present",dur=2.5),
 b(tp+2.8,"spawn",id="hw1",prop="heat_waves",x=900,y=1130,layer="front"),b(tp+3.0,"spawn",id="hw2",prop="heat_waves",x=1040,y=1130,layer="front"),
 b(tp+3.0,"remove",id="cl"),b(tp+3.0,"remove",id="thL"),b(tp+3.01,"spawn",id="thL2",prop="th_t17",x=715,y=840,layer="back"),
 b(tp+4.6,"remove",id="thL2"),b(tp+4.61,"spawn",id="thL3",prop="th_t22",x=715,y=840,layer="back"),
 b(tp+3.2,"pose",who="eng",pose="hands_warm",dur=3),b(tp+3.2,"emote",who="eng",emotion="happy",dur=4),b(tp+3.2,"camera",x=800,y=1000,zoom=0.95,dur=1.5,ease="easeInOut"),
 say(0.4,"n22",2.0),say(tp+0.1,"n23",2.9),say(tp+3.3,"n24",3.4)]
print(tp)
mk("story_09_s08",tp+7.5,START(),be)
# ═════ S9 ═════
be=STV()+[b(0,"camera",x=780,y=1000,zoom=0.95,dur=0.01),b(0,"spawn",id="thL",prop="th_t22",x=715,y=840,layer="back")]
for k in range(13): be.append(b(0,"spawn",id=f"pp{k}",prop="pipe_h",x=575+54*k,y=1250,layer="back"))
be+=[b(0,"spawn",id="r1",prop="rad",x=900,y=1250,layer="front"),b(0,"spawn",id="r2",prop="rad",x=1040,y=1250,layer="front"),
 b(0,"spawn",id="hw1",prop="heat_waves",x=900,y=1130,layer="front"),b(0,"spawn",id="hw2",prop="heat_waves",x=1040,y=1130,layer="front"),
 b(0,"place",who="eng",x=640,y=0,face="right"),b(0,"pose",who="eng",pose="idle",dur=0.3),b(0,"emote",who="eng",emotion="happy",dur=1.5),
 b(1.0,"walk",who="eng",x=760,y=0,dur=1.2,face="right"),
 b(2.4,"pose",who="eng",pose="hands_up",dur=1.0),b(2.4,"emote",who="eng",emotion="happy",dur=1.2),
 b(3.0,"outfit",who="eng",shirt="#7fb2e6",sleeve="#f4cfae"),b(3.0,"spawn",id="swp",prop="sweater_pr",x=655,y=1125,layer="front"),
 b(3.6,"walk",who="eng",x=730,y=0,dur=0.6,face="left"),
 b(4.4,"pose",who="eng",pose="sit",dur=1.2),b(4.4,"emote",who="eng",emotion="happy",dur=2),
 b(6.6,"spawn",id="cw",prop="cold_waves",x=1020,y=900,scale=1.3,layer="front"),b(6.6,"camera",x=900,y=900,zoom=0.9,dur=1.8,ease="easeInOut"),
 b(6.7,"pose",who="eng",pose="sit_up",dur=2.5),b(6.7,"emote",who="eng",emotion="surprised",dur=2.5),b(6.9,"fx",kind="exclaim",who="eng",dur=0.8),
 say(0.5,"n25",2.2),say(6.2,"n26",4.0)]
mk("story_09_s09",12.0,START(),be)
# ═════ захват 4: сцены 10–12 ═════
def SYS(floor1=True,floor2=True,base=True,waves=True):
    be=[]
    if floor1:
        for k in range(11): be.append(b(0,"spawn",id=f"f1p{k}",prop="pipe_h",x=575+54*k,y=1250,layer="back"))
        for i,x in enumerate((900,1040)): be.append(b(0,"spawn",id=f"f1r{i}",prop="rad",x=x,y=1250,layer="front"))
        if waves: be+=[b(0,"spawn",id="f1w0",prop="heat_waves",x=900,y=1130,layer="front"),b(0,"spawn",id="f1w1",prop="heat_waves",x=1040,y=1130,layer="front")]
    if floor2:
        for k in range(10): be.append(b(0,"spawn",id=f"vp{k}",prop="pipe_v",x=1145,y=1250-54*k,layer="back"))
        for k in range(19): be.append(b(0,"spawn",id=f"f2p{k}",prop="pipe_h",x=1120-54*k,y=690,layer="back"))
        for i,(x,sc) in enumerate(((560,1),(700,1),(200,0.8))):
            be.append(b(0,"spawn",id=f"f2r{i}",prop="rad",x=x,y=690,layer="front",scale=sc))
            if waves: be.append(b(0,"spawn",id=f"f2w{i}",prop="heat_waves",x=x,y=575,layer="front",scale=sc))
    if base:
        for k in range(10): be.append(b(0,"spawn",id=f"bp{k}",prop="pipe_v",x=580,y=1304+54*k,layer="back"))
        for k in range(10): be.append(b(0,"spawn",id=f"bh{k}",prop="pipe_h",x=290+54*k,y=1790,layer="back"))
        be+=[b(0,"spawn",id="boil",prop="boiler",x=180,y=1810,layer="front"),b(0,"spawn",id="tank",prop="tank",x=400,y=1810,layer="front"),
             b(0,"spawn",id="pm1",prop="pump",x=500,y=1790,layer="front"),b(0,"spawn",id="pm2",prop="pump",x=720,y=1790,layer="front")]
    return be
# ═════ S10 ═════
be=STV()+[b(0,"camera",x=900,y=1000,zoom=0.95,dur=0.01),b(0,"spawn",id="r1",prop="rad",x=900,y=1250,layer="front"),b(0,"spawn",id="r2",prop="rad",x=1040,y=1250,layer="front")]
for k in range(11): be.append(b(0,"spawn",id=f"f1p{k}",prop="pipe_h",x=575+54*k,y=1250,layer="back"))
be+=[b(0,"place",who="eng",x=1120,y=-45,face="left"),b(0,"pose",who="eng",pose="idle",dur=0.3),b(0,"outfit",who="eng",shirt="#7fb2e6",sleeve="#f4cfae"),
 b(0.4,"walk",who="eng",x=790,y=-545,dur=3.4,ease="linear",face="left"),b(3.8,"walk",who="eng",x=770,y=-560,dur=0.3,ease="linear"),
 b(0.4,"camera",x=900,y=800,zoom=0.95,dur=3.4,ease="easeInOut")]
for k in range(10): be.append(b(0.8+0.12*k,"spawn",id=f"vp{k}",prop="pipe_v",x=1145,y=1250-54*k,layer="back"))
be+=[b(4.2,"walk",who="eng",x=300,y=-560,dur=3.0,ease="linear",face="left"),b(4.2,"pose",who="eng",pose="rake",dur=3.0)]
for k in range(19): be.append(b(4.2+0.15*k,"spawn",id=f"f2p{k}",prop="pipe_h",x=1120-54*k,y=690,layer="back"))
be+=[b(4.2,"camera",x=620,y=700,zoom=0.95,dur=3.0,ease="easeInOut")]
for i,(x,sc,t0) in enumerate(((560,1,7.4),(700,1,8.0),(200,0.8,8.6))):
    be+=[b(t0,"spawn",id=f"f2r{i}",prop="rad",x=x,y=690,layer="front",scale=0.01),b(t0+0.02,"move",id=f"f2r{i}",scale=sc,dur=0.5,ease="easeInOut"),b(t0+0.7,"spawn",id=f"f2w{i}",prop="heat_waves",x=x,y=575,layer="front",scale=sc)]
be+=[b(7.4,"pose",who="eng",pose="present",dur=2.4),b(7.4,"emote",who="eng",emotion="happy",dur=2.4),
 b(10.2,"camera",x=450,y=1450,zoom=0.75,dur=1.3,ease="easeInOut")]
for k in range(10): be.append(b(11.0+0.1*k,"spawn",id=f"bp{k}",prop="pipe_v",x=580,y=1304+54*k,layer="back"))
for k in range(10): be.append(b(12.0+0.1*k,"spawn",id=f"bh{k}",prop="pipe_h",x=290+54*k,y=1790,layer="back"))
for i,(pid,pr_,x,y,t0) in enumerate((("tank","tank",400,1810,11.2),("boil","boiler",180,1810,11.6),("pm1","pump",500,1790,13.0),("pm2","pump",720,1790,13.3))):
    be+=[b(t0,"spawn",id=pid,prop=pr_,x=x,y=y,layer="front",scale=0.01),b(t0+0.02,"move",id=pid,scale=1,dur=0.5,ease="easeInOut")]
be+=[b(14.4,"camera",x=600,y=950,zoom=0.62,dur=2.0,ease="easeInOut"),b(14.4,"pose",who="eng",pose="hips",dur=3),b(14.4,"emote",who="eng",emotion="tired",dur=3),
 say(0.4,"n27",3.0),say(5.6,"n28",5.4),say(12.6,"n29",4.4)]
mk("story_09_s10",17.8,START(),be)
# ═════ S11 ═════
be=STV()+SYS()+[b(0,"spawn",id="snow",prop="snow_out",x=0,y=0,layer="back"),b(0,"spawn",id="sf",prop="snowfall",x=0,y=0,layer="front"),
 b(0,"camera",x=800,y=1000,zoom=0.9,dur=0.01),b(0,"outfit",who="eng",shirt="#7fb2e6",sleeve="#f4cfae"),
 b(0,"place",who="eng",x=730,y=0,face="right"),b(0,"spawn",id="cup",prop="cup",x=730,y=1250),b(0.01,"hold",id="cup",who="eng",hand="R"),
 b(0,"pose",who="eng",pose="sit_lean",dur=14),b(0,"emote",who="eng",emotion="happy",dur=14),
 b(1.5,"camera",x=600,y=950,zoom=0.62,dur=6.0,ease="easeInOut"),
 say(0.3,"n30",3.2),say(3.7,"n31",1.6),say(5.4,"n32",1.8),say(7.3,"n33",2.2),say(9.8,"n34",4.2)]
mk("story_09_s11",14.5,START(),be)
# ═════ S12 ═════
be=STV()+SYS(waves=True)+[b(0,"outfit",who="eng",shirt="#7fb2e6",sleeve="#f4cfae"),b(0,"camera",x=800,y=1000,zoom=0.95,dur=0.01),
 b(0,"spawn",id="snow",prop="snow_out",x=0,y=0,layer="back"),b(0,"spawn",id="sf",prop="snowfall",x=0,y=0,layer="front"),
 b(0,"spawn",id="tb",prop="k_table",x=840,y=1250,layer="back"),b(0,"spawn",id="bf",prop="bill_flat",x=840,y=1120,layer="back"),
 b(0,"place",who="eng",x=730,y=0,face="right"),b(0,"pose",who="eng",pose="sit_cozy",dur=1.5),b(0,"emote",who="eng",emotion="happy",dur=1.5),
 b(1.8,"pose",who="eng",pose="sit_lean",dur=2.0),b(1.8,"emote",who="eng",emotion="neutral",dur=2.0),
 b(3.0,"move",id="bf",rot=180,dur=0.7,ease="easeInOut"),
 b(4.0,"camera",x=800,y=1100,zoom=1.2,dur=0.8,ease="easeInOut"),
 b(4.4,"spawn",id="bw1",prop="bill_w1",x=800,y=1400,layer="front",scale=0.95)]
for i,(k,t0) in enumerate((("w2",5.6),("w3",6.8),("w4",8.0))):
    be+=[b(t0,"remove",id=f"bw{i+1}"),b(t0+0.01,"spawn",id=f"bw{i+2}",prop="bill_"+k,x=800,y=1400,layer="front",scale=0.95),b(t0,"shake",dur=0.4,amp=4)]
be+=[b(9.4,"remove",id="bw4"),b(9.4,"camera",x=800,y=1000,zoom=0.95,dur=0.01),
 b(9.5,"portrait",on="eng",dur=4.5,zoom=2.4,angle="q45",bg="blur"),
 b(9.5,"pose",who="eng",pose="sit_slump",dur=1.5),b(9.5,"emote",who="eng",emotion="worried",dur=1.5),
 b(11.0,"pose",who="eng",pose="sit_up",dur=3.5),b(11.0,"emote",who="eng",emotion="smug",dur=3.5),
 b(10.0,"marker",name="тихий щелчок радиатора"),b(14.2,"marker",name="пауза, радиатор тихо щёлкает; конец"),
 say(10.4,"n35",3.8)]
mk("story_09_s12",16.5,START(),be)
