# Evaluation record — 2026-11-02

The revised skill is evaluated by the decisions it produces for a game, not by concept coverage. These checks distinguish design reasoning, code evidence, engine execution and subjective play.

## Current package and host

- Skill Creator `quick_validate.py` passed in Python UTF-8 mode (`python -X utf8`); the system-default Windows decoder cannot read some typographic punctuation.
- Actual `codex-cli 0.166.0-alpha.5.1` app-server `skills/list` discovered the revised package in a fresh isolated `.agents/skills/gamedev` directory: one result, `scope=repo`, `enabled=true`.
- Both hosts use the same `name`/`description` frontmatter and local Markdown references; the installed package requires no website access, provider-specific substitutions, scripts or connectors.
- Claude Code runtime execution remains untested because its CLI is unavailable; compatibility is based on its documented skill format, not an executed Claude session.

## Independent transfer checks

A fresh evaluator received the skill and the following requests, without intended answers or prior findings. It did not access a game project or execute a game. These are actual reasoning outcomes, not proof that the proposed mechanics feel better.

| Request | Decision produced | Discriminating check |
| --- | --- | --- |
| Complete a small Godot delivery prototype with movement and pickup already present. | One package, destination, validated delivery, visible result and repeat; no new currency, upgrades or mission system. | Normal controls complete two loops; remote, empty-handed and repeated interactions cannot lose or double-deliver the package. |
| Keep a heavy sword's 0.25-second hit and 0.8-second readiness while investigating recovery presses. | Preserve commitment timing; compare explicit rejection with a bounded accepted queue near readiness, treating the window as a hypothesis. | One command consumed at readiness; interrupted/rejected presses never fire later; unwanted follow-up attacks reject the buffering experiment. |
| Assess feel in a game whose navigation depends on sound. | Retain navigation-bearing audio; reduce only optional decoration if such a layer exists. | Compare the same route and cue interpretation while accounting for learning; do not remove the mechanic to test its feel. |

An independent editorial review found an assumption that repetition always needs strategic variety. The revised loop exercise now explicitly supports mastery, controllability, attributable mistakes and expression as well as consequential choices.

## WalkingCity: revision-specific design evaluation

The revised skill was independently applied to the actual project in read-only mode, asking for one experiment about unsatisfying construction/upgrade decisions using existing systems. The evaluator was not given previous bug findings. It verified the active scene/config and normal input paths before choosing a design hypothesis.

It found an existing tradeoff worth making legible: a new greenhouse costs 25 scrap and a tile, providing food for 14 crew; upgrading the existing greenhouse costs 30 scrap, takes no additional tile, and provides food for 12. With the same 12-bed limit, both initially support growth from 7 to 12, but the next housing purchase has a different consequence. These are source-derived values, not observed player outcomes.

Evidence, relative to `Assets/WalkingCity/`: `Generated/WalkingCityConfig.asset:189` and `:239` hold the active costs/multipliers; `Scripts/Core/CityEconomy.cs:48`, `:92` and `:365` calculate food capacity, upgrade cost and growth. `Scripts/UI/Hud.cs:507` presents build name/price; `:741` and `:794` already preview individual building output. The evaluator correctly avoided claiming there was no preview at all.

Its single proposed experiment preserves prices, rules and pacing while comparing the existing UI with an external paper card showing city-level consequences. It asks players to predict the population limit and their next decision before explaining the rule. Separate fresh groups avoid teaching A's participants the answer before B. Failure to improve understanding rejects the information hypothesis; extra clicks or different selections alone are not success.

The experiment was **designed, not conducted**; the hypothesis that information is causing dissatisfaction remains unproven. No game or Unity process was launched for this revision. This evaluation prompted the explicit learning/order-effect caveat in the skill, not a new UI requirement for every game.

## Earlier Unity execution, preserved as historical evidence

The first edition (`dbc88ef`) was tested against WalkingCity source HEAD `fa8bbf33d49d8a3e85c77ec8239328173d91bcfa`, Unity `6000.3.26f1`, with the real serialized config. The [original full record](https://github.com/ultiomusic/gamedev-skill/blob/dbc88ef42dc759092ff5f08915dab55a7110e6f4/tests/README.md) and its commit history preserve that evidence; those engine runs were not repeated for this instruction-only rewrite.

| Historical run | Total | Passed | Failed | Skipped |
| --- | ---: | ---: | ---: | ---: |
| Existing EditMode baseline | 98 | 95 | 2 | 1 |
| Baseline plus six temporary behavioral probes | 104 | 98 | 5 | 1 |
| Existing geometry failures after probe removal | 2 | 0 | 2 | 0 |

Three additional failures reproduced a misplaced merchant marker, interrupted building placement and a zero-payout pickup being discarded; three isolated correction prototypes passed. The original two failures involved coplanar geometry. No correction was integrated into game source, and the temporary fixture and metadata were removed. Those findings inform the skill's ownership, interruption and delayed-settlement rules, but do not establish the revised design exercises' effectiveness.

No rendered playtest, phone profiling, or Claude runtime session was performed. Read-only design analysis and synthetic experiments must not be represented as completed in-game improvements. WalkingCity source and HEAD remain unchanged, with its original untracked files preserved; no game commit was made.
