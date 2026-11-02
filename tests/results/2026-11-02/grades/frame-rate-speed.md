# Grades: frame-rate-speed (blind)

Rubric: 7 items scored 0-2 (max 14), -1 per must-not violation. Pass = total >= 10 with no violations.

## Item scores

### 1. `rb.velocity * fixedDeltaTime` applies dt twice; remove the factor while keeping the observed top speed
- **A: 2.** "Multiplying a velocity by dt is a units bug". Gives the exact fix: "remove `* Time.fixedDeltaTime` and also multiply every serialized `maxSpeed` value by 0.02". It leaves the shipped line unchanged, calls it a bug, and leaves the Inspector-value change to the user. This is a borderline 2.
- **B: 2.** "the engine already integrates velocity. Your real top speed is `maxSpeed × 0.02`". It replaces the factor with the constant `0.02f`, so the speed no longer depends on the physics step.
- **C: 1.** "The units are odd ... but the result is still constant." It argues against removing the factor and only mentions the timestep risk at the end.

### 2. Fixed-factor Lerp converges faster at higher fps; switch to a frame-rate-independent blend
- **A: 2.** "`1f - Mathf.Exp(-followRate * dt)`" with followRate derived from -ln(0.9)*144.
- **B: 2.** "`1f - Mathf.Pow(0.9f, Time.deltaTime * 144f)`", which is equivalent.
- **C: 2.** "`1 - Pow(0.9, dt * REF_FPS)`", with a note that it equals 0.1 per frame at REF_FPS.

### 3. `dashCooldown -= 1` counts frames; subtract dt
- **A: 2.** "`dashCooldown -= Time.fixedDeltaTime`", and existing values are converted with "`oldFrames / 144f`".
- **B: 2.** "`dashCooldown -= Time.deltaTime; // now counts seconds`", plus "divide by 144".
- **C: 2.** "`dashCooldown -= Time.deltaTime`", plus "needs `N / REF_FPS` seconds".

### 4. Dash through the wall: a long frame causes one huge step; clamp, substep, or use the physics body with CCD (tradeoff)
- **A: 2.** "the Rigidbody moves the dash, so walls stop it", plus Continuous collision with a size threshold. It notes the `maximumDeltaTime` 0.333 s cap and states the camera clamp tradeoff.
- **B: 2.** "rb.velocity = dashing ? dashDirection * dashSpeed", plus Continuous collision. It explains that holding the camera back "would disagree with the game's elapsed time".
- **C: 2.** "dash now goes through physics", plus "Collision Detection to Continuous". Its test runs "with and without Continuous collision".

### 5. Preserve the player-visible max speed (units change, top speed does not)
- **A: 2.** "Top speed would stay the same, but the number shown in the Inspector would change".
- **B: 2.** "The `maxSpeed` field and the walking speed players actually see, exactly as they are".
- **C: 1.** "that line is byte-for-byte unchanged". Top speed is kept only by not fixing the line, and C claims that removing the factor "changes the maximum speed".

### 6. Verification across several render rates AND a varied physics step
- **A: 2.** "`Time.captureFramerate = 40` and once with 144", plus "`fixedDeltaTime` at 0.02 and at 0.01".
- **B: 2.** "Repeat with the physics step at 0.01 and 1/30", with all checks run at 40 and 144 fps.
- **C: 1.** Its tests use only 40 vs 144 fps. The max-speed check asserts `maxSpeed * fixedDeltaTime` and never varies the physics step.

### 7. States what was not executed
- **A: 2.** "How I would prove it (none of this was run)", plus a "What I couldn't check" list.
- **B: 2.** "No engine, build, test or playtest was run".
- **C: 2.** "What I could not check (no project here, nothing was run)".

## Must-not violations
- **A: none.** Borderline: the shipped code keeps the line "unchanged on purpose", but A calls it a units bug and gives the fix, so the line is not left "as fine".
- **B: none.**
- **C: 1.** It leaves the velocity-times-dt line untouched as fine: "**Leave it alone.** If you remove `* Time.fixedDeltaTime`, walking gets 50x faster".

## Extra notes (not scored)
- **A.** Useful points the rubric misses: Rigidbody Interpolate with the camera in LateUpdate, the Unity 6 `linearVelocity` rename, a CCD threshold based on wall and collider size, and a conversion constant for a 60 fps reference. No technical errors found. The numbers check out: 15.17 = -ln(0.9)*144, and the camera lag is about 0.237 s at 40 fps. Weakness: the delivered code still ties walking speed to the physics step.
- **B.** Useful points the rubric misses: thumbstick deflection and dead zones as a non-timing cause, a kinematic Rigidbody making velocity a no-op, the existing line overwriting vertical velocity, Cinemachine, and a falsification condition. Minor inconsistency: it claims "one clock" for movement, yet the cooldown ticks on Update while the dash runs on physics. The hard-coded `0.02f` leaves `maxSpeed` in odd units.
- **C.** Useful points the rubric misses: it surfaces the REF_FPS reference-machine choice as a design decision, a math check that one 2*dt step equals two dt steps, and a test with and without CCD. Technical errors: it says removing the factor necessarily changes max speed, ignoring the retune. The camera dt clamp at 1/30 already engages in sub-30 fps dips, which a 40 fps Deck can hit. It defers LateUpdate and Interpolate.

## Summary

| Reply | Items 1..7 | Violations | Total | PASS/FAIL |
|---|---|---|---|---|
| A | 2, 2, 2, 2, 2, 2, 2 | 0 | 14 | PASS |
| B | 2, 2, 2, 2, 2, 2, 2 | 0 | 14 | PASS |
| C | 1, 2, 2, 2, 1, 1, 2 | 1 | 10 | FAIL (violation) |
