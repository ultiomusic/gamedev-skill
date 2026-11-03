# Engine notes

Read only the section for the project's engine and verify every API against the installed version. These notes say where the truth lives and what the common traps look like in each engine; the specialist briefs hold the general rules.

## Unity

- Establish truth from `ProjectSettings/ProjectVersion.txt`, package manifest/lock, Graphics/Quality settings, build profiles/scenes and serialized assets. A README or template claiming URP does not prove a render-pipeline asset is assigned.
- Trace the instantiated scene/prefab and its overrides before changing a C# initializer. Inspect runtime-created objects too; keep `.meta` GUIDs and serialized field compatibility stable.
- Use the installed input system and its configured update mode. Capture edges/callbacks once, hand them to the simulation without losing or duplicating them between fixed ticks, and account for touch pointer IDs and EventSystem/UI capture.
- `Transform` displacement and `CharacterController.Move` take a displacement; Rigidbody velocity APIs take a velocity (Unity 6 renames `Rigidbody.velocity` to `linearVelocity`). Let the active physics body own movement and use its native fixed-step/interpolation/CCD support instead of fighting it with Transform writes. Verify expected speed/distance and vary the physics step when testing integration: render-FPS changes alone can miss an extra dt multiplier inside `FixedUpdate`.
- Follow the final simulated/interpolated target at the appropriate camera phase, normally `LateUpdate` or the existing camera system. Compose shake separately; don't create a second camera writer or assume Cinemachine is installed.
- Keep scaled gameplay time distinct from `unscaledDeltaTime`/real-time waits. A hit-stop timer cannot depend on the clock it stops; local effects should not overwrite a shared `Time.timeScale` owner or restore it blindly to 1.
- Balance subscriptions and coroutine/tween cancellation with `OnEnable`/`OnDisable` and pool reuse. Check play-mode reload settings before relying on static initialization. Restore original presentation values on interruption.
- Prefer existing ParticleSystem pools, LODGroup, renderer culling, SpriteAtlas and navigation facilities when present. Inspect render-pipeline batching support and material instances before proposing rendering changes.
- On Android and iOS the default frame rate is usually 30 until `Application.targetFrameRate` is set, and mobile ignores `QualitySettings.vSyncCount`. A target that does not divide the display refresh rate runs at a lower divisor (60 on a 90 Hz screen gives 45). Check both before treating 30 fps as a performance problem.
- Use Profiler/Frame Debugger and a representative player build for performance conclusions. Editor/batchmode timing, source inspection and an old executable cannot establish current mobile GPU performance or subjective feel.

Run tests with the project's own Unity version after inspecting its test assemblies, writing results outside the game source tree. Do not start a second Editor on the same project or kill an unrelated Editor.

```text
<matching Unity executable> -batchmode -nographics -projectPath <project> -runTests -testPlatform EditMode -testResults <absolute-results.xml> -logFile <absolute-editor.log>
```

Do not add `-quit` to a Test Framework run: the runner owns completion. Check XML counts/results and the fresh log, not merely process exit. Select PlayMode tests for lifecycle/input/simulation behavior when available; a project may legitimately have no such suite. Graphics and interaction checks need a rendering-capable run. A tiny temporary regression fixture is preferable to introducing a test framework the project does not have; remove it and its generated `.meta` afterwards. Preserve existing untracked files, user edits, saves and settings.

## Godot

- Truth lives in `project.godot` (version features, main scene, autoloads, physics tick rate, input map), `export_presets.cfg`, and the `.tscn` scenes with their overrides. Godot 3 and 4 APIs differ: read `config_version` (4 is Godot 3, 5 is Godot 4) and the version in `config/features` before writing code.
- `CharacterBody2D/3D.velocity` is a velocity: `move_and_slide()` applies the physics delta itself, so multiplying the velocity by `delta` first ties speed to the tick rate. Integrate your own accelerations by `delta`, then call `move_and_slide()` once per tick.
- `is_on_floor()` reports the result of the last `move_and_slide()`. Clear coyote grace on the tick that sets the jump velocity, or the stale grounded result refills it.
- Gameplay movement belongs in `_physics_process`, visuals in `_process`. Use the project's physics interpolation setting where the version has one, rather than smoothing the same motion in two places.
- `Engine.time_scale` is global. A hit stop that lowers it must end on a timer that ignores time scale (the fourth argument of `SceneTree.create_timer` in Godot 4) or on real ticks.
- Pooled or re-added nodes keep their signal connections and running tweens. Check `is_connected()` before connecting, and kill the previous tween before starting another.
- Profile an exported debug build attached to the editor (Profiler, Monitors, Visual Profiler); release templates have no debugger, so time them with an in-game frame-time overlay or an external profiler. Editor runs include editor overhead. Use the project's existing test addon, such as GUT or GdUnit4, when one is installed.

