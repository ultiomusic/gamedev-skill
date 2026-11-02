# Four visual fixes: ring, label, health sprites, crate lighting

The fragments look like Unity (`Camera.WorldToScreenPoint`, `transform.LookAt`), so I've written the fixes in Unity terms. The same ideas work in any engine. Every change below affects rendering only. None of them moves `unit.root`, a collider, a layer or a raycast, so the selection rules stay as they are.

## 1. Selection ring flickers: z-fighting

**Cause:** the ring sits at exactly `floor.y`. It has the same depth as the floor, so the depth test picks a winner pixel by pixel and frame by frame. Mobile makes it worse because depth precision is usually lower there (16 or 24 bit, sometimes a far/near ratio set for a big map).

**Smallest fix (choose one):**
- **A. Lift it:** `ring.y = floor.y + 0.01f;`. That's one line. Scale the 0.01 to your world units and camera far plane.
- **B. Depth bias in the ring's material** (`Offset -1, -1` in a ShaderLab pass, or the equivalent polygon offset or depth-bias setting). This needs a small shader or material change, but nothing moves in the world.

**Tradeoffs:**
- **A:** at grazing camera angles the ring can look like it floats, or it can clip into the floor on slopes and uneven ground. Too small an epsilon still flickers at long range.
- **B:** keeps the ring flat on the floor. How strong the bias is varies by GPU and API, so it needs a check on real devices.
- **Optional extra:** moving the ring to a transparent queue with `ZWrite Off` after the floor also hides the fighting. However, it changes sort order against other transparent objects. I'd only do that if the ring is supposed to be translucent anyway.
- **Root cause:** a near plane that's too small (for example 0.01) makes z-fighting worse everywhere. Raising it is a valid fix, but it affects the whole scene, so check close-up shots before doing it.

**Confirm:**
- Orbit the camera at a low pitch (10 to 20 degrees) and zoom to the farthest distance players can reach, on the editor and on a real phone.
- The ring should show no shimmer or striping while the camera moves.
- At a grazing angle, check that the ring doesn't visibly float (fix A) and isn't cut by the floor (fix B).

## 2. Name label beside the character, and labels behind the camera

**Cause:** the label projects `unit.root.position`. The root stays at the spawn point, but the visible mesh is a child offset by (1.5, 0, 0), so the label lands 1.5 units to the side. Separately, when `screenPos.z < 0` the point is behind the camera. The projection then mirrors it, and a ghost label appears on screen.

**Smallest fix:**
```csharp
// anchor to what the player sees, not the logical root (root is left alone: selection may use it)
Vector3 anchor = unit.meshChild.position + Vector3.up * labelHeight;
Vector3 screenPos = cam.WorldToScreenPoint(anchor);
label.enabled = screenPos.z > 0;
if (label.enabled) label.position = screenPos;
```
A dedicated empty `LabelAnchor` transform parented under the animated mesh is just as small, and lets an artist set the height.

**Tradeoffs:**
- **A fixed child or anchor transform** is stable. If the animation moves the body away from the child's pivot (root motion baked into a bone), the label still drifts a little.
- **`renderer.bounds.center` plus the extents** follows the pose, but bobs every frame with the animation, so I'd avoid it.
- **Don't "fix" the offset by moving `unit.root` onto the mesh.** It's probably what selection and gameplay read, so that would change the selection rules. However, the child offset of 1.5 units suggests the selection ring or hitbox may also be centered on the root rather than on the visible body. Check that, but don't change it as part of this task.
- **Mobile:** `WorldToScreenPoint` returns physical pixels. If the label lives on a scaled Canvas (Screen Space - Camera, or a Canvas Scaler), convert with `RectTransformUtility.ScreenPointToLocalPointInRectangle`. Otherwise the label is offset on high-DPI phones even after this fix.

**Confirm:**
- Take a screenshot with a unit idle and walking. The label should be horizontally centered over the head within a few pixels.
- Rotate the camera until a labeled unit is directly behind it. No label should appear on screen.
- Check on a phone at native resolution and in a different aspect ratio.

