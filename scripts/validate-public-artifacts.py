#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path


FORBIDDEN_PATTERNS = [
    re.compile(r"tok_[A-Za-z0-9._=-]+"),
    re.compile(r'"key"\s*:\s*"[0-9a-fA-F]{16,}"'),
    re.compile(r'"keyId"\s*:\s*"[0-9a-fA-F]{16,}"'),
    re.compile(r'"key_id"\s*:\s*"[0-9a-fA-F]{16,}"'),
    re.compile(r"flow-cdn", re.IGNORECASE),
    re.compile(r"cvattv", re.IGNORECASE),
]


def scan_file(path: Path) -> list[str]:
    if path.suffix.lower() not in {".json", ".xml", ".m3u", ".m3u8", ".txt", ".md"}:
        return []
    text = path.read_text(encoding="utf-8", errors="ignore")
    findings = []
    for pattern in FORBIDDEN_PATTERNS:
        if pattern.search(text):
            findings.append(f"{path}: patron prohibido {pattern.pattern}")
    return findings


def validate_latest(root: Path) -> list[str]:
    latest = root / "releases" / "latest.json"
    if not latest.exists():
        return ["Falta releases/latest.json"]
    data = json.loads(latest.read_text(encoding="utf-8"))
    required = [
        "versionCode",
        "versionName",
        "minSupportedVersionCode",
        "apkUrl",
        "sha256",
        "sizeBytes",
        "releasedAt",
        "mandatory",
        "notes",
    ]
    missing = [key for key in required if key not in data]
    errors = [f"latest.json sin campo {key}" for key in missing]
    if "sha256" in data and not re.fullmatch(r"[0-9a-fA-F]{64}", str(data["sha256"])):
        errors.append("latest.json sha256 invalido")
    return errors


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    errors = validate_latest(root)
    for path in root.rglob("*"):
        if path.is_file() and ".git" not in path.parts:
            errors.extend(scan_file(path))
    if errors:
        print("Validacion publica fallo:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Artefactos publicos validados.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
