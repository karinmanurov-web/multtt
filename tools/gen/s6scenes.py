import json
exec(open('s5scenes.py').read().split("CX=440")[0])
START=lambda x=540: {"location":"room","view":"main","chars":{"bld":{"x":x,"face":"right"},"narr":NARR}}
def room(ceil=620,door="door_closed",slabs=False,sock=1215,ball=160):
    be=[b(0,"spawn",id="ceil",prop="ceiling",x=540,y=ceil),b(0,"spawn",id="door",prop=door,x=870,y=1250,layer="back"),
        b(0,"spawn",id="s1",prop="socket",x=520,y=sock,layer="back"),b(0,"spawn",id="s2",prop="socket",x=620,y=sock,layer="back")]
    if slabs:
        for i,x in enumerate(range(-10,1100,200)): be.append(b(0,"spawn",id=f"sl{i}",prop="slab",x=x,y=1250,layer="back"))
    return be
# ═════ S1 ═════
be=[b(0,"spawn",id="ceil",prop="ceiling",x=540,y=620),b(0,"spawn",id="door",prop="door_closed",x=870,y=1250,layer="back"),
 b(0,"spawn",id="s1",prop="socket",x=520,y=1164,layer="back"),b(0,"spawn",id="s2",prop="socket",x=620,y=1164,layer="back"),
 b(0,"spawn",id="lv",prop="level_tilt",x=640,y=1010),b(0.05,"hold",id="lv",who="bld",hand="R"),
 b(0,"pose",who="bld",pose="idle",dur=3.0),say(0.2,"n01",2.2),
 b(0.4,"spawn",id="ball",prop="ball",x=760,y=1262,layer="front"),b(0.6,"move",id="ball",x=170,dur=2.2,ease="easeIn",rot=-900),
 b(0.6,"marker",name="шарик катится, мягкий стук"),
 b(2.8,"pose",who="bld",pose="idle",dur=1.0),b(2.9,"emote",who="bld",emotion="neutral",dur=0.1),
 say(3.2,"n02",3.5),b(3.2,"release",id="lv",drop=False),b(3.2,"remove",id="lv"),
 b(3.3,"spawn",id="bk",prop="bucket",x=860,y=1262,layer="back"),b(3.3,"spawn",id="rk",prop="rake",x=560,y=1250),b(3.35,"hold",id="rk",who="bld",hand="R"),
 b(3.3,"pose",who="bld",pose="rake",dur=3.0)]
mk("story_06_s01",7.2,START(),be)
# ═════ S2 ═════
be=[b(0,"spawn",id="ceil",prop="ceiling",x=540,y=620),b(0,"spawn",id="door",prop="door_closed",x=870,y=1250,layer="back"),
 b(0,"spawn",id="s1",prop="socket",x=520,y=1164,layer="back"),b(0,"spawn",id="s2",prop="socket",x=620,y=1164,layer="back"),
 b(0,"spawn",id="ball",prop="ball",x=170,y=1262,layer="front"),b(0,"spawn",id="bk",prop="bucket",x=960,y=1262,layer="back"),
 b(0,"spawn",id="rk",prop="rake",x=300,y=1250),b(0.05,"hold",id="rk",who="bld",hand="R"),b(0,"pose",who="bld",pose="rake",dur=2.4),b(0,"place",who="bld",x=100,face="right"),
 b(0.1,"walk",who="bld",x=880,dur=2.2,ease="linear")]
for i,x in enumerate(range(-10,1100,200)):
    t=0.3+i*0.35
    be+=[b(t,"spawn",id=f"sl{i}",prop="slab",x=x,y=1250,layer="back"),b(t,"fx",kind="dust",x=x,y=1240,dur=0.4)]
be+=[b(2.5,"release",id="rk",drop=False),b(2.5,"remove",id="rk"),b(2.5,"spawn",id="lv",prop="level_ok",x=640,y=1010),b(2.55,"hold",id="lv",who="bld",hand="R"),
 b(2.5,"pose",who="bld",pose="cheer",dur=1.4),b(2.5,"emote",who="bld",emotion="happy",dur=1.4),b(2.6,"fx",kind="stars",who="bld",dur=1.0),b(2.5,"marker",name="дзынь"),
 say(2.8,"n03",3.8),
 b(4.1,"release",id="lv",drop=False),b(4.1,"remove",id="lv"),
 b(4.0,"walk",who="bld",x=690,dur=0.7,face="right"),b(4.8,"pose",who="bld",pose="pull",dur=1.8),b(4.9,"emote",who="bld",emotion="confused",dur=2.0),
 b(4.9,"move",id="door",x=878,dur=0.12),b(5.1,"move",id="door",x=866,dur=0.12),b(5.3,"move",id="door",x=878,dur=0.12),b(5.5,"move",id="door",x=868,dur=0.12),
 b(4.9,"shake",dur=1.0,amp=3),b(4.9,"marker",name="дверь скребёт по полу, не открывается")]
