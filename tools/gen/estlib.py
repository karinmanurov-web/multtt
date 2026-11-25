import json,os
exec(open('s5lib.py').read().split("random.seed(5)")[0])
PR=lib['props']
def pr(n,sh,grip=(0,0),upright=False):
    d={"grip":list(grip),"shapes":sh}
    if upright: d["upright"]=True
    PR[n]=d
# калькулятор (рука держит за низ)
pr('calc',[R(-34,-60,68,100,'#4a4f63',9,OUT,5),R(-24,-50,48,22,'#b8f0c8',4,OUT,3)]+[R(-24+c*17,-18+r*17,13,12,'#e8765a' if (r==2 and c==2) else '#cfd3e0',3,OUT,2) for r in range(3) for c in range(3)],grip=(0,30))
# длинный чек (висит из руки вниз)
pts_l=[(-30,0),(30,0),(30,520)]+[(30-(i%2)*8-((i+1)%2)*0,520+i*0) for i in range(0)]
zig=[(30,520),(18,532),(6,520),(-6,532),(-18,520),(-30,532)]
pr('receipt',[P([(-30,0),(30,0)]+zig,'#fffdf5',OUT,4)]+[L(-20,26+i*34,20-(i%3)*9,26+i*34,'#8a8f9e',4) for i in range(14)]+[L(-20,500,20,500,'#d94a3d',5)],grip=(0,6),upright=True)
# красный карандаш
pr('red_pen',[R(-4,-60,8,90,'#d94a3d',2,OUT,3),P([(-4,30),(4,30),(0,44)],'#f2d6b0',OUT,2)],grip=(0,0))
json.dump(lib,open(LIB,'w'),ensure_ascii=False,indent=2); print('ok est props')
