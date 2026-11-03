# Changelog

All notable changes to this skill are listed here. Versions follow the git tags.

## Unreleased

- Add an MIT license, a contributing guide, issue templates and this changelog.
- Restore `tests/validate.py` for the flat layout and run it in CI.

## 1.0.0 - 2026-11-02

First release of **gamedev**, a skill for Claude Code and Codex that builds, tunes and fixes games.

- Four specialists: game feel, 3D & rendering, systems and performance. A request about a single concept skips delegation and takes a direct path.
- 39 concepts with starting values and the first trap to check, from coyote time and jump arcs to z-fighting, save data and frame budgets.
- Engine notes for Unity, Godot, Unreal and the web, read only for the engine your project uses.
- Changes are checked at the relevant frame rates or on a representative build, and the report says what could not be verified.
