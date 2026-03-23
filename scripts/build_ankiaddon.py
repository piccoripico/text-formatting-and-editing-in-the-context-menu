from __future__ import annotations

import argparse
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

REPO_ROOT = Path(__file__).resolve().parent.parent
ADDON_ROOT = REPO_ROOT / "Text-Tools"
DEFAULT_OUTPUT = REPO_ROOT / "dist" / "Text-Tools.ankiaddon"


def should_include(path: Path) -> bool:
    rel = path.relative_to(ADDON_ROOT)

    if any(part == "__pycache__" for part in rel.parts):
        return False

    if path.suffix.lower() in {".pyc", ".pyo"}:
        return False

    if rel.parts and rel.parts[0] == "user_files" and rel.name != "README.txt":
        return False

    return True


def build_package(output_path: Path) -> list[Path]:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    packaged_files: list[Path] = []

    with ZipFile(output_path, "w", compression=ZIP_DEFLATED) as archive:
        for path in sorted(ADDON_ROOT.rglob("*")):
            if not path.is_file() or not should_include(path):
                continue

            rel = path.relative_to(ADDON_ROOT)
            archive.write(path, arcname=rel.as_posix())
            packaged_files.append(rel)

    return packaged_files


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build a clean .ankiaddon package from the Text-Tools add-on directory."
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help=f"Output .ankiaddon path (default: {DEFAULT_OUTPUT})",
    )
    args = parser.parse_args()

    packaged_files = build_package(args.output.resolve())
    print(f"Built {args.output.resolve()}")
    print(f"Included {len(packaged_files)} files:")
    for rel in packaged_files:
        print(f" - {rel.as_posix()}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
