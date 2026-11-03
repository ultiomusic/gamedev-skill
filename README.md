<p align="center">
  <img src="images/hero.svg" width="880" alt="/gamedev: a skill for Claude Code and Codex that builds, tunes and fixes games">
</p>

<p align="center">
  <a href="https://github.com/ultiomusic/gamedev-skill/actions/workflows/validate.yml"><img src="https://github.com/ultiomusic/gamedev-skill/actions/workflows/validate.yml/badge.svg" alt="validate"></a>
</p>

For game developers using Claude Code or Codex: describe what feels wrong in your game, like a floaty jump or a stutter, and it finds the cause and fixes it in your own code.

<!-- DEMO GIF (5-10 s): record `/gamedev the jump feels floaty` from the request to the fixed jump, save it as images/demo.gif, and swap this comment for that image. -->

```bash
git clone https://github.com/ultiomusic/gamedev-skill.git ~/.claude/skills/gamedev
```

For Codex, clone into `~/.agents/skills/gamedev` instead. To install for one project only, clone into `.claude/skills/gamedev` or `.agents/skills/gamedev` inside it. Restart the session afterwards.

## Use

<p align="center">
  <img src="images/flow.svg" width="880" alt="How it works: you ask, it sets what must feel right, takes a direct fix for one concept or runs specialists for mixed work, changes your code, and reports what was verified">
</p>

Ask in plain words, or call it directly (`$gamedev` in Codex):

```text
/gamedev add coyote time and a jump buffer, keep the jump height
/gamedev the decal on the floor flickers
/gamedev shooting stutters every few seconds
/gamedev audit this game without editing files
```

## What it knows

<p align="center">
  <img src="images/game-feel.svg" width="880" alt="Game feel: the same late jump press is ignored without coyote time and accepted with a 0.12 second window">
  <img src="images/rendering.svg" width="880" alt="3D and rendering: a decal on the same plane as the floor flickers, a lifted decal stays stable">
  <img src="images/systems.svg" width="880" alt="Systems: a new bullet per shot stalls on garbage collection, a pool of 14 keeps firing smoothly">
  <img src="images/performance.svg" width="880" alt="Performance: frames against the 16.7 ms budget, one render spike crosses it and stutters">
</p>

Engine notes for Unity, Godot, Unreal, Bevy and the web load only when your project uses that engine.

## Contributing

New concepts, engine notes and bug reports are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md). Released under the [MIT License](LICENSE).
