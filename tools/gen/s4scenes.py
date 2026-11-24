import os; REPO=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..'))+'/'
import json
D=REPO+''
def mk(id,dur,start,beats):
    beats=sorted(beats,key=lambda b:b['t'])
    json.dump({"id":id,"duration":dur,"start":start,"defs":{},"beats":beats},open(D+f'scenes/{id}.json','w'),ensure_ascii=False,indent=2)
NARR={"type":"extra","x":540,"face":"left","hidden":True,"shirt":"#24242a","sy":0.8}
def b(t,do,**k): return {"t":t,"do":do,**k}
def say(t,line,d,who="narr"): return b(t,"say",who=who,line=line,dur=d)
def clock(t,mn,hr,n=""):
    return [b(t,"spawn",id="hh"+n,prop="clock_hour",x=540,y=640,rot=hr),b(t,"spawn",id="mm"+n,prop="clock_min",x=540,y=640,rot=mn)]
def noclock(t,n=""): return [b(t,"remove",id="hh"+n),b(t,"remove",id="mm"+n)]
# ───── S1 ─────
beats=[b(0,"pose",who="eng",pose="sit",dur=3.7),say(0.2,"n01",3.7),
 b(3.9,"view",id="clock",transition="cut"),b(3.9,"hide",who="eng"),*clock(3.9,0,270),
 say(4.0,"n02",1.7),b(4.5,"move",id="mm",rot=5,dur=1.2),
 *noclock(5.9),b(5.9,"view",id="desk",transition="cut"),b(5.9,"show",who="eng"),
 b(5.9,"pose",who="eng",pose="sit_up",dur=1.0),b(6.0,"emote",who="eng",emotion="confused",dur=1.0),
 say(6.2,"n03",3.0),
 b(7.0,"portrait",on="eng",dur=1.5,zoom=2.3,angle="q45",bg="blur"),b(7.0,"emote",who="eng",emotion="shocked",dur=1.5),
 b(7.2,"fx",kind="question",who="eng",dur=1.2),
 b(9.3,"view",id="clock",transition="cut"),b(9.3,"hide",who="eng"),*clock(9.3,90,277.5,"b"),b(9.3,"marker",name="tick"),
 *noclock(9.9,"b"),b(9.9,"view",id="desk",transition="cut"),b(9.9,"show",who="eng"),
 say(10.0,"n04",3.6),
 b(10.0,"pose",who="eng",pose="sit_tap",dur=1.4),b(11.4,"pose",who="eng",pose="sit_up",dur=1.2),b(12.6,"pose",who="eng",pose="sit_lean",dur=0.9),b(13.5,"pose",who="eng",pose="sit_slump",dur=1.0),
 b(11.4,"emote",who="eng",emotion="tired",dur=3)]
mk("story_04_s01",14.8,{"location":"office_day","view":"desk","chars":{"eng":{"x":540,"face":"right"},"narr":NARR},
 },beats)
