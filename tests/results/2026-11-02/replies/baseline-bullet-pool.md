**Short answer: don't do either yet.** Neither "pool everything" nor "lower shadow resolution" fits what your code shows.

- Shadow cost is roughly the same every frame. It can't explain a hitch that comes back every few seconds, and lowering it makes the game look worse.
- Pooling everything adds more objects that each need a full reset. Your pool's reuse bugs show that cost already.
- The 45 fps Editor average says nothing about a spike.

Your code shows two separate problems:
- **Reused bullets keep the previous shot's state.** That is a correctness bug, and it is certain from the snippet.
- **Every hit allocates new objects.** That is a likely cause of the stutter, but it is a hypothesis until you measure it.

**Goal:** sustained fire keeps steady frame times. Every shot starts from its own state, resolves exactly once, and shows exactly one hit flash.

## 1. Fix reuse: reset everything in Acquire and have one exit (certain from the code)

`Acquire` never resets `velocity`, `homingTarget`, `lifetime`, the trail or the `OnHit` listeners. `OnBulletHit` has no guard either.

- **Old target:** a shot with no target keeps the previous bullet's `homingTarget`. That target may have died while the bullet sat in the pool. This assumes your fire code only assigns a target when one exists, which I can't see.
- **Invisible:** the likeliest causes are:
  - leftover `lifetime <= 0`, which kills the bullet on its first frame;
  - a stale trail;
  - a **double release**. A hit plus an expiry, or two colliders in one frame, pushes the same bullet twice. Two later shots then share one instance, so one of them "disappears".
- **Listener build-up:** if `OnHit +=` runs on every fire, one hit runs N times: N damage settlements, N flashes and N pushes. It also gets worse the longer you play.

Smallest change, keeping your pool, prefab, damage rules and one flash per hit:

```text
Acquire(pos, dir, speed, target /*may be null*/):
  b = inactive.Pop() ?? Instantiate(prefab)   // subscribe OnHit -> Resolve ONCE, at creation only
  b.gen++                                      // invalidates stale callbacks
  b.position = pos; b.velocity = dir * speed
  b.homingTarget = target                      // always assigned, including null
  b.lifetime = prefab.lifetime
  b.trail.Clear()                              // after moving, before visible
  b.active = true                              // commit point, last
  return b

Resolve(b, gen, hit /*null = expired*/):       // the only exit, for hits AND expiry
  if (!b.active || gen != b.gen) return        // no double release, no hit-after-release
  b.active = false
  if hit: apply damage once; raise one hit cue
  b.homingTarget = null                        // the pool never holds a target
  inactive.Push(b)

Homing tick: if target is null or dead -> clear it and fly straight
```

Also send misses and expired bullets through `Resolve`. Otherwise the pool keeps instantiating during combat. Once the capture below gives you the measured peak (you estimate about 60), pre-warm the pool to that number plus some margin. Keep the `Instantiate` fallback so no shot is ever dropped, but count how often it fires.

## 2. Likely cause of the stutter: each hit allocates a flash (hypothesis)

Every hit creates a new MuzzleFlash quad with **its own material instance** and destroys it 0.2 s later. Under sustained fire that is a steady stream of garbage, and a hitch every few seconds is the typical pattern of a garbage-collection pause.

Two things make it worse:
- Depending on the engine, destroying the quad may not free its material instance, so materials could pile up in memory.
- Listener build-up multiplies the flashes.

Smallest change: pool a small fixed set of flash quads (enough for the peak hits per 0.2 s) that share **one material**. Set the per-flash fade through your engine's per-instance properties. This keeps the cue the player relies on: one flash per hit, for the same 0.2 s, with the same look and draw order.

Pool only this flash and the bullets. Don't pool anything else unless the capture shows it churning.

## What measurement decides it

Use a **development player build with profiling enabled**, on your target device rather than in the Editor. Fix the scene, seed and camera, and script the firing:
1. A first burst.
2. About 60 s of sustained fire after warm-up.
3. A return to idle.

Record:
- **CPU:** garbage-collection events and bytes allocated per frame and per hit; Instantiate, Destroy and material-creation counts.
- **Over time:** material count, managed heap size, OnHit handler count per hit, and pool size.
- **GPU:** transparent-pass and shadow-pass time. This is where you would see a shadow cause. I expect none.
- **Frame time:** median, a high percentile, the maximum, and when each spike happens.
- **Gameplay:** shots fired vs hits registered vs flashes shown.

Then make one change at a time (first the reuse fix, then flash pooling) and capture the same sequence again.

**A cause is ruled out** if its markers don't line up with the spikes.

**Reject a fix if any of these is true:**
- The frame-time tail doesn't improve beyond a tolerance you set before the run.
- The hitch moves somewhere else.
- Memory goes over budget.
- Any shot, hit or flash goes missing.

**For the reuse fix:** pre-warm the pool with 1 bullet and fire:
- A homing shot that kills its target.
- A shot with no target.
- A shot that expires.
- A forced hit and expiry on the same frame.

Repeat that cycle 50 times. Compare every reused bullet's velocity, target, lifetime, visibility and trail against a fresh instance. Settlements, flashes and pushes per shot must each be 1, and `inactive` must never contain a duplicate.

## What I could not check

- There is no project here, so nothing was run, profiled or tested. Everything above comes from the snippet.
- **Not visible in the snippet:**
  - the expiry path, which is the biggest risk: if it also pushes, that is the double release;
  - where `OnHit` is subscribed;
  - where `homingTarget` is set;
  - whether `active` is the engine's own active flag;
  - how your engine frees materials on destroy.
- **No timings exist.** Once a capture exists, the ranking of the stutter causes could change.

I ran two specialists in parallel, both read-only: Performance on the stutter and Systems on the reuse state. Rendering wasn't consulted. When you switch the flash to a shared material, check by eye that it looks the same as before.
