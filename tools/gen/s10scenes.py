import json
exec(open('s5scenes.py').read().split("CX=440")[0])
HERO={"type":"eng","x":-300,"face":"right","sy":0.82}
START=lambda: {"location":"cottage2","chars":{"narr":NARR,"eng":dict(HERO)}}
PJ=dict(shirt="#6f86c4",sleeve="#6f86c4",pants="#6f86c4",shoe="#c98a4a",pj=True,stripe="#cfdcff")
BED_X,BED_Y=450,-690
def FIX(lamp=True,hum=False,day=False):
    be=[b(0,"outfit",who="eng",**PJ)]
    if not day: be+=[b(0,"spawn",id="no",prop="night_out",x=0,y=0,layer="back"),b(0,"spawn",id="mn",prop="moon",x=1500,y=-250,layer="back"),b(0,"spawn",id="nd",prop="night_dim",x=0,y=0,layer="back")]
    be+=[
        b(0,"spawn",id="stv",prop="stove",x=330,y=1100,layer="back"),b(0,"spawn",id="bs",prop="brick_stove",x=520,y=1250,layer="back"),b(0,"spawn",id="ch",prop="chimney",x=520,y=1068,layer="back"),
        b(0,"spawn",id="nt_l",prop="lamp_on" if lamp else "lamp_off",x=575,y=616,layer="back",scale=0.8)]
    if lamp: be.append(b(0,"spawn",id="lg",prop="lamp_glow",x=575,y=616,layer="back",scale=0.8))
    elif not day: be.append(b(0,"spawn",id="nd2",prop="night_dim2",x=0,y=0,layer="back"))
    for k in range(11): be.append(b(0,"spawn",id=f"f1p{k}",prop="pipe_h",x=575+54*k,y=1250,layer="back"))
    for i,x in enumerate((900,1040)): be.append(b(0,"spawn",id=f"f1r{i}",prop="rad",x=x,y=1250,layer="front"))
    for k in range(10): be.append(b(0,"spawn",id=f"vp{k}",prop="pipe_v",x=1145,y=1250-54*k,layer="back"))
    for k in range(19): be.append(b(0,"spawn",id=f"f2p{k}",prop="pipe_h",x=1120-54*k,y=690,layer="back"))
    be.append(b(0,"spawn",id="f2r0",prop="rad",x=350,y=520,layer="back",scale=0.8))
    for k in range(10): be.append(b(0,"spawn",id=f"bp{k}",prop="pipe_v",x=580,y=1304+54*k,layer="back"))
    for k in range(10): be.append(b(0,"spawn",id=f"bh{k}",prop="pipe_h",x=290+54*k,y=1790,layer="back"))
    be+=[b(0,"spawn",id="boil",prop="boiler",x=180,y=1810,layer="back"),b(0,"spawn",id="tank",prop="tank",x=400,y=1810,layer="back"),
         b(0,"spawn",id="pm1",prop="pump",x=500,y=1790,layer="back"),b(0,"spawn",id="pm2",prop="pump",x=720,y=1790,layer="back")]
    return be
def LIE(t=0):  # герой лежит в кровати под одеялом
    return [b(t,"place",who="eng",x=BED_X,y=BED_Y,face="right"),b(t,"pose",who="eng",pose="lie")]
def BLANKET(t=0): return [b(t,"spawn",id="bl",prop="blanket",x=160,y=612,layer="front"),b(t,"spawn",id="pl",prop="pillow",x=140,y=600,layer="back")]
def POP(t,prop,x,y,dur=0.9,sc=1.0,id=None):
    i=id or f"pop{prop}{int(t*100)}"
    return [b(t,"spawn",id=i,prop=prop,x=x,y=y,layer="front",scale=0.01),b(t+0.02,"move",id=i,scale=sc,dur=0.25,ease="easeInOut"),b(t+dur,"remove",id=i)]
