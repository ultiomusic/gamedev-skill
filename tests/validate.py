"""Static checks for the gamedev skill. Run: python tests/validate.py

Checks frontmatter, local links, size limits, and that each specialist brief
covers the concepts SKILL.md assigns to it. Exit code 1 on any failure.
Standard library only.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "SKILL.md"
NAME = "gamedev"
MAX_BYTES = 10_000
BRIEFS = ["game-feel.md", "3d-rendering.md", "systems.md", "performance.md"]
DOCS = [SKILL, ROOT / "README.md", ROOT / "engines.md", *(ROOT / b for b in BRIEFS)]

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
    if fm.get("name") != NAME:
        fail(f"SKILL.md: name '{fm.get('name')}' != '{NAME}'")
    desc = fm.get("description", "")
    if not desc:
        fail("SKILL.md: empty description")
    if len(desc) > 1024:
        fail(f"SKILL.md: description {len(desc)} chars > 1024")


def check_links():
    for md in DOCS:
        for target in re.findall(r"\]\(([^)]+)\)|src=\"([^\"]+)\"", read(md)):
            target = next(t for t in target if t)
            if re.match(r"^[a-z]+://|^#|^mailto:", target):
                continue
            target = target.split("#")[0]
            if not (md.parent / target).exists():
                fail(f"{md.name}: broken link {target}")


def check_sizes():
    for md in [SKILL, ROOT / "engines.md", *(ROOT / b for b in BRIEFS)]:
        n = md.stat().st_size
        if n > MAX_BYTES:
            fail(f"{md.name}: {n} bytes > {MAX_BYTES}")


def check_concepts():
    """Every concept in SKILL.md's specialist table must appear in its brief."""
    total = 0
    rows = re.findall(r"^\| \[[^\]]+\]\(([\w-]+\.md)\).*\| ([^|]+) \|$", read(SKILL), re.M)
    if {brief for brief, _ in rows} != set(BRIEFS):
        fail(f"SKILL.md: specialist table links {sorted(b for b, _ in rows)}, expected {sorted(BRIEFS)}")
    for brief, concepts in rows:
        text = read(ROOT / brief)
        if "## Starting values and traps" not in text:
            fail(f"{brief}: missing '## Starting values and traps' section")
        for concept in concepts.split(","):
            concept = concept.strip()
            total += 1
            if concept.lower() not in text.lower():
                fail(f"{brief}: concept '{concept}' not covered")
    return total


if __name__ == "__main__":
    check_frontmatter()
    check_links()
    check_sizes()
    total = check_concepts()
    if failures:
        print("\n".join("FAIL " + f for f in failures))
        sys.exit(1)
    print(f"OK: frontmatter, links, sizes, {total} concepts")
