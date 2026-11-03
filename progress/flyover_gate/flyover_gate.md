# Flyover gate (data pass)

Inputs: GKD `Penmar.GKD`, signs `progress/hole_signs.json`, trees `trees.csv`, greens `course.svg`, heightmap `heightmap_2049.raw`, pin index 0.

Pass = yaw and pitch under 5 deg in every 1 s window, opening camera clear of crowns with the sign in frame and unhidden, terrain clearance 5 m+, crown clearance 1.5 m+ on the whole path, no part of the green cut off ahead or to the side in the end frame (the part under the camera is reported, not failed), pin in frame and not behind a crown.

| Hole | s | yaw/1s | pitch/1s | end pitch (target) | end h / short (used) | terrain min (after rise) | crown min (tree, frame), lift rise/flight | first: crown / sight / in frame | green: in / under cam / cut off (pull-back to fit) | pin | result | opening move |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 16.1 | 0.2 | 4.5 | -29.3 (-29.3) | 13.2 / 22.5 | 13.2 | 5.2 (29, f88), 0.0 / 0.0 | 12.8 / 12.2 / yes | 100% / 0 / 0 (0 m) | in, sight 11.5 | **OK** |  |
| 2 | 18.2 | 1.2 | 4.5 | -29.6 (-29.6) | 15.9 / 27.5 | 15.9 | 4.3 (16, f206), 0.0 / 0.0 | 8.4 / 8.6 / yes | 91% / 6 / 0 (0 m) | in, sight 4.9 | **OK** |  |
| 3 | 12.7 | 0.0 | 3.6 | -29.5 (-29.5) | 14.8 / 25.5 | 14.8 | 1.5 (425, f52), 0.0 / 0.0 | 3.1 / 2.2 / yes | 100% / 0 / 0 (0 m) | in, sight 4.0 | **OK** |  |
| 4 | 16.6 | 1.4 | 4.5 | -29.6 (-29.6) | 12.8 / 22.0 | 12.8 | 2.4 (195, f70), 0.0 / 0.0 | 5.7 / 5.7 / yes | 100% / 0 / 0 (0 m) | in, sight 5.6 | **OK** |  |
| 5 | 13.6 | 0.0 | 4.5 | -29.7 (-29.7) | 12.7 / 21.5 | 12.7 | 2.8 (199, f74), 0.0 / 0.0 | 5.2 / 5.0 / yes | 100% / 0 / 0 (0 m) | in, sight 4.9 | **OK** |  |
| 6 | 21.5 | 0.1 | 4.5 | -30.1 (-30.1) | 14.4 / 24.5 | 14.4 | 4.1 (245, f68), 0.0 / 0.0 | 7.0 / 6.4 / yes | 96% / 3 / 0 (0 m) | in, sight 7.1 | **OK** |  |
| 7 | 18.2 | 0.2 | 4.5 | -29.5 (-29.5) | 13.8 / 23.5 | 13.7 | 3.5 (220, f64), 0.0 / 3.0 | 5.5 / 5.6 / yes | 100% / 0 / 0 (0 m) | in, sight 8.9 | **OK** |  |
| 8 | 12.7 | 0.0 | 3.8 | -29.9 (-29.9) | 15.6 / 27.0 | 15.6 | 4.3 (311, f54), 0.0 / 0.0 | 5.6 / 5.6 / yes | 94% / 5 / 0 (0 m) | in, sight 4.2 | **OK** |  |
| 9 | 18.8 | 1.0 | 4.5 | -29.7 (-29.7) | 15.3 / 26.0 | 15.3 | 2.6 (204, f66), 0.0 / 6.7 | 6.6 / 6.6 / yes | 96% / 3 / 0 (0 m) | in, sight 3.3 | **OK** |  |
| 10 | 16.0 | 0.2 | 4.5 | -29.3 (-29.3) | 13.2 / 22.5 | 13.2 | 5.0 (29, f86), 0.0 / 0.0 | 12.3 / 11.7 / yes | 100% / 0 / 0 (0 m) | in, sight 11.5 | **OK** |  |
| 11 | 17.9 | 1.2 | 4.5 | -29.6 (-29.6) | 15.9 / 27.5 | 15.9 | 4.4 (16, f200), 0.0 / 0.0 | 9.8 / 9.0 / yes | 91% / 6 / 0 (0 m) | in, sight 4.9 | **OK** |  |
| 12 | 12.7 | 0.0 | 4.5 | -29.5 (-29.5) | 14.8 / 25.5 | 14.8 | 4.0 (271, f252), 0.0 / 0.0 | 9.3 / 8.9 / yes | 100% / 0 / 0 (0 m) | in, sight 3.3 | **OK** |  |
| 13 | 16.6 | 1.4 | 4.5 | -29.6 (-29.6) | 12.8 / 22.0 | 12.8 | 2.4 (195, f70), 0.0 / 0.0 | 5.7 / 5.7 / yes | 100% / 0 / 0 (0 m) | in, sight 5.6 | **OK** |  |
| 14 | 12.7 | 0.0 | 3.6 | -29.7 (-29.7) | 12.4 / 21.0 | 12.3 | 4.0 (326, f58), 0.0 / 0.0 | 5.7 / 5.7 / yes | 100% / 0 / 0 (0 m) | in, sight 4.7 | **OK** |  |
| 15 | 19.0 | 0.1 | 4.5 | -30.1 (-30.1) | 14.4 / 24.5 | 14.4 | 6.4 (326, f62), 0.0 / 0.0 | 7.6 / 7.6 / yes | 96% / 3 / 0 (0 m) | in, sight 7.1 | **OK** |  |
| 16 | 16.0 | 0.3 | 4.5 | -29.5 (-29.5) | 13.8 / 23.5 | 13.7 | 1.7 (209, f64), 0.0 / 0.0 | 5.3 / 5.2 / yes | 100% / 0 / 0 (0 m) | in, sight 8.9 | **OK** |  |
| 17 | 12.7 | 0.0 | 3.7 | -29.9 (-29.9) | 15.6 / 27.0 | 15.6 | 2.7 (68, f80), 0.0 / 0.0 | 10.1 / 10.1 / yes | 94% / 5 / 0 (0 m) | in, sight 4.1 | **OK** |  |
| 18 | 16.8 | 1.1 | 4.5 | -29.7 (-29.7) | 15.3 / 26.0 | 15.3 | 3.4 (0, f92), 0.0 / 0.0 | 13.1 / 13.2 / yes | 96% / 3 / 0 (0 m) | in, sight 3.3 | **OK** |  |

End spot: 12 m short of the pin, 8 m over the ground (v4 default 12 / 8), pulled back per hole until the green fits (--end-fit).

Failed holes: none

Poster frames (first / rise / mid / approach / end) per hole are in flyover_gate.json; shots for the PC render in flyover_shots.json (7215 frames).
