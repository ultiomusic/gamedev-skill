# Boss arena: 40 fps vs 60 target

**Short answer:** don't do either yet. The capture doesn't show a bottleneck that shadows or mesh merging would fix. Measure a player build first. It may turn out you don't need to change any content.

## What the numbers say

- 60 fps means a 16.6 ms frame. 40 fps means about 25 ms.
- Each stage fits the budget: main thread 9 ms, render thread 6 ms, GPU 11 ms. If they overlapped normally, the frame would take about as long as the slowest stage (around 11 ms, so roughly 90 fps).
- 9 + 6 + 11 = 26 ms, which is about 38 fps. That matches "about 40 fps" closely. It suggests the stages are running one after another instead of overlapping, or that something outside these three numbers is using the frame. The likeliest suspect is the Editor with the profiler attached.

## Ranked hypotheses

1. **Measurement artifact or serialized pipeline (most likely).** The capture was taken in the Editor with the profiler attached. That adds Editor overhead (scene view, inspector, profiler collection) and can make the CPU wait for the GPU each frame, so the stages add up instead of overlapping. A real CPU-GPU sync point (a GPU readback, a blocking query, a vsync or frame-queue setting) would look the same, and it would still show in a build.
2. **GPU fill rate from the smoke.** 12 stacked full-screen translucent layers shade every pixel about 12 extra times. GPU is the largest stage (11 ms), and this is the most likely large real cost inside it, especially at 1440p or 4K.
3. **Shadows.** The shadow-caster passes add GPU time and probably a good share of the 1200 draw calls. They are a real cost but unmeasured. If they matter, tune them (cascades, distance, resolution, which objects cast shadows) instead of removing them.
4. **Main-thread AI.** 400 AI updates plus 400 raycasts every frame is a likely chunk of the 9 ms. Raycasts alone are usually cheap; the per-agent AI update is the bigger suspect. Fix it by spreading the work over frames (update 1/4 of the agents each frame, stagger line-of-sight checks) or batching the raycasts. This only matters if the main thread becomes the limiting stage.
5. **Draw calls (1200 at 6 ms render thread).** These are not the bottleneck on desktop. **Merging every mesh into one is a bad trade:** it turns off frustum and occlusion culling, LOD and per-object sorting, so the GPU draws the whole arena every frame. It also makes memory and iteration worse. It moves cost onto the GPU, which is already the largest stage. If draw calls ever do matter, use GPU instancing for the 400 enemies (same mesh) or batch the static scenery, not one giant mesh.

## The one change to test first

**Run the same scene as a player build instead of in the Editor.** This changes no content.

**Invariant (everything else stays the same):** same arena, same camera position or scripted path, all 400 enemies active, all 12 smoke layers and shadows on, same resolution and quality level, vsync off, same machine. Only the host changes, from Editor to player.

## The capture that decides it

Use a development player build with the profiler connected remotely (or a non-development build that logs frame timing). Capture about 300 frames in the boss fight, not a single frame. Record median and p95 for frame time, main thread, render thread and GPU time, and note any wait markers on the main thread or render thread (waiting for the GPU, waiting for present, waiting for the render thread).

How to read it:

- **Median frame is 16.6 ms or less:** it was the Editor and profiler. Change nothing in the content.
- **Frame time is close to the slowest stage, and GPU is over 16.6 ms:** the arena is GPU-bound. A/B test the smoke first (12 layers vs 2, or render it at half resolution), then shadow settings, and measure the change in GPU ms each time. Invariant: the smoke and shadows look the same in a fixed-camera screenshot comparison, within whatever difference art agrees to.
- **Frame time is close to the sum of the stages, and there are large wait markers:** there is a sync point. Find what is blocking (a readback, a query, the frame-queue setting) before touching any content.
- **Main thread is the slowest stage:** spread the AI and raycast work over frames. Invariant: enemy behaviour (detection range and how quickly enemies react) stays the same in a scripted test.

## What I could not check here

- The engine and version, render resolution, vsync and frame-queue settings, and the GPU or CPU model.
- Whether 9/6/11 ms are single-frame or average numbers, and whether they include wait time.
- Shadow settings, the smoke shader's cost, and the AI code.
- How a player build actually performs. Nothing was run, built or profiled. Everything above comes from one Editor capture, so the ranking is a hypothesis until the player-build capture is taken.