mk("story_06_s02",7.6,START(100),be)
# ═════ S3 ═════
be=room(slabs=True,sock=1215)[:4]+[b(0,"spawn",id="ball",prop="ball",x=170,y=1262,layer="front")]
be=[b(0,"spawn",id="ceil",prop="ceiling",x=540,y=620),b(0,"spawn",id="d1",prop="door_closed",x=870,y=1250,layer="back")]
for i,x in enumerate(range(-10,1100,200)): be.append(b(0,"spawn",id=f"sl{i}",prop="slab",x=x,y=1250,layer="back"))
be+=[b(0,"spawn",id="s1",prop="socket",x=520,y=1238,layer="back"),b(0,"spawn",id="s2",prop="socket",x=620,y=1238,layer="back"),
 b(0,"spawn",id="ball",prop="ball",x=170,y=1262,layer="front"),
 b(0,"pose",who="bld",pose="saw",dur=2.6),say(0.3,"n04",2.0),
 b(0.2,"spawn",id="sw",prop="saw",x=870,y=1195,layer="front"),b(0.2,"marker",name="пила по дереву"),
 b(0.3,"fx",kind="dust",x=870,y=1190,dur=2.2),
 b(2.6,"remove",id="sw"),b(2.6,"remove",id="d1"),b(2.6,"spawn",id="d2",prop="door_cut",x=870,y=1250,layer="back"),
 b(2.8,"remove",id="d2"),b(2.8,"spawn",id="d3",prop="door_open",x=870,y=1250,layer="back"),b(2.8,"pose",who="bld",pose="idle",dur=0.8),b(2.9,"emote",who="bld",emotion="happy",dur=0.7),
 b(3.5,"walk",who="bld",x=410,dur=0.8,face="right"),
 b(3.6,"camera",x=520,y=1150,zoom=2.0,dur=0.5),
 b(3.7,"pose",who="bld",pose="think",dur=2.4),b(3.8,"emote",who="bld",emotion="tired",dur=1.8),say(3.7,"n05",3.0),
 b(5.2,"spawn",id="mx",prop="mark_x",x=520,y=1110,layer="back"),
 b(5.7,"move",id="s1",y=1120,dur=0.5),b(5.7,"move",id="s2",y=1120,dur=0.5),b(6.2,"remove",id="mx"),b(6.0,"marker",name="розетки поднимают"),
 b(6.7,"camera",reset=True,dur=0.5),b(6.8,"emote",who="bld",emotion="neutral",dur=0.1)]
mk("story_06_s03",7.8,START(650),be)
# ═════ S4 ═════
def static(ceil=620):
    be=[b(0,"spawn",id="ceil",prop="ceiling",x=540,y=ceil),b(0,"spawn",id="door",prop="door_open",x=870,y=1250,layer="back")]
    for i,x in enumerate(range(-10,1100,200)): be.append(b(0,"spawn",id=f"sl{i}",prop="slab",x=x,y=1250,layer="back"))
    be+=[b(0,"spawn",id="s1",prop="socket",x=520,y=1120,layer="back"),b(0,"spawn",id="s2",prop="socket",x=620,y=1120,layer="back"),b(0,"spawn",id="ball",prop="ball",x=170,y=1262,layer="front")]
    return be
be=static()+[b(0,"pose",who="bld",pose="cheer",dur=1.8),b(0,"emote",who="bld",emotion="happy",dur=1.8),say(0.3,"n06",1.8),
 b(2.3,"move",id="ceil",y=745,dur=0.9,ease="easeIn"),b(2.3,"shake",dur=1.2,amp=4),b(2.3,"marker",name="потолок ползёт вниз, скрип"),
 b(2.9,"pose",who="bld",pose="ouch",dur=1.6),b(2.9,"emote",who="bld",emotion="shocked",dur=1.2),b(3.0,"fx",kind="stars",x=540,y=740,dur=1.0),b(3.0,"marker",name="дзынь: каска о потолок"),
 say(4.2,"n07",2.6),
 b(4.6,"pose",who="bld",pose="crouch_idle",dur=1.2),b(4.8,"emote",who="bld",emotion="angry",dur=1.6),
 b(6.3,"pose",who="bld",pose="crouch_walk",dur=3.0),b(6.3,"walk",who="bld",x=250,dur=3.0,ease="linear",face="left"),b(6.4,"emote",who="bld",emotion="tired",dur=3.0),
 b(7.0,"fx",kind="dust",x=480,y=745,dur=0.5),b(8.0,"fx",kind="dust",x=380,y=745,dur=0.5)]
for x in [0]: pass
be=[bb for bb in be]
mk("story_06_s04",9.6,START(540),be)
# ═════ S5 ═════
be=static(745)+[b(0,"spawn",id="lv",prop="level_ok",x=500,y=1030),b(0.05,"hold",id="lv",who="bld",hand="R"),
 b(0,"pose",who="bld",pose="crouch_idle",dur=2.3),b(0,"emote",who="bld",emotion="tired",dur=2.2),say(0.3,"n08",1.6),
 b(2.3,"release",id="lv",drop=False),b(2.3,"remove",id="lv"),
 b(2.3,"portrait",on="bld",dur=1.1,zoom=2.4,angle="side",bg="blur"),
 b(3.4,"portrait",on="bld",dur=3.2,zoom=2.4,angle="q45",bg="blur"),
 b(2.4,"emote",who="bld",emotion="frown",dur=4.3)]
mk("story_06_s05",6.9,START(250),be)
print('ok')
