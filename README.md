# gamedev

A shared skill for Claude Code and Codex with four specialist subagent roles for building and improving games.
Entry point: [`skills/gamedev/SKILL.md`](skills/gamedev/SKILL.md).

## How it works

Start with the player's intent and the intended experience, then find the disconnect between
input, rules, actual outcomes, feedback, and the next decision. For new mechanics, complete
a playable loop reachable through normal controls; for existing mechanics, choose the smallest
change with the greatest expected impact.

A request for heavier movement becomes an investigation of acceleration, stopping distance,
and visual weight. More satisfying construction connects payment, placement, completion,
and the next choice. When a game feels boring, examine whether its existing choices change
the next decision before adding systems.

## Four specialists

| Area | Subagent task label | Responsibility |
| --- | --- | --- |
| [3D & Rendering](skills/gamedev/references/3d-rendering.md) | `gamedev-3d-rendering` | Geometry, spaces, materials, lighting, projection, composition, and readability. |
| [Game Feel](skills/gamedev/references/game-feel.md) | `gamedev-game-feel` | Input response, movement, action rhythm, camera motion, and audiovisual feedback. |
| [Systems](skills/gamedev/references/systems.md) | `gamedev-systems` | Playable loops, authoritative rules, economy, progression, AI, and persistence. |
| [Performance](skills/gamedev/references/performance.md) | `gamedev-performance` | Frame pacing, CPU/GPU bottlenecks, allocations, memory, and streaming. |

The main skill coordinates the work. It selects relevant specialists, passes each a bounded
assignment and its role brief, waits for results, and integrates one coherent change.
Full game audits use all four; focused tasks use only the relevant roles. Independent work
runs in parallel within the host's limits. Shared files and the game Editor have one owner.

These labels name delegated tasks. The skill uses the host's available general-purpose
subagents without requiring custom agent registration, model overrides, or extra dependencies.
[Codex supports delegation through skill instructions](https://learn.chatgpt.com/docs/agent-configuration/subagents);
[Claude Code provides an Agent tool and general-purpose workers](https://code.claude.com/docs/en/sub-agents).
If delegation is unavailable, the same briefs run sequentially in the main agent, which reports that limitation.

Each brief contains a concrete experiment and an evidence-based return contract.
Read the [Unity notes](skills/gamedev/references/unity.md) only for Unity work.
The guidance is self-contained and works offline; execution uses the project's existing tools.

## Installation

Copy the **entire** `skills/gamedev` folder to the appropriate destination:

| Tool | Project destination | Invocation |
| --- | --- | --- |
| Codex | `.agents/skills/gamedev/` | `$gamedev` |
| Claude Code | `.claude/skills/gamedev/` | `/gamedev` |

For personal installation, use `~/.agents/skills/gamedev/` for Codex or
`~/.claude/skills/gamedev/` for Claude Code. The same package supports automatic discovery
and requires no API key, MCP server, or installation script. Restart the session if it does
not appear. The layout follows the documented skill formats for
[Codex](https://learn.chatgpt.com/docs/build-skills) and
[Claude Code](https://code.claude.com/docs/en/skills).

## Example requests

```text
$gamedev Make movement feel heavy but responsive; keep the existing controller and improve stopping and direction changes.
/gamedev Use all four specialists to audit this game without editing files; combine their findings by player impact and evidence.
$gamedev Use 3D & Rendering to investigate selection-marker drift; preserve the camera controller and gameplay rules.
/gamedev Use Systems and Game Feel to improve construction feedback; give shared files one owner and preserve economy rules.
$gamedev Use Performance to investigate this encounter hitch; measure the bottleneck before choosing an optimization.
```

## Evaluation

The [evaluation record](tests/README.md) distinguishes execution from design assessment.
Earlier WalkingCity tests exposed three behavioral bugs; no permanent game source changes
or game repository commits were made. Claude Code runtime execution has not been tested
in this environment; compatibility is based on the shared file format and portable instructions.
