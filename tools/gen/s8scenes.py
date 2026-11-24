import json
exec(open('s5scenes.py').read().split("CX=440")[0])
LANGF='lang/story_08.ru.json'
STONES=[380,500,620]
def cross(w,t,x0,dirn,hop_wobble=None,walk_v=200,log=False):
    """переход реки: dirn=+1 слева направо. Возвращает (beats, t_end). hop_wobble=(stone_index, dur)"""
    be=[]; ex=1100 if dirn>0 else -250
    top,bot=(40,300) if dirn>0 else (960,700)
    be.append(b(t,"walk",who=w,x=top,y=-220,dur=abs(top-x0)/walk_v,ease="linear",face="right" if dirn>0 else "left")); t+=abs(top-x0)/walk_v
    be.append(b(t,"walk",who=w,x=bot,y=0,dur=1.5,ease="linear")); t+=1.5
    seq=STONES if dirn>0 else STONES[::-1]
    far=700 if dirn>0 else 300
    if log:
        be.append(b(t,"walk",who=w,x=bot+dirn*10,y=-60,dur=0.25,ease="linear")); t+=0.25
        be.append(b(t,"walk",who=w,x=far-dirn*10,y=-60,dur=abs(far-bot)/130,ease="linear")); t+=abs(far-bot)/130
        be.append(b(t,"walk",who=w,x=far,y=0,dur=0.25,ease="linear")); t+=0.25
    else:
        for k,sx in enumerate(seq+[far]):
            be.append(b(t,"pose",who=w,pose="hop",dur=0.5)); be.append(b(t,"walk",who=w,x=sx,y=0,dur=0.5,ease="linear")); t+=0.5
            be.append(b(t,"pose",who=w,pose="idle",dur=0.1))
            if hop_wobble and k==hop_wobble[0]:
                d=hop_wobble[1]
                be+=[b(t,"pose",who=w,pose="balance",dur=d),b(t,"emote",who=w,emotion="surprised",dur=d),b(t+0.1,"fx",kind="exclaim",who=w,dur=0.8)]
                t+=d
                be.append(b(t,"emote",who=w,emotion="neutral",dur=0.3))
            t+=0.2
    be.append(b(t,"walk",who=w,x=top if False else (960 if dirn>0 else 40),y=-220,dur=1.5,ease="linear")); t+=1.5
    be.append(b(t,"walk",who=w,x=ex,y=-220,dur=abs((960 if dirn>0 else 40)-ex)/walk_v,ease="linear")); t+=abs((960 if dirn>0 else 40)-ex)/walk_v
    return be,t
EXTRAS={"ex1":{"type":"extra","x":-250,"face":"right","sy":0.8,"shirt":"#d8695f","hair":"#4a3426"},
 "ex2":{"type":"extra","x":1250,"face":"left","sy":0.8,"shirt":"#4a8fd0","hat":"#e8c24a","pants":"#3a4a6b"},
 "ex3":{"type":"extra","x":-430,"face":"right","sy":0.8,"shirt":"#7bbf6a","glasses":True,"hair":"#2a2a2a"},
 "ex4":{"type":"extra","x":1400,"face":"left","sy":0.8,"shirt":"#b07ad0","hair":"#8a5a2b"},
 "ex5":{"type":"extra","x":-600,"face":"right","sy":0.8,"shirt":"#e8a24a","hair":"#6a3f26"}}
def START(chars,cam=None):
    d={"location":"river","chars":{"narr":NARR}}
    for k in chars: d["chars"][k]=EXTRAS[k] if k in EXTRAS else chars[k]
    return d
CAM=lambda t=0:b(t,"camera",x=500,y=960,zoom=0.65,dur=0.01)
# ═════ S1 ═════
be=[CAM(0)]+[b(0,"spawn",id=f"st{i}",prop="stone",x=x,y=1280,layer="back") for i,x in enumerate(STONES)]+[b(0,"spawn",id="rd1",prop="reeds",x=305,y=1262,layer="back"),b(0,"spawn",id="rd2",prop="reeds",x=695,y=1262,layer="back"),say(0.3,"n01",7.5),say(8.0,"n02",2.3),b(0.3,"marker",name="тихая музыка, шаги, плеск")]
b1,e1=cross("ex1",0.3,-250,+1); b2,e2=cross("ex2",3.2,1250,-1,hop_wobble=(1,1.3)); b3,e3=cross("ex3",3.6,-430,+1)
be+=b1+b2+b3
print("ends",e1,e2,e3)
mk("story_08_s01",10.6,START(["ex1","ex2","ex3"]),be)


