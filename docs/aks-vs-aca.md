from __future__ import annotations

import os
from pathlib import Path


def main() -> None:
    dataset_path = Path(os.getenv("DATASET_PATH", "data/international_results.csv"))
    dataset_path.parent.mkdir(parents=True, exist_ok=True)
    if dataset_path.exists():
        print(f"Dataset already present: {dataset_path}")
        return

    print("The dataset is not committed to this repository.")
    print("Download the official international football results CSV to this local path:")
    print(f"  {dataset_path}")
    print("Then rerun this script or start the app.")


if __name__ == "__main__":
    main()
