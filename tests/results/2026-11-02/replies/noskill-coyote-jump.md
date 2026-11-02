# Late and double jumps: fix

## What is wrong in this fragment

1. **Mid-air second jump (the "double jump").** A jump never uses up the coyote window. You jump from the ground, `graceLeft` is still about 0.3, and a second press in the next 0.3 s passes `graceLeft > 0` and jumps again in mid-air.
2. **Re-jump just after takeoff.** For the next frame or two after a jump, `CheckGround()` can still return true. The ground probe still touches the floor, and at 50 Hz physics against a faster render rate the contact data is up to 20 ms old. Each of those frames sets `graceLeft` back to 0.3, so a quick second press resets `velocity.y` again. That gives an extra jump, too.
3. **The "too late" press never expires.** `queuedJump = true` stays set with no time limit. A press made long before landing (even seconds before) fires on the next landing, so the player gets a jump they didn't ask for. The comment shows the intent was a jump buffer. It just needs a time limit.

**Missed ledge jumps:** in this code, a press is dropped only after `graceLeft` reaches zero, which takes 0.3 s. That window is already generous. Two things can still eat it:
- A long frame (a hitch) where `dt` alone is bigger than the window.
- More likely, something outside this fragment. The 50 Hz physics step may overwrite `velocity.y` (ground snap, or a landing clamp while the player still touches the ledge), or `CheckGround` may read stale data. I can't see that code. See "Limits" below.

## Smallest change

```text
Update(dt):
  grounded = CheckGround() and velocity.y <= 0   // rising = just jumped, not standing (y-up)
  if grounded:
    graceLeft = 0.3
  else:
    graceLeft -= dt

  if JumpPressed():
    bufferLeft = 0.15                // was: queuedJump = true, with no expiry
    if not (grounded or graceLeft > 0):
      ShowText("too late")
  else:
    bufferLeft -= dt

  if bufferLeft > 0 and (grounded or graceLeft > 0):
    velocity.y = jumpSpeed
    bufferLeft = 0
    graceLeft = 0                    // one jump per ground contact

  ApplyGravity(dt)
  MoveAndCollide(velocity * dt)
```

The changes, line by line:
- `and velocity.y <= 0` on grounded fixes bug 2.
- `graceLeft = 0` on jump fixes bug 1.
- The `queuedJump` flag becomes a `bufferLeft` timer, which fixes bug 3.

Both press branches set the same thing, so the duplicated `queuedJump = true` collapses into one line. The code also needs `bufferLeft = 0` at init, in place of `queuedJump`.

## What it keeps

- **Jump height:** `jumpSpeed`, `ApplyGravity` and the order of integration are unchanged, so jump height and the floaty arc stay exactly as they are.
- **Timing:** the 0.3 s coyote window is unchanged.
- **Landing jumps and the "too late" text:** a press shortly before landing still jumps on landing, so landings still feel responsive. "too late" still shows at the same moment.
- **Removed:** one jump per ground contact is now enforced. Pre-landing presses older than 0.15 s no longer fire.

## How to prove it

Write a headless test that drives `Update` with a scripted `CheckGround`, `JumpPressed` and `dt`, and counts how often `velocity.y` is set to `jumpSpeed`. Run every case at dt = 1/30, 1/60 and 1/144, plus one 0.25 s hitch frame:

| Case | Expected |
|---|---|
| Walk off a ledge, press at +0.29 s | 1 jump |
| Walk off a ledge, press at +0.31 s | 0 jumps, "too late" shown |
| Jump from the ground, press again 1 frame later and 0.1 s later (ground stub still true for 2 frames) | 1 jump total |
| Press 1.0 s before landing | 0 jumps on landing |
| Press 0.1 s before landing | 1 jump on landing |
| Apex height, old code against new, single press, same dt | identical |

Then do a short in-engine playtest at a capped 30 fps and an uncapped frame rate:
- Ledge running jumps
- Mashing jump
- Pressing jump while falling onto a platform

## Limits (nothing was run here)

- **No engine or project:** none of the above was executed. It is reasoning from the fragment only.
- **Up/down direction:** the code assumes y points up. If y points down, the check becomes `velocity.y >= 0`.
- **Slopes and moving platforms:** walking up a slope or riding a rising platform can make `velocity.y > 0` while standing. That would turn off grounded, and a climb longer than 0.3 s would then block jumps. Test both.
- **Missed ledge jumps may not be fixed:** if the cause is the 50 Hz step overwriting `velocity.y` or stale `CheckGround` data, this change does not fix it. The fix would then be to keep the request here and apply the jump inside the fixed step. I need to see that code to confirm.
- **New tuning value:** 0.15 s for the buffer is my choice, not a number from your game. Tune it to taste.
