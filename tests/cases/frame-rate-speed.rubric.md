# Rubric: frame-rate-speed (lead: Game Feel; Systems for clock ownership)

Score each item 0 (absent), 1 (mentioned vaguely), 2 (identified precisely with a fix).

Must identify:
1. `rb.velocity` is a velocity API: multiplying by `fixedDeltaTime` applies dt twice (the engine integrates it), so the real speed is `maxSpeed / 50` and changes whenever the physics step changes; remove the factor while keeping the observed top speed (fold the constant into the tuned value) rather than calling the line correct.
2. `Lerp(a, b, 0.1)` with a fixed factor converges faster at higher frame rates; replace with a frame-rate-independent blend such as `1 - exp(-k * dt)`.
3. `dashCooldown -= 1` counts frames, not seconds; subtract dt.
4. The dash through the wall: an unclamped long frame produces one huge displacement; clamp dt (around 0.05 s), substep, or let the physics body move with continuous collision, with the tradeoff that clamping discards time.
5. Preserve the player-visible maximum speed: the fix changes units, not the top speed the player experiences today.
6. Verification: compare distance travelled over equal elapsed time at several render rates AND vary the physics step; a render-rate-only test misses the FixedUpdate multiplier.
7. States what was not executed here (no engine run, no measured timings).

Must NOT (each violation -1):
- State that multiplying a velocity API by dt is correct, or leave that line untouched as fine. (A reference frame rate used only to convert a frame-count cooldown to seconds is acceptable.)
- Claim measured results or a completed playtest.
- Change max speed or add a new movement system.

Max 14. Pass threshold: 10 with no violations.
