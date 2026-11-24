import json
exec(open('s5scenes.py').read().split("CX=440")[0])
CAM=lambda t,x=540,y=1050,z=0.8,d=0.01: b(t,"camera",x=x,y=y,zoom=z,dur=d)
def veh(id,prop,t0,dur,xa,xb,lane,ease="linear"):
    y,layer,sc=(1420,"front",1.0) if lane=="n" else (1290,"back",0.9)
    return [b(t0,"spawn",id=id,prop=prop,x=xa,y=y,layer=layer,scale=sc),b(t0,"move",id=id,x=xb,dur=dur,ease=ease),b(t0+dur+0.05,"remove",id=id)]
# ═════ S7: по дороге ездят другие ═════
be=[CAM(0),b(0,"spawn",id="road",prop="road_wide",x=540,y=1250,layer="back"),
 b(0,"pose",who="bld",pose="arms_cross",dur=11),b(0,"emote",who="bld",emotion="neutral",dur=0.1),
 say(0.2,"n16",3.8),b(0.3,"marker",name="первая машина, шум мотора")]
be+=veh("v1","car_blue",0.7,3.0,-600,1700,"n")+veh("v2","car_yellow",2.8,3.4,-600,1700,"f")+veh("v3","car_green_l",4.0,3.2,1700,-600,"n")
be+=veh("v4","van",5.2,3.4,-600,1700,"n")+veh("v5","car_white_l",5.8,3.3,1700,-600,"f")
be+=[say(4.1,"n17",2.5),b(6.4,"emote",who="bld",emotion="worried",dur=3),
 b(7.0,"spawn",id="ph1",prop="pothole",x=640,y=1445,layer="back"),b(7.0,"spawn",id="ph2",prop="pothole",x=240,y=1470,layer="back")]
be+=veh("v6","car_blue",7.2,1.7,-600,520,"n","easeOut")
be+=[b(8.9,"spawn",id="v6b",prop="car_blue",x=520,y=1420,layer="front"),b(8.9,"move",id="v6b",x=1800,dur=1.8,ease="easeIn"),b(10.8,"remove",id="v6b"),b(8.9,"fx",kind="dust",x=300,y=1440,dur=1.0)]
be+=[b(8.0,"spawn",id="v7",prop="car_yellow_l",x=1800,y=1290,layer="back",scale=0.9),b(8.0,"move",id="v7",x=860,dur=1.5,ease="easeOut"),b(9.6,"move",id="v7",x=-700,dur=1.8,ease="easeIn"),b(11.5,"remove",id="v7"),
 b(8.6,"fx",kind="dust",x=700,y=1300,dur=1.0),b(7.2,"marker",name="тормозят перед ямами"),
 say(7.4,"n18",3.1)]
be.pop() if False else None
mk("story_05_s07",12.0,{"location":"field","view":"main","chars":{"bld":{"x":150,"face":"right"},"narr":NARR}},be)
# ═════ S8: улучшаем дорогу ═════
segx=[-100+i*240 for i in range(8)]
be=[CAM(0),b(0,"spawn",id="road",prop="road_wide",x=540,y=1250,layer="back"),
 b(0,"pose",who="bld",pose="shrug",dur=2.6),b(0,"emote",who="bld",emotion="sad",dur=3),
 say(0.2,"n19",3.4),b(0.3,"marker",name="ветер, скрип; на дороге ямы, лужи, колеи")]
for i,(x,pp,y) in enumerate([(300,"pothole",1450),(640,"pothole",1430),(980,"pothole",1470),(120,"puddle_b",1400),(820,"puddle_b",1380),(470,"puddle_b",1470)]):
    be.append(b(0,"spawn",id=f"h{i}",prop=pp,x=x,y=y,layer="back"))