SCN=[b(0,"spawn",id=f"st{i}",prop="stone",x=x,y=1280,layer="back") for i,x in enumerate(STONES)]+[b(0,"spawn",id="rd1",prop="reeds",x=305,y=1262,layer="back"),b(0,"spawn",id="rd2",prop="reeds",x=695,y=1262,layer="back")]
# ═════ S2 ═════
HERO={"type":"bld","x":-520,"face":"right","sy":0.8}
be=[b(0,"camera",x=300,y=960,zoom=0.65,dur=0.01),b(0,"place",who="bld",x=-520,y=-220,face="right")]+SCN
be+=[b(0,"spawn",id="tr",prop="tree_log",x=-130,y=1030,layer="back"),say(0.3,"n03",3.3),say(3.9,"n04",3.6),say(7.6,"n05",3.0),
 b(0.2,"walk",who="bld",x=-440,dur=1.9,ease="linear"),
 b(2.2,"emote",who="bld",emotion="surprised",dur=0.9),b(2.3,"fx",kind="idea",who="bld",dur=1.0),
 b(3.0,"remove",id="tr"),b(3.0,"spawn",id="lc",prop="log_carry",x=-300,y=1030),b(3.05,"hold",id="lc",who="bld",hand="R"),
 b(3.0,"pose",who="bld",pose="mow",dur=3.3),b(3.2,"emote",who="bld",emotion="angry",dur=3.0),b(3.2,"fx",kind="sweat",who="bld",dur=2.8),
 b(3.2,"walk",who="bld",x=-130,dur=3.0,ease="linear"),b(3.2,"marker",name="кряхтение, волочение"),
 b(6.3,"release",id="lc",drop=False),b(6.3,"remove",id="lc"),
 b(6.3,"spawn",id="lf",prop="log_flat",x=90,y=1025,rot=0,layer="back"),
 b(6.35,"move",id="lf",x=200,y=1150,rot=22,dur=0.55,ease="easeIn"),
 b(6.9,"move",id="lf",x=500,y=1250,rot=0,dur=0.5,ease="bounce"),
 b(7.4,"fx",kind="dust",x=330,y=1245,dur=0.8),b(7.4,"shake",dur=0.4,amp=5),
 b(6.3,"pose",who="bld",pose="idle",dur=1.0),b(6.3,"emote",who="bld",emotion="happy",dur=1.2),
 b(6.4,"walk",who="bld",x=40,y=-220,dur=0.8,ease="linear"),b(7.2,"walk",who="bld",x=300,y=0,dur=1.4,ease="linear"),
 b(8.65,"walk",who="bld",x=335,y=-60,dur=0.3,ease="linear"),
 b(9.0,"pose",who="bld",pose="hop",dur=0.5),b(9.0,"move",id="lf",rot=-2.5,dur=0.15),b(9.2,"move",id="lf",rot=2,dur=0.2),b(9.4,"move",id="lf",rot=-1.2,dur=0.2),b(9.6,"move",id="lf",rot=0,dur=0.3),
 b(9.5,"pose",who="bld",pose="idle",dur=1.0),b(9.6,"emote",who="bld",emotion="happy",dur=1.0)]
mk("story_08_s02",10.8,{"location":"river","chars":{"narr":NARR,"bld":HERO}},be)
# ═════ S3 ═════
be=[CAM(0)]+SCN+[b(0,"spawn",id="lf",prop="log_flat",x=500,y=1250,layer="back"),say(0.3,"n06",5.1),say(5.8,"n07",5.7)]
LY=lambda x:-220+(x-40)*220/260
RY=lambda x:-220+(960-x)*220/260
be+=[b(0,"place",who="ex3",x=190,y=LY(190),face="right"),b(0,"place",who="ex5",x=105,y=LY(105),face="right"),b(0,"place",who="ex4",x=810,y=RY(810),face="left"),
 b(0.1,"emote",who="ex3",emotion="worried",dur=3.0),b(0.1,"emote",who="ex4",emotion="worried",dur=3.0)]
