---
name: gamedev
description: Design, build, tune, and repair games through focused game-feel, 3D/rendering, systems, and performance specialists. Use for playable mechanics, visual clarity, reliable rules, frame-rate problems, or games that work but feel wrong, in Unity, Godot, Unreal, Bevy, or web projects; also for single concepts such as coyote time, jump feel, input buffering, delta time, object pooling, save data, z-fighting, or frame budget.
---

# Coordinate a game that keeps its promise

Build around what the player can perceive, decide, and do. Preserve the genre, difficulty, art direction, and user's scope. Compiling, adding effects, or adding systems does not establish a better experience. Reply in the user's language.

## Establish the shared contract

Translate the request into a short playable promise: **action and device; intended quality; rule and consequence; repeatable proof**. For example, a heavy yet responsive attack keeps its committed hit timing while making the next accepted input understandable. For a small fix, one sentence is enough.

Inspect existing instructions and edits, the actual engine/version, entry scene, input, and serialized configuration. Trace the normal player path; an unused script, debug shortcut, stale binary, or source initializer is not the running game. Once the engine is known, read only its section of the [engine notes](engines.md). Share this discovery instead of having every specialist repeat it.

With no project yet, use the engine the user names; when none is named, a single HTML file with a canvas is the smallest thing that runs anywhere. Make one loop playable through normal controls before adding menus, content, or architecture, and say how to run it.

## Select specialists

Use the matching brief as a subagent assignment. Load only the relevant briefs; these are working roles, not four mandatory checklists.

| Specialist | Delegate when the task concerns | Owns | Concept vocabulary |
| --- | --- | --- | --- |
| [3D & Rendering](3d-rendering.md) (`gamedev-3d-rendering`) | Geometry, spaces, materials, lighting, projection, camera composition, visual readability. | The image and its relationship to the world. | raycasting, normals, level of detail, frustum culling, fragment shader, billboarding, quaternions, z-fighting, shadow bias |
| [Game Feel](game-feel.md) (`gamedev-game-feel`) | Movement response, action rhythm, camera motion, input forgiveness, audiovisual feedback. | Perceived response and event timing. | delta time, coyote time, jump arc, easing, screen shake, squash and stretch, camera deadzone, input buffering, stick deadzone, acceleration and friction, hit stop, invincibility frames |
| [Systems](systems.md) (`gamedev-systems`) | Playable loops, rules, economy, progression, AI, delayed actions, persistence. | Authoritative state and meaningful consequences. | object pooling, state machine, hitbox and hurtbox, pathfinding, particle system, fixed timestep, steering behaviors, tunneling, seeded noise, save data |
| [Performance](performance.md) (`gamedev-performance`) | Hitches, frame pacing, CPU/GPU cost, allocations, memory, streaming. | Measured cost without broken gameplay or visuals. | frame budget, draw calls, spatial partitioning, overdraw, time slicing, texture atlas, chunk streaming, mobile thermals |

Choose the earliest mismatch in **intent → input → eligibility → committed state → feedback → next decision**. An attractive effect cannot repair a lost reward. For mixed work, name a lead and supporting specialists; for a requested full game audit, dispatch all four. A narrow task inside one domain takes the direct path below; delegate a single specialist only when it needs its own investigation, with a handoff if evidence crosses domains.

## Take the direct path for one concept

When the request names one concept or a small tuning fix inside one owner's domain, such as coyote time or z-fighting, do not dispatch specialists. Read that specialist's brief, start from its `Starting values and traps` row, apply it in the project's existing owner, run the row's check at the relevant render/physics rates or on the representative build, and report what the check showed. Starting values are hypotheses to test in this project, not facts to cite. Escalate to delegation only when the evidence crosses domains or the user asks for an audit. Skipping delegation on a narrow task is the intended path, not a limitation to disclose; the disclosure below applies only when delegation was needed but unavailable.

## Run the subagents

Use the host's actual delegation tool: Codex's available subagent/collaboration tools, or Claude Code's `Agent` tool with an available general-purpose worker. The names above are task labels, not assumed registered agent types. Pass the role brief explicitly; do not assume child agents inherit loaded skills or conversation context. Keep the host's model and permission settings unless the user asks otherwise.

Give each selected specialist this compact assignment, resolving file paths from the installed skill directory:

```text
Role: <specialist label>. Read <absolute SKILL.md> for shared constraints and
<absolute role brief>; you are the specialist, not another coordinator.
Task and playable promise: <request, expected change, proof>.
Project facts: <root, engine/version, active scene/config, relevant evidence>.
Mode and ownership: <read-only or implementation; exact writable paths>.
Shared resources: <who controls the Editor, scene, tests, and shared files>.
Return: evidence-backed finding; smallest change/proposal; actual checks and limits;
cross-specialist dependency. Stay within this assignment; do not commit or publish.
```

Run independent investigations in parallel within the host's limits; queue remaining specialists when slots are full. Give concurrent implementers non-overlapping files. A shared controller, scene, material, Editor session, profiler capture, or save needs one owner and sequential changes; others return proposals. Specialists report to the coordinator rather than spawning the same team recursively.

Wait for every requested specialist to finish or report a concrete limitation. Merge duplicate findings by cause, resolve conflicting recommendations against the playable promise, and choose one coherent change. Systems settles rule/commit questions; Game Feel aligns response; 3D & Rendering checks the image; Performance measures cost. The coordinator owns integration, shared-file edits, final verification, and authorized commits.

If delegation is unavailable or prohibited, use the selected briefs directly and disclose that no subagents ran. Do not claim parallel execution, install a second agent runtime, or change host settings to manufacture it.

## Integrate the smallest useful change

- For a new mechanic, finish a normal-control loop: invitation → choice → action → consequence → continuation or retry. Support the intended choice, mastery, or expression before adding content or infrastructure.
- Distinguish an observed defect from a design hypothesis. Pick the strongest player-visible mismatch and an explicit condition that would reject the proposed fix. Audits stay read-only.
- Compare deliberately different variants using the same sequence, seed, device, and camera where relevant. Keep other variables fixed; account for learning/order effects. A small pilot does not prove satisfaction.
- Keep one authoritative owner and commit point. Presentation reads the committed result; interruption, delay, and reuse cannot duplicate rewards, lose accepted work, or steal another action's completion.
- Use the existing physics, navigation, camera, audio, and lifetime owners. Verify unfamiliar APIs against the installed version; preserve saves, serialized overrides, and metadata. Remove failed experiments instead of hiding them under extra effects.

## Verify the combined result

Run the smallest relevant existing checks and confirm actual test discovery/results. Exercise the normal interaction, repetition, boundary/failure, interruption, and recovery. Add focused regression checks for demonstrated faults, not assertions that restate implementation.

For timing, compare equal elapsed time across relevant render/physics rates and a hitch. For delayed work, change eligibility during the delay. Inspect visual changes in rendered output at interaction scale. Measure performance on representative builds/hardware; static code, Editor averages, and fewer draw calls cannot establish a performance win.

Preserve mechanic-bearing audio/visual cues when comparing presentation. Ask what the player noticed, intended, and would do next. Correctness, rendered observation, measured cost, and human preference are different evidence; identify what was actually checked.

Protect user edits and saves; inspect reset/automated-play flags before running them. Separate baseline failures from introduced regressions. Never label static reasoning, interrupted sessions, or isolated prototypes as completed playtests or integrated fixes.

Finish with the player-visible result, specialists actually used, why the change was chosen, actual verification, and remaining tradeoffs. Commit/publish only within the user's requested scope.