CAM=lambda t,x,y,z,d=1.0: b(t,"camera",x=x,y=y,zoom=z,dur=d,ease="easeInOut")
# ═════ S1 · Тишина ═════
be=FIX(lamp=True)+BLANKET()+LIE()+[CAM(0,450,800,1.2,0.01),b(0,"emote",who="eng",emotion="neutral",dur=0.5),
 b(0.4,"marker",name="поздняя ночь, тихо; щелчок выключателя на 1.6 с"),
 b(1.4,"pose",who="eng",pose="lie_ear"),
 b(1.9,"remove",id="lg"),b(1.9,"remove",id="nt_l"),b(1.9,"spawn",id="nt_l2",prop="lamp_off",x=575,y=616,layer="back",scale=0.8),b(1.9,"spawn",id="nd2",prop="night_dim2",x=0,y=0,layer="back"),
 b(2.0,"pose",who="eng",pose="lie"),b(2.2,"emote",who="eng",emotion="happy",dur=5),
 b(3.0,"spawn",id="zz",prop="snd_zzz",x=200,y=470,layer="front",scale=0.01),b(3.02,"move",id="zz",scale=1,dur=0.4),
 CAM(4.2,540,900,0.9,2.2)]
mk("story_10_s01",8.5,START(),be)
# ═════ S2 · Кап-кап ═════
be=FIX(lamp=False)+BLANKET()+LIE()+[CAM(0,450,800,1.2,0.01),b(0,"spawn",id="tp",prop="tap",x=695,y=598,layer="front",scale=1.5),b(0,"emote",who="eng",emotion="happy",dur=0.5)]
for tt in (0.9,2.9):
    be+=[b(tt,"spawn",id=f"dr{int(tt)}",prop="drop",x=725,y=545,layer="front",scale=1.4),b(tt+0.02,"move",id=f"dr{int(tt)}",y=612,dur=0.35,ease="easeIn"),b(tt+0.37,"remove",id=f"dr{int(tt)}")]
    be+=POP(tt+0.35,"snd_kap",710,420,0.9,1.0)
be+=[b(1.3,"emote",who="eng",emotion="surprised",dur=1.2),b(1.3,"marker",name="кап… кап… (капля)"),
 b(3.3,"emote",who="eng",emotion="angry",dur=0.8),
 b(3.6,"pose",who="eng",pose="idle"),b(3.6,"remove",id="bl"),b(3.6,"place",who="eng",x=330,y=-650,face="right"),
 b(4.0,"walk",who="eng",x=640,y=-560,dur=1.8,face="right"),
 b(5.8,"pose",who="eng",pose="valve_pull",dur=1.2),b(5.8,"emote",who="eng",emotion="angry",dur=1.2),b(5.8,"marker",name="скрип крана"),
 b(6.0,"remove",id="tp"),b(6.0,"spawn",id="tp2",prop="tap",x=695,y=598,layer="front",scale=1.5),
 b(7.2,"pose",who="eng",pose="idle"),b(7.2,"emote",who="eng",emotion="neutral",dur=0.5),
 b(7.4,"walk",who="eng",x=BED_X,y=BED_Y,dur=2.0,face="left"),
 b(9.5,"pose",who="eng",pose="lie"),b(9.5,"place",who="eng",x=BED_X,y=BED_Y,face="right"),b(9.5,"spawn",id="bl2",prop="blanket",x=160,y=612,layer="front"),b(9.6,"emote",who="eng",emotion="happy",dur=1.5)]
