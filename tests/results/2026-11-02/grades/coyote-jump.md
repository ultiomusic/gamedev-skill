# Blind grade: coyote-jump

Rubric: tests/cases/coyote-jump.rubric.md (7 items, 0/1/2 each, max 14; pass = 10 or more with no violations).
A score of 2 needs a precise identification AND a concrete fix or check.

## Item scores

### 1. Grace window never consumed at jump
- **A: 2**. "Taking off doesn't clear `graceLeft`." The fix adds `graceLeft = 0` at takeoff.
- **B: 2**. "A jump never uses up the coyote window." The fix adds `graceLeft = 0  // one jump per ground contact`.
- **C: 2**. "The ledge grace is never used up by a jump." The fix adds `graceLeft = 0` with the comment "the jump uses up the ledge grace".

### 2. Stale `grounded` on the takeoff frame refills the window
- **A: 2**. "On the takeoff frame you are still grounded, so grace is reset to 0.3." The fix clears grace at takeoff. If test C fails, it adds `velocity.y <= 0`.
- **B: 2**. "CheckGround() can still return true... sets graceLeft back to 0.3". The fix uses `CheckGround() and velocity.y <= 0` and also clears grace.
- **C: 2**. "can still report ground for a frame or two... refills grace". The fix uses `velocity.y <= 0` and also clears grace.

### 3. `queuedJump` never expires; needs a bounded buffer (about 0.1 s) consumed once
- **A: 2**. "That queue never expires". A deletes the queue. If a buffer is wanted back, it gives "a separate short buffer (around 0.1 s) that is used up". Test B checks "no jump on landing".
- **B: 2**. "`queuedJump = true` stays set with no time limit". `bufferLeft = 0.15` is consumed once (`bufferLeft = 0`), and the test row "Press 1.0 s before landing" expects 0 jumps. 0.15 s is at the high end of "about 0.1".
- **C: 2**. "bounded buffer replaces the unbounded queuedJump". `jumpBuffer = 0.1` is set and consumed once.

### 4. A rejected ("too late") press must not be queued
- **A: 2**. "a rejected press is dropped, not queued". A also says to show "too late" only after a buffer expires.
- **B: 0**. B does the opposite: "the duplicated `queuedJump = true` collapses into one line". A press that shows "too late" still sets `bufferLeft = 0.15`. It can jump on landing within 0.15 s, right after "too late" was shown.
- **C: 2**. "A press that doesn't count never turns into a jump later". "too late" is shown only when the buffer expires, so a rejected press can never fire.

### 5. 0.3 s is outside the usual range (about 0.1 to 0.15 s); propose a smaller value to test
- **A: 0**. A keeps "the 0.3 s ledge window" as untouched and never questions its size.
- **B: 1**. "That window is already generous". B notes that it is large but gives no range and proposes no smaller value.
- **C: 1**. "the usual range is 0.1–0.15 s". C names the range but declines to propose a smaller value to test and defers it.

### 6. Keeps jump height and gravity (no `jumpSpeed` retune)
- **A: 2**. "`jumpSpeed`, gravity... are untouched". A rejects the fix if apex or airtime moves more than 2%.
- **B: 2**. "`jumpSpeed`, `ApplyGravity`... are unchanged". A test row expects the apex to be identical between old and new code.
- **C: 2**. "same launch speed: same height". The pass rule requires peak height and air time to match the old code.

### 7. Verification across press timings, double presses, frame rates and the 50 Hz step; names its limits
- **A: 2**. "30, 60, 144 and 240 Hz render rate, with physics at 50 Hz". Tests A to E cover in-time, late, double and hitch presses, and a section lists what was not seen.
- **B: 1**. Press timings, double presses and dt values of 1/30, 1/60 and 1/144 are all covered, and the limits are named. The headless test stubs `CheckGround`, though, and the verification never runs across the 50 Hz physics step.
- **C: 2**. "30, 60, 144 and 240 Hz with physics at 50 Hz". The table covers early, late, double, held and hitch presses, and there is a Limits section.

## Must-NOT violations
- **A: none.** "nothing was edited, built, run or playtested". A mentions a subagent review as process, not as a measured outcome.
- **B: none.** "none of the above was executed".
- **C: none.** "Nothing was run." Its mention of a "Systems specialist" is workflow, not an invented project file.

## Totals
- A: 2+2+2+2+0+2+2 = 12 - 0 = **12**
- B: 2+2+2+0+1+2+1 = 10 - 0 = **10**
- C: 2+2+2+2+1+2+2 = 13 - 0 = **13**

## Notes outside the rubric (not scored)

**Useful points the rubric does not cover**
- **A:** Moving `graceLeft -= dt` after the press check stops one hitch frame from eating the whole window. A also sets a concrete reject rule: wrong jump count, a landing jump after a rejected press, or apex/airtime drift above 2%.
- **B:** It gives caveats for y-down axes and for slopes or rising platforms with `velocity.y <= 0`. It also proposes applying the jump inside the fixed step if the 50 Hz physics overwrites it.
- **C:** It flags unclamped `dt`. It adds an old-vs-new column to the test table and a trace criterion ("set but the body didn't rise") to separate a physics override from the other causes. It offers a "rising from a jump" flag as the moving-platform alternative.

**Technical errors the rubric does not catch**
- **A:** It deletes the landing buffer the original comment asked for, which is a responsiveness regression. The decrement-after-check makes the effective grace 0.3 s + dt, which depends on frame rate. Test E accepts a press 0.37 s after leaving the ledge. A also calls the hitch cause "Proven" when only the code path is shown, not that hitches happen.
- **B:** "too late" now also shows for valid pre-landing presses that will still jump within 0.15 s. Its claim that "too late" still shows at the same moment leaves the message misleading.
- **C:** "too late" now also fires for harmless early mid-air presses, which C partly acknowledges ("you may want to change the wording"). It refers to a "Systems specialist's fixed-timestep handover" that does not exist in the case.

## Summary

| Reply | Items 1..7 | Violations | Total | PASS/FAIL |
|---|---|---|---|---|
| A | 2, 2, 2, 2, 0, 2, 2 | 0 | 12 | PASS |
| B | 2, 2, 2, 0, 1, 2, 1 | 0 | 10 | PASS |
| C | 2, 2, 2, 2, 1, 2, 2 | 0 | 13 | PASS |