# ───── S2 ─────
KW=NARR
beats=[b(0,"spawn",id="ket",prop="kettle",x=150,y=1090),
 b(0,"walk",who="eng",x=200,dur=1.3),b(1.4,"hold",id="ket",who="eng",hand="R"),
 say(0.2,"n05",1.8),
 b(2.0,"camera",x=190,y=1000,zoom=2.0,dur=0.6),b(2.1,"pose",who="eng",pose="present",dur=1.0),
 b(3.3,"emote",who="eng",emotion="sad",dur=2.2),b(3.3,"pose",who="eng",pose="tired",dur=2.0),
 say(3.4,"n06",2.0),b(3.6,"fx",kind="sweat",who="eng",dur=1.2),
 b(5.3,"camera",reset=True,dur=0.5),
 b(5.4,"walk",who="eng",x=215,dur=1.0),
 b(6.4,"release",id="ket",drop=False),b(6.4,"move",id="ket",x=392,y=1088,dur=0.3),
 b(6.4,"spawn",id="hdl",prop="tap_handle",x=330,y=985),
 b(6.7,"pose",who="eng",pose="crank",dur=1.6),
 b(7.0,"move",id="hdl",rot=50,dur=0.6),
 b(7.0,"spawn",id="wt",prop="water_thin",x=394,y=990),
 say(6.6,"n07",2.5),
 say(9.2,"n08",1.3),
 b(9.9,"marker",name="щелчок: метал"),
 b(9.9,"remove",id="wt"),
 b(9.9,"spawn",id="fo",prop="fountain",x=394,y=962),
 b(9.9,"move",id="ket",x=520,y=1230,arc=-260,rot=140,dur=0.7),
 b(9.9,"move",id="hdl",x=330,y=985,rot=-35,dur=0.2),
 b(9.9,"walk",who="eng",x=160,dur=0.55,ease="easeOut",face="keep"),
 b(9.9,"pose",who="eng",pose="fall_back",dur=1.4),b(9.9,"emote",who="eng",emotion="shocked",dur=2),b(9.9,"fx",kind="exclaim",who="eng",dur=1.0),
 b(9.9,"shake",dur=2.0,amp=12),
 b(9.9,"callout",on="eng",key="c_burst",style="slam",dur=1.4),
 b(11.3,"pose",who="eng",pose="hands_up",dur=1.0),
 b(9.9,"spawn",id="flood",prop="flood",x=540,y=2850,layer="front"),b(10.0,"move",id="flood",y=2290,dur=2.6)]
mk("story_04_s02",12.6,{"location":"office_day","view":"kitchen","chars":{"eng":{"x":-80,"face":"right"},"narr":NARR}},beats)
# ───── S3 ─────
beats=[b(0,"spawn",id="fo",prop="fountain",x=394,y=962),b(0,"spawn",id="hdl",prop="tap_handle",x=330,y=985,rot=-35),
 b(0,"spawn",id="flood",prop="flood",x=540,y=2290,layer="front"),b(0.1,"move",id="flood",y=2230,dur=13),
 b(0,"spawn",id="val",prop="valve",x=880,y=905),
 b(0,"shake",dur=14,amp=3),
 b(0,"pose",who="eng",pose="crank",dur=2.6),
 say(0.2,"n09",2.6),b(0.4,"move",id="hdl",rot=720,dur=2.4),
 b(2.8,"camera",x=330,y=1000,zoom=2.2,dur=0.5),b(2.9,"move",id="hdl",rot=1800,dur=2.8),b(2.9,"pose",who="eng",pose="crank",dur=2.8),
 say(3.1,"n10",2.8),b(3.2,"fx",kind="sweat",who="eng",dur=1.5),b(3.2,"emote",who="eng",emotion="angry",dur=2.8),
 b(6.1,"camera",reset=True,dur=0.4),
 say(6.4,"n11",1.9),b(6.4,"walk",who="eng",x=755,dur=1.4),b(6.4,"emote",who="eng",emotion="worried",dur=1.5),
 b(8.0,"camera",x=745,y=1010,zoom=2.0,rot=-5,dur=0.5),
 b(8.0,"pose",who="eng",pose="valve_pull",dur=2.6),b(8.0,"emote",who="eng",emotion="angry",dur=2.8),
 b(8.4,"marker",name="скрип металла"),b(9.2,"shake",dur=1.4,amp=7),
 b(10.6,"marker",name="срыв вентиля"),
 b(10.6,"move",id="val",x=330,y=1200,arc=-320,rot=900,dur=0.8),
 b(10.6,"walk",who="eng",x=590,dur=0.6,ease="easeOut",face="keep"),b(10.6,"pose",who="eng",pose="fall_back",dur=1.2),
 b(10.6,"emote",who="eng",emotion="shocked",dur=1.0),
 b(11.8,"camera",reset=True,dur=0.5),
 b(11.9,"pose",who="eng",pose="tired",dur=1.5),b(11.9,"emote",who="eng",emotion="tired",dur=2),
 b(12.0,"portrait",on="eng",dur=1.5,zoom=2.4,angle="side",bg="blur"),
 say(12.5,"n12",0.9)]
