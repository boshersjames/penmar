"""Tierra lessons for Penmar greens and bunkers (Oct 28 play test):
- Collar: fairway-height ring around every green (3 m on the sides, 5 m at the back) so balls roll out; deep rough stays >= 6 m off greens.
- Bunkers: no fairway, rough or deep polygon may overlap sand (no z-fighting, no fairway physics in the sand); a 2 m first-cut lip of rough around each.
- Writes bunkers.csv with the Tierra depth profile per bunker (BunkerDepth tool): depth by size, flat floor, steep face toward the green."""
import re, csv, sys, os, numpy as np
sys.path.insert(0, "/home/claude/moorpark")
import coursekit as ck
from shapely.geometry import Polygon, Point, LineString
from shapely.ops import unary_union
from shapely import affinity
S = 2000
svg = open("course.svg").read()
def polys(label):
    i0 = svg.find('inkscape:label="%s"' % label); blk = svg[i0:svg.find("</g>", i0)]; out = []
    for d in re.findall(r' d="([^"]+)"', blk):
        rings = []
        for sp in re.split(r"(?=M )", d.strip()):
            n = [float(v) for v in re.findall(r"-?\d+\.?\d*", sp)]
            pts = [(n[k], S - n[k + 1]) for k in range(0, len(n) - 1, 2)]
            if len(pts) > 2: rings.append(Polygon(pts).buffer(0))
        if rings:
            rings.sort(key=lambda p: -p.area); g = rings[0]
            for r in rings[1:]: g = g.symmetric_difference(r)
            out.append(g)
    return out
def U(label): return unary_union(polys(label))
c = ck.load_cfg(); holes, yv, _ = ck.hole_data(c)
G, B, T = polys("Green"), U("Bunker"), U("Tee")
fw, rough, deep = U("Fairway"), U("Rough"), U("Deep")
everything = unary_union([fw, rough, deep, T, B, unary_union(G)])
# collar: 3 m ring, stretched to 5 m behind the green (away from the hole's approach)
collars = []
for g in G:
    cen = np.array(g.centroid.coords[0])
    h = min(holes, key=lambda hh: np.hypot(*(np.array(hh["green"]) - cen)))
    route = [np.array(h["line"][0])] + [np.array(p) for p in h["path"]]
    app = cen - route[-1]; app = app / (np.linalg.norm(app) or 1)          # direction of play into the green
    back = affinity.translate(g.buffer(5), *(app * 2.0))                   # shifted ring = deeper at the back
    collars.append(unary_union([g.buffer(3), back.intersection(g.buffer(5))]))
collar = unary_union(collars).difference(unary_union(G)).difference(B.buffer(0.3)).difference(T)
fw = unary_union([fw, collar]).difference(B.buffer(0.3)).difference(unary_union(G))
lip = B.buffer(2).difference(B)
keep_clear = unary_union([unary_union(G).buffer(6), B.buffer(2), fw, T])
deep = deep.difference(keep_clear).buffer(-0.3).buffer(0.3)
deep = unary_union([p for p in getattr(deep, "geoms", [deep]) if p.area > 30])
rough = everything.difference(unary_union([fw, deep, T, B, unary_union(G)])).buffer(-0.05).buffer(0.05)
for nm, gg in [("fairway", fw), ("rough", rough), ("deep", deep)]:
    print("%s %.2f ha, overlap with sand %.2f m2" % (nm, gg.area / 1e4, gg.intersection(B).area))
def d_of(p):
    rings = [p.exterior] + list(p.interiors)
    return " ".join("M " + " L ".join("%.3f,%.3f" % (a, S - b) for a, b in list(r.coords)[:-1]) + " Z" for r in rings)
def put(svg, label, geom, pid, col):
    gs = [g.simplify(0.2) for g in getattr(geom, "geoms", [geom]) if g.area > 1]
    paths = "\n".join('<path id="%s_%d" style="fill:%s;fill-opacity:1;fill-rule:evenodd;stroke:none" d="%s"/>' % (pid, n, col, d_of(g)) for n, g in enumerate(gs))
    i0 = svg.find('inkscape:label="%s"' % label); a = svg.find(">", i0) + 1; b = svg.find("</g>", i0)
    return svg[:a] + "\n" + paths + "\n" + svg[b:]
svg = put(svg, "Fairway", fw, "fairway", "#43E561")
svg = put(svg, "Rough", rough, "rough", "#278438")
svg = put(svg, "Deep", deep, "deep", "#164B20")
open("course.svg", "w").write(svg)
# bunker depth profile (Tierra BunkerDepth, Oct 28): depth by area, flat floor < 3 deg, face up to 25-30 deg toward the green, entry < 12 deg
w = csv.writer(open("bunkers.csv", "w", newline=""))
w.writerow(["bunker", "x", "z", "area_m2", "depth_m", "face_toward_x", "face_toward_z", "hole", "kind"])
for k, b in enumerate(getattr(B, "geoms", [B])):
    cen = np.array(b.centroid.coords[0]); a = b.area
    depth = 0.25 if a < 60 else 0.35 if a <= 150 else 0.5
    h = min(holes, key=lambda hh: min(np.hypot(*(np.array(hh["green"]) - cen)), LineString([hh["line"][0]] + hh["path"] + [hh["green"]]).distance(Point(cen))))
    gd = np.hypot(*(np.array(h["green"]) - cen))
    w.writerow([k, "%.2f" % cen[0], "%.2f" % cen[1], "%.0f" % a, depth, "%.2f" % h["green"][0], "%.2f" % h["green"][1], h["hole"], "greenside" if gd < 40 else "fairway"])
print(open("bunkers.csv").read())
