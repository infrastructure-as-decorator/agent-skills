import re
from pathlib import Path

ROOT = Path(__file__).parents[1]
SKILLS = ROOT / "skills"
NAMES = {"build-with-lambda-api-decorators", "maintain-lambda-api-decorators"}


def frontmatter(skill):
    text = (skill / "SKILL.md").read_text()
    match = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    assert match
    return dict(re.findall(r"^(name|description): (.+)$", match.group(1), re.MULTILINE))


def test_exactly_two_public_skills_match_frontmatter():
    actual = {path.name for path in SKILLS.iterdir() if path.is_dir()}
    assert actual == NAMES
    assert not (ROOT / ".agents/skills").exists()
    assert not (ROOT / ".claude/skills").exists()
    assert not (ROOT / ".github/skills").exists()
    for name in NAMES:
        metadata = frontmatter(SKILLS / name)
        assert metadata["name"] == name
        assert metadata["description"]


def test_skills_have_distinct_responsibilities_and_no_static_contracts():
    consumer = frontmatter(SKILLS / "build-with-lambda-api-decorators")
    maintainer = frontmatter(SKILLS / "maintain-lambda-api-decorators")
    assert consumer["description"] != maintainer["description"]
    for name in NAMES:
        skill = SKILLS / name
        assert (skill / "agents/openai.yaml").is_file()
        assert not list(skill.rglob("api-contract.json"))
        assert not list(skill.rglob("CHANGELOG*"))
    assert not (SKILLS / "lambda-api-decorators-development").exists()


def test_reference_links_resolve():
    for skill in (SKILLS / name for name in NAMES):
        text = (skill / "SKILL.md").read_text()
        for reference in re.findall(r"\]\((references/[^)]+)\)", text):
            assert (skill / reference).is_file(), reference


def test_consumer_isolated_from_maintainer_workflows():
    text = (SKILLS / "build-with-lambda-api-decorators/SKILL.md").read_text()
    assert "Git history" in text
    assert "release workflows" in text
    assert "Docusaurus" in text
    assert "current_user(event)" in text
    assert "CurrentUserError" in text
    assert "claims" in (SKILLS / "build-with-lambda-api-decorators/references/authentication-and-user.md").read_text()


def test_openai_metadata_is_versionless_and_discriminating():
    for name in NAMES:
        text = (SKILLS / name / "agents/openai.yaml").read_text()
        assert 'display_name: "' in text
        assert 'short_description: "' in text
        assert f'default_prompt: "Use ${name}' in text
        assert "version" not in text.lower()
