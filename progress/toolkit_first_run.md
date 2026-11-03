# First headless toolkit run (2026-11-03)

Run from the course folder, course-build at e6d245d pose_solve.py: LiDAR+tree skyline fit per photo, diagnostic by default (validated on Tierra: applying it is worse than the compass); flip check; rule block.

## doctor.py

```
ok   course.json                            /home/user/penmar/course.json
ok   paths.toolkit                          /home/user/course-build
ok   heightmap size                         8396802 bytes (= 2049^2 x 2)
ok   gkd parses                             Penmar Golf Course: 18 holes, 18 enabled
ok   svg greens match gkd                   11 outlines, 18 of 18 enabled holes matched
ok   paths.satellite                        /home/user/penmar/satellite.jpg
ok   paths.trees_csv                        /home/user/penmar/trees.csv
WARN paths.signs                            missing (/home/user/penmar/progress/hole_signs.json)
WARN paths.photos_root                      missing (/home/user/penmar/course_photos)
ok   python numpy                           
ok   python scipy                           
ok   python matplotlib                      
ok   python PIL                             
ok   python pyproj                          
ok   python laspy                           
ok   python pillow_heif                     
ok   tool git                               
ok   tool git-lfs                           
ok   tool ffmpeg                            
ok   tool yt-dlp                            
info unity_project                          C:/GSP/Penmar_Project not on this machine
info automation latest run                  none here

0 FAIL, 2 WARN
[exit 0]
```

## gkd_tools.py check

```
25 checks, 0 failing
[exit 0]
```

## green_report.py --smooth 0.6

```
# Green report (penmar, surface: course heightmap order 3, low-pass sigma 0.6 m)

Rules: pin area <= 1.7 deg over 17 points, pins >= 3 m from the edge, >= 4 valid areas >= 3 m apart; internal slope 1-3%.

| hole | area m2 | relief m | slope mean/p90 % | >3% | pins fail | pin angles | usable % | areas | flag | pass |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 367 | 0.27 | 1.4 / 1.9 | 5 | 0/4 | Thu:0.7 Fri:0.6 Sat:0.7 Sun:0.9 | 93 | 33 |  | PASS |
| 2 | 453 | 0.37 | 1.2 / 2.0 | 1 | 1/4 | Thu:0.5 Fri:0.7 Sat:0.5 Sun:0.8 | 92 | 39 |  | FAIL |
| 3 | 341 | 0.43 | 1.5 / 2.7 | 8 | 1/4 | Thu:0.8 Fri:1.8 Sat:0.8 Sun:0.9 | 88 | 28 |  | FAIL |
| 4 | 352 | 0.36 | 1.3 / 2.2 | 2 | 2/4 | Thu:0.8 Fri:1.1 Sat:1.0 Sun:0.9 | 94 | 32 |  | FAIL |
| 5 | 411 | 0.24 | 1.2 / 2.0 | 0 | 0/4 | Thu:0.4 Fri:0.8 Sat:0.7 Sun:0.8 | 94 | 37 |  | PASS |
| 6 | 317 | 0.20 | 0.9 / 1.6 | 1 | 2/4 | Thu:0.3 Fri:0.5 Sat:1.3 Sun:0.6 | 96 | 28 | flat <1% | FAIL |
| 7 | 415 | 0.17 | 0.8 / 1.8 | 0 | 0/4 | Thu:0.5 Fri:0.4 Sat:0.4 Sun:0.5 | 98 | 40 | flat <1% | PASS |
| 8 | 490 | 0.23 | 0.9 / 1.7 | 1 | 0/4 | Thu:0.5 Fri:0.6 Sat:0.2 Sun:0.8 | 97 | 44 | flat <1% | PASS |
| 9 | 408 | 0.42 | 1.4 / 2.2 | 2 | 2/4 | Thu:0.8 Fri:1.5 Sat:1.8 Sun:0.6 | 92 | 36 |  | FAIL |
| 10 | 367 | 0.27 | 1.4 / 1.9 | 5 | 0/4 | Thu:0.7 Fri:0.6 Sat:0.7 Sun:0.9 | 93 | 33 |  | PASS |
| 11 | 453 | 0.37 | 1.2 / 2.0 | 1 | 1/4 | Thu:0.5 Fri:0.7 Sat:0.5 Sun:0.8 | 92 | 39 |  | FAIL |
| 12 | 341 | 0.43 | 1.5 / 2.7 | 8 | 1/4 | Thu:0.8 Fri:1.8 Sat:0.8 Sun:0.9 | 88 | 28 |  | FAIL |
| 13 | 352 | 0.36 | 1.3 / 2.2 | 2 | 2/4 | Thu:0.8 Fri:1.1 Sat:1.0 Sun:0.9 | 94 | 32 |  | FAIL |
| 14 | 411 | 0.24 | 1.2 / 2.0 | 0 | 0/4 | Thu:0.4 Fri:0.8 Sat:0.7 Sun:0.8 | 94 | 37 |  | PASS |
| 15 | 317 | 0.20 | 0.9 / 1.6 | 1 | 2/4 | Thu:0.3 Fri:0.5 Sat:1.3 Sun:0.6 | 96 | 28 | flat <1% | FAIL |
| 16 | 415 | 0.17 | 0.8 / 1.8 | 0 | 0/4 | Thu:0.5 Fri:0.4 Sat:0.4 Sun:0.5 | 98 | 40 | flat <1% | PASS |
| 17 | 490 | 0.23 | 0.9 / 1.7 | 1 | 0/4 | Thu:0.5 Fri:0.6 Sat:0.2 Sun:0.8 | 97 | 44 | flat <1% | PASS |
| 18 | 408 | 0.42 | 1.4 / 2.2 | 2 | 2/4 | Thu:0.8 Fri:1.5 Sat:1.8 Sun:0.6 | 92 | 36 |  | FAIL |
wrote progress/green_report
[exit 0]
```

