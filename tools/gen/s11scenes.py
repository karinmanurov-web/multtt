import json,math
exec(open('s5scenes.py').read().split("CX=440")[0])
LANG={}
def line(k,t): LANG[k]=t
class Q:
    def __init__(s,t=0.4): s.t=t; s.b=[]
    def say(s,key,text,who='narr',gap=0.12):
        LANG[key]=text; t0=s.t; d=len(text)/14+0.1
        s.b.append(b(t0,"say",who=who,line=key,dur=round(d,2))); s.t=t0+d+gap; return t0
    def wait(s,d): s.t+=d
ARC={"type":"arch","x":1500,"face":"left"}
def START(eng=170,bld=900):
    return {"location":"field","chars":{"narr":NARR,"eng":{"x":eng,"face":"right"},"bld":{"x":bld,"face":"left"},"arc":dict(ARC)}}
HX=540
def sp(i,prop,x,y=1250,layer="back",**k): return b(0,"spawn",id=i,prop=prop,x=x,y=y,layer=layer,**k)
def SP(t,i,prop,x,y=1250,layer="back",**k): return b(t,"spawn",id=i,prop=prop,x=x,y=y,layer=layer,**k)
def ballc(th=0,R=250,x0=HX,sc=1.0):               # центр шара при наклоне палочки th° (палочка 380, перекрытие 30)
    d=(380+R*sc-30); a=math.radians(th); return round(x0+d*math.sin(a),1),round(1250-d*math.cos(a),1)
def DUST(t,x,y=1200): return b(t,"fx",kind="dust",x=x,y=y,dur=0.7)
def SIT(t,id,prop,x,y=1250,layer="front",sc=1.0):  # лист/предмет в руке
    return [SP(t,id,prop,x,y,layer,scale=sc)]
def BLACK(t):
    be=[]
    for k in range(5): be.append(b(t+0.18*k,"spawn",id=f"bk{k}",prop="black_s",x=0,y=0,layer="front"))
    be.append(b(t+0.95,"spawn",id="bkf",prop="black_f",x=0,y=0,layer="front")); return be
def BIG(t,id,prop,x=540,y=640,sc=2.6,d=3.0):
    return [SP(t,id,prop,x,y,"back",scale=sc),b(t+d,"remove",id=id)]
# ═════ S1 · Идеальный проект ═════
q=Q(0.4); be=[sp("sh","sk_house",170,1250,"front"),b(0,"hold",id="sh",who="eng"),b(0.05,"pose",who="eng",pose="present"),b(0.1,"emote",who="eng",emotion="happy",dur=14)]
t=q.say("s1n01","Ты наконец получил проект обычного одноэтажного дома.")
be+=[b(t+0.2,"pose",who="bld",pose="idle")]
t=q.say("s1n02","Всё рассчитано: фундамент, стены, крыша.")
be+=[SP(t,"k1","sk_h1",540,650,"back",scale=2.6),b(t+1.0,"remove",id="k1"),SP(t+1.0,"k2","sk_h2",540,650,"back",scale=2.6),b(t+1.9,"remove",id="k2"),SP(t+1.9,"k3","sk_house",540,650,"back",scale=2.6),b(t+3.3,"remove",id="k3"),b(t+0.2,"pose",who="eng",pose="present")]
t=q.say("s1n03","Строитель уже приступил к работе, и впервые за долгое время ничего не предвещает проблем.")
be+=[b(t,"release",id="sh",drop=False),b(t+0.02,"remove",id="sh"),b(t+0.05,"pose",who="eng",pose="hips"),
  SP(t,"sv","shovel",900,1250,"front"),b(t+0.05,"hold",id="sv",who="bld"),b(t+0.3,"pose",who="bld",pose="rake"),
  SP(t,"dp","dirt_pile",700,1250,"back",scale=0.4),b(t+0.4,"move",id="dp",scale=1.0,dur=5.0,ease="linear"),
  SP(t+2.5,"hf","house_f",HX,1250,"back"),DUST(t+2.5,HX,1230)]
