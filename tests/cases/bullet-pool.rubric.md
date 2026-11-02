# Rubric: bullet-pool (lead: Systems; Performance for the stutter)

Score each item 0 (absent), 1 (mentioned vaguely), 2 (identified precisely with a fix).

Must identify:
1. Incomplete reset on reuse: velocity, homing target, lifetime timer, trail (clear it), and the accumulating `OnHit` listeners must be reset; this explains old-target and invisible bullets.
2. Pool growth with `Instantiate` inside combat defeats the purpose; preallocate the peak (about 60 plus a margin) and define the empty-pool policy (reject, recycle oldest, or grow outside the hot path) with a warning.
3. The muzzle flash spawn/destroy with a unique material per quad is unpooled churn and allocation; it is a stronger stutter candidate than the bullets.
4. The stutter cause is a hypothesis until captured: ask for a profiler capture distinguishing GC / allocation spikes from GPU cost; an Editor frame rate is not evidence of player-build performance.
5. Rejects "pool everything" and shadow-resolution changes as unsupported by evidence; pooling does not reduce overdraw and shadows are unrelated to the described symptoms.
6. Preserves the gameplay rule: a bullet hits once; listener accumulation would also cause duplicate hit effects.
7. States what was not executed (no profiler, no engine run).

Must NOT (each violation -1):
- Report a measured frame-time improvement.
- Propose an engine-wide pooling framework or scheduler.
- Invent profiler numbers or hardware.

Max 14. Pass threshold: 10 with no violations.
