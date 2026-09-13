"""
run_all.py -- one-command reproduction of the CAP182 SS2 pipeline.

Steps: download data -> train Model 1 -> train Model 2 -> compare.
Run:  python scripts/run_all.py
"""
from __future__ import annotations
import runpy, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)


def _run(module_file: str):
    print("\n" + "=" * 70 + f"\n>>> {module_file}\n" + "=" * 70, flush=True)
    try:
        runpy.run_path(os.path.join(HERE, module_file), run_name="__main__")
    except SystemExit as e:
        # Each step raises SystemExit(code); treat non-zero as a hard failure.
        code = e.code if isinstance(e.code, int) else (0 if e.code is None else 1)
        if code != 0:
            raise RuntimeError(f"{module_file} exited with code {code}")


def main() -> int:
    for step in ["download_data.py", "environment_report.py",
                 "train_model1_logreg.py", "train_model2_xgboost.py",
                 "explain_models.py", "compare_models.py"]:
        _run(step)
    print("\nPipeline complete. See experimental-results/ for outputs.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