mk("story_11_s01",round(q.t+0.6,1),START(),sorted(be,key=lambda x:x['t']))
# ═════ S2 · Небольшие изменения ═════
q=Q(0.3)
be=[sp("hf","fnd_a",HX),sp("dp","dirt_pile",700,scale=1.0),sp("sv","shovel",760,1250,"front"),b(0,"hold",id="sv",who="bld"),b(0.1,"pose",who="bld",pose="rake"),
 b(0,"place",who="eng",x=-120,face="right"),sp("sg","sk_garage",-120,1250,"front"),b(0,"hold",id="sg",who="eng"),b(0.1,"walk",who="eng",x=350,dur=1.6,face="right")]
t=q.say("s2n01","Не прошло и дня, как заказчик захотел гараж.")
be+=[b(t+1.8,"pose",who="eng",pose="present"),b(t+1.8,"emote",who="eng",emotion="worried",dur=2)]
t=q.say("s2n02","Фундамент пришлось расширить.")
be+=[b(t,"remove",id="hf"),SP(t,"hf2","fnd_b",HX),SP(t+0.4,"gf","garage_f",HX+400),DUST(t+0.4,HX+400,1230),b(t+0.4,"pose",who="bld",pose="rake")]
q.t+=0.2
t=q.say("s2d01","Гараж отменили. Но теперь нужна башня.",who="eng")
be+=[b(t,"release",id="sg",drop=False),b(t+0.02,"remove",id="sg"),SP(t,"st","sk_tower",350,1250,"front"),b(t+0.05,"hold",id="st",who="eng"),b(t+0.1,"pose",who="eng",pose="present"),
 b(t+1.2,"remove",id="gf"),SP(t+1.4,"tf","tower_f",HX+250),DUST(t+1.4,HX+250,1230),b(t+1.5,"emote",who="bld",emotion="neutral",dur=2.5)]
t=q.say("s2n03","Строитель перестроил фундамент ещё раз.")
be+=[b(t,"pose",who="bld",pose="rake"),DUST(t+0.5,HX-200,1230),b(t+2.0,"emote",who="bld",emotion="tired",dur=2)]
t=q.say("s2n04","К этому моменту ты уже перестал удивляться.")
be+=[b(t,"release",id="st",drop=True),b(t,"pose",who="eng",pose="arms_cross"),b(t,"emote",who="eng",emotion="neutral",dur=3.5),b(t+0.4,"portrait",on="eng",dur=2.6,zoom=2.6,bg="blur")]
mk("story_11_s02",round(q.t+0.6,1),START(170,820),sorted(be,key=lambda x:x['t']))
# ═════ S3 · Архитекторша ═════
q=Q(0.3)
be=[sp("hf","fnd_a",HX),sp("dp","dirt_pile",720),b(0,"place",who="arc",x=1400,face="left"),sp("sl","sk_lolli",1400,1250,"front"),b(0,"hold",id="sl",who="arc"),b(0.1,"walk",who="arc",x=900,dur=1.8,face="left"),
 b(0,"pose",who="eng",pose="idle")]
