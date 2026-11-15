"""Chahar's provincial boundaries from the China Postal Atlas sheet for Chahar
(1:900,000; 1930s, after 1928). The red boundary lines are taken by colour,
skeletonised and split into branches at their junctions (ch_branches.py logic,
run on the sheet), then georeferenced to the sheet's own grid: the 114, 115 and
116° E meridians and 40, 41 and 42° N parallels, fitted bilinearly (residuals
under 0.003°). Writes chahar-postal-atlas-lines.json. Not used on the map at present: the lines were judged wrong (October 2026) and taken off pending a check.

Needs chahar-postal-atlas-branches.json (the traced pixel branches) beside this script; the sheet itself is
not kept in the repository.
"""
import numpy as np, json
from shapely.geometry import LineString
mer={114:(211.3,-0.004),115:(521.5,0.00177),116:(832.0,0.00453)}
par={41:(451.75,-0.00255),40:(854.4,-0.0062),42:(48.0,0.0)}
cp=[]
for lon,(a,b) in mer.items():
    for lat,(c,d) in par.items():
        # x=a+b*y ; y=c+d*x
        y=(c+d*a)/(1-d*b); x=a+b*y; cp.append((x,y,lon,lat))
cp=np.array(cp)
def F(px): x,y=(px[:,0]-500)/400,(px[:,1]-500)/400; return np.c_[np.ones(len(x)),x,y,x*y]
C=np.linalg.lstsq(F(cp[:,:2]),cp[:,2:],rcond=None)[0]
print('resid deg', np.round(F(cp[:,:2])@C-cp[:,2:],4).max())
br=[np.array(b,float) for b in json.load(open('chahar-postal-atlas-branches.json'))]
def ll(b): return F(b)@C
def join(*parts):
    out=[]
    for p,rev in parts:
        q=br[p][::-1] if rev else br[p]
        out+= list(q)
    return np.array(out)
lines={'chahar-suiyuan':join((11,True),(10,True)),'suiyuan-shanxi':join((6,False)),'chahar-shanxi':join((7,False)),
'shanxi-hebei':join((1,False)),'chahar-hebei':join((8,False),(4,True),(0,False)),'chahar-jehol':join((2,True),(3,False)),'hebei-jehol':join((9,False),(5,False))}
out={}
for k,v in lines.items():
    l=LineString(ll(v)).simplify(0.006)
    out[k]=[[round(x,3),round(y,3)] for x,y in l.coords]; print(k,len(out[k]),out[k][0],out[k][-1])
json.dump(out,open('chahar-postal-atlas-lines.json','w'))
