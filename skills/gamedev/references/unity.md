# Unity integration

Read this only for Unity projects; verify APIs against the installed editor version.

- Establish truth from `ProjectSettings/ProjectVersion.txt`, package manifest/lock, Graphics/Quality settings, build profiles/scenes and serialized assets. A README or template claiming URP does not prove a render-pipeline asset is assigned.
- Trace the instantiated scene/prefab and its overrides before changing a C# initializer. Inspect runtime-created objects too; keep `.meta` GUIDs and serialized field compatibility stable.
- Use the installed input system and its configured update mode. Capture edges/callbacks once, hand them to the simulation without losing or duplicating them between fixed ticks, and account for touch pointer IDs and EventSystem/UI capture.
- `Transform` displacement and `CharacterController.Move` take a displacement; Rigidbody velocity APIs take a velocity. Let the active physics body own movement and use its native fixed-step/interpolation/CCD support instead of fighting it with Transform writes. Verify expected speed/distance and vary the physics step when testing integration: render-FPS changes alone can miss an extra dt multiplier inside `FixedUpdate`.
- Follow the final simulated/interpolated target at the appropriate camera phase, normally `LateUpdate` or the existing camera system. Compose shake separately; don't create a second camera writer or assume Cinemachine is installed.
- Keep scaled gameplay time distinct from `unscaledDeltaTime`/real-time waits. A hit-stop timer cannot depend on the clock it stops; local effects should not overwrite a shared `Time.timeScale` owner or restore it blindly to 1.
- Balance subscriptions and coroutine/tween cancellation with `OnEnable`/`OnDisable` and pool reuse. Check play-mode reload settings before relying on static initialization. Restore original presentation values on interruption.
- Prefer existing ParticleSystem pools, LODGroup, renderer culling, SpriteAtlas and navigation facilities when present. Inspect render-pipeline batching support and material instances before proposing rendering changes.
- Use Profiler/Frame Debugger and a representative player build for performance conclusions. Editor/batchmode timing, source inspection and an old executable cannot establish current mobile GPU performance or subjective feel.

## Minimal execution evidence

Use the version in the project, inspect existing test assemblies/harnesses first, and write results outside the game source tree when possible. Do not start a second Editor on the same project or kill an unrelated Editor.

```text
<matching Unity executable> -batchmode -nographics -projectPath <project> -runTests -testPlatform EditMode -testResults <absolute-results.xml> -logFile <absolute-editor.log>
```

Do not add `-quit` to a Test Framework run: the runner owns completion. Check XML counts/results and the fresh log, not merely process exit. Select PlayMode tests for lifecycle/input/simulation behavior when available; a project may legitimately have no such suite. Graphics and interaction checks need a rendering-capable run. A tiny temporary regression fixture is preferable to introducing a test framework the project already has.

For a skill evaluation, keep the game diff separate from the skill repo, record baseline HEAD/status, and remove your temporary fixture and its generated `.meta` only after execution. Preserve existing untracked files, user edits, saves and settings. Commit game changes only when the user actually requested that.
