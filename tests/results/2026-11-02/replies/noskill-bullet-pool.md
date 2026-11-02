**Short answer: don't pool everything, and don't lower shadow resolution yet.** Your pool is in place, but two parts of it are wrong, and the hit effect isn't pooled at all. Both of your visual bugs come from those two pool defects. The stutter most likely comes from the unpooled hit effect, but you need one profiler capture to confirm that before changing anything else.

## What the fragments show

1. **Reused bullets keep state from their last life.** `Acquire` sets only `active` and `position`. So a recycled bullet still has its old `velocity` and `homingTarget`, which is why it flies toward an old target. It also keeps its old `lifetime` and trail. If the lifetime has already run out, the bullet is switched off almost immediately. If the trail still holds points from where it died, it draws a streak back to that spot. Either one would explain the "invisible" bullets.
2. **`OnHit` listeners pile up.** If something runs `OnHit += ...` every time a bullet is fired, a bullet used N times runs N handlers when it hits. That adds work and garbage on every hit. Worse, if `OnBulletHit` runs twice for the same bullet, that bullet goes into `inactive` twice. Two later `Acquire` calls then get the same object, and one of the two shots seems to vanish or teleport.
3. **The pool grows during combat.** `Instantiate` runs whenever the pool is empty, so the first few big fights create new bullets in the middle of gameplay.
4. **Every hit creates and destroys a muzzle flash.** Each one is a new object with its own material copy, destroyed 0.2 s later. That is a steady stream of allocations, which fits a stutter "every few seconds" (a garbage collection pause). In Unity, destroying the object does not destroy a material created through `.material`, so those copies also build up in memory until something unloads them.

## The smallest changes

```text
Bullet Acquire(pos):
  b = inactive.Pop() ?? Instantiate(prefab)
  b.velocity = 0
  b.homingTarget = null
  b.lifetime = b.maxLifetime
  b.trail.Clear()              // after setting position, so no streak from the old spot
  b.position = pos
  b.active = true
  return b

OnBulletHit(b):
  if (!b.active) return        // guard: never push the same bullet twice
  b.active = false
  flashPool.Acquire(b.position)   // instead of spawning a new flash
  inactive.Push(b)
```

- **Listeners:** subscribe to `OnHit` once, when the bullet is created. Alternatively, set `OnHit = null` when the bullet is released and subscribe again on fire. Never add a listener on each `Acquire` without removing it.
- **Pre-warm:** create about 80 bullets at level load (peak is about 60, plus some headroom), and about 10 flashes, since each lasts only 0.2 s.
- **Flash pool:** use the same pop/push pattern as the bullets, with **one shared material**. If each flash needs its own colour or alpha, use a `MaterialPropertyBlock` (or the equivalent in your engine) instead of a material copy.

**What these changes keep the same:** the pool API and every caller, how bullets behave and look, how flashes look (same material and same 0.2 s), and your shadow quality. Nothing new is added beyond a second small pool.

## Why not "pool everything" or lower shadows

- Pooling only matters for objects created at runtime in high numbers. Here that means bullets (already pooled) and flashes. Pooling anything else adds code without removing a cause.
- Shadow resolution is a fixed GPU cost paid every frame. It can lower your average fps, but it cannot cause a spike every few seconds. Change it only if a profile shows the GPU is the bottleneck.
- 45 fps in the Editor says little. The Editor adds its own CPU overhead and garbage. Measure in a development build on the target hardware.

## The measurement that settles the cause

Profile a development build on the target device during 30–60 s of sustained shooting, with the profiler's CPU timeline and memory views open:

1. **Check the spike frames.** If `GC.Collect` (garbage collection) takes most of the spike, the cause is allocation. Look at the **GC Alloc per frame** column while shooting: it should be about 0 B after the fix. If it shows `Instantiate` or a first-use shader or material cost instead, pre-warming is the fix.
2. **Count material instances** with a memory snapshot before and after a minute of combat. If the count rises, the flash materials are leaking.
3. **Count `Instantiate` calls in combat** after pre-warming. It should be 0.
4. **Check whether the steady 45 fps is CPU- or GPU-bound** in the build. Look at shadows only if the GPU is the bottleneck. This is a separate question from the stutter.

Repeat the same capture after the changes. If the spike frames no longer show `GC.Collect` and per-frame allocation is close to zero during combat, the cause is confirmed.

## What I could not check

- **Engine:** I assumed Unity, which matches "C#-style" with `Instantiate`. `trail.Clear()`, `MaterialPropertyBlock` and the material leak are specific to Unity.
- **Where `OnHit +=` runs:** I didn't see that code, so the stacked-listener and double-push explanation is inferred, not seen.
- **How "invisible" is drawn:** I didn't see how lifetime or rendering works, so the stale-lifetime and stale-trail explanations are likely, not proven.
- **No profiler data, platform, shadow settings, or other per-frame allocations** (strings, LINQ, closures in the fire code). Any of these could add to the garbage collection pressure.

---
Skipped: shadow and quality tuning, and pooling anything other than bullets and flashes. Risk: if the spike frames don't show garbage collection, the cause is somewhere these fragments don't cover, and the capture above is how you'll see it.
