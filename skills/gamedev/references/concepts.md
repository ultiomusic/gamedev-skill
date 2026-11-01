# Technique selection: 34 concepts

These are implementation decisions and acceptance checks. Read only the rows relevant to the task; examples are tunable, and built-in engine support takes precedence over reimplementation.

## 3D and rendering — 8 concepts

| Concept / use when | Decision and trap to avoid | Observable check |
| --- | --- | --- |
| Raycasting — picking, visibility, contact | Define origin, direction, range, layers, trigger policy and nearest/all-hit semantics; exclude self and use a volume sweep when thickness matters. | Hit the intended target at edges; UI and the shooter cannot steal the query. |
| Normals — slopes, impacts, reflections | Compare normalized vectors in the same space; use `dot(normal, up) >= cos(maxSlope)` and transform normals correctly under nonuniform scale. | Just-below/above-limit slopes classify correctly; effects face the surface. |
| Level of detail — distant geometry cost | Select by projected importance with hysteresis/fade where supported; preserve silhouette and independent gameplay/collision. | Oscillating near a threshold does not flicker; GPU time actually improves. |
| Frustum culling — unseen render work | Prefer engine bounds/culling, account for deformation and all relevant cameras/shadows; never equate invisible with gameplay-inactive. | Gameplay-relevant state stays correct off-screen; re-entry has no popping or stale state. |
| Fragment shader — surface/pixel effects | Use the project's shading language/pipeline, expose parameters, verify coordinate/color spaces and transparency; cost follows shaded coverage, not just mesh size. | Effect works in the target build and at large screen coverage within GPU budget. |
| Billboarding — readable world labels | Choose screen-aligned versus world-upright rotation and correct local facing axis; handle the rendering camera and parent transforms. | Label remains legible from orbiting/elevated cameras without mirroring. |
| Quaternions — orientation blends | Use engine shortest-arc interpolation with normalized rotations and explicit local/world order; `Slerp(current,target,k)` is not fixed-duration motion. | Cross the Euler wrap boundary smoothly; duration behaves consistently across frame rates. |
| Z-fighting — coplanar flicker | Remove duplicate surfaces, use appropriate decals/bias, and tighten clip range; don't repair depth with arbitrary large offsets. | Inspect near and far angles in the actual target depth pipeline. |

## Game feel — 10 concepts

| Concept / use when | Decision and trap to avoid | Observable check |
| --- | --- | --- |
| Delta time — frame-dependent behavior | Integrate rates once; use `1-exp(-k*dt)` for exponential response. Don't multiply engine velocity or mouse/touch displacement by dt; clamping discards elapsed time. | Equal input over equal elapsed time gives equivalent motion at low/high FPS and after hitches. |
| Easing — mechanical transitions | For a duration use clamped elapsed/duration from a captured start; repeated lerp is asymptotic smoothing. Define interruption/retarget behavior and avoid overshoot on semantic values. | End value is exact; interruptions do not jump or accumulate drift. |
| Screen shake — consequential impacts | Layer bounded, decaying positional/rotational noise over the authoritative camera; choose intensity by event importance and honor reduced motion. | Shake ends at zero without camera drift; aiming and UI remain usable. |
| Squash and stretch — readable motion/contact | Deform a visual child about the contact pivot, preserve intended volume and original scale, and cancel/reset safely; leave gameplay geometry independent. | Silhouette sells contact without moving hitboxes; repeated triggers restore the authored scale. |
| Coyote time — forgiving ledge departure | Track last valid support time and one consumed jump; deliberate jump takeoff must not grant a second jump. Omit where there is no such action. | Late-within-window succeeds once; late-outside and a second press fail correctly. |
| Input buffering — early action near eligibility | Store a timestamped press, expire/cancel it, and consume it once at eligibility; held input is not a new edge. Don't queue unrelated UI transactions. | Just-early succeeds once; expired, canceled, and UI-captured input never fires later. |
| Camera deadzone — distracting follow | Hold camera inside a chosen region, then follow smoothly; coordinate bounds, look-ahead, zoom and teleport reset with one camera owner. | Small movement stays stable; fast motion, edges and teleport keep the subject visible. |
| Hit stop — unreadable impact | Freeze only intended participants; advance release on an unaffected clock, keep input collection live, and explicitly choose UI/particle/camera behavior. | Stop ends even while simulation is paused; overlapping hits do not freeze forever or erase input. |
| Acceleration and friction — sluggish or abrupt control | Tune acceleration, braking and reversal separately in units/s², or time-based damping; preserve analog magnitude and avoid diagonal speed gain. | Measure start/stop distance and reversal at multiple rates; no unintended overshoot or slide. |
| Invincibility frames — repeated damage immunity | Gate damage with an explicit time/state rule, give readable feedback, and preserve collision/navigation unless phasing is intended. | Damage is blocked within the window and resumes after it; pooling/death clears immunity. |