## flyover_gate.py --end-fit --no-plots

```
no signs file at /home/user/penmar/progress/hole_signs.json: provisional sign spots from the back tees
hole  1: 403 frames  16.1 s (x1.00) yaw/1s 0.23 pitch/1s 4.50 | end pitch -29.3 (pin -29.3) h 13.2 m, 22.5 m short | terrain 13.2 m crown 5.2 m (tree 29, lift 0.0/0.0) | first: crown 12.8 sight 12.2 in-frame True | green 100% (cut off 0, pull-back 0.0) pin True sight 11.5 -> OK
hole  2: 454 frames  18.2 s (x1.00) yaw/1s 1.16 pitch/1s 4.50 | end pitch -29.6 (pin -29.6) h 15.9 m, 27.5 m short | terrain 15.9 m crown 4.3 m (tree 16, lift 0.0/0.0) | first: crown 8.4 sight 8.6 in-frame True | green 91% (cut off 0, pull-back 0.0) pin True sight 4.9 -> OK
hole  3: 317 frames  12.7 s (x1.00) yaw/1s 0.00 pitch/1s 3.63 | end pitch -29.5 (pin -29.5) h 14.8 m, 25.5 m short | terrain 14.8 m crown 1.5 m (tree 425, lift 0.0/0.0) | first: crown 3.1 sight 2.2 in-frame True | green 100% (cut off 0, pull-back 0.0) pin True sight 4.0 -> OK
hole  4: 414 frames  16.6 s (x1.00) yaw/1s 1.41 pitch/1s 4.50 | end pitch -29.6 (pin -29.6) h 12.8 m, 22.0 m short | terrain 12.8 m crown 2.4 m (tree 195, lift 0.0/0.0) | first: crown 5.7 sight 5.7 in-frame True | green 100% (cut off 0, pull-back 0.0) pin True sight 5.6 -> OK
hole  5: 339 frames  13.6 s (x1.00) yaw/1s 0.00 pitch/1s 4.50 | end pitch -29.7 (pin -29.7) h 12.7 m, 21.5 m short | terrain 12.7 m crown 2.8 m (tree 199, lift 0.0/0.0) | first: crown 5.2 sight 5.0 in-frame True | green 100% (cut off 0, pull-back 0.0) pin True sight 4.9 -> OK
hole  6: 537 frames  21.5 s (x1.00) yaw/1s 0.09 pitch/1s 4.50 | end pitch -30.1 (pin -30.1) h 14.4 m, 24.5 m short | terrain 14.4 m crown 4.1 m (tree 245, lift 0.0/0.0) | first: crown 7.0 sight 6.4 in-frame True | green 96% (cut off 0, pull-back 0.0) pin True sight 7.1 -> OK
hole  7: 455 frames  18.2 s (x1.00) yaw/1s 0.18 pitch/1s 4.50 | end pitch -29.5 (pin -29.5) h 13.8 m, 23.5 m short | terrain 13.7 m crown 3.5 m (tree 220, lift 0.0/3.0) | first: crown 5.5 sight 5.6 in-frame True | green 100% (cut off 0, pull-back 0.0) pin True sight 8.9 -> OK
hole  8: 317 frames  12.7 s (x1.00) yaw/1s 0.00 pitch/1s 3.82 | end pitch -29.9 (pin -29.9) h 15.6 m, 27.0 m short | terrain 15.6 m crown 4.3 m (tree 311, lift 0.0/0.0) | first: crown 5.6 sight 5.6 in-frame True | green 94% (cut off 0, pull-back 0.0) pin True sight 4.2 -> OK
hole  9: 469 frames  18.8 s (x1.00) yaw/1s 0.97 pitch/1s 4.50 | end pitch -29.7 (pin -29.7) h 15.3 m, 26.0 m short | terrain 15.3 m crown 2.6 m (tree 204, lift 0.0/6.7) | first: crown 6.6 sight 6.6 in-frame True | green 96% (cut off 0, pull-back 0.0) pin True sight 3.3 -> OK
hole 10: 400 frames  16.0 s (x1.00) yaw/1s 0.24 pitch/1s 4.50 | end pitch -29.3 (pin -29.3) h 13.2 m, 22.5 m short | terrain 13.2 m crown 5.0 m (tree 29, lift 0.0/0.0) | first: crown 12.3 sight 11.7 in-frame True | green 100% (cut off 0, pull-back 0.0) pin True sight 11.5 -> OK
hole 11: 448 frames  17.9 s (x1.00) yaw/1s 1.18 pitch/1s 4.50 | end pitch -29.6 (pin -29.6) h 15.9 m, 27.5 m short | terrain 15.9 m crown 4.4 m (tree 16, lift 0.0/0.0) | first: crown 9.8 sight 9.0 in-frame True | green 91% (cut off 0, pull-back 0.0) pin True sight 4.9 -> OK
hole 12: 317 frames  12.7 s (x1.00) yaw/1s 0.00 pitch/1s 4.50 | end pitch -29.5 (pin -29.5) h 14.8 m, 25.5 m short | terrain 14.8 m crown 4.0 m (tree 271, lift 0.0/0.0) | first: crown 9.3 sight 8.9 in-frame True | green 100% (cut off 0, pull-back 0.0) pin True sight 3.3 -> OK
hole 13: 414 frames  16.6 s (x1.00) yaw/1s 1.41 pitch/1s 4.50 | end pitch -29.6 (pin -29.6) h 12.8 m, 22.0 m short | terrain 12.8 m crown 2.4 m (tree 195, lift 0.0/0.0) | first: crown 5.7 sight 5.7 in-frame True | green 100% (cut off 0, pull-back 0.0) pin True sight 5.6 -> OK
hole 14: 317 frames  12.7 s (x1.00) yaw/1s 0.00 pitch/1s 3.58 | end pitch -29.7 (pin -29.7) h 12.4 m, 21.0 m short | terrain 12.3 m crown 4.0 m (tree 326, lift 0.0/0.0) | first: crown 5.7 sight 5.7 in-frame True | green 100% (cut off 0, pull-back 0.0) pin True sight 4.7 -> OK
hole 15: 475 frames  19.0 s (x1.00) yaw/1s 0.15 pitch/1s 4.50 | end pitch -30.1 (pin -30.1) h 14.4 m, 24.5 m short | terrain 14.4 m crown 6.4 m (tree 326, lift 0.0/0.0) | first: crown 7.6 sight 7.6 in-frame True | green 96% (cut off 0, pull-back 0.0) pin True sight 7.1 -> OK
hole 16: 401 frames  16.0 s (x1.00) yaw/1s 0.27 pitch/1s 4.50 | end pitch -29.5 (pin -29.5) h 13.8 m, 23.5 m short | terrain 13.7 m crown 1.7 m (tree 209, lift 0.0/0.0) | first: crown 5.3 sight 5.2 in-frame True | green 100% (cut off 0, pull-back 0.0) pin True sight 8.9 -> OK
hole 17: 317 frames  12.7 s (x1.00) yaw/1s 0.00 pitch/1s 3.70 | end pitch -29.9 (pin -29.9) h 15.6 m, 27.0 m short | terrain 15.6 m crown 2.7 m (tree 68, lift 0.0/0.0) | first: crown 10.1 sight 10.1 in-frame True | green 94% (cut off 0, pull-back 0.0) pin True sight 4.1 -> OK
hole 18: 421 frames  16.8 s (x1.00) yaw/1s 1.11 pitch/1s 4.50 | end pitch -29.7 (pin -29.7) h 15.3 m, 26.0 m short | terrain 15.3 m crown 3.4 m (tree 0, lift 0.0/0.0) | first: crown 13.1 sight 13.2 in-frame True | green 96% (cut off 0, pull-back 0.0) pin True sight 3.3 -> OK
Failed holes: none

Poster frames (first / rise / mid / approach / end) per hole are in flyover_gate.json; shots for the PC render in flyover_shots.json (7215 frames).
[exit 0]
```

