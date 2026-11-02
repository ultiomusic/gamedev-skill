# Case: boss arena below budget

User request: "The boss arena runs at about 40 fps on a desktop that should do 60. Profiler, one
capture: CPU main thread 9 ms, render thread 6 ms, GPU 11 ms, 1200 draw calls. The team wants to
drop shadows and merge every mesh into one. What should we actually do?"

No project is on disk; this is the only evidence. Also in the arena:

- 400 enemies each run a raycast to the player every frame and update AI every frame.
- 12 full-screen translucent smoke layers are stacked over the arena.
- The capture was taken in the Editor with the profiler attached; no player build was measured.

Return the ranked hypotheses, the one change you would test first with its invariant, and the capture
that would decide it. State what you could not check here.