## Systems — 9 concepts

| Concept / use when | Decision and trap to avoid | Observable check |
| --- | --- | --- |
| Finite state machine — incompatible actions | Make legal transitions and entry/exit cleanup explicit; keep orthogonal states separate instead of multiplying flags or building a generic framework. | Illegal transitions are rejected; cancel/death/restart cannot leave stale movement or feedback. |
| Hitbox and hurtbox — attack/contact ownership | Separate attack from damage reception, filter teams/layers and deduplicate per attack-target pair; don't apply damage once per overlapping collider each frame. | One attack causes intended damage once, including multi-collider targets and persistent overlap. |
| Fixed timestep — stable simulation | Use engine fixed updates or a bounded accumulator plus render interpolation; define backlog policy and bridge input edges. Fixed dt alone does not ensure determinism. | Equivalent runs remain within tolerance; a hitch cannot cause unbounded catch-up or missed input. |
| Tunneling — fast objects skip collision | Use suitable CCD/sweeps with object extent and relative motion; a ray at the destination is insufficient. Avoid globally shrinking timestep without measurement. | Fast/small bodies hit thin obstacles and moving targets under the worst supported step. |
| Pathfinding — routes around obstacles | Match graph/navmesh to agent clearance and costs; handle no-path, stale/partial paths and moving obstacles. For custom A*, match an admissible heuristic to costs and prevent corner cutting; throttle replans. | Narrow gaps, unreachable goals and changed obstacles produce safe, bounded outcomes; custom routes match expected cost. |
| Steering behaviors — local movement along intent | Bound acceleration/speed, choose avoidance priority and arrival braking; local steering cannot solve global traps. Reuse physics/navigation ownership. | Agents arrive without orbiting and avoid neighbors without blocking forever. |
| Seeded noise — reproducible procedural variation | Persist seed plus generator version/parameters and player changes; isolate random streams. A seed alone is not a complete save or cross-version guarantee. | Recreating with the same inputs matches; unrelated random calls do not reshuffle the world. |
| Object pooling — measured lifetime churn | Reset timers, transforms, physics, subscriptions, trails and gameplay flags; define overflow and release ownership. Pool only where churn justifies retained memory. | Reacquired objects behave fresh, double release is caught, and peak memory stays bounded. |
| Particle system — transient feedback | Emit bursts on meaningful events and continuous effects at time-based rates; choose local/world space, lifetime and cap. Reuse only with complete reset, never retrigger a burst each frame. | One event gives one burst; continuous density is comparable across FPS, load is bounded, reuse has no stale particles. |

## Performance — 7 concepts

| Concept / use when | Decision and trap to avoid | Observable check |
| --- | --- | --- |
| Frame budget — missed responsiveness target | Derive milliseconds as `1000/targetFPS`; capture CPU/GPU, allocations, p95/p99 and spikes after warmup on representative hardware. FPS averages hide hitches. | Same scene/run before and after meets the stated budget without lost behavior. |
| Draw calls — submission-bound CPU | Inspect batching breaks, materials and instancing in the frame debugger; preserve culling and ordering. Fewer calls need not mean faster frames. | CPU/GPU timings improve; batching doesn't inflate invisible geometry or break transparency. |
| Spatial partitioning — excessive neighbor queries | Use engine broad phase first; custom grids must cover full object bounds, neighboring cells, negative coordinates and deduplicate pairs; use 3D neighborhoods in 3D. | Results equal a brute-force oracle at boundaries/large extents with fewer candidate checks. |
| Overdraw — fill-rate-heavy effects/UI | Measure transparent screen coverage, trim/cap layers and consider reduced-resolution effects only when justified; invisible pixels can still cost shading. | Worst-case overlapping effects reduce GPU time while important feedback remains readable. |
| Time slicing — expensive nonurgent decisions | Budget decisions by time or buckets, define maximum staleness/fairness, and keep movement/input timely; stagger reinitialization to avoid synchronized spikes. | No agent starves, response latency stays acceptable at low FPS, spikes actually fall. |
| Texture atlas — compatible texture switches | Use engine atlasing, mip-safe padding/extrusion, correct UVs and memory limits; shared texture alone doesn't guarantee one batch across materials, masks or sorting. | No edge bleed at scaled/mipped views; frame debugger confirms the intended batching. |
| Chunk streaming — large world residency | Preload ahead, unload farther out, stage activation, cancel stale requests and persist mutations; protect collision readiness and active references at boundaries. | Fast travel/teleport and repeated border crossings avoid holes, thrashing and lost progress. |
