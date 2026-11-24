import json
exec(open('s5scenes.py').read().split("CX=440")[0])
N=12
PX=lambda i:320+62*i
HX=lambda i:PX(i)-190
START=lambda x:{"location":"yard","view":"main","chars":{"bld":{"x":x,"face":"right"},"narr":NARR}}
def fence_raw():
    return [b(0,"spawn",id=f"r{i}",prop="pk_raw",x=PX(i),y=1250,layer="back") for i in range(N)]
def paint(i0,i1,t0,step,prop,tag,old=None,holdwalk=True):
    be=[]
    for k,i in enumerate(range(i0,i1)):
        t=t0+k*step
        if old: be.append(b(t,"remove",id=f"{old}{i}"))
        be.append(b(t,"spawn",id=f"{tag}{i}",prop=prop,x=PX(i),y=1250,layer="back"))
        be.append(b(t-step+0.02 if k else t-0.05,"walk",who="bld",x=HX(i),dur=step*0.9,ease="linear"))
    return be
def gear(brush,can,t=0.05):
    return [b(0,"spawn",id="br",prop=brush,x=300,y=1250),b(t,"hold",id="br",who="bld",hand="R"),
            b(0,"spawn",id="cn",prop=can,x=300,y=1250),b(t,"hold",id="cn",who="bld",hand="L")]
# ═════ S1 ═════
be=fence_raw()+gear("brush_g1","can_g1")+[b(0,"pose",who="bld",pose="paint",dur=7.0),b(0,"emote",who="bld",emotion="neutral",dur=0.2),
 say(0.2,"n01",2.4),say(3.3,"n02",2.3)]
be+=paint(0,7,1.0,0.45,"pk_g1","a")
be+=[b(1.0,"marker",name="мазки кистью, тихая музыка"),b(4.5,"pose",who="bld",pose="shrug",dur=2.4),b(4.7,"emote",who="bld",emotion="worried",dur=2.2),
 b(4.5,"release",id="br",drop=False),b(4.5,"remove",id="br"),b(4.5,"spawn",id="br2",prop="brush_dry",x=300,y=1250),b(4.55,"hold",id="br2",who="bld",hand="R"),
 b(4.6,"marker",name="кисть скребёт по пустой банке")]
mk("story_07_s01",7.0,START(HX(0)-30),be)
# ═════ S2 ═════
be=fence_raw()+[b(0,"spawn",id=f"a{i}",prop="pk_g1",x=PX(i),y=1250,layer="back") for i in range(7)]
be+=[b(0,"spawn",id="br2",prop="brush_dry",x=300,y=1250),b(0.05,"hold",id="br2",who="bld",hand="R"),
 b(0,"spawn",id="cn",prop="can_e",x=300,y=1250),b(0.05,"hold",id="cn",who="bld",hand="L"),
 b(0,"pose",who="bld",pose="shrug",dur=1.4),b(0,"emote",who="bld",emotion="worried",dur=1.4),say(0.3,"n03",2.6),
 b(1.5,"pose",who="bld",pose="idle",dur=1.6),b(1.5,"walk",who="bld",x=1350,dur=1.6,ease="easeIn",face="right"),
 b(3.1,"release",id="br2",drop=False),b(3.1,"remove",id="br2"),b(3.1,"release",id="cn",drop=False),b(3.1,"remove",id="cn"),
 b(3.1,"spawn",id="br3",prop="brush_g2",x=300,y=1250),b(3.15,"hold",id="br3",who="bld",hand="R"),
 b(3.1,"spawn",id="cn2",prop="can_g2",x=300,y=1250),b(3.15,"hold",id="cn2",who="bld",hand="L"),
 b(3.1,"place",who="bld",x=-160,face="right"),b(3.15,"pose",who="bld",pose="idle",dur=1.5),
 b(3.2,"walk",who="bld",x=HX(7),dur=1.5,ease="easeOut"),say(3.5,"n04",2.4),
 b(4.7,"pose",who="bld",pose="paint",dur=2.8),b(4.7,"emote",who="bld",emotion="neutral",dur=0.2)]
