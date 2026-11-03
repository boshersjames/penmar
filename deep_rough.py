"""Penmar rough plays rough: keep a 4 m first cut (Rough) around fairways, greens and tees; everything else in the old
Rough layer, including the ground under the tree lines, becomes Deep (GSPdeeprough). Rewrites course.svg Rough and Deep layers."""
import re
from shapely.geometry import Polygon
from shapely.ops import unary_union
S = 2000
svg = open("course.svg").read()
def polys(label):
    i0 = svg.find('inkscape:label="%s"' % label); blk = svg[i0:svg.find("</g>", i0)]
    out = []
    for d in re.findall(r' d="([^"]+)"', blk):
        rings = []
        for sp in re.split(r"(?=M )", d.strip()):
            n = [float(v) for v in re.findall(r"-?\d+\.?\d*", sp)]
            pts = [(n[k], S - n[k + 1]) for k in range(0, len(n) - 1, 2)]
            if len(pts) > 2: rings.append(Polygon(pts).buffer(0))
        if rings:  # evenodd: outer minus holes
            rings.sort(key=lambda p: -p.area); g = rings[0]
            for r in rings[1:]: g = g.symmetric_difference(r)
            out.append(g)
    return unary_union(out)
rough = polys("Rough"); fw = polys("Fairway"); gr = polys("Green"); te = polys("Tee")
first_cut = unary_union([fw.buffer(4), gr.buffer(4), te.buffer(4)])
deep = rough.difference(first_cut).buffer(-0.5).buffer(0.5)
deep = unary_union([p for p in getattr(deep, "geoms", [deep]) if p.area > 30])
new_rough = rough.difference(deep)
def d_of(p):
    rings = [p.exterior] + list(p.interiors)
    return " ".join("M " + " L ".join("%.3f,%.3f" % (a, S - b) for a, b in list(r.coords)[:-1]) + " Z" for r in rings)
def put(svg, label, geom, pid, col):
    gs = [g.simplify(0.25) for g in getattr(geom, "geoms", [geom]) if g.area > 1]
    paths = "\n".join('<path id="%s_%d" style="fill:%s;fill-opacity:1;fill-rule:evenodd;stroke:none" d="%s"/>' % (pid, n, col, d_of(g)) for n, g in enumerate(gs))
    i0 = svg.find('inkscape:label="%s"' % label); a = svg.find(">", i0) + 1; b = svg.find("</g>", i0)
    return svg[:a] + "\n" + paths + "\n" + svg[b:]
col = lambda pid: re.search(r'id="%s_0" style="fill:(#[0-9A-Fa-f]{6})' % pid, svg)
rough_col = col("rough").group(1)
svg = put(svg, "Rough", new_rough, "rough", rough_col)
svg = put(svg, "Deep", deep, "deep", "#164B20")
open("course.svg", "w").write(svg)
print("Rough (first cut) %.2f ha, Deep %.2f ha, Fairway %.2f ha" % (new_rough.area / 1e4, deep.area / 1e4, fw.area / 1e4))
