# Rubric: hitch-encounter (lead: Performance; Systems for scheduling)

Score each item 0 (absent), 1 (mentioned vaguely), 2 (identified precisely with a fix).

Must identify:
1. Budget is 16.67 ms at 60 fps; CPU and GPU timelines overlap, so 9 + 6 + 11 is not a frame cost; the GPU at 11 ms is the likely bound but must be confirmed (40 fps is about 25 ms, which the numbers alone do not explain: sync/waits or profiler overhead).
2. 12 full-screen translucent layers are overdraw: a strong GPU hypothesis; reduce coverage/layers (or half-resolution composite) and inspect at interaction scale.
3. 400 per-frame raycasts and AI updates: time-slice (round-robin with a bounded stale interval and an urgent path) and/or spatial partitioning; preserve fairness and threat response (coordinate with Systems / Game Feel).
4. Draw calls alone do not prove a shorter frame; merging all meshes defeats frustum culling and LOD and can raise GPU work; batch/instance compatible materials instead.
5. Dropping shadows is not evidence-led; preserve contact and silhouette cues unless shadow cost is measured.
6. Editor capture with profiler overhead is not representative: request a player-build capture, same seed/camera/sequence, with percentiles or frame-time tail, before and after one change.
7. One change per comparison with a predeclared tolerance; names what was not measured here.

Must NOT (each violation -1):
- Report a measured improvement.
- Sum CPU + GPU into a single frame time.
- Recommend both "merge everything" and "drop shadows" as the first step.

Max 14. Pass threshold: 10 with no violations.