t=q.say("s3n01","Но настоящие изменения начались после того, как жена попросила тебя построить дом в форме чупа-чупса.")
be+=[b(t+1.4,"pose",who="arc",pose="present"),b(t+3.0,"remove",id="sl"),SP(t+3.0,"sl2","sk_lolli",540,640,"back",scale=2.8),b(t+3.0,"release",id="sl",drop=False)]
t=q.say("s3n02","Жилой этаж должен был выглядеть как огромная конфета, а держаться всё это — на тонкой палочке.")
be+=[b(t+5.2,"remove",id="sl2")]
t=q.say("s3d01","А на чём он будет стоять?",who="eng"); be+=[b(t,"emote",who="eng",emotion="surprised",dur=2)]
t=q.say("s3d02","На палочке.",who="arc"); be+=[b(t,"pose",who="arc",pose="present"),b(t+0.8,"place",who="bld",x=700,face="left"),b(t+1.0,"emote",who="bld",emotion="worried",dur=2.0)]
t=q.say("s3n03","Ты решил, что подобную конструкцию вполне можно рассчитать.")
be+=[b(t,"pose",who="eng",pose="think")]
t=q.say("s3n04","Строитель решил, что подобную конструкцию вполне можно построить.")
be+=[b(t,"remove",id="hf"),SP(t,"hf3","fnd_a",HX),SP(t+0.3,"st","lp_st1",HX),DUST(t+0.3,HX,1230),b(t+0.5,"pose",who="bld",pose="hammer")]
bx,by=ballc(0,250)
t=q.say("s3n05","И оба ошиблись.")
be+=[SP(t-1.0,"ball","lp_ball",bx,by,"back"),DUST(t-1.0,bx,by+150),b(t,"camera",x=540,y=850,zoom=0.8,dur=1.2),b(t+0.6,"shake",dur=0.8,amp=8)]
mk("story_11_s03",round(q.t+0.8,1),START(170,620),sorted(be,key=lambda x:x['t']))
# ═════ S4 · Геология ═════
q=Q(0.3); bx,by=ballc(0,250)
be=[sp("hf","fnd_a",HX),sp("st","lp_st1",HX),sp("ball","lp_ball",bx,by),b(0,"camera",x=540,y=850,zoom=0.8,dur=0.01),b(0,"place",who="eng",x=230,face="right"),b(0,"place",who="bld",x=800,face="left")]
t=q.say("s4n01","Для начала выяснилось, что грунт совершенно не подходит для такой конструкции.")
tx,ty=ballc(7,250)
be+=[b(t+0.8,"move",id="st",rot=7,dur=2.4),b(t+0.8,"move",id="ball",x=tx,y=ty,dur=2.4),b(t+1.0,"emote",who="eng",emotion="worried",dur=3),b(t+1.2,"fx",kind="sweat",on="eng",anchor="head",dur=1.5)]
t=q.say("s4n02","По отчёту здесь должна была быть скала.")
be+=[SP(t,"cb","clipboard",230,1250,"front"),b(t+0.05,"hold",id="cb",who="eng"),b(t+0.1,"pose",who="eng",pose="present")]
t=q.say("s4n03","На деле Строитель обнаружил болото.")
be+=[SP(t+0.2,"bp","bog_pool",HX,1262,"back"),SP(t+0.3,"bg","bog_chunk",HX+90,1250,"front",scale=0.9),b(t+0.4,"move",id="bg",x=HX+380,y=1170,arc=140,dur=1.2),b(t+0.4,"pose",who="bld",pose="pull"),
 b(t+0.5,"move",id="st",rot=12,dur=1.8),*[b(t+0.5,"move",id="ball",x=ballc(12,250)[0],y=ballc(12,250)[1],dur=1.8)],b(t+1.6,"fx",kind="boom",x=HX+380,y=1180,dur=0.5)]
be+=[b(t+1.8,"spawn",id="snd1",prop="snd_chmok",x=HX+200,y=1050,layer="front"),b(t+3.0,"remove",id="snd1")]
q.t+=0.1
t=q.say("s4d01","Это… не тот отчёт.",who="eng"); be+=[b(t,"emote",who="eng",emotion="shocked",dur=2),b(t+0.2,"pose",who="eng",pose="facepalm")]
t=q.say("s4n04","Пришлось укреплять фундамент, который теперь занимал половину участка.")
be+=[b(t,"remove",id="bp"),b(t,"remove",id="bg"),b(t,"remove",id="hf"),SP(t,"hfc","fnd_c",HX),b(t,"move",id="st",rot=0,dur=0.6),b(t,"move",id="ball",x=ballc(0,250)[0],y=ballc(0,250)[1],dur=0.6),DUST(t+0.3,HX,1230),b(t+0.3,"pose",who="bld",pose="rake"),b(t+0.3,"pose",who="eng",pose="idle")]
t=q.say("s4n05","Палочка пока оставалась тонкой.")
be+=[b(t,"camera",x=540,y=1000,zoom=1.5,dur=1.4)]
mk("story_11_s04",round(q.t+0.6,1),START(230,800),sorted(be,key=lambda x:x['t']))
# ═════ S5 · Размеры ═════
q=Q(0.3); bx,by=ballc(0,250)
be=[sp("hf","fnd_c",HX),sp("st","lp_st1",HX),sp("ball","lp_ball",bx,by),b(0,"camera",x=540,y=850,zoom=0.8,dur=0.01),b(0,"place",who="eng",x=170,face="right"),b(0,"place",who="bld",x=650,face="left"),
 b(0,"place",who="arc",x=960,face="left")]