# ex1: слева направо, ex2: справа налево, встреча в 5.8
be+=[b(1.5,"walk",who="ex1",x=40,y=-220,dur=1.2,ease="linear"),b(2.7,"walk",who="ex1",x=300,y=0,dur=1.5,ease="linear"),
 b(4.2,"walk",who="ex1",x=310,y=-60,dur=0.25,ease="linear"),b(4.45,"walk",who="ex1",x=455,y=-60,dur=1.3,ease="linear"),
 b(1.5,"walk",who="ex2",x=960,y=-220,dur=1.4,ease="linear"),b(2.9,"walk",who="ex2",x=700,y=0,dur=1.5,ease="linear"),
 b(4.4,"walk",who="ex2",x=690,y=-60,dur=0.25,ease="linear"),b(4.65,"walk",who="ex2",x=545,y=-60,dur=1.1,ease="linear")]
# переговоры
be+=[b(5.8,"pose",who="ex1",pose="shrug",dur=1.5),b(5.8,"emote",who="ex1",emotion="worried",dur=1.5),b(5.9,"fx",kind="question",who="ex1",dur=1.2),
 b(6.0,"pose",who="ex2",pose="point",dur=1.4),b(6.0,"emote",who="ex2",emotion="angry",dur=1.4),
 b(7.4,"pose",who="ex1",pose="crouch_idle",dur=2.6),b(7.4,"emote",who="ex1",emotion="neutral",dur=2.6),
 b(8.3,"pose",who="ex2",pose="jump",dur=0.8),b(8.3,"walk",who="ex2",x=400,y=-60,dur=0.8,ease="linear"),
 b(9.1,"pose",who="ex2",pose="idle",dur=0.2),b(9.1,"walk",who="ex2",x=300,y=-60,dur=0.8,ease="linear"),
 b(9.9,"walk",who="ex2",x=290,y=0,dur=0.3,ease="linear"),
 b(10.0,"pose",who="ex1",pose="idle",dur=1.0),b(10.0,"walk",who="ex1",x=700,y=-60,dur=1.6,ease="linear"),
 b(10.1,"walk",who="ex3",x=300,y=0,dur=1.2,ease="soft"),b(10.5,"walk",who="ex5",x=200,y=LY(200),dur=0.8,ease="linear")]
mk("story_08_s03",11.8,START(["ex1","ex2","ex3","ex4","ex5"]),be)

PXK=lambda k:246+72*k
def planks(t0,step=0.0,ids="pk",y=1190,layer="back"):
    return [b(t0+k*step,"spawn",id=f"{ids}{k}",prop="plank",x=PXK(k),y=y,layer=layer) for k in range(8)]
