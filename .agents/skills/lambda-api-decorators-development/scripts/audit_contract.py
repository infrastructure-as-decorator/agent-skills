#!/usr/bin/env python3
"""Audit local Infrastructure as Decorators repositories and examples."""
from __future__ import annotations

import argparse
import ast
import re
import subprocess
from pathlib import Path

KNOWN = ("lambda-api-decorators", "lambda-api-decorators-cdk", "lambda-api-decorators-examples", "docs")
HTTP_NAMES = {"get", "post", "put", "patch", "delete", "head", "options", "route", "http"}


def git(repo: Path, *args: str) -> str:
    result = subprocess.run(["git", *args], cwd=repo, text=True, capture_output=True)
    return result.stdout.strip() if result.returncode == 0 else "unknown"


def python_findings(path: Path) -> list[str]:
    findings = []
    for file in path.rglob("*.py"):
        try:
            tree = ast.parse(file.read_text(encoding="utf-8"))
        except (OSError, SyntaxError):
            continue
        text = file.read_text(encoding="utf-8")
        if re.search(r"requestContext['\"]\s*\]\s*\[\s*['\"]authorizer['\"]\s*\]\s*\[\s*['\"]claims['\"]", text) or "requestContext.authorizer.claims" in text:
            findings.append(f"WARNING manual claim parsing: {file}")
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                decorators = []
                for dec in node.decorator_list:
                    name = dec.func.id if isinstance(dec, ast.Call) and isinstance(dec.func, ast.Name) else dec.id if isinstance(dec, ast.Name) else ""
                    if name.lower() in HTTP_NAMES:
                        decorators.append(name)
                if len(decorators) > 1:
                    findings.append(f"WARNING multiple HTTP decorators on {node.name}: {file}")
    return findings


def dependency_findings(path: Path) -> list[str]:
    findings = []
    for file in path.rglob("*"):
        if file.name.startswith("requirements") or file.name == "pyproject.toml":
            try:
                text = file.read_text(encoding="utf-8")
            except OSError:
                continue
            if re.search(r"git\+|\s-e\s|^-e\s|path\s*=|file://", text, re.MULTILINE):
                findings.append(f"WARNING Git dependency or editable/path install: {file}")
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="directory containing known repositories")
    args = parser.parse_args()
    for name in KNOWN:
        repo = args.root / name
        if not repo.is_dir():
            print(f"{name}: absent (not fatal)")
            continue
        dirty = bool(git(repo, "status", "--porcelain"))
        print(f"{name}: branch={git(repo, 'branch', '--show-current')} HEAD={git(repo, 'rev-parse', 'HEAD')} tag={git(repo, 'describe', '--tags', '--abbrev=0')} working_tree={'dirty' if dirty else 'clean'}")
        contracts = list(repo.rglob("_agent/api-contract.json"))
        print(f"  contracts: {', '.join(map(str, contracts)) if contracts else 'none (published package may provide it)'}")
        for finding in python_findings(repo) + dependency_findings(repo):
            print(f"  {finding}")
    if args.root.name not in KNOWN:
        for finding in python_findings(args.root) + dependency_findings(args.root):
            print(f"root: {finding}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