## Unreal

- Truth lives in the `.uproject` (engine association, plugins), `Config/Default*.ini`, and Blueprint assets. Gameplay often sits in Blueprints that text search cannot read; say what you could not inspect instead of assuming the C++ is the whole game.
- Let `UCharacterMovementComponent` own character movement and tune its properties (max walk speed, acceleration, braking, ground friction, air control, jump velocity, gravity scale) before writing actor locations. `AddMovementInput` takes an input scale, not a time step; multiplying it by delta time slows movement at high frame rates.
- Character Movement has no coyote window or input buffer. Add them where jump eligibility is decided, and keep `JumpMaxHoldTime` for variable jump height.
- Global time dilation also slows the timer meant to end a hit stop. Prefer per-actor `CustomTimeDilation` on the fighters and end it on real time.
- Physics steps once per frame with the frame delta (capped by Max Physics Delta Time) unless substepping or async physics is on, so tunneling gets worse at low frame rates. Enable CCD on fast primitives or substepping, and test at the lowest supported frame rate.
- Read `stat unit` as overlapping threads (Game, Draw, GPU): frame time follows the slowest, not their sum. Profile a packaged Development or Test build with Unreal Insights; Play In Editor includes editor cost.

## Bevy

- Truth lives in `Cargo.toml` (Bevy version, features, profiles) and the `App::new()` chain with the plugins it adds. APIs change every minor release (`delta_seconds()` became `delta_secs()` in 0.15); match the installed version.
- A system runs only if its schedule, `run_if` conditions and current state allow it. Check those before trusting code that looks live.
- In `FixedUpdate`, `Res<Time>` is the fixed clock (64 Hz by default), which ticks zero or several times per frame: `just_pressed` read there is lost or doubled. Latch presses in a resource outside the fixed schedule and clear them when consumed. Transforms moved there are not interpolated by default.
- Profile `--release` builds; debug builds are many times slower unless `[profile.dev.package."*"]` sets `opt-level = 3`.

## Web (Canvas, Three.js, Phaser, PixiJS)

- Truth lives in `package.json` and its lockfile (engine version), the bundler config, and the HTML entry that actually loads. Check the production build, not only the dev server.
- Convert time once to seconds: Phaser's `update(time, delta)` gives milliseconds, PixiJS `ticker.deltaTime` is a frame factor near 1 at 60 fps (`deltaMS` is milliseconds), and Three.js `Timer.getDelta()` (which replaces the deprecated `Clock`) gives seconds.
- `requestAnimationFrame` pauses in background tabs, so the first frame back can carry seconds of delta. Clamp it and pause the game on `visibilitychange`.
- Ignore key auto-repeat (`event.repeat`) when reading press edges, and set `touch-action: none` on the game canvas so touches do not scroll or zoom the page.
- Phones commonly report a `devicePixelRatio` of 2 to 3 and some up to 4, up to sixteen times the pixels. Cap the render resolution, for example at `Math.min(devicePixelRatio, 2)`, before optimizing shaders.
- Allocating vectors or arrays inside the frame loop feeds the garbage collector; reuse scratch objects. Read draw calls from the renderer, such as `renderer.info` in Three.js (set `info.autoReset = false` when post-processing renders several passes).
- An `AudioContext` created before user activation stays suspended. Call `resume()` from a `click`, `keydown`, `pointerup` or `touchend` handler; `touchstart`, mouse moves and gamepad buttons do not count.
- Profile in the browser's Performance panel on a real phone. CPU throttling only approximates a slower CPU and leaves the desktop GPU untouched, so desktop numbers, throttled or not, do not predict mobile.
