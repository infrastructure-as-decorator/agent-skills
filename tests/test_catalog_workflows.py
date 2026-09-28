from pathlib import Path

ROOT = Path(__file__).parents[1]


def test_ci_validates_catalog_and_dry_runs_publish():
    text = (ROOT / ".github/workflows/ci.yml").read_text()
    assert "python -m pytest -q" in text
    assert "python -m compileall -q skills tests" in text
    assert "gh skill publish --dry-run" in text
    assert "2.90.0" in text
    assert "git diff --check" in text


def test_readme_documents_individual_github_installation():
    text = (ROOT / "README.md").read_text()
    for name in ("build-with-lambda-api-decorators", "maintain-lambda-api-decorators"):
        assert f"gh skill preview infrastructure-as-decorator/agent-skills" in text
        assert f"gh skill install infrastructure-as-decorator/agent-skills" in text
        assert name in text
    assert "@v1.0.0" in text
    assert "gh skill update" in text
    assert "public preview" in text
    assert ".agents/skills" not in text
    assert "No es necesario instalar ambos" in text


def test_publish_is_tag_only_and_safe_to_rerun():
    text = (ROOT / ".github/workflows/publish.yml").read_text()
    assert 'tags:' in text and '"v*.*.*"' in text
    assert "^v[0-9]+\\.[0-9]+\\.[0-9]+$" in text
    assert "git merge-base --is-ancestor" in text
    assert "gh skill publish --dry-run" in text
    assert 'gh skill publish --tag "$GITHUB_REF_NAME"' in text
    assert "gh release view" in text
    assert "gh release create" not in text
    assert "git commit" not in text
    assert "git push" not in text
    assert "GH_TOKEN: ${{ github.token }}" in text