t=q.say("s5n01","Затем Архитекторша решила немного увеличить конфету.")
be+=[b(t+0.4,"pose",who="arc",pose="point_up")]
bx2,by2=ballc(0,250,HX,1.3)
t=q.say("s5n02","Всего на пару метров.")
be+=[b(t,"move",id="ball",x=bx2,y=by2,scale=1.3,dur=1.4,ease="backSoft"),b(t,"emote",who="eng",emotion="worried",dur=2)]
t=q.say("s5n03","Но теперь шар не помещался на палочке.")
be+=[b(t+0.3,"remove",id="st"),SP(t+0.3,"st1","lp_st_bent",HX,1250,"back"),b(t+0.5,"fx",kind="sweat",on="eng",anchor="head",dur=1.5)]
t=q.say("s5d01","А можно сделать палочку потолще?",who="arc"); be+=[b(t,"pose",who="arc",pose="present")]
t=q.say("s5n04","Пришлось утолщать опору, расширять фундамент и менять расчёты.")
be+=[b(t,"remove",id="st1"),SP(t,"st2","lp_st2",HX),b(t,"pose",who="bld",pose="hammer"),DUST(t,HX,1230),b(t+2.4,"remove",id="st2"),SP(t+2.4,"st3","lp_st3",HX),DUST(t+2.4,HX,1230)]
t=q.say("s5d02","Только не меняй диаметр фундамента!",who="eng")
be+=[b(t,"emote",who="eng",emotion="furious",dur=2),b(t,"pose",who="eng",pose="angry"),b(t+0.5,"remove",id="hf"),SP(t+0.5,"hfx","fnd_cx",HX),b(t+0.5,"spawn",id="k",prop="snd_krak",x=HX-200,y=1100,layer="front"),b(t+2.0,"remove",id="k"),b(t+0.5,"shake",dur=0.5,amp=10)]
t=q.say("s5n05","Строитель уже начал подозревать, что строит не дом, а памятник твоим ошибкам.")
be+=[b(t,"pose",who="eng",pose="idle"),b(t+0.2,"emote",who="bld",emotion="tired",dur=3),b(t+0.4,"portrait",on="bld",dur=2.6,zoom=2.6,bg="blur")]
mk("story_11_s05",round(q.t+0.6,1),START(170,640),sorted(be,key=lambda x:x['t']))
# ═════ S6 · Парящий дом ═════
q=Q(0.3); bx,by=ballc(0,250,HX,1.3)
be=[sp("hf","fnd_cx",HX),sp("st","lp_st3",HX),sp("ball","lp_ball",bx,by,scale=1.3),b(0,"camera",x=540,y=850,zoom=0.8,dur=0.01),b(0,"place",who="eng",x=200,face="right"),b(0,"place",who="bld",x=650,face="left"),b(0,"place",who="arc",x=1400,face="left"),
 sp("sf","sk_float",1400,1250,"front"),b(0,"hold",id="sf",who="arc"),b(0.1,"walk",who="arc",x=960,dur=1.6,face="left")]
t=q.say("s6n01","Когда конструкция наконец обрела устойчивость, Архитекторша захотела, чтобы дом выглядел парящим над землёй.")
be+=[b(t+1.2,"pose",who="arc",pose="present"),b(t+3.0,"release",id="sf",drop=False),b(t+3.0,"remove",id="sf"),SP(t+3.0,"sfb","sk_float",540,620,"back",scale=2.8),b(t+8.0,"remove",id="sfb")]
t=q.say("s6d01","Это визуализация.",who="eng"); be+=[b(t,"pose",who="eng",pose="present")]
t=q.say("s6d02","А я думала, это проект.",who="arc"); be+=[b(t,"emote",who="arc",emotion="surprised",dur=1.5)]
t=q.say("s6n02","Однако Строитель уже закрепил дом на кране и начал поднимать его.")
tb=by-250*1.3
be+=[b(t,"camera",x=620,y=760,zoom=0.62,dur=1.2),
 SP(t,"cr","crane_tw",1800,1250,"back"),b(t+0.1,"move",id="cr",x=1000,dur=1.4),SP(t,"cj","crane_jib",1800,-250,"back"),b(t+0.1,"move",id="cj",x=1000,dur=1.4),
 SP(t+1.6,"cc","crane_car",HX,-250,"front"),SP(t+1.6,"cab","crane_cab",HX,tb,"front"),
 b(t+2.4,"pose",who="bld",pose="pull"),
 b(t+3.0,"move",id="cab",y=tb-100,dur=2.2),b(t+3.0,"move",id="ball",y=by-100,dur=2.2),b(t+3.0,"move",id="st",y=1150,dur=2.2),
 SP(t+3.0,"shd","sun_ray",HX,1262,"back",scale=0.01)]
