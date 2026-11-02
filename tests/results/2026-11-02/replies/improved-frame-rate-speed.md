## Fixing movement that changes with frame rate

**Goal:** for the same amount of play time, walking, dashing and the camera should behave the same at 40 fps on the Steam Deck, at 144 fps on your PC, and during a hitch. A dash should never go through a wall. Top speed stays as it is now.

This covers both movement timing and dash collision, so I used two specialists who only read the code and made no edits:
- **Game Feel (lead):** movement, dash cooldown timing and the camera.
- **Systems:** dash collision and the physics clock.

Neither one wrote code. I combined their results below. All of this comes from reading the four lines you sent. There's no project here, so I didn't run or test anything.

### Which lines change with frame rate

| Line | Changes between 40 and 144 fps? | Why |
|---|---|---|
| `rb.velocity = moveInput * maxSpeed * Time.fixedDeltaTime` | **No** | It runs in `FixedUpdate` at a fixed 50 Hz, so the walking speed is `maxSpeed * 0.02` on both machines. Multiplying a velocity by dt is a units bug, but what it really ties walking speed to is the physics step rate, not the frame rate. |
| `dashCooldown -= 1` | **Yes, most likely the main cause** | It counts frames, not seconds. On the Deck the cooldown lasts 3.6 times longer, so you get fewer dashes and cover less ground in the same time. |
| `Lerp(camera, target, 0.1)` | **Yes** | Each frame the camera closes 10% of the gap. That gives about 0.24 s of lag at 40 fps and 0.066 s at 144 fps, so the camera trails more on the Deck and movement looks slower. After a hitch it catches up in a sudden whip. |
| `transform.position += dashDirection * dashSpeed * Time.deltaTime` | No in normal play. **Tunnels during a hitch.** | Setting the position directly skips the Rigidbody and its collision checks. After a hitch the large `deltaTime` (limited by `Time.maximumDeltaTime`, default 0.333 s) moves the player past the wall in one step. It also works against the velocity that `FixedUpdate` sets. |

### The smallest change

```csharp
void FixedUpdate() {
    if (dashCooldown > 0f) dashCooldown -= Time.fixedDeltaTime;   // seconds, on the same clock as the dash
    rb.velocity = dashing
        ? dashDirection * dashSpeed                                // the Rigidbody moves the dash, so walls stop it
        : moveInput * maxSpeed * Time.fixedDeltaTime;              // unchanged on purpose, see below
}

void Update() {
    // remove the old cooldown and dash lines from here
}

void LateUpdate() {                                                // follow the player after physics and interpolation
    const float followRate = 15.17f;                               // -ln(0.9) * 144: matches Lerp 0.1 at 144 fps
    float dt = Mathf.Min(Time.deltaTime, 0.05f);                   // camera only: a hitch becomes a short catch-up, not a jump
    camera.position = Vector3.Lerp(camera.position, target.position, 1f - Mathf.Exp(-followRate * dt));
}
```

Other changes that go with the code above:
- **Make `dashCooldown` a `float` holding seconds.** Wherever it's set, use `oldFrames / 144f`. For example, a 30-frame cooldown becomes 0.208 s. Check the serialized value after changing it from int to float.
- **If the dash ends after a number of frames, convert that too** to a timer in `FixedUpdate` that subtracts `Time.fixedDeltaTime`. I couldn't see how the dash ends.
- **Set Rigidbody Interpolation to Interpolate.** Otherwise the camera at 144 fps follows a position that only updates 50 times a second.
- **Set Collision Detection to Continuous** if `dashSpeed * 0.02` is more than about half the thickness of the thinnest wall or of the player's collider. Use ContinuousDynamic if walls move. Also confirm the Rigidbody is not kinematic.
- **Unity 6 renamed `velocity` to `linearVelocity`.** Use whichever your installed version has.

### What this keeps the same

- **Walking top speed.** I left the walking line alone because it isn't what makes the Deck slower, and you asked not to change maximum speed. It still has the units bug: changing the physics step later would change walking speed. To fix that properly, remove `* Time.fixedDeltaTime` and also multiply every serialized `maxSpeed` value by 0.02, including prefab and scene overrides. Top speed would stay the same, but the number shown in the Inspector would change, so that's your call.
- **Dash speed and distance.** `dashSpeed` is already in units per second.
- **The dash rhythm and camera feel you have on your PC.** The `/144` and `15.17` conversions assume your PC is the reference. If the values were tuned at 60 fps, use `/60f` and `6.32f`.

### How I would prove it (none of this was run)

1. **Same results at both frame rates.** Write a PlayMode test that holds the same input and dashes on a fixed schedule for 3 s, once with `Time.captureFramerate = 40` and once with 144. Pass if:
   - final positions match within 1%,
   - the number of dashes is equal,
   - the camera's distance from the player at 1, 2 and 3 s matches.
   If walking distance alone already differs, there's another cause these lines don't show, such as how `moveInput` is read, and this fix is wrong.
2. **Hitch during a dash.** Dash toward the thinnest wall and force a 1 s stall on the frame the dash starts (for example with `Thread.Sleep`). Pass if the player never ends up past the wall. Also check that the camera catches up within about 0.2 s and doesn't jump.
3. **Physics step change.** Run the walk test with `fixedDeltaTime` at 0.02 and at 0.01. Dash distance should match. Walking speed will differ until the units fix above is made, which confirms that limitation.
4. **Steam Deck build.** A real Deck build at 40 fps is the only thing that confirms the change works on the device and feels right. The checks above only measure timing; they can't tell you whether it feels good.

### What I couldn't check

- How `moveInput` is read and whether it is clamped to length 1.
- How long a dash lasts and the cooldown's starting value.
- Your actual Rigidbody settings and `Time.maximumDeltaTime`.
- Whether physics is really 50 Hz on the Deck build.

**Trade-off:** capping the camera's dt at 0.05 s means that for a moment after a hitch the camera trails more than it would if the frame rate had stayed steady. If playtesters prefer the camera to stay locked to the player, remove the cap. The cap has no effect at 40 or 144 fps; it only kicks in below 20 fps.
