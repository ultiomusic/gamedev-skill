**Short answer: hold off on both proposals for now. Neither is backed by this capture. First capture a player build, then test one change: thin the smoke.**

**Goal:** the boss fight holds 60 fps (16.67 ms per frame) on the target desktop. Boss telegraphs, threats, shadow contact cues and AI reactions have to stay as they are. A player-build capture of the same fight proves it.

## What the capture actually says

- At 60 fps you have 16.67 ms per frame. All three numbers fit inside that: main thread 9 ms, render thread 6 ms, GPU 11 ms.
- When the CPU and GPU run in parallel, the frame takes about as long as the slowest of them. Here that is 11 ms, or roughly 90 fps. But you see 40 fps, which is 25 ms. That leaves about 14 ms that none of these numbers explains.
- 9 + 6 + 11 = 26 ms, which is close to 25. Adding the threads together is the usual trap, and it would make any of them look guilty. CPU and GPU time overlap, so the sum is not a real frame cost.
- The capture was taken in the Editor with the profiler attached. That adds its own cost (the Editor loop, Scene view, profiler overhead) and doesn't show what the shipped game does. The Game view may also render at a different resolution than fullscreen, so GPU fill cost could be higher or lower in a real build.
- We also don't know whether "one capture" is a single frame or an average. A 40 fps average can come from many 16.7 ms frames mixed with spikes, or from vsync dropping frames to 33 ms. That would be a frame-time spike problem, not a steady per-frame cost.

## Ranked hypotheses

1. **The 25 ms comes from measurement or waiting, not from the arena's work.** The likely causes are Editor and profiler overhead, CPU/GPU sync stalls, vsync, or spikes hidden in an average. This ranks first because none of the measured thread times exceeds the budget. If it's true, the player build already runs close to 60 and none of the other changes is needed.
2. **GPU fill cost from the 12 full-screen translucent smoke layers.** The GPU is the largest of the three numbers. Twelve stacked full-screen layers means each pixel gets shaded and blended at least 12 times. That cost grows with resolution, so a fullscreen build could cost more than the Editor view. Dropping shadows or merging meshes does nothing about it. Transparent pixels that look empty still cost shading.
3. **Main-thread work from the AI: 400 raycasts plus 400 AI updates every frame.** It's plausible, but at 9 ms the main thread is under budget. It only matters if the player build shows the main thread as the limiting thread.
4. **Render-thread cost from 1200 draw calls.** At 6 ms this is the smallest number. Fewer draw calls don't by themselves make a frame shorter.
5. **Shadows.** We have no measurement of the shadow pass yet, so there's nothing to say they're expensive.

## About the team's two proposals

- **Merge every mesh into one:** this attacks the smallest number (render thread, 6 ms) and has real costs:
  - The engine can no longer skip parts of the arena that are off-camera (frustum culling), so the whole arena is drawn every frame.
  - It gets in the way of per-object materials, LODs and shadow settings.
  - It can increase GPU vertex work.

  If the build shows the render thread is the limit, instance repeated meshes and batch static meshes that share a material instead.
- **Drop shadows:** shadows give contact and silhouette cues, which matter for reading boss attacks and enemy positions. Only touch them if a GPU per-pass capture shows the shadow pass is expensive. Even then, try a shorter shadow distance, fewer cascades or fewer small shadow casters before turning shadows off.

## The capture that decides it

Measure the **player build** on the target desktop at the shipping resolution and quality settings, in fullscreen, with release-like settings:

- Use a repeatable sequence: the same arena, seed, camera path and boss phase. Warm up first, then record at least 60 s of sustained fighting. Keep the first-use spikes in a separate recording.
- Record frame-time distribution (median, p95, p99), not just the average.
- Record per-frame main-thread time, render-thread time and the wait/present markers.
- Record **GPU per-pass timings** from GPU timing markers or a GPU frame debugger: opaque, shadow, transparent/smoke and post-processing.
- Note whether vsync was on.
- Repeat the run 3 or more times to see how noisy it is.

What each result points to:

- **p95 already meets 16.7 ms in the build:** hypothesis 1 is confirmed. Stop optimizing the arena.
- **GPU-bound, with the transparent pass the largest:** run the smoke test below.
- **Main thread is the limit:** spread AI decisions across frames (see below).
- **Render thread is the limit:** use instancing or batch meshes that share a material. Don't merge everything.

## The one change to test first: cut the smoke overdraw

**Change:** replace the 12 stacked full-screen layers with a few layers (for example 2 or 3). Alternatively, render the smoke at half resolution and composite it back. Change only the smoke and keep everything else the same.

**Invariant:** at the normal gameplay camera, these stay readable:
- the boss telegraphs
- enemy silhouettes
- arena edges and hazards

Gameplay doesn't change: the same hits land and the same cues appear. The smoke still looks like the intended art.

**Accept or reject:** run the build capture above twice, with the original smoke and the reduced smoke, using the same sequence and device.

- **Accept** if the transparent-pass and total GPU time drop by more than the run-to-run noise, and p95 frame time moves toward 16.7 ms. Readability must hold when you compare the rendered frames.
- **Reject** if GPU time doesn't drop meaningfully, if the cost moves to another pass, or if any threat or telegraph gets harder to read.

I chose this as the first test because:
- the GPU is the largest measured cost, and full-screen overdraw is its most obvious source here;
- the change can be undone and doesn't touch gameplay state;
- unlike merging meshes, it doesn't break culling;
- unlike dropping shadows, it doesn't remove contact cues.

**If the main thread turns out to be the limit:** split the 400 enemies into 4 to 8 groups and give each group a new line-of-sight check and decision on one frame in turn. Movement and animation still run every frame. This needs three rules so that the AI stays fair:
- a cap on how many frames a decision can go stale;
- an urgent path for events like a player attack or a boss phase change, so they don't wait for their group's turn;
- a measurement of the added reaction delay.

## What I could not check

There's no project here. I don't know the engine and version, the render pipeline, the display resolution and vsync settings, the GPU model, or whether "one capture" is one frame or an average. I also don't know how the smoke is built (particles or full-screen quads/volumes), how the 9 ms splits between raycasts and AI logic, or the art direction for smoke and shadows. Everything above is a hypothesis from six numbers and three facts; nothing was measured or run.

I treated this as a Performance question and also used the Systems and 3D & Rendering guidance (for AI fairness and for shadow/smoke readability). No subagents ran: without a project or capture on disk, there was nothing for them to investigate beyond these numbers.

Not checked: any build, frame-time distribution or per-pass GPU cost. If you change shadows or smoke without a readability check, players can lose threat cues even though the frame rate looks better.
