"""Record the software environment used for the CAP182 SS2 experiment."""
from __future__ import annotations

import json
import platform
import sys
from importlib.metadata import version

from common import RESULTS_DIR


PACKAGES = [
    "numpy", "pandas", "scikit-learn", "xgboost", "scipy",
    "matplotlib", "joblib",
]


def main() -> int:
    report = {
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "packages": {name: version(name) for name in PACKAGES},
    }
    out = RESULTS_DIR + "/environment.json"
    with open(out, "w", encoding="utf-8") as stream:
        json.dump(report, stream, indent=2)
    print("Environment:", json.dumps(report, indent=2))
    print("Wrote experimental-results/environment.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