mk("story_10_s02",11.5,START(),be)
# ═════ S3 · Холодильник ═════
be=FIX(lamp=False)+BLANKET()+LIE()+[CAM(0,450,800,1.2,0.01),b(0,"spawn",id="tp",prop="tap",x=695,y=598,layer="front",scale=1.5),b(0,"emote",who="eng",emotion="happy",dur=0.5),
 b(1.0,"spawn",id="fo",prop="fridge_ov",x=0,y=0,layer="front"),b(1.0,"spawn",id="hw",prop="hum_waves",x=185,y=1040,layer="front"),
 b(1.0,"marker",name="тихое гудение холодильника"),*POP(1.1,"snd_uu",330,1010,1.8,0.8),
 b(2.2,"emote",who="eng",emotion="worried",dur=1.2),
 b(3.0,"spawn",id="pil",prop="pillow_c",x=92,y=380,layer="front"),b(3.02,"move",id="pil",y=634,dur=0.45,ease="easeIn"),
 b(4.6,"remove",id="fo"),b(4.6,"remove",id="hw"),b(4.6,"spawn",id="fo2",prop="fridge_ov2",x=0,y=0,layer="front"),b(4.6,"spawn",id="hw2",prop="hum_waves_r",x=185,y=1040,layer="front",scale=1.3),
 b(4.6,"marker",name="компрессор: гудение нарастает"),*POP(4.7,"snd_UU",330,1000,2.2,1.0),b(4.8,"shake",dur=1.4,amp=5),
 b(6.4,"remove",id="pil"),b(6.4,"remove",id="bl"),b(6.4,"pose",who="eng",pose="idle"),b(6.4,"place",who="eng",x=330,y=-650,face="right"),
 b(6.4,"emote",who="eng",emotion="furious",dur=2.5),b(6.5,"fx",kind="anger",x=340,y=440,dur=1.2)]
mk("story_10_s03",9.5,START(),be)
# ═════ захват 2: сцены 4–6 ═════
def DROP(id_,x,y0,y1,t,dur=0.5):
    return [b(t,"spawn",id=id_,prop="drop",x=x,y=y0,layer="front",scale=1.4),b(t+0.02,"move",id=id_,y=y1,dur=dur,ease="easeIn"),b(t+dur+0.04,"remove",id=id_)]
# ═════ S4 · Отопление ═════
be=FIX(lamp=False)+BLANKET()+LIE()+[CAM(0,450,800,1.2,0.01),b(0,"emote",who="eng",emotion="happy",dur=0.5),
 b(0.5,"remove",id="f2r0"),b(0.5,"spawn",id="rk",prop="rad_shake",x=350,y=520,layer="back",scale=0.8),*POP(0.6,"snd_tuk",360,390,1.8,1.0),
 b(0.6,"marker",name="металлический стук в радиаторе"),b(1.0,"emote",who="eng",emotion="surprised",dur=1.2),b(2.2,"emote",who="eng",emotion="angry",dur=0.8),
 b(2.6,"remove",id="rk"),b(2.6,"spawn",id="rn",prop="rad",x=350,y=520,layer="back",scale=0.8),
 b(2.6,"remove",id="bl"),b(2.6,"place",who="eng",x=255,y=-650,face="right"),b(2.6,"pose",who="eng",pose="idle"),
 b(3.0,"pose",who="eng",pose="touch"),b(3.0,"emote",who="eng",emotion="neutral",dur=1.0),
 b(4.2,"pose",who="eng",pose="valve_up"),b(4.2,"spawn",id="ap",prop="air_puffs",x=392,y=424,layer="front"),*POP(4.3,"snd_shsh",420,340,1.8,1.0),b(4.3,"marker",name="шипение выпускаемого воздуха"),
 b(6.0,"remove",id="ap"),b(6.0,"pose",who="eng",pose="idle"),b(6.0,"emote",who="eng",emotion="happy",dur=1.0),
 b(6.3,"walk",who="eng",x=BED_X,y=BED_Y,dur=1.3,face="right"),
 b(7.8,"place",who="eng",x=BED_X,y=BED_Y,face="right"),b(7.8,"pose",who="eng",pose="lie"),b(7.8,"spawn",id="bl2",prop="blanket",x=160,y=612,layer="front"),b(7.8,"emote",who="eng",emotion="happy",dur=0.9),
 b(7.8,"marker",name="тишина (пауза)"),
 b(8.8,"remove",id="rn"),b(8.8,"spawn",id="rb",prop="rad_bubbles",x=350,y=520,layer="back",scale=0.8),*POP(8.9,"snd_bul",330,380,1.8,1.0),
 b(8.9,"marker",name="громкое бульканье в трубах"),b(9.2,"emote",who="eng",emotion="furious",dur=1.5)]
