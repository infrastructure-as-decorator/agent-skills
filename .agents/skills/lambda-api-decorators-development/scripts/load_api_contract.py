#!/usr/bin/env python3
"""Resolve a packaged Infrastructure as Decorators API contract."""
from __future__ import annotations

import argparse
import importlib.metadata as metadata
import json
import sys
import zipfile
from pathlib import Path, PurePosixPath

SUPPORTED_SCHEMA = {"1.0"}


class ContractError(Exception):
    pass


def validate(contract: dict, behavior: str) -> None:
    if not isinstance(contract, dict):
        raise ContractError("contract JSON must contain an object")
    if contract.get("schema_version") not in SUPPORTED_SCHEMA:
        raise ContractError(f"unsupported schema_version {contract.get('schema_version')!r}; supported: {sorted(SUPPORTED_SCHEMA)}")
    required = {"schema_version", "distribution", "import_package", "exports", "functions", "decorators", "classes", "exceptions"}
    missing = sorted(required - contract.keys())
    if missing:
        raise ContractError("contract missing required fields: " + ", ".join(missing))
    if "version" in contract:
        raise ContractError("contract must not contain package version")
    if not isinstance(behavior, str) or not behavior.strip():
        raise ContractError("behavior.md must be non-empty")
    for field in ("exports", "functions", "decorators", "classes", "exceptions"):
        if not isinstance(contract[field], list):
            raise ContractError(f"contract field {field!r} must be an array")


def from_directory(directory: Path) -> tuple[dict, str, str]:
    if not directory.is_dir():
        raise ContractError(f"No contract found: checkout directory does not exist: {directory}")
    candidates = [directory / "_agent", *[p / "_agent" for p in directory.glob("src/*") if p.is_dir()], *[p / "_agent" for p in directory.iterdir() if p.is_dir()]]
    agent = next((p for p in candidates if (p / "api-contract.json").is_file()), None)
    if agent is None:
        raise ContractError(f"No contract found under checkout {directory}")
    return _read_files(agent / "api-contract.json", agent / "behavior.md", "checkout", "unreleased")


def from_wheel(wheel: Path) -> tuple[dict, str, str]:
    if not wheel.is_file():
        raise ContractError(f"wheel not found: {wheel}")
    with zipfile.ZipFile(wheel) as archive:
        names = set(archive.namelist())
        contract_name = next((n for n in names if n.endswith("/_agent/api-contract.json") or n == "_agent/api-contract.json"), None)
        if not contract_name:
            raise ContractError(f"No contract found in wheel {wheel}")
        behavior_name = str(PurePosixPath(contract_name).parent / "behavior.md")
        if behavior_name not in names:
            raise ContractError(f"wheel is missing {behavior_name}")
        try:
            contract = json.loads(archive.read(contract_name).decode())
        except json.JSONDecodeError as exc:
            raise ContractError(f"invalid JSON in wheel contract: {exc}") from exc
        behavior = archive.read(behavior_name).decode()
        validate(contract, behavior)
        version = _wheel_version(archive)
        return contract, "wheel", version


def _wheel_version(archive: zipfile.ZipFile) -> str:
    dist_info = next((n for n in archive.namelist() if n.endswith(".dist-info/METADATA")), None)
    if not dist_info:
        return "unknown"
    for line in archive.read(dist_info).decode(errors="replace").splitlines():
        if line.lower().startswith("version:"):
            return line.split(":", 1)[1].strip()
    return "unknown"


def _read_files(contract_path: Path, behavior_path: Path, kind: str, version: str) -> tuple[dict, str, str]:
    if not behavior_path.is_file():
        raise ContractError(f"missing behavior.md next to {contract_path}")
    try:
        contract = json.loads(contract_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ContractError(f"invalid JSON in {contract_path}: {exc}") from exc
    validate(contract, behavior_path.read_text(encoding="utf-8"))
    return contract, kind, version


def from_installed(distribution: str) -> tuple[dict, str, str]:
    try:
        dist = metadata.distribution(distribution)
    except metadata.PackageNotFoundError as exc:
        raise ContractError(f"installed distribution {distribution!r} is unavailable; provide --checkout or --wheel") from exc
    files = list(dist.files or [])
    contract_rel = next((p for p in files if str(p).endswith("/_agent/api-contract.json") or str(p) == "_agent/api-contract.json"), None)
    if contract_rel is None:
        raise ContractError(f"installed distribution {distribution!r} has no _agent/api-contract.json")
    contract_path = Path(dist.locate_file(contract_rel))
    behavior_path = contract_path.with_name("behavior.md")
    return _read_files(contract_path, behavior_path, "installed", dist.version)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group()
    source.add_argument("--distribution", help="installed distribution name")
    source.add_argument("--checkout", type=Path, help="local checkout containing the packaged contract")
    source.add_argument("--wheel", type=Path, help="local .whl file")
    parser.add_argument("--json", action="store_true", dest="as_json", help="emit machine-readable JSON")
    args = parser.parse_args(argv)
    try:
        if args.checkout:
            contract, kind, version = from_directory(args.checkout)
        elif args.wheel:
            contract, kind, version = from_wheel(args.wheel)
        elif args.distribution:
            contract, kind, version = from_installed(args.distribution)
        else:
            parser.error("one of --distribution, --checkout, or --wheel is required")
        result = {
            "source_kind": kind,
            "publication_state": "unknown",
            "version": version,
            "contract": contract,
        }
        if args.as_json:
            print(json.dumps(result, indent=2, sort_keys=True))
        else:
            print(f"source: {kind}\npublication state: unknown\nversion: {version}\ndistribution: {contract['distribution']}\nimport package: {contract['import_package']}")
        return 0
    except (ContractError, OSError, zipfile.BadZipFile) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
