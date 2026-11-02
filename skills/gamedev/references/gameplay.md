# Exercises for building and tuning gameplay

Use the exercise that answers the current design question. Each ends in a small change and a way to reject it; none is a compulsory feature list. Values below are relationships to derive from the game's scale and intent, not prescribed feel settings.

## 1. Make a loop worth repeating

Write a single cycle using player verbs: notice a need, choose an approach, act, read the consequence, try again. Identify the decision that changes the next cycle, or the execution skill the player is learning to perform more reliably. For a quiet builder that may be storage versus production; for an action game it may be position versus commitment; a puzzle may reward understanding, and a rhythm game may reward mastery of the same pattern.

For a choice-driven loop, try two plausible actions from the same starting state. If they always lead to the same next decision at the same cost, investigate whether the distinction is cosmetic or an intentional expressive choice. Strengthen an existing consequence before inventing another resource, timer or progression layer. If one option dominates, test a situational cost, timing or spatial constraint instead of inflating every number. For mastery, compare repeated attempts for controllability, attributable mistakes and learning instead of forcing strategic variety.

Walk the opening through normal controls without insider knowledge. Is the first useful action visible, its consequence understandable, and another action available? Teach through a safe opportunity and a changed situation that reuses the lesson. Add explanation where an actual misunderstanding remains; do not solve an unreadable action with a wall of tutorial text.

**Experiment:** change one existing cost, affordance or consequence; replay the same short scenario with two approaches, or repeat the same task when mastery is the goal. Keep the change only if it supports the intended choice, learning or expression, or removes the identified confusion. Do not equate more clicks, longer waiting or a higher reward count with engagement.

## 2. Shape movement without hiding input

Separate input acknowledgment, acceleration, maximum speed, braking, reversal and presentation. “Heavy” can mean momentum, a planted pose or low-frequency sound; it need not mean a delayed command. Choose which property communicates weight and which remains responsive.

Derive a first tuning point from designer-readable targets. For constant acceleration, `a = targetSpeed / timeToSpeed`; for constant braking, `brake = speed² / (2 * stopDistance)`. A constant-gravity jump with rise height `h` and time to apex `t` starts from `gravityMagnitude = 2h/t²`, `launchSpeed = 2h/t`; variable gravity or air control needs its own model. These idealized relationships need collision/slope validation, not literal reuse in every controller.

Sample and preserve input intent; cap diagonal magnitude without destroying analog control. Where forgiveness serves the game, an early buffered press and late support grace must be separately bounded and consumed once. Deliberate takeoff must not refresh a second jump. For touch, distinguish tap, drag, release, cancellation and the finger that owns the gesture.

**Experiment:** start, release, reverse, traverse a narrow passage, and repeat on relevant surfaces at different frame/physics rates. Compare measured distances and missed corrections. If motion is correct but looks late, examine camera/animation phase before increasing simulation speed.

## 3. Give actions readable commitment and recovery

Lay out an action in time: intent accepted, anticipation, rule commits, consequence is shown, next action becomes legal. Label cancel/replace/queue behavior at each stage. An animation's end is not automatically the right commit point, and an attractive recovery can still frustrate the next input.

For an attack, align active contact, hit detection and sound; deduplicate per attack/target and distinguish damage immunity from physical collision. Choose query/volume/continuous collision according to the actual reach and speed. A late visible trail must not imply a hit that the rule rejects. For construction, separate a placement preview from a charged/occupied tile and from its settling animation. Re-selection must not cancel construction completion.

Deliver immediate acknowledgment, event-aligned consequence and clear readiness. Reserve louder sound, stronger deformation, longer local pause or camera motion for higher importance; don't use all channels at maximum for every event. Keep simulation and feedback clocks intentional, and give repeated events a bounded overlap policy.

**Experiment:** interrupt at each boundary, press again just before readiness, and trigger several events together. Check one commit, truthful success/failure feedback, the intended next action, and a return to the authored resting pose. Adjust timing before adding more particles.

## 4. Make the camera and image support the next decision