mk("story_04_s03",14.2,{"location":"office_day","view":"kitchen","chars":{"eng":{"x":215,"face":"right"},"narr":NARR}},beats)
# ───── S4 ─────
MASTER={"type":"extra","x":330,"face":"right","hidden":False,"skin":"#f0c9a5","shirt":"#fafafa","sleeve":"#fafafa","pants":"#d9dde6","shoe":"#fafafa","hair":"#3a2c24"}
beats=[b(0,"spawn",id="fo",prop="fountain",x=394,y=962),b(0,"spawn",id="hdl",prop="tap_handle",x=330,y=985,rot=-35),
 b(0,"spawn",id="flood",prop="flood",x=540,y=2230,layer="front"),b(0.1,"move",id="flood",y=2205,dur=5),
 b(0,"shake",dur=17,amp=3),
 b(0,"spawn",id="ph",prop="phone",x=560,y=1070),b(0.1,"hold",id="ph",who="eng",hand="R"),
 b(0,"pose",who="eng",pose="idle",dur=5.0),
 say(0.2,"n13",3.5),say(3.9,"n14",1.5),
 b(5.4,"location",id="phone_screen",transition="cut"),b(5.4,"hide",who="eng"),b(5.4,"remove",id="fo"),b(5.4,"remove",id="flood"),b(5.4,"remove",id="hdl"),
 b(5.4,"spawn",id="ctap",prop="clean_tap",x=640,y=1094),
 b(5.4,"show",who="master"),
 say(5.6,"n15",3.0,who="master"),
 b(8.8,"location",id="office_day",view="kitchen",transition="cut"),b(8.8,"show",who="eng"),b(8.8,"hide",who="master"),b(8.8,"spawn",id="fo2",prop="fountain",x=394,y=962),b(8.8,"spawn",id="hdl2",prop="tap_handle",x=330,y=985,rot=-35),b(8.8,"spawn",id="flood2",prop="flood",x=540,y=2205,layer="front"),b(8.9,"move",id="flood2",y=2195,dur=2.5),b(8.8,"remove",id="ctap"),
 b(8.8,"pose",who="eng",pose="point",dur=1.2),b(8.9,"emote",who="eng",emotion="confused",dur=2.4),
 say(9.0,"n16",2.2),b(9.2,"fx",kind="question",who="eng",dur=1.2),
 b(11.5,"location",id="phone_screen",transition="cut"),b(11.5,"hide",who="eng"),b(11.5,"show",who="master"),b(11.5,"remove",id="fo2"),b(11.5,"remove",id="flood2"),b(11.5,"remove",id="hdl2"),b(11.5,"spawn",id="ctool",prop="clean_tool",x=640,y=1094),
 say(11.7,"n17",3.0,who="master"),
 b(14.9,"location",id="office_day",view="kitchen",transition="cut"),b(14.9,"show",who="eng"),b(14.9,"hide",who="master"),b(14.9,"spawn",id="fo3",prop="fountain",x=394,y=962),b(14.9,"spawn",id="hdl3",prop="tap_handle",x=330,y=985,rot=-35),b(14.9,"spawn",id="flood3",prop="flood",x=540,y=2195,layer="front"),b(15.0,"move",id="flood3",y=2185,dur=4),b(14.9,"remove",id="ctool"),
 b(14.9,"pose",who="eng",pose="crank",dur=1.0),
 b(15.9,"marker",name="усиленный фонтан"),b(15.9,"remove",id="fo3"),b(15.9,"spawn",id="fo4",prop="fountain",x=394,y=962,scale=1.35),b(15.9,"shake",dur=1.5,amp=16),
 b(15.9,"callout",on="eng",key="c_more",style="shake",dur=1.4),
 b(15.9,"spawn",id="cart",prop="cartridge",x=340,y=1000),b(15.9,"move",id="cart",x=470,y=1180,arc=-300,rot=540,dur=0.8),
 b(15.9,"spawn",id="p1",prop="tap_part",x=340,y=990),b(15.9,"move",id="p1",x=100,y=1250,arc=-260,rot=300,dur=0.8),
 b(15.9,"spawn",id="p2",prop="cap_part",x=340,y=990),b(15.9,"move",id="p2",x=650,y=1250,arc=-340,rot=200,dur=0.9),
 b(15.9,"walk",who="eng",x=190,dur=0.8,ease="easeOut",face="keep"),b(15.9,"pose",who="eng",pose="fall_back",dur=0.9),
 b(16.9,"pose",who="eng",pose="idle",dur=1),b(16.9,"emote",who="eng",emotion="tired",dur=2),
 say(17.1,"n18",1.2)]
