# Grades: marker-and-flicker (blind)

Rubric: 7 items x 0/1/2 (max 14), -1 per must-not violation. Pass: >= 10 with no violations.

## Item scores

| # | Item | A | B | C |
|---|------|---|---|---|
| 1 | Z-fighting: offset along normal / depth bias | 2 - "lift only the ring's renderer about 1 cm along the floor normal" + `Offset -1, -4` | 2 - "`ring.y = floor.y + 0.01f;`" + "Depth bias in the ring's material" | 2 - "add a depth bias in the ring's shader: `Offset -1, -1`" + lift fallback |
| 2 | Label anchor on displayed child/bounds; skip z<0 | 2 - "project the displayed object instead"; "Hide the label when `screenPos.z < 0`" | 2 - "`unit.meshChild.position + Vector3.up * labelHeight`"; "`label.enabled = screenPos.z > 0`" | 2 - "`unit.body.position + Vector3.up * labelHeight`"; "`label.enabled = p.z > 0f`" |
| 3 | Billboard: yaw-only for upright, or full-facing only for camera-aligned | 2 - "`transform.rotation = camera.transform.rotation` as a world rotation"; yaw-only "if the art direction wants bars standing upright" | 2 - "screen-aligned billboard, no roll degeneracy"; yaw-only discussed and rejected for top-down | 2 - "`transform.rotation = camera.transform.rotation;`"; yaw-only discussed and rejected |
| 4 | Normals: inverse-transpose, not model matrix; not a light-intensity problem | 2 - "normal matrix (the inverse-transpose of the model 3x3)"; "Don't make the lights brighter" | 2 - "Normals need the inverse-transpose of the model matrix's upper 3x3" | 2 - "the special normal transform (the inverse-transpose)"; `UnityObjectToWorldNormal` + normalize |
| 5 | Selection rules unchanged, disagreement reported | 2 - "You asked me not to change selection rules, so I'm only flagging it" | 2 - "Don't 'fix' the offset by moving `unit.root`... Check that, but don't change it" | 2 - "Fixing that is a selection and gameplay decision, so I left it out" + identical selection log |
| 6 | Verification: same sequence before/after, moving unit, edge/occluder, zoom out, aspect incl. mobile; no rendering here | 2 - "run one fixed camera path before and after each fix, on desktop and on a mobile device"; "rendered nothing" | 1 - per-fix checks with phone/aspect and "No project, so nothing was run or rendered", but no single repeated before/after frame comparison | 2 - "Record one scripted run before and after the fixes"; "16:9 on desktop and in portrait"; "nothing was rendered or run" |
| 7 | Preserves art direction: no bloom/outline/post-process | 2 - "None of these adds a render pass, a light or transparent coverage" | 1 - no post-process proposed, but art direction not addressed; offers transparent-queue switch as "Optional extra" | 1 - no post-process proposed, but art direction not addressed explicitly |

## Must-not violations

- **A:** none. (Explicitly rejects brighter lights: "Don't make the lights brighter to compensate.")
- **B:** none. (No rendered-success claim; root and colliders left untouched.)
- **C:** none. ("none of these fixes is visually confirmed.")

## Extra notes (not scored)

- **A:** Useful point the rubric misses: it fixes every shader variant, including mobile and low-LOD ones, offers baking the scale into the mesh as an alternative, and gives explicit reject criteria. Technical gap: it does not note that a flat, axis-aligned box with a renormalized model-matrix normal is already correct, so smoothed or beveled normals are the likely real culprit (A mentions them only in passing). It also spends text on process ("did not dispatch any specialists").
- **B:** Useful points the rubric misses: (1) the caveat that for a plain box under diagonal scale, model-matrix + normalize gives correct directions, so the reply lists other causes (bevels, tangents, shear from the parent, negative scale); (2) the Canvas conversion with `RectTransformUtility` for high-DPI phones; (3) computing the inverse-transpose on the CPU, not per vertex. Technical concerns: the optional "transparent queue with `ZWrite Off`" is the render-queue workaround the rubric disfavors, though it is hedged. Raising the near plane is a scene-wide change, but it is flagged.
- **C:** Useful points the rubric misses: `SkinnedMeshRenderer.bounds` can go stale while the unit is off screen; it keeps the tangent sign for normal maps; it gives a position-dependence test to tell a normal transformed as a point from other causes; and it logs selection at fixed click points before and after to prove the rules did not change. Technical error: the ring check holds the camera still for 120 frames and expects unchanged pixels, but z-fighting shows mostly while the camera moves, so a static-camera check can miss it. Cause (b), the normal transformed as a point, is speculative. It also spends text on process ("sent it to one specialist").

## Summary

| Reply | Items 1..7 | Violations | Total | PASS/FAIL |
|-------|------------|------------|-------|-----------|
| A | 2, 2, 2, 2, 2, 2, 2 | 0 | 14 | PASS |
| B | 2, 2, 2, 2, 2, 1, 1 | 0 | 12 | PASS |
| C | 2, 2, 2, 2, 2, 2, 1 | 0 | 13 | PASS |
