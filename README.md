# Penmar Golf Course (GSPro build)

"Penmar by the Sea", 1233 Rose Ave, Venice CA. City of Los Angeles municipal 9-hole course, par 33. Built with `coursekit.py` (same pipeline as Moorpark and Tierra Rejada). One of the five courses for the OPCD licensed-designer server.

## Frame
- 2000 m square, centre 34.006361815, -118.459344037 (James's centre point). EPSG:6340, see `course.json` for the SW corner.
- Unity x = metres east, z = metres north, y = elevation - 4 m.
- `heightmap_2049.raw`: 2049 x 2049, 16-bit, Windows byte order. Unity Terrain 2000 x 43 x 2000 (about 1 m per sample). Ground 5.8 to 45.5 m.

## LiDAR
USGS 3DEP `CA_LosAngeles_1_B23` (QL1, flown 2023-24), 17.2 points/m2 (about 4x Tierra's 2018 survey), 68.7 M points, noise removed.
The only other survey here is `USGS_LPC_CA_LosAngeles_2016_LAS_2018` (8.3 pts/m2, 3.1 ground/m2), so B23 wins.

    python ../../coursekit.py lidar --ept CA_LosAngeles_1_B23

`points.npz` is not in git; rerun the line above to rebuild it (about 1 minute).

## Satellite
`satellite.jpg`: NAIP, 4096 px, 0.49 m/px (fetched on the Mac; the imagery servers are blocked from the cloud container). Terrain Size 2000.

## Holes
`map.osm` from James (OSM export, 2026-10-28): 9 hole lines, 21 tees, 11 greens, 9 bunkers, 1 fairway, no cart paths mapped.
`holes.csv` / `tees.csv`: OSM hole lengths match the card closely (hole 1 276 vs 281 Blue, hole 6 429 vs 436).

## Scorecard (`scorecard.csv`, photo in `reference/scorecard.png`)
Par 4 4 3 4 3 4 4 3 4 = 33. Men's HCP 6 3 8 9 2 1 5 7 4.
Tees Blue 2582 (32.0/104), White 2474 (31.6/102), Gold 2308 (30.9/99). Women: Blue 34.7/115, White 34.1/113, Gold 33.2/109.
Every tee also has an "Alt" yardage for the second nine (Blue Alt 2282, White Alt 2168, Gold Alt 2013), so an 18-hole GSPro layout can play holes 1-9 from the main tees and 10-18 from the Alt tees.
The hole plaques show slightly older numbers (hole 1: 271 White, 257 Gold; hole 7: 368 White). The build follows the scorecard.

## Course character (from James)
- Greens are mostly flat with no break: keep green surfaces flat, don't add shaping.
- Every tee has a concrete plaque: "PENMAR BY THE SEA", hole number, par, White and Gold yardage, engraved hole map, "CITY OF LOS ANGELES" (`reference/plaque_hole1.png`, `reference/plaque_hole3.png`, `reference/plaque_hole4.png` (288 / 270), `reference/plaque_hole7.png` (368 / 336, card says 342 / 332), `reference/tee_hole1.png`; full footer "CITY OF LOS ANGELES / DEPARTMENT OF RECREATION AND PARKS", sign on a square post). Good tee-sign asset to model.
- Tree-lined parkland: tall pines, eucalyptus and broadleaf. `trees.csv`: 534 LiDAR trees (3 m+), see below.

## Greenkeeper: `Penmar.GKD` (draft)
    python ../../coursekit.py card --repeat-nine --ob --line-tees --template ../../Moorpark_RidgelineCreekside.GKD --name "Penmar Golf Course" --scene Penmar
- 18 holes: 1-9 from the main tees, 10-18 replay the same holes from the Alt tees (`card.csv`, new `--repeat-nine` option in coursekit).
- Tees Blue -> Blue, White -> White, Gold -> Yellow. Every card yardage landed on a mapped OSM tee box except some Alt tees
  placed on the hole line at the card yardage: 12 Gold, 14 White/Gold, 15 Gold, 16 all, 18 all. Check those.
- Ratings: 18-hole = 2 x the card's 9-hole ratings (Blue 64.0/104, White 63.2/102, Gold 61.8/99; White and Gold match GHIN's 18-hole numbers).
  Stroke index: front nine odd (2n-1), back nine even (2n).
- OB: the coursekit draft put interior OB on the tree lines between holes, which is wrong here (tree lines are playable), so it was removed.
  OB line = the OSM course boundary pulled in 1.5 m (the fence). No water. Check: clubhouse and parking lot by holes 6/9 sit inside the line.
- Course info: altitude 30 ft, wind 250 degrees (onshore sea breeze; check the convention against Tierra), Parkland keyword.
- Fairways: only hole 6's fairway is in OSM; the photo trace is weak (1.7 ha) because summer NAIP fairways and rough look alike. Retrace in Inkscape.
- Preview: `ob_preview.jpg` (white = OB, orange = tees, yellow = aim points, cyan = greens).

## Fence and nets (for Tierra -> Build Fences; same `segment,x,z,y` layout as Tierra Rejada, y = ground - 4 m from the heightmap)
- `fences.csv`: 12 ft (3.66 m) **chain-link** perimeter fence (build it with `unity/ChainLinkFence.cs`, menu Penmar -> Build Chain-Link Fence, not the Tierra split-rail tool) around the whole course on the OSM course boundary, one closed segment, posts about 5 m apart, 2,436 m.
- `nets.csv`, both 100 ft (30.5 m) poles:
  - segment 0: behind the hole 3 green on the perimeter fence line, 80 m centred where the tee-to-green line meets the fence (25 m behind the green).
  - Poles every ~10 m (brown poles, see `reference/hole2_net_road.png`).
  - segment 1: hole 2, along the road (left side), 15-19 m (about 20 yds) off the tee boxes, from 10 m behind the back tee to 100 yds down the hole, 101 m.
- Preview `fence_net_preview.jpg` (white = fence, magenta = nets). Lengths are my guess from James's description; adjust the ends if the real nets are longer.
- Bathroom between the 3 and 5 greens: not in OSM or visible in LiDAR (under trees). Location to be confirmed.

## Unity tool: `unity/ChainLinkFence.cs`
Copy to `Assets/Editor/`, copy `fences.csv` to `Assets/Penmar/`, then Penmar -> Build Chain-Link Fence -> Build.
12 ft by default. Galvanised steel posts every 3 m (keeps every corner), top and mid rails, see-through diamond mesh (generated texture, cutout, both sides),
all sitting on the terrain. Mesh collider = GSPtimber (solid: balls never pass through, per BoJa's checklist), posts and rail = GSPconcrete.
Builds under `CHAINLINK_FENCES`; rebuilding replaces it. Not yet run on the PC.
- Typical perimeter fence: `reference/fence_chainlink.png` (plain galvanised chain link about 12 ft high, top and mid rails, posts about 3 m apart, no windscreen; also `reference/fence_12ft.png`).
- Hole 2 road side (Street View, `reference/hole2_net_road.png`): permanent chain-link fence with a dark green windscreen on the lower part, tall brown net poles just inside it. The second, lower fence by the kerb was temporary construction fencing: leave it out.
- Cart paths are dirt / decomposed granite, not concrete (hole 7 photo). None are mapped in OSM yet.

## Fairways (`course.svg` Fairway layer, 5.28 ha)
Neither the summer photo nor the LiDAR separates fairway from rough here (intensity is saturated over all turf; ground roughness is noise),
so fairways are drawn by design: `fairways.py` lays a 36 m corridor along each OSM hole line on the par 4s (from about 60 yds off
the back tee to the green) and a 22 m approach apron on the par 3s, then cuts out LiDAR tree canopy (2 m clear of the drip line),
bunkers, tees and greens and smooths the edge. Preview `fairway_preview.jpg`. Aim points were rebuilt from it (`card` + `fix_ob.py`).

## Easter egg: Harrison Ford's plane
`props.csv`: on 5 Mar 2015 Harrison Ford crash-landed his yellow 1942 Ryan PT-22 left of the 7th green, coming to rest between the
two hole 8 tees. Placed at the midpoint of the hole 8 tee boxes, nose down with the right wing low. Needs a PT-22 model (yellow wings,
red cowling, US roundels), a divot scar behind it, collider GSPtimber. Photos `reference/plane_*.png`.

## Look (photos in `reference/`)
- Trees: Canary Island and Italian stone pines, Monterey cypress (rust-brown in winter), redwoods and eucalyptus. Lots of tall straight pines along 4 and 7.
- Greens are flat with gentle mounds behind them (7, 2), fringe a slightly darker cut. Kikuyu everywhere, fairway barely different from rough.

## Rough plays rough (James: fairways are nice, the rough is rough, the trees block balls)
- `deep_rough.py` splits the old Rough layer: a 4 m first cut (Rough, GSPrough) around fairways, greens and tees, and everything
  beyond it, including under the tree lines, as Deep (GSPdeeprough). Fairway 5.3 ha, first cut 6.2 ha, deep rough 11.2 ha. Preview `rough_preview.jpg`.
- Trees: `trees.csv` is back to all 534 LiDAR trees (the satellite colour check was dropping the rust-brown Monterey cypress).
  Plant with Tierra -> Plant LiDAR Trees: trunk colliders GSPtimber, canopy colliders GSPleaves, so they knock balls down.

## Restroom between the 3 and 5 greens
James's pin 34.005018, -118.465085; the LiDAR shows a 3.5 m flat roof under the canopy about 12 m SW of it (Unity 456.5, 848).
Simple square brown block building with a flat roof (`reference/bathroom.png`), in `props.csv` as 4.5 x 4.5 x 3.2 m.
Build with `unity/PenmarProps.cs` (Penmar -> Build Buildings): walls + roof collider GSPconcrete. Not OB (an obstruction, play it as it lies).

## Bunkers and green surrounds (Tierra play-test lessons, Oct 28)
At Tierra the ball rolled fast through the sand and could be punched out with no loft, the bowls were too deep and steep, and the rough
behind some greens grabbed balls. `surrounds.py` applies the fixes here up front:
- No fairway, rough or deep polygon overlaps the sand (0 m2 checked), so the sand mesh is the only surface there: no fairway physics, no z-fighting.
- A 2 m first-cut lip of rough around every bunker; deep rough kept 2 m+ off sand and 6 m+ off every green.
- A fairway-height collar around every green: 3 m on the sides, about 5 m at the back, so balls roll out.
- `bunkers.csv`: the Tierra BunkerDepth profile per bunker: depth 0.25 m under 60 m2, 0.35 m for 60-150 m2, 0.5 m above 150 m2;
  flat floor (< 3 deg), a steeper face (25-30 deg) toward the green named in face_toward_x/z, gentle entry (< 12 deg) on the low side.
- In Unity: bunker meshes get the sand physics material (check in the collider sweep that every Bunker mesh reports sand, none fairway),
  sand colour warmer and less white, about (0.80, 0.76, 0.66), subtle rake noise, darker damp edges.
- Note from Tierra: GSPro's own sand penalty is mild (about 8% ball speed, no spin or launch penalty) and the course file can't make it stricter.
Areas now: fairway (with collars) 5.7 ha, first cut 2.2 ha, deep rough 11.0 ha, sand 0.1 ha (9 bunkers).

## BoJa feedback checklist pass (course-build/BOJA_FEEDBACK_CHECKLIST.md, Oct 28)
Done in the data:
- Tees never stacked: where the card gives two colours the same yardage (Blue = White on 3, 7, 12, 13, 15, 16; White = Gold on 17) the second colour sits 3 m to the side, same yardage (`fix_ob.py`). All tees inside the OB line.
- Par 3s have no aim point, so they aim at the green. Par 4 aim points sit at the widest part of the fairway.
- Bunkers clean and graded by size (`bunkers.csv`), collars 3 m / 5 m, deep rough 6 m+ off greens (`surrounds.py`).
- Nets and fences: solid colliders (fence mesh GSPtimber; build the 100 ft nets with solid colliders too, not GSPleaves).
- OB = one clean line on the course fence, no interior patches, no drop zones needed.
- Cart paths: `cartpaths.csv` now has the 6 dirt paths inside the fence (1.9 km) from OSM footways, checked on the photo (`cartpaths_preview.jpg`).
  Build them dirt/decomposed-granite tan, not white concrete, about 1.8 m wide and lifted 4 cm.
- Trees: 534 LiDAR trees checked on the satellite (`trees_on_satellite.png`).
- Restroom: brown block, flat roof, matches BoJa's photo.
To do on the PC: own project C:\GSP\Penmar_Project; Flyover reads the project GKD; no compile errors; in Greenkeeper set stimp about 10,
green firmness Normal, fairway firmness moderate (set in Penmar.GKD: DefaultStimp 2, MaxStimp 5, GreenFirmness 0, FairwayFirmness 0, Tierra's approved values);
tree LOD and billboards like Tierra; canopy colliders at about 80% of the crown and a shot sweep from every tee; warm tan sand;
backdrop: 1-2 km of flat Westside city (Santa Monica airport to the north-east, Santa Monica Mountains on the horizon) with fog.
Cross-hole misses: Penmar's holes run side by side with only tree lines between them and no OB inside the fence, which is how the real course plays.

## Back-nine (Alt) tee pads
The 10 Alt tees with no mapped OSM box (12 Gold, 14 White and Gold, 15 Gold, all three on 16 and 18) now stand on flat tee pads
added to the Tee layer of `course.svg` (`alt_tee_pads.py`: 7 m along the line x 9 m across, neighbours merged, a 2 m first cut around them).
Every tee in `Penmar.GKD` is now on a Tee polygon.

`map.osm.xml` is the OSM export in plain git (the cloud can't push LFS files, and `*.osm` is LFS-tracked): copy it to `map.osm` before running coursekit or OPCD.

## Repo note (2026-11-03)
This folder is now its own repo (split out of the moorpark branch `claude/project-thread-j2x22i`) wired to the course-build toolkit via `course.json`.
heightmap: `heightmap_2049.raw` was rebuilt in the cloud on 2026-11-03 (`lidar` then `heightmap`; the first `lidar` run died with an `http.client.IncompleteRead` at tile 1650/2072 and the retry finished from `ept_cache/`) and is committed through LFS. If it is missing or an LFS pointer, rebuild with `python3 ../moorpark/coursekit.py lidar --ept CA_LosAngeles_1_B23` then `python3 ../moorpark/coursekit.py heightmap` (coursekit.py from the moorpark repo, run from inside this folder) on the PC. `ept_cache/` and `points.npz` are ignored.