mk("story_10_s04",10.8,START(),be)
# ═════ S5 · Насос ═════
be=FIX(lamp=False)+BLANKET()+LIE()+[CAM(0,450,1500,0.9,0.01),b(0,"emote",who="eng",emotion="happy",dur=0.5),
 b(0.5,"remove",id="pm1"),b(0.5,"spawn",id="pmo",prop="pump_ov",x=500,y=1790,layer="back"),b(0.5,"spawn",id="hwp",prop="hum_waves",x=560,y=1700,layer="front"),
 *POP(0.7,"snd_zh",640,1560,2.0,1.0),b(0.6,"marker",name="включился насос в котельной"),
 b(1.4,"emote",who="eng",emotion="angry",dur=1.0),
 b(2.2,"remove",id="bl"),b(2.2,"place",who="eng",x=330,y=-650,face="right"),b(2.2,"pose",who="eng",pose="idle"),b(2.2,"emote",who="eng",emotion="angry",dur=0.8),
 # путь вниз: снаружи слева по лестнице в подвал (монтажная склейка)
 b(3.0,"camera",x=-60,y=1480,zoom=0.9,dur=0.01),b(3.0,"place",who="eng",x=-370,y=0,face="right"),b(3.0,"pose",who="eng",pose="idle"),
 b(3.1,"walk",who="eng",x=-30,y=560,dur=2.4,ease="linear",face="right"),
 b(5.6,"camera",x=400,y=1620,zoom=0.95,dur=0.01),b(5.6,"place",who="eng",x=70,y=560,face="right"),
 b(5.7,"walk",who="eng",x=440,y=560,dur=1.4,face="right"),
 b(7.2,"pose",who="eng",pose="poke"),
 b(7.5,"remove",id="pmo"),b(7.5,"remove",id="hwp"),b(7.5,"spawn",id="pmd",prop="pump_off",x=500,y=1790,layer="back"),b(7.5,"marker",name="щелчок: насос выключен"),
 b(7.6,"emote",who="eng",emotion="happy",dur=1.0),
 b(8.6,"camera",x=450,y=1150,zoom=0.8,dur=0.01),b(8.6,"place",who="eng",x=BED_X,y=BED_Y,face="right"),b(8.6,"pose",who="eng",pose="lie"),b(8.6,"spawn",id="bl2",prop="blanket",x=160,y=612,layer="front"),b(8.7,"emote",who="eng",emotion="happy",dur=1.0),
 b(9.6,"remove",id="pmd"),b(9.6,"spawn",id="pmo2",prop="pump_ov",x=500,y=1790,layer="back"),b(9.6,"spawn",id="hwp2",prop="hum_waves",x=560,y=1700,layer="front"),*POP(9.8,"snd_zh",650,1560,2.0,1.0),
 b(9.7,"marker",name="насос снова включился"),
 b(10.8,"camera",x=250,y=640,zoom=1.5,dur=1.3,ease="easeInOut"),b(10.8,"pose",who="eng",pose="lie_look"),b(10.8,"emote",who="eng",emotion="furious",dur=2.5)]
