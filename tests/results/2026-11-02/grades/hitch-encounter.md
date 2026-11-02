# Blind grade: hitch-encounter

Rubric: 7 items x 0-2 (max 14), -1 per must-not violation. Pass: >= 10 with no violations.

## Item scores

| # | Item | A | B | C |
|---|------|---|---|---|
| 1 | Budget 16.67 ms; overlap, sum is not frame cost; GPU likely bound, confirm; 25 ms unexplained | 2 - "threads normally run in parallel ... roughly the longest one (about 11 ms)" | 2 - "CPU and GPU time overlap, so the sum is not a real frame cost" | 2 - "If they overlapped normally ... as long as the slowest stage" |
| 2 | Smoke overdraw; fewer layers / half-res; inspect at interaction scale | 2 - "merge the 12 layers into fewer, or ... half-resolution buffer" + "at the gameplay camera" | 2 - "a few layers (for example 2 or 3) ... half resolution"; "at the normal gameplay camera" | 2 - "12 layers vs 2, or render it at half resolution"; "fixed-camera screenshot comparison" |
| 3 | AI/raycasts: time-slice, bounded staleness, urgent path; fairness; Systems | 2 - "cap on how stale ... (for example <=100 ms)"; "immediate update whenever line of sight changes" | 2 - "a cap on how many frames a decision can go stale"; "an urgent path" | 1 - "update 1/4 of the agents each frame" (no staleness cap, no urgent path) |
| 4 | Draw calls alone != shorter frame; merge-all kills culling/LOD, raises GPU; instance/batch | 2 - "breaks culling, LOD"; "instancing or static batching on the static arena geometry only" | 2 - "can increase GPU vertex work"; "instance repeated meshes and batch static meshes" | 2 - "turns off frustum and occlusion culling, LOD"; "GPU instancing ... or batch the static scenery" |
| 5 | Shadows not evidence-led; keep contact/silhouette cues unless measured | 2 - "Shadows help players see where enemies are standing"; "test run to measure them" | 2 - "shadows give contact and silhouette cues"; "Only touch them if a GPU per-pass capture" | 1 - "real cost but unmeasured ... tune them" (no gameplay-cue argument) |
| 6 | Player-build capture, same seed/camera/sequence, percentiles, before/after | 2 - "fixed seed and a fixed camera path"; "p50 and p99" | 2 - "same arena, seed, camera path and boss phase"; "median, p95, p99" | 2 - "Record median and p95"; "same camera position or scripted path" (no seed) |
| 7 | One change per comparison, predeclared tolerance; names what was not measured | 2 - "GPU time drops by at least 1 ms and by more than twice the run-to-run variation" | 2 - "drop by more than the run-to-run noise"; "Repeat the run 3 or more times" | 1 - "within whatever difference art agrees to" (tolerance deferred; no repeats/noise) |

## Must-not violations

- Report a measured improvement: none. A "nothing was measured"; B "nothing was measured or run"; C "Nothing was run, built or profiled".
- Sum CPU + GPU into a single frame time: none counted. All three compute 26 ms but frame it against the overlap model. C comes closest ("9 + 6 + 11 = 26 ms, which is about 38 fps. That matches"), but it treats that as a sign of serialization, not as the frame cost.
- Recommend merge-all and drop-shadows as the first step: none. All three reject both.

## Summary

| Reply | Items 1..7 | Violations | Total | PASS/FAIL |
|-------|-----------|------------|-------|-----------|
| A | 2, 2, 2, 2, 2, 2, 2 | 0 | 14 | PASS |
| B | 2, 2, 2, 2, 2, 2, 2 | 0 | 14 | PASS |
| C | 2, 2, 1, 2, 1, 2, 1 | 0 | 11 | PASS |

## Extra notes (not scored)

- **A.** Useful: the vsync arithmetic (25 ms = 3 refreshes at 120 Hz; 40 fps at 60 Hz as 16.7/33.3 alternation), the single-factor isolation runs (smoke off / shadows off / AI frozen), and GC markers. Error: Hypothesis 1 states "the numbers add up instead of overlapping" as fact. The 26 ≈ 25 match is weak, possibly coincidental evidence.
- **B.** Useful: the Editor Game-view resolution may differ from fullscreen, which changes fill cost; it keeps first-use spikes in a separate recording; it tunes shadows (distance, cascades) before removing them; and it notes that transparent pixels that look empty still cost shading. Error: none found.
- **C.** Useful: it names concrete sync causes (GPU readback, blocking query, frame-queue setting) and gives a decision tree that compares frame time with the slowest stage and with the sum. Errors:
  - It leans on the sum match as evidence.
  - It asserts without evidence that draw calls "are not the bottleneck" and that shadows are "probably a good share of the 1200 draw calls".
  - GPU instancing for 400 animated enemies assumes they are not skinned meshes, or it needs special handling.
  - Its "first change" is the measurement host (Editor to player), not a content change.
  - The GPU-bound branch triggers only when GPU > 16.6 ms, so a GPU close to the budget is not covered.
