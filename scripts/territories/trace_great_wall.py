"""Trace the Great Wall from the Nakamura (1941) map, into great_wall_nakamura.json
(copy it to src/data/great-wall.json).

Run fit_nakamura.py first; needs the scan as nakamura.png beside this script.
The map draws the Wall as a heavy line with white dots. Dots are detected on
the heavy lines and the dotted stretches kept (gaps under about 15 px
bridged). Along the Ordos the dots are faint, but the map runs the Wall on
Mengjiang's state border there, so that border is followed from the Ningxia
corner to North Shansi. The Japanese map 蒙疆地域圖 draws the same line.
"""
import numpy as np, cv2, json, networkx as nx
from skimage.morphology import skeletonize
from scipy.spatial import cKDTree
from pyproj import Proj
from shapely.geometry import LineString
P=Proj(proj='lcc',lat_1=37,lat_2=47,lat_0=43,lon_0=113,ellps='WGS84')
C=np.load('nak_coef.npy')
def feats(p): x,y=p[:,0]/100,p[:,1]/100; return np.c_[np.ones(len(x)),x,y,x*x,x*y,y*y]
S=4
im=cv2.imread('nakamura.png'); g=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
big=cv2.resize(g,None,fx=S,fy=S,interpolation=cv2.INTER_CUBIC).astype(int)
dark=(big<90).astype(np.uint8)
# white dots sitting on dark lines (relaxed)
bright=(big>120).astype(np.uint8)
n,lab,st,cen=cv2.connectedComponentsWithStats(bright,8)
darkfrac=cv2.blur(dark.astype(np.float32),(17,17))
dots=np.array([cen[i] for i in range(1,n) if 3<=st[i,4]<=70 and st[i,2]<=11 and st[i,3]<=11 and darkfrac[int(cen[i][1]),int(cen[i][0])]>0.38])
# drop the legend box
dots=dots[~((dots[:,0]<395*S/2)&(dots[:,1]<430*S/2))]
# thick lines = dark after closing the dots, then opening (line width ~4-5 px at 1x)
closed=cv2.morphologyEx(dark,cv2.MORPH_CLOSE,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(9,9)))
thick=cv2.morphologyEx(closed,cv2.MORPH_OPEN,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(9,9)))
sk=skeletonize(thick.astype(bool))
ys,xs=np.nonzero(sk); pts=np.c_[xs,ys]
td=cKDTree(dots); dd,_=td.query(pts)
near=dd<10
# keep skeleton pixels near dots, then fill gaps up to 60 px (15 px at 1x) along the skeleton graph
G=nx.Graph(); idx={tuple(p):k for k,p in enumerate(pts)}
for k,(x,y) in enumerate(pts):
    for dx in(-1,0,1):
        for dy in(-1,0,1):
            j=idx.get((x+dx,y+dy))
            if j is not None and j>k: G.add_edge(k,j,weight=float(np.hypot(dx,dy)))
seeds=set(np.nonzero(near)[0].tolist())
keep=set(seeds)
for s in list(seeds):
    if s not in G: continue
    lengths,paths=nx.single_source_dijkstra(G,s,cutoff=70)
    for t,l in lengths.items():
        if t in seeds and t!=s: keep.update(paths[t])
H=G.subgraph(keep).copy()
lines=[]
for comp in nx.connected_components(H):
    if len(comp)<80: continue
    T=H.subgraph(comp).copy()
    while T.number_of_nodes()>80:
        a=next(iter(T.nodes)); dist=nx.single_source_dijkstra_path_length(T,a); b=max(dist,key=dist.get)
        dist2,paths=nx.single_source_dijkstra(T,b); c=max(dist2,key=dist2.get)
        if dist2[c]<80: break
        path=paths[c]; lines.append(pts[path]/S); T.remove_nodes_from(path)
        T.remove_nodes_from([n for n in list(T.nodes) if T.degree(n)==0])
vis=cv2.resize(im,None,fx=2,fy=2)
cols=[(0,0,255),(0,160,0),(255,0,0),(0,140,255),(200,0,200),(0,200,200),(120,60,0),(60,0,120)]
for k,l in enumerate(lines):
    for a,b in zip(l[:-1:3],l[3::3]): cv2.line(vis,(int(a[0]*2),int(a[1]*2)),(int(b[0]*2),int(b[1]*2)),cols[k%8],3)
    cv2.putText(vis,str(k),(int(l[0][0]*2),int(l[0][1]*2)),cv2.FONT_HERSHEY_SIMPLEX,0.7,cols[k%8],2)
cv2.imwrite('wall2_vis.png',vis)
out=[]
for l in lines:
    ls=LineString(feats(l)@C).simplify(1000); lon,lat=P(*np.array(ls.coords).T,inverse=True)
    out.append([[round(float(a),3),round(float(b),3)] for a,b in zip(lon,lat)])
json.dump({'greatWall':out},open('great_wall_nakamura.json','w'),separators=(',',':'))
for k,o in enumerate(out): print(k,len(o),o[0],o[-1])
print('dots',len(dots))

# ---- Ordos stretch: the wall runs on Mengjiang's southern border from the Ningxia corner to the
# Yellow River and on to North Shansi; its dots are faint here, so follow the border line itself.
def nearest_node(px):
    d,k=cKDTree(pts).query(np.array(px)*S); return int(k)
a=nearest_node((101,466)); b=nearest_node((298,414))
path=nx.shortest_path(G,a,b,weight='weight')
ordos=pts[path]/S
print('ordos path px',len(path), ordos[0], ordos[len(ordos)//2], ordos[-1])
ls=LineString(feats(ordos)@C).simplify(1000); lon,lat=P(*np.array(ls.coords).T,inverse=True)
out=[o for o,l in zip(out,lines) if not (l[:,0].max()<300 and l[:,1].min()>400)]   # drop the Ordos fragments
out.append([[round(float(a),3),round(float(b),3)] for a,b in zip(lon,lat)])
json.dump({'greatWall':out},open('great_wall_nakamura.json','w'),separators=(',',':'))
for a_,b_ in zip(ordos[:-1:3],ordos[3::3]): cv2.line(vis,(int(a_[0]*2),int(a_[1]*2)),(int(b_[0]*2),int(b_[1]*2)),(255,0,255),3)
cv2.imwrite('wall2_vis.png',vis)
print('final lines',len(out),[len(o) for o in out])