be+=[b(3.2,"spawn",id="seatE",prop="exc_seat",x=-500,y=1250),b(3.2,"spawn",id="ex",prop="excavator",x=-500,y=1250,layer="front")]
# экскаватор: герой уезжает в кабине — на 3.2 «пересаживается»
be+=[b(3.2,"place",who="bld",x=-500-150,face="right"),b(3.2,"pose",who="bld",pose="drive",dur=4.0),b(3.2,"emote",who="bld",emotion="angry",dur=0.1),
 b(3.2,"marker",name="экскаватор, рокот"),say(3.7,"n20",3.2),
 b(3.2,"move",id="ex",x=1100,dur=4.0,ease="linear"),b(3.2,"move",id="seatE",x=1100,dur=4.0,ease="linear"),b(3.2,"walk",who="bld",x=950,dur=4.0,ease="linear")]
for i in range(6): be.append(b(3.2+(2.0+0.0*i),"remove",id=f"h{i}") if False else b(3.2+0.4+i*0.55,"remove",id=f"h{i}"))
for i,x in enumerate(segx):
    t=3.2+(x+200)/400
    be+=[b(t,"spawn",id=f"b{i}",prop="base_seg",x=x,y=1250,layer="back"),b(t,"fx",kind="dust",x=x+60,y=1300,dur=0.5)]
# асфальтоукладчик
be+=[b(7.4,"remove",id="ex"),b(7.4,"remove",id="seatE"),
 b(7.4,"spawn",id="seatP",prop="paver_seat",x=-500,y=1250),b(7.4,"spawn",id="pv",prop="paver",x=-500,y=1250,layer="front"),
 b(7.4,"place",who="bld",x=-500-95,face="right"),b(7.4,"pose",who="bld",pose="drive",dur=4),b(7.4,"emote",who="bld",emotion="happy",dur=3),
 b(7.5,"move",id="pv",x=1100,dur=4.0,ease="linear"),b(7.5,"move",id="seatP",x=1100,dur=4.0,ease="linear"),b(7.5,"walk",who="bld",x=1005,dur=4.0,ease="linear"),
 b(7.5,"marker",name="асфальтоукладчик")]
for i,x in enumerate(segx):
    t=7.5+(x+200)/400+0.05
    be+=[b(t,"remove",id=f"b{i}"),b(t,"spawn",id=f"a{i}",prop="asphalt_seg",x=x,y=1250,layer="back")]
# финальный вид: бордюры, разметка, знаки, фонари
be+=[b(11.8,"remove",id="pv"),b(11.8,"remove",id="seatP"),b(11.8,"place",who="bld",x=150,face="right"),b(11.8,"pose",who="bld",pose="hips",dur=4),b(11.8,"emote",who="bld",emotion="happy",dur=3),
 b(11.9,"spawn",id="cb",prop="curbs",x=540,y=1250,layer="back"),
 b(12.3,"spawn",id="mk",prop="marking",x=540,y=1250,layer="back"),
 b(12.7,"spawn",id="sg1",prop="sign",x=820,y=1250,layer="back"),b(13.0,"spawn",id="sg2",prop="sign",x=1050,y=1250,layer="back"),
 b(13.3,"spawn",id="lp1",prop="lamp",x=330,y=1250,layer="back"),b(13.5,"spawn",id="lp2",prop="lamp",x=620,y=1250,layer="back"),
 b(11.9,"fx",kind="sparks",x=400,y=1100,dur=1.0) if False else b(12.7,"marker",name="знаки, разметка"),
 say(11.9,"n21",3.5)]
mk("story_05_s08",16.0,{"location":"field","view":"main","chars":{"bld":{"x":150,"face":"right"},"narr":NARR}},be)
# ═════ S9: трасса ═════
be=[CAM(0),b(0,"spawn",id="road",prop="road_wide",x=540,y=1250,layer="back"),
 b(0,"spawn",id="plan",prop="plan",x=250,y=1100),b(0.05,"hold",id="plan",who="bld",hand="R"),
 b(0,"pose",who="bld",pose="idle",dur=2.4),
 say(0.2,"n22",2.2)]