t=q.say("s6n03","В какой-то момент стало ясно, что визуализация была единственной частью проекта, которая действительно работала.")
be+=[b(t+0.5,"emote",who="eng",emotion="shocked",dur=3),b(t+0.5,"pose",who="eng",pose="facepalm"),b(t+0.8,"emote",who="arc",emotion="happy",dur=5)]
mk("story_11_s06",round(q.t+0.6,1),START(200,720),sorted(be,key=lambda x:x['t']))
# ═════ S7 · Сроки ═════
q=Q(0.3); bx,by=ballc(0,250,HX,1.3); tb=by-250*1.3
be=[sp("hf","fnd_cx",HX),sp("st","lp_st3",HX,1150),sp("ball","lp_ball",bx,by-100,scale=1.3),sp("cr","crane_tw",1000),sp("cj","crane_jib",1000,-250),sp("cc","crane_car",HX,-250,"front"),sp("cab","crane_cab",HX,tb-100,"front"),
 b(0,"camera",x=620,y=800,zoom=0.7,dur=0.01),b(0,"place",who="eng",x=240,face="right"),b(0,"place",who="bld",x=780,face="left"),b(0,"place",who="arc",x=1500,face="left")]
t=q.say("s7n01","К этому времени стройка отставала от графика на несколько недель.")
be+=[SP(t+0.3,"cw","cal_w",110,700,"back",scale=1.6),b(t+0.3,"pose",who="eng",pose="point_up"),b(t+0.4,"emote",who="eng",emotion="worried",dur=3),b(t+3.5,"remove",id="cw")]
t=q.say("s7n02","Ты решил ускорить работу и составил новый план.")
be+=[b(t,"pose",who="eng",pose="write"),SP(t+2.4,"pl","sk_house",240,1250,"front"),b(t+2.45,"hold",id="pl",who="eng")]
t=q.t; q.t+=1.6; LANG["s7n03"]="Строитель получил план."
be+=[b(t,"walk",who="eng",x=560,dur=1.2),b(t+1.0,"release",id="pl",drop=False),b(t+1.02,"remove",id="pl"),SP(t+1.0,"pl2","sk_house",780,1250,"front"),b(t+1.05,"hold",id="pl2",who="bld")]
t=q.say("s7d01","Вчера вы сказали, что дом будет на палочке.",who="bld"); be+=[b(t,"emote",who="bld",emotion="neutral",dur=2.5)]
t=q.say("s7d02","Я не мог знать, что палочка будет такой сложной.",who="eng"); be+=[b(t,"pose",who="eng",pose="shrug")]
t=q.say("s7n04","Через минуту Архитекторша принесла ещё один.")
be+=[b(t,"place",who="arc",x=1400,face="left"),SP(t,"sp3","sk_lolli2",1400,1250,"front"),b(t+0.05,"hold",id="sp3",who="arc"),b(t+0.1,"walk",who="arc",x=930,dur=1.8,face="left"),b(t+1.9,"pose",who="arc",pose="present")]
t=q.say("s7n05","Теперь дом должен был быть выше, легче, шире и, желательно, дешевле.")
be+=[b(t,"place",who="eng",x=500,face="right"),b(t+0.3,"emote",who="eng",emotion="shocked",dur=3),b(t+0.5,"emote",who="bld",emotion="shocked",dur=3)]
t=q.say("s7n06","Срок сдачи остался прежним.")
be+=[b(t,"portrait",on="eng",dur=2.2,zoom=2.6,bg="blur"),b(t,"emote",who="eng",emotion="furious",dur=2.2)]
mk("story_11_s07",round(q.t+0.6,1),START(240,780),sorted(be,key=lambda x:x['t']))
# ═════ S8 · Последнее изменение ═════
q=Q(0.3); bx,by=ballc(0,250,HX,1.3)
be=[sp("hf","fnd_cx",HX),sp("st","lp_st3",HX),sp("ball","lp_ball",bx,by,scale=1.3),b(0,"camera",x=540,y=850,zoom=0.8,dur=0.01),b(0,"place",who="eng",x=200,face="right"),b(0,"place",who="bld",x=650,face="left"),b(0,"place",who="arc",x=960,face="left"),
 sp("sp","sk_spin",930,1250,"front"),b(0,"hold",id="sp",who="arc"),b(0.05,"pose",who="arc",pose="present")]
