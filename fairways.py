"""Penmar fairways by design: a corridor along each OSM hole line, clipped to open turf (no LiDAR canopy, no bunkers/tees),
because neither the photo nor the LiDAR separates fairway from rough here. Writes the Fairway layer of course.svg."""
import sys, os, re, json, numpy as np
sys.path.insert(0, "/home/claude/moorpark"); os.chdir("/home/claude/moorpark/courses/penmar")
import coursekit as ck
from shapely.geometry import LineString, Polygon, Point
from shapely.ops import unary_union, substring
from shapely import affinity
from scipy import ndimage
from skimage import measure
c = ck.load_cfg(); S = int(c["size"])
holes, yv, _ = ck.hole_data(c)
P = np.load("points.npz"); x, z, h, cl = P["x"], P["n"], P["z"], P["c"]
X0, Z0, X1, Z1, R = 300, 580, 1340, 1360, 1.0
W, H = int((X1 - X0) / R), int((Z1 - Z0) / R)
m = (x > X0) & (x < X1) & (z > Z0) & (z < Z1)
x, z, h, cl = x[m], z[m], h[m], cl[m]
i, j = ((x - X0) / R).astype(int), ((z - Z0) / R).astype(int)
g = cl == 2
s = np.zeros((W, H)); k = np.zeros((W, H)); np.add.at(s, (i[g], j[g]), h[g]); np.add.at(k, (i[g], j[g]), 1)
dtm = np.where(k > 0, s / np.maximum(k, 1), np.nan)
idx = ndimage.distance_transform_edt(np.isnan(dtm), return_distances=False, return_indices=True); dtm = dtm[tuple(idx)]
dsm = np.full((W, H), -1e9); np.maximum.at(dsm, (i, j), h)
canopy = ndimage.binary_closing((dsm - dtm) > 2.0, iterations=1)
canopy = ndimage.binary_dilation(canopy, iterations=2)          # 2 m clear of the drip line

def mask_poly(mask):
    polys = []
    for ct in measure.find_contours(np.pad(mask, 1).astype(float), 0.5):
        pts = [(X0 + (a - 1 + .5) * R, Z0 + (b - 1 + .5) * R) for a, b in ct]
        if len(pts) > 3: polys.append(Polygon(pts).buffer(0))
    return polys
# canopy polygons (holes in the mask handled by symmetric difference of nested contours -> use union of small ones is fine)
canopy_poly = unary_union([p for p in mask_poly(canopy) if p.area > 4])

bound = Polygon([(334.2, 789.96), (357.75, 751.9), (377.42, 720.08), (427.22, 639.48), (439.87, 619.47), (441.67, 616.55), (1307.08, 1151.12), (1229.79, 1275.8), (1200.32, 1319.14), (1130.91, 1276.08), (1122.86, 1274.89), (560.6, 929.29), (557.08, 926.99)]).buffer(-6)
svg = open("course.svg").read()
def layer_polys(label):
    i0 = svg.find('inkscape:label="%s"' % label); blk = svg[i0:svg.find("</g>", i0)]
    out = []
    for d in re.findall(r' d="([^"]+)"', blk):
        for sp in re.split(r"(?=M )", d.strip()):
            nums = [float(v) for v in re.findall(r"-?\d+\.?\d*", sp)]
            pts = [(nums[q], S - nums[q + 1]) for q in range(0, len(nums) - 1, 2)]
            if len(pts) > 2: out.append(Polygon(pts).buffer(0))
    return unary_union(out)
greens, tees, bunkers = layer_polys("Green"), layer_polys("Tee"), layer_polys("Bunker")
block = unary_union([canopy_poly, bunkers.buffer(2.5), tees.buffer(3), greens.buffer(1.0)])

fw_all = []
for hh in holes:
    route = LineString(np.vstack([hh["line"][0]] + hh["path"] + [hh["green"]]))
    L = route.length; par = int(hh["par"] or 4)
    if par >= 4: seg, half = substring(route, 55, L - 14), 18      # starts ~60 yds off the back tee, 36 m wide
    else:        seg, half = substring(route, max(10, L - 50), L - 13), 11   # short approach apron on the par 3s
    corr = seg.buffer(half, cap_style=1)
    fw = corr.intersection(bound).difference(block)
    fw = fw.buffer(-3).buffer(3)                                     # drop slivers and smooth the edge
    if fw.is_empty: continue
    parts = [p for p in getattr(fw, "geoms", [fw]) if p.area > 150]
    # keep pieces touching the hole line only
    parts = [p for p in parts if p.distance(seg) < 2]
    fw_all += [p.simplify(0.3) for p in parts]
    print("hole %s par %d: %.0f m2 in %d piece(s)" % (hh["hole"], par, sum(p.area for p in parts), len(parts)))
fw_u = unary_union(fw_all)
geoms = list(getattr(fw_u, "geoms", [fw_u]))
print("Fairway total %.2f ha" % (fw_u.area / 1e4))
def d_of(p):
    rings = [p.exterior] + list(p.interiors)
    return " ".join("M " + " L ".join("%.3f,%.3f" % (a, S - b) for a, b in list(r.coords)[:-1]) + " Z" for r in rings)
paths = "\n".join('<path id="fairway_%d" style="fill:#43E561;fill-opacity:1;fill-rule:evenodd;stroke:none" d="%s"/>' % (n, d_of(p)) for n, p in enumerate(geoms))
i0 = svg.find('inkscape:label="Fairway"'); a = svg.find(">", i0) + 1; b = svg.find("</g>", i0)
svg = svg[:a] + "\n" + paths + "\n" + svg[b:]
open("course.svg", "w").write(svg)
json.dump({"canopy_note": "LiDAR >2 m, dilated 2 m"}, open("/tmp/claude-0/pm/fw/done.json", "w"))
