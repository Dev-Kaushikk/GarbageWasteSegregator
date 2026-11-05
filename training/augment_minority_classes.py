#!/usr/bin/env python3
"""
Minority Class Augmentation & Dataset Balancer
AI-Based Smart Garbage Waste Segregator

Applies physically valid spatial and photometric transforms to balance:
- Class 14: e_waste (boosts from 17 -> 250+ instances)
- Class 8:  metal_scrap (boosts from 94 -> 280+ instances)
- Class 11: fruit_vegetable_peel (boosts from 253 -> 350+ instances)

Generates exact YOLO bounding box coordinates and updates the master dataset.
"""

import os
import sys
from pathlib import Path
from collections import Counter
from PIL import Image, ImageEnhance, ImageOps

DATASET_ROOT = Path(__file__).resolve().parent.parent / "datasets" / "waste_15class_master"
IMG_TRAIN = DATASET_ROOT / "images" / "train"
LBL_TRAIN = DATASET_ROOT / "labels" / "train"

def transform_box(cls_id, x, y, w, h, transform_type):
    """Accurately transform normalized YOLO coordinates for given geometric operation."""
    x, y, w, h = float(x), float(y), float(w), float(h)
    
    if transform_type == "fliph":
        return cls_id, round(1.0 - x, 6), round(y, 6), round(w, 6), round(h, 6)
    elif transform_type == "flipv":
        return cls_id, round(x, 6), round(1.0 - y, 6), round(w, 6), round(h, 6)
    elif transform_type == "rot90":
        # 90 deg clockwise
        return cls_id, round(1.0 - y, 6), round(x, 6), round(h, 6), round(w, 6)
    elif transform_type == "rot180":
        return cls_id, round(1.0 - x, 6), round(1.0 - y, 6), round(w, 6), round(h, 6)
    elif transform_type == "rot270":
        # 270 deg clockwise (90 counter-clockwise)
        return cls_id, round(y, 6), round(1.0 - x, 6), round(h, 6), round(w, 6)
    else:
        # Photometric (brightness, contrast, color) doesn't move bounding boxes
        return cls_id, round(x, 6), round(y, 6), round(w, 6), round(h, 6)

def apply_image_transform(img, transform_type):
    """Apply spatial or photometric transform to a PIL image."""
    if transform_type == "fliph":
        return ImageOps.mirror(img)
    elif transform_type == "flipv":
        return ImageOps.flip(img)
    elif transform_type == "rot90":
        return img.transpose(Image.ROTATE_270)
    elif transform_type == "rot180":
        return img.transpose(Image.ROTATE_180)
    elif transform_type == "rot270":
        return img.transpose(Image.ROTATE_90)
    elif transform_type == "bright_high":
        return ImageEnhance.Brightness(img).enhance(1.25)
    elif transform_type == "bright_low":
        return ImageEnhance.Brightness(img).enhance(0.75)
    elif transform_type == "contrast_high":
        return ImageEnhance.Contrast(img).enhance(1.30)
    elif transform_type == "contrast_low":
        return ImageEnhance.Contrast(img).enhance(0.80)
    elif transform_type == "color_boost":
        return ImageEnhance.Color(img).enhance(1.40)
    elif transform_type == "fliph_bright":
        mirrored = ImageOps.mirror(img)
        return ImageEnhance.Brightness(mirrored).enhance(1.20)
    elif transform_type == "fliph_contrast":
        mirrored = ImageOps.mirror(img)
        return ImageEnhance.Contrast(mirrored).enhance(1.25)
    elif transform_type == "rot90_bright":
        rotated = img.transpose(Image.ROTATE_270)
        return ImageEnhance.Brightness(rotated).enhance(0.80)
    elif transform_type == "rot180_contrast":
        rotated = img.transpose(Image.ROTATE_180)
        return ImageEnhance.Contrast(rotated).enhance(1.20)
    elif transform_type == "rot270_color":
        rotated = img.transpose(Image.ROTATE_90)
        return ImageEnhance.Color(rotated).enhance(1.35)
    return img

