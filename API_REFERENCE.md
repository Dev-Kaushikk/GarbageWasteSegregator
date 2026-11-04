# Garbage Waste Segregator - Key API Endpoints Reference

## Endpoint Index

### Data Access Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check status |
| GET | `/api/datasets` | List all available datasets |
| GET | `/api/datasets/{id}/stats` | Detailed statistics per dataset |
| GET | `/api/datasets/{id}/images/{split}/{filename}` | Serve training image |
| GET | `/api/datasets/{id}/labels/{split}/{filename}` | Serve annotation file |

### Training Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/training/runs` | List all training runs |
| GET | `/api/training/runs/{id}/status` | Real-time run status |
| GET | `/api/training/runs/{id}/predictions` | Saved predictions list |

### File Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/files/list/{directory}` | Files in directory |
| GET | `/api/files/tree/{directory}` | Full file tree structure |

### Prediction Endpoint
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/predict` | Run YOLO model on uploaded image |

## Example API Calls

```bash
# Health check
curl http://localhost:5000/api/health

# List datasets
curl http://localhost:5000/api/datasets

# Dataset stats
curl http://localhost:5000/api/datasets/taco_yolo/stats

# Serve an image
curl http://localhost:5000/api/datasets/taco_yolo/images/train/taco_0.jpg -o train_sample.jpg

# List training runs
curl http://localhost:5000/api/training/runs

# Get training status
curl http://localhost:5000/api/training/runs/yolo11n_fresh/status

# Run prediction with base64 image
curl -X POST http://localhost:5000/api/predict \
  -F "image=@uploaded_image.jpg"
```

## Response Formats

### Datasets List Response
```json
{
  "datasets": [
    {
      "id": "taco_yolo",
      "name": "taco_yolo",
      "description": "Base TACO dataset converted to YOLO format",
      "path": "/.../datasets/taco_yolo",
      "type": "image-classification",
      "splits": { "train": {"images": 80, "objects": 200}, ... },
      "classes": ["plastic_bottle", ...],
      "total_images": 463,
      "class_count": 10
    }
  ],
  "total": 2
}
```

### Training Runs Response
```json
{
  "runs": [
    {
      "id": "yolo11n_fresh",
      "name": "Yolo11n Fresh",
      "path": ".../yolo11n_fresh",
      "status": "completed",
      "final_metrics": {
        "metrics/mAP50(B)": 0.33287,
        "metrics/precision(B)": 0.33287,
        ...
      },
      "weights": ".../best.pt",
      "config": ".../args.yaml"
    }
  ],
  "total": 2
}
```

### Prediction Response
```json
{
  "success": true,
  "predictions": [
    {
      "class_id": 6,
      "class_name": "glass",
      "confidence": 0.969,
      "bounding_box": { "x1": 0.47, "y1": 0.47, "x2": 0.82, "y2": 0.68 },
      "area": 0.039
    }
  ],
  "total_detections": 3
}
```
