# WasteSegregator AI

An autonomous computer vision system for real-time waste localization, 15-class material classification, and automated circular segregation recommendations.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)
![React](https://img.shields.io/badge/react-18.x-61dafb.svg)
![YOLO11](https://img.shields.io/badge/yolo-11n-00FFFF.svg)
![Database](https://img.shields.io/badge/database-SQLite%203-003B57.svg)

---

## 🚀 Features

### Core Intelligence
- **Real-Time Multi-Object Localization**: YOLO11 neural detector locates and segments multiple waste items in cluttered scenes.
- **15-Class Municipal Taxonomy**: Standardized categorization across Plastics, Fibers, Metals, Organics, Polystyrene, Textiles, and E-Waste.
- **Tri-Model Consensus Ensemble**: Weighted Boxes Fusion (WBF) combines flagship, high-precision, and Kaggle-trained checkpoints to maximize reliability.
- **Deterministic Segregation Engine**: Rule-based intelligence maps detected items to 6 circular disposal streams (Recycle, Compost, Reuse, RDF, Special Disposal, General Waste).
- **Audit Reports & Certificates**: Generates official municipal waste audit certificates with session timestamps, item tallies, and carbon diversion metrics.

### Modern UI/UX
- **Responsive Layout**: Clean desktop and mobile layout with unified container spacing and navigation.
- **Live Camera Scanner**: Real-time webcam frame ingestion with interactive threshold controls and voice guidance.
- **Interactive Analytics**: Interactive Chart.js visualizers for material recovery ratios, diversion rates, and longitudinal history.
- **Session Pagination**: SQLite-backed history table with 10–15 items/page pagination, status filtering, and modal dossiers.

---

## 🛠️ Technology Stack

- **Deep Learning**: Ultralytics YOLO11 (PyTorch 2.x backend)
- **Hardware Acceleration**: Apple Metal Performance Shaders (MPS) / NVIDIA CUDA
- **Backend API**: Python 3.10+, Flask 3.x, CORS
- **Database**: SQLite 3 (ACID-compliant local persistence with WAL mode)
- **Frontend UI**: React 18, React Router v6, Tailwind CSS
- **Iconography & Visuals**: Lucide React, Chart.js, React-Chartjs-2
- **Audio Feedback**: Web Speech API for automated voice guidance

---

## 📋 Prerequisites

- **Python**: 3.10 or higher
- **Node.js**: 18.x or higher with `npm`
- **Modern Web Browser**: Chrome, Safari, Edge, or Firefox

---

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/GarbageWasteSegregator.git
cd GarbageWasteSegregator
```

### 2. Launch Services (1-Click)
Run the launcher script to automatically configure virtual environments, verify weights, and start both the backend API and frontend dev server:
```bash
./start.sh
```

### 3. Access Applications
- **Frontend Web UI**: [http://localhost:3000](http://localhost:3000)
- **Backend API & Status**: [http://localhost:5000](http://localhost:5000)
- **API Health Check**: [http://localhost:5000/api/health](http://localhost:5000/api/health)

### 4. Stop Services
```bash
./stop.sh
```

---

## 📁 Project Structure

```text
GarbageWasteSegregator/
├── backend/                  # Flask REST API, SQLite persistence & consensus engine
│   ├── app.py                # REST endpoints, CORS & dashboard renderer
│   ├── model_manager.py      # YOLO loader & Tri-Model Consensus (WBF)
│   ├── recommendation_engine.py # Deterministic circular segregation rules
│   ├── db.py                 # SQLite schema, queries & analytics
│   ├── waste_knowledge.py    # Disposal actions, hazard levels & eco advice
│   └── requirements.txt      # Python dependencies
├── frontend/                 # React 18 client application
│   ├── src/
│   │   ├── pages/            # Home, Scanner, Dashboard, History, Benchmarks, Settings, About
│   │   ├── components/       # Navbar, Layout, EcoImpactCard, Modals
│   │   ├── services/         # Axios API client
│   │   └── utils/            # 15-class taxonomy constants & formatters
│   └── package.json          # Node dependencies & React scripts
├── training/                 # Dataset preparation, augmentation & training pipeline
│   ├── build_15class_master_dataset.py # Master 15-class dataset consolidator
│   ├── augment_minority_classes.py     # Class-aware augmentation
│   ├── boost_dataset_balance.py        # Dataset rebalancer
│   ├── train_15class_master.py         # 100-Epoch local training runner (MPS/CUDA)
│   ├── finetune_balanced_model.py      # Fine-tuning runner
│   └── waste_segregator_kaggle_master.ipynb # Kaggle GPU training notebook
├── models/                   # Model weights (.pt), metrics & confusion matrix
├── screenshots/              # Application screenshots & UI previews
├── test_images/              # Verification sample imagery
├── start.sh                  # 1-Click launcher
├── stop.sh                   # 1-Click shutdown
├── LICENSE                   # MIT License
└── README.md                 # Project documentation
```

---

## 📊 15-Class Target Taxonomy

| ID | Class Label | Category | Designated Disposal Stream |
|:--:|---|---|---|
| `#0` | Plastic Bottle | Plastics | Blue Bin (Recyclable) |
| `#1` | Plastic Wrapper | Plastics | Grey Bin (RDF / Energy Recovery) |
| `#2` | Plastic Bag | Plastics | Soft Plastic Depot |
| `#3` | Plastic Container | Plastics | Blue Bin (Recyclable) |
| `#4` | Paper | Paper & Fiber | Blue Bin (Paper Stream) |
| `#5` | Cardboard Carton | Paper & Fiber | Blue Bin (Cardboard Stream) |
| `#6` | Glass | Glass | Teal/Blue Bin (Glass Recycling) |
| `#7` | Metal Can | Metals | Blue Bin (Metals) |
| `#8` | Metal Scrap | Metals | Scrap Metal Depot |
| `#9` | Styrofoam (EPS) | Polystyrene | EPS Depot / Grey Bin |
| `#10` | Food Waste | Organics | Green Bin (Compost) |
| `#11` | Fruit / Vegetable Peel | Organics | Green Bin (Compost) |
| `#12` | Garden Waste | Organics | Green Bin (Yard Waste) |
| `#13` | Textile | Textiles | Clothing Donation / Textile Bank |
| `#14` | E-Waste | Electronics | Dedicated E-Waste Depot |

---

## 📈 Model Performance Highlights

- **Flagship Model**: YOLO11n trained for 100 epochs on 8,718 master images
- **Mean Average Precision (mAP50)**: **66.2%**
- **High-Precision Model (yolo11s)**: **72.3% Precision** @ 800px
- **Kaggle Master Peak Precision**: **77.0% Precision** @ 800px
- **Average Inference Latency**: **<100ms** on Apple Silicon (M-series MPS) / NVIDIA GPU

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Commit your changes (`git commit -m 'feat: add improvement'`)
4. Push to the branch (`git push origin feature/improvement`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
