**Short answer: don't do either yet.** Pooling everything and lowering shadow resolution aren't supported by what you've shown me. Your pool has a correctness bug, and that bug explains the wrong-target and invisible bullets. The stutter most likely comes from per-hit allocation feeding the garbage collector, but only a capture on a player build can confirm that. Below are the smallest fixes and the measurement that decides it.

**The goal:** every shot leaves the muzzle with *this* shot's velocity and target, it is visible, it hits exactly once, and sustained fire on the target build has no periodic hitch. All of that without losing hit feedback or shadows.

I split the work between two specialist subagents, both read-only:
- **Systems** led on pool state.
- **Performance** looked at the stutter.

I then merged their findings. Nothing was run: there's no project here, only your code fragments.

## 1. Fix the pool reset (Systems, do this first)

`Acquire` sets only `active` and `position`, so every other field keeps the previous shot's value:

| Symptom | Field that is never reset |
| --- | --- |
| Flies toward an old target | `homingTarget` and `velocity` |
| Invisible | A used-up `lifetime` that expires on the first frame, or leftover trail/renderer state from the last hit. The trail can also draw a streak from the old hit point to the muzzle. |
| Hit effects run several times | `OnHit +=` is never removed, so after N reuses the handler runs N times |

There is also a possible second cause of invisible bullets, which I couldn't check. If the miss or expiry path also pushes bullets, a bullet that hits and expires in the same frame is pushed twice. `Pop` then gives the same instance to two shots, and one of them seems to vanish.

The smallest change:

```
Acquire(pos, vel, target):
  b = inactive.Pop()
  if b == null: warn("bullet pool exhausted"); b = Instantiate(prefab)
  b.position = pos; b.velocity = vel; b.homingTarget = target
  b.lifetime = prefab.lifetime
  b.trail.Clear(); b.trail.emitting = true; b.renderer.enabled = true   // clear after setting position
  b.active = true                                                        // last
  return b

Release(b):                       // the ONLY return path, for hit and expiry/miss
  if !b.active: return            // prevents double push
  b.active = false; b.homingTarget = null; b.trail.emitting = false
  inactive.Push(b)

// Subscribe OnHit once when the bullet is created, never per shot (or set it to null in Release).
OnBulletHit(b): if !b.active: return; ...damage, flash...; Release(b)
```

Also fill the pool with about 64 bullets at load (your peak is about 60). Keep the warned fallback grow, so no shot is ever rejected and no live bullet is recycled.

This keeps your pool structure, your damage rules and how bullets behave. Only stale state is removed.

**Check:** set the pool size to 1. Fire at A and hit, then fire at B. Assert these for the reused bullet:
- It is the same instance.
- On its first frame it is at the muzzle, with B's velocity and target, full lifetime, an empty trail and the renderer on.
- `OnHit` fires exactly once.

Then make a bullet hit and expire in the same frame, and assert it is pushed only once. If any assert fails, the fix is wrong.

## 2. The stutter (Performance): fix only what a capture shows

These are hypotheses taken from your code, ranked. None of them is measured:
1. **Hit-flash churn.** Every hit creates a MuzzleFlash quad with its own material instance and destroys it 0.2 s later. Allocating steadily like that during fire produces garbage collections at regular intervals, which fits "every few seconds". Unique materials also stop the flashes batching together.
2. **Listener build-up.** Each `OnHit +=` on reuse can allocate, and the cost grows over the session. If those stale handlers spawn feedback, they also multiply hypothesis 1.
3. **The pool keeps growing.** Bullets only return on hit, so misses may never come back. If so, `Instantiate` keeps running in combat instead of only during warmup.

If the capture confirms them, the smallest changes are below. Make **one change per before/after comparison**.
- **Flashes:** reuse them from a small capped pool with one shared material, using a per-instance property for anything that varies. Reset the 0.2 s timer when a flash is reused. Every hit still shows the same flash for the same time.
- **Listeners and bullet pool:** both are already covered by the reset fix in section 1.

**"Pool everything?"** No. Pool only churn the capture demonstrates, which here is probably bullets and flashes, and keep each pool bounded.

**"Lower shadow resolution?"** No evidence points at shadows. A periodic hitch is a few rare slow frames, not a low average, and you'd be giving up visuals the player uses. Reconsider only if the GPU shadow pass is what spikes on the hitch frames.

**The measurement that decides it**

Capture the same scripted firing sequence (same seed and camera) on a development or profiling **player build on the target device**. Cover warmup, about 60 s of sustained fire, and a stretch after cleanup. Record:
- Frame time p50, p99 and max, plus when each spike happens.
- GC bytes allocated per frame, and GC collection markers.
- Instantiate and Destroy markers, pool growth count, and live flash count.
- `OnHit` listener count and material instance count.
- GPU markers, including the shadow pass.

How to read it:
- **Hypothesis 1 confirmed:** spikes line up with GC markers, and the allocations trace back to spawning flashes.
- **Hypothesis 2 confirmed:** allocation per shot and listener count rise over time, and spikes get more frequent.
- **Hypothesis 3 confirmed:** spikes line up with Instantiate, or the pool keeps growing past about 60.
- **Shadows ruled out:** spike frames are dominated by CPU or GC work and the shadow pass stays flat.
- **GC ruled out:** spikes appear with no GC marker.

Your 45 fps in the Editor doesn't settle any of this. The Editor adds its own overhead and allocations, an average hides the few long frames a hitch is made of, and you haven't said what frame rate you're aiming for.

## What I couldn't check

- I didn't know the engine and couldn't run, profile or test anything. Everything above is reasoning from your fragments.
- I couldn't see the miss and expiry path, how bullets are made visible, the trail and event APIs, whether material instances are freed when objects are destroyed, or whether incremental GC is on.
- So the cause of the invisible bullets is a strong hypothesis, not proven, and the stutter ranking stays unverified until that capture exists.
- If the expiry path doesn't go through `Release`, the double push will remain.