be+=paint(7,12,4.9,0.45,"pk_g2","c")
be+=[b(7.1,"pose",who="bld",pose="idle",dur=0.6)]
mk("story_07_s02",7.8,START(HX(7)),be)
# ═════ S3 ═════
be=fence_raw()+[b(0,"spawn",id=f"a{i}",prop="pk_g1",x=PX(i),y=1250,layer="back") for i in range(7)]+[b(0,"spawn",id=f"c{i}",prop="pk_g2",x=PX(i),y=1250,layer="back") for i in range(7,12)]
be+=gear("brush_g2","can_g2")+[b(0,"pose",who="bld",pose="idle",dur=1.6),b(0,"emote",who="bld",emotion="happy",dur=1.4),say(0.3,"n05",3.2)]
for k in range(4):
    t=1.3+k*0.35
    be+=[b(t,"remove",id=f"a{k}"),b(t,"spawn",id=f"p{k}",prop="pk_g1p",x=PX(k),y=1250,layer="back")]
    for j in range(3):
        fx=PX(k)+(j-1)*18
        be+=[b(t,"spawn",id=f"f{k}{j}",prop="flake",x=fx,y=1000+j*60,layer="front"),b(t+0.02,"move",id=f"f{k}{j}",x=fx+(j-1)*40,y=1250,rot=360*(j+1),dur=0.9,ease="easeIn"),b(t+0.95,"remove",id=f"f{k}{j}")]
be+=[b(1.4,"marker",name="краска хрустит, чешуйки падают"),
 b(2.4,"pose",who="bld",pose="shrug",dur=1.2),b(2.4,"emote",who="bld",emotion="surprised",dur=1.0),b(2.5,"fx",kind="exclaim",who="bld",dur=0.9),
 b(3.7,"pose",who="bld",pose="idle",dur=0.6),b(3.7,"emote",who="bld",emotion="tired",dur=2.6),
 b(4.4,"pose",who="bld",pose="idle",dur=3.0),b(4.4,"walk",who="bld",x=HX(0),dur=2.6,ease="easeInOut",face="left"),
 b(7.0,"walk",who="bld",x=HX(0),dur=0.2,face="right")]
mk("story_07_s03",7.4,START(HX(11)),be)
# ═════ S4 ═════
be=fence_raw()+[b(0,"spawn",id=f"p{i}",prop="pk_g1p",x=PX(i),y=1250,layer="back") for i in range(4)]+[b(0,"spawn",id=f"a{i}",prop="pk_g1",x=PX(i),y=1250,layer="back") for i in range(4,7)]+[b(0,"spawn",id=f"c{i}",prop="pk_g2",x=PX(i),y=1250,layer="back") for i in range(7,12)]
be+=gear("brush_g2","can_g2")+[b(0,"pose",who="bld",pose="idle",dur=1.0),b(0,"emote",who="bld",emotion="neutral",dur=0.2),say(0.2,"n06",2.4),
 b(1.2,"pose",who="bld",pose="paint",dur=5.0),b(1.2,"marker",name="кисть, мазки заново")]
for k,i in enumerate(range(12)):
    t=1.2+k*0.42
    old="p" if i<4 else ("a" if i<7 else "c")
    be+=[b(t,"remove",id=f"{old}{i}"),b(t,"spawn",id=f"n{i}",prop="pk_g2",x=PX(i),y=1250,layer="back"),
         b(t-0.4 if k else t-0.05,"walk",who="bld",x=HX(i),dur=0.38,ease="linear")]
be+=[say(4.3,"n07",2.0),b(6.3,"pose",who="bld",pose="idle",dur=1.0),b(6.3,"emote",who="bld",emotion="tired",dur=1.3)]
mk("story_07_s04",7.6,START(HX(0)),be)
# ═════ S5 ═════
X0=HX(11)
be=[b(0,"spawn",id=f"n{i}",prop="pk_g2",x=PX(i),y=1250,layer="back") for i in range(12)]
be+=[b(0,"spawn",id="vs",prop="vest_stain",x=X0,y=1110,layer="back"),
 b(0,"pose",who="bld",pose="idle",dur=1.0),b(0,"emote",who="bld",emotion="neutral",dur=0.3),
 b(0.5,"pose",who="bld",pose="idle",dur=1.4),b(0.5,"walk",who="bld",x=X0-280,dur=1.3,ease="easeInOut",face="left"),
 b(0.5,"marker",name="шаги, тишина"),
 b(1.9,"walk",who="bld",x=X0-280,dur=0.05,face="right"),
 b(1.95,"emote",who="bld",emotion="confused",dur=0.8),
 b(1.9,"camera",x=X0-140,y=1050,zoom=1.5,dur=1.0),
 b(3.1,"angle",who="bld",angle="back",dur=0.4),b(3.25,"vest",who="bld",color="#2f8049",stripe="#276f40"),
 b(3.6,"pose",who="bld",pose="angry",dur=2.6),b(3.7,"shake",dur=1.8,amp=4),b(3.7,"fx",kind="anger",who="bld",dur=1.6),
 b(3.7,"marker",name="низкое рычание")]
mk("story_07_s05",6.4,START(X0),be)
print('ok')
