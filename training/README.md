# Model Training & Dataset Pipeline

This directory contains scripts and notebooks for dataset consolidation, synthetic augmentation, cloud/local model training, and performance benchmarking for the **WasteSegregator AI** 15-class taxonomy.

## Directory Contents

| Script / File | Description | Execution Environment |
|---|---|---|
| `build_15class_master_dataset.py` | Consolidates TACO, Roboflow subsets, and annotations into the unified 15-class master dataset (`datasets/waste_15class_master/`). | Local / Prep |
| `augment_minority_classes.py` | Geometric & photometric augmentations (horizontal flip, brightness, noise) for underrepresented categories (e-waste, peels, metals). | Local / Prep |
| `boost_dataset_balance.py` | Class-aware rebalancing pipeline that generates additional augmented samples to reach equal class distribution. | Local / Prep |
| `package_dataset.py` | Fast archive utility that packages the balanced dataset into a compressed zip file for cloud GPU uploads. | Local / Prep |
| `train_15class_master.py` | Master training runner for YOLO11n models on local hardware (Apple Silicon MPS / NVIDIA CUDA). | Local GPU/MPS |
| `finetune_balanced_model.py` | Fine-tunes pre-trained weights for 30 epochs with reduced learning rate on the rebalanced dataset. | Local GPU/MPS |
| `resume_offline_training.py` | Checkpoint recovery script to resume interrupted training jobs seamlessly from `last.pt`. | Local / Remote |
| `generate_kaggle_notebook.py` | Programmatic generator for Kaggle Jupyter training notebooks with dependencies and hyperparameter configs. | Local Utility |
| `kaggle_train_script.py` | Automated training script executed inside remote cloud GPU environments (Kaggle P100 / T4 x2). | Cloud GPU |
| `waste_segregator_kaggle_master.ipynb` | Ready-to-run Kaggle notebook for 100-epoch master training with validation plots and model export. | Kaggle / Colab |

## Typical Workflow

1. **Dataset Synthesis & Balancing:**
   ```bash
   python3 training/build_15class_master_dataset.py
   python3 training/boost_dataset_balance.py
   ```

2. **Package for Remote Cloud GPU (Optional):**
   ```bash
   python3 training/package_dataset.py
   ```

3. **Train Locally with Apple Silicon (MPS) or NVIDIA CUDA:**
   ```bash
   python3 training/train_15class_master.py
   ```

4. **Fine-Tune Minority Classes:**
   ```bash
   python3 training/finetune_balanced_model.py
   ```