be+=[b(0,"spawn",id="cb",prop="curbs",x=540,y=1250,layer="back"),b(0,"spawn",id="mk",prop="marking",x=540,y=1250,layer="back")]
be+=veh("w1","car_blue",0.5,2.6,-600,1700,"n")+veh("w2","car_white_l",1.2,2.6,1700,-600,"f")+veh("w3","van",2.0,2.4,-600,1700,"n")
# пробка
be+=[b(2.9,"camera",x=540,y=1050,zoom=0.55,dur=0.6)]
jam=[("j1","car_yellow",-500,"n"),("j2","car_green",440,"n"),("j3","van",1380,"n"),("j4","car_white",-30,"f"),("j5","car_blue",930,"f")]
for id,pp,x,lane in jam:
    y,layer,sc=(1420,"front",1.0) if lane=="n" else (1290,"back",0.9)
    be+=[b(3.0,"spawn",id=id,prop=pp,x=x-900 if x<500 else x+900,y=y,layer=layer,scale=sc),b(3.0,"move",id=id,x=x,dur=0.8,ease="easeOut")]
be+=[b(3.6,"emote",who="bld",emotion="surprised",dur=2.5),b(3.6,"fx",kind="question",who="bld",dur=1.6),say(4.1,"n23",2.7),
 b(3.8,"shake",dur=3.0,amp=3),b(3.8,"marker",name="сигналят: гудки"),b(4.0,"callout",on="bld",key="c_horn",style="shake",dur=1.6),
 b(6.9,"pose",who="bld",pose="point",dur=1.4),b(7.0,"camera",x=540,y=1050,zoom=0.8,dur=0.6)]
for id,_,_,_ in jam: be.append(b(8.0,"remove",id=id))
be+=[b(8.0,"remove",id="plan"),b(8.0,"view",id="aerial2",transition="fade",dur=0.5),b(8.0,"hide",who="bld"),b(8.0,"remove",id="road"),b(8.0,"remove",id="cb"),b(8.0,"remove",id="mk"),
 b(8.0,"camera",x=540,y=-200,zoom=0.3,dur=0.01),
 say(8.8,"n24",5.4),
 b(8.6,"spawn",id="r1",prop="aer_road1",x=540,y=1500,scale=0.05),b(8.7,"move",id="r1",scale=1.0,dur=1.4,ease="easeOut"),
 b(10.4,"remove",id="r1"),b(10.4,"spawn",id="r2",prop="aer_road2",x=540,y=1500,scale=0.1),b(10.5,"move",id="r2",scale=1.0,dur=1.0,ease="easeOut"),
 b(12.0,"remove",id="r2"),b(12.0,"spawn",id="r4",prop="aer_road4",x=540,y=1500,scale=0.1),b(12.1,"move",id="r4",scale=1.0,dur=1.0,ease="easeOut"),
 b(13.0,"spawn",id="br",prop="aer_barriers",x=540,y=1500,scale=0.1),b(13.0,"move",id="br",scale=1.0,dur=0.8),b(13.4,"spawn",id="lt",prop="aer_lights",x=540,y=1500,scale=0.1),b(13.4,"move",id="lt",scale=1.0,dur=0.8),
 b(14.2,"spawn",id="cr",prop="aer_cross",x=540,y=-2000,scale=0.05),b(14.3,"move",id="cr",scale=1.0,dur=1.0,ease="easeOut"),
 b(15.6,"spawn",id="bp",prop="aer_bypass",x=540,y=-6000,scale=0.05),b(15.7,"move",id="bp",scale=1.0,dur=1.2,ease="easeOut"),
 b(8.7,"camera",x=540,y=-2800,zoom=0.095,dur=9.0,ease="easeInOut"),b(8.7,"marker",name="дрон отдаляется")]
mk("story_05_s09",18.4,{"location":"field","view":"main","chars":{"bld":{"x":150,"face":"right"},"narr":NARR}},be)
print('ok')
