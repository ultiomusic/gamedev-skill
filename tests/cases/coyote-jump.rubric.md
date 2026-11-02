# Rubric: coyote-jump (lead: Game Feel)

Score each item 0 (absent), 1 (mentioned vaguely), 2 (identified precisely with a fix).

Must identify:
1. The grace window is never consumed when the jump fires, so one window can grant a second jump.
2. `grounded` still reads true on the takeoff frame (velocity is set after the refill), so the window refills from stale grounded state; the fix clears grace at takeoff or reorders the check.
3. `queuedJump` never expires: a press is remembered forever and fires on the next landing. A buffer needs a bounded lifetime (about 0.1 s) and one consumption.
4. A rejected press ("too late") must not be queued; rejection and buffering are different contracts.
5. 0.3 s is well outside the usual starting range (about 0.1 to 0.15 s); proposes a smaller value as a starting point to test, not as a fact.
6. Keeps jump height and gravity unchanged (does not retune `jumpSpeed`).
7. Verification: repeat early / near-edge / late presses and rapid double presses at low, target and high frame rates (and across the 50 Hz physics step); names what could not be checked here.

Must NOT (each violation -1):
- Claim the fix was tested in an engine or report measured outcomes.
- Add an input framework, new mechanic, or change jump height / gravity.
- Invent project files, engine versions, or player data.

Max 14. Pass threshold: 10 with no violations.
