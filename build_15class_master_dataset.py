#!/usr/bin/env python3
"""
Master 15-Class Waste Dataset Builder for AI-Based Smart Garbage Waste Segregator
Consolidates and balances:
1. datasets/taco_yolo
2. ~/Downloads/waste_datasets_extra/Yolo V7 Trash 03-22-2023.v2i.yolov8
3. ~/Downloads/waste_datasets_extra/YOLO Waste Detection.v2-add-new-photos.yolov8
4. ~/Desktop/TACO/data/annotations.json (batteries & metal items)
"""
import os
import sys
import shutil
import random
from pathlib import Path
from collections import Counter, defaultdict
import yaml

PROJECT_ROOT = Path("/Users/devkaushik/Desktop/GarbageWasteSegregator")
OUTPUT_DIR = PROJECT_ROOT / "datasets" / "waste_15class_master"
EXTRA_DIR = Path.home() / "Downloads" / "waste_datasets_extra"
TACO_YOLO = PROJECT_ROOT / "datasets" / "taco_yolo"

TARGET_CLASSES = [
    "plastic_bottle",        # 0
    "plastic_wrapper",       # 1
    "plastic_bag",           # 2
    "plastic_container",     # 3
    "paper",                 # 4
    "cardboard_carton",      # 5
    "glass",                 # 6
    "metal_can",             # 7
    "metal_scrap",           # 8
    "styrofoam",             # 9
    "food_waste",            # 10
    "fruit_vegetable_peel",  # 11
    "garden_waste",          # 12
    "textile",               # 13
    "e_waste",               # 14
]

# Mapping for Yolo V7 Trash (27 classes)
V7_MAPPING = {
    0: 7,   # Cans -> metal_can
    1: 5,   # Cardboard -> cardboard_carton
    2: 6,   # Colored Glass Bottles -> glass
    3: 6,   # Colored-Glass-Bottles -> glass
    4: 13,  # Face Mask -> textile
    5: 13,  # Face-Mask -> textile
    6: 6,   # Glass Bottle -> glass
    7: 4,   # Paper Bag -> paper
    8: 4,   # Paper Cup -> paper
    9: 4,   # Paper-Cup -> paper
    10: 4,  # PaperBag -> paper
    11: 5,  # Paperboard -> cardboard_carton
    12: 11, # Peel -> fruit_vegetable_peel
    13: 12, # Pile of Leaves -> garden_waste
    14: 2,  # Plastic Bag -> plastic_bag
    15: 0,  # Plastic Bottle -> plastic_bottle
    16: 3,  # Plastic Cup -> plastic_container
    17: 1,  # Plastic Wrapper -> plastic_wrapper
    18: 2,  # Plastic-Bag -> plastic_bag
    19: 0,  # Plastic-Bottle -> plastic_bottle
    20: 1,  # Plastic-Wrapper -> plastic_wrapper
    21: 3,  # PlasticCups -> plastic_container
    22: 13, # Rags -> textile
    23: 9,  # Styrofoam -> styrofoam
    24: 5,  # Tetra Pack -> cardboard_carton
    25: 5,  # Tetra Pak -> cardboard_carton
    26: 5,  # Tetra-Pak -> cardboard_carton
}

# Mapping for YOLO Waste Detection (10 classes)
WASTE_DETECTION_MAPPING = {
    0: 7,   # Aluminum can -> metal_can
    1: 5,   # Cardboard -> cardboard_carton
    2: 3,   # Container for household chemicals -> plastic_container
    3: 6,   # Glass bottle -> glass
    4: 10,  # Organic -> food_waste
    5: 4,   # Paper -> paper
    6: 2,   # Plastic bag -> plastic_bag
    7: 0,   # Plastic bottle -> plastic_bottle
    8: 3,   # Plastic cup -> plastic_container
    9: 7,   # Tin -> metal_can
}

# Mapping for TACO YOLO (10 classes)
TACO_YOLO_MAPPING = {
    0: 0,   # plastic_bottle -> plastic_bottle
    1: 1,   # plastic_wrapper -> plastic_wrapper
    2: 2,   # plastic_film_bag -> plastic_bag
    3: 3,   # plastic_container -> plastic_container
    4: 4,   # paper -> paper
    5: 5,   # cardboard_carton -> cardboard_carton
    6: 6,   # glass -> glass
    7: 7,   # metal_can -> metal_can
    8: 8,   # metal_small_item -> metal_scrap
    9: 9,   # styrofoam -> styrofoam
}