mk("story_10_s05",13.6,START(),be)
# ═════ S6 · Участок ═════
be=FIX(lamp=False)+BLANKET()+LIE()+[CAM(0,780,1050,0.85,0.01),b(0,"emote",who="eng",emotion="happy",dur=0.5),
 b(0.4,"spawn",id="tb",prop="timer_box",x=1370,y=1250,layer="front"),b(0.4,"spawn",id="sp",prop="sprinkler",x=1290,y=1250,layer="front"),b(0.4,"spawn",id="ws",prop="wall_splash",x=1196,y=1160,layer="front"),
 *POP(0.6,"snd_ss",1250,1000,2.0,1.0),b(0.5,"marker",name="включился автоматический полив: ш-ш-ш"),
 b(1.4,"emote",who="eng",emotion="angry",dur=1.0),
 b(2.4,"remove",id="bl"),b(2.4,"place",who="eng",x=330,y=-650,face="right"),b(2.4,"pose",who="eng",pose="idle"),b(2.4,"emote",who="eng",emotion="angry",dur=0.8),
 b(3.2,"camera",x=1150,y=1100,zoom=0.85,dur=0.01),b(3.2,"place",who="eng",x=1100,y=0,face="right"),b(3.2,"pose",who="eng",pose="idle"),
 b(3.3,"walk",who="eng",x=1300,y=0,dur=1.3,face="right"),
 b(4.7,"pose",who="eng",pose="poke"),
 b(5.0,"remove",id="sp"),b(5.0,"remove",id="ws"),b(5.0,"remove",id="tb"),b(5.0,"spawn",id="tb2",prop="timer_box_off",x=1370,y=1250,layer="front"),b(5.0,"marker",name="щелчок: полив выключен"),
 b(5.1,"emote",who="eng",emotion="happy",dur=1.0),
 b(6.3,"camera",x=250,y=800,zoom=0.9,dur=0.01),b(6.3,"spawn",id="vz",prop="visor",x=-10,y=540,layer="front"),
 b(6.3,"place",who="eng",x=BED_X,y=BED_Y,face="right"),b(6.3,"pose",who="eng",pose="lie"),b(6.3,"spawn",id="bl2",prop="blanket",x=160,y=612,layer="front"),b(6.4,"emote",who="eng",emotion="happy",dur=1.0),
 b(6.3,"marker",name="тихо, ночь"),
 *DROP("dx1",-45,180,522,7.3,0.5),*POP(7.8,"snd_dzin",-60,430,1.0,1.0),b(7.9,"emote",who="eng",emotion="surprised",dur=1.0),b(7.8,"marker",name="дзынь: капля о козырёк"),
 *DROP("dx2",-45,180,522,9.2,0.5),*POP(9.7,"snd_dzin",-60,430,1.0,1.0),b(9.8,"emote",who="eng",emotion="furious",dur=1.5),b(9.7,"marker",name="дзынь")]
mk("story_10_s06",11.5,START(),be)
# ═════ захват 3: сцены 7–9 ═════
def BLACKOUT(t):
    be=[]
    for k in range(5): be.append(b(t+0.18*k,"spawn",id=f"bk{k}",prop="black_s",x=0,y=0,layer="front"))
    be.append(b(t+0.95,"spawn",id="bkf",prop="black_f",x=0,y=0,layer="front"))
    return be
# ═════ S7 · Ветер ═════
be=FIX(lamp=False)+BLANKET()+LIE()+[CAM(0,250,600,0.75,0.01),b(0,"emote",who="eng",emotion="happy",dur=0.5),
 b(0.3,"spawn",id="rs",prop="roof_sheet",x=0,y=0,layer="front"),b(0.3,"spawn",id="wd",prop="wind_a",x=140,y=300,layer="front"),
 *POP(1.0,"snd_bam",150,-120,1.0,1.0),b(1.0,"marker",name="хлопает незакреплённый лист металла"),
 b(1.6,"emote",who="eng",emotion="angry",dur=1.0),
 b(2.4,"remove",id="bl"),b(2.4,"place",who="eng",x=330,y=-650,face="right"),b(2.4,"pose",who="eng",pose="idle"),b(2.4,"emote",who="eng",emotion="angry",dur=0.8),
 b(3.2,"camera",x=-20,y=620,zoom=0.75,dur=0.01),b(3.2,"place",who="eng",x=-300,y=0,face="right"),b(3.2,"pose",who="eng",pose="idle"),
 b(3.2,"spawn",id="ld",prop="ladder",x=-110,y=1250,layer="back"),b(3.2,"move",id="ld",rot=-86,dur=0.01),
 b(3.4,"pose",who="eng",pose="hands_up"),b(3.5,"move",id="ld",rot=4,dur=1.4,ease="easeInOut"),b(3.5,"walk",who="eng",x=-170,y=0,dur=1.2,face="right"),
 b(5.2,"pose",who="eng",pose="idle"),b(5.2,"walk",who="eng",x=-112,y=0,dur=0.5,face="right"),
 b(5.8,"walk",who="eng",x=-30,y=-1095,dur=3.2,ease="linear",face="right"),
 b(9.1,"pose",who="eng",pose="hammer"),b(9.1,"emote",who="eng",emotion="angry",dur=1.2),
 b(9.8,"remove",id="rs"),b(9.8,"spawn",id="rs2",prop="roof_sheet2",x=0,y=0,layer="front"),b(9.8,"remove",id="wd"),b(9.8,"spawn",id="wd2",prop="wind_b",x=140,y=300,layer="front"),
 *POP(10.0,"snd_hlop",190,-120,1.4,1.0),b(10.0,"marker",name="ветер сильнее, лист хлопает громче"),
 b(11.0,"remove",id="rs2"),b(11.0,"spawn",id="rs3",prop="roof_sheet3",x=0,y=0,layer="front"),
 b(11.0,"pose",who="eng",pose="idle"),b(11.0,"emote",who="eng",emotion="furious",dur=3.0),b(11.2,"fx",kind="anger",x=-30,y=-60,dur=1.2),
 CAM(11.2,60,260,0.95,1.6),*POP(11.4,"snd_hlop",190,-140,1.6,1.3)]