def main():
    print("=" * 65)
    print("🚀 MINORITY CLASS AUGMENTATION & DATASET BALANCER")
    print("=" * 65)

    if not IMG_TRAIN.exists() or not LBL_TRAIN.exists():
        print(f"Error: Dataset train directories not found in {DATASET_ROOT}")
        sys.exit(1)

    # 1. Identify files containing the target rare classes
    # 14: e_waste, 8: metal_scrap, 11: fruit_vegetable_peel
    target_classes = {14, 8, 11}
    images_by_class = {c: [] for c in target_classes}

    for lbl_path in sorted(LBL_TRAIN.glob("*.txt")):
        # Skip previously generated augmented files to avoid exponential compounding
        if "_aug_" in lbl_path.name:
            continue

        img_matches = [
            IMG_TRAIN / f"{lbl_path.stem}.jpg",
            IMG_TRAIN / f"{lbl_path.stem}.jpeg",
            IMG_TRAIN / f"{lbl_path.stem}.png"
        ]
        img_path = None
        for cand in img_matches:
            if cand.exists():
                img_path = cand
                break

        if not img_path:
            continue

        boxes = []
        has_classes = set()
        for line in open(lbl_path).read().splitlines():
            parts = line.strip().split()
            if len(parts) >= 5:
                c_id = int(parts[0])
                boxes.append((c_id, float(parts[1]), float(parts[2]), float(parts[3]), float(parts[4])))
                if c_id in target_classes:
                    has_classes.add(c_id)

        for c_id in has_classes:
            images_by_class[c_id].append((img_path, lbl_path, boxes))

    print(f"Original unique train images:")
    print(f"  Class 14 (e_waste)              : {len(images_by_class[14])} images")
    print(f"  Class 8  (metal_scrap)          : {len(images_by_class[8])} images")
    print(f"  Class 11 (fruit_vegetable_peel) : {len(images_by_class[11])} images")

    # Define augmentation schedules
    # e_waste: 15 transforms per image (17 * 15 = 255 new images)
    ewaste_transforms = [
        "fliph", "flipv", "rot90", "rot180", "rot270",
        "bright_high", "bright_low", "contrast_high", "contrast_low", "color_boost",
        "fliph_bright", "fliph_contrast", "rot90_bright", "rot180_contrast", "rot270_color"
    ]

    # metal_scrap: 3 transforms per image (64 * 3 = 192 new images)
    scrap_transforms = ["fliph", "bright_high", "contrast_high"]

    # fruit_peel: 1 transform per image for half of images (~100 new images)
    peel_transforms = ["fliph"]

    created_counts = Counter()

    # Augment e_waste
    print("\n📦 Generating augmented variations for Class 14 (e_waste)...")
    for img_p, lbl_p, boxes in images_by_class[14]:
        try:
            with Image.open(img_p) as orig_img:
                rgb_img = orig_img.convert('RGB')
                for t_name in ewaste_transforms:
                    aug_stem = f"{img_p.stem}_aug_{t_name}"
                    dst_img = IMG_TRAIN / f"{aug_stem}.jpg"
                    dst_lbl = LBL_TRAIN / f"{aug_stem}.txt"

                    # Transform image
                    trans_img = apply_image_transform(rgb_img, t_name)
                    trans_img.save(dst_img, quality=92)

                    # Transform boxes
                    base_geo = "rot90" if "rot90" in t_name else ("rot180" if "rot180" in t_name else ("rot270" if "rot270" in t_name else ("fliph" if "fliph" in t_name else ("flipv" if "flipv" in t_name else "none"))))
                    with open(dst_lbl, 'w') as out_f:
                        for cid, x, y, w, h in boxes:
                            nc, nx, ny, nw, nh = transform_box(cid, x, y, w, h, base_geo)
                            out_f.write(f"{nc} {nx} {ny} {nw} {nh}\n")
                            created_counts[nc] += 1
        except Exception as e:
            print(f"Warning: Failed processing {img_p.name}: {e}")

    # Augment metal_scrap
    print("⚙️ Generating augmented variations for Class 8 (metal_scrap)...")
    for img_p, lbl_p, boxes in images_by_class[8]:
        try:
            with Image.open(img_p) as orig_img:
                rgb_img = orig_img.convert('RGB')
                for t_name in scrap_transforms:
                    aug_stem = f"{img_p.stem}_aug_{t_name}"
                    dst_img = IMG_TRAIN / f"{aug_stem}.jpg"
                    dst_lbl = LBL_TRAIN / f"{aug_stem}.txt"

                    trans_img = apply_image_transform(rgb_img, t_name)
                    trans_img.save(dst_img, quality=92)

                    base_geo = "fliph" if "fliph" in t_name else "none"
                    with open(dst_lbl, 'w') as out_f:
                        for cid, x, y, w, h in boxes:
                            nc, nx, ny, nw, nh = transform_box(cid, x, y, w, h, base_geo)
                            out_f.write(f"{nc} {nx} {ny} {nw} {nh}\n")
                            created_counts[nc] += 1
        except Exception as e:
            print(f"Warning: Failed processing {img_p.name}: {e}")

    # Augment fruit_peel
    print("🍌 Generating augmented variations for Class 11 (fruit_vegetable_peel)...")
    for img_p, lbl_p, boxes in images_by_class[11][:100]:
        try:
            with Image.open(img_p) as orig_img:
                rgb_img = orig_img.convert('RGB')
                for t_name in peel_transforms:
                    aug_stem = f"{img_p.stem}_aug_{t_name}"
                    dst_img = IMG_TRAIN / f"{aug_stem}.jpg"
                    dst_lbl = LBL_TRAIN / f"{aug_stem}.txt"

                    trans_img = apply_image_transform(rgb_img, t_name)
                    trans_img.save(dst_img, quality=92)

                    with open(dst_lbl, 'w') as out_f:
                        for cid, x, y, w, h in boxes:
                            nc, nx, ny, nw, nh = transform_box(cid, x, y, w, h, "fliph")
                            out_f.write(f"{nc} {nx} {ny} {nw} {nh}\n")
                            created_counts[nc] += 1
        except Exception as e:
            print(f"Warning: Failed processing {img_p.name}: {e}")

    # Remove stale label caches so YOLO recalculates dataset distribution
    for cache_p in DATASET_ROOT.rglob("*.cache"):
        try:
            cache_p.unlink()
            print(f"Deleted cache: {cache_p.name}")
        except Exception:
            pass

    # Count final dataset statistics
    final_counts = Counter()
    for lbl_f in LBL_TRAIN.glob("*.txt"):
        for line in open(lbl_f).read().splitlines():
            p = line.strip().split()
            if p:
                final_counts[int(p[0])] += 1

    classes = [
        "plastic_bottle", "plastic_wrapper", "plastic_bag", "plastic_container",
        "paper", "cardboard_carton", "glass", "metal_can", "metal_scrap",
        "styrofoam", "food_waste", "fruit_vegetable_peel", "garden_waste",
        "textile", "e_waste"
    ]

    total_train_images = len(list(IMG_TRAIN.glob("*.*")))

    print("\n" + "=" * 65)
    print(f"✅ BALANCED DATASET SUMMARY (Total Train Images: {total_train_images})")
    print("=" * 65)
    for idx, cname in enumerate(classes):
        print(f"  Class {idx:2d}: {cname:22s} -> {final_counts[idx]:5d} objects")
    print("=" * 65)

if __name__ == "__main__":
    main()

