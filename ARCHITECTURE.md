# Garbage Waste Segregator - Architecture Overview

## System Components

```
Garbage Waste Segregator/
│
├── backend/          Flask REST API (port 5000)
│   ├── app.py        API server with 12 endpoints
│   └── run.sh        Setup & management script
│
├── frontend/         React SPA (port 3000)
│   └── src/
│       ├── App.js     Router configuration (6 pages)
│       ├── components/  15 UI components
│       └── services/    API client with error handling
│
├── training/        Training pipeline manager
│   ├── training_pipeline.js  Node.js orchestrator
│   └── run_pipeline.sh      Shell wrapper
│
├── datasets/        YOLO format training data
│   ├── taco_yolo/   Base dataset (~463 images, 10 classes)
│   └── taco_plus_waste_v1/  Combined dataset (~1193 images)
│
└── runs/            Training experiment directories
    └── detect/runs/garbage/
        ├── yolo11n_fresh/    Experiment 1 (completed)
        └── yolo11n_768_experiment/  Experiment 2 (in progress)
```

## Data Flow Diagram

```
User → Frontend (React) ←→ Backend API (Flask)
                          ↓
                    Dataset Files
                        ↓
                  Backend Endpoints
                        ↓
              Pre-trained Model (models/yolo11n.pt)
```

## Communication Protocols

| Direction | Protocol | Port | Content |
|-----------|----------|------|---------|
| Frontend → Backend | HTTP GET/POST | 5000 | JSON requests |
| Backend → Datasets | HTTP Static | - | Image files |
| Model → Prediction | Ultralytics YOLO | - | Binary model load |

## Training Pipeline Flow

```
1. validateEnvironment()
      ↓
2. prepareDatasets()
      ↓
3. runTraining(baseline: 50 epochs, 640px)
      ↓
4. runTraining(second: 100 epochs, 768px)
      ↓
5. generateSummaryReport()
```
