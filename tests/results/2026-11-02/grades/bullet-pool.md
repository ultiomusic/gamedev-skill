# Blind grades: bullet-pool

Rubric: 7 items, 0/1/2 each (max 14), -1 per must-not violation. Pass: >= 10 with no violations.
A 2 needs the item identified precisely and a concrete fix or check.

## Item scores

| # | Item | A | B | C |
|---|------|---|---|---|
| 1 | Incomplete reset on reuse (velocity, target, lifetime, trail, OnHit), explains symptoms | **2**: "b.homingTarget = null ... b.trail.Clear()" plus "subscribe to `OnHit` once" | **2**: table mapping symptom to "Field that is never reset", plus a full reset in `Acquire` | **2**: "never resets `velocity`, `homingTarget`, `lifetime`, the trail or the `OnHit`", plus a full reset |
| 2 | In-combat `Instantiate` growth; preallocate peak + margin; empty-pool policy with warning | **1**: "create about 80 bullets at level load", but the fallback stays a silent `?? Instantiate(prefab)` with no policy and no warning | **2**: "warn(\"bullet pool exhausted\"); b = Instantiate(prefab)", with about 64 prewarmed and the policy stated (grow, never reject) | **2**: "Keep the `Instantiate` fallback ... but count how often it fires", with a prewarm of measured peak plus margin |
| 3 | Muzzle flash spawn/destroy with unique material is churn; stronger stutter candidate | **2**: "The stutter most likely comes from the unpooled hit effect", fixed with a flash pool, one material and a MaterialPropertyBlock | **2**: ranked first, "Hit-flash churn", fixed with a capped pool and a shared material | **2**: "Likely cause of the stutter: each hit allocates a flash", fixed with a pooled set and one material |
| 4 | Stutter is a hypothesis until captured; capture GC vs GPU; Editor fps is not evidence | **2**: "If `GC.Collect` ... takes most of the spike"; "45 fps in the Editor says little" | **2**: "Spikes line up with GC markers" or "shadow pass stays flat"; "45 fps in the Editor doesn't settle" | **2**: "garbage-collection events ... GPU: transparent-pass and shadow-pass time"; "player build ... rather than in the Editor" |
| 5 | Rejects "pool everything" and shadows as unsupported | **2**: "Shadow resolution ... cannot cause a spike every few seconds" | **2**: "Pool only churn the capture demonstrates"; "No evidence points at shadows" | **2**: "Neither \"pool everything\" nor \"lower shadow resolution\" fits" |
| 6 | Gameplay rule: a bullet hits once; listener build-up gives duplicate hit effects | **1**: "a bullet used N times runs N handlers", framed only as garbage and double push; it never states the hit-once rule or names duplicate effects | **2**: "it hits exactly once"; "`OnHit` fires exactly once" assert | **2**: "one hit runs N times: N damage settlements, N flashes", fixed with a gen/active guard |
| 7 | States what was not executed (no profiler, no engine run) | **2**: "No profiler data, platform, shadow settings" in a "could not check" section | **2**: "couldn't run, profile or test anything" | **2**: "nothing was run, profiled or tested" |

Note on item 5: none of the three says that pooling does not reduce overdraw. All three still give the core rejection with reasons and a conditional check, so all score 2.

Note on item 2: B and C both keep the growth inside the hot path (grow with a warning or a counter), not outside it. The policy is explicit and signalled, so both score 2. A has no policy at all.

## Must-not violations

| Reply | Violations |
|-------|------------|
| A | None. "it should be about 0 B after the fix" is a stated target, not a measured result. |
| B | None. "about 60 s of sustained fire" is a capture length, not an invented reading. |
| C | None. |

## Uncovered points (not scored)

- **A, useful:** points out that in Unity, `.material` copies are not freed when the object is destroyed, so they leak. Also flags first-use shader/material cost as an alternative spike source, and checks material count with a memory snapshot.
  **A, error:** the code comment says `trail.Clear()` runs "after setting position", but the code clears the trail before `b.position = pos`, so the old-spot streak can still occur. Also, `b.velocity = 0` leaves velocity to an unseen caller.
- **B, useful:** adds a pool-size-1 reuse test and a same-frame hit-plus-expiry test for the double push. Also notes that unique materials break batching, and that misses may never return to the pool.
  **B, error:** the prewarm of 64 leaves a thin margin over the peak of about 60. Process note: it claims subagents were used, which cannot be verified and is not a technical error.
- **C, useful:** handles homing when the target is null or dead, checks `inactive` for duplicates, tracks the shots/hits/flashes reconciliation and the transparent-pass time, and sets reject-the-fix criteria before the run.
  **C, error:** the `gen` check is ineffective as written. `OnHit` is subscribed once at creation, so the handler must capture `gen` at fire time, or `gen != b.gen` never trips. Same process note about subagents as B.

## Summary

| Reply | Items 1..7 | Violations | Total | PASS/FAIL |
|-------|------------|------------|-------|-----------|
| A | 2, 1, 2, 2, 2, 1, 2 | 0 | 12 | PASS |
| B | 2, 2, 2, 2, 2, 2, 2 | 0 | 14 | PASS |
| C | 2, 2, 2, 2, 2, 2, 2 | 0 | 14 | PASS |
