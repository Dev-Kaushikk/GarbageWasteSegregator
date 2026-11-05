#!/usr/bin/env python3
"""
AI-Based Smart Garbage Waste Segregator
Balanced Dataset Fine-Tuning Pipeline (Target: 75% - 82%+ mAP50)

Fine-tunes the 100-Epoch Flagship model (yolo11n_15class_best.pt) on the newly
balanced master dataset (8,718 images, 32,900+ annotations with 1,000+ objects
per minority class).
"""

import os
import sys
import argparse
from pathlib import Path
from datetime import datetime

# Configure Ultralytics cache directory
os.environ.setdefault("YOLO_CONFIG_DIR", "/tmp/ultralytics")

import torch
from ultralytics import YOLO

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATASET_YAML = PROJECT_ROOT / "datasets" / "waste_15class_master" / "data.yaml"
BASE_WEIGHTS = PROJECT_ROOT / "models" / "yolo11n_15class_best.pt"
OUTPUT_DIR = PROJECT_ROOT / "runs" / "detect" / "runs" / "garbage"

def select_device():
    if torch.backends.mps.is_available() and torch.backends.mps.is_built():
        print("⚡ Hardware Acceleration: Apple Silicon Metal Performance Shaders (MPS)")
        return "mps"
    elif torch.cuda.is_available():
        gpu_name = torch.cuda.get_device_name(0)
        print(f"⚡ Hardware Acceleration: NVIDIA CUDA ({gpu_name})")
        return 0
    print("⚠️ Hardware Acceleration: Standard CPU")
    return "cpu"

def main():
    parser = argparse.ArgumentParser(description="Fine-tune YOLO11 on balanced 15-class waste dataset")
    parser.add_argument("--epochs", type=int, default=30, help="Number of fine-tuning epochs (default: 30)")
    parser.add_argument("--batch", type=int, default=16, help="Batch size (default: 16)")
    parser.add_argument("--imgsz", type=int, default=640, help="Image resolution (default: 640)")
    parser.add_argument("--weights", type=str, default=str(BASE_WEIGHTS), help="Base weights checkpoint")
    parser.add_argument("--device", type=str, default=None, help="Device to train on (auto / mps / 0 / cpu)")
    args = parser.parse_args()

    print("=" * 70)
    print("🚀 BALANCED DATASET FINE-TUNING PIPELINE (Target: 75% - 82%+ mAP50)")
    print("=" * 70)
    print(f"Timestamp:      {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Dataset YAML:   {DATASET_YAML}")
    print(f"Base Weights:   {args.weights}")
    print(f"Target Epochs:  {args.epochs}")
    print(f"Batch Size:     {args.batch}")
    print(f"Resolution:     {args.imgsz}x{args.imgsz}")

    device = args.device if args.device else select_device()
    print(f"Device:         {device}")
    print("-" * 70)

    if not Path(args.weights).exists():
        print(f"❌ Base weights not found: {args.weights}")
        sys.exit(1)

    if not DATASET_YAML.exists():
        print(f"❌ Dataset YAML not found: {DATASET_YAML}")
        sys.exit(1)

    # Initialize model from best flagship checkpoint
    print(f"\n📦 Loading pretrained flagship weights from {args.weights}...")
    model = YOLO(args.weights)

    run_name = f"yolo11n_15class_balanced_boost"

    print("\n🔥 Starting fine-tuning with conservative LR (lr0=0.0005, AdamW)...")
    results = model.train(
        data=str(DATASET_YAML),
        epochs=args.epochs,
        batch=args.batch,
        imgsz=args.imgsz,
        device=device,
        optimizer="AdamW",
        lr0=0.0005,         # Lower learning rate preserves master weights while learning rare classes
        lrf=0.01,
        cos_lr=True,
        mosaic=0.5,
        mixup=0.1,
        close_mosaic=5,
        degrees=10.0,
        fliplr=0.5,
        workers=2 if str(device) == "mps" else 8,
        project=str(OUTPUT_DIR),
        name=run_name,
        exist_ok=True,
        save=True,
        save_period=5,
        val=True,
        plots=True
    )

    best_pt = OUTPUT_DIR / run_name / "weights" / "best.pt"
    print("\n" + "=" * 70)
    print("🎉 FINE-TUNING COMPLETE!")
    print(f"   Best weights saved to: {best_pt}")
    print("=" * 70)

if __name__ == "__main__":
    main()

