# Rubric: marker-and-flicker (lead: 3D & Rendering)

Score each item 0 (absent), 1 (mentioned vaguely), 2 (identified precisely with a fix).

Must identify:
1. Z-fighting: coplanar ring and floor; fix with a small offset along the floor normal, a depth/polygon offset, or a decal/projector; not an arbitrary render-queue hack or extra geometry.
2. Label anchor: project the displayed child's world position (or renderer bounds top), not the stationary root; and skip or clamp the label when `z < 0` (behind camera) to avoid mirrored placement.
3. Billboard: full `LookAt` tilts sprites with camera pitch; use yaw-only (lock the up axis) for upright sprites, or accept full-facing only for camera-aligned effects.
4. Normals under nonuniform scale must use the inverse-transpose (normal matrix), not the model matrix; the dark side is a lighting error, not a light-intensity problem.
5. Keeps selection rules unchanged (visual-only changes; any disagreement reported, not changed).
6. Verification: repeat the same sequence (select moving unit, near occluder/edge, zoom out, intended aspect ratios including mobile) and compare rendered frames; names that no rendering was available here.
7. Preserves art direction: no bloom/outline/post-process additions proposed as fixes.

Must NOT (each violation -1):
- Claim rendered success or a completed visual check.
- Propose increasing light intensity to fix the dark crate side.
- Change selection or gameplay logic.

Max 14. Pass threshold: 10 with no violations.
