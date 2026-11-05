#!/usr/bin/env python3
"""
AI-Based Smart Garbage Waste Segregator
Targeted Class Balancer & Dataset Booster (Option B)

Pushes underrepresented minority classes above 1,000+ instances:
- Class 8:  metal_scrap          (from 376 -> 1,100+ instances)
- Class 14: e_waste              (from 272 -> 1,000+ instances)
- Class 12: garden_waste         (from 755 -> 1,400+ instances)
- Class 3:  plastic_container    (from 635 -> 1,300+ instances)
- Class 11: fruit_vegetable_peel (from 506 -> 1,000+ instances)

Features:
- Exact geometric bounding box coordinate transformations (Flips, 90/180/270 rotations)
- Photometric transforms (Brightness, Contrast, Color enhancement)
- No bounding box clipping or label corruption
- Automatic removal of stale YOLO label cache files
"""

import os
import sys
from pathlib import Path
from collections import Counter, defaultdict
from PIL import Image, ImageEnhance, ImageOps

DATASET_ROOT = Path(__file__).resolve().parent.parent / "datasets" / "waste_15class_master"
IMG_TRAIN = DATASET_ROOT / "images" / "train"
LBL_TRAIN = DATASET_ROOT / "labels" / "train"

CLASS_NAMES = [
    "plastic_bottle", "plastic_wrapper", "plastic_bag", "plastic_container",
    "paper", "cardboard_carton", "glass", "metal_can", "metal_scrap",
    "styrofoam", "food_waste", "fruit_vegetable_peel", "garden_waste",
    "textile", "e_waste"
]

def transform_box(cls_id, x, y, w, h, transform_type):
    """Accurately transform normalized YOLO coordinates for geometric operations."""
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
        # Photometric (brightness, contrast, color) does not alter bounding box geometry
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
        return ImageEnhance.Brightness(img).enhance(0.80)
    elif transform_type == "contrast_high":
        return ImageEnhance.Contrast(img).enhance(1.25)
    elif transform_type == "contrast_low":
        return ImageEnhance.Contrast(img).enhance(0.85)
    elif transform_type == "color_boost":
        return ImageEnhance.Color(img).enhance(1.30)
    elif transform_type == "fliph_bright":
        mirrored = ImageOps.mirror(img)
        return ImageEnhance.Brightness(mirrored).enhance(1.15)
    elif transform_type == "fliph_contrast":
        mirrored = ImageOps.mirror(img)
        return ImageEnhance.Contrast(mirrored).enhance(1.20)
    elif transform_type == "rot90_bright":
        rotated = img.transpose(Image.ROTATE_270)
        return ImageEnhance.Brightness(rotated).enhance(0.85)
    return img

