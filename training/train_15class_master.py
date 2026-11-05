#!/usr/bin/env python3
"""
High-Performance 15-Class YOLO11n Training Pipeline
AI-Based Smart Garbage Waste Segregator
Trained on: datasets/waste_15class_master
Hardware: Apple Silicon M4 MPS Acceleration
"""
import os
import sys
import shutil
import json
from pathlib import Path
from datetime import datetime

# Configure Ultralytics cache directory
os.environ['YOLO_CONFIG_DIR'] = '/tmp/ultralytics'

import torch
from ultralytics import YOLO

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATASET_YAML = PROJECT_ROOT / "datasets" / "waste_15class_master" / "data.yaml"
PRETRAINED_WEIGHTS = PROJECT_ROOT / "models" / "yolo11n.pt"
OUTPUT_DIR = PROJECT_ROOT / "runs" / "detect" / "runs" / "garbage"
TARGET_MODEL_PATH = PROJECT_ROOT / "models" / "yolo11n_15class_best.pt"

def select_device():
    if torch.backends.mps.is_available():
        print("⚡ Hardware Acceleration: Apple Silicon Metal Performance Shaders (MPS)")
        return "mps"
    elif torch.cuda.is_available():
        print("⚡ Hardware Acceleration: NVIDIA CUDA")
        return "0"
    print("⚠️ Hardware Acceleration: Standard CPU")
    return "cpu"

def main():
    print("=" * 70)
    print("🚀 AI-Based Smart Garbage Waste Segregator - 15-Class Training")
    print("=" * 70)
    print(f"Timestamp:      {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Dataset Config: {DATASET_YAML}")
    print(f"Base Weights:   {PRETRAINED_WEIGHTS}")
    
    device = select_device()
    
    if not DATASET_YAML.exists():
        print(f"❌ Dataset YAML not found: {DATASET_YAML}")
        sys.exit(1)
        
    if not PRETRAINED_WEIGHTS.exists():
        print(f"⚠️ {PRETRAINED_WEIGHTS} not found, Ultralytics will auto-download yolo11n.pt")
        weights_src = "yolo11n.pt"
    else:
        weights_src = str(PRETRAINED_WEIGHTS)

    # Initialize YOLO model
    print(f"\n📦 Initializing YOLO11n architecture from {weights_src}...")
    model = YOLO(weights_src)

    # Training parameters optimized for M4 16GB
    # 6,349 images total: 5,077 train / 635 val / 637 test
    epochs = 25
    batch_size = 16
    imgsz = 640
    run_name = "yolo11n_15class_master"

    print(f"⚙️ Hyperparameters:")
    print(f"   Epochs:          {epochs}")
    print(f"   Batch Size:      {batch_size}")
    print(f"   Image Resolution: {imgsz}x{imgsz}")
    print(f"   Optimizer:       AdamW (cos_lr=True, lr0=0.002, lrf=0.01)")
    print(f"   Augmentation:    Mosaic=1.0, Mixup=0.1, Fliplr=0.5, CloseMosaic=5")
    print(f"   Device:          {device}")
    print(f"   Output Run:      {OUTPUT_DIR}/{run_name}")
    print("-" * 70)

    try:
        results = model.train(
            data=str(DATASET_YAML),
            epochs=epochs,
            batch=batch_size,
            imgsz=imgsz,
            device=device,
            patience=10,
            save=True,
            save_period=-1,
            project=str(OUTPUT_DIR),
            name=run_name,
            exist_ok=True,
            pretrained=True,
            optimizer="AdamW",
            lr0=0.002,
            lrf=0.01,
            cos_lr=True,
            mosaic=1.0,
            mixup=0.1,
            close_mosaic=5,
            degrees=10.0,
            fliplr=0.5,
            workers=2,
            verbose=True,
            val=True
        )
        print("\n✅ Training finished successfully!")

    except Exception as e:
        print(f"\n❌ Training encountered an error: {e}")
        # If MPS runs into memory or unsupported op, fallback to CPU
        if device == "mps":
            print("🔄 Falling back to CPU training with batch=8...")
            results = model.train(
                data=str(DATASET_YAML),
                epochs=epochs,
                batch=8,
                imgsz=512,
                device="cpu",
                project=str(OUTPUT_DIR),
                name=run_name,
                exist_ok=True,
                workers=1
            )
        else:
            raise e

    # Locate best weights
    best_weights = OUTPUT_DIR / run_name / "weights" / "best.pt"
    if best_weights.exists():
        TARGET_MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(best_weights, TARGET_MODEL_PATH)
        print("\n" + "=" * 70)
        print(f"🎉 BEST 15-CLASS MODEL WEIGHTS EXPORTED:")
        print(f"   Source:      {best_weights}")
        print(f"   Production:  {TARGET_MODEL_PATH} ({TARGET_MODEL_PATH.stat().st_size / 1e6:.2f} MB)")
        print("=" * 70)

        # Run final evaluation on the test split
        print("\n📊 Running formal evaluation on test split...")
        try:
            val_model = YOLO(str(TARGET_MODEL_PATH))
            metrics = val_model.val(data=str(DATASET_YAML), split="test", imgsz=imgsz, device=device)
            print("\nFinal Test Metrics:")
            print(f"   mAP50:    {metrics.box.map50:.4f}")
            print(f"   mAP50-95: {metrics.box.map:.4f}")
            print(f"   Precision: {metrics.box.mp:.4f}")
            print(f"   Recall:    {metrics.box.mr:.4f}")

            summary = {
                "timestamp": datetime.now().isoformat(),
                "model": "YOLO11n-15Class",
                "classes_count": 15,
                "dataset": "waste_15class_master",
                "total_images": 6349,
                "test_map50": round(float(metrics.box.map50), 4),
                "test_map50_95": round(float(metrics.box.map), 4),
                "test_precision": round(float(metrics.box.mp), 4),
                "test_recall": round(float(metrics.box.mr), 4),
                "weights_path": str(TARGET_MODEL_PATH)
            }
            with open(PROJECT_ROOT / "models" / "model_metrics.json", "w") as mf:
                json.dump(summary, mf, indent=2)
            print("Saved metrics summary to models/model_metrics.json")
        except Exception as eval_err:
            print(f"⚠️ Validation evaluation note: {eval_err}")

    print("\n🏁 Master 15-Class Training Pipeline Complete!")

if __name__ == '__main__':
    main()

