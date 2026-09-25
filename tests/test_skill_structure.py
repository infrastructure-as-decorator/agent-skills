from pathlib import Path

ROOT = Path(__file__).parents[1]
SKILL = ROOT / ".agents/skills/lambda-api-decorators-development"


def test_required_structure_exists():
    for relative in [
        "SKILL.md", "agents/openai.yaml", "references/contract-schema.md",
        "references/repositories.md", "references/anti-patterns.md",
        "references/validation.md", "scripts/load_api_contract.py",
        "scripts/audit_contract.py",
    ]:
        assert (SKILL / relative).is_file(), relative


def test_skill_has_frontmatter_and_no_snapshot_contracts():
    text = (SKILL / "SKILL.md").read_text()
    assert text.startswith("---\n") and "name:" in text and "description:" in text
    assert not list(SKILL.rglob("api-contract.json"))
    assert not (ROOT / "CHANGELOG.md").exists()
