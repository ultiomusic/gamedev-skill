**Goal:** on desktop and on phones, the selected unit's ring sits steadily on the floor, its name label sits over the body you can see, health bars stay level and readable from steep camera angles, and stretched crates are lit evenly. What can be selected, and how, stays exactly the same.

**Approach:** this is purely a rendering problem, so I sent it to one specialist (3D & Rendering) in read-only mode and reviewed the result myself. I didn't bring in the Game Feel, Systems or Performance specialists because nothing here touches timing, rules or measured cost. One boundary for Systems is noted below.

**Limits:** nothing was rendered or run. Your project isn't on disk, so I didn't know the engine version, render pipeline, shader source, Canvas setup or target phones. The API names suggest Unity, but I haven't confirmed that. Everything below is a reasoned fix based on the four fragments, with the check that would confirm or reject it.

## 1. Selection ring flickers: two surfaces at the same depth
- **Cause:** the ring quad sits at exactly `floor.y` with an opaque material. Ring and floor are in the same plane, so they fight over which one is in front each frame.
- **Smallest fix:** add a depth bias in the ring's shader: `Offset -1, -1`. The ring stays where it is but always draws over the floor. If you can't edit the shader, lift the ring slightly instead: `y = floor.y + 0.01f`.
- **Tradeoff:** a lift that's too small still flickers on phones, which have less depth precision, especially with a large far-to-near camera range. A lift that's too big makes the ring look like it floats when the camera is low. The ring should also neither cast nor receive shadows.
- **Check:** hold the camera still for about 120 frames at a 15° and a 60° angle, fully zoomed out, on a real phone. The ring's pixels must not change from frame to frame. Reject the fix if the ring starts showing through the unit's feet or nearby props.

## 2. Name label sits beside the character and appears when the unit is behind the camera
- **Cause:** the label is placed using `unit.root`, which stays at the spawn point. The animated mesh is a child offset by (1.5, 0, 0), so the label lands 1.5 units to the side of what you see. The label is also drawn when `screenPos.z < 0`, so a mirrored "ghost" label appears for units behind the camera.
- **Smallest fix:**
  ```csharp
  var p = cam.WorldToScreenPoint(unit.body.position + Vector3.up * labelHeight); // body = animated child or head bone
  label.enabled = p.z > 0f;
  ```
- **Tradeoff:** follow the child or a head bone rather than `SkinnedMeshRenderer.bounds`, which can go stale while the unit is off screen. If the label sits on a scaled Canvas, the screen position needs the usual conversion to Canvas coordinates.
- **Check:** with the unit walking and turning, the label stays centred over its head from every direction. Pan until the unit is behind the camera: no label should appear. Check on a phone in portrait as well.

## 3. Health sprites tilt when the camera looks down
- **Cause:** `LookAt(camera.position)` turns each sprite toward the camera's position on all three axes. As a result, each bar tilts differently depending on where it is on screen. When the camera looks almost straight down, the bars roll. `LookAt` also points the sprite's back at the camera, so bars can show mirrored.
- **Smallest fix:** `transform.rotation = camera.transform.rotation;`. Every bar then lies flat to the screen and stays level.
- **Tradeoff:** the bars no longer angle toward the camera. They may cut into nearby geometry a little differently. I rejected a billboard that only turns around the vertical axis, because from above it shrinks to a thin line.
- **Check:** sweep the camera from 20° to 89° looking down, with bars in the centre and at the edges of the screen. They should stay level, and the fill should run the right way (not mirrored).

## 4. One side of stretched crates renders dark
- **Cause:** the crate is scaled (1, 1, 3), and the lighting transforms normals (surface directions) with the plain model matrix. That isn't correct when an object is stretched unevenly. Two possible causes fit the evidence:
  - **(a)** the shader skips the special normal transform (the inverse-transpose) and doesn't re-normalise. On a box, that skews the corner or bevel normals and leaves faces lit too brightly or too dimly.
  - **(b)** the normal is transformed as if it were a point, which picks up the crate's position. Then the shading depends on where the crate stands.
- **Smallest fix:** use the engine's own normal transform: `UnityObjectToWorldNormal` (built-in pipeline) or `TransformObjectToWorldNormal` (URP/HDRP). Then `normalize` again in the fragment shader. If the crate uses normal maps, keep the tangent sign (`unity_WorldTransformParams.w`).
- **Tradeoff:** none to speak of. Just confirm the edit doesn't break the pipeline's batching for these materials.
- **Check:** put a (1,1,3) crate next to a (1,1,1) crate and orbit a directional light around them. Matching faces should be equally bright at the same light angle. Move an unscaled crate far from the world origin: if it turns dark as well, the cause is (b).

## Confirming the fixes in the game
Record one scripted run before and after the fixes: select a unit, orbit the camera, change its angle, zoom out fully, move the unit behind the camera, then sweep the light. Capture it at 16:9 on desktop and in portrait on a real phone. Also log which unit gets selected for a fixed set of click points. That log must be identical before and after, which shows the selection rules didn't change.

## Remaining risks
- **Clicks may miss the visible body:** the label fix only reads the body's position. Selection logic is untouched. But if clicks are tested against a collider on `unit.root`, players clicking the body you can see will miss, because it is 1.5 units away. Fixing that is a selection and gameplay decision, so I left it out on purpose.
- **Ring and health bars may sit on the old spot:** they may be attached to `root` too. If so, they also sit 1.5 units beside the body. Moving them would mark a clickable area that isn't the real one, so decide that together with the click question above.

Skipped: actual rendering, on-device testing and the shader and Canvas sources (they weren't available), so none of these fixes is visually confirmed.
Risk: the 1.5-unit gap between `root` and the visible body probably affects clicking as well, and fixing that would change how selection works.
