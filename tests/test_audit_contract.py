import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).parents[1] / "skills/maintain-lambda-api-decorators/scripts/audit_contract.py"
FIXTURES = Path(__file__).parent / "fixtures"


def test_audit_reports_antipatterns_as_warnings():
    result = subprocess.run([sys.executable, str(SCRIPT), "--root", str(FIXTURES / "audit_repo")], text=True, capture_output=True)
    assert result.returncode == 0
    assert "manual claim parsing" in result.stdout
    assert "multiple HTTP decorators" in result.stdout
    assert "Git dependency" in result.stdout


def test_audit_missing_repositories_is_not_fatal():
    result = subprocess.run([sys.executable, str(SCRIPT), "--root", str(FIXTURES)], text=True, capture_output=True)
    assert result.returncode == 0
    assert "absent" in result.stdout
