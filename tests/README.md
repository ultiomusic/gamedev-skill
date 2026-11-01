# Validation record — 2026-11-02

This tests the skill's decisions and portability, not a claim that WalkingCity is bug-free or that subjective feel improved. The game was an evaluation target, not a deliverable to modify.

## Package and host checks

- Skill Creator `quick_validate.py`: passed frontmatter/name/scaffold validation.
- All 34 primary-source concept URLs appear once; no missing/extra concepts; all local references resolve.
- Actual `codex-cli 0.166.0-alpha.5.1` app-server `skills/list`, against an isolated `.agents/skills/gamedev` installation: exactly one `gamedev`, `scope=repo`, `enabled=true`.
- Claude Code: shared `name`/`description` frontmatter, relative references and `.claude/skills/gamedev` layout checked against [official documentation](https://code.claude.com/docs/en/skills); **Claude execution was not tested because its CLI was unavailable**. There are no Codex-only tools, substitutions, or APIs in the instructions.
- Independent source review checked completeness, engineering correctness and unnecessary bulk. Continuous emission, A* heuristics and intentional off-screen dormancy were clarified from that review.

## Independent decision probes

The evaluator received the skill and requests, without expected answers; these were reasoning probes, not executed game tests.

| Request | Observed behavior |
| --- | --- |
| Review `body.linearVelocity = input * speed * Time.deltaTime` and propose a regression. | Removed extra dt conceptually, preserved movement/gravity ownership, checked units, and proposed known-distance tests with varied physics timestep as well as render FPS. |
| Investigate impact freeze/shake that survives reuse, with only the symptom supplied. | Kept causes hypothetical; traced release clock, shared camera/time ownership, stale callbacks and interruption cleanup; made no execution claim. |
| Change the copyright year in a game studio marketing website footer. | Did not activate gameplay workflow; proposed only the requested footer edit. |

These probes motivated explicit snippet-only guidance and a physics-step regression reminder.

## WalkingCity execution

Source HEAD: `fa8bbf33d49d8a3e85c77ec8239328173d91bcfa`; Unity `6000.3.26f1`; Built-in renderer; touch-first autonomous city builder. The active scene/config and installed packages took precedence over stale Godot/URP template claims.

| Run | Total | Passed | Failed | Skipped |
| --- | ---: | ---: | ---: | ---: |
| Existing EditMode suite before the forward test | 98 | 95 | 2 | 1 |
| Existing suite plus six temporary behavioral probes | 104 | 98 | 5 | 1 |
| Existing geometry failures rerun after removing probes | 2 | 0 | 2 | 0 |

The original failures were `CoplanarTests.DeckCrewHasNoCoplanarFaces` and `CoplanarTests.HavensOnTheirGroundHaveNoCoplanarFaces`: overlapping crew/haven geometry. `UiKitTests.KitSheet_Render` was skipped because its opt-in marker was absent. These are not skill-induced regressions.

An independent evaluator received only the skill, project path and a read-only audit request, then created a temporary fixture in the existing EditMode assembly. It exercised actual project methods and a cloned serialized GameConfig without booting the game or writing player saves.

| Contract failure reproduced | Evidence | Minimal correction tested as an isolated prototype |
| --- | --- | --- |
| Merchant badge follows an unmoving parent, not the rendered ship. | `Scripts/Gameplay/Merchant.cs:81`: at route z=1000, badge/ship-anchor separation was 1005.29944 units. | Derive the anchor from the ship transform; the prototype followed a further 25-unit route movement. |
| Re-tapping a building during its arrival captures an in-flight pose as the new rest position. | `Scripts/Core/GameDirector.cs:584` (`PopIn.Play`): final y=1.2 instead of 0; arrival callback count=0. | Do not interrupt an active arrival with the tap nod; the prototype restored y=0 and invoked landing once. |
| A pickup is discarded if storage fills while it travels. | `Scripts/Gameplay/PickupField.cs:349`: amount=8, stored=0, active=false, one success event. | Recheck capacity before completion and requeue the cache on zero payout; prototype retained amount and returned to non-flying state. |

Paths above are relative to `Assets/WalkingCity/`. The three desired-behavior assertions failed against current code; three correction prototypes passed. **No fixes were integrated into game source**, so prototype success is not end-to-end fix verification; partial pickup overflow still needs a design policy. These findings motivated completion-time validation for delayed actions and an explicit read-only/baseline-failure exception in the skill.

The [34-concept applicability matrix](walkingcity-coverage.md) records 27 code-evidenced mechanisms, 4 unverified candidates and 3 inapplicable techniques. Code evidence is not runtime approval; coyote time, invincibility frames and global pathfinding were not added to this game's design.

## Reproduction and limits

Baseline command, with absolute paths substituted; the Test Framework owns process completion:

```text
<Unity 6000.3.26f1 executable> -batchmode -nographics -projectPath <WalkingCity> -runTests -testPlatform EditMode -testResults <results.xml> -logFile <editor.log>
```

Inspect fresh XML test counts and the log's exit status (2 for the failing runs); process launch alone is not success. The same command ran the six temporary probes in the existing test assembly. Their C# fixture and raw XML/log evidence are preserved in the local evidence archive delivered with this work, not in the portable skill.

The temporary test and generated `.meta` were removed. Tracked source/asset hashes, HEAD and the original six untracked backup/temp entries remained unchanged; no game commit was made. Source-controlled skill changes are confined to this repository.

No rendered playtest, phone profiling, full frame-rate matrix, or Claude runtime session was performed. Existing Windows binaries predated HEAD; capture/soak harnesses can save real journal data, and their reset flag deletes it. Neither was run. Those limits do not prevent reproducing the isolated contract failures above, but they do prevent claims about visual comfort, current-build GPU performance or overall game feel.
