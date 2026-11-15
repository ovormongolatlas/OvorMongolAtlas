"""Trace state territories from Narangoa & Cribb's 1935-1940 map into
an intermediate file (nc-1935-1940-polys.json) for combine_territories.py.

Source map: Li Narangoa and Robert Cribb, Historical Atlas of Northeast Asia,
1590-2010 (Columbia University Press, 2014), the 1935-1940 map, as reproduced
in Dotno Dashdorj Pount, "Immigrants of Inner Mongolia" (MA dissertation,
2015), Map 2, p. 19. The scan itself is not kept in this repository (the atlas
is in copyright); put it beside this script as SCAN to rerun.

Method:
 1. Classify the map's fill colours (dark blue = Prince De's Mongol Military
    Government, 1936; mid blue = additional territory ruled by the Mongol
    Leagues Allied Autonomous Government, 1937; pale blue = territory it
    claimed; orange/green = Manchukuo), close small gaps left by labels and
    drawn lines, and take each area's outline.
 2. Georeference by rubber-sheeting (piecewise affine on a Delaunay mesh of
    control points): each control point is a town dot on the source map
    paired with that town's real position. Outlines therefore keep the
    relation to towns that the atlas drew. A single affine fit to the same
    points has an RMS error of about 24 km (leave-one-out about 30 km), which
    is the honest accuracy of the result.
 3. Topology: Mongol areas are clipped to the Mongolian People's Republic
    guide line (src/data/mpr-border-sectors.json); gaps of under 20 km between
    Manchukuo and Mongol-held territory (artefacts of the drawn boundary
    lines) are given to Manchukuo; outlines are simplified to 2.5 km.

Requires: pip install numpy scipy shapely pyproj opencv-python-headless pillow
"""
SCAN = 'nc-1935-1940.png'
MPR_SECTORS = '../../src/data/mpr-border-sectors.json'
OUT = 'nc-1935-1940-polys.json'  # intermediate; combine_territories.py builds src/data/territories.json
import numpy as np, cv2, json
from PIL import Image, ImageFilter
from pyproj import Proj
from scipy.spatial import Delaunay
from shapely.geometry import Polygon, LineString, MultiPolygon, mapping
from shapely.ops import unary_union
P=Proj(proj='lcc',lat_1=37,lat_2=47,lat_0=43,lon_0=113,ellps='WGS84')

CPS={'Ulaanbaatar':(574.3,833.0,106.917,47.918),'Zamin Uud':(717.9,1059.8,111.898,43.716),'Wuyuan':(561.0,1185.7,108.27,41.09),
 'Baotou':(651.8,1202.9,109.84,40.65),'Koko Khota':(714.8,1212.8,111.66,40.81),'Kalgan':(835.9,1202.0,114.88,40.81),
 'Beiping':(908.0,1253.7,116.40,39.91),'Tanggu':(952.0,1294.0,117.65,39.02),'Qiqihar':(1162,866,123.92,47.35),
 'Xinjing':(1243,1015,125.32,43.88),'Harbin':(1268.2,934.2,126.63,45.75),'Mukden':(1170,1157,123.43,41.80),
 'Tamsagbulag':(942.1,876.3,117.28,47.23),'Hailar':(1027,767,119.76,49.21),'Manzhouli':(947,757,117.43,49.59),'Dolon Nuur':(872.7,1104.0,116.485,42.207)}
src=np.array([[v[0],v[1]] for v in CPS.values()]); dst=np.array([P(v[2],v[3]) for v in CPS.values()])
Aall=np.hstack([src,np.ones((len(src),1))]); Mg,*_=np.linalg.lstsq(Aall,dst,rcond=None)
tri=Delaunay(src)
Ms=[]
for s in tri.simplices:
    A=np.hstack([src[s],np.ones((3,1))]); Ms.append(np.linalg.solve(A,dst[s]))
def px2xy(pts):
    pts=np.asarray(pts,float); idx=tri.find_simplex(pts); out=np.empty_like(pts)
    for i,(p,t) in enumerate(zip(pts,idx)):
        M=Ms[t] if t>=0 else Mg
        out[i]=np.array([p[0],p[1],1.0])@M
    return out

im=Image.open(SCAN).convert('RGB')
sm=np.array(im.filter(ImageFilter.MedianFilter(7))).astype(int)
R,G,B=sm[...,0],sm[...,1],sm[...,2]
blue=(B>190)&(B-R>120); dark=blue&(G<188)&(R<20); cyan=blue&~dark
light=(B>225)&(B-R>15)&(B-R<=120)&(G>215)
orange=(R>215)&(R-B>25)&(G>190)&(G-B>15)&(R-G<40)
green=(G>195)&(G>R+5)&(B<175)&(R>150); pink=(R>180)&(R-G>70)&(R-B>40)
def u8(m): return m.astype(np.uint8)*255
def opened(m,k): return cv2.morphologyEx(u8(m),cv2.MORPH_OPEN,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(k,k)))>0
def poly_from(mask, close, seed):
    m=cv2.morphologyEx(u8(mask),cv2.MORPH_CLOSE,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(close,close)))
    m=cv2.morphologyEx(m,cv2.MORPH_OPEN,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5)))
    cs,_=cv2.findContours(m,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    cs=[c for c in cs if cv2.pointPolygonTest(c,seed,False)>=0]
    c=max(cs,key=cv2.contourArea)[:,0,:].astype(float)
    return Polygon(px2xy(c)).buffer(0)
seed=(780,1080)
mmg=poly_from(dark,23,seed)
ruled=poly_from(dark|cyan,27,seed)
claimed=poly_from(dark|cyan|opened(light,9),35,seed)
manchu=poly_from(orange|green|pink,41,(1100,1000))

# MPR: everything north/west of the MPR guide line (modern line; approximate in the sectors that matter here)
mb=json.load(open(MPR_SECTORS))
line=mb['C']+mb['D'][1:]+mb['E'][1:]
ring=line+[[116.684,60],[80,60],[80,line[0][1]]]
mpr=Polygon([P(a,b) for a,b in ring]).buffer(0)

ruled=unary_union([ruled,mmg]); claimed=unary_union([claimed,ruled])
mmg=mmg.difference(mpr); ruled=ruled.difference(mpr); claimed=claimed.difference(mpr)
# close the hairline gaps left by the source's drawn boundary lines between Manchukuo and Mongol-ruled territory
d=20000
gap=manchu.buffer(d).intersection(claimed.buffer(d)).difference(manchu).difference(claimed)
manchu=unary_union([manchu,gap]).buffer(3000).buffer(-3000).difference(claimed)
def clean(g):
    g=g.buffer(0)
    if isinstance(g,MultiPolygon): g=max(g.geoms,key=lambda p:p.area)
    g=Polygon(g.exterior)  # drop interior holes (labels)
    return g.simplify(2500)
out={}
for k,g in [('mmg',mmg),('ruled',ruled),('claimed',claimed),('manchukuo',manchu)]:
    g=clean(g)
    lon,lat=P(*np.array(g.exterior.coords).T,inverse=True)
    out[k]=[[round(float(a),3),round(float(b),3)] for a,b in zip(lon,lat)]
    print(k,len(out[k]),round(g.area/1e6),'km2')
json.dump(out,open(OUT,'w'),separators=(',',':'))