LOGS=[b(0,"spawn",id="lf",prop="log_flat",x=500,y=1250,layer="back")]
# ═════ S4 ═════
be=[b(0,"camera",x=300,y=960,zoom=0.65,dur=0.01),b(0,"place",who="bld",x=-440,y=-220,face="right")]+SCN+LOGS
be+=[say(0.3,"n08",2.0),say(3.0,"n09",3.6),say(7.8,"n10",2.9),
 b(0,"spawn",id="lc2",prop="log_carry",x=-300,y=1030),b(0.05,"hold",id="lc2",who="bld",hand="R"),b(0,"pose",who="bld",pose="mow",dur=2.7),b(0,"emote",who="bld",emotion="angry",dur=2.6),
 b(0.2,"walk",who="bld",x=-130,dur=2.4,ease="linear"),
 b(2.6,"release",id="lc2",drop=False),b(2.6,"remove",id="lc2"),
 b(2.6,"spawn",id="l2",prop="log_flat",x=90,y=1025,layer="back"),b(2.65,"move",id="l2",x=200,y=1150,rot=22,dur=0.5,ease="easeIn"),b(3.15,"move",id="l2",x=500,y=1262,rot=0,dur=0.45,ease="bounce"),
 b(3.55,"fx",kind="dust",x=330,y=1255,dur=0.6),
 b(2.6,"pose",who="bld",pose="idle",dur=1.0),b(2.6,"emote",who="bld",emotion="neutral",dur=0.3),
 b(2.7,"walk",who="bld",x=-440,dur=0.9,ease="linear",face="left"),
 b(3.7,"spawn",id="lc3",prop="log_carry",x=-300,y=1030),b(3.75,"hold",id="lc3",who="bld",hand="R"),b(3.7,"pose",who="bld",pose="mow",dur=2.0),b(3.7,"emote",who="bld",emotion="angry",dur=1.9),
 b(3.7,"walk",who="bld",x=-130,dur=1.6,ease="linear",face="right"),
 b(5.4,"release",id="lc3",drop=False),b(5.4,"remove",id="lc3"),
 b(5.4,"spawn",id="l3",prop="log_flat",x=90,y=1025,layer="back"),b(5.45,"move",id="l3",x=200,y=1150,rot=22,dur=0.45,ease="easeIn"),b(5.9,"move",id="l3",x=500,y=1274,rot=0,dur=0.4,ease="bounce"),
 b(6.3,"fx",kind="dust",x=330,y=1265,dur=0.6),
 b(5.4,"pose",who="bld",pose="idle",dur=1.0),b(5.4,"emote",who="bld",emotion="happy",dur=1.0),
 b(5.6,"walk",who="bld",x=40,y=-220,dur=0.6,ease="linear"),b(6.2,"walk",who="bld",x=205,y=-76,dur=1.0,ease="linear")]
# настил: доски падают сверху по одной, герой за ними с молотком
T0=7.2
for k in range(8):
    t=T0+k*0.38
    be+=[b(t,"spawn",id=f"pk{k}",prop="plank",x=PXK(k),y=1100,layer="back"),b(t+0.02,"move",id=f"pk{k}",y=1190,dur=0.2,ease="easeIn"),
         b(t+0.12,"walk",who="bld",x=PXK(k)-90,y=-76 if k>0 else -76,dur=0.3,ease="linear")]
be+=[b(T0,"pose",who="bld",pose="hammer",dur=3.2),b(T0,"marker",name="стук молотка")]
be+=[b(10.4,"pose",who="bld",pose="idle",dur=1.5),b(10.4,"emote",who="bld",emotion="happy",dur=1.5),
 b(10.5,"walk",who="bld",x=-300,y=-220,dur=0.1,face="right") if False else b(10.5,"walk",who="bld",x=620,y=-76,dur=1.5,ease="soft")]
# люди идут уже свободно
be+=[b(8.6,"walk",who="ex1",x=40,y=-220,dur=1.2,ease="linear"),b(9.8,"walk",who="ex1",x=210,y=-76,dur=1.1,ease="linear"),b(10.9,"walk",who="ex1",x=790,y=-76,dur=2.6,ease="linear"),
 b(8.6,"walk",who="ex2",x=960,y=-220,dur=1.0,ease="linear"),b(9.6,"walk",who="ex2",x=790,y=-76,dur=1.0,ease="linear"),b(10.6,"walk",who="ex2",x=210,y=-76,dur=2.6,ease="linear")]
