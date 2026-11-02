# Frame-rate-consistent movement: the smallest fix

## What is actually wrong

| Line | Frame-rate dependent? | Effect |
|---|---|---|
| `rb.velocity = moveInput * maxSpeed * Time.fixedDeltaTime` (FixedUpdate) | **No.** `fixedDeltaTime` is a constant 0.02 s, so walk speed is the same at 40 and 144 fps. The units are odd (velocity times a timestep) but the result is still constant. | **Leave it alone.** If you remove `* Time.fixedDeltaTime`, walking gets 50x faster, and that changes the maximum speed you said to keep. |
| `dashCooldown -= 1` (Update) | **Yes.** It counts frames, not seconds. At 144 fps the cooldown runs out 3.6x faster than at 40 fps. | This is the main reason the PC covers more ground: it can dash 3.6x as often. |
| `transform.position += dashDirection * dashSpeed * Time.deltaTime` (Update) | The speed is right (units per second), but it moves the transform directly and skips the physics engine. | During a hitch, `deltaTime` gets large (Unity caps it at 0.333 s by default), so the player teleports in one step and can go through a wall. That big jump is also the likely cause of the camera snap. |
| `Lerp(camera, target, 0.1)` (Update) | **Yes.** It closes 10% of the gap per frame, so the camera catches up 3.6x faster at 144 fps than at 40 fps. | The camera feels different on each device. |

## The change (4 lines)

```text
FixedUpdate():
  if dashing: rb.velocity = dashDirection * dashSpeed            # dash now goes through physics
  else:       rb.velocity = moveInput * maxSpeed * Time.fixedDeltaTime   # unchanged

Update():
  dt = Min(Time.deltaTime, 1/30)   # shortcut: a hitch longer than 33 ms eases the camera instead of snapping it; remove if you want exact real-time catch-up
  camera.position = Lerp(camera.position, target.position, 1 - Pow(0.9, dt * REF_FPS))
  if dashCooldown > 0: dashCooldown -= Time.deltaTime            # now counts seconds
  # removed: transform.position += dashDirection * dashSpeed * Time.deltaTime
```

Plus one setting: set the player Rigidbody's **Collision Detection to Continuous** (or Continuous Dynamic). At 50 Hz a dash moves `dashSpeed * 0.02` per physics step. If that is more than the wall's thickness, discrete collision can still miss the wall.

## What it preserves

- **Maximum walk speed:** that line is byte-for-byte unchanged.
- **Dash speed:** `dashSpeed * deltaTime` per frame was already `dashSpeed` units per second. Setting `rb.velocity = dashDirection * dashSpeed` gives the same units per second. Do **not** multiply this line by `fixedDeltaTime`.
- **Camera feel at the reference frame rate:** `1 - 0.9^(dt*REF_FPS)` equals exactly 0.1 per frame at `REF_FPS`, and the camera covers the same distance per second at any other frame rate.
- **Dash cooldown length on one machine:** this is the one value you have to convert by hand (see below).

## The decision this needs from you

The cooldown value is currently in frames, so the same number means different lengths of time on your two machines. Whatever sets it (`dashCooldown = N` is not in the fragments) needs `N / REF_FPS` seconds. Choose `REF_FPS` to match the machine where the feel was tuned:
- 144 if that was your PC, which keeps the PC feel and makes the Deck faster;
- 40 if it should feel like the Deck does today.

Use the same `REF_FPS` for the camera. This is a design call, so I have not picked it for you.

## How to prove it

1. **Same distance at 40 vs 144 fps.** Write a PlayMode test that sets `Time.captureFramerate` (or `Application.targetFrameRate`) to 40, then 144. Feed scripted input (walk plus dash spam) for 10 s and assert that the final positions and the number of dashes match within a small tolerance. Before the fix this fails because of the dash count. After the fix it should pass.
2. **No tunneling.** Dash at a thin wall, force a ~1 s stall partway through (for example, block the main thread for a second in one frame) and assert the player ends up on the near side. Run it with and without Continuous collision to show which part does the work.
3. **Max speed unchanged.** Hold full input with no dash and assert the speed equals `maxSpeed * fixedDeltaTime`, the same value as before.
4. **Camera.** Run a pure-math check that one step of `2*dt` equals two steps of `dt` (to within rounding), and a PlayMode check that the camera's distance to the target after 1 s matches at 40 and 144 fps.
5. On the real Steam Deck, play the same route on both machines and compare times.

## What I could not check (no project here, nothing was run)

- Where `dashCooldown` is set and in what units, and how `dashing` ends. If the dash duration also counts frames, it needs the same `-= Time.deltaTime` fix.
- The Unity version. In Unity 6, `rb.velocity` is `rb.linearVelocity`.
- Rigidbody interpolation and collision settings, wall thickness, `Time.maximumDeltaTime`, and whether `moveInput` is read with per-frame smoothing.
- Whether the camera snap comes only from the dash teleport. If the camera still jitters at 144 fps, move the follow to `LateUpdate` and turn on Rigidbody **Interpolate**. That is a likely next step, but I have not included it as required.

Skipped: cleaning up the odd `maxSpeed * fixedDeltaTime` units, because doing so would retune walk speed. Risk: if you ever change the Fixed Timestep, walk speed will change with it.
