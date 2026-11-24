# Собирает docs/props_index.md: локации и предметы из library.json одной строкой каждый
import json,os,re
R=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
L=json.load(open(R+'/library.json'))
def bb(sh,acc):
    for s in sh:
        t=s.get('t')
        if t=='rect': acc+=[(s['x'],s['y']),(s['x']+s['w'],s['y']+s['h'])]
        elif t in('circle','ellipse'):
            rx=s.get('r',s.get('rx',0)); ry=s.get('r',s.get('ry',0)); acc+=[(s['x']-rx,s['y']-ry),(s['x']+rx,s['y']+ry)]
        elif t=='poly': acc+=[tuple(p) for p in s['pts']]
        elif t=='line': acc+=[(s['x1'],s['y1']),(s['x2'],s['y2'])]
        elif t=='g' and not s.get('anim'): bb(s.get('shapes',[]),acc)
out=['# Индекс библиотеки (автогенерация: python3 tools/props_index.py)\n','## Локации\n']
for k,v in L['locations'].items(): out.append(f"- `{k}`"+(f" — ракурсы: {', '.join(v.get('views',{}))}" if v.get('views') else ''))
out.append('\n## Предметы (имя · размер примерно W×H · отметки)\n')
groups={}
for k,v in sorted(L['props'].items()):
    acc=[];bb(v.get('shapes',[]),acc)
    sz=f"{int(max(a for a,b in acc)-min(a for a,b in acc))}×{int(max(b for a,b in acc)-min(b for a,b in acc))}" if acc else '—'
    tag=('up ' if v.get('upright') else '')+('рука' if v.get('grip') and v['grip']!=[0,0] else '')
    groups.setdefault(re.split(r'[_0-9]',k)[0],[]).append(f"`{k}` {sz}{' '+tag.strip() if tag.strip() else ''}")
for g,items in sorted(groups.items()): out.append(f"- **{g}**: "+'; '.join(items))
open(R+'/docs/props_index.md','w').write('\n'.join(out)+'\n'); print(len(L['props']),'props')
