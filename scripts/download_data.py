"""
download_data.py -- Downloads the UCI Bank Marketing dataset (Moro et al., 2014).

Downloads the original dataset from the UCI Machine Learning Repository (data set
number 222) and extracts bank-additional-full.csv (41,188 observations,
20 attributes) to datasets/. The original CSV file is not version-controlled;
this script reproduces it without version control.

Usage:  python scripts/download_data.py
"""
from __future__ import annotations
import io
import os
import sys
import zipfile
import urllib.request

from common import DATA_DIR, RAW_CSV

UCI_ZIP_URL = "https://archive.ics.uci.edu/static/public/222/bank+marketing.zip"
TARGET_CSV_NAME = "bank-additional-full.csv"


def _find_and_extract(zbytes: bytes, target_name: str, out_path: str) -> bool:
    """Search a (possibly nested) zip for target_name and write it to out_path."""
    with zipfile.ZipFile(io.BytesIO(zbytes)) as z:
        for name in z.namelist():
            if name.endswith(target_name):
                with z.open(name) as f:
                    data = f.read()
                with open(out_path, "wb") as out:
                    out.write(data)
                return True
        # Not found at this level -- recurse into nested .zip members
        for name in z.namelist():
            if name.lower().endswith(".zip"):
                nested = z.read(name)
                if _find_and_extract(nested, target_name, out_path):
                    return True
    return False


def main() -> int:
    os.makedirs(DATA_DIR, exist_ok=True)
    if os.path.exists(RAW_CSV):
        print(f"Already present: {RAW_CSV}")
        return 0
    print(f"Downloading {UCI_ZIP_URL} ...")
    req = urllib.request.Request(UCI_ZIP_URL, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        zbytes = resp.read()
    print(f"Downloaded {len(zbytes)/1e6:.1f} MB. Extracting {TARGET_CSV_NAME} ...")
    ok = _find_and_extract(zbytes, TARGET_CSV_NAME, RAW_CSV)
    if not ok:
        print("ERROR: could not locate", TARGET_CSV_NAME, file=sys.stderr)
        return 1
    print(f"Saved: {RAW_CSV}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
