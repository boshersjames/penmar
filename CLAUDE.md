# Penmar GSPro course

Real course rebuilt for GSPro (Unity 2018.2.8f1, OPCD). Toolkit: `../course-build` (the course-build repo). Read its
`README.md` once, then the skill for the element you are working on in `../course-build/skills/`. All thresholds come from
`../course-build/rules/*.json`; this course's overrides are in `course.json` under `rule_overrides`.

## Where things are
- `course.json`: frame, paths, GKD fields, tee slot map, overrides. Every script reads paths from here.
- Unity project: `C:\GSP\Penmar_Project`. Editor tools in `Assets\Editor\` are copies from `../course-build\unity\shared\`; sync with
  `../course-build\automation\Run-CourseAutomation.ps1 -SyncTools`.
- Automation output: `C:\GSP\Penmar_Project\AutomationOutput\latest.txt` then that folder's `summary.md` and `shots\`.
- Never change `C:\GSProV1\Core\GSP\Courses\` without backing up the GKD first.

## Driving Unity
- Unity closed: `../course-build\automation\Run-CourseAutomation.ps1 -Config automation\Penmar.json [-Steps "a,b"]`.
- Unity open: `../course-build\automation\Send-UnityCommand.ps1 <ping|run|shots|invoke|describe|menu|save|refresh>`.

## Process
Follow `course-build-gates`: one hole, one edit, photo pair each; control hole before/after on course-wide passes; back up
scene, terrain and GKD before every change. Run the LiDAR review (D1-D18) before the first gate and record answers in
`course_photos/decisions.csv`.

## Cost discipline
Measure with tools, not eyes. Colour: `colour_match.py`. Green edges: the edge survey. Pins: the pin-area test. Read the
summary a tool writes; open a render only when a number says something is wrong.

## This course
Split out of the moorpark repo (branch `claude/project-thread-j2x22i`, `courses/penmar`). `README.md` has the full data history.
- Frame: 2000 m square centred on 34.006362, -118.459344 (EPSG:6340, SW 364237.29 E, 3762821.35 N), y = elevation - 4 m,
  Unity Terrain 2000 x 43 x 2000. Ground 5.8 to 45.5 m.
- Survey: USGS 3DEP `CA_LosAngeles_1_B23` (QL1, 2023-24), 17.2 pts/m2. Satellite NAIP 4096 px (0.49 m/px).
- 9 physical holes played as 18 in `Penmar.GKD` (`--repeat-nine`): 10-18 replay 1-9 from the Alt tees. `holes` = 18 (enabled
  GKD holes, what the tools loop over); `holes_physical` = 9.
- `course.json` carries coursekit's keys beside the toolkit's; keep both in step. `paths.gkd` is `Penmar.GKD` at the repo root.
- Heightmap: `heightmap_2049.raw` was rebuilt here from USGS 3DEP (not in the moorpark repo); to rebuild, from inside this folder run
  `python ../moorpark/coursekit.py lidar --ept CA_LosAngeles_1_B23` then `python ../moorpark/coursekit.py heightmap`. See README.md.
- Open questions: Alt tee pads on 12, 14, 15, 16, 18; the restroom location; net lengths; the 8th-tee PT-22 model.
