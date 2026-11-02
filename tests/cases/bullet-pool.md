# Case: shooting stutter with a pool already in place

User request: "Shooting causes a stutter every few seconds. I already added a bullet pool but it still
stutters, and sometimes recycled bullets fly toward an old target or are invisible. The Editor shows
about 45 fps. Should I pool everything and lower shadow resolution?"

No project is on disk; these fragments are the only evidence. C#-style, garbage-collected runtime.

```text
Bullet Acquire(pos):
  b = inactive.Pop() ?? Instantiate(prefab)     // grows during combat when empty
  b.active = true
  b.position = pos
  return b
  // not touched on reuse: velocity, homingTarget, lifetime, trail renderer, OnHit += listeners

OnBulletHit(b):
  spawn 1 new MuzzleFlash quad (translucent, unique material instance), destroyed after 0.2 s
  b.active = false; inactive.Push(b)
```

Peak simultaneous bullets is about 60. Return the smallest changes, what they preserve, and what
measurement would decide the stutter's cause. State what you could not check here.