## 3. Health sprites tilt when the camera looks down

**Cause:** `LookAt(camera.position)` turns each sprite toward the camera's position using world up as the roll reference. Two things go wrong:
- Sprites in different parts of the screen face slightly different directions, which looks like skew.
- As the camera pitches toward straight down, the look direction becomes parallel to world up. The roll is then undefined and the sprites spin or flip.

**Smallest fix:** align every sprite with the camera's rotation instead of pointing it at the camera's position:
```csharp
transform.rotation = cam.transform.rotation;   // screen-aligned billboard, no roll degeneracy
```
If the sprite shows its back face or appears mirrored, multiply by `Quaternion.Euler(0, 180, 0)`. Which you need depends on how the quad was authored, and I can't see that here.

**Tradeoffs:**
- **Screen-aligned (above):** all bars are parallel to the screen and stay upright on screen at any pitch. That's what health bars usually want. They no longer look "3D".
- **Y-axis only (cylindrical):** the bars stay upright in the world but go edge-on in a top-down view. That's wrong for this camera.
- **Screen-space UI**, like the name label, is another option, but it's a bigger change.

**Confirm:**
- Sweep the camera pitch from 0 to 90 degrees, and roll it if the game allows that.
- The bars should stay rectangular and level on screen with no flip at 90 degrees.
- Check bars at the screen edges as well as the center.

## 4. One side of scaled crates renders dark

**Cause:** the crate has non-uniform scale (1, 1, 3), and its normals are transformed with the model matrix. That's wrong under non-uniform scale. Normals need the inverse-transpose of the model matrix's upper 3x3, followed by `normalize`. Without that, the normals end up with the wrong direction and length, and the faces get the wrong N·L.

**Smallest fix:** in the crate's shader:
```hlsl
float3 n = UnityObjectToWorldNormal(v.normal);          // Unity: uses inverse-transpose
// or, generically: normalize(mul(v.normal, (float3x3)unity_WorldToObject));
```
Outside Unity, compute `transpose(inverse(mat3(model)))` once per object on the CPU and pass it as a uniform. Don't invert per vertex, which is especially costly on mobile. Normalize in the fragment shader too.

**Tradeoffs:**
- The fix costs one extra matrix uniform per draw, which is negligible.
- The alternative is to bake the scale into a 1x1x3 mesh so the scale stays uniform. That's zero shader work, but it adds another asset and doesn't help other non-uniformly scaled props.
- Check for a missing `normalize` as well. A missing normalize alone makes some faces too bright or too dark relative to each other.

**One caveat:** for a plain box with flat, axis-aligned face normals and only this diagonal scale, a model-matrix transform followed by `normalize` happens to give the right directions. If the crate is that simple and the shader already normalizes, the dark face may have a different cause. Candidates are:
- smoothed or beveled normals,
- a normal map with tangents scaled the same wrong way,
- a scaled-and-rotated parent, which introduces shear,
- negative scale flipping the winding.

The inverse-transpose fix is still correct, but check these too.

**Confirm:**
- Place a scaled crate next to an unscaled one with the same rotation, under one directional light, and rotate the light.
- The matching faces should have matching brightness.
- For a definitive check, render the world normals as color (`n * 0.5 + 0.5`). Each face should show a flat, pure axis color.

## What I could not check here

- **No project, so nothing was run or rendered.** I don't know the engine version, render pipeline (Built-in, URP or HDRP), depth buffer format, camera near/far planes or target GPUs. All of these set the ring epsilon or bias, and I haven't verified any of the values above.
- **How selection works:** collider, root, or ring. I assumed it reads `unit.root` and colliders. That's why none of the fixes touch them.
- **Missing source:**
  - the crate shader and mesh normals, so I can't confirm the dark side comes from the normal transform alone;
  - the sprite quad's authoring orientation, which decides whether the 180-degree flip is needed;
  - the label's Canvas mode and scaling.
