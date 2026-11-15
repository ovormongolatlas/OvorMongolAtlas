"""Trace South Chahar (察南政府) and North Shansi (晉北政府) from the Japanese
map 蒙疆地域圖 for the Timeline Map.

Source: 蒙疆地域圖, Japanese, undated (厚和 for Hohhot and separate 察南/晉北
governments suggest about 1937-1939). The scan is not kept in this repository;
put it beside this script as SCAN to rerun.

Method:
 1. Keep only the map's thick black boundary lines (dark pixels that survive a
    7 px morphological opening). Two short gaps where a red railway and the
    red iron-mine symbol cover the line north of Kalgan are bridged by hand
    (BRIDGE below); then each government is flood-filled from a point inside it.
 2. Georeference by rubber-sheeting on 27 town symbols (pixel centres refined
    to the symbol, paired with the towns' real positions). Leaving each town
    out in turn, the mesh predicts it to within about 12 km (RMS).
Output: jp-mengjiang-polys.pkl, read by combine_territories.py.
Requires: pip install numpy scipy shapely pyproj opencv-python-headless
"""
import numpy as np, cv2, json, pickle
from pyproj import Proj
from scipy.spatial import Delaunay
from shapely.geometry import Polygon
SCAN='mengjiang-chiikizu.png'
P=Proj(proj='lcc',lat_1=37,lat_2=47,lat_0=43,lon_0=113,ellps='WGS84')
REAL={'Kalgan':(114.88,40.82),'Xuanhua':(115.05,40.61),'Zhangbei':(114.71,41.16),'Chongli':(115.28,40.97),'Guyuan':(115.69,41.67),
'Kangbao':(114.60,41.85),'Shangdu':(113.56,41.56),'Xinghe':(113.83,40.87),'Datong':(113.30,40.09),'Fengzhen':(113.15,40.44),
'Hohhot':(111.66,40.82),'Jining':(113.10,41.03),'Liangcheng':(112.50,40.53),'Horinger':(111.82,40.38),'Togtoh':(111.19,40.27),
'Qingshuihe':(111.68,39.91),'Daixian':(112.96,39.07),'Ningwu':(112.30,39.00),'Beijing':(116.40,39.91),'Zhuozhou':(115.97,39.49),
'Baotou':(110.05,40.59),'Taiyuan':(112.55,37.87),'Yinchuan':(106.27,38.47),'Chengde':(117.93,40.97),'Duolun':(116.48,42.20),
'Chifeng':(118.96,42.27),'Jinzhou':(121.13,41.10)}
CPS={"Kalgan": [1854.3, 1346.1], "Xuanhua": [1876.3, 1400.9], "Zhangbei": [1845.6, 1281.2], "Chongli": [1900.4, 1330.4], "Guyuan": [2008.8, 1220.6], "Kangbao": [1837.9, 1174.2], "Shangdu": [1665.0, 1179.3], "Xinghe": [1701.2, 1333.3], "Datong": [1554.2, 1471.8], "Fengzhen": [1550.7, 1390.5], "Hohhot": [1302.9, 1275.0], "Jining": [1557.8, 1274.0], "Liangcheng": [1401.2, 1372.5], "Horinger": [1332.3, 1375.2], "Togtoh": [1222.0, 1364.3], "Qingshuihe": [1271.2, 1437.6], "Daixian": [1469.2, 1637.6], "Ningwu": [1366.5, 1655.0], "Beijing": [2074.3, 1585.9], "Zhuozhou": [1990.8, 1664.6], "Baotou": [1057.6, 1256.8], "Tianjin": [2609.4, 1976.8], "Taiyuan": [1358.1, 1912.6], "Yinchuan": [301.9, 1578.9], "Chengde": [2364.8, 1395.7], "Duolun": [2104.2, 1069.8], "Chifeng": [2512.0, 1127.0], "Jinzhou": [2906.7, 1391.1]}  # pixel centres on SCAN
BRIDGE=[(1795,1302),(1828,1306),(1850,1325),(1880,1348),(1910,1372),(1945,1380),(1968,1362)]
SEEDS={'chanan':(1790,1530),'jinbei':(1390,1500)}

g=cv2.cvtColor(cv2.imread(SCAN),cv2.COLOR_BGR2GRAY)
thick=cv2.morphologyEx(((g<70)*255).astype(np.uint8),cv2.MORPH_OPEN,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(7,7)))
cv2.polylines(thick,[np.array(BRIDGE,np.int32)],False,255,9)
names=[n for n in CPS if n in REAL]
src=np.array([CPS[n] for n in names],float); dst=np.array([P(*REAL[n]) for n in names])
Mg,*_=np.linalg.lstsq(np.hstack([src,np.ones((len(src),1))]),dst,rcond=None)
tri=Delaunay(src); Ms=[np.linalg.solve(np.hstack([src[s],np.ones((3,1))]),dst[s]) for s in tri.simplices]
def px2xy(pts):
    idx=tri.find_simplex(pts)
    return np.array([np.array([p[0],p[1],1.0])@(Ms[t] if t>=0 else Mg) for p,t in zip(pts,idx)])
out={}
for name,seed in SEEDS.items():
    d=5 if name=='chanan' else 9
    bar=cv2.dilate(thick,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(d,d)))
    bar[:8,:]=bar[-8:,:]=255; bar[:,:8]=bar[:,-8:]=255
    m=255-bar; cv2.floodFill(m,np.zeros((m.shape[0]+2,m.shape[1]+2),np.uint8),seed,128)
    reg=cv2.dilate(((m==128)*255).astype(np.uint8),cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(d+4,d+4)))
    c=max(cv2.findContours(reg,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)[0],key=cv2.contourArea)[:,0,:].astype(float)
    out[name]=Polygon(px2xy(c)).buffer(0).simplify(2000)
pickle.dump(out,open('jp-mengjiang-polys.pkl','wb'))