## gate_report.py

```
# Gate report: penmar (18 holes)

Sources: flyover, lidar-proxy. Missing: Unity CourseGreenChecks (checks/greens_all18.csv): run Course Checks > Greens on the PC.

GKD checks: all pass

| hole | source | step cm | lip cm | col dy | tiers | crown m | pins fail | usable % | areas | fall dir | flyover | result |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | lidar-proxy+flyover | - | - | - | - | - | 0 | 93 | 33 | - | PASS | PASS |
| 2 | lidar-proxy+flyover | - | - | - | - | - | 1 | 92 | 39 | - | PASS | PASS warn: pins(lidar) |
| 3 | lidar-proxy+flyover | - | - | - | - | - | 1 | 88 | 28 | - | PASS | PASS warn: pins(lidar) |
| 4 | lidar-proxy+flyover | - | - | - | - | - | 2 | 94 | 32 | - | PASS | PASS warn: pins(lidar) |
| 5 | lidar-proxy+flyover | - | - | - | - | - | 0 | 94 | 37 | - | PASS | PASS |
| 6 | lidar-proxy+flyover | - | - | - | - | - | 2 | 96 | 28 | - | PASS | PASS warn: pins(lidar) |
| 7 | lidar-proxy+flyover | - | - | - | - | - | 0 | 98 | 40 | - | PASS | PASS |
| 8 | lidar-proxy+flyover | - | - | - | - | - | 0 | 97 | 44 | - | PASS | PASS |
| 9 | lidar-proxy+flyover | - | - | - | - | - | 2 | 92 | 36 | - | PASS | PASS warn: pins(lidar) |
| 10 | lidar-proxy+flyover | - | - | - | - | - | 0 | 93 | 33 | - | PASS | PASS |
| 11 | lidar-proxy+flyover | - | - | - | - | - | 1 | 92 | 39 | - | PASS | PASS warn: pins(lidar) |
| 12 | lidar-proxy+flyover | - | - | - | - | - | 1 | 88 | 28 | - | PASS | PASS warn: pins(lidar) |
| 13 | lidar-proxy+flyover | - | - | - | - | - | 2 | 94 | 32 | - | PASS | PASS warn: pins(lidar) |
| 14 | lidar-proxy+flyover | - | - | - | - | - | 0 | 94 | 37 | - | PASS | PASS |
| 15 | lidar-proxy+flyover | - | - | - | - | - | 2 | 96 | 28 | - | PASS | PASS warn: pins(lidar) |
| 16 | lidar-proxy+flyover | - | - | - | - | - | 0 | 98 | 40 | - | PASS | PASS |
| 17 | lidar-proxy+flyover | - | - | - | - | - | 0 | 97 | 44 | - | PASS | PASS |
| 18 | lidar-proxy+flyover | - | - | - | - | - | 2 | 92 | 36 | - | PASS | PASS warn: pins(lidar) |
wrote progress/gate_report
[exit 0]
```