def clean_box(x, y, w, h):
    x = max(0.001, min(0.999, float(x)))
    y = max(0.001, min(0.999, float(y)))
    w = max(0.001, min(0.999, float(w)))
    h = max(0.001, min(0.999, float(h)))
    # Clip width/height so box stays inside [0, 1]
    if x - w / 2 < 0:
        w = 2 * x
    if x + w / 2 > 1:
        w = 2 * (1 - x)
    if y - h / 2 < 0:
        h = 2 * y
    if y + h / 2 > 1:
        h = 2 * (1 - y)
    return round(x, 6), round(y, 6), round(w, 6), round(h, 6)

def collect_records():
    records = []  # list of dict(source, img_path, boxes=[(target_cls, x, y, w, h)])

    # 1. TACO YOLO
    if TACO_YOLO.exists():
        for split in ['train', 'val', 'test']:
            img_dir = TACO_YOLO / 'images' / split
            lbl_dir = TACO_YOLO / 'labels' / split
            if not img_dir.exists() or not lbl_dir.exists():
                continue
            for img_p in img_dir.glob('*.*'):
                lbl_p = lbl_dir / f"{img_p.stem}.txt"
                if not lbl_p.exists():
                    continue
                boxes = []
                for line in open(lbl_p).read().splitlines():
                    parts = line.strip().split()
                    if len(parts) >= 5:
                        src_c = int(parts[0])
                        tgt_c = TACO_YOLO_MAPPING.get(src_c)
                        if tgt_c is not None:
                            x, y, w, h = clean_box(parts[1], parts[2], parts[3], parts[4])
                            boxes.append((tgt_c, x, y, w, h))
                if boxes:
                    records.append({'source': 'taco', 'img_path': img_p, 'boxes': boxes})

    # 2. Yolo V7 Trash
    v7_root = EXTRA_DIR / "Yolo V7 Trash 03-22-2023.v2i.yolov8"
    if v7_root.exists():
        for split in ['train', 'valid', 'test']:
            img_dir = v7_root / split / 'images'
            lbl_dir = v7_root / split / 'labels'
            if not img_dir.exists() or not lbl_dir.exists():
                continue
            for img_p in img_dir.glob('*.*'):
                lbl_p = lbl_dir / f"{img_p.stem}.txt"
                if not lbl_p.exists():
                    continue
                boxes = []
                for line in open(lbl_p).read().splitlines():
                    parts = line.strip().split()
                    if len(parts) >= 5:
                        src_c = int(parts[0])
                        tgt_c = V7_MAPPING.get(src_c)
                        if tgt_c is not None:
                            x, y, w, h = clean_box(parts[1], parts[2], parts[3], parts[4])
                            boxes.append((tgt_c, x, y, w, h))
                if boxes:
                    records.append({'source': 'v7_trash', 'img_path': img_p, 'boxes': boxes})

    # 3. YOLO Waste Detection
    wd_root = EXTRA_DIR / "YOLO Waste Detection.v2-add-new-photos.yolov8"
    if wd_root.exists():
        for split in ['train', 'valid', 'test']:
            img_dir = wd_root / split / 'images'
            lbl_dir = wd_root / split / 'labels'
            if not img_dir.exists() or not lbl_dir.exists():
                continue
            for img_p in img_dir.glob('*.*'):
                lbl_p = lbl_dir / f"{img_p.stem}.txt"
                if not lbl_p.exists():
                    continue
                boxes = []
                for line in open(lbl_p).read().splitlines():
                    parts = line.strip().split()
                    if len(parts) >= 5:
                        src_c = int(parts[0])
                        tgt_c = WASTE_DETECTION_MAPPING.get(src_c)
                        if tgt_c is not None:
                            x, y, w, h = clean_box(parts[1], parts[2], parts[3], parts[4])
                            boxes.append((tgt_c, x, y, w, h))
                if boxes:
                    records.append({'source': 'wd_waste', 'img_path': img_p, 'boxes': boxes})

    return records

