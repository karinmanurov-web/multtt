import json
exec(open('s5scenes.py').read().split("CX=440")[0])
# ═════ S4: бульдозер ═════
DZ=-190; V4=209; x0=330
def dzx(t): return x0+V4*(t-0.2)
be=[b(0,"spawn",id="seat",prop="dozer_seat",x=x0,y=1250),b(0,"spawn",id="dz",prop="dozer",x=x0,y=1250,layer="front"),
 b(0,"spawn",id="pile",prop="dirt_pile",x=x0+470,y=1250,layer="front"),
 b(0,"spawn",id="ds",prop="dirt_strip",x=x0+400,y=1250,layer="back"),
 b(0,"pose",who="bld",pose="drive",dur=6.0),b(0,"emote",who="bld",emotion="neutral",dur=0.1),
 say(0.2,"n09",2.2),b(0.3,"marker",name="бульдозер: низкий рокот")]
xsC=[900+i*110 for i in range(12)]
for i,x in enumerate(xsC): be.append(b(0,"spawn",id=f"c{i}",prop="grass_mid" if i%2 else "grass_clump",x=x,y=1250,layer="back"))
T1=6.0
for tgt,(nm) in (("dz",None),):
    pass
be+=[b(0.2,"move",id="dz",x=dzx(T1),dur=T1-0.2,ease="linear"),b(0.2,"move",id="seat",x=dzx(T1),dur=T1-0.2,ease="linear"),
     b(0.2,"move",id="pile",x=dzx(T1)+470,dur=T1-0.2,ease="linear"),b(0.2,"move",id="ds",x=dzx(T1)+400,dur=T1-0.2,ease="linear"),
     b(0.2,"walk",who="bld",x=dzx(T1)+DZ,dur=T1-0.2,ease="linear")]
for i,x in enumerate(xsC):
    tt=0.2+(x-480-x0)/V4
    if tt<T1: be+=[b(tt,"remove",id=f"c{i}"),b(tt,"fx",kind="dust",x=x,y=1230,dur=0.5)]
be+=[b(2.6,"camera",x=900,y=1050,zoom=0.68,dur=1.3),b(4.0,"camera",x=1400,y=1050,zoom=0.68,dur=2.0),
 b(3.0,"say",who="narr",line="n10",dur=0.0) if False else say(3.2,"n10",2.6),
 # смена кадра: машина по новой дороге
 b(6.2,"remove",id="dz"),b(6.2,"remove",id="seat"),b(6.2,"remove",id="pile"),b(6.2,"remove",id="ds"),b(6.2,"camera",x=540,y=1000,zoom=0.8,dur=0.01),
 b(6.2,"spawn",id="road",prop="dirt_strip",x=3000,y=1250,layer="back"),
 b(6.2,"spawn",id="cs",prop="car_seat",x=-420,y=1250),b(6.2,"spawn",id="car",prop="car",x=-420,y=1250,layer="front"),
 b(6.2,"place",who="bld",x=-480,face="right"),b(6.2,"pose",who="bld",pose="drive",dur=5),b(6.2,"emote",who="bld",emotion="happy",dur=5),
 b(6.3,"move",id="car",x=1500,dur=4.8,ease="linear"),b(6.3,"move",id="cs",x=1500,dur=4.8,ease="linear"),b(6.3,"walk",who="bld",x=1440,dur=4.8,ease="linear"),
 b(6.3,"marker",name="машина едет, пыль")]
for k in range(8): be.append(b(6.6+k*0.55,"fx",kind="dust",x=-300+k*230,y=1240,dur=0.9))
mk("story_05_s04",11.6,{"location":"field","view":"main","chars":{"bld":{"x":x0+DZ,"face":"right"},"narr":NARR}},be)

# ═════ S5: дождь ═════
cx=440
be=[b(0,"spawn",id="road",prop="dirt_strip",x=3000,y=1250,layer="back"),
 b(0,"spawn",id="seat",prop="car_seat",x=cx,y=1250),b(0,"spawn",id="car",prop="car",x=cx,y=1250,layer="front"),
 b(0,"pose",who="bld",pose="drive",dur=2.4),b(0,"emote",who="bld",emotion="happy",dur=1.0),
 say(0.4,"n11",2.2),
 b(0.8,"spawn",id="cl",prop="storm_cloud",x=-900,y=160,layer="front"),b(0.8,"move",id="cl",x=540,dur=2.2,ease="easeOut"),
 b(1.0,"spawn",id="d1",prop="dark",x=0,y=0,layer="front"),b(1.9,"spawn",id="d2",prop="dark",x=0,y=0,layer="front"),b(2.7,"spawn",id="d3",prop="dark",x=0,y=0,layer="front"),
 b(1.8,"spawn",id="rain",prop="rain",x=0,y=0,layer="front"),b(1.9,"fx",kind="flash",dur=0.3),b(1.9,"marker",name="дождь, раскат грома"),
 b(2.4,"emote",who="bld",emotion="worried",dur=1.0),
 b(3.0,"spawn",id="mud",prop="mud_strip",x=540,y=1250,layer="back"),
 b(3.2,"camera",x=cx+300,y=1180,zoom=2.0,dur=0.6),b(3.3,"pose",who="bld",pose="drive_sink",dur=3.0),b(3.3,"emote",who="bld",emotion="angry",dur=3.0),
 b(3.4,"move",id="car",y=1300,dur=2.8,ease="linear"),b(3.4,"move",id="seat",y=1300,dur=2.8,ease="linear"),
 b(3.4,"shake",dur=2.8,amp=5),b(3.4,"fx",kind="dust",x=cx+300,y=1270,dur=2.8),b(3.4,"marker",name="колёса буксуют в грязи"),
 say(3.6,"n12",2.7),
 b(6.4,"camera",reset=True,dur=0.5),
 b(6.9,"place",who="bld",x=900,face="left"),b(6.9,"pose",who="bld",pose="shrug",dur=1.6),b(6.9,"emote",who="bld",emotion="sad",dur=3),
 b(6.9,"spawn",id="mf",prop="mud_front",x=900,y=1262,layer="front"),
 b(8.6,"pose",who="bld",pose="arms_cross",dur=3.0),b(8.8,"fx",kind="sweat",who="bld",dur=1.2),
 say(9.6,"n13",2.3)]
