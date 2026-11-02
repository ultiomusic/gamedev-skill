# Case: late and double jumps (2D platformer)

User request: "Players say jumps off ledges sometimes don't happen, and sometimes they get a
double jump they shouldn't. Fix it. Keep the jump height and the floaty feel."

No project is on disk; this fragment is the only evidence. Engine-neutral, runs at render rate.
Physics also steps at a fixed 50 Hz elsewhere; `JumpPressed()` is an edge read in this update.

```text
Update(dt):
  grounded = CheckGround()
  if grounded:
    graceLeft = 0.3
  else:
    graceLeft -= dt

  if JumpPressed():
    if grounded or graceLeft > 0:
      queuedJump = true
    else:
      ShowText("too late")
      queuedJump = true        // "so the next landing feels responsive"

  if queuedJump and (grounded or graceLeft > 0):
    velocity.y = jumpSpeed
    queuedJump = false

  ApplyGravity(dt)
  MoveAndCollide(velocity * dt)
```

Return the smallest change, what it preserves, and how you would prove it, including the
limits of what you could check here.