t=q.say("s8n01","Когда казалось, что проект наконец завершён, Архитекторша решила добавить вращение.")
be+=[b(t+2.0,"remove",id="sp")]
be+=[SP(t+2.0,"spb","sk_spin",540,620,"back",scale=2.8)]
t=q.say("s8n02","Дом должен был крутиться, как настоящая конфета.")
be+=[b(t+2.0,"remove",id="spb")]
t=q.say("s8d01","Для вращения нужна ось.",who="eng"); be+=[b(t,"pose",who="eng",pose="point")]
t=q.say("s8d02","Для оси нужен фундамент.",who="bld"); be+=[b(t,"pose",who="bld",pose="point")]
t=q.say("s8d03","Для фундамента нужна геология.",who="eng"); be+=[b(t,"emote",who="eng",emotion="worried",dur=2)]
t=q.say("s8d04","А можно, чтобы он ещё и светился?",who="arc"); be+=[b(t,"pose",who="arc",pose="present"),b(t,"emote",who="arc",emotion="happy",dur=2.5)]
t=q.say("s8n03","Строитель достал гирлянду.")
be+=[SP(t,"gg","garland_g",760,1250,"front"),b(t+0.05,"hold",id="gg",who="bld"),b(t+0.2,"pose",who="bld",pose="present")]
t=q.say("s8d05","Нет. Нет, это уже не предусмотрено.",who="eng"); be+=[b(t,"pose",who="eng",pose="hands_up"),b(t,"emote",who="eng",emotion="furious",dur=2.5)]
t=q.say("s8n04","Ты понял, что расчёты больше не имеют значения.")
be+=[b(t,"release",id="gg",drop=True),b(t,"remove",id="ball"),SP(t,"gw","glow_ball",bx,by,"back",scale=1.3),SP(t,"ball2","lp_ball_spin",bx,by,"back",scale=1.3),SP(t,"gl","garland",bx,by,"back",scale=1.3),
 b(t,"pose",who="eng",pose="facepalm"),b(t+0.2,"camera",x=540,y=900,zoom=0.8,dur=0.01)]
mk("story_11_s08",round(q.t+0.8,1),START(200,730),sorted(be,key=lambda x:x['t']))
# ═════ S9 · Результат ═════
q=Q(0.3); bx,by=ballc(0,250,HX,1.3)
be=[sp("hf","fnd_cx",HX),sp("st","lp_st3",HX),sp("gw","glow_ball",bx,by,scale=1.3),sp("ball2","lp_ball_spin",bx,by,scale=1.3),sp("gl","garland",bx,by,scale=1.3),
 b(0,"camera",x=540,y=850,zoom=0.8,dur=0.01),b(0,"place",who="eng",x=200,face="right"),b(0,"place",who="bld",x=650,face="left"),b(0,"place",who="arc",x=970,face="left"),b(0,"emote",who="eng",emotion="worried",dur=1.5)]
