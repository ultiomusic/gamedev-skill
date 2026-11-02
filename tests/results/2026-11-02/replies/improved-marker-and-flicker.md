# Selection ring, name label, health sprites, crate lighting

**What the fix should achieve:** with the mouse on desktop or touch on mobile, a selected unit shows a steady ring on the floor under it, a name label over its visible body and health bars that sit flat to the screen. Scaled crates light the same way as unscaled ones. Selection rules stay exactly as they are. **How to prove it:** run one fixed camera path before and after each fix, on desktop and on a mobile device, and compare the rendered frames. The path should cover head-on views, grazing angles, looking straight down, the screen edge and the target behind the camera.

All four problems are in the 3D & Rendering area (z-fighting, label anchor and projection, billboarding, normal transform). So I worked from that one area's guide and did not dispatch any specialists. That is the normal approach for a narrow task like this; nothing was unavailable. `Camera.WorldToScreenPoint` suggests Unity, but the engine, its version and the render pipeline are not confirmed. The Unity names below are a likely mapping, not verified APIs.

## Fixes, smallest first

### 1. Selection ring flickers: z-fighting
- **Cause:** the quad sits at exactly `floor.y`, so it is coplanar with the floor. The two surfaces fight over depth. This gets worse at grazing angles, at long distances and on mobile, where depth precision is lower.
- **Change:** lift only the ring's renderer about 1 cm along the floor normal (`y = floor.y + 0.01`). If a collider or any selection logic reads the ring's transform, move only a render-only child so selection rules don't change. Also check that the camera near plane is about 0.1 and not 0.01. A near plane that is too small wastes depth precision and causes this kind of flicker.
- **Alternative:** keep the quad coplanar and give the ring material a polygon offset (ShaderLab `Offset -1, -4`). This avoids any visible gap, but it means changing a material or shader.
- **Tradeoff:** too large a lift makes the ring look like it floats at close zoom. On sloped or uneven floors, the lift has to follow the surface normal.

### 2. Name label sits beside the character: wrong anchor, and no check for targets behind the camera
- **Cause:** the label projects `unit.root`, which stays at the spawn point. The visible mesh is a child offset by (1.5, 0, 0).
- **Change:** project the displayed object instead. Use the animated child's world position plus a height offset, or the top of its renderer bounds, or a head bone if one exists. Read it after animation has run (`LateUpdate`). Hide the label when `screenPos.z < 0`. Behind-camera points project mirrored, so today they show up as stray labels.
- **Tradeoff:** a bounds-based anchor bobs slightly with the animation. A fixed bone or offset is steadier but has to be set per rig.
- **Boundary for Systems, not changed here:** if selection or targeting also uses `unit.root`, what the player clicks is about 1.5 units away from what they see. You asked me not to change selection rules, so I'm only flagging it. Whether root and mesh are meant to separate is a rules question.

### 3. Health sprites tilt when the camera looks down: the wrong billboard type
- **Cause:** `LookAt(camera.position)` turns each sprite toward a point. Sprites away from screen centre therefore end up at different angles. As the camera pitches toward straight down, the default world-up reference degenerates and causes roll or spin.
- **Change:** health bars should take the full camera rotation and stay parallel to the screen: set `transform.rotation = camera.transform.rotation` as a **world** rotation, so a rotating parent doesn't add its own turn.
- **Only if the art direction wants bars standing upright in the world:** use yaw only (zero the y part of the to-camera vector, normalize it, then look along it). Tradeoff: at steep top-down angles, yaw-only bars shrink to thin slivers.

### 4. One side of scaled crates renders dark: normals transformed with the model matrix
- **Cause:** with the (1, 1, 3) non-uniform scale, the model matrix skews and stretches normals. Smoothed or bevelled normals bend toward z, and their length changes too.
- **Change:** in the crate's lighting, transform normals with the normal matrix (the inverse-transpose of the model 3x3), then renormalize. Unity provides `UnityObjectToWorldNormal` (built-in pipeline) and `TransformObjectToWorldNormal` (URP); use whichever matches the installed pipeline. Fix every shader variant, including mobile and low-LOD ones. Don't make the lights brighter to compensate.
- **Alternative:** bake the scale into a separate crate mesh. Lighting is then correct with no shader change, but you have an extra asset to maintain.

None of these adds a render pass, a light or transparent coverage. I expect no meaningful performance cost, but I measured nothing.

## How to confirm each fix in rendered output
Use the game view or a player build (not the Scene view), with the same camera path and seed before and after, on desktop and on one real mobile device:

- **Ring:** orbit to grazing angles at maximum zoom-out and watch for several seconds. Pass: no flicker. Then zoom fully in. Pass: no visible gap under the ring. Repeat the usual select and deselect clicks or taps. Pass: the same units are selected as before.
- **Label:** select a unit that is moving and animating, then pan it to the screen edge. Pass: the label stays centred over the visible body. Rotate the camera until the unit is behind it. Pass: no label appears. Check the mobile aspect ratio too. If the label lives in a scaled UI canvas, screen pixels and canvas units may differ.
- **Health bars:** with several units spread across the screen, pitch the camera from horizontal to straight down. Pass: every bar stays level on screen, with no roll or spin, including near straight down.
- **Crate:** put a (1, 1, 3) crate next to a (1, 1, 1) crate and sweep a light, or the camera, around both. Pass: each face of the scaled crate is shaded like the same face of the unscaled one. A temporary debug view of world normals makes any skew obvious; remove it afterwards.
- **Reject a fix if:** the ring visibly floats, the label drifts off the body or jitters, the bars read worse at your usual camera angle, or the crate looks right only after changing light intensity.

## What I could not check
There is no project on disk, so I edited nothing and rendered nothing. Everything above is a source-level hypothesis based on the four fragments. I could not confirm:
- the engine, its version or the render pipeline
- the actual crate shader, or whether it normalizes the normal
- whether the ring has a collider or any selection role
- why `unit.root` stays at spawn
- the label's UI canvas mode
- the mobile depth-buffer precision or the camera near and far planes

No test, build or play session was run.