def balance_and_build(records):
    print(f"Total available candidate images with valid labels: {len(records)}")

    # Index records by classes they contain
    class_to_records = defaultdict(list)
    for idx, r in enumerate(records):
        classes_in_image = set(c for c, _, _, _, _ in r['boxes'])
        for c in classes_in_image:
            class_to_records[c].append(idx)

    # Print initial distribution
    print("\nInitial class presence (images containing class):")
    for c_id, name in enumerate(TARGET_CLASSES):
        print(f"  {c_id:2}: {name:22} -> {len(class_to_records[c_id]):5} images")

    # Smart balancing:
    # Always include all images with rare classes: [8, 9, 10, 11, 12, 13, 14]
    rare_classes = {8, 9, 10, 11, 12, 13, 14}
    selected_indices = set()

    for rc in rare_classes:
        for idx in class_to_records[rc]:
            selected_indices.add(idx)

    print(f"\nAfter adding all rare-class images: {len(selected_indices)} unique images selected.")

    # For common classes [0, 1, 2, 3, 4, 5, 6, 7], sample up to 500 images each
    random.seed(42)
    common_classes = [0, 1, 2, 3, 4, 5, 6, 7]
    for cc in common_classes:
        candidates = class_to_records[cc]
        # Filter candidates not yet selected
        unselected = [i for i in candidates if i not in selected_indices]
        sample_size = min(400, len(unselected))
        if sample_size > 0:
            picked = random.sample(unselected, sample_size)
            selected_indices.update(picked)

    print(f"Total balanced dataset selection: {len(selected_indices)} images.")

    selected_records = [records[i] for i in sorted(selected_indices)]
    random.shuffle(selected_records)

    # Split: 80% train, 10% val, 10% test
    n = len(selected_records)
    n_train = int(n * 0.80)
    n_val = int(n * 0.10)
    splits = {
        'train': selected_records[:n_train],
        'val': selected_records[n_train:n_train + n_val],
        'test': selected_records[n_train + n_val:]
    }

    # Prepare directories
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)

    for s in ['train', 'val', 'test']:
        (OUTPUT_DIR / 'images' / s).mkdir(parents=True, exist_ok=True)
        (OUTPUT_DIR / 'labels' / s).mkdir(parents=True, exist_ok=True)

    obj_counter = Counter()

    for s, recs in splits.items():
        print(f"Writing {s} split ({len(recs)} images)...")
        for i, r in enumerate(recs):
            src_img = r['img_path']
            ext = src_img.suffix.lower()
            dst_stem = f"{r['source']}_{src_img.stem}_{i:05d}"
            dst_img = OUTPUT_DIR / 'images' / s / f"{dst_stem}{ext}"
            dst_lbl = OUTPUT_DIR / 'labels' / s / f"{dst_stem}.txt"

            # Copy image
            shutil.copy2(src_img, dst_img)

            # Write label
            with open(dst_lbl, 'w') as lf:
                for c, x, y, w, h in r['boxes']:
                    lf.write(f"{c} {x} {y} {w} {h}\n")
                    obj_counter[c] += 1

    # Write data.yaml
    data_yaml = {
        'path': str(OUTPUT_DIR),
        'train': 'images/train',
        'val': 'images/val',
        'test': 'images/test',
        'nc': len(TARGET_CLASSES),
        'names': TARGET_CLASSES
    }
    with open(OUTPUT_DIR / 'data.yaml', 'w') as yf:
        yaml.dump(data_yaml, yf, default_flow_style=False, sort_keys=False)

    print("\n" + "=" * 65)
    print("✅ MASTER 15-CLASS DATASET CREATED SUCCESSFULLY")
    print("=" * 65)
    print(f"Location: {OUTPUT_DIR}")
    print(f"Total Images: {len(selected_records)}")
    print(f"  Train: {len(splits['train'])}")
    print(f"  Val:   {len(splits['val'])}")
    print(f"  Test:  {len(splits['test'])}")
    print("\nFinal Object Counts by Class:")
    for c_id, name in enumerate(TARGET_CLASSES):
        print(f"  {c_id:2}: {name:22} | {obj_counter[c_id]:5} objects")
    print("=" * 65)

if __name__ == '__main__':
    print("🚀 Collecting candidate waste records across datasets...")
    records = collect_records()
    balance_and_build(records)

