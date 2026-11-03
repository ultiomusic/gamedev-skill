# Contributing

Thanks for helping make games feel better. Issues get a first reply within 24 hours.

## Report a wrong or weak fix

Open a [skill gave a wrong fix](https://github.com/ultiomusic/gamedev-skill/issues/new?template=wrong-fix.yml) issue with the engine and version, the exact request, what the skill changed, and what the game did afterwards. A short clip helps more than a long description.

## Add or improve a concept

1. Pick the owning brief: [game-feel.md](game-feel.md), [3d-rendering.md](3d-rendering.md), [systems.md](systems.md) or [performance.md](performance.md).
2. Add one row to its `Starting values and traps` table: a starting value to test, the first trap to check, and how to confirm the fix.
3. Add the concept's name to that specialist's row in the table in [SKILL.md](SKILL.md).

Engine-specific details go in that engine's section of [engines.md](engines.md), not in a brief.

## Style

- Write instructions for the agent, not explanations for a reader. Short, imperative, no filler.
- Starting values are hypotheses to test in the user's project, not facts.
- Keep `SKILL.md`, `engines.md` and each brief under 10 KB; the agent loads them whole.

## Check before opening a pull request

```bash
python tests/validate.py
```

It checks frontmatter, local links, file sizes, and that every concept listed in `SKILL.md` appears in its brief. CI runs the same check on every pull request.
