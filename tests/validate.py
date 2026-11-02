"""Static checks for the gamedev skill. Run: python tests/validate.py

Checks frontmatter, local links, size limits, and that each specialist brief
covers its concepts. Exit code 1 on any failure. Standard library only.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL_DIR = ROOT / "skills" / "gamedev"
SKILL = SKILL_DIR / "SKILL.md"
REFS = SKILL_DIR / "references"
MAX_BYTES = {"SKILL.md": 10_000, "reference": 10_000}

# concept -> (owning reference, regex that must match in that file)
CONCEPTS = {
    "game-feel.md": {
        "delta time": r"delta time",
        "coyote time": r"coyote",
        "easing": r"easing",
        "screen shake": r"screen shake|shake",
        "squash and stretch": r"squash",
        "camera deadzone": r"deadzone|dead zone",
        "input buffering": r"input buffer|buffer",
        "acceleration and friction": r"accelerat",
        "hit stop": r"hit[- ]stop",
        "invincibility frames": r"invincib|i-frame",
    },
    "3d-rendering.md": {
        "raycasting": r"raycast",
        "normals": r"normal",
        "level of detail": r"level of detail|\bLOD",
        "frustum culling": r"frustum",
        "fragment shader": r"fragment shader",
        "billboarding": r"billboard",
        "quaternions": r"quaternion",
        "z-fighting": r"z-fight",
    },
    "systems.md": {
        "object pooling": r"pool",
        "state machine": r"state machine",
        "hitbox and hurtbox": r"hitbox",
        "pathfinding": r"pathfind|A\*",
        "particle system": r"particle",
        "fixed timestep": r"fixed timestep|fixed[- ]step",
        "steering behaviors": r"steering",
        "tunneling": r"tunnel",
        "seeded noise": r"seed",
    },
    "performance.md": {
        "frame budget": r"frame budget|16\.67",
        "draw calls": r"draw call",
        "spatial partitioning": r"spatial partition|uniform grid",
        "overdraw": r"overdraw",
        "time slicing": r"time[- ]slic",
        "texture atlas": r"atlas",
        "chunk streaming": r"chunk",
    },
}

failures = []


def fail(msg):
    failures.append(msg)


def read(path):
    return path.read_text(encoding="utf-8")


def check_frontmatter():
    text = read(SKILL)
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return fail("SKILL.md: missing YAML frontmatter")
    fm = dict(re.findall(r"^(\w+):\s*(.*)$", m.group(1), re.M))
    if fm.get("name") != SKILL_DIR.name:
        fail(f"SKILL.md: name '{fm.get('name')}' != folder '{SKILL_DIR.name}'")
    desc = fm.get("description", "")
    if not desc:
        fail("SKILL.md: empty description")
    if len(desc) > 1024:
        fail(f"SKILL.md: description {len(desc)} chars > 1024")


def check_links():
    for md in [SKILL, ROOT / "README.md", *REFS.glob("*.md")]:
        for target in re.findall(r"\]\(([^)]+)\)", read(md)):
            if re.match(r"^[a-z]+://|^#|^mailto:", target):
                continue
            target = target.split("#")[0]
            if not (md.parent / target).exists():
                fail(f"{md.relative_to(ROOT)}: broken link {target}")


def check_sizes():
    n = SKILL.stat().st_size
    if n > MAX_BYTES["SKILL.md"]:
        fail(f"SKILL.md: {n} bytes > {MAX_BYTES['SKILL.md']}")
    for ref in REFS.glob("*.md"):
        n = ref.stat().st_size
        if n > MAX_BYTES["reference"]:
            fail(f"{ref.name}: {n} bytes > {MAX_BYTES['reference']}")


def check_concepts():
    skill_text = read(SKILL)
    for ref_name, concepts in CONCEPTS.items():
        ref = REFS / ref_name
        if not ref.exists():
            fail(f"missing reference {ref_name}")
            continue
        text = read(ref)
        if "## Starting values and traps" not in text:
            fail(f"{ref_name}: missing '## Starting values and traps' section")
        if f"references/{ref_name}" not in skill_text:
            fail(f"SKILL.md: does not link references/{ref_name}")
        for concept, pattern in concepts.items():
            if not re.search(pattern, text, re.I):
                fail(f"{ref_name}: concept '{concept}' not covered")
    for case in (ROOT / "tests" / "cases").glob("*.md"):
        if case.name.endswith(".rubric.md"):
            continue
        if not case.with_name(case.stem + ".rubric.md").exists():
            fail(f"tests/cases/{case.name}: missing rubric")


if __name__ == "__main__":
    for check in (check_frontmatter, check_links, check_sizes, check_concepts):
        check()
    total = len(CONCEPTS) and sum(len(c) for c in CONCEPTS.values())
    if failures:
        print("\n".join("FAIL " + f for f in failures))
        sys.exit(1)
    print(f"OK: frontmatter, links, sizes, {total} concepts, case rubrics")
