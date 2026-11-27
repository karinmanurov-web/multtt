import os,json
exec(open('s5scenes.py').read().split("CX=440")[0])
LANG={"snd_ring":"Дзынь-дзынь!","snd_zzz":"Z z z","snd_tap":"Тук-тук-тук","snd_dzin":"Дзынь."}
PJ=dict(shirt="#6f86c4",sleeve="#6f86c4",pants="#6f86c4",shoe="#c98a4a",pj=True,stripe="#cfdcff")
class S:
    def __init__(s,id,chars=None):
        s.id=id; s.b=[]; s.prev=None; s.chars=chars or {}; s.n=0
    def vo(s,key,text,gap=0.5,t=None):
        LANG[key]=text; bt={"do":"say","who":"narr","line":key}
        if s.prev is None: bt["t"]=0.5 if t is None else t
        else: bt.update(after=s.prev,gap=gap)
        s.b.append(bt); s.prev=key; return key
    def t0(s,t,do,**k): s.b.append({"t":t,"do":do,**k})
    def w(s,key,do,g=0,**k): s.b.append({"do":do,"with":key,"gap":g,**k})
    def uid(s): s.n+=1; return f"u{s.n}"
    def hop(s,key,g,x0,x1,y,hops=7,prop="px_run"):
        """Пиксель прибегает прыжками; в конце садится (px_sit с новым id). Возвращает id сидящего."""
        i=s.uid(); j=s.uid(); step=(x1-x0)/hops; d=0.13
        s.w(key,"spawn",g,id=i,prop=prop,x=x0,y=y,layer="front",scale=0.9)
        for k in range(hops):
            gg=g+0.02+k*2*d
            s.w(key,"move",gg,id=i,x=x0+step*(k+0.5),y=y-70,dur=d,ease="easeOut"); s.w(key,"move",gg+d,id=i,x=x0+step*(k+1),y=y,dur=d,ease="easeIn")
        gend=g+0.02+hops*2*d
        s.w(key,"remove",gend,id=i); s.w(key,"spawn",gend,id=j,prop="px_sit",x=x1,y=y,layer="front",scale=0.9)
        return j
    def done(s,loc="cottage2",tail=1.0,eng=None,start_eng=None):
        s.b.append({"do":"emote","after":s.prev,"gap":0,"who":"eng","emotion":"neutral","dur":tail})
        c={"narr":NARR,"eng":start_eng or {"x":300,"face":"right"}}; c.update(s.chars)
        json.dump({"id":s.id,"start":{"location":loc,"view":"main","chars":c},"defs":{},"beats":s.b},open(D+f'scenes/{s.id}.json','w'),ensure_ascii=False,indent=1)
def CAM(s,x,y,z,t=0): s.t0(t,"camera",x=x,y=y,zoom=z,dur=0.01)
F2=-560
def INS(s,key,g,id,prop,dur,cx,cy,z):
    s.w(key,"inset",g,id=id,prop=prop,x=cx,y=round(cy+(400-960)/z),scale=0.8,dur=dur)
def RING(s,key,g,x,y):
    s.w(key,"spawn",g,id=s.uid(),prop="snd_ring",x=x,y=y,layer="front",scale=1.0) if False else None
    i=s.uid(); s.w(key,"spawn",g,id=i,prop="snd_ring",x=x,y=y,layer="front"); s.w(key,"remove",g+1.6,id=i); s.w(key,"shake",g,dur=0.8,amp=5)
