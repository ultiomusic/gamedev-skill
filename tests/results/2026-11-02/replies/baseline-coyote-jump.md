## Goal for this fix

If you press jump within 0.3 s of walking off a ledge, you get exactly one jump. A later press gets no jump, either now or when you land. You never get a second jump in the air. The jump height and the floaty arc stay as they are.

## What causes it

The code fragment you sent proves both of these:

- **Double jump, cause 1: grace is never used up.** Taking off doesn't clear `graceLeft`. On the takeoff frame you are still grounded, so grace is reset to 0.3. That means any second press in the next ~0.3 s passes `graceLeft > 0` and jumps again in mid-air. A ledge-grace jump has the same hole.
- **Double jump, cause 2: rejected presses still fire.** The "too late" branch shows the message and then sets `queuedJump = true` anyway. That queue never expires, so the player gets a jump they never asked for on the next landing, right after being told they were too late.

The missed ledge jumps are only partly explained by the code:

- **Proven: a long frame can eat the window.** `graceLeft -= dt` runs before the press is checked. One long frame (about 0.3 s, a hitch) just after leaving the ledge uses up the whole window, and that frame's press is rejected. It then fires late, on landing, because of cause 2.
- **Not proven: physics may overwrite the jump.** The jump is set at render rate, but physics steps at 50 Hz elsewhere. If that fixed step owns `grounded` or resets `velocity` on the ground, it could overwrite the jump. I can't see that code. If ledge misses still happen without hitches after this fix, look there next.

## Smallest change

This deletes `queuedJump` and adds no new code paths:

```text
Update(dt):
  grounded = CheckGround()
  if grounded:
    graceLeft = 0.3

  if JumpPressed():
    if graceLeft > 0:                  // grounded implies graceLeft = 0.3
      velocity.y = jumpSpeed
      graceLeft = 0                    // takeoff uses up the grace window
    else:
      ShowText("too late")             // a rejected press is dropped, not queued

  if not grounded:
    graceLeft -= dt                    // reduce after checking the press, so one hitch frame can't eat it

  ApplyGravity(dt)
  MoveAndCollide(velocity * dt)
```

**What stays the same:** `jumpSpeed`, gravity, the 0.3 s ledge window and the movement integration are untouched, so jump height and floatiness don't change. The change only decides *whether* a jump starts, never how it moves.

**What you lose:** the landing buffer the old comment wanted ("so the next landing feels responsive"). It's gone because it had no time limit and it fired presses the game had rejected. If you want it back, add a separate short buffer (around 0.1 s) that is used up when it fires. Make the "too late" message show only after the buffer expires.

**Add only if needed:** if `CheckGround` still reports grounded on the frame after takeoff, grace gets reset to 0.3 and a fast second press jumps again. Test C below checks for this at 240 Hz. If it fails, change the check to `grounded = CheckGround() and velocity.y <= 0`, and then check moving platforms.

## How to prove it

Use scripted input with the same level and start position each time. Run at 30, 60, 144 and 240 Hz render rate, with physics at 50 Hz. Record when each press happened, whether it was accepted, when the jump fired, the apex height and the airtime.

- **A. Ledge presses in time:** walk off, then press at +0, +0.1 and +0.29 s. Expect exactly one jump each time, with the same apex as a ground jump.
- **B. Ledge presses too late:** press at +0.31 and +0.5 s. Expect no jump, the "too late" message, and **no jump on landing**.
- **C. Ground jump, then press again:** press again 1 frame, 0.05, 0.15 and 0.29 s later. Expect one jump in total.
- **D. Ledge-grace jump, then press again:** press again at +0.05 s. Expect one jump in total.
- **E. Hitch:** at 60 Hz, insert a single 0.35 s frame 0.02 s after walking off, with the press read on that frame. Expect the jump to be accepted.

**Reject the fix if** any run gives a jump count other than the expected one, any landing jump follows a rejected press, or apex height or airtime moves more than about 2% from the current ground jump at any rate. Then ask players whether ledge jumps feel fair. Correct timing doesn't prove the feel is right.

## What was actually checked

- **Specialists used:** one Game Feel specialist ran as a subagent and did a read-only review. I applied the Systems rules myself (one point where the jump is decided, grace used up once, rejected presses never fire later). I did not start a separate Systems subagent.
- **What was done:** this is analysis of the code fragment only. No project exists here, so nothing was edited, built, run or playtested, and none of tests A to E have been run.
- **Not seen:** `CheckGround`, the 50 Hz physics step, and whether that step also applies gravity or movement. So the second cause of the ledge misses is still a guess until you record a trace.
