# Case: speed differs by frame rate

User request: "Movement is slower on the Steam Deck at 40 fps than on my PC at 144 fps, and the
camera snaps after a hitch. Make it consistent. Don't change the maximum speed."

No project is on disk; these fragments are the only evidence. Unity-style names; physics steps at 50 Hz.

```text
FixedUpdate():
  rb.velocity = moveInput * maxSpeed * Time.fixedDeltaTime

Update():
  camera.position = Lerp(camera.position, target.position, 0.1)
  if dashCooldown > 0: dashCooldown -= 1
  if dashing: transform.position += dashDirection * dashSpeed * Time.deltaTime
```

A one-second hitch during a dash moved the player through a wall once. Return the smallest change,
what it preserves, and how you would prove it, including what you could not check here.