# ═════ S1 · Пробуждение (07:00) ═════
CX,CY,Z=432,768,1.25
s=S("story_14_s01"); CAM(s,CX,CY,Z)
s.t0(0,"outfit",who="eng",**PJ)
s.t0(0,"spawn",id="bl",prop="blanket",x=160,y=612,layer="front"); s.t0(0,"spawn",id="pl",prop="pillow",x=140,y=600,layer="back")
s.t0(0,"spawn",id="nt_l",prop="lamp_off",x=575,y=616,layer="back",scale=0.8)
s.t0(0,"place",who="eng",x=450,y=-690,face="right"); s.t0(0,"pose",who="eng",pose="lie")
n=s.vo("n01","Ты просыпаешься и, ещё не открыв глаза, тянешься к телефону.")
s.w(n,"remove",1.2,id="bl"); s.w(n,"place",1.3,who="eng",x=330,y=F2,face="right"); s.w(n,"pose",1.3,who="eng",pose="type"); s.w(n,"give",1.4,who="eng",id="ph",prop="phone",hand="L")
n=s.vo("n02","Первое сообщение за день. Помощник прибегает мгновенно и садится рядом.")
px=s.hop(n,0.6,1150,540,690,hops=7)
n=s.vo("n03","Ты пишешь, пишешь, пишешь... и упираешься в лимит.")
INS(s,n,0.2,"ch","chat_ok",1.7,CX,CY,Z); INS(s,n,2.0,"lk","chat_lock",2.2,CX,CY,Z); s.w(n,"shake",2.0,dur=0.5,amp=6)
n=s.vo("n04","Помощник исчезает так же мгновенно.")
s.w(n,"remove",0.3,id=px); s.w(n,"emote",0.4,who="eng",emotion="shocked",dur=2.5)
n=s.vo("n05","Ничего страшного. Ты ставишь таймер на пять часов, чтобы вернуться минута в минуту.")
s.w(n,"pose",0.2,who="eng",pose="point"); INS(s,n,0.8,"tm","tm_5",3.8,CX,CY,Z); s.w(n,"emote",0.8,who="eng",emotion="smug",dur=3.5)
s.done(start_eng={"x":450,"face":"right"})
# ═════ S2 · Обед (12:00) ═════
CX,CY,Z=432,1010,1.25
s=S("story_14_s02"); CAM(s,CX,CY,Z)
s.t0(0,"spawn",id="tb",prop="k_table",x=420,y=1250,layer="back"); s.t0(0,"spawn",id="ch",prop="k_chair",x=300,y=1250,layer="back")
s.t0(0,"spawn",id="bw",prop="bowl",x=500,y=1120,layer="front"); s.t0(0,"spawn",id="phn",prop="phone",x=440,y=1105,layer="front",rot=80,scale=0.8)
s.t0(0,"place",who="eng",x=350,y=0,face="right"); s.t0(0,"pose",who="eng",pose="sit"); s.t0(0,"give",who="eng",id="sp",prop="spoon")
n=s.vo("n06","Пять часов проходят в ожидании. Таймер звонит прямо за обедом.")
RING(s,n,2.0,420,900); s.w(n,"emote",2.0,who="eng",emotion="surprised",dur=2.0)
n=s.vo("n07","Помощник прибегает мгновенно, и ты пишешь, не выпуская ложку.")
px=s.hop(n,0.4,-100,600,1250,hops=6); s.w(n,"pose",0.6,who="eng",pose="sit_type"); s.w(n,"emote",0.6,who="eng",emotion="happy",dur=3)
n=s.vo("n08","Суп остывает, а лимит заканчивается ещё быстрее.")
INS(s,n,0.8,"lk","chat_lock",2.4,CX,CY,Z); s.w(n,"shake",0.8,dur=0.5,amp=6)
n=s.vo("n09","Помощник исчезает, и ты наконец доедаешь холодный суп.")
s.w(n,"remove",0.3,id=px); s.w(n,"pose",0.4,who="eng",pose="sit_slump"); s.w(n,"emote",0.4,who="eng",emotion="tired",dur=3)
n=s.vo("n10","Таймер. Ещё пять часов.")
INS(s,n,0.2,"tm","tm_5",2.4,CX,CY,Z); s.w(n,"pose",0.3,who="eng",pose="sit")
s.done(start_eng={"x":350,"face":"right"})
# ═════ S3 · Разговор (17:00) ═════
CX,CY,Z=540,960,1.0
s=S("story_14_s03",{"bld":{"x":1350,"face":"left"}}); CAM(s,CX,CY,Z)
s.t0(0,"place",who="eng",x=650,y=0,face="right"); s.t0(0,"pose",who="eng",pose="idle")
n=s.vo("n11","К вечеру к тебе заходит Строитель — обсудить работу.")
s.w(n,"walk",0.3,who="bld",x=900,y=0,dur=2.2,face="left"); s.w(n,"pose",2.6,who="bld",pose="present")
n=s.vo("n12","Но тут звенит таймер.")
RING(s,n,0.2,650,760); s.w(n,"emote",0.2,who="eng",emotion="surprised",dur=1.5); s.w(n,"give",0.8,who="eng",id="ph",prop="phone",hand="L"); s.w(n,"pose",0.8,who="eng",pose="teeth_type")
n=s.vo("n13","Помощник прибегает мгновенно, а ты киваешь Строителю и одновременно пишешь.")
px=s.hop(n,0.4,-100,420,1250,hops=5,prop="px_run") ; s.w(n,"emote",0.4,who="eng",emotion="happy",dur=3); s.w(n,"pose",0.4,who="bld",pose="point",dur=2.5)
n=s.vo("n14","Строитель замечает, что его не слушают.")
s.w(n,"pose",0.3,who="bld",pose="arms_cross"); s.w(n,"emote",0.3,who="bld",emotion="angry",dur=2.6)
n=s.vo("n15","Лимит заканчивается ровно в тот момент, когда Строитель заканчивает говорить.")
INS(s,n,0.6,"lk","chat_lock",2.2,CX,CY,Z); s.w(n,"remove",0.7,id=px); s.w(n,"stow",0.9,id="ph"); s.w(n,"pose",0.9,who="eng",pose="idle"); s.w(n,"emote",1.0,who="eng",emotion="smug",dur=3)
n=s.vo("n16","Ты ставишь таймер. Строитель только вздыхает.")
INS(s,n,0.2,"tm","tm_5",2.4,CX,CY,Z); s.w(n,"emote",0.4,who="bld",emotion="tired",dur=3)
s.done(start_eng={"x":650,"face":"right"})
# ═════ S4 · Зубы (22:00) ═════
CX,CY,Z=648,768,1.25
s=S("story_14_s04"); CAM(s,CX,CY,Z)
s.t0(0,"place",who="eng",x=800,y=F2,face="left"); s.t0(0,"pose",who="eng",pose="teeth"); s.t0(0,"give",who="eng",id="br",prop="brush_h",hand="R")
n=s.vo("n17","Перед сном ты идёшь чистить зубы.")
s.w(n,"emote",0.3,who="eng",emotion="tired",dur=3)
n=s.vo("n18","Таймер звонит. Помощник тут как тут.")
RING(s,n,0.2,930,300); px=s.hop(n,0.5,1250,1000,F2+1250,hops=4); s.w(n,"give",0.8,who="eng",id="ph",prop="phone",hand="L"); s.w(n,"pose",0.8,who="eng",pose="teeth_type"); s.w(n,"emote",0.8,who="eng",emotion="surprised",dur=2)
n=s.vo("n19","Ты пишешь одной рукой, а другой чистишь зубы.")
s.w(n,"emote",0.2,who="eng",emotion="happy",dur=3.5)
n=s.vo("n20","Лимит. Помощник исчезает. Ты наконец полощешь рот.")
INS(s,n,0.2,"lk","chat_lock",2.0,CX,CY,Z); s.w(n,"remove",0.3,id=px); s.w(n,"stow",1.0,id="ph"); s.w(n,"pose",1.0,who="eng",pose="teeth")
n=s.vo("n21","Ставишь таймер и ложишься спать.")
INS(s,n,0.2,"tm","tm_5",2.4,CX,CY,Z); s.w(n,"stow",0.2,id="br"); s.w(n,"pose",0.2,who="eng",pose="idle")
s.done(start_eng={"x":800,"face":"left"})
# ═════ S5 · Ночь (03:00) ═════
CX,CY,Z=432,768,1.25
s=S("story_14_s05"); CAM(s,CX,CY,Z)
s.t0(0,"outfit",who="eng",**PJ)
s.t0(0,"spawn",id="no",prop="night_out",x=0,y=0,layer="back"); s.t0(0,"spawn",id="mn",prop="moon",x=900,y=120,layer="back",scale=0.6); s.t0(0,"spawn",id="nd",prop="night_dim",x=0,y=0,layer="back")
s.t0(0,"spawn",id="bl",prop="blanket",x=160,y=612,layer="front"); s.t0(0,"spawn",id="pl",prop="pillow",x=140,y=600,layer="back")
s.t0(0,"spawn",id="al",prop="alarm",x=575,y=616,layer="back",scale=0.8)
s.t0(0,"place",who="eng",x=450,y=-690,face="right"); s.t0(0,"pose",who="eng",pose="lie")
n=s.vo("n22","В три часа ночи звонит будильник.")
RING(s,n,0.6,430,330)
n=s.vo("n23","Лимит сбросился, а значит, спать некогда.")
s.w(n,"remove",0.4,id="bl"); s.w(n,"place",0.5,who="eng",x=330,y=F2,face="right"); s.w(n,"pose",0.5,who="eng",pose="tired"); s.w(n,"emote",0.5,who="eng",emotion="tired",dur=3); s.w(n,"remove",0.5,id="al")
n=s.vo("n24","Помощник уже сидит рядом, а ты пишешь сонными пальцами.")
px=s.hop(n,0.2,1150,540,690,hops=7); s.w(n,"give",0.3,who="eng",id="ph",prop="phone",hand="L"); s.w(n,"pose",0.4,who="eng",pose="type")
n=s.vo("n25","Лимит. Помощник исчезает. Ты ставишь таймер и снова засыпаешь.")
INS(s,n,0.2,"lk","chat_lock",1.8,CX,CY,Z); s.w(n,"remove",0.3,id=px); s.w(n,"stow",1.0,id="ph")
s.w(n,"place",1.6,who="eng",x=450,y=-690,face="right"); s.w(n,"pose",1.6,who="eng",pose="lie"); s.w(n,"spawn",1.6,id="bl2",prop="blanket",x=160,y=612,layer="front")
s.w(n,"spawn",2.0,id="zz",prop="snd_zzz",x=170,y=380,layer="front")
n=s.vo("n26","Зато ты ни разу не пропустил своё окно.")
s.w(n,"remove",0.2,id="zz"); INS(s,n,0.2,"tm","tm_5",2.2,CX,CY,Z)
n=s.vo("n27","А утром всё начнётся заново.")
s.w(n,"blackout",1.4)
s.done(tail=2.5,start_eng={"x":450,"face":"right"})
json.dump({"lang":"ru","cps":14,"lines":LANG},open(D+'lang/story_14.ru.json','w'),ensure_ascii=False,indent=2)
print('ok',len(LANG))
