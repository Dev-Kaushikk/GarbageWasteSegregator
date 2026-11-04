#!/usr/bin/env python3
"""
Fast packager for the 8,574-image balanced master dataset into a Kaggle/Drive upload zip.
Uses compression level 1 for maximum speed and small file size (~2.4 GB).
"""
import os
import sys
import zipfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
DATASET_DIR = PROJECT_ROOT / "datasets" / "waste_15class_master"
OUTPUT_ZIP = PROJECT_ROOT / "datasets" / "waste_15class_master_balanced.zip"

def package():
    if not DATASET_DIR.exists():
        print(f"❌ Dataset folder not found: {DATASET_DIR}")
        sys.exit(1)

    print(f"📦 Packaging {DATASET_DIR} into {OUTPUT_ZIP}...")
    files_to_pack = [p for p in DATASET_DIR.rglob("*") if p.is_file() and not p.name.startswith(".")]
    total = len(files_to_pack)
    print(f"Found {total} files to package.")

    with zipfile.ZipFile(OUTPUT_ZIP, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=1) as zf:
        for idx, file_path in enumerate(files_to_pack, 1):
            arcname = file_path.relative_to(DATASET_DIR.parent)
            zf.write(file_path, arcname)
            if idx % 1000 == 0 or idx == total:
                print(f"  Processed {idx}/{total} files ({idx/total*100:.1f}%)...")

    size_mb = OUTPUT_ZIP.stat().st_size / (1024 * 1024)
    print(f"\n✅ Created: {OUTPUT_ZIP} ({size_mb:.1f} MB)")
    print("👉 Upload this zip to Kaggle Datasets or Google Drive for 100-epoch training!")

if __name__ == "__main__":
    package()

