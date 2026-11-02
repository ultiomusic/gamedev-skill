# gamedev

A shared skill for Claude Code and Codex to design, implement, and improve game mechanics and game feel.
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

[Gameplay exercises](skills/gamedev/references/gameplay.md) turn these decisions into small
experiments covering loops, movement, action timing, cameras, economies, encounters, and
stability under load. Read the [Unity notes](skills/gamedev/references/unity.md) only for Unity work.
The skill is self-contained and works offline. Other engines use the project's existing tools.

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
/gamedev Construction feels unsatisfying; inspect payment, placement, feedback, and the next choice, then implement one small improvement.
$gamedev Complete this prototype's first playable loop with an action, a meaningful result, and a way to try again.
/gamedev Choices in my city builder feel too similar; propose one design experiment using existing systems without changing files.
```

## Evaluation

The [evaluation record](tests/README.md) distinguishes execution from design assessment.
Earlier WalkingCity tests exposed three behavioral bugs; no permanent game source changes
or game repository commits were made. Claude Code runtime execution has not been tested
in this environment; compatibility is based on the shared file format and portable instructions.
