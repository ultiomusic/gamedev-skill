---
name: gamedev
description: Build, debug, or polish gameplay, controls, camera, feedback, rendering, and runtime performance in game projects; use for game-feel reviews and AI-generated gameplay fixes.
---

# Game development with evidence

Make the player's intended action responsive, readable, and consistent at the target frame rate. Preserve the game's genre and design; more effects or more architecture are not inherently improvements. Reply in the user's language.

## Establish the smallest useful target

1. Read project instructions and inspect the current diff before editing. Identify the actual engine/version, render pipeline, entry scene, input system, platform, and existing verification tools from executable configuration and assets. Treat stale templates as claims to verify.
2. Describe one player-visible problem and its reproduction: action, expected response, observed response, and conditions. For a new feature, establish that contract before implementation. An audit stays read-only unless changes are requested.
3. Choose the highest-impact cause: lost or duplicated input, broken rules/timing, unreadable feedback, then measured cost. Trace input → state transition → simulation → presentation before adding polish.
4. Set a small acceptance check appropriate to the game: one tap produces one purchase, an action survives a brief lockout, camera never hides the target, or worst-case frame time stays within budget. Record baseline evidence and assumptions.

## Choose techniques by symptom

Read the relevant rows of [the 34-concept guide](references/concepts.md); use its trigger, implementation trap, and check together. It is a coverage list, not a requirement to add every technique to every game. For a full-coverage audit, mark each concept verified, evidenced only in code, not applicable with a reason, or unverified with a concrete next check.

- Dropped actions or inconsistent motion: timing, input buffering, state transitions; coyote time only where ledge forgiveness makes sense.
- Sliding, snapping, or disorienting follow: acceleration/friction, easing, camera deadzone, rotation interpolation.
- Weak or confusing consequences: event-driven particles, animation deformation, restrained shake or local hit stop when appropriate.
- Incorrect hits or navigation: queries and normals, hit ownership, collision continuity, pathfinding versus local steering.
- Stutters or visual waste: measure CPU/GPU/allocations first, then choose rendering, lifetime, scheduling, or streaming techniques.

For Unity, also read [Unity integration](references/unity.md). For another engine, use its installed version's native lifecycle, physics, rendering, and test facilities; verify uncertain APIs in official documentation rather than porting Unity calls.

## Implement without the usual agent mistakes

- Keep one authoritative owner for movement, state, and camera composition; extend the existing system before creating another manager, event bus, input reader, or update loop.
- Separate gameplay truth from presentation. Visual recoil, shake, squash, or interpolation must not silently change colliders, targeting, economy, or saved state.
- Track units and clock domains: rates integrate once, displacement and engine-integrated velocity do not. Distinguish scaled simulation, unscaled UI/feedback, and real elapsed time used by persistence.
- Sample input edges in the input lifecycle and consume each action once at a valid transition; define expiry, cancellation, UI capture, and pause/focus behavior. Do not buffer purchases or destructive actions without a design reason.
- Give temporary effects explicit ownership and cleanup on completion, interruption, disable, scene change, and reuse. Restore the previous state rather than a guessed default.
- Keep tuning values named, bounded, and expressed in seconds or world units. Example values are starting hypotheses, not universal constants; compare feel before/after under identical conditions.
- Reuse engine features and existing assets. Add dependencies or abstractions only when a demonstrated need outweighs their cost; avoid unrelated refactors and speculative optimization.
- Match feedback to consequence: acknowledge input immediately, show success only after success, explain rejection, and keep important states distinguishable without relying solely on color, sound, or motion. Respect existing reduced-motion/intensity and audio settings.

## Verify the actual behavior

1. Run the smallest existing checks that exercise the changed behavior, then the relevant integration/build check. Confirm test count, failures, and fresh result artifacts; a successful process or zero discovered tests is not a passing suite.
2. Exercise a short representative play loop including success, failure, and retry. For timing/input changes compare low, target, and high frame rates, a hitch, rapid/held input, and pause/resume; for lifecycle changes include disable/re-enable, pooling or scene reload as applicable.
3. Inspect the real scene/prefab wiring and serialized overrides, not just source defaults. For visuals inspect the running output; for performance capture representative device/build measurements and state hardware, scene, duration, and frame-time statistics.
4. Use isolated tests or temporary fixtures when necessary; protect existing work and player saves, and remove only artifacts you created. Inspect harness arguments before running reset, auto-play, soak, or capture modes. Do not claim an old binary verifies new source.
5. Report observed results separately from code inferences and untested feel. If execution is blocked, name the blocker and provide the exact remaining check; do not turn a static review into a playtest claim.

Stop when the agreed behavior works, relevant regressions pass, and the change remains small. If a technique is irrelevant, record why instead of expanding scope. If a test fails, fix the demonstrated cause and rerun the affected check.

## Handoff

Give the player-visible result, changed files, before/after evidence, commands or reproduction steps, and remaining limitations. For an audit rank only actionable findings with file/line evidence, likely player impact, and a minimal fix; label hypotheses. Commit or publish only within the user's requested scope.
