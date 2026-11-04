import json
from pathlib import Path

notebook = {
    "cells": [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# 🗑️ AI-Based Smart Garbage Waste Segregator — 100-Epoch Master Training\n",
                "### Target: 72% - 78%+ mAP50, >75% Precision across 15 Waste Classes\n",
                "\n",
                "**Optimized Hyperparameters:**\n",
                "- **Architecture**: YOLO11 Nano (`yolo11n.pt`)\n",
                "- **Epochs**: 100 full epochs with Cosine Annealing (`cos_lr=True`)\n",
                "- **Resolution**: `imgsz=800` (4x more pixel surface for small items like caps, peels, scrap)\n",
                "- **Loss Tuning**: Focal Loss `fl_gamma=1.5` + `cls=0.7` + `box=7.5`\n",
                "- **Augmentation**: `copy_paste=0.3`, `mixup=0.15`, `mosaic=1.0` with `close_mosaic=10`\n",
                "- **Platform**: Kaggle GPU (NVIDIA T4 x2 or P100 — 100% Free 30h/week)"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Step 1: Install Ultralytics and Verify NVIDIA GPU\n",
                "!pip install -q ultralytics gdown\n",
                "!nvidia-smi"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## Step 2: Locate or Download the 15-Class Master Dataset\n",
                "This step automatically searches for your dataset:\n",
                "1. If you uploaded it as a **Kaggle Dataset**, it detects it instantly in `/kaggle/input/`.\n",
                "2. If you want to download directly from **Google Drive**, uncomment the `gdown` line."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "import os\n",
                "import sys\n",
                "import shutil\n",
                "import zipfile\n",
                "from pathlib import Path\n",
                "\n",
                "WORKING_DIR = Path(\"/kaggle/working\")\n",
                "DATASET_DIR = WORKING_DIR / \"waste_15class_master\"\n",
                "\n",
                "# --- Option A: Download from Google Drive (if needed) ---\n",
                "# Replace with your Google Drive File ID if you want direct download:\n",
                "# !gdown \"YOUR_GOOGLE_DRIVE_FILE_ID\" -O /kaggle/working/dataset.zip\n",
                "\n",
                "# --- Auto-Detection ---\n",
                "if not DATASET_DIR.exists():\n",
                "    kaggle_input = Path(\"/kaggle/input\")\n",
                "    found_in_input = False\n",
                "    for p in kaggle_input.glob(\"**/*\"):\n",
                "        if p.name == \"data.yaml\" or (p.is_dir() and (p / \"images\" / \"train\").exists()):\n",
                "            source_dir = p.parent if p.name == \"data.yaml\" else p\n",
                "            print(f\"✅ Found dataset in Kaggle input: {source_dir}\")\n",
                "            DATASET_DIR = source_dir\n",
                "            found_in_input = True\n",
                "            break\n",
                "    \n",
                "    if not found_in_input:\n",
                "        zip_files = list(WORKING_DIR.glob(\"*.zip\")) + list(kaggle_input.glob(\"**/*.zip\"))\n",
                "        if zip_files:\n",
                "            zip_path = zip_files[0]\n",
                "            print(f\"📦 Unzipping dataset from {zip_path}...\")\n",
                "            with zipfile.ZipFile(zip_path, \"r\") as zip_ref:\n",
                "                zip_ref.extractall(DATASET_DIR)\n",
                "            print(\"✅ Extraction complete!\")\n",
                "        else:\n",
                "            print(\"⚠️ No dataset found. Please upload dataset.zip or attach as Kaggle Dataset.\")\n",
                "\n",
                "print(f\"Active Dataset Directory: {DATASET_DIR}\")"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## Step 3: Configure `data.yaml` Paths\n",
                "Ensures train and val paths point dynamically to the active environment."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "yaml_file = WORKING_DIR / \"data.yaml\"\n",
                "\n",
                "yaml_content = f\"\"\"path: {DATASET_DIR.resolve()}\n",
                "train: images/train\n",
                "val: images/val\n",
                "test: images/test\n",
                "nc: 15\n",
                "names:\n",
                "  0: plastic_bottle\n",
                "  1: plastic_wrapper\n",
                "  2: plastic_bag\n",
                "  3: plastic_container\n",
                "  4: paper\n",
                "  5: cardboard_carton\n",
                "  6: glass\n",
                "  7: metal_can\n",
                "  8: metal_scrap\n",
                "  9: styrofoam\n",
                "  10: food_waste\n",
                "  11: fruit_vegetable_peel\n",
                "  12: garden_waste\n",
                "  13: textile\n",
                "  14: e_waste\n",
                "\"\"\"\n",
                "\n",
                "with open(yaml_file, \"w\") as f:\n",
                "    f.write(yaml_content)\n",
                "\n",
                "print(f\"✅ data.yaml written to: {yaml_file}\")\n",
                "train_count = len(list((DATASET_DIR / \"images\" / \"train\").glob(\"*.*v\")) + list((DATASET_DIR / \"images\" / \"train\").glob(\"*.jp*\")) + list((DATASET_DIR / \"images\" / \"train\").glob(\"*.png\")))\n",
                "val_count = len(list((DATASET_DIR / \"images\" / \"val\").glob(\"*.jp*\")) + list((DATASET_DIR / \"images\" / \"val\").glob(\"*.png\")))\n",
                "print(f\"📊 Ready: {train_count} train images | {val_count} validation images\")"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## Step 4: Run 100-Epoch Master Training\n",
                "Starts the full training run with Cosine LR, `imgsz=800`, Focal loss, and advanced augmentations."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "from ultralytics import YOLO\n",
                "\n",
                "# Starting from yolo11n.pt\n",
                "model = YOLO(\"yolo11n.pt\")\n",
                "\n",
                "results = model.train(\n",
                "    data=str(yaml_file),\n",
                "    epochs=100,\n",
                "    batch=16,\n",
                "    imgsz=800,              # 800px resolves small items (peels, bottle caps, cans)\n",
                "    device=0,\n",
                "    optimizer=\"AdamW\",\n",
                "    lr0=0.003,              # Balanced starting LR\n",
                "    lrf=0.01,               # Decays to 0.00003 at epoch 100\n",
                "    cos_lr=True,            # Cosine annealing schedule\n",
                "    warmup_epochs=3,\n",
                "    box=7.5,                # High box localization penalty\n",
                "    cls=0.7,                # High classification penalty\n",
                "    fl_gamma=1.5,           # Focal loss: heavily weights hard samples (plastic bags, scrap)\n",
                "    mosaic=1.0,             # Full mosaic for diverse multiobject scenes\n",
                "    mixup=0.15,             # Mixup for stacked/occluded waste items\n",
                "    copy_paste=0.3,         # Copy-paste minority objects onto diverse backgrounds\n",
                "    close_mosaic=10,        # Turn off mosaic in last 10 epochs for clean convergence\n",
                "    degrees=10.0,\n",
                "    fliplr=0.5,\n",
                "    workers=4,\n",
                "    project=\"/kaggle/working/runs/detect\",\n",
                "    name=\"yolo11n_15class_kaggle_master\",\n",
                "    exist_ok=True,\n",
                "    save=True,\n",
                "    save_period=10,\n",
                "    val=True,\n",
                "    plots=True\n",
                ")"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## Step 5: Evaluate & Print Per-Class Performance"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "best_weights = \"/kaggle/working/runs/detect/yolo11n_15class_kaggle_master/weights/best.pt\"\n",
                "best_model = YOLO(best_weights)\n",
                "\n",
                "val_res = best_model.val(data=str(yaml_file), split=\"val\", imgsz=800, device=0)\n",
                "\n",
                "print(\"\\n=================== 15-CLASS KAGGLE MASTER RESULTS ===================\")\n",
                "print(f\"Overall mAP@50:    {val_res.box.map50 * 100:.2f}%\")\n",
                "print(f\"Overall Precision: {val_res.box.mp * 100:.2f}%\")\n",
                "print(f\"Overall Recall:    {val_res.box.mr * 100:.2f}%\")\n",
                "print(f\"Overall mAP50-95:  {val_res.box.map * 100:.2f}%\")\n",
                "print(\"-\" * 68)\n",
                "names = val_res.names\n",
                "for i in sorted(names.keys()):\n",
                "    p = val_res.box.p[i] * 100 if len(val_res.box.p) > i else 0\n",
                "    r = val_res.box.r[i] * 100 if len(val_res.box.r) > i else 0\n",
                "    ap50 = val_res.box.ap50[i] * 100 if len(val_res.box.ap50) > i else 0\n",
                "    print(f\"[{i:2d}] {names[i]:22s} | mAP50: {ap50:5.1f}% | P: {p:5.1f}% | R: {r:5.1f}%\")\n",
                "print(\"======================================================================\")"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## Step 6: 1-Click Export Archive\n",
                "Packages `best.pt`, `results.csv`, confusion matrix, and PR curves into a single zip file ready to download."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "run_dir = Path(\"/kaggle/working/runs/detect/yolo11n_15class_kaggle_master\")\n",
                "zip_filename = \"/kaggle/working/yolo11n_15class_kaggle_master.zip\"\n",
                "\n",
                "with zipfile.ZipFile(zip_filename, \"w\", compression=zipfile.ZIP_DEFLATED) as zipf:\n",
                "    for file_path in run_dir.rglob(\"*\"):\n",
                "        if file_path.is_file() and not (\"epoch\" in file_path.name and file_path.name.endswith(\".pt\")):\n",
                "            arcname = file_path.relative_to(run_dir)\n",
                "            zipf.write(file_path, arcname)\n",
                "\n",
                "print(f\"🎉 SUCCESS! Training results zipped to: {zip_filename}\")\n",
                "print(f\"📦 File size: {os.path.getsize(zip_filename) / (1024*1024):.1f} MB\")\n",
                "print(\"👉 Go to Kaggle right sidebar -> 'Output' -> Click the 3 dots on 'yolo11n_15class_kaggle_master.zip' -> Download!\")"
            ]
        }
    ],
    "metadata": {
        "accelerator": "GPU",
        "kaggle": {
            "accelerator": "nvidiaTeslaT4",
            "dataSources": [],
            "dockerImageVersionId": 30698,
            "isGpuEnabled": True,
            "isInternetEnabled": True,
            "language": "python"
        },
        "language_info": {
            "name": "python",
            "version": "3.10"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 2
}

output_path = Path("waste_segregator_kaggle_master.ipynb")
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(notebook, f, indent=2)

print(f"✅ Generated {output_path.resolve()} ({output_path.stat().st_size} bytes)")

