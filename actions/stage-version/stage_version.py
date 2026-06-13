#!/usr/bin/env python3
"""Apply a TestPyPI staging version and provider dependency pins to the working
tree, in place, without committing.

Used by the `stage-version` composite action so that the org's `testpypi.yml`
workflows can build a staging wheel from `main` with a synthetic version
injected only into the ephemeral CI checkout. The rewrite logic mirrors the
release orchestrator's `stage_testpypi.py` (project version, Python
requirement pins, CMake find_package/find_dependency versions).

Inputs are read from the environment so the composite action can pass a
multiline pin list without shell-quoting hazards:

    STAGE_VERSION  required, e.g. "999.0.3"
    STAGE_PINS     optional, newline-separated "package=version" (or
                   "package==version"); lines with an empty version are ignored
    STAGE_ROOT     optional working directory (default ".")
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path


TEXT_FILE_NAMES = {"Apptainer", "CMakeLists.txt"}
TEXT_FILE_SUFFIXES = {".cmake", ".in", ".md", ".toml", ".txt", ".yml", ".yaml"}
EXCLUDED_DIRS = {
    ".git",
    ".github",
    ".venv",
    "__pycache__",
    "build",
    "build_debug",
    "build_release",
    "build_Debug",
    "build_Release",
    "dependencies-build",
    "dependencies-install",
    "old",
}


def replace_project_version(text: str, version: str) -> str:
    return re.sub(r'(?m)^version\s*=\s*"[^"]+"', f'version = "{version}"', text, count=1)


def replace_python_requirement(text: str, package: str, version: str, operator: str = "==") -> str:
    # Consume the whole (possibly comma-separated) version specifier so a pin
    # like "pyyggdrasil>=0.0.17,<0.1" becomes "pyyggdrasil==999.0.2" rather than
    # the contradictory "pyyggdrasil==999.0.2,<0.1" that no version satisfies.
    clause = r"(?:==|>=|~=|<=|!=|>|<)\s*[0-9][A-Za-z0-9.!+_-]*"
    pattern = rf"(?<![A-Za-z0-9_.-]){re.escape(package)}\s*{clause}(?:\s*,\s*{clause})*"
    return re.sub(pattern, f"{package}{operator}{version}", text)


def replace_cmake_dependency(text: str, package: str, version: str) -> str:
    pattern = rf"(find_(?:package|dependency)\(\s*{re.escape(package)})(?P<body>[^)]*)\)"

    def replace(match: re.Match[str]) -> str:
        head = match.group(1)
        body = match.group("body")
        stripped = body.lstrip()
        leading = body[: len(body) - len(stripped)]
        version_pattern = r"(?P<prefix>\s+)[0-9][A-Za-z0-9.!+_-]*"
        if re.match(version_pattern, body):
            body = re.sub(version_pattern, rf"\g<prefix>{version}", body, count=1)
        else:
            separator = leading if leading else " "
            body = f"{separator}{version} {stripped}"
        return f"{head}{body})"

    return re.sub(pattern, replace, text)


def is_patchable_text_file(relative_path: Path) -> bool:
    if any(part in EXCLUDED_DIRS for part in relative_path.parts):
        return False
    return relative_path.name in TEXT_FILE_NAMES or relative_path.suffix in TEXT_FILE_SUFFIXES


def iter_patchable_files(root: Path) -> list[Path]:
    return sorted(
        path
        for path in root.rglob("*")
        if path.is_file() and is_patchable_text_file(path.relative_to(root))
    )


def parse_pins(raw: str) -> dict[str, str]:
    pins: dict[str, str] = {}
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        package, sep, version = line.partition("=")
        package = package.strip()
        version = version.lstrip("=").strip()  # tolerate "pkg==ver"
        if not sep or not package or not version:
            continue
        pins[package] = version
    return pins


def stage(root: Path, version: str, pins: dict[str, str]) -> list[Path]:
    changed: list[Path] = []
    for path in iter_patchable_files(root):
        old = path.read_text()
        new = old
        if path.name == "pyproject.toml":
            new = replace_project_version(new, version)
        for package, pin_version in pins.items():
            new = replace_python_requirement(new, package, pin_version)
            new = replace_cmake_dependency(new, package, pin_version)
        if new != old:
            path.write_text(new)
            changed.append(path)
    return changed


def main() -> int:
    version = os.environ.get("STAGE_VERSION", "").strip()
    if not version:
        print("STAGE_VERSION must be set", file=sys.stderr)
        return 2
    pins = parse_pins(os.environ.get("STAGE_PINS", ""))
    root = Path(os.environ.get("STAGE_ROOT", ".")).resolve()

    changed = stage(root, version, pins)

    print(f"staged version={version} pins={pins or '{}'}")
    for path in changed:
        print(f"  patched {path.relative_to(root)}")
    if not changed:
        print("  (no files changed)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