mk("story_08_s04",12.4,{"location":"river","chars":{"narr":NARR,"bld":HERO,"ex1":dict(EXTRAS["ex1"],x=-250,hidden=True),"ex2":dict(EXTRAS["ex2"],x=1250,hidden=True)}},be+[b(8.55,"place",who="ex1",x=-250,y=-220,face="right"),b(8.55,"place",who="ex2",x=1250,y=-220,face="left")])
# ═════ S5 ═════
HY=lambda x:-220+(x-40)*220/260
be=[b(0,"camera",x=500,y=960,zoom=0.65,dur=0.01)]+SCN+LOGS+[b(0,"spawn",id="l2",prop="log_flat",x=500,y=1262,layer="back"),b(0,"spawn",id="l3",prop="log_flat",x=500,y=1274,layer="back")]+planks(0)
be+=[b(0,"place",who="bld",x=150,y=HY(150),face="right"),b(0,"pose",who="bld",pose="arms_cross",dur=15),b(0,"emote",who="bld",emotion="neutral",dur=0.3),
 say(0.3,"n11",3.8),say(4.4,"n12",3.6),say(8.6,"n13",5.2),
 b(0,"spawn",id="ct",prop="cart",x=-250,y=1030),b(0.05,"hold",id="ct",who="ex3",hand="R"),b(0,"pose",who="ex3",pose="mow",dur=3.8),
 b(0.4,"walk",who="ex3",x=40,y=-220,dur=1.45,ease="linear"),b(1.85,"walk",who="ex3",x=210,y=-76,dur=1.2,ease="linear"),b(3.05,"walk",who="ex3",x=320,y=-76,dur=0.9,ease="linear"),
 b(3.95,"pose",who="ex3",pose="idle",dur=4.0),
 # велосипедист
 b(4.2,"spawn",id="bk",prop="bike_rider",x=-420,y=1030,layer="front",scale=1.5),
 b(4.4,"move",id="bk",x=40,y=1030,dur=1.3,ease="linear"),b(5.7,"move",id="bk",x=210,y=1174,dur=0.6,ease="linear"),b(6.3,"move",id="bk",x=790,y=1174,dur=1.9,ease="linear"),
 b(8.2,"move",id="bk",x=960,y=1030,dur=0.6,ease="linear"),b(8.8,"move",id="bk",x=1500,y=1030,dur=1.6,ease="linear"),
 b(5.0,"emote",who="bld",emotion="surprised",dur=0.8),
 # тележка выезжает на мост
 b(8.6,"pose",who="ex3",pose="mow",dur=2.0),b(8.6,"walk",who="ex3",x=400,y=-76,dur=0.95,ease="linear"),
 b(9.55,"remove",id="pk6"),b(9.55,"spawn",id="pc",prop="plank_crack",x=PXK(6),y=1192,layer="back"),
 b(9.55,"move",id="pk5",y=1196,dur=0.15),b(9.55,"move",id="pk7",y=1196,dur=0.15),
 b(9.55,"fx",kind="dust",x=PXK(6),y=1170,dur=0.7),b(9.55,"shake",dur=0.5,amp=6),b(9.55,"marker",name="треск доски"),
 b(9.65,"walk",who="ex3",x=405,y=-66,dur=0.15,ease="linear"),b(9.65,"pose",who="ex3",pose="shrug",dur=2.5),b(9.65,"emote",who="ex3",emotion="surprised",dur=2.5),b(9.7,"fx",kind="exclaim",who="ex3",dur=1.0),
 b(10.4,"emote",who="bld",emotion="worried",dur=3.5),b(10.6,"pose",who="bld",pose="facepalm",dur=3.5)]
mk("story_08_s05",14.6,{"location":"river","chars":{"narr":NARR,"bld":HERO,"ex3":dict(EXTRAS["ex3"],x=-250,hidden=True)}},be+[b(0.0,"place",who="ex3",x=-250,y=-220,face="right")])

# ═════ S6 ═════
be=[b(0,"camera",x=500,y=960,zoom=0.65,dur=0.01)]+SCN+[b(0,"spawn",id=f"lg{i}",prop="log_flat",x=500,y=1250+12*i,layer="back") for i in range(3)]
be+=[b(0,"spawn",id=f"pk{k}",prop="plank_crack" if k==6 else "plank",x=PXK(k),y=1190,layer="back") for k in range(8)]
be+=[b(0,"place",who="bld",x=-150,y=-220,face="right"),b(0,"pose",who="bld",pose="idle",dur=0.4),b(0,"emote",who="bld",emotion="neutral",dur=0.3),
 say(0.3,"n14",2.2),say(2.8,"n15",4.4),say(7.9,"n16",3.9)]
# опоры вырастают
for i,x in enumerate((400,600)):
    be+=[b(0.5+i*0.3,"spawn",id=f"pier{i}",prop="pier",x=x,y=1262,scale=0.05,layer="back"),b(0.55+i*0.3,"move",id=f"pier{i}",scale=1,dur=1.6,ease="easeOut"),b(2.2+i*0.3,"fx",kind="dust",x=x,y=1262,dur=0.6)]
