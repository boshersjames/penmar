"""After `coursekit.py card`: Penmar OB = the course fence (OSM boundary pulled in 1.5 m); no interior OB on tree lines."""
import json, numpy as np
from shapely.geometry import Polygon
c = json.load(open("course.json")); S = c["size"]
fence = [(334.2, 789.96), (357.75, 751.9), (377.42, 720.08), (427.22, 639.48), (439.87, 619.47), (441.67, 616.55), (1307.08, 1151.12), (1229.79, 1275.8), (1200.32, 1319.14), (1130.91, 1276.08), (1122.86, 1274.89), (560.6, 929.29), (557.08, 926.99)]
poly = Polygon(fence).buffer(-1.5).simplify(0.5)
H = np.fromfile("heightmap_2049.raw", "<u2").reshape(2049, 2049)
y = lambda x, z: float(H[int(round(z / S * 2048)), int(round(x / S * 2048))]) / 65535 * c["terrain_height"]
d = json.load(open("Penmar.GKD", encoding="utf-8-sig"))
cs = list(poly.exterior.coords)[:-1]
d["pOOB"] = {"pointCount": len(cs), "coords": [{"x": round(x, 3), "y": round(y(x, z), 3), "z": round(z, 3)} for x, z in cs]}
d["Hazards"] = []; d["hazardCount"] = 0
json.dump(d, open("Penmar.GKD", "w"), separators=(",", ":"))
print("pOOB = course fence (%d points), interior OB removed" % len(cs))

# Tees with the same card yardage (Blue = White on 3, 7, 12, 13, 15, 16; White = Gold on 17) must not stack on one spot
# (BoJa checklist): move the shorter-named colour 3 m sideways, square to the line to the green, same yardage.
d = json.load(open("Penmar.GKD", encoding="utf-8-sig"))
order = ["Black", "Green", "Blue", "White", "Yellow", "Red", "Junior"]
moved = []
for h in d["Holes"]:
    tees = [t for t in h["Tees"] if t["Position"] and t["Enabled"] and t["TeeType"] in order]
    gc = next((t["Position"] for t in h["Tees"] if t["TeeType"] == "GreenCenterPoint" and t["Position"]), None)
    if not gc: continue
    tees.sort(key=lambda t: order.index(t["TeeType"]))
    for i, a in enumerate(tees):
        for b in tees[i + 1:]:
            pa, pb = a["Position"], b["Position"]
            if abs(pa["x"] - pb["x"]) < 1 and abs(pa["z"] - pb["z"]) < 1:
                v = np.array([gc["x"] - pa["x"], gc["z"] - pa["z"]]); v /= np.linalg.norm(v)
                nx, nz = pb["x"] - 3 * v[1], pb["z"] + 3 * v[0]
                pb.update({"x": round(nx, 3), "z": round(nz, 3), "y": round(y(nx, nz), 3)})
                moved.append("%d %s" % (h["HoleNumber"], b["TeeType"]))
json.dump(d, open("Penmar.GKD", "w"), separators=(",", ":"))
print("Unstacked tees (3 m sideways):", ", ".join(moved) or "none")

# Tierra's approved green settings (BoJa checklist): stimp 10, green Normal, fairway firmness moderate
d = json.load(open("Penmar.GKD", encoding="utf-8-sig"))
d.update({"DefaultStimp": 2, "MaxStimp": 5, "FairwayFirmnessDefault": 0, "GreenFirmnessDefault": 0})
json.dump(d, open("Penmar.GKD", "w"), separators=(",", ":"))

# Approved course description (course-build/course_descriptions.md, BoJa 10/28)
d = json.load(open("Penmar.GKD", encoding="utf-8-sig"))
d["CourseInfo"] = json.load(open("course.json"))["gkd"]["CourseInfo"]
d["Designer"] = "jboshers"   # BoJa: GSPro shows their handle on every course
json.dump(d, open("Penmar.GKD", "w"), separators=(",", ":"))
