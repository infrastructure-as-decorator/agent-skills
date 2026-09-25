import json
import subprocess
import sys
import zipfile
import importlib.util
import os
from pathlib import Path

SCRIPT = Path(__file__).parents[1] / ".agents/skills/lambda-api-decorators-development/scripts/load_api_contract.py"
FIXTURES = Path(__file__).parent / "fixtures"


def load_module():
    spec = importlib.util.spec_from_file_location("contract_loader", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run(*args):
    return subprocess.run([sys.executable, str(SCRIPT), *args], text=True, capture_output=True)


def make_wheel(path):
    wheel = path / "demo_package-2.3.4-py3-none-any.whl"
    with zipfile.ZipFile(wheel, "w") as archive:
        archive.writestr("demo_package/_agent/api-contract.json", (FIXTURES / "valid_package/_agent/api-contract.json").read_bytes())
        archive.writestr("demo_package/_agent/behavior.md", "# Behavior\n")
        archive.writestr("demo_package-2.3.4.dist-info/METADATA", "Metadata-Version: 2.1\nName: demo-package\nVersion: 2.3.4\n")
        archive.writestr("demo_package-2.3.4.dist-info/WHEEL", "Wheel-Version: 1.0\nTag: py3-none-any\n")
        archive.writestr("demo_package-2.3.4.dist-info/RECORD", "demo_package-2.3.4.dist-info/RECORD,,\n")
    return wheel


def test_checkout_is_unreleased_and_json_output():
    result = run("--checkout", str(FIXTURES / "checkout_unreleased"), "--json")
    assert result.returncode == 0
    data = json.loads(result.stdout)
    assert data["source_kind"] == "checkout"
    assert data["version"] == "unreleased"
    assert data["contract"]["distribution"] == "demo-package"


def test_invalid_json_has_actionable_error():
    result = run("--checkout", str(FIXTURES / "invalid_json"))
    assert result.returncode != 0
    assert "JSON" in result.stderr


def test_missing_behavior_has_actionable_error():
    result = run("--checkout", str(FIXTURES / "missing_behavior"))
    assert result.returncode != 0
    assert "behavior.md" in result.stderr


def test_unknown_schema_is_rejected():
    path = FIXTURES / "valid_package/_agent/api-contract.json"
    payload = json.loads(path.read_text())
    payload["schema_version"] = "99.0"
    temp = FIXTURES / "_tmp_unknown_schema"
    (temp / "_agent").mkdir(parents=True, exist_ok=True)
    (temp / "_agent/api-contract.json").write_text(json.dumps(payload))
    (temp / "_agent/behavior.md").write_text("# Behavior")
    try:
        result = run("--checkout", str(temp))
        assert result.returncode != 0
        assert "schema_version" in result.stderr
    finally:
        (temp / "_agent/api-contract.json").unlink()
        (temp / "_agent/behavior.md").unlink()
        (temp / "_agent").rmdir()
        temp.rmdir()


def test_help_and_missing_source():
    assert run("--help").returncode == 0
    result = run("--checkout", str(FIXTURES / "does-not-exist"))
    assert result.returncode != 0
    assert "No contract" in result.stderr


def test_wheel_source_and_version(tmp_path):
    wheel = make_wheel(tmp_path)
    result = run("--wheel", str(wheel), "--json")
    assert result.returncode == 0
    data = json.loads(result.stdout)
    assert data["source_kind"] == "wheel"
    assert data["version"] == "2.3.4"
    assert data["publication_state"] == "unknown"
    assert "published" not in result.stdout


def test_same_local_wheel_installed_in_isolated_target_is_installed(tmp_path):
    wheel = make_wheel(tmp_path)
    target = tmp_path / "installed"
    install = subprocess.run(
        [sys.executable, "-m", "pip", "install", "--no-deps", "--target", str(target), str(wheel)],
        text=True,
        capture_output=True,
    )
    assert install.returncode == 0, install.stderr
    environment = os.environ.copy()
    environment["PYTHONPATH"] = str(target)
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--distribution", "demo-package", "--json"],
        text=True,
        capture_output=True,
        env=environment,
    )
    assert result.returncode == 0, result.stderr
    data = json.loads(result.stdout)
    assert data["source_kind"] == "installed"
    assert data["version"] == "2.3.4"
    assert data["publication_state"] == "unknown"
    assert "published" not in result.stdout


def test_human_and_structured_output_use_same_source_terminology(tmp_path):
    wheel = make_wheel(tmp_path)
    structured = run("--wheel", str(wheel), "--json")
    human = run("--wheel", str(wheel))
    assert structured.returncode == human.returncode == 0
    assert json.loads(structured.stdout)["source_kind"] == "wheel"
    assert "source: wheel" in human.stdout
    assert "publication state: unknown" in human.stdout
    assert "published" not in human.stdout


def test_uninstalled_distribution_is_actionable():
    result = run("--distribution", "definitely-not-installed-demo-package")
    assert result.returncode != 0
    assert "--checkout" in result.stderr


def test_installed_distribution_is_resolved_without_importing_package(monkeypatch, tmp_path):
    module = load_module()
    package_root = tmp_path / "demo_package" / "_agent"
    package_root.mkdir(parents=True)
    for name in ("api-contract.json", "behavior.md"):
        (package_root / name).write_bytes((FIXTURES / "valid_package/_agent" / name).read_bytes())

    class FakeDistribution:
        version = "7.8.9"
        files = ["demo_package/_agent/api-contract.json", "demo_package/_agent/behavior.md"]

        def locate_file(self, relative):
            return tmp_path / relative

    monkeypatch.setattr(module.metadata, "distribution", lambda name: FakeDistribution())
    contract, kind, version = module.from_installed("demo-package")
    assert contract["distribution"] == "demo-package"
    assert kind == "installed"
    assert version == "7.8.9"