be+=[b(0.5,"pose",who="bld",pose="hammer",dur=2.0),b(0.5,"marker",name="стук, бетон")]
# настил поднимается на уровень плато
for k in range(8):
    be+=[b(2.9,"move",id=f"pk{k}",y=1046,dur=1.3,ease="easeInOut")]
for i in range(3):
    be+=[b(2.9,"move",id=f"lg{i}",y=1106+12*i,dur=1.3,ease="easeInOut"),b(4.3,"remove",id=f"lg{i}")]
be+=[b(4.3,"spawn",id="gd",prop="girder",x=500,y=1082,layer="back"),b(2.9,"pose",who="bld",pose="point_up",dur=1.4),b(3.0,"emote",who="bld",emotion="happy",dur=1.3)]
# перила
be+=[b(4.6,"spawn",id="rl",prop="rail",x=500,y=1030,scale=0.05,layer="back"),b(4.65,"move",id="rl",scale=1,dur=0.6,ease="backSoft"),b(5.3,"remove",id="pk6"),b(5.3,"spawn",id="pk6n",prop="plank",x=PXK(6),y=1046,layer="back")]
# подъезды: насыпи
be+=[b(5.6,"spawn",id="fl",prop="fill_L",x=0,y=0,layer="back"),b(5.9,"spawn",id="fr",prop="fill_R",x=0,y=0,layer="back"),
 b(5.6,"shake",dur=0.5,amp=5),b(5.6,"fx",kind="dust",x=170,y=1030,dur=0.8),b(5.9,"fx",kind="dust",x=830,y=1030,dur=0.8),b(5.6,"marker",name="грохот насыпи")]
# герой идёт по мосту и стоит довольный
be+=[b(5.0,"pose",who="bld",pose="idle",dur=0.5),b(5.0,"walk",who="bld",x=1150,y=-220,dur=2.8,ease="soft"),b(7.85,"walk",who="bld",x=1150,y=-220,dur=0.05,face="left"),b(7.9,"pose",who="bld",pose="arms_cross",dur=4.0),b(7.9,"emote",who="bld",emotion="happy",dur=4.0)]
# машина на мосту
be+=[b(7.9,"spawn",id="cr",prop="car_blue",x=-380,y=1030,scale=0.4,layer="front"),b(8.0,"move",id="cr",x=1450,y=1030,dur=3.5,ease="linear")]
mk("story_08_s06",12.0,{"location":"river","chars":{"narr":NARR,"bld":dict(HERO,hidden=True)}},be)

BRIDGE6=[b(0,"spawn",id=f"pier{i}",prop="pier",x=x,y=1262,layer="back") for i,x in enumerate((400,600))]+[b(0,"spawn",id="gd",prop="girder",x=500,y=1082,layer="back")]+[b(0,"spawn",id=f"pk{k}",prop="plank",x=PXK(k),y=1046,layer="back") for k in range(8)]+[b(0,"spawn",id="rl",prop="rail",x=500,y=1030,layer="back"),b(0,"spawn",id="fl",prop="fill_L",x=0,y=0,layer="back"),b(0,"spawn",id="fr",prop="fill_R",x=0,y=0,layer="back")]
# ═════ S7 ═════
be=[b(0,"camera",x=500,y=960,zoom=0.65,dur=0.01)]+SCN+BRIDGE6
be+=[b(0,"place",who="bld",x=200,y=-220,face="right"),b(0,"pose",who="bld",pose="idle",dur=0.5),b(0,"emote",who="bld",emotion="happy",dur=1.0),
 say(0.3,"n17",1.7),say(2.3,"n18",5.9)]
def car(i,prop,x0,x1,t0,dur,ease="easeOut",sc=0.4,y=1030):
    return [b(t0,"spawn",id=f"cv{i}",prop=prop,x=x0,y=y,scale=sc,layer="back"),b(t0+0.02,"move",id=f"cv{i}",x=x1,dur=dur,ease=ease)]
