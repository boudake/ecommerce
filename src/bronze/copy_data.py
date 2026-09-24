from __future__ import annotations

import shutil
from pathlib import Path


def copy_data_to_landing(source_dir: str | Path, landing_dir: str | Path) -> list[Path]:
    """Copy CSV files from a source data directory into a landing directory."""
    source_path = Path(source_dir)
    landing_path = Path(landing_dir)

    landing_path.mkdir(parents=True, exist_ok=True)

    copied_files: list[Path] = []
    for csv_file in sorted(source_path.glob("*.csv")):
        target = landing_path / csv_file.name
        shutil.copy2(csv_file, target)
        copied_files.append(target)

    return copied_files


if __name__ == "__main__":
    copy_data_to_landing("data", "data/landing")
