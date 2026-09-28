import re
from pathlib import Path

ROOT = Path(__file__).parents[1]
SKILLS = ROOT / ".agents/skills"
CONSUMER = SKILLS / "build-with-lambda-api-decorators"
MAINTAINER = SKILLS / "maintain-lambda-api-decorators"


def frontmatter(skill):
    text = (skill / "SKILL.md").read_text()
    match = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    assert match
    return dict(re.findall(r"^(name|description): (.+)$", match.group(1), re.MULTILINE))


def test_both_skills_have_portable_structure_and_distinct_metadata():
    assert not (SKILLS / "lambda-api-decorators-development").exists()
    consumer = frontmatter(CONSUMER)
    maintainer = frontmatter(MAINTAINER)
    assert consumer["name"] == "build-with-lambda-api-decorators"
    assert maintainer["name"] == "maintain-lambda-api-decorators"
    assert consumer["description"] != maintainer["description"]
    assert set(consumer) == {"name", "description"}
    assert set(maintainer) == {"name", "description"}


def test_required_resources_and_no_static_contracts():
    for skill in (CONSUMER, MAINTAINER):
        assert (skill / "SKILL.md").is_file()
        assert (skill / "agents/openai.yaml").is_file()
        assert not list(skill.rglob("api-contract.json"))
    assert (CONSUMER / "references/authentication-and-user.md").is_file()
    assert (MAINTAINER / "scripts/load_api_contract.py").is_file()
    assert (MAINTAINER / "scripts/audit_contract.py").is_file()
    assert not (ROOT / "CHANGELOG.md").exists()


def test_reference_links_resolve():
    for skill in (CONSUMER, MAINTAINER):
        text = (skill / "SKILL.md").read_text()
        for reference in re.findall(r"\]\((references/[^)]+)\)", text):
            assert (skill / reference).is_file(), reference


def test_consumer_isolated_from_maintainer_workflows():
    text = (CONSUMER / "SKILL.md").read_text()
    assert "checkout" in text
    assert "Git history" in text
    assert "release workflows" in text
    assert "Docusaurus" in text
    assert "audit" in text
    assert "current_user(event)" in text
    assert "CurrentUserError" in text
    assert "claims" in (CONSUMER / "references/authentication-and-user.md").read_text()


def test_forward_scenarios_route_to_the_right_skill():
    consumer = (CONSUMER / "SKILL.md").read_text()
    maintainer = (MAINTAINER / "SKILL.md").read_text()
    assert "published Python packages" in consumer
    assert "official ecosystem repositories" in maintainer
    assert "Examples must use published PyPI versions" in maintainer
    assert "source and tests are authoritative" in maintainer