be+=car(0,"car_blue",-420,330,1.0,1.9)+car(1,"car_yellow_l",1420,670,1.2,1.9)+car(2,"car_green",-900,-50,1.9,2.2)+car(3,"van_l",1900,1050,2.2,2.3)+car(4,"car_white",-1300,-430,2.7,2.3)+car(5,"car_blue_l",2300,1430,3.1,2.3)
be+=[b(3.1,"shake",dur=0.3,amp=4),b(3.15,"fx",kind="exclaim",x=420,y=800,dur=1.0),b(3.3,"fx",kind="exclaim",x=580,y=800,dur=1.0),b(3.2,"marker",name="гудки, все гудят"),
 b(3.6,"emote",who="bld",emotion="worried",dur=1.8),b(4.2,"fx",kind="sweat",on="bld",dur=1.5),
 b(4.4,"fx",kind="exclaim",x=60,y=800,dur=1.0),b(4.9,"fx",kind="exclaim",x=860,y=800,dur=1.0),b(5.2,"shake",dur=0.3,amp=3),
 b(6.0,"emote",who="bld",emotion="neutral",dur=1.0),
 b(6.7,"portrait",on="bld",dur=1.0,zoom=2.4,angle="side",bg="blur"),b(7.7,"portrait",on="bld",dur=2.4,zoom=2.4,angle="q45",bg="blur")]
mk("story_08_s07",10.2,{"location":"river","chars":{"narr":NARR,"bld":dict(HERO,hidden=True)}},be)
# ═════ S8 ═════
be=[b(0,"camera",x=500,y=960,zoom=0.65,dur=0.01),b(8.5,"camera",x=500,y=1000,zoom=0.5,dur=2.5,ease="easeInOut")]+SCN+BRIDGE6
be+=[b(0,"place",who="bld",x=200,y=-220,face="right"),b(0,"pose",who="bld",pose="point",dur=2.5),b(0,"emote",who="bld",emotion="neutral",dur=0.3),
 say(0.3,"n19",2.2),say(2.9,"n20",1.2),say(4.4,"n21",4.2)]
# убираем узкий настил, ставим широкую дорогу
for k in range(8): be.append(b(0.7,"remove",id=f"pk{k}"))
be+=[b(0.7,"remove",id="rl"),b(0.7,"remove",id="gd"),b(0.7,"spawn",id="rw",prop="road_wide",x=0,y=0,layer="back"),b(0.7,"shake",dur=0.6,amp=7),b(0.7,"fx",kind="dust",x=500,y=1130,dur=1.0),b(0.9,"fx",kind="dust",x=100,y=1130,dur=1.0),b(1.1,"fx",kind="dust",x=900,y=1130,dur=1.0),b(0.7,"marker",name="асфальт, грохот")]
for i,x in enumerate((340,500,660)):
    be+=[b(3.0+i*0.3,"spawn",id=f"pw{i}",prop="pier_w",x=x,y=1262,scale=0.05,layer="back"),b(3.05+i*0.3,"move",id=f"pw{i}",scale=1,dur=1.0,ease="easeOut"),b(4.0+i*0.3,"fx",kind="dust",x=x,y=1262,dur=0.6)]
be+=[b(4.6,"pose",who="bld",pose="think",dur=3.5),b(4.6,"emote",who="bld",emotion="confused",dur=3.5),b(5.0,"fx",kind="question",on="bld",dur=1.5)]
# потоки машин по трём полосам
LN=[(1058,0.40),(1092,0.43),(1126,0.46)]
sp=[("car_green",-500),("car_white",-1100),("car_yellow",-1700),("van",-2300)]
for j,(p,x0) in enumerate(sp):
    lane=j%2
    be+=[b(5.2+j*0.2,"spawn",id=f"c8_{j}",prop=p,x=-700-j*50,y=LN[lane][0],scale=LN[lane][1],layer="back"),b(5.22+j*0.2,"move",id=f"c8_{j}",x=1700,dur=3.4,ease="linear")]
