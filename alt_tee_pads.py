"""Alt (back-nine) tees with no mapped OSM box sit on the hole line at the card yardage. Give each a flat tee pad in course.svg
(7 m along the line x 9 m across, Tee layer) and cut fairway/rough/deep out from under it, so the tee stands on a real box."""
import json, re, numpy as np
from shapely.geometry import Polygon, Point
from shapely.ops import unary_union
from shapely import affinity
S = 2000
d = json.load(open("Penmar.GKD", encoding="utf-8-sig"))
svg = open("course.svg").read()
def polys(label):
    i0 = svg.find('inkscape:label="%s"' % label); blk = svg[i0:svg.find("</g>", i0)]; out = []
    for dd in re.findall(r' d="([^"]+)"', blk):
        rings = []
        for sp in re.split(r"(?=M )", dd.strip()):
            n = [float(v) for v in re.findall(r"-?\d+\.?\d*", sp)]
            pts = [(n[k], S - n[k + 1]) for k in range(0, len(n) - 1, 2)]
            if len(pts) > 2: rings.append(Polygon(pts).buffer(0))
        if rings:
            rings.sort(key=lambda p: -p.area); g = rings[0]
            for r in rings[1:]: g = g.symmetric_difference(r)
            out.append(g)
    return unary_union(out)
tees = polys("Tee")
pads, report = [], []
for h in d["Holes"]:
    gc = next((t["Position"] for t in h["Tees"] if t["TeeType"] == "GreenCenterPoint" and t["Position"]), None)
    for t in h["Tees"]:
        if not (t["Position"] and t["Enabled"] and t["TeeType"] in ("Black", "Green", "Blue", "White", "Yellow", "Red")): continue
        p = Point(t["Position"]["x"], t["Position"]["z"])
        if tees.buffer(0.5).contains(p): continue
        v = np.array([gc["x"] - p.x, gc["z"] - p.y]); ang = np.degrees(np.arctan2(v[1], v[0]))
        pad = affinity.rotate(Polygon([(-3.5, -4.5), (3.5, -4.5), (3.5, 4.5), (-3.5, 4.5)]), ang, origin=(0, 0))
        pads.append(affinity.translate(pad, p.x, p.y)); report.append("%d %s" % (h["HoleNumber"], t["TeeType"]))
new = unary_union(pads).buffer(0.8, join_style=1).buffer(-0.8, join_style=1)   # merge neighbours, round corners
print("Pads for:", ", ".join(report))
def d_of(p):
    rings = [p.exterior] + list(p.interiors)
    return " ".join("M " + " L ".join("%.3f,%.3f" % (a, S - b) for a, b in list(r.coords)[:-1]) + " Z" for r in rings)
def put(label, geom, pid, col):
    global svg
    gs = [g for g in getattr(geom, "geoms", [geom]) if g.area > 1]
    paths = "\n".join('<path id="%s_%d" style="fill:%s;fill-opacity:1;fill-rule:evenodd;stroke:none" d="%s"/>' % (pid, n, col, d_of(g)) for n, g in enumerate(gs))
    i0 = svg.find('inkscape:label="%s"' % label); a = svg.find(">", i0) + 1; b = svg.find("</g>", i0)
    svg = svg[:a] + "\n" + paths + "\n" + svg[b:]
tee_col = re.search(r'id="tee_0" style="fill:(#[0-9A-Fa-f]{6})', svg).group(1)
put("Tee", unary_union([tees, new]), "tee", tee_col)
for lab, pid, col in [("Fairway", "fairway", "#43E561"), ("Rough", "rough", "#278438"), ("Deep", "deep", "#164B20")]:
    put(lab, polys(lab).difference(new), pid, col)
# a 2 m first-cut ring around the new pads instead of deep rough
ring = new.buffer(2).difference(new)
deep = polys("Deep"); put("Deep", deep.difference(ring), "deep", "#164B20")
put("Rough", unary_union([polys("Rough"), ring.intersection(deep)]), "rough", "#278438")
open("course.svg", "w").write(svg)
print("Added %d pad(s), %.0f m2" % (len(getattr(new, "geoms", [new])), new.area))
