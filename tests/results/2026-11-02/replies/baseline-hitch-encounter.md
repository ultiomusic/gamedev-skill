# Boss arena at 40 fps: what to actually do

**Short answer:** do neither of the team's changes yet. Merging every mesh would break the enemies. Dropping shadows targets a cost nobody has measured. The capture you have was taken in the Editor, so start by measuring a player build. After that, the first change to test is probably reducing the smoke's fill cost.

**The goal:** a steady 60 fps (16.7 ms per frame) in the boss arena on the target desktop. The same seed should still produce the same enemy reactions, and the smoke, enemies and boss telegraphs should read the same at the gameplay camera.

**How I ran this:** Performance was the lead specialist. I ran it as one read-only subagent (a general-purpose `Agent` worker given the Performance brief). I didn't run Systems or 3D & Rendering separately; their parts are listed under "Handoffs" below. Nothing was executed, built or profiled. Everything here is reasoning from the numbers in your message.

## What the one capture does and doesn't show

The capture shows main thread 9 ms, render thread 6 ms, GPU 11 ms and 1200 draw calls. **Each of those fits inside 16.7 ms on its own.** These threads normally run in parallel, so a healthy frame would take roughly the longest one (about 11 ms) plus waits. The ~25 ms you're seeing is close to their sum (26 ms). That suggests one of these:

- the work is being forced to run one after another (a sync point or GPU readback, or the Editor and profiler serializing it)
- there is Editor cost that isn't in these markers
- vsync is rounding frame times up. On a 120 Hz display, 25 ms is exactly 3 refreshes. On a 60 Hz display, "40 fps" usually means frames alternating between 16.7 ms and 33.3 ms, which is a frame-pacing problem rather than too much work.

A single Editor capture with the profiler attached can't tell these apart, and it says nothing about the shipped build.

## Ranked hypotheses

1. **The Editor or a sync wait is causing most of the gap.** This is the most likely explanation, because the numbers add up instead of overlapping. The player build may already be close to budget.
2. **Smoke overdraw on the GPU.** Twelve full-screen translucent layers blend every pixel at least 12 times. That is the largest cost visible, and the GPU is the longest single track.
3. **AI on the main thread.** 400 AI updates and 400 raycasts run every frame. The AI logic is the more likely cost; single raycasts are usually cheap. The capture doesn't separate the two.
4. **Draw-call submission (6 ms on the render thread).** 1200 draw calls is moderate for a desktop. This only matters if a build capture shows the render thread holding up the frame.
5. **Shadows.** Nothing in the capture isolates their cost.

## The team's two proposals

- **Merging every mesh into one: reject.** The 400 enemies move and animate independently. One merged mesh breaks culling, LOD, transparent sort order and per-object materials, and fewer draw calls don't by themselves make a frame shorter. If the build shows submission is the bottleneck, use instancing or static batching on the **static arena geometry only**.
- **Dropping shadows: not yet.** Shadows help players see where enemies are standing, and their cost hasn't been measured. Turn shadows off in a test run to measure them, not as the fix.

## First step: measure, then test one change

**Step 0, measure.** Make a development player build with profiling markers and run it on the target desktop at the shipping resolution and quality settings.
- Use the same boss-arena state each time: all 400 enemies active, all smoke on screen, a fixed seed and a fixed camera path.
- Warm up for 10 s, capture for 60 s, and repeat 3 times.
- Turn vsync and the frame limiter off for the cost runs. Do one extra run with vsync on, and record the display's refresh rate.
- Record these markers:
  - main-thread total
  - AI update
  - raycasts/physics queries
  - render-thread submit
  - wait-for-GPU, wait-for-render-thread and present
  - GC and allocations
  - per-pass GPU times for shadows, opaque geometry and smoke/transparents (from a GPU profiler or frame debugger)
- Then do one run each with a single thing turned off: **smoke off**, **shadows off**, **AI and raycasts frozen**. This shows how much each one costs.

**First change, if the smoke-off run shows smoke is the biggest GPU cost:** cut the smoke's fill cost. Either merge the 12 layers into fewer, or draw them into a half-resolution buffer and composite it once.
- **What must not change:** gameplay code stays untouched, so the same seed gives the same enemy reactions. At the gameplay camera, smoke density, coverage and silhouette must match the old version in side-by-side screenshots. Boss and enemy telegraphs must stay as visible as before.
- **Keep it if:** frame time is at or under 15 ms for the median frame and at or under 16.7 ms for the slowest 1% (p50 and p99), **and** GPU time drops by at least 1 ms and by more than twice the run-to-run variation.
- **Drop it if:** the cost moves to another thread, frame pacing gets worse, or the smoke or telegraphs become harder to read.

If the build shows a different biggest cost, test that one first instead:
- main thread → AI (see Systems below)
- render thread → static batching of the arena
- a sync or present wait → find what the frame is waiting on

## Handoffs

- **3D & Rendering:** picks how to reduce the smoke and checks that it still reads correctly. Makes the call on shadows if their test run shows they cost a lot.
- **Systems:** needed only if the main thread is the bottleneck. AI and raycasts could run every 2–4 frames, staggered across enemies. That needs a cap on how stale an enemy's reaction can get (for example ≤100 ms). It also needs an immediate update whenever line of sight changes, an enemy is hit, or the player is close, so every enemy still reacts correctly.

## What I couldn't check

There is no project, build, engine or hardware here, so nothing was measured, and none of these timings were estimated. Still unknown:
- the display refresh rate and whether vsync is on
- the resolution
- whether the "GPU 11 ms" is measured or an Editor estimate
- whether the 9 ms includes the Editor's own loop
- whether the numbers are averages or include spikes
- memory and GC behaviour
- what shadows and AI actually cost

The main risk is that the team optimizes against Editor numbers while the real limit is vsync pacing or a sync stall.
