"""
AI-Based Smart Garbage Waste Segregator
100-Epoch Master Training Script for Kaggle / Colab
Target: 72% - 78%+ mAP50, >75% Precision across 15 Waste Classes
"""

import os
import sys
import shutil
import zipfile
from pathlib import Path

# --- 1. System Setup ---
print("🚀 [1/5] Setting up environment...")
os.system("pip install -q ultralytics gdown")

import torch
from ultralytics import YOLO

print(f"CUDA Available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"GPU: {torch.cuda.get_device_name(0)}")

# --- 2. Locate Dataset ---
print("\n📂 [2/5] Locating 15-class master dataset...")
WORKING_DIR = Path("/kaggle/working" if Path("/kaggle").exists() else "/content")
DATASET_DIR = WORKING_DIR / "waste_15class_master"

if not DATASET_DIR.exists():
    # Check /kaggle/input if attached as dataset
    kaggle_input = Path("/kaggle/input")
    found = False
    if kaggle_input.exists():
        for p in kaggle_input.glob("**/*"):
            if p.name == "data.yaml" or (p.is_dir() and (p / "images" / "train").exists()):
                source_dir = p.parent if p.name == "data.yaml" else p
                print(f"✅ Found dataset in Kaggle input: {source_dir}")
                DATASET_DIR = source_dir
                found = True
                break

    if not found:
        # Search for any zip
        search_dirs = [WORKING_DIR]
        if kaggle_input.exists():
            search_dirs.append(kaggle_input)
        
        zip_candidates = []
        for d in search_dirs:
            zip_candidates.extend(d.glob("*.zip"))
            zip_candidates.extend(d.glob("**/*.zip"))

        if zip_candidates:
            zip_path = zip_candidates[0]
            print(f"📦 Extracting {zip_path} to {DATASET_DIR}...")
            with zipfile.ZipFile(zip_path, "r") as z:
                z.extractall(DATASET_DIR)
            print("✅ Extraction complete.")
        else:
            print("⚠️ No dataset found. Please attach dataset as Kaggle Dataset or download zip.")

# --- 3. Generate data.yaml with Absolute Paths ---
print("\n📝 [3/5] Configuring data.yaml...")
yaml_file = WORKING_DIR / "data.yaml"
yaml_content = f"""path: {DATASET_DIR.resolve()}
train: images/train
val: images/val
test: images/test
nc: 15
names:
  0: plastic_bottle
  1: plastic_wrapper
  2: plastic_bag
  3: plastic_container
  4: paper
  5: cardboard_carton
  6: glass
  7: metal_can
  8: metal_scrap
  9: styrofoam
  10: food_waste
  11: fruit_vegetable_peel
  12: garden_waste
  13: textile
  14: e_waste
"""
with open(yaml_file, "w") as f:
    f.write(yaml_content)

print(f"✅ data.yaml ready at {yaml_file}")

# --- 4. Launch 100-Epoch Master Training ---
print("\n🔥 [4/5] Launching 100-Epoch YOLO11 Master Training with Winning Hyperparameters...")
model = YOLO("yolo11n.pt")

results = model.train(
    data=str(yaml_file),
    epochs=100,
    batch=16,
    imgsz=800,              # 800px resolves small items (peels, bottle caps, cans)
    device=0,
    optimizer="AdamW",
    lr0=0.003,              # Balanced starting LR
    lrf=0.01,               # Decays to 0.00003 at epoch 100
    cos_lr=True,            # Cosine annealing schedule
    warmup_epochs=3,
    box=7.5,                # High box localization penalty
    cls=0.7,                # High classification penalty
    fl_gamma=1.5,           # Focal loss: heavily weights hard samples (plastic bags, scrap)
    mosaic=1.0,             # Full mosaic for diverse multiobject scenes
    mixup=0.15,             # Mixup for stacked/occluded waste items
    copy_paste=0.3,         # Copy-paste minority objects onto diverse backgrounds
    close_mosaic=10,        # Turn off mosaic in last 10 epochs for clean convergence
    degrees=10.0,
    fliplr=0.5,
    workers=4,
    project=str(WORKING_DIR / "runs" / "detect"),
    name="yolo11n_15class_kaggle_master",
    exist_ok=True,
    save=True,
    save_period=10,
    val=True,
    plots=True
)

# --- 5. Export Results Zip ---
print("\n📦 [5/5] Packaging results for local download...")
run_dir = WORKING_DIR / "runs" / "detect" / "yolo11n_15class_kaggle_master"
zip_filename = WORKING_DIR / "yolo11n_15class_kaggle_master.zip"

with zipfile.ZipFile(zip_filename, "w", compression=zipfile.ZIP_DEFLATED) as zipf:
    for file_path in run_dir.rglob("*"):
        if file_path.is_file() and not ("epoch" in file_path.name and file_path.name.endswith(".pt")):
            arcname = file_path.relative_to(run_dir)
            zipf.write(file_path, arcname)

print(f"\n🎉 ALL DONE! Download your model from: {zip_filename}")
print(f"File size: {os.path.getsize(zip_filename) / (1024*1024):.1f} MB")