mk("story_05_s05",12.4,{"location":"field","view":"main","chars":{"bld":{"x":cx-60,"face":"right"},"narr":NARR}},be)

# ═════ S6: грунтовая дорога ═════
TX=0
segx=[-100+i*240 for i in range(7)]
be=[b(0,"spawn",id="road",prop="dirt_strip",x=3000,y=1250,layer="back"),
 b(0,"camera",x=540,y=1000,zoom=0.8,dur=0.01),
 b(0,"spawn",id="ts",prop="truck_seat",x=-500,y=1250),b(0,"spawn",id="tr",prop="dump_truck",x=-500,y=1250,layer="front"),
 b(0,"spawn",id="bd",prop="dump_bed_full",x=-500-470,y=1250-190,layer="front"),
 b(0,"place",who="bld",x=-500+320,face="right"),b(0,"pose",who="bld",pose="drive",dur=4.0),b(0,"emote",who="bld",emotion="neutral",dur=0.1),
 say(0.2,"n14",2.8),
 b(0.2,"move",id="tr",x=380,dur=2.0),b(0.2,"move",id="ts",x=380,dur=2.0),b(0.2,"move",id="bd",x=380-470,dur=2.0),b(0.2,"walk",who="bld",x=380+320,dur=2.0),
 b(0.3,"marker",name="самосвал подъезжает"),
 b(2.4,"move",id="bd",rot=-36,dur=1.1),b(3.6,"remove",id="bd"),b(3.6,"spawn",id="be",prop="dump_bed",x=380-470,y=1250-190,rot=-36,layer="front"),b(4.1,"move",id="be",rot=0,dur=0.9),b(2.4,"marker",name="кузов поднимается, камни сыплются"),
 b(2.8,"spawn",id="gp",prop="gravel_pile",x=380-520,y=1250,layer="back",scale=0.2),b(2.9,"move",id="gp",scale=1.1,dur=1.0,ease="easeOut"),
 b(2.9,"fx",kind="dust",x=380-520,y=1230,dur=1.2),b(2.9,"shake",dur=1.0,amp=4),
 b(3.7,"move",id="tr",x=1250,dur=2.2,ease="linear"),b(3.7,"move",id="ts",x=1250,dur=2.2,ease="linear"),b(3.7,"move",id="be",x=1250-470,dur=2.2,ease="linear"),b(3.7,"walk",who="bld",x=1250+320,dur=2.2,ease="linear")]
for i,x in enumerate(segx):
    t=3.9+i*0.26
    be.append(b(t,"spawn",id=f"g{i}",prop="gravel_seg",x=x,y=1250,layer="back"))
be+=[b(3.7,"remove",id="gp"),
 # смена: каток
 b(6.1,"remove",id="tr"),b(6.1,"remove",id="ts"),b(6.1,"remove",id="be"),
 b(6.1,"spawn",id="rs",prop="roller_seat",x=-500,y=1250),b(6.1,"spawn",id="ro",prop="roller",x=-500,y=1250,layer="front"),
 b(6.1,"place",who="bld",x=-500-130,face="right"),b(6.1,"pose",who="bld",pose="drive",dur=4.0),b(6.1,"emote",who="bld",emotion="happy",dur=3),
 b(6.2,"move",id="ro",x=1100,dur=4.0,ease="linear"),b(6.2,"move",id="rs",x=1100,dur=4.0,ease="linear"),b(6.2,"walk",who="bld",x=970,dur=4.0,ease="linear"),
 b(6.2,"marker",name="каток, уплотнение"),
 say(8.0,"n15",3.0)]
for i,x in enumerate(segx):
    t=6.2+(x+200)/400+0.05
    be+=[b(t,"remove",id=f"g{i}"),b(t,"spawn",id=f"rd{i}",prop="road_seg",x=x,y=1250,layer="back")]
be+=[b(10.3,"remove",id="ro"),b(10.3,"remove",id="rs"),b(10.3,"hide",who="bld"),
 b(10.3,"camera",x=700,y=1000,zoom=0.72,dur=0.01),
 b(10.0,"callout",on="bld",key="c_road",style="pop",dur=1.6) if False else b(10.3,"marker",name="конфетти, «ура»"),
 b(10.3,"fx",kind="confetti",x=700,y=900,dur=2.0),
 b(11.2,"show",who="bld"),b(11.2,"place",who="bld",x=-480,face="right"),b(11.2,"pose",who="bld",pose="drive",dur=4),b(11.2,"emote",who="bld",emotion="happy",dur=4),
 b(11.2,"spawn",id="cs",prop="car_seat",x=-420,y=1250),b(11.2,"spawn",id="car",prop="car",x=-420,y=1250,layer="front"),
 b(11.3,"move",id="car",x=1500,dur=4.6,ease="linear"),b(11.3,"move",id="cs",x=1500,dur=4.6,ease="linear"),b(11.3,"walk",who="bld",x=1440,dur=4.6,ease="linear")]
for k in range(7): be.append(b(11.6+k*0.6,"fx",kind="dust",x=-300+k*260,y=1240,dur=0.9))
mk("story_05_s06",16.2,{"location":"field","view":"main","chars":{"bld":{"x":-180,"face":"right"},"narr":NARR}},be)
print('ok')