Decide what the player needs to see next: landing area, approaching threat, neighboring tiles or the selected unit's destination. Frame for that information before choosing smoothing. Test screen edges, occluders, aspect ratios, zoom extremes and UI coverage; minimum clickable/legible screen size matters more than a world-space offset alone.

Keep one camera composition owner. Follow the final simulation pose, handle teleports explicitly, and use deadzones/look-ahead only when they reduce unwanted motion without hiding relevant space. Blend rotations along the intended arc; apply temporary shake around a stable pose. Labels and selection cues must track their rendered target, use the correct projection, and avoid accidental mirroring or occlusion.

Fix depth/silhouette/contrast problems before shader embellishment. Validate normals and surface offsets in the same coordinate space; decorative deformation must not produce stale render bounds or misleading contact. Preserve the existing visual language instead of pasting in unrelated “juice.”

**Experiment:** replay a turn, selection or encounter with only framing changed. Compare whether the needed target is visible before action and whether the camera needs manual correction. Inspect the actual output; matrix math alone cannot establish comfort or readability.

## 5. Preserve trust when rewards and progression are delayed

Treat an action as intent → validated commitment → settlement. Use one source of truth for inventory, health, currency and unlocks; UI counters may animate toward the authoritative value but may not award it again. Preview the meaningful cost/result before commitment and report the amount actually accepted.

Change the world while the animation runs: fill storage, spend the balance, replace the target, cancel, pause or reload. Decide whether to reserve, reject, refund, retain a remainder or return the object. Neither a success sound for zero payout nor silently lost overflow is an acceptable accidental policy. Reused object identity and saved pending work need explicit treatment.

Assess progression by new decisions, capability and pressure, not only rising numbers. Compare plausible strategies, recovery after a mistake, and the point at which waiting has no interesting decision. Keep intentional idle pacing; do not add urgency, punishment or monetization to manufacture engagement. Seeded generation must preserve player changes and generator compatibility, not just the seed.

**Experiment:** run a short ordinary path plus a boundary path through the same action. Account for value before/after, ensure it commits once, and confirm the player can explain the next useful choice. A bot simulation can test arithmetic/pacing bounds, not prove satisfaction.

## 6. Make opposition teachable and fair

Separate knowledge, decision, navigation and execution. Define what an agent can perceive and how it reacts before changing its intelligence or health. Telegraph meaningful intent early enough for the intended response; make damage rules and visuals agree. Distinguish “the player chose poorly” from “the game hid the information.”

Use global routing for connectivity and local steering for neighbors/arrival; neither substitutes for the other. Respect body clearance, unreachable goals and dynamic obstruction. Give decision scheduling a maximum stale interval and urgent-event path; keep movement/control smooth. Difficulty can change options, timing and coordination without granting unexplained perception or damage exceptions.

**Experiment:** repeat a controlled encounter with a valid response, a deliberate mistake and a blocked route. Verify the response matters, the failure is attributable, and retry returns the player to agency without stale targets/state. Do not add enemies or combat to a game whose loop does not call for them.

## 7. Keep the loop stable under load

Reproduce the expensive moment rather than optimizing an empty scene. Set a target in milliseconds (`1000 / targetFPS`), compare CPU/GPU and allocations, and inspect slow frames after warmup. Keep the same scene, settings and action sequence when comparing variants.

Choose the lever that matches evidence: reduce compatible material/state changes for submission cost; reduce transparent coverage/shader work for fill cost; use engine spatial queries or bounded decision work for simulation cost; pool actual lifetime churn with full reset; stream/activate in bounded work with hysteresis and safe cancellation for traversal spikes. Atlases, instancing, LOD and culling still need correct ordering, bounds, shadows and memory behavior.

Sacrifice low-value decoration before input, critical telegraphs or state correctness. Off-screen gameplay may still matter; skipped simulation needs an explicit policy. Spatial broad-phase candidates still need exact checks. Streaming must retain persistent edits and collision readiness; a seed or pooled chunk is not a save system.

**Experiment:** replay the busiest relevant action, including fast travel or repeated spawning if applicable. Accept an optimization only when timing improves without changing outcomes, losing readable cues, increasing unacceptable memory, or postponing the hitch to the next boundary.
