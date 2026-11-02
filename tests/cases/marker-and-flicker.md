# Case: flickering ring and offset label (3D, desktop and mobile)

User request: "The selection ring flickers on the floor, the name label floats beside the character
instead of over it, and the health sprites tilt weirdly when the camera looks down. Also one side of
scaled crates renders dark. Fix the visuals without changing selection rules."

No project is on disk; these fragments are the only evidence.

```text
SelectionRing: flat quad placed at y = floor.y exactly, default opaque material
NameLabel:     screenPos = Camera.WorldToScreenPoint(unit.root.position)
               // unit.root stays at the spawn point; the animated mesh is a child offset by (1.5, 0, 0)
               // label is drawn even when screenPos.z < 0
HealthSprite:  transform.LookAt(camera.position)  // full 3-axis
Crate:         scale (1, 1, 3); lighting uses the model matrix to transform normals
```

Return the smallest corrections, the tradeoffs, and how you would confirm them in rendered output.
State what you could not check here.