def main():
    print("=" * 70)
    print("🚀 TARGETED CLASS BALANCER & DATASET BOOSTER")
    print("   AI-Based Smart Garbage Waste Segregator")
    print("=" * 70)

    if not IMG_TRAIN.exists() or not LBL_TRAIN.exists():
        print(f"❌ Error: Dataset directories not found at {DATASET_ROOT}")
        sys.exit(1)

    # Count initial distribution
    initial_counts = Counter()
    for lbl_f in LBL_TRAIN.glob("*.txt"):
        for line in open(lbl_f).read().splitlines():
            parts = line.strip().split()
            if parts:
                initial_counts[int(parts[0])] += 1

    print("\n📊 Initial Training Distribution:")
    for idx, name in enumerate(CLASS_NAMES):
        tag = "🔴 LOW" if initial_counts[idx] < 600 else "🟢 OK"
        print(f"  [{idx:2d}] {name:22s}: {initial_counts[idx]:5d} objects ({tag})")

    # Define targeted transform policies per class
    target_policies = {
        8: ["fliph", "fliph_bright", "contrast_high", "rot90"],             # metal_scrap: 4 transforms
        14: ["fliph", "fliph_bright", "contrast_high", "rot90", "rot180"],   # e_waste: 5 transforms
        12: ["fliph", "contrast_high", "bright_low"],                       # garden_waste: 3 transforms
        3: ["fliph", "contrast_high"],                                      # plastic_container: 2 transforms
        11: ["fliph", "bright_high"]                                        # fruit_vegetable_peel: 2 transforms
    }

    # Find unique original images containing target classes
    images_by_class = defaultdict(list)
    for lbl_path in sorted(LBL_TRAIN.glob("*.txt")):
        if "_aug_" in lbl_path.name or "_boost_" in lbl_path.name:
            continue

        img_cand = None
        for ext in [".jpg", ".jpeg", ".png", ".webp"]:
            c = IMG_TRAIN / f"{lbl_path.stem}{ext}"
            if c.exists():
                img_cand = c
                break

        if not img_cand:
            continue

        boxes = []
        present_classes = set()
        for line in open(lbl_path).read().splitlines():
            p = line.strip().split()
            if len(p) >= 5:
                cid = int(p[0])
                boxes.append((cid, float(p[1]), float(p[2]), float(p[3]), float(p[4])))
                if cid in target_policies:
                    present_classes.add(cid)

        for cid in present_classes:
            images_by_class[cid].append((img_cand, lbl_path, boxes))

    print("\n🔍 Found Source Images for Targeted Boosting:")
    for cid in target_policies:
        print(f"  Class {cid:2d} ({CLASS_NAMES[cid]:22s}): {len(images_by_class[cid])} unique images")

    # Apply targeted augmentations
    created_images = 0
    added_boxes = Counter()

    for cid, transforms in target_policies.items():
        print(f"\n⚡ Boosting Class {cid:2d} ({CLASS_NAMES[cid]}) with {len(transforms)} transformations...")
        for img_path, lbl_path, boxes in images_by_class[cid]:
            try:
                with Image.open(img_path) as orig_img:
                    rgb_img = orig_img.convert("RGB")
                    for t_name in transforms:
                        aug_stem = f"{img_path.stem}_boost_{t_name}"
                        dst_img = IMG_TRAIN / f"{aug_stem}.jpg"
                        dst_lbl = LBL_TRAIN / f"{aug_stem}.txt"

                        # Skip if already exists
                        if dst_img.exists() and dst_lbl.exists():
                            continue

                        # Transform image
                        aug_img = apply_image_transform(rgb_img, t_name)
                        aug_img.save(dst_img, quality=92)

                        # Determine geometric box mapping
                        geo_mode = "fliph" if "fliph" in t_name else (
                            "rot90" if "rot90" in t_name else (
                                "rot180" if "rot180" in t_name else "none"
                            )
                        )

                        with open(dst_lbl, "w") as out_f:
                            for b_cid, bx, by, bw, bh in boxes:
                                nc, nx, ny, nw, nh = transform_box(b_cid, bx, by, bw, bh, geo_mode)
                                out_f.write(f"{nc} {nx} {ny} {nw} {nh}\n")
                                added_boxes[nc] += 1

                        created_images += 1
            except Exception as e:
                print(f"⚠️ Warning on {img_path.name}: {e}")

    # Remove stale YOLO cache files
    print("\n🧹 Clearing stale YOLO label cache files...")
    for cache_f in DATASET_ROOT.rglob("*.cache"):
        try:
            cache_f.unlink()
            print(f"  Deleted: {cache_f}")
        except Exception:
            pass

    # Count final distribution
    final_counts = Counter()
    for lbl_f in LBL_TRAIN.glob("*.txt"):
        for line in open(lbl_f).read().splitlines():
            p = line.strip().split()
            if p:
                final_counts[int(p[0])] += 1

    total_train_images = len(list(IMG_TRAIN.glob("*.*")))

    print("\n" + "=" * 70)
    print(f"🎉 DATASET BOOSTING COMPLETE! (Total Train Images: {total_train_images})")
    print(f"   Generated {created_images} new targeted high-quality training images")
    print("=" * 70)
    print("Class ID | Class Name              | Before  | After   | Gain")
    print("-" * 70)
    for idx, name in enumerate(CLASS_NAMES):
        before = initial_counts[idx]
        after = final_counts[idx]
        diff = after - before
        gain_str = f"+{diff}" if diff > 0 else "0"
        print(f"  [{idx:2d}]   | {name:23s} | {before:7d} | {after:7d} | {gain_str:>6s}")
    print("=" * 70)

if __name__ == "__main__":
    main()