t=q.say("s9n01","Дом начал вращаться.")
be+=[b(t,"shake",dur=1.0,amp=4)]
bx2,by2=ballc(0,250,HX,1.3)
t=q.say("s9n02","Палочка согнулась.")
be+=[b(t,"remove",id="st"),SP(t,"stb","lp_st_bent",HX),b(t,"move",id="ball2",x=bx2+120,y=by2+40,rot=14,dur=1.2),b(t,"move",id="gl",x=bx2+120,y=by2+40,dur=1.2),b(t,"move",id="gw",x=bx2+120,y=by2+40,dur=1.2)]
t=q.say("s9n03","Фундамент треснул.")
be+=[b(t,"spawn",id="k",prop="snd_krak",x=HX-220,y=1100,layer="front"),b(t+1.4,"remove",id="k"),b(t,"shake",dur=0.8,amp=12),DUST(t,HX,1230)]
t=q.say("s9n04","И огромный чупа-чупс медленно покатился по строительной площадке.")
be+=[b(t,"remove",id="ball2"),b(t,"remove",id="gl"),b(t,"remove",id="gw"),SP(t,"bb","lp_ball",bx2+120,by2+40,"back",scale=1.3),
 b(t+0.1,"move",id="bb",x=1700,y=1250-250*1.3,rot=720,dur=6.0,ease="easeIn"),b(t+0.4,"move",id="stb",rot=82,dur=1.5),b(t+1.6,"fx",kind="dust",x=HX,y=1230,dur=0.8),
 b(t+0.5,"pose",who="eng",pose="shrug"),b(t+1.0,"fx",kind="dust",on="eng",anchor="body",dur=1.2),b(t+1.0,"fx",kind="dust",on="bld",anchor="body",dur=1.2)]
t=q.say("s9n05","Ты стоял рядом со Строителем, покрытый строительной пылью, и пытался понять, на каком этапе всё пошло не так.")
be+=[b(t,"camera",x=560,y=1000,zoom=1.05,dur=1.2),b(t+0.2,"walk",who="eng",x=330,dur=1.4,face="right"),b(t+0.3,"walk",who="bld",x=570,dur=1.2,face="left"),b(t+0.3,"walk",who="arc",x=830,dur=1.4,face="left"),b(t+1.4,"emote",who="eng",emotion="neutral",dur=5),b(t+1.4,"pose",who="eng",pose="think"),b(t+1.6,"pose",who="bld",pose="arms_cross")]
t=q.say("s9d01","Ну… зато получилось необычно.",who="arc"); be+=[b(t,"emote",who="arc",emotion="happy",dur=2)]
t=q.say("s9d02","Мы построили не дом.",who="eng"); be+=[b(t,"emote",who="eng",emotion="sad",dur=1.8)]
t=q.say("s9d03","Мы построили замечание к проекту.",who="bld"); be+=[b(t,"emote",who="bld",emotion="neutral",dur=2.5)]
t=q.say("s9n06","Архитекторша тем временем уже подготовила новый проект.")
be+=[SP(t,"sq","sk_pool",940,1250,"front"),b(t+0.05,"hold",id="sq",who="arc"),b(t+0.2,"pose",who="arc",pose="present")]
t=q.say("s9d04","А теперь давайте обсудим бассейн.",who="arc")
be+=[b(t,"emote",who="arc",emotion="happy",dur=2.2)]
t=q.say("s9n07","На этот раз — дом с бассейном.")
be+=[b(t,"camera",x=540,y=960,zoom=1.0,dur=0.8),SP(t+0.2,"sqb","sk_pool_big",540,700,"back",scale=2.2)]
t=q.say("s9n08","И, кажется, бассейн должен был быть на крыше.")
be+=[b(t,"camera",x=540,y=780,zoom=1.15,dur=2.5),b(t+0.8,"emote",who="eng",emotion="shocked",dur=3),b(t+0.8,"pose",who="eng",pose="facepalm"),*BLACK(t+3.4)]
mk("story_11_s09",round(q.t+3.2,1),START(170,640),sorted(be,key=lambda x:x['t']))
for _k,_v in {'snd_krak':'КРАК!','snd_bum':'БУМ!','snd_shlep':'Шлёп!','snd_trr':'Тр-р-р…','snd_chmok':'Чвяк!'}.items(): LANG[_k]=_v
json.dump({"lang":"ru","cps":14,"lines":LANG},open(D+'lang/story_11.ru.json','w'),ensure_ascii=False,indent=2)
print('ok',len(LANG))
