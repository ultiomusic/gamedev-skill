**What the fix has to deliver:** one press gives at most one jump. A press counts if it lands while the player is on the ground, within the existing 0.3 s ledge grace, or up to 0.1 s before landing. A press that doesn't count never turns into a jump later. Jump height, gravity and air time stay exactly as they are.

I took the direct path: this is coyote time plus input buffering, both inside the Game Feel brief, so I didn't start any specialist subagents. Everything below comes from reading your fragment. Nothing was run.

## What's wrong in the fragment

1. **The ledge grace is never used up by a jump (this causes the double jump).** After a normal jump, `graceLeft` keeps counting down from 0.3. Any press in the first ~0.3 s of the rise passes `graceLeft > 0` and fires a second jump.
2. **The ground check can still say "grounded" just after takeoff.** `CheckGround()` runs before the body has moved far. If physics only updates contacts at 50 Hz, it can also lag. Either way it can still report ground for a frame or two after the jump starts. That refills grace to 0.3 and even passes the `grounded` branch. How often this happens depends on render rate, which fits "sometimes".
3. **A press marked "too late" still fires later.** That branch sets `queuedJump = true` with no expiry. The game says "too late", then jumps on its own at the next landing, however much later that is. If the player also presses on landing, the leftover grace from bug 1 lets that press fire a second jump.
4. **Missed ledge jumps can't be explained from this fragment alone.** Grace is already a generous 0.3 s, so at a steady frame rate the code accepts these presses. There are two candidates I can't confirm without your project:
   - A hitch frame (`dt` is not clamped) drains the whole grace before the press is read.
   - The separate 50 Hz physics step overwrites `velocity.y`, or resolves ground contact, after this render-rate update has set it. Then the jump is accepted but eaten.

## The smallest change

```text
Update(dt):
  grounded = CheckGround() and velocity.y <= 0     // no stale ground while rising after takeoff
  if grounded:
    graceLeft = 0.3                                 // unchanged
  else:
    graceLeft -= dt

  if JumpPressed():
    jumpBuffer = 0.1                                // bounded buffer replaces the unbounded queuedJump
  else if jumpBuffer > 0:
    jumpBuffer -= dt
    if jumpBuffer <= 0:
      ShowText("too late")                          // only shown once the press has really expired

  if jumpBuffer > 0 and (grounded or graceLeft > 0):
    velocity.y = jumpSpeed                          // same launch speed: same height
    jumpBuffer = 0                                  // one press, one jump
    graceLeft = 0                                   // the jump uses up the ledge grace

  ApplyGravity(dt)
  MoveAndCollide(velocity * dt)
```

`queuedJump` is removed. Your idea of making the next landing feel responsive stays, but now as a 0.1 s window that is used once. A press up to 0.1 s before landing still jumps on the landing frame.

**What stays the same:** `jumpSpeed`, `ApplyGravity`, movement and the 0.3 s grace length are untouched, so jump height, the floaty arc and how forgiving ledges are all stay as they were.

**What changes:**
- "too late" now shows 0.1 s after a press that didn't count, not at the moment of the press. It also covers presses made too early before landing, so you may want to change the wording.
- `velocity.y <= 0` assumes y points up and that nothing else writes upward speed while standing. If moving platforms add their own upward speed into `velocity.y`, replace this check with a "rising from a jump" flag that clears on landing.

## How to prove it

Run a scripted input replay with fixed press times. Use render rates of 30, 60, 144 and 240 Hz with physics at 50 Hz, plus one 0.25 s hitch. Compare old and new code on the same level and the same input:

| Sequence | Expected after the fix | Old code |
|---|---|---|
| Walk off a ledge, press 0.05 / 0.25 / 0.29 s after leaving | Exactly one jump each | One jump |
| Walk off a ledge, press 0.31 s after leaving | No jump; "too late" 0.1 s later; **no jump on landing** | Automatic jump on landing |
| Jump from the ground, press again 0.02 / 0.1 / 0.2 s after takeoff | No second jump | Second jump |
| Press 0.08 s before landing | One jump on the landing frame | One jump |
| Press 0.3 s before landing | No jump, text shown | Jumps on landing |
| Hold jump through several landings | One jump in total | One jump |
| Walk off a ledge with a 0.25 s hitch, press right after it | Record what happens: decides missed-jump candidate A | — |

**Pass rule:** jumps fired equals presses accepted in every row, at every rate. Peak height and air time match the old code within one frame of movement.

**When to reject this fix as the cure for missed jumps:** if a trace of the press frame shows `velocity.y = jumpSpeed` was set but the body didn't rise, the 50 Hz physics owner is overriding it. That fix belongs in the physics code, not in this update, and would need the Systems specialist's fixed-timestep handover.

## Limits

- I had no project or engine. I couldn't see `CheckGround`, `ApplyGravity`, `MoveAndCollide` or the 50 Hz step, and I ran no replay.
- The double-jump causes are clear in the code. The cause of missed ledge jumps is a hypothesis until the trace or the hitch row above runs.
- Nobody has played this, so whether it still feels floaty to players is unconfirmed.

Not done: I didn't clamp `dt`, shorten the 0.3 s grace (the usual range is 0.1–0.15 s, but a shorter grace would make more ledge jumps miss) or move jump input onto the fixed physics step. Each waits on the trace above.
