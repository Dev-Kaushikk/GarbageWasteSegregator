#!/usr/bin/env python3
"""
AI-Based Smart Garbage Waste Segregator
Offline Resume Training Script (Epoch 31 -> Epoch 100)
Architecture: YOLO11s | Dataset: waste_15class_master | Imgsz: 800px

Instructions:
  1. Make sure you have python installed.
  2. Install dependencies:
       pip install ultralytics torch torchvision
  3. Run this script:
       python resume_offline_training.py
"""

import os
import sys
import argparse
from pathlib import Path

def get_device():
    import torch
    if torch.cuda.is_available():
        gpu_name = torch.cuda.get_device_name(0)
        gpu_mem = torch.cuda.get_device_properties(0).total_memory / (1024**3)
        print(f"⚡ NVIDIA GPU Detected: {gpu_name} ({gpu_mem:.1f} GB VRAM)")
        return 0, gpu_mem
    elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        print("⚡ Apple Silicon Metal Performance Shaders (MPS) Detected")
        return "mps", 16.0
    else:
        print("⚠️ No dedicated GPU detected. Using CPU (Warning: CPU training is slow).")
        return "cpu", 0.0

def find_file(name, search_dirs):
    for d in search_dirs:
        p = Path(d)
        if (p / name).exists():
            return (p / name).resolve()
        # Search subdirectories
        matches = list(p.glob(f"**/{name}"))
        if matches:
            return matches[0].resolve()
    return None

def main():
    parser = argparse.ArgumentParser(description="Resume YOLO11s 15-Class Training Offline")
    parser.add_argument("--weights", type=str, default=None, help="Path to last.pt checkpoint")
    parser.add_argument("--data", type=str, default=None, help="Path to data.yaml")
    parser.add_argument("--batch", type=int, default=None, help="Batch size (default: auto based on VRAM)")
    parser.add_argument("--imgsz", type=int, default=800, help="Image size (default: 800)")
    parser.add_argument("--workers", type=int, default=4, help="Dataloader workers (default: 4)")
    args = parser.parse_args()

    print("=" * 70)
    print("♻️  WASTE SEGREGATOR AI - RESUME OFFLINE TRAINING (EPOCH 31 -> 100)")
    print("=" * 70)

    # 1. Locate last.pt
    search_dirs = [".", "..", "runs", "models", "weights"]
    weights_path = Path(args.weights) if args.weights else find_file("last.pt", search_dirs)
    if not weights_path or not weights_path.exists():
        print("❌ Could not find 'last.pt' checkpoint!")
        print("   Please place 'last.pt' in the current folder or pass --weights path/to/last.pt")
        sys.exit(1)
    print(f"✅ Found Checkpoint: {weights_path} ({weights_path.stat().st_size / 1e6:.1f} MB)")

    # 2. Locate data.yaml
    yaml_search = [".", "..", "waste_15class_master", "datasets/waste_15class_master"]
    data_path = Path(args.data) if args.data else find_file("data.yaml", yaml_search)
    if not data_path or not data_path.exists():
        print("❌ Could not find 'data.yaml'!")
        print("   Please make sure the 'waste_15class_master' folder is unzipped here,")
        print("   or pass --data path/to/data.yaml")
        sys.exit(1)
    print(f"✅ Found Dataset:    {data_path}")

    # Ensure dataset path in data.yaml matches its actual parent directory
    try:
        import re
        dataset_dir = data_path.parent.resolve()
        with open(data_path, "r") as f:
            yaml_text = f.read()
        fixed_yaml = re.sub(r"path:\s*.*", f"path: {dataset_dir}", yaml_text)
        with open(data_path, "w") as f:
            f.write(fixed_yaml)
        print(f"✅ Configured data.yaml path: {dataset_dir}")
    except Exception as e:
        print(f"⚠️ Note on data.yaml: {e}")

    # 3. Detect Device & Optimal Batch
    device, vram = get_device()
    
    # Auto-adjust batch size based on available VRAM if not specified
    if args.batch is not None:
        batch_size = args.batch
    else:
        if device == "cpu":
            batch_size = 4
        elif vram >= 14.0:
            batch_size = 16  # Fits on 16GB VRAM (Tesla T4, RTX 4080/3090)
        elif vram >= 8.0:
            batch_size = 8   # Fits comfortably on 8GB VRAM (RTX 3070, 4060)
        elif vram >= 5.0:
            batch_size = 6   # Fits on 6GB VRAM (RTX 3060 Laptop, 2060)
        else:
            batch_size = 4   # Fits on 4GB VRAM (RTX 3050 Laptop)

    print(f"⚙️ Config: Device={device} | Batch={batch_size} | Imgsz={args.imgsz} | Target Epochs=100")
    print("-" * 70)

    try:
        from ultralytics import YOLO
    except ImportError:
        print("❌ Ultralytics is not installed.")
        print("   Run: pip install ultralytics torch torchvision")
        sys.exit(1)

    print(f"\n🔄 Loading checkpoint and preparing resume from Epoch 31...")
    model = YOLO(str(weights_path))

    try:
        results = model.train(
            data=str(data_path),
            resume=True,
            device=device,
            batch=batch_size,
            imgsz=args.imgsz,
            workers=args.workers,
            save=True,
            save_period=5
        )
        print("\n" + "=" * 70)
        print("🎉 TRAINING COMPLETE (100/100 Epochs)!")
        print("=" * 70)
        print("Find your newly trained flagship weights in:")
        print("👉 runs/detect/.../weights/best.pt")
        print("Send 'best.pt' and 'results.csv' back to copy into the project!")

    except Exception as e:
        err_msg = str(e)
        if "out of memory" in err_msg.lower() or "cuda oom" in err_msg.lower():
            print("\n❌ CUDA Out of Memory Error!")
            print(f"   Batch size {batch_size} was too large for your GPU VRAM.")
            half_batch = max(2, batch_size // 2)
            print(f"👉 Please retry with a smaller batch size:")
            print(f"   python resume_offline_training.py --batch {half_batch}")
        else:
            print(f"\n❌ Training failed with error: {e}")
            raise e

if __name__ == "__main__":
    main()