be+=[b(5.4,"spawn",id="c8_l",prop="car_blue_l",x=1800,y=LN[2][0],scale=LN[2][1],layer="back"),b(5.42,"move",id="c8_l",x=-800,dur=4.0,ease="linear"),
 b(6.4,"spawn",id="c8_l2",prop="van_l",x=2000,y=LN[2][0],scale=LN[2][1],layer="back"),b(6.42,"move",id="c8_l2",x=-800,dur=4.2,ease="linear")]
mk("story_08_s08",11.0,{"location":"river","chars":{"narr":NARR,"bld":dict(HERO,hidden=True)}},be)

# ═════ S9 / S10: река_big ═════
BIGPIERS=[b(0,"spawn",id=f"bp{i}",prop="pier_big",x=x,y=1262,layer="back") for i,x in enumerate((650,850,1050,1250,1450))]
FORD=[b(0,"spawn",id=f"fs{k}",prop="stone",x=620+k*100,y=1345,layer="back") for k in range(10)]
BL=[(758,0.22),(792,0.24),(826,0.26)]
# ═════ S9 ═════
be=[b(0,"camera",x=1050,y=800,zoom=0.75,dur=0.01),b(0.3,"camera",x=1050,y=1000,zoom=0.42,dur=12.0,ease="easeInOut")]+BIGPIERS+FORD
be+=[say(0.5,"n22",3.1),say(4.0,"n23",4.6),say(9.3,"n24",4.5),b(0.3,"marker",name="шум трафика нарастает")]
props=["car_blue","car_yellow","van","car_green","car_white","car_blue"]
for j in range(18):
    ln=j%2; p=props[j%len(props)]
    be+=[b(0,"spawn",id=f"v{j}",prop=p,x=-600-j*330,y=BL[ln][0],scale=BL[ln][1],layer="back"),b(0.02,"move",id=f"v{j}",x=-600-j*330+7600,dur=13.5,ease="linear")]
for j in range(10):
    p=["car_yellow_l","van_l","car_white_l","car_green_l","car_blue_l"][j%5]
    be+=[b(0,"spawn",id=f"w{j}",prop=p,x=3000+j*600,y=BL[2][0],scale=BL[2][1],layer="back"),b(0.02,"move",id=f"w{j}",x=3000+j*600-8200,dur=13.5,ease="linear")]
be+=[b(0,"spawn",id="dt",prop="dump_truck",x=-1500,y=BL[1][0],scale=0.16,layer="back"),b(0.02,"move",id="dt",x=6000,dur=13.5,ease="linear")]
mk("story_08_s09",14.0,{"location":"river_big","chars":{"narr":NARR,"bld":dict(HERO,hidden=True)}},be)
# ═════ S10 ═════
be=[b(0,"camera",x=900,y=640,zoom=0.55,dur=0.01)]+BIGPIERS+FORD
be+=[b(0,"place",who="bld",x=760,y=-520,face="right"),b(0,"pose",who="bld",pose="idle",dur=0.5),b(0,"emote",who="bld",emotion="neutral",dur=0.5)]
be+=[b(0.2,"spawn",id="tk",prop="dump_truck",x=-700,y=BL[2][0]+20,scale=0.55,layer="front"),b(0.22,"move",id="tk",x=2600,dur=3.2,ease="linear"),b(0.3,"shake",dur=2.6,amp=3),b(0.3,"marker",name="тяжёлый грузовик, вибрация моста"),
 b(1.4,"emote",who="bld",emotion="surprised",dur=1.2),
 b(2.6,"camera",x=900,y=1450,zoom=0.55,dur=1.6,ease="easeInOut"),
 say(3.2,"n25",3.2),
 b(4.9,"camera",x=900,y=640,zoom=0.55,dur=0.8,ease="easeInOut"),b(4.9,"emote",who="bld",emotion="neutral",dur=1.5),
 b(6.0,"portrait",on="bld",dur=1.0,zoom=2.4,angle="side",bg="blur"),b(7.0,"portrait",on="bld",dur=3.0,zoom=2.4,angle="q45",bg="blur")]
mk("story_08_s10",10.0,{"location":"river_big","chars":{"narr":NARR,"bld":dict(HERO,hidden=True)}},be)
print('ok')