mk("story_10_s07",14.0,START(),be)
# ═════ S8 · Полная тишина ═════
be=FIX(lamp=False)+BLANKET()+LIE()
be=[x for x in be if not (x.get("id") in ("f2r0","pm1","bl","pl") and x["do"]=="spawn")]
be+=[CAM(0,680,1150,0.75,0.01),
 b(0,"spawn",id="rb",prop="rad_bubbles",x=350,y=520,layer="back",scale=0.8),
 b(0,"spawn",id="pmo",prop="pump_ov",x=500,y=1790,layer="back"),b(0,"spawn",id="hwp",prop="hum_waves",x=560,y=1700,layer="back"),
 b(0,"spawn",id="fo2",prop="fridge_ov2",x=0,y=0,layer="front"),b(0,"spawn",id="hw2",prop="hum_waves_r",x=185,y=1040,layer="front",scale=1.3),
 b(0,"spawn",id="tb",prop="timer_box",x=1370,y=1250,layer="front"),b(0,"spawn",id="sp",prop="sprinkler",x=1290,y=1250,layer="front"),b(0,"spawn",id="ws",prop="wall_splash",x=1196,y=1160,layer="front"),
 b(0,"spawn",id="pl",prop="pillow",x=140,y=600,layer="back"),
 b(0,"place",who="eng",x=330,y=-650,face="right"),b(0,"pose",who="eng",pose="idle"),b(0,"emote",who="eng",emotion="furious",dur=1.4),b(0.1,"marker",name="всё шумит одновременно"),
 b(1.6,"place",who="eng",x=250,y=0,face="left"),b(1.6,"pose",who="eng",pose="poke"),b(2.2,"remove",id="fo2"),b(2.2,"remove",id="hw2"),*POP(2.2,"snd_shk",230,960,1.0,1.0),b(2.2,"marker",name="щёлк: холодильник"),
 b(3.2,"place",who="eng",x=255,y=-650,face="right"),b(3.2,"pose",who="eng",pose="valve_up"),b(3.9,"remove",id="rb"),b(3.9,"spawn",id="rn",prop="rad",x=350,y=520,layer="back",scale=0.8),*POP(3.9,"snd_shk",380,360,1.0,1.0),b(3.9,"marker",name="щёлк: отопление"),
 b(4.8,"place",who="eng",x=440,y=560,face="right"),b(4.8,"pose",who="eng",pose="poke"),b(5.4,"remove",id="pmo"),b(5.4,"remove",id="hwp"),b(5.4,"spawn",id="pmd",prop="pump_off",x=500,y=1790,layer="back"),*POP(5.4,"snd_shk",560,1600,1.0,1.0),b(5.4,"marker",name="щёлк: насос"),
 b(6.2,"place",who="eng",x=1290,y=0,face="right"),b(6.2,"pose",who="eng",pose="poke"),b(6.8,"remove",id="sp"),b(6.8,"remove",id="ws"),b(6.8,"remove",id="tb"),b(6.8,"spawn",id="tb2",prop="timer_box_off",x=1370,y=1250,layer="front"),*POP(6.8,"snd_shk",1330,1050,1.0,1.0),b(6.8,"marker",name="щёлк: полив"),
 b(7.6,"place",who="eng",x=330,y=-650,face="left"),b(7.6,"pose",who="eng",pose="hands_up"),b(7.6,"spawn",id="sh1",prop="shutter",x=210,y=300,layer="back"),b(7.7,"move",id="sh1",y=510,dur=0.9,ease="easeInOut"),b(7.7,"marker",name="закрывает окна"),
 b(8.8,"place",who="eng",x=BED_X,y=BED_Y,face="right"),b(8.8,"pose",who="eng",pose="lie"),b(8.8,"spawn",id="bl2",prop="blanket",x=160,y=612,layer="front"),b(8.9,"emote",who="eng",emotion="happy",dur=2.5),
 b(9.2,"spawn",id="zz",prop="snd_zzz",x=200,y=470,layer="front",scale=0.01),b(9.22,"move",id="zz",scale=1,dur=0.4),b(9.0,"marker",name="абсолютная тишина")]