mk("story_04_s04",19.0,{"location":"office_day","view":"kitchen","chars":{"eng":{"x":560,"face":"right"},"narr":NARR,"master":dict(MASTER,hidden=True)}},beats)

# ───── S5 ─────
beats=[b(0,"spawn",id="flood",prop="flood",x=540,y=2185,layer="front"),b(0,"move",id="flood",y=2135,dur=5),
 b(0,"spawn",id="ph",prop="phone",x=520,y=1070),b(0,"hold",id="ph",who="eng",hand="L"),
 b(0,"spawn",id="cart",prop="cartridge",x=560,y=1070),b(0,"hold",id="cart",who="eng",hand="R"),
 b(0,"pose",who="eng",pose="tired",dur=1.8),b(0,"emote",who="eng",emotion="tired",dur=2),
 b(1.9,"release",id="cart",drop=False),b(1.9,"move",id="cart",x=470,y=1090,dur=0.4,arc=-30),
 b(2.0,"release",id="ph",drop=False),b(2.0,"move",id="ph",x=520,y=1090,dur=0.4,arc=-30),
 b(2.5,"pose",who="eng",pose="wipe",dur=1.2),
 b(3.6,"walk",who="eng",x=1000,dur=1.3,face="keep"),
 b(4.9,"location",id="office_day",view="desk",transition="cut"),b(4.9,"remove",id="cart"),b(4.9,"remove",id="ph"),
 b(4.9,"place",who="eng",x=540,face="right"),b(4.9,"pose",who="eng",pose="sit_slump",dur=1.2),
 b(4.9,"emote",who="eng",emotion="tired",dur=3),
 b(5.0,"spawn",id="pd",prop="puddle",x=540,y=1262,layer="front"),
 say(5.3,"n19",2.2),b(6.5,"pose",who="eng",pose="sit",dur=1.5)]
mk("story_04_s05",8.2,{"location":"office_day","view":"kitchen","chars":{"eng":{"x":440,"face":"right"},"narr":NARR}},beats)
# ───── S6 ─────
beats=[*clock(0,180,285),b(0,"hide",who="eng"),
 b(0.1,"move",id="mm",rot=182,dur=1.8),
 *noclock(2.0),b(2.0,"view",id="desk",transition="cut"),b(2.0,"show",who="eng"),
 b(2.0,"pose",who="eng",pose="sit",dur=4),b(2.0,"emote",who="eng",emotion="tired",dur=0.9),
 b(2.0,"portrait",on="eng",dur=1.2,zoom=2.4,angle="side",bg="blur"),
 b(3.2,"portrait",on="eng",dur=2.4,zoom=2.4,angle="q45",bg="blur"),
 b(3.2,"emote",who="eng",emotion="neutral",dur=2.4)]
mk("story_04_s06",6.2,{"location":"office_day","view":"clock","chars":{"eng":{"x":540,"face":"right"},"narr":NARR}},beats)
