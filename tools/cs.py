import sys,subprocess
from PIL import Image
sc,ts=sys.argv[1],sys.argv[2]
import os
r=subprocess.run(['node','rs.js',sc,os.environ.get('LANGF','lang/story_04.ru.json'),ts,'cs_'+sc],capture_output=True,text=True,cwd='.')
print(r.stdout.strip()[:400],r.stderr.strip()[:300])
L=ts.split(',');ims=[Image.open(f'shots/cs_{sc}_{t}.png').resize((360,640)) for t in L]
o=Image.new('RGB',(360*min(len(L),5),640*((len(L)+4)//5)))
for i,im in enumerate(ims): o.paste(im,((i%5)*360,(i//5)*640))
o.save(f'shots/cs_{sc}.png')