mk("story_10_s08",11.5,START(),be)
# ═════ S9 · Финал ═════
be=FIX(lamp=False,day=True)+BLANKET()+LIE()+[CAM(0,450,800,1.2,0.01),b(0,"emote",who="eng",emotion="happy",dur=0.8),b(0.2,"marker",name="утро, тихо"),
 b(0.8,"spawn",id="al",prop="alarm",x=575,y=616,layer="front",scale=0.6),
 b(1.4,"remove",id="al"),b(1.4,"spawn",id="alb",prop="alarm",x=450,y=1000,layer="front",scale=4.2),*POP(1.6,"snd_ring",450,520,1.4,1.0),b(1.5,"marker",name="звонит будильник"),
 b(3.4,"remove",id="alb"),b(3.4,"spawn",id="al2",prop="alarm",x=575,y=616,layer="front",scale=0.6),b(3.4,"emote",who="eng",emotion="surprised",dur=0.8),
 b(4.4,"emote",who="eng",emotion="neutral",dur=2.0),
 b(6.4,"remove",id="bl"),b(6.4,"place",who="eng",x=330,y=-650,face="right"),b(6.4,"pose",who="eng",pose="idle"),
 b(7.0,"outfit",who="eng",shirt="#7fb2e6",sleeve="#7fb2e6",pants="#33405e",shoe="#4a3328",pj=False),b(7.0,"fx",kind="dust",x=330,y=500,dur=0.6),
 b(7.8,"camera",x=-60,y=1480,zoom=0.9,dur=0.01),b(7.8,"place",who="eng",x=-370,y=0,face="right"),b(7.8,"pose",who="eng",pose="idle"),b(7.9,"walk",who="eng",x=-30,y=560,dur=2.4,ease="linear",face="right"),
 b(10.4,"camera",x=400,y=1620,zoom=0.95,dur=0.01),b(10.4,"place",who="eng",x=70,y=560,face="right"),b(10.5,"walk",who="eng",x=640,y=560,dur=3.2,face="right"),
 b(13.9,"remove",id="pm1"),b(13.9,"spawn",id="pmo",prop="pump_ov",x=500,y=1790,layer="back"),b(13.9,"spawn",id="hwp",prop="hum_waves",x=560,y=1700,layer="front"),*POP(14.0,"snd_zh",540,1560,2.0,1.0),b(13.95,"marker",name="насос снова гудит"),
 b(14.2,"walk",who="eng",x=636,y=560,dur=1.2,face="left"),b(14.2,"emote",who="eng",emotion="worried",dur=1.5),
 *BLACKOUT(16.0),
 say(8.0,"n01",4.4)]
mk("story_10_s09",18.0,START(),be)
