---
name: gamedev
description: Design, build, tune, and repair playable game mechanics and game feel; use for controls, combat, cameras, progression, feedback, and gameplay performance, including AI-generated games that work but feel wrong.
---

# Make the player's action matter

Build around what the player can perceive, decide, and do. A mechanic is complete when its intention, rule, consequence, and next opportunity agree. Compiling, adding effects, or implementing more systems does not establish that agreement. Preserve the intended genre, difficulty and art direction; reply in the user's language.

## Start with a playable promise

Translate the request into a short working contract; for a small fix, one sentence is enough:
- **Action:** what the player tries, in which situation, on which input device.
- **Character:** one or two desired qualities and their tension, such as heavy yet controllable, tense yet readable, or relaxed yet consequential.
- **Rule:** when the action is allowed, what success changes, and what rejection, interruption or failure does.
- **Proof:** a repeatable sequence in which the player can notice the intended difference.

Use existing design and runtime evidence to fill gaps. When intent is vague, choose a small reversible hypothesis and state the assumption; clarify only if the answer changes the design substantially. With only a snippet or symptom, give bounded guidance without inventing a project or execution.

Inspect the current diff, instructions, actual engine/version, entry scene, input and serialized configuration before editing. Trace the normal player path to the mechanic; do not mistake an unused script, debug shortcut or source initializer for the running game. Read [Unity integration](references/unity.md) for Unity execution and wiring.

## Find the break in the experience

For an existing mechanic, trace **intent → input → eligibility → committed state → feedback → next decision**. Find the earliest mismatch; late-stage polish cannot repair an earlier broken promise.

| What the player experiences | First investigation | A useful outcome |
| --- | --- | --- |
| “It ignored me” or “I did not mean that” | Input ownership, UI capture, action eligibility, consumption and cancellation. | The intended action is acknowledged once; rejected actions explain why without firing later. |
| “It works, but feels wrong” | Start/stop/reversal, contact timing, camera framing, and feedback relative to the state change. | Change a named response characteristic while preserving the rule and challenge. |
| “I do the same thing every time” | Whether the intended reward is a consequential choice, expression, or mastery of execution. | A meaningful tradeoff, clearer consequence, or learnable challenge without inventing unwanted variety. |
| “I lost and do not know why” | Threat visibility, telegraph, actual collision/damage, and the route back to agency. | The player can attribute the outcome and name a different action to try. |
| “It gets worse when busy” | The same interaction under peak simulation, visual and input load. | Stable action timing and readable priorities within the measured frame budget. |

For a new mechanic, build the smallest complete loop reachable through normal controls: invitation → choice → action → consequence → continuation or retry. Finish that loop before multiplying content, upgrade trees, managers or configuration. Decide where the new action lives in the existing loop and which old behavior it replaces or extends.

For design or tuning work, read the relevant exercise in [the gameplay playbook](references/gameplay.md). Use it to produce an implementation or a falsifiable experiment, not a list of techniques. Audits stay read-only and rank findings instead of adding features.

## Turn a feeling into a controllable change

1. Choose the strongest player-visible mismatch. Record the current response and the proposed difference; distinguish an observed defect from a design hypothesis.
2. Pick a small set of parameters tied to that difference. Express movement as time/distance/acceleration, action rhythm as eligibility/commit/recovery, and feedback as onset/peak/decay. Do not hide latency under animation or transplant constants from another genre.
3. Compare two deliberately distinguishable variants under the same sequence, seed, device and camera when useful. Keep other variables fixed; test a coordinated group only when its interaction is the hypothesis. Account for learning/order effects with counterbalanced runs or comparable fresh scenarios/players; a small pilot is not statistical proof. Avoid exposing every internal constant as a tuning control.
4. Choose using the promised experience and its cost. Greater immediacy can reduce weight; more anticipation can improve fairness but slow repetition; stronger feedback can obscure the next decision. Record the tradeoff instead of calling every increase an improvement.
5. Retain the smallest coherent change, remove experimental clutter, and stop when the stated contract is met. If the hypothesis fails, revert that experiment before adding compensating effects.

## Make the implementation keep its promise

- Give each action one authoritative commit point and owner. Acknowledge a press separately from confirming success; award, charge, damage, spawn and emit success feedback from the committed result, once. Decide what is queued, replaceable, cancelable or irreversible.
- Revalidate delayed actions when they complete. Reserve capacity/resources when needed, release reservations on cancellation, and define partial acceptance/refund behavior. A target or pooled object must still represent the same action when a callback returns.
- Keep simulation truth separate from display. Shake, recoil, squash, hover and interpolation must not accidentally move collision, selection anchors or saved state; intentional aim changes belong to gameplay. Derive world feedback from the object actually shown, in the correct space.
- Interruptions are normal gameplay: repeat, reverse, pause, lose focus, cancel, die, unload and reuse. Define which action wins; an effect must not steal another action's completion callback, remember an intermediate pose as home, or restore someone else's clock/camera state.
- Use units and clock domains explicitly. Integrate rates once; engine-integrated velocity and pointer displacement are not rates to multiply by dt again. Use an unaffected clock to end a freeze; fixed simulation needs bounded catch-up, input bridging and separate render interpolation.
- Use the existing engine and project owners for physics, navigation, camera, audio and lifetime. Check unfamiliar APIs against the installed engine version before depending on them. Do not add a parallel controller or a generic framework for a local symptom. Preserve save compatibility, serialized overrides and metadata.
- Give feedback a hierarchy: critical threat/rejection, primary action, then ambient decoration. Coordinate contact sound, visible contact and state change; vary repeated sounds without changing their meaning, limit simultaneous voices/effects, and respect motion/audio settings. Essential information needs an alternative when a channel is unavailable.
- Optimize the measured bottleneck while preserving the action contract. Off-screen does not mean irrelevant, pooling does not reduce overdraw, and fewer draw calls do not guarantee shorter frames. Simplify low-value work before reducing control responsiveness or hiding needed information.

## Judge the result by play and evidence

Run the smallest relevant existing checks, and confirm actual test discovery/results. Then exercise the normal interaction: first attempt, repeat, boundary/failure, interruption and recovery. Add focused regression checks for demonstrated faults, not tests that restate your implementation.

For timing changes, compare equal elapsed time at low/target/high render rates and relevant physics steps, including a hitch. For delayed work, change eligibility during the delay. For visual changes, inspect the rendered scene at the actual interaction scale. For performance, measure representative builds/hardware and slow-frame statistics rather than editor averages.

When evaluating feel, compare the same play sequence before/after. Where useful, reduce optional presentation layers to check whether the rule remains legible; preserve audio/visual cues that are themselves the mechanic. Ask what the player noticed, intended and would do next, rather than merely whether it “feels better.” Automated correctness and human preference are different evidence.

Protect existing edits and saves; inspect automated-play/reset flags before running them. A stale binary cannot validate new source. Separate baseline failures from introduced regressions; fix only within the authorized task. Never report static analysis or an isolated prototype as a rendered playtest or integrated fix.

Finish with the player-visible change, why it was chosen, what was actually tested, and the remaining tradeoff or uncertainty. For audits give evidence, a minimal correction and the next discriminating test; for implementation deliver the working loop rather than an unsolicited roadmap. Commit/publish only within the user's requested scope.
